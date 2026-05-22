// ThemeProvider tests — T-FR-0006-04 TEST phase.
// Spec: docs/design/mantle-ui.md § Theme persistence.

import { act, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import type { Bridge } from '../shell/types'
import { THEME_STORAGE_KEY } from './tokens'
import { ThemeProvider, useThemePreference } from './ThemeProvider'

const bridge: Bridge = {
  subscribe: () => () => {},
  pushToPlugin: vi.fn(),
  broadcastToAllPlugins: vi.fn(),
}

function Probe() {
  const { preference, reconciled } = useThemePreference()
  return (
    <div>
      <span data-testid="preference">{preference}</span>
      <span data-testid="reconciled">{reconciled ? 'yes' : 'no'}</span>
    </div>
  )
}

describe('ThemeProvider', () => {
  beforeEach(() => {
    localStorage.clear()
    document.documentElement.removeAttribute('data-hearth-theme')
    vi.stubGlobal('fetch', vi.fn())
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('boots from localStorage before server reconcile', async () => {
    localStorage.setItem(THEME_STORAGE_KEY, 'light')

    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ theme: 'dark' }),
    } as Response)

    render(
      <ThemeProvider bridge={bridge}>
        <Probe />
      </ThemeProvider>,
    )

    expect(screen.getByTestId('preference').textContent).toBe('light')

    await waitFor(() => {
      expect(screen.getByTestId('reconciled').textContent).toBe('yes')
    })

    expect(screen.getByTestId('preference').textContent).toBe('dark')
    expect(localStorage.getItem(THEME_STORAGE_KEY)).toBe('dark')
    expect(bridge.broadcastToAllPlugins).toHaveBeenCalled()
  })

  it('broadcasts hearth.theme on preference change', async () => {
    vi.mocked(fetch)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ theme: 'system' }),
      } as Response)
      .mockResolvedValueOnce({ ok: true, json: async () => ({ theme: 'dark' }) } as Response)

    function Changer() {
      const { setPreference } = useThemePreference()
      return (
        <button type="button" onClick={() => void setPreference('dark')}>
          dark
        </button>
      )
    }

    render(
      <ThemeProvider bridge={bridge}>
        <Changer />
      </ThemeProvider>,
    )

    await waitFor(() => expect(fetch).toHaveBeenCalled())

    await act(async () => {
      screen.getByRole('button', { name: 'dark' }).click()
    })

    const themeCalls = vi
      .mocked(bridge.broadcastToAllPlugins)
      .mock.calls.filter((call) => call[0]?.type === 'hearth.theme')
    expect(themeCalls.length).toBeGreaterThan(0)
    expect(themeCalls[themeCalls.length - 1][0]).toEqual(
      expect.objectContaining({ type: 'hearth.theme', tokens: expect.objectContaining({ mode: 'dark' }) }),
    )
  })
})
