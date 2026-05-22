// REWORK-REQUIRED RW-U1 — Dashboard is a plugin list, not home grid (dashboard.md).
// REWORK-REQUIRED RW-U2 — Settings chrome route missing (mantle-ui.md). T-FR-0001-04.
import { useEffect, useMemo, useState, useSyncExternalStore } from 'react'
import { NavLink, Route, Routes, useLocation } from 'react-router-dom'

import { isMantleEmbedMode } from './mantle/embedMode'
import { InstallPrompt, PluginFrame } from './mantle'
import { MantleEmbedApp } from './MantleEmbedApp'
import { usePlugins } from './usePlugins'
import { ChromeSlot } from './shell/ChromeSlot'
import { useChromeSlotRegistry } from './shell/useChromeSlotRegistry'
import { usePostMessageBridge } from './shell/usePostMessageBridge'

const homeTab = { key: 'home', label: 'Home', path: '/' } as const

function useDesktopLayout(): boolean {
  return useSyncExternalStore(
    (onStoreChange) => {
      const mediaQuery = window.matchMedia('(min-width: 768px)')
      mediaQuery.addEventListener('change', onStoreChange)
      return () => mediaQuery.removeEventListener('change', onStoreChange)
    },
    () => window.matchMedia('(min-width: 768px)').matches,
  )
}

function DashboardView() {
  const [status, setStatus] = useState<string | null>(null)
  const plugins = usePlugins()

  function decodeBase64Url(base64Url: string): ArrayBuffer {
    const padded = `${base64Url}${'='.repeat((4 - (base64Url.length % 4)) % 4)}`
    const base64 = padded.replace(/-/g, '+').replace(/_/g, '/')
    const raw = window.atob(base64)
    const output = new Uint8Array(raw.length)
    for (let i = 0; i < raw.length; i += 1) {
      output[i] = raw.charCodeAt(i)
    }
    return output.slice().buffer
  }

  function isStandalonePwa(): boolean {
    return (
      window.matchMedia('(display-mode: standalone)').matches ||
      ('standalone' in navigator && Boolean((navigator as Navigator & { standalone?: boolean }).standalone))
    )
  }

  async function ensurePushSubscription(): Promise<void> {
    if (!('Notification' in window)) {
      if (!isStandalonePwa()) {
        throw new Error(
          'Web Push on iPhone requires opening Hearth from the Home Screen icon (Add to Home Screen first), not from Safari.',
        )
      }
      throw new Error('Notifications are not supported in this browser.')
    }
    if (!('serviceWorker' in navigator)) {
      throw new Error('Service workers are not supported in this browser.')
    }

    let permission = Notification.permission
    if (permission === 'default') {
      permission = await Notification.requestPermission()
    }
    if (permission !== 'granted') {
      throw new Error(`Notification permission is ${permission}.`)
    }

    const registration = await navigator.serviceWorker.ready
    const existing = await registration.pushManager.getSubscription()
    if (existing) {
      const response = await fetch('/api/push/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(existing.toJSON()),
      })
      if (!response.ok) {
        throw new Error(`Failed to sync subscription: HTTP ${response.status}`)
      }
      return
    }

    const keyResponse = await fetch('/api/push/vapid-public-key')
    if (!keyResponse.ok) {
      throw new Error(`Failed to load VAPID key: HTTP ${keyResponse.status}`)
    }
    const keyPayload = (await keyResponse.json()) as { publicKey?: string }
    if (!keyPayload.publicKey) {
      throw new Error('VAPID key payload was empty.')
    }

    const subscription = await registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: decodeBase64Url(keyPayload.publicKey),
    })

    const subscribeResponse = await fetch('/api/push/subscribe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(subscription.toJSON()),
    })
    if (!subscribeResponse.ok) {
      throw new Error(`Failed to store subscription: HTTP ${subscribeResponse.status}`)
    }
  }

  async function sendTestNotification(): Promise<void> {
    setStatus('Requesting notification permission...')
    try {
      await ensurePushSubscription()
      setStatus('Sending...')
      const response = await fetch('/api/push/test', { method: 'POST' })
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      const data = (await response.json()) as {
        attempted: number
        sent: number
        remaining: number
        error?: string | null
      }
      if (data.error && data.sent === 0) {
        throw new Error(data.error)
      }
      const suffix = data.error ? ` Last error: ${data.error}` : ''
      setStatus(`Sent ${data.sent}/${data.attempted}. Active subscriptions: ${data.remaining}.${suffix}`)
    } catch (error) {
      setStatus(`Failed to send test notification: ${error instanceof Error ? error.message : 'unknown error'}`)
    }
  }

  return (
    <main className="mx-auto flex min-h-[60svh] w-full max-w-3xl items-center px-4 pb-28 pt-8 md:px-8 md:pb-16">
      <section className="w-full rounded-2xl border border-[var(--hearth-surface)] bg-[var(--hearth-surface)] p-6 shadow-sm">
        <h1 className="text-2xl font-semibold text-[var(--hearth-fg)]">Hearth</h1>
        <p className="mt-3 text-[var(--hearth-muted)]">
          Mantle shell — registry-driven navigation. Install plugins via the hub; tabs appear when enabled.
        </p>
        {plugins.length === 0 ? (
          <p className="mt-3 text-sm text-[var(--hearth-muted)]">No enabled plugins in the registry yet.</p>
        ) : (
          <ul className="mt-3 list-inside list-disc text-sm text-[var(--hearth-muted)]">
            {plugins.map((plugin) => (
              <li key={plugin.slug}>
                <NavLink to={`/${plugin.slug}`} className="underline">
                  {plugin.name}
                </NavLink>
              </li>
            ))}
          </ul>
        )}
        <button
          type="button"
          onClick={() => {
            void sendTestNotification()
          }}
          className="mt-5 rounded-lg bg-[var(--hearth-accent)] px-4 py-2 text-sm font-medium text-[var(--hearth-bg)]"
        >
          Send test notification
        </button>
        {status && <p className="mt-3 text-sm text-[var(--hearth-muted)]">{status}</p>}
      </section>
    </main>
  )
}

// PluginFrame is imported from ./mantle/PluginFrame — see src/mantle/.

function activePluginSlug(pathname: string, pluginSlugs: string[]): string | null {
  const match = pathname.match(/^\/([^/]+)/)
  if (!match) return null
  const slug = match[1]
  return pluginSlugs.includes(slug) ? slug : null
}

function App() {
  if (isMantleEmbedMode()) {
    return <MantleEmbedApp />
  }

  const location = useLocation()
  const isDesktop = useDesktopLayout()
  const plugins = usePlugins()
  const pluginSlugs = useMemo(() => plugins.map((p) => p.slug), [plugins])
  const activeSlug = activePluginSlug(location.pathname, pluginSlugs)
  const activePlugin = activeSlug ? plugins.find((p) => p.slug === activeSlug) : undefined
  const isAppMode = activeSlug !== null
  const navTabs = [homeTab, ...plugins.map((plugin) => ({ key: plugin.slug, label: plugin.name, path: `/${plugin.slug}` }))]

  const bridge = usePostMessageBridge()
  const chrome = useChromeSlotRegistry(bridge, activeSlug)
  const [pluginTitle, setPluginTitle] = useState<string | null>(null)

  useEffect(() => {
    setPluginTitle(null)
  }, [activeSlug])

  useEffect(() => {
    const unsub = bridge.subscribe('hearth.title', (msg) => {
      document.title = `${msg.title} — Hearth`
      if (activeSlug) setPluginTitle(msg.title)
    })
    return unsub
  }, [bridge, activeSlug])

  const shellClass = [
    'shell',
    'min-h-svh',
    'bg-[var(--hearth-bg)]',
    'font-sans',
    'text-[var(--hearth-fg)]',
    chrome.hasChromeSlots ? 'has-chrome-slots' : '',
    isAppMode ? 'shell--app-mode' : '',
  ]
    .filter(Boolean)
    .join(' ')

  return (
    <div className={shellClass}>
      {isDesktop && isAppMode ? (
        <header
          aria-label="Mantle top bar"
          className="top-bar border-b border-[var(--hearth-surface)] bg-[var(--hearth-surface)]"
        >
          <nav className="mx-auto flex h-16 max-w-6xl items-center gap-3 px-6">
            <NavLink to="/" className="home-back" aria-label="Home">
              ‹
            </NavLink>
            <h1 className="min-w-0 truncate text-lg font-semibold">
              {pluginTitle ?? activePlugin?.name ?? activeSlug}
            </h1>
            <span className="top-bar-spacer" />
            <ChromeSlot
              slot="top"
              items={chrome.topItems}
              isDesktop
              onInvoke={(id, itemId) => chrome.invoke('top', id, itemId)}
            />
            <button type="button" className="text-sm text-[var(--hearth-muted)]" aria-label="Account">
              User
            </button>
          </nav>
        </header>
      ) : isDesktop ? (
        <header aria-label="Mantle top bar" className="border-b border-[var(--hearth-surface)] bg-[var(--hearth-surface)]">
          <nav className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
            <div className="flex items-center gap-3">
              <img src="/logo.svg" alt="Hearth" className="h-6 w-6" />
              <span className="font-semibold">Hearth</span>
            </div>
            <ul className="flex items-center gap-4 text-sm">
              {navTabs.map((tab) => (
                <li key={tab.key}>
                  <NavLink to={tab.path} className="rounded-md px-3 py-2 hover:bg-[var(--hearth-bg)]" end={tab.path === '/'}>
                    {tab.label}
                  </NavLink>
                </li>
              ))}
            </ul>
          </nav>
        </header>
      ) : isAppMode ? (
        <header
          aria-label="Mantle top bar"
          className="top-bar border-b border-[var(--hearth-surface)] bg-[var(--hearth-bg)] px-4 pb-3 pt-[calc(0.75rem+var(--hearth-safe-top))]"
        >
          <NavLink to="/" className="home-back" aria-label="Home">
            ‹
          </NavLink>
          <h1 className="min-w-0 flex-1 truncate text-lg font-semibold">
            {pluginTitle ?? activePlugin?.name ?? activeSlug}
          </h1>
          <ChromeSlot
            slot="top"
            items={chrome.topItems}
            isDesktop={false}
            onInvoke={(id, itemId) => chrome.invoke('top', id, itemId)}
          />
          <button type="button" className="text-sm text-[var(--hearth-muted)]" aria-label="Account">
            User
          </button>
        </header>
      ) : (
        <header className="border-b border-[var(--hearth-surface)] bg-[var(--hearth-bg)] px-4 pb-3 pt-[calc(0.75rem+var(--hearth-safe-top))]">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">Hearth</h2>
            <span className="text-sm text-[var(--hearth-muted)]">User</span>
          </div>
        </header>
      )}

      <Routes>
        <Route path="/" element={<DashboardView />} />
        {plugins.map((plugin) => (
          <Route key={plugin.slug} path={`/${plugin.slug}`} element={<PluginFrame slug={plugin.slug} name={plugin.name} active={true} />} />
        ))}
      </Routes>

      <InstallPrompt />

      {!isDesktop && isAppMode ? (
        <nav
          aria-label="Shell navigation"
          className="bottom-bar bottom-bar--app fixed inset-x-0 bottom-0 border-t border-[var(--hearth-surface)] bg-[var(--hearth-surface)] pb-[calc(0.5rem+var(--hearth-safe-bottom))] pt-2"
        >
          <div className="nav-pinned nav-pinned--start">
            <NavLink to="/" className="block rounded-lg px-3 py-3 text-center text-xs text-[var(--hearth-muted)] hover:bg-[var(--hearth-bg)]">
              Home
            </NavLink>
          </div>
          <ChromeSlot
            slot="bottom"
            items={chrome.bottomItems}
            isDesktop={false}
            onInvoke={(id, itemId) => chrome.invoke('bottom', id, itemId)}
          />
          <div className="nav-pinned nav-pinned--end">
            <button
              type="button"
              className="rounded-lg px-3 py-3 text-xs text-[var(--hearth-muted)]"
              aria-label="Settings"
            >
              ⚙
            </button>
          </div>
        </nav>
      ) : !isDesktop ? (
        <nav
          aria-label="Mantle bottom tabs"
          className="fixed inset-x-0 bottom-0 border-t border-[var(--hearth-surface)] bg-[var(--hearth-surface)] px-2 pb-[calc(0.5rem+var(--hearth-safe-bottom))] pt-2"
        >
          <ul
            className="mx-auto grid max-w-md gap-1"
            style={{ gridTemplateColumns: `repeat(${Math.min(navTabs.length, 4)}, minmax(0, 1fr))` }}
          >
            {navTabs.slice(0, 4).map((tab) => (
              <li key={tab.key}>
                <NavLink
                  to={tab.path}
                  end={tab.path === '/'}
                  className="block rounded-lg px-3 py-3 text-center text-xs text-[var(--hearth-muted)] hover:bg-[var(--hearth-bg)]"
                >
                  {tab.label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      ) : null}
    </div>
  )
}

export default App
