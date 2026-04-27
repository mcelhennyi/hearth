import { useSyncExternalStore } from 'react'
import { NavLink, Navigate, Route, Routes } from 'react-router-dom'

const tabs = [
  { key: 'dashboard', label: 'Dashboard', path: '/dashboard' },
  { key: 'groceries', label: 'Groceries', path: '/groceries' },
  { key: 'recipes', label: 'Recipes', path: '/recipes' },
  { key: 'ideas', label: 'Ideas', path: '/ideas' },
] as const

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

function PlaceholderTile() {
  return (
    <main className="mx-auto flex min-h-[60svh] w-full max-w-3xl items-center px-4 pb-28 pt-8 md:px-8 md:pb-16">
      <section className="w-full rounded-2xl border border-[var(--hearth-surface)] bg-[var(--hearth-surface)] p-6 shadow-sm">
        <h1 className="text-2xl font-semibold text-[var(--hearth-fg)]">PWA-ready</h1>
        <p className="mt-3 text-[var(--hearth-muted)]">
          Mantle shell is installed with manifest, service worker, safe-area support, and placeholder routes.
        </p>
      </section>
    </main>
  )
}

function App() {
  const isDesktop = useDesktopLayout()

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
              {tabs.map((tab) => (
                <li key={tab.key}>
                  <NavLink to={tab.path} className="rounded-md px-3 py-2 hover:bg-[var(--hearth-bg)]">
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
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<PlaceholderTile />} />
        <Route path="/groceries" element={<PlaceholderTile />} />
        <Route path="/recipes" element={<PlaceholderTile />} />
        <Route path="/ideas" element={<PlaceholderTile />} />
      </Routes>

      {!isDesktop && (
        <nav
          aria-label="Mantle bottom tabs"
          className="fixed inset-x-0 bottom-0 border-t border-[var(--hearth-surface)] bg-[var(--hearth-surface)] px-2 pb-[calc(0.5rem+var(--hearth-safe-bottom))] pt-2"
        >
          <ul className="mx-auto grid max-w-md grid-cols-4 gap-1">
            {tabs.map((tab) => (
              <li key={tab.key}>
                <NavLink
                  to={tab.path}
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
