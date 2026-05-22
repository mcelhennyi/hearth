import { fireEvent, render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { Grid } from './Grid'
import type { DashboardLayout, PluginRegistryEntry, SystemStrip, SystemTile } from './types'

const MOBILE_LAYOUT: DashboardLayout = {
  version: 1,
  columns: 4,
  blocks: [
    { id: 'b-groceries', type: 'app-shortcut', plugin: 'groceries', x: 0, y: 0, w: 1, h: 1 },
    { id: 'default-system-ca-trust', type: 'system', x: 1, y: 0, w: 1, h: 1 },
  ],
}

const DESKTOP_LAYOUT: DashboardLayout = {
  version: 1,
  columns: 8,
  blocks: [
    { id: 'b-a', type: 'app-shortcut', plugin: 'alpha', x: 0, y: 0, w: 1, h: 1 },
    { id: 'b-b', type: 'app-shortcut', plugin: 'beta', x: 1, y: 0, w: 2, h: 1 },
    { id: 'b-w', type: 'widget', plugin: 'pantry', surface: 'count', x: 3, y: 0, w: 2, h: 2 },
  ],
}

const TILES: SystemTile[] = [
  {
    id: 'ca-trust',
    title: 'Trust local CA',
    body: 'Install certificate',
    action: { nav: '/settings#trust-ca' },
    hidden_by_user: false,
    suppressed: false,
  },
]

const PLUGINS: PluginRegistryEntry[] = [
  { slug: 'groceries', name: 'Groceries', state: 'enabled', kind: 'app' },
  { slug: 'alpha', name: 'Alpha', state: 'enabled', kind: 'app' },
  { slug: 'beta', name: 'Beta App', state: 'enabled', kind: 'app' },
]

const STRIP: SystemStrip = {
  id: 'pwa-install',
  title: 'Install Hearth',
  body: 'Add to Home Screen',
  action: { nav: '/settings' },
  dismissed: false,
}

function renderGrid(
  layout: DashboardLayout,
  columns: number,
  options?: { strip?: SystemStrip | null; offline?: boolean },
): ReturnType<typeof render> {
  return render(
    <MemoryRouter>
      <Grid
        layout={layout}
        tiles={TILES}
        strip={options?.strip ?? null}
        plugins={PLUGINS}
        columns={columns}
        offline={options?.offline}
        onStripDismissed={() => undefined}
      />
    </MemoryRouter>,
  )
}

describe('Grid snapshots', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn())
  })

  it('matches mobile grid snapshot (4 columns)', () => {
    const { container } = renderGrid(MOBILE_LAYOUT, 4)
    const grid = screen.getByTestId('dashboard-grid')
    expect(grid).toHaveStyle({ '--hearth-columns': '4' })
    expect(container.querySelector('.dashboard-grid')).toMatchSnapshot()
  })

  it('matches desktop grid snapshot (8 columns)', () => {
    const { container } = renderGrid(DESKTOP_LAYOUT, 8, { strip: STRIP })
    const grid = screen.getByTestId('dashboard-grid')
    expect(grid).toHaveStyle({ '--hearth-columns': '8' })
    expect(container.querySelector('.dashboard-scroll')).toMatchSnapshot()
  })
})

describe('Grid interactions', () => {
  it('app shortcut navigates to plugin route', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <Routes>
          <Route
            path="/"
            element={
              <Grid
                layout={MOBILE_LAYOUT}
                tiles={TILES}
                strip={null}
                plugins={PLUGINS}
                columns={4}
                onStripDismissed={() => undefined}
              />
            }
          />
          <Route path="/groceries" element={<div data-testid="plugin-page">Groceries app</div>} />
        </Routes>
      </MemoryRouter>,
    )

    fireEvent.click(screen.getByTestId('block-app-groceries'))
    expect(screen.getByTestId('plugin-page')).toBeInTheDocument()
  })
})
