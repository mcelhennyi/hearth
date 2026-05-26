import { useEffect, useSyncExternalStore } from 'react'

import './dashboard.css'
import './edit/edit.css'
import { Strip } from './blocks/Strip'
import { BlockPicker, EditGrid, useEditMode } from './edit'
import { EmptyState } from './EmptyState'
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

  if (layout.blocks.length === 0) {
    return (
      <main className="dashboard-main" data-testid="dashboard-view">
        <div className="dashboard-scroll" data-testid="dashboard-scroll">
          {offline ? (
            <p className="dashboard-offline-badge" data-testid="dashboard-offline-badge">
              Offline — showing cached layout
            </p>
          ) : null}
          {strip ? (
            <div className="dashboard-empty-strip">
              <Strip strip={strip} columns={columns} onDismissed={refresh} />
            </div>
          ) : null}
          <EmptyState />
        </div>
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
