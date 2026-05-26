// SettingsModal a11y tests — T-FR-0006-04 TEST phase.
// Spec: docs/design/mantle-ui.md § Settings modal.

import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { useEffect } from 'react'
import { describe, expect, it, vi } from 'vitest'

import { ThemeProvider } from '../theme/ThemeProvider'
import type { Bridge } from './types'
import { SettingsProvider, useSettings } from './SettingsContext'
import { SettingsModal } from './SettingsModal'

const bridge: Bridge = {
  subscribe: () => () => {},
  pushToPlugin: vi.fn(),
  broadcastToAllPlugins: vi.fn(),
}

function OpenOnMount() {
  const { openSettings } = useSettings()
  useEffect(() => {
    openSettings('theme')
  }, [openSettings])
  return <SettingsModal isDesktop={true} />
}

function Harness({ isDesktop = true }: { isDesktop?: boolean }) {
  return (
    <SettingsProvider>
      <ThemeProvider bridge={bridge}>
        <OpenOnMount />
        {!isDesktop && null}
      </ThemeProvider>
    </SettingsProvider>
  )
}

describe('SettingsModal', () => {
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
})
