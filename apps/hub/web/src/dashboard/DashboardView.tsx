import { useSyncExternalStore } from 'react'

import './dashboard.css'
import { Grid } from './Grid'
import { useDashboardData } from './useDashboardData'

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

/** Home dashboard at `/` — docs/design/dashboard.md */
export function DashboardView() {
  const isDesktop = useDesktopLayout()
  const columns = isDesktop ? 8 : 4
  const { layout, tiles, strip, plugins, loading, offline, error, refresh } = useDashboardData()

  if (loading && !layout) {
    return (
      <main className="dashboard-main" data-testid="dashboard-loading">
        <p className="dashboard-loading-text">Loading dashboard…</p>
      </main>
    )
  }

  if (!layout) {
    return (
      <main className="dashboard-main" data-testid="dashboard-error">
        <p className="dashboard-error-text">{error ?? 'Could not load dashboard.'}</p>
      </main>
    )
  }

  return (
    <main className="dashboard-main" data-testid="dashboard-view">
      <Grid
        layout={layout}
        tiles={tiles}
        strip={strip}
        plugins={plugins}
        columns={columns}
        offline={offline}
        onStripDismissed={refresh}
      />
    </main>
  )
}
