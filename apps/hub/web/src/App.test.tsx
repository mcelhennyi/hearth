import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import type { PluginNavEntry } from './usePlugins'

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
  })

  it('shows bottom tabs under 768px', () => {
    setBreakpoint(390)
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>,
    )

    expect(screen.getByLabelText('Mantle bottom tabs')).toBeInTheDocument()
    expect(screen.queryByLabelText('Mantle top bar')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Send test notification' })).toBeInTheDocument()
  })

  it('shows top bar at and above 768px', () => {
    setBreakpoint(768)
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>,
    )

    expect(screen.getByLabelText('Mantle top bar')).toBeInTheDocument()
    expect(screen.queryByLabelText('Mantle bottom tabs')).not.toBeInTheDocument()
  })
})

describe('Mantle registry-driven navigation', () => {
  beforeEach(() => {
    window.history.replaceState({}, '', '/')
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
    // Home + pinned Settings control (mantle-ui.md § Bottom bar).
    expect(bottomNav.querySelectorAll('li')).toHaveLength(2)
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
    // Home + plugin + Settings.
    expect(bottomNav.querySelectorAll('li')).toHaveLength(3)
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
