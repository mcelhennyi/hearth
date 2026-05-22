// Tests for ChromeSlot rendering (T-FR-0006-06).

import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

import { ChromeSlot } from './ChromeSlot'
import type { ChromeRegistryEntry } from './useChromeSlotRegistry'

function buttons(count: number, prefix = 'btn'): ChromeRegistryEntry[] {
  return Array.from({ length: count }, (_, i) => ({
    id: `${prefix}-${i}`,
    payload: { kind: 'button' as const, id: `${prefix}-${i}`, label: `Action ${i}` },
  }))
}

describe('ChromeSlot', () => {
  it('renders visible buttons up to the top cap', () => {
    render(
      <ChromeSlot slot="top" items={buttons(2)} isDesktop={false} onInvoke={vi.fn()} />,
    )
    expect(screen.getByRole('button', { name: 'Action 0' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Action 1' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'More actions' })).not.toBeInTheDocument()
  })

  it('shows overflow menu when top items exceed visible cap (3)', () => {
    render(
      <ChromeSlot slot="top" items={buttons(5)} isDesktop={false} onInvoke={vi.fn()} />,
    )
    expect(screen.getByRole('button', { name: 'Action 0' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Action 1' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Action 2' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Action 3' })).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'More actions' })).toBeInTheDocument()
  })

  it('overflow menu lists labels for collapsed top items', () => {
    render(
      <ChromeSlot slot="top" items={buttons(5)} isDesktop={false} onInvoke={vi.fn()} />,
    )
    fireEvent.click(screen.getByRole('button', { name: 'More actions' }))
    expect(screen.getByRole('menuitem', { name: 'Action 3' })).toBeInTheDocument()
    expect(screen.getByRole('menuitem', { name: 'Action 4' })).toBeInTheDocument()
  })

  it('uses bottom visible cap of 4 before overflow', () => {
    render(
      <ChromeSlot slot="bottom" items={buttons(6, 'b')} isDesktop={false} onInvoke={vi.fn()} />,
    )
    expect(screen.getByRole('button', { name: 'Action 0' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Action 3' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Action 4' })).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'More actions' })).toBeInTheDocument()
  })

  it('calls onInvoke when a visible button is clicked', () => {
    const onInvoke = vi.fn()
    render(
      <ChromeSlot
        slot="top"
        items={[{ id: 'add', payload: { kind: 'button', id: 'add', label: 'Add item' } }]}
        isDesktop={false}
        onInvoke={onInvoke}
      />,
    )
    fireEvent.click(screen.getByRole('button', { name: 'Add item' }))
    expect(onInvoke).toHaveBeenCalledWith('add')
  })
})
