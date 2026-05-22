import { useEffect, useSyncExternalStore } from 'react'

import './dashboard.css'
import './edit/edit.css'
import { BlockPicker, EditGrid, useEditMode } from './edit'
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
  const { layout, tiles, allTiles, strip, plugins, loading, offline, error, refresh, setLayout } =
    useDashboardData()
  const edit = useEditMode()

  useEffect(() => {
    if (!layout) {
      edit.registerSource(null)
      return
    }
    edit.registerSource({
      layout,
      columns,
      plugins,
      allTiles,
      offline,
      onLayoutSaved: setLayout,
    })
  }, [allTiles, columns, edit.registerSource, layout, offline, plugins, setLayout])

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
      <EditGrid
        viewLayout={layout}
        tiles={tiles}
        strip={strip}
        plugins={plugins}
        columns={columns}
        offline={offline}
        onStripDismissed={refresh}
      />
      <BlockPicker />
    </main>
  )
}
