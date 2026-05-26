// REWORK-REQUIRED RW-U1 — Dashboard is a plugin list, not home grid (dashboard.md).
import { useEffect, useState, useSyncExternalStore } from 'react'
import type { FormEvent } from 'react'
import { NavLink, Route, Routes } from 'react-router-dom'

import { isMantleEmbedMode } from './mantle/embedMode'
import { InstallPrompt, PluginFrame } from './mantle'
import { MantleEmbedApp } from './MantleEmbedApp'
import { usePlugins } from './usePlugins'

const homeTab = { key: 'home', label: 'Home', path: '/' } as const
const settingsTab = { key: 'settings', label: 'Settings', path: '/settings' } as const

type AuthProvider = 'builtin' | 'external'

interface AuthSettings {
  provider: AuthProvider
  external_verify_url: string | null
}

interface SettingsResponse {
  auth: AuthSettings
}

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

function SettingsView() {
  const [provider, setProvider] = useState<AuthProvider>('builtin')
  const [externalVerifyUrl, setExternalVerifyUrl] = useState('')
  const [status, setStatus] = useState('Loading settings...')
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    let cancelled = false

    async function loadSettings(): Promise<void> {
      try {
        const response = await fetch('/api/settings')
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`)
        }
        const payload = (await response.json()) as SettingsResponse
        if (cancelled) {
          return
        }
        setProvider(payload.auth.provider)
        setExternalVerifyUrl(payload.auth.external_verify_url ?? '')
        setStatus('Settings loaded.')
      } catch (error) {
        if (!cancelled) {
          setStatus(`Failed to load settings: ${error instanceof Error ? error.message : 'unknown error'}`)
        }
      }
    }

    void loadSettings()
    return () => {
      cancelled = true
    }
  }, [])

  async function saveSettings(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault()
    setSaving(true)
    setStatus('Saving...')
    try {
      const response = await fetch('/api/settings', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          auth: {
            provider,
            external_verify_url: externalVerifyUrl.trim() || null,
          },
        }),
      })
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      const payload = (await response.json()) as SettingsResponse
      setProvider(payload.auth.provider)
      setExternalVerifyUrl(payload.auth.external_verify_url ?? '')
      setStatus('Auth provider settings saved.')
    } catch (error) {
      setStatus(`Failed to save settings: ${error instanceof Error ? error.message : 'unknown error'}`)
    } finally {
      setSaving(false)
    }
  }

  return (
    <main className="mx-auto flex w-full max-w-3xl px-4 pb-28 pt-8 md:px-8 md:pb-16">
      <section className="w-full rounded-lg border border-[var(--hearth-surface)] bg-[var(--hearth-surface)] p-5 shadow-sm">
        <h1 className="text-xl font-semibold text-[var(--hearth-fg)]">Settings</h1>
        <form className="mt-5 space-y-5" onSubmit={(event) => void saveSettings(event)}>
          <fieldset className="space-y-3">
            <legend className="text-sm font-medium text-[var(--hearth-fg)]">Auth provider</legend>
            <label className="flex items-start gap-3 rounded-md border border-[color-mix(in_srgb,var(--hearth-muted)_35%,transparent)] p-3 text-sm">
              <input
                type="radio"
                name="auth-provider"
                value="builtin"
                checked={provider === 'builtin'}
                onChange={() => setProvider('builtin')}
                className="mt-1"
              />
              <span>
                <span className="block font-medium text-[var(--hearth-fg)]">Built-in Hearth users</span>
                <span className="block text-[var(--hearth-muted)]">Use the local hearth-users verify service.</span>
              </span>
            </label>
            <label className="flex items-start gap-3 rounded-md border border-[color-mix(in_srgb,var(--hearth-muted)_35%,transparent)] p-3 text-sm">
              <input
                type="radio"
                name="auth-provider"
                value="external"
                checked={provider === 'external'}
                onChange={() => setProvider('external')}
                className="mt-1"
              />
              <span>
                <span className="block font-medium text-[var(--hearth-fg)]">External verify URL</span>
                <span className="block text-[var(--hearth-muted)]">Use a custom service that returns Hearth user claims.</span>
              </span>
            </label>
          </fieldset>

          <label className="block text-sm font-medium text-[var(--hearth-fg)]">
            Verify URL
            <input
              type="url"
              value={externalVerifyUrl}
              onChange={(event) => setExternalVerifyUrl(event.target.value)}
              placeholder="https://auth.example.test/verify"
              className="mt-2 block w-full rounded-md border border-[color-mix(in_srgb,var(--hearth-muted)_35%,transparent)] bg-[var(--hearth-bg)] px-3 py-2 text-sm text-[var(--hearth-fg)] outline-none focus:border-[var(--hearth-accent)]"
            />
          </label>

          {provider === 'external' && (
            <p className="rounded-md border border-[color-mix(in_srgb,var(--hearth-accent)_45%,transparent)] bg-[color-mix(in_srgb,var(--hearth-accent)_12%,transparent)] p-3 text-sm text-[var(--hearth-fg)]">
              If the external service is unreachable or misconfigured, Hearth verify fails closed with HTTP 503.
            </p>
          )}

          <div className="flex flex-wrap items-center gap-3">
            <button
              type="submit"
              disabled={saving}
              className="rounded-md bg-[var(--hearth-accent)] px-4 py-2 text-sm font-medium text-[var(--hearth-accent-fg)] disabled:cursor-not-allowed disabled:opacity-60"
            >
              {saving ? 'Saving...' : 'Save'}
            </button>
            <p role="status" className="text-sm text-[var(--hearth-muted)]">
              {status}
            </p>
          </div>
        </form>
      </section>
    </main>
  )
}

// PluginFrame is imported from ./mantle/PluginFrame — see src/mantle/.

function ShellApp() {
  const isDesktop = useDesktopLayout()
  const plugins = usePlugins()

  const navTabs = [
    homeTab,
    ...plugins.map((plugin) => ({ key: plugin.slug, label: plugin.name, path: `/${plugin.slug}` })),
    settingsTab,
  ]

  return (
    <div className="min-h-svh bg-[var(--hearth-bg)] font-sans text-[var(--hearth-fg)]">
      {isDesktop ? (
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
        <Route path="/settings" element={<SettingsView />} />
        {plugins.map((plugin) => (
          <Route key={plugin.slug} path={`/${plugin.slug}`} element={<PluginFrame slug={plugin.slug} name={plugin.name} active={true} />} />
        ))}
      </Routes>

      <InstallPrompt />

      {!isDesktop && (
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
      )}
    </div>
  )
}

function App() {
  if (isMantleEmbedMode()) {
    return <MantleEmbedApp />
  }

  return <ShellApp />
}

export default App
