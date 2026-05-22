import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import type { ReactNode } from 'react'
import { MemoryRouter } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import 'fake-indexeddb/auto'

import { SettingsProvider } from '../shell/SettingsContext'
import { SettingsModal } from '../shell/SettingsModal'
import { ThemeProvider } from '../theme/ThemeProvider'
import type { Bridge } from '../shell/types'
import { DashboardView } from './DashboardView'
import { EmptyState } from './EmptyState'
import type { DashboardLayout } from './types'

const EMPTY_LAYOUT: DashboardLayout = { version: 1, columns: 4, blocks: [] }

const bridge: Bridge = {
  subscribe: () => () => {},
  pushToPlugin: vi.fn(),
  broadcastToAllPlugins: vi.fn(),
}

function mockFetch(handlers: Record<string, unknown>): void {
  vi.stubGlobal(
    'fetch',
    vi.fn((input: RequestInfo) => {
      const url = typeof input === 'string' ? input : input.url
      const handler = handlers[url]
      if (handler === undefined) {
        return Promise.resolve({ ok: false, json: async () => ({}) })
      }
      return Promise.resolve({ ok: true, json: async () => handler })
    }),
  )
}

function Harness({ children }: { children: ReactNode }) {
  return (
    <MemoryRouter>
      <SettingsProvider>
        <ThemeProvider bridge={bridge}>
          {children}
          <SettingsModal isDesktop={false} />
        </ThemeProvider>
      </SettingsProvider>
    </MemoryRouter>
  )
}

describe('EmptyState', () => {
  beforeEach(() => {
    vi.stubGlobal('matchMedia', (query: string) => ({
      matches: false,
      media: query,
      onchange: null,
      addEventListener: () => undefined,
      removeEventListener: () => undefined,
      addListener: () => undefined,
      removeListener: () => undefined,
      dispatchEvent: () => false,
    }))
  })

  it('renders headline, body, and CTA', () => {
    render(
      <Harness>
        <EmptyState />
      </Harness>,
    )

    expect(screen.getByTestId('dashboard-empty-state')).toBeInTheDocument()
    expect(screen.getByText('Your dashboard is empty.')).toBeInTheDocument()
    expect(
      screen.getByText('Enable plugins in Settings to populate your home grid.'),
    ).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Open Settings' })).toBeInTheDocument()
  })

  it('opens Settings modal at the Plugins tab when CTA is clicked', async () => {
    render(
      <Harness>
        <EmptyState />
      </Harness>,
    )

    fireEvent.click(screen.getByRole('button', { name: 'Open Settings' }))

    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument()
    })

    const pluginsTab = screen.getByRole('tab', { name: 'Plugins' })
    expect(pluginsTab).toHaveAttribute('aria-selected', 'true')
  })
})

describe('DashboardView empty layout', () => {
  beforeEach(() => {
    vi.stubGlobal('matchMedia', (query: string) => ({
      matches: false,
      media: query,
      onchange: null,
      addEventListener: () => undefined,
      removeEventListener: () => undefined,
      addListener: () => undefined,
      removeListener: () => undefined,
      dispatchEvent: () => false,
    }))
  })

  it('renders EmptyState when layout has zero blocks', async () => {
    mockFetch({
      '/api/dashboard/layout': EMPTY_LAYOUT,
      '/api/system/tiles': { tiles: [] },
      '/api/system/strips': { strip: null },
      '/api/plugins': [],
    })

    render(
      <Harness>
        <DashboardView />
      </Harness>,
    )

    await waitFor(() => {
      expect(screen.getByTestId('dashboard-empty-state')).toBeInTheDocument()
    })
    expect(screen.queryByTestId('dashboard-grid')).not.toBeInTheDocument()
  })
})
