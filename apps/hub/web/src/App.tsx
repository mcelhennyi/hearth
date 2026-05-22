// REWORK-REQUIRED RW-U2 — Settings chrome route missing (mantle-ui.md). Partial: modal only.
import { useEffect, useMemo, useState, useSyncExternalStore } from 'react'
import { NavLink, Route, Routes, useLocation } from 'react-router-dom'

import { DashboardView } from './dashboard/DashboardView'
import { isMantleEmbedMode } from './mantle/embedMode'
import { InstallPrompt, PluginFrame } from './mantle'
import { MantleEmbedApp } from './MantleEmbedApp'
import { usePlugins } from './usePlugins'
import { ChromeSlot } from './shell/ChromeSlot'
import { SettingsModal, SettingsTrigger } from './shell/SettingsModal'
import { SettingsProvider } from './shell/SettingsContext'
import { useChromeSlotRegistry } from './shell/useChromeSlotRegistry'
import { usePostMessageBridge } from './shell/usePostMessageBridge'
import { ThemeProvider } from './theme/ThemeProvider'

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
    <SettingsProvider>
      <ThemeProvider bridge={bridge}>
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
                  <li>
                    <SettingsTrigger
                      variant="desktop-top"
                      className="rounded-md px-3 py-2 text-[var(--hearth-muted)] hover:bg-[var(--hearth-bg)]"
                    />
                  </li>
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
              <Route
                key={plugin.slug}
                path={`/${plugin.slug}`}
                element={
                  <PluginFrame
                    slug={plugin.slug}
                    name={plugin.name}
                    active={activeSlug === plugin.slug}
                    bridge={bridge}
                  />
                }
              />
            ))}
          </Routes>

          <InstallPrompt />

          {!isDesktop && isAppMode ? (
            <nav
              aria-label="Shell navigation"
              className="bottom-bar bottom-bar--app fixed inset-x-0 bottom-0 border-t border-[var(--hearth-surface)] bg-[var(--hearth-surface)] pb-[calc(0.5rem+var(--hearth-safe-bottom))] pt-2"
            >
              <div className="nav-pinned nav-pinned--start">
                <NavLink
                  to="/"
                  className="block rounded-lg px-3 py-3 text-center text-xs text-[var(--hearth-muted)] hover:bg-[var(--hearth-bg)]"
                >
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
                <SettingsTrigger
                  variant="mobile-icon"
                  className="flex min-h-11 min-w-11 items-center justify-center rounded-lg text-lg hover:bg-[var(--hearth-bg)]"
                  aria-label="Settings"
                />
              </div>
            </nav>
          ) : !isDesktop ? (
            <nav
              aria-label="Mantle bottom tabs"
              className="fixed inset-x-0 bottom-0 border-t border-[var(--hearth-surface)] bg-[var(--hearth-surface)] px-2 pb-[calc(0.5rem+var(--hearth-safe-bottom))] pt-2"
            >
              <ul
                className="mx-auto grid max-w-md gap-1"
                style={{ gridTemplateColumns: `repeat(${Math.min(navTabs.length + 1, 5)}, minmax(0, 1fr))` }}
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
                <li className="flex justify-center">
                  <SettingsTrigger
                    variant="mobile-icon"
                    className="flex min-h-11 min-w-11 items-center justify-center rounded-lg text-lg hover:bg-[var(--hearth-bg)]"
                    aria-label="Settings"
                  />
                </li>
              </ul>
            </nav>
          ) : null}

          {isDesktop && (
            <div className="fixed inset-x-0 bottom-0 border-t border-[var(--hearth-surface)] bg-[var(--hearth-surface)] px-6 py-2">
              <div className="mx-auto flex max-w-6xl items-center justify-end">
                <SettingsTrigger
                  variant="desktop-bottom"
                  className="rounded-md px-3 py-2 text-sm text-[var(--hearth-muted)] hover:bg-[var(--hearth-bg)]"
                />
              </div>
            </div>
          )}

          <SettingsModal isDesktop={isDesktop} />
        </div>
      </ThemeProvider>
    </SettingsProvider>
  )
}

export default App
