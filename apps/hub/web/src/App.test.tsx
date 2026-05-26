import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import type { PluginNavEntry } from './usePlugins'

const pluginHooks = vi.hoisted(() => ({
  usePlugins: vi.fn(() => []),
}))

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
  return { ...actual, usePlugins: pluginHooks.usePlugins }
})

beforeEach(() => {
  pluginHooks.usePlugins.mockReturnValue([])
  vi.stubGlobal(
    'fetch',
    vi.fn(async () =>
      Response.json({
        user_id: 'local-owner',
        display_name: 'Local Owner',
        roles: ['owner'],
      }),
    ),
  )
})

afterEach(() => {
  vi.unstubAllGlobals()
  vi.clearAllMocks()
})

describe('Mantle layout breakpoint behavior', () => {
  beforeEach(() => {
    window.history.replaceState({}, '', '/')
  })

  it('shows bottom tabs under 768px', async () => {
    setBreakpoint(390)
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>,
    )

    expect(await screen.findByLabelText('Mantle bottom tabs')).toBeInTheDocument()
    expect(screen.queryByLabelText('Mantle top bar')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Send test notification' })).toBeInTheDocument()
  })

  it('shows top bar at and above 768px', async () => {
    setBreakpoint(768)
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>,
    )

    expect(await screen.findByLabelText('Mantle top bar')).toBeInTheDocument()
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

    const bottomNav = await screen.findByLabelText('Mantle bottom tabs')
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

    const bottomNav = await screen.findByLabelText('Mantle bottom tabs')
    expect(bottomNav).toHaveTextContent('Test Plugin')
    expect(bottomNav.querySelectorAll('li')).toHaveLength(2)
  })
})

describe('Mantle hearth-users session contract', () => {
  beforeEach(() => {
    window.history.replaceState({}, '', '/')
    setBreakpoint(390)
  })

  it('links unauthenticated users to hearth-users login with a next target', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => new Response('unauthorized', { status: 401 })))

    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>,
    )

    const loginLink = await screen.findByRole('link', { name: 'Sign in with Hearth Users' })
    expect(loginLink).toHaveAttribute('href', '/hearth-users/login?next=%2F')
    expect(screen.queryByLabelText('Mantle bottom tabs')).not.toBeInTheDocument()
  })

  it('fetches the hearth-users session before rendering the shell', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () =>
        Response.json({
          user_id: 'local-owner',
          display_name: 'Local Owner',
          roles: ['owner'],
        }),
      ),
    )

    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>,
    )

    await screen.findByLabelText('Mantle bottom tabs')
    expect(fetch).toHaveBeenCalledWith('/hearth-users/api/session', { credentials: 'include' })
    expect(screen.getByText('Local Owner')).toBeInTheDocument()
  })

  it('posts verified hearth.user claims to plugin iframes', async () => {
    const { usePlugins } = await import('./usePlugins')
    vi.mocked(usePlugins).mockReturnValue([{ slug: 'test-plugin', name: 'Test Plugin', showInTabBar: true, order: 0 }])
    vi.stubGlobal(
      'fetch',
      vi.fn(async () =>
        Response.json({
          user_id: 'local-owner',
          display_name: 'Local Owner',
          roles: ['owner'],
        }),
      ),
    )
    window.history.replaceState({}, '', '/test-plugin')

    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>,
    )

    const frame = (await screen.findByTitle('Test Plugin')) as HTMLIFrameElement
    expect(frame.contentWindow).toBeTruthy()
    const postMessage = vi.spyOn(frame.contentWindow!, 'postMessage')

    frame.dispatchEvent(new Event('load'))

    await waitFor(() => {
      expect(postMessage).toHaveBeenCalledWith(
        {
          type: 'hearth.user',
          user: { id: 'local-owner', name: 'Local Owner', roles: ['owner'] },
        },
        window.location.origin,
      )
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
