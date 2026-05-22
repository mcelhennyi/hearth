// REWORK-REQUIRED RW-U2 — Settings chrome route missing (mantle-ui.md). T-FR-0006-04.
import { useEffect, useSyncExternalStore } from 'react'
import { NavLink, Route, Routes } from 'react-router-dom'

import { DashboardView } from './dashboard/DashboardView'
import { isMantleEmbedMode } from './mantle/embedMode'
import { InstallPrompt, PluginFrame } from './mantle'
import { MantleEmbedApp } from './MantleEmbedApp'
import { usePlugins } from './usePlugins'
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

function App() {
  if (isMantleEmbedMode()) {
    return <MantleEmbedApp />
  }

  const isDesktop = useDesktopLayout()
  const plugins = usePlugins()
  const navTabs = [homeTab, ...plugins.map((plugin) => ({ key: plugin.slug, label: plugin.name, path: `/${plugin.slug}` }))]

  const bridge = usePostMessageBridge()
  useEffect(() => {
    const unsub = bridge.subscribe('hearth.title', (msg) => {
      document.title = `${msg.title} — Hearth`
    })
    return unsub
  }, [bridge])

  return (
    <div className="flex min-h-svh flex-col bg-[var(--hearth-bg)] font-sans text-[var(--hearth-fg)]">
      {isDesktop ? (
        <header aria-label="Mantle top bar" className="shrink-0 border-b border-[var(--hearth-surface)] bg-[var(--hearth-surface)]">
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
        <header className="shrink-0 border-b border-[var(--hearth-surface)] bg-[var(--hearth-bg)] px-4 pb-3 pt-[calc(0.75rem+var(--hearth-safe-top))]">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">Hearth</h2>
            <span className="text-sm text-[var(--hearth-muted)]">User</span>
          </div>
        </header>
      )}

      <div className="flex min-h-0 flex-1 flex-col">
        <Routes>
          <Route path="/" element={<DashboardView />} />
          {plugins.map((plugin) => (
            <Route
              key={plugin.slug}
              path={`/${plugin.slug}`}
              element={<PluginFrame slug={plugin.slug} name={plugin.name} active={true} />}
            />
          ))}
        </Routes>
      </div>

      <InstallPrompt />

      {!isDesktop && (
        <nav
          aria-label="Mantle bottom tabs"
          className="fixed inset-x-0 bottom-0 shrink-0 border-t border-[var(--hearth-surface)] bg-[var(--hearth-surface)] px-2 pb-[calc(0.5rem+var(--hearth-safe-bottom))] pt-2"
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

export default App
