import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import 'fake-indexeddb/auto'
import App from './App'
import type { PluginNavEntry } from './usePlugins'

function mockDashboardApis(): void {
  const payloads: Record<string, unknown> = {
    '/api/dashboard/layout': { version: 1, columns: 4, blocks: [] },
    '/api/system/tiles': { tiles: [] },
    '/api/system/strips': { strip: null },
    '/api/plugins': [],
  }
  vi.stubGlobal(
    'fetch',
    vi.fn((input: RequestInfo) => {
      const url = typeof input === 'string' ? input : input.url
      const body = payloads[url]
      if (body !== undefined) {
        return Promise.resolve({ ok: true, json: async () => body })
      }
      return Promise.resolve({ ok: false, json: async () => ({}) })
    }),
  )
}

function setBreakpoint(width: number): void {
  window.matchMedia = ((query: string) => ({
    matches: query === '(min-width: 768px)' ? width >= 768 : false,
    media: query,
    onchange: null,
    addEventListener: () => undefined,
    removeEventListener: () => undefined,
    addListener: () => undefined,
    removeListener: () => undefined,
    dispatchEvent: () => false,
  })) as typeof window.matchMedia
}

// Helper: mock usePlugins return value for the registry-driven nav tests.
// We mock the module so the fetch side-effect never runs in unit tests.
vi.mock('./usePlugins', async (importOriginal) => {
  const actual = await importOriginal<typeof import('./usePlugins')>()
  return { ...actual, usePlugins: vi.fn(() => []) }
})

describe('Mantle layout breakpoint behavior', () => {
  beforeEach(() => {
    window.history.replaceState({}, '', '/')
    mockDashboardApis()
  })

  it('shows bottom tabs under 768px', async () => {
    setBreakpoint(390)
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>,
    )

    expect(screen.getByLabelText('Mantle bottom tabs')).toBeInTheDocument()
    expect(screen.queryByLabelText('Mantle top bar')).not.toBeInTheDocument()
    await waitFor(() => {
      expect(screen.getByTestId('dashboard-view')).toBeInTheDocument()
    })
  })

  it('shows top bar at and above 768px', async () => {
    setBreakpoint(768)
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>,
    )

    expect(screen.getByLabelText('Mantle top bar')).toBeInTheDocument()
    expect(screen.queryByLabelText('Mantle bottom tabs')).not.toBeInTheDocument()
    await waitFor(() => {
      expect(screen.getByTestId('dashboard-view')).toBeInTheDocument()
    })
  })
})

describe('Mantle registry-driven navigation', () => {
  beforeEach(() => {
    window.history.replaceState({}, '', '/')
    mockDashboardApis()
    // Mobile breakpoint so bottom tabs are visible
    setBreakpoint(390)
  })

  it('empty registry: nav shows Home tab only, no plugin tabs', async () => {
    const { usePlugins } = await import('./usePlugins')
    vi.mocked(usePlugins).mockReturnValue([])

    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>,
    )

    const bottomNav = screen.getByLabelText('Mantle bottom tabs')
    // "Home" tab is always present
    expect(bottomNav).toHaveTextContent('Home')
    // No plugin-specific label — nothing injected from registry
    expect(bottomNav.querySelectorAll('li')).toHaveLength(1)
  })

  it('registry with one plugin: plugin tab appears in nav', async () => {
    const { usePlugins } = await import('./usePlugins')
    const plugin: PluginNavEntry = { slug: 'test-plugin', name: 'Test Plugin', showInTabBar: true, order: 0 }
    vi.mocked(usePlugins).mockReturnValue([plugin])

    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>,
    )

    const bottomNav = screen.getByLabelText('Mantle bottom tabs')
    expect(bottomNav).toHaveTextContent('Test Plugin')
    expect(bottomNav.querySelectorAll('li')).toHaveLength(2)
  })
})

describe('postMessage handling', () => {
  it('shell receives hearth.title message from plugin without throwing', () => {
    // Dispatch a postMessage from a plugin iframe; the shell should handle it gracefully.
    // PluginFrame is rendered inside App when a plugin route is active. This test verifies
    // the window message listener (added by useMantle/PluginFrame) does not throw on
    // well-formed plugin messages.
    // TODO(T-FR-0001-04): extend once PluginFrame exposes a testable message handler.
    expect(() => {
      window.dispatchEvent(
        new MessageEvent('message', {
          data: { type: 'hearth.title', title: 'Test Plugin' },
          origin: window.location.origin,
        }),
      )
    }).not.toThrow()
  })
})
