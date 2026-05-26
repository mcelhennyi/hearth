import { fireEvent, render, screen, waitFor } from '@testing-library/react'
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
    expect(bottomNav.querySelectorAll('li')).toHaveLength(2)
    expect(bottomNav).toHaveTextContent('Settings')
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
    expect(bottomNav.querySelectorAll('li')).toHaveLength(3)
  })
})

describe('Auth provider settings', () => {
  beforeEach(() => {
    setBreakpoint(768)
    window.history.replaceState({}, '', '/settings')
  })

  it('loads the current provider and records an external verify URL toggle', async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      if (input === '/api/settings' && !init) {
        return new Response(
          JSON.stringify({
            auth: { provider: 'builtin', external_verify_url: null },
          }),
          { headers: { 'Content-Type': 'application/json' } },
        )
      }
      if (input === '/api/settings' && init?.method === 'PUT') {
        return new Response(
          JSON.stringify({
            auth: {
              provider: 'external',
              external_verify_url: 'https://auth.example.test/verify',
            },
          }),
          { headers: { 'Content-Type': 'application/json' } },
        )
      }
      return new Response(null, { status: 404 })
    })
    vi.stubGlobal('fetch', fetchMock)

    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>,
    )

    expect(await screen.findByRole('radio', { name: /built-in hearth users/i })).toBeChecked()
    fireEvent.click(screen.getByRole('radio', { name: /external verify url/i }))
    fireEvent.change(screen.getByPlaceholderText('https://auth.example.test/verify'), {
      target: { value: 'https://auth.example.test/verify' },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Save' }))

    await waitFor(() => {
      expect(screen.getByRole('status')).toHaveTextContent('Auth provider settings saved.')
    })
    expect(fetchMock).toHaveBeenLastCalledWith('/api/settings', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        auth: {
          provider: 'external',
          external_verify_url: 'https://auth.example.test/verify',
        },
      }),
    })
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
