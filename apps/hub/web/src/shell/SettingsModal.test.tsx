// SettingsModal a11y tests — T-FR-0006-04 TEST phase.
// Spec: docs/design/mantle-ui.md § Settings modal.

import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { useEffect } from 'react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { ThemeProvider } from '../theme/ThemeProvider'
import type { Bridge } from './types'
import { SettingsProvider, useSettings, type SettingsTab } from './SettingsContext'
import { SettingsModal } from './SettingsModal'

const bridge: Bridge = {
  subscribe: () => () => {},
  pushToPlugin: vi.fn(),
  broadcastToAllPlugins: vi.fn(),
}

function OpenOnMount({ tab = 'theme' }: { tab?: SettingsTab }) {
  const { openSettings } = useSettings()
  useEffect(() => {
    openSettings(tab)
  }, [openSettings, tab])
  return <SettingsModal isDesktop={true} />
}

function Harness({
  isDesktop = true,
  tab = 'theme',
}: {
  isDesktop?: boolean
  tab?: SettingsTab
}) {
  return (
    <SettingsProvider>
      <ThemeProvider bridge={bridge}>
        <OpenOnMount tab={tab} />
        {!isDesktop && null}
      </ThemeProvider>
    </SettingsProvider>
  )
}

describe('SettingsModal', () => {
  beforeEach(() => {
    vi.stubGlobal(
      'fetch',
      vi.fn((input: RequestInfo | URL) => {
        const path = input.toString()
        if (path === '/api/user/preferences') {
          return Promise.resolve({ ok: false, json: async () => ({}) })
        }
        return Promise.reject(new Error(`Unexpected fetch: ${path}`))
      }),
    )
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('closes on Escape', async () => {
    render(<Harness />)
    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeTruthy()
    })

    fireEvent.keyDown(window, { key: 'Escape' })
    await waitFor(() => {
      expect(screen.queryByRole('dialog')).toBeNull()
    })
  })

  it('traps Tab focus within the dialog panel', async () => {
    render(<Harness />)
    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeTruthy()
    })
    const dialog = screen.getByRole('dialog')
    const focusables = dialog.querySelectorAll<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
    )
    expect(focusables.length).toBeGreaterThan(1)

    const first = focusables[0]
    const last = focusables[focusables.length - 1]
    last.focus()

    fireEvent.keyDown(window, { key: 'Tab' })
    expect(document.activeElement).toBe(first)
  })

  it('shows admin user management controls for admins without password hashes', async () => {
    const fetchMock = vi.fn((input: RequestInfo | URL) => {
      const path = input.toString()
      if (path === '/api/user/preferences') {
        return Promise.resolve({ ok: false, json: async () => ({}) })
      }
      if (path === '/hearth-users/api/session') {
        return Promise.resolve({
          ok: true,
          json: async () => ({
            user_id: 'admin_1',
            display_name: 'Ada',
            roles: ['admin', 'user'],
          }),
        })
      }
      if (path === '/hearth-users/api/admin/users') {
        return Promise.resolve({
          ok: true,
          json: async () => ({
            users: [
              {
                user_id: 'admin_1',
                username: 'ada',
                display_name: 'Ada Lovelace',
                roles: ['admin', 'user'],
                disabled: false,
              },
              {
                user_id: 'user_2',
                username: 'grace',
                display_name: 'Grace Hopper',
                roles: ['user'],
                disabled: true,
              },
            ],
          }),
        })
      }
      return Promise.reject(new Error(`Unexpected fetch: ${path}`))
    })
    vi.stubGlobal('fetch', fetchMock)

    render(<Harness tab="account" />)

    expect(await screen.findByRole('heading', { name: 'User management' })).toBeTruthy()
    expect(screen.getByRole('button', { name: 'Create user' })).toBeTruthy()
    expect(screen.getByText('Grace Hopper')).toBeTruthy()
    expect(screen.getByRole('button', { name: 'Enable Grace Hopper' })).toBeTruthy()
    expect(document.body.textContent).not.toContain('password_hash')
    expect(fetchMock).toHaveBeenCalledWith('/hearth-users/api/session', {
      credentials: 'include',
    })
    expect(fetchMock).toHaveBeenCalledWith('/hearth-users/api/admin/users', {
      credentials: 'include',
    })
  })

  it('hides admin user management controls for non-admins', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn((input: RequestInfo | URL) => {
        const path = input.toString()
        if (path === '/api/user/preferences') {
          return Promise.resolve({ ok: false, json: async () => ({}) })
        }
        if (path === '/hearth-users/api/session') {
          return Promise.resolve({
            ok: true,
            json: async () => ({ user_id: 'user_1', display_name: 'Grace', roles: ['user'] }),
          })
        }
        return Promise.reject(new Error(`Unexpected fetch: ${path}`))
      }),
    )

    render(<Harness tab="account" />)

    expect(await screen.findByText('Admin role required.')).toBeTruthy()
    expect(screen.queryByRole('button', { name: 'Create user' })).toBeNull()
    expect(screen.queryByText('User management')).toBeNull()
  })
})
