import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { useEffect } from 'react'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import 'fake-indexeddb/auto'

import { EditChrome } from './EditChrome'
import { EditGrid } from './EditGrid'
import { EditModeProvider, useEditMode } from './EditModeContext'
import type { DashboardLayout, PluginRegistryEntry, SystemTile } from '../types'

const LAYOUT: DashboardLayout = {
  version: 1,
  columns: 4,
  blocks: [
    { id: 'b-a', type: 'app-shortcut', plugin: 'alpha', x: 0, y: 0, w: 1, h: 1 },
    { id: 'b-b', type: 'app-shortcut', plugin: 'beta', x: 2, y: 0, w: 1, h: 1 },
  ],
}

const TILES: SystemTile[] = []
const PLUGINS: PluginRegistryEntry[] = [
  { slug: 'alpha', name: 'Alpha', state: 'enabled', kind: 'app' },
  { slug: 'beta', name: 'Beta', state: 'enabled', kind: 'app' },
]

function mockDesktop(): void {
  vi.stubGlobal('matchMedia', (query: string) => ({
    matches: query === '(min-width: 768px)',
    media: query,
    onchange: null,
    addEventListener: () => undefined,
    removeEventListener: () => undefined,
    addListener: () => undefined,
    removeListener: () => undefined,
    dispatchEvent: () => false,
  }))
}

function mockReducedMotion(): void {
  vi.stubGlobal('matchMedia', (query: string) => ({
    matches: query === '(prefers-reduced-motion: reduce)',
    media: query,
    onchange: null,
    addEventListener: () => undefined,
    removeEventListener: () => undefined,
    addListener: () => undefined,
    removeListener: () => undefined,
    dispatchEvent: () => false,
  }))
}

function mockGridRect(): void {
  Element.prototype.getBoundingClientRect = vi.fn(function (this: Element) {
    if (this.getAttribute('data-testid') === 'dashboard-grid') {
      return {
        x: 0,
        y: 0,
        width: 400,
        height: 400,
        top: 0,
        left: 0,
        right: 400,
        bottom: 400,
        toJSON: () => ({}),
      } as DOMRect
    }
    return {
      x: 0,
      y: 0,
      width: 80,
      height: 80,
      top: 0,
      left: 0,
      right: 80,
      bottom: 80,
      toJSON: () => ({}),
    } as DOMRect
  })
}

function RegisterEditSource({ layout }: { layout: DashboardLayout }) {
  const edit = useEditMode()
  useEffect(() => {
    edit.registerSource({
      layout,
      columns: 4,
      plugins: PLUGINS,
      allTiles: TILES,
      offline: false,
      onLayoutSaved: () => undefined,
    })
    return () => edit.registerSource(null)
  }, [edit.registerSource, layout])
  return null
}

function TestHarness({
  layout = LAYOUT,
  isDesktop = false,
}: {
  layout?: DashboardLayout
  isDesktop?: boolean
}) {
  if (isDesktop) {
    mockDesktop()
  }

  return (
    <MemoryRouter>
      <EditModeProvider>
        <RegisterEditSource layout={layout} />
        <EditChrome isDashboard />
        <EditGrid
          viewLayout={layout}
          tiles={TILES}
          strip={null}
          plugins={PLUGINS}
          columns={4}
          onStripDismissed={() => undefined}
        />
      </EditModeProvider>
    </MemoryRouter>
  )
}

describe('dashboard edit mode', () => {
  beforeEach(() => {
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    mockGridRect()
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => LAYOUT,
      } as Response),
    )
  })

  afterEach(() => {
    vi.useRealTimers()
    vi.restoreAllMocks()
  })

  it('enters via 600ms long-press on the grid', async () => {
    vi.useFakeTimers()
    render(<TestHarness />)
    await act(async () => {
      await Promise.resolve()
    })

    const grid = screen.getByTestId('dashboard-grid')
    fireEvent.pointerDown(grid)
    await act(async () => {
      await vi.advanceTimersByTimeAsync(600)
    })
    expect(screen.getByTestId('dashboard-edit-done')).toBeInTheDocument()
  })

  it('enters via Edit button on desktop', () => {
    render(<TestHarness isDesktop />)
    fireEvent.click(screen.getByTestId('dashboard-edit-enter'))
    expect(screen.getByTestId('dashboard-edit-done')).toBeInTheDocument()
  })

  it('shows collision banner and disables Done when blocks overlap', () => {
    const overlapping: DashboardLayout = {
      version: 1,
      columns: 4,
      blocks: [
        { id: 'b-a', type: 'app-shortcut', plugin: 'alpha', x: 0, y: 0, w: 1, h: 1 },
        { id: 'b-b', type: 'app-shortcut', plugin: 'beta', x: 0, y: 0, w: 1, h: 1 },
      ],
    }
    render(<TestHarness layout={overlapping} isDesktop />)
    fireEvent.click(screen.getByTestId('dashboard-edit-enter'))

    expect(screen.getByTestId('dashboard-edit-collision-banner')).toHaveTextContent(/overlapping/i)
    expect(screen.getByTestId('dashboard-edit-done')).toBeDisabled()
  })

  it('uses dashed outline instead of jiggle when prefers-reduced-motion', async () => {
    mockReducedMotion()
    vi.useFakeTimers()
    render(<TestHarness />)
    await act(async () => {
      await Promise.resolve()
    })
    const grid = screen.getByTestId('dashboard-grid')
    fireEvent.pointerDown(grid)
    await act(async () => {
      await vi.advanceTimersByTimeAsync(600)
    })

    expect(grid).toHaveClass('dashboard-grid--reduced-motion')
  })

  it('starts dragging from a block long-press without reusing a stale pointer event', async () => {
    vi.useFakeTimers()
    render(<TestHarness />)
    await act(async () => {
      await Promise.resolve()
    })

    const block = screen.getByTestId('dashboard-block-wrap-b-a')
    fireEvent.pointerDown(block, { clientX: 20, clientY: 20, pointerId: 1 })
    await act(async () => {
      await vi.advanceTimersByTimeAsync(600)
    })

    expect(screen.getByTestId('dashboard-edit-done')).toBeInTheDocument()
    expect(block).toHaveClass('dashboard-block-wrap--dragging')

    fireEvent.pointerMove(block, { clientX: 140, clientY: 20, pointerId: 1 })
    expect(block).toHaveStyle({ transform: 'translate(120px, 0px)' })

    fireEvent.pointerUp(block, { clientX: 140, clientY: 20, pointerId: 1 })
    expect(block).not.toHaveClass('dashboard-block-wrap--dragging')
  })

  it('PUTs layout on Done', async () => {
    const putMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => LAYOUT,
    } as Response)
    const fetchMock = vi.fn((input: RequestInfo, init?: RequestInit) => {
      const url = typeof input === 'string' ? input : input.url
      if (url === '/api/dashboard/layout' && init?.method === 'PUT') {
        return putMock()
      }
      return Promise.resolve({ ok: true, json: async () => ({}) } as Response)
    })
    vi.stubGlobal('fetch', fetchMock)

    render(<TestHarness isDesktop />)
    fireEvent.click(screen.getByTestId('dashboard-edit-enter'))
    fireEvent.click(screen.getByTestId('dashboard-edit-done'))

    await waitFor(() => {
      expect(putMock).toHaveBeenCalledTimes(1)
    })
  })

  it('does not PUT layout on Cancel', async () => {
    mockDesktop()
    const putMock = vi.fn()
    const fetchMock = vi.fn((input: RequestInfo, init?: RequestInit) => {
      const url = typeof input === 'string' ? input : input.url
      if (url === '/api/dashboard/layout' && init?.method === 'PUT') {
        return putMock()
      }
      return Promise.resolve({ ok: true, json: async () => ({}) } as Response)
    })
    vi.stubGlobal('fetch', fetchMock)

    render(<TestHarness isDesktop />)
    fireEvent.click(screen.getByTestId('dashboard-edit-enter'))
    fireEvent.click(screen.getByTestId('dashboard-edit-cancel'))

    expect(putMock).not.toHaveBeenCalled()
    expect(screen.queryByTestId('dashboard-edit-done')).not.toBeInTheDocument()
  })
})
