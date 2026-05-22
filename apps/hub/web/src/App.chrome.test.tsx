// App integration: chrome slots + route-change unmount (T-FR-0006-06).

import { act, render, screen, waitFor } from '@testing-library/react'
import { createMemoryRouter, RouterProvider } from 'react-router-dom'
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

vi.mock('./usePlugins', async (importOriginal) => {
  const actual = await importOriginal<typeof import('./usePlugins')>()
  return { ...actual, usePlugins: vi.fn(() => []) }
})

describe('App chrome slots', () => {
  beforeEach(() => {
    setBreakpoint(390)
    document.title = 'Hearth'
  })

  it('clears top chrome when navigating from plugin route to dashboard', async () => {
    const { usePlugins } = await import('./usePlugins')
    const plugin: PluginNavEntry = { slug: 'groceries', name: 'Groceries', showInTabBar: true, order: 0 }
    vi.mocked(usePlugins).mockReturnValue([plugin])

    const router = createMemoryRouter([{ path: '/*', element: <App /> }], {
      initialEntries: ['/groceries'],
    })
    render(<RouterProvider router={router} />)

    act(() => {
      window.dispatchEvent(
        new MessageEvent('message', {
          data: {
            type: 'hearth.chrome.mount',
            slot: 'top',
            surface: 'app',
            payload: { kind: 'button', id: 'add', label: 'Add item' },
          },
          origin: window.location.origin,
        }),
      )
    })

    expect(screen.getByRole('button', { name: 'Add item' })).toBeInTheDocument()
    expect(document.querySelector('.shell')).toHaveClass('has-chrome-slots')

    await act(async () => {
      await router.navigate('/')
    })

    await waitFor(() => {
      expect(screen.queryByRole('button', { name: 'Add item' })).not.toBeInTheDocument()
    })
    expect(document.querySelector('.shell')).not.toHaveClass('has-chrome-slots')
  })
})
