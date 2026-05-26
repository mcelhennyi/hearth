import { render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import 'fake-indexeddb/auto'

import { writeLayoutCache } from './layoutCache'
import { DashboardView } from './DashboardView'
import { EditModeProvider } from './edit'
import type { DashboardLayout } from './types'

const CACHED: DashboardLayout = {
  version: 1,
  columns: 4,
  blocks: [{ id: 'b-g', type: 'app-shortcut', plugin: 'groceries', x: 0, y: 0, w: 1, h: 1 }],
}

function mockFetch(handlers: Record<string, unknown | (() => never)>): void {
  vi.stubGlobal(
    'fetch',
    vi.fn((input: RequestInfo) => {
      const url = typeof input === 'string' ? input : input.url
      const handler = handlers[url]
      if (typeof handler === 'function') {
        return Promise.reject(handler())
      }
      if (handler === undefined) {
        return Promise.resolve({ ok: false, json: async () => ({}) })
      }
      return Promise.resolve({ ok: true, json: async () => handler })
    }),
  )
}

describe('DashboardView offline cache', () => {
  beforeEach(async () => {
    vi.stubGlobal('matchMedia', (query: string) => ({
      matches: query === '(min-width: 768px)' ? false : false,
      media: query,
      onchange: null,
      addEventListener: () => undefined,
      removeEventListener: () => undefined,
      addListener: () => undefined,
      removeListener: () => undefined,
      dispatchEvent: () => false,
    }))
    const dbs = await indexedDB.databases()
    await Promise.all(dbs.map((db) => db.name && indexedDB.deleteDatabase(db.name)))
  })

  it('rehydrates layout from IndexedDB when network fails', async () => {
    await writeLayoutCache(CACHED)
    mockFetch({
      '/api/dashboard/layout': () => new Error('offline'),
      '/api/system/tiles': { tiles: [] },
      '/api/system/strips': { strip: null },
      '/api/plugins': [],
    })

    render(
      <MemoryRouter>
        <EditModeProvider>
          <DashboardView />
        </EditModeProvider>
      </MemoryRouter>,
    )

    await waitFor(() => {
      expect(screen.getByTestId('dashboard-offline-badge')).toBeInTheDocument()
    })
    expect(screen.getByTestId('block-app-groceries')).toBeInTheDocument()
  })
})
