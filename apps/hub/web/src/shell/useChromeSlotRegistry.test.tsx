// Tests for chrome slot registry (T-FR-0006-06).

import { act, renderHook } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'

import type { Bridge, InboundMessage } from './types'
import { useChromeSlotRegistry } from './useChromeSlotRegistry'

type TestBridge = Bridge & { emit: (msg: InboundMessage) => void }

function makeBridge(): TestBridge {
  const handlers = new Map<string, Set<(payload: unknown) => void>>()
  const pushToPlugin = vi.fn()
  return {
    subscribe(type, handler) {
      let set = handlers.get(type)
      if (!set) {
        set = new Set()
        handlers.set(type, set)
      }
      set.add(handler as (payload: unknown) => void)
      return () => set?.delete(handler as (payload: unknown) => void)
    },
    pushToPlugin,
    broadcastToAllPlugins: vi.fn(),
    emit(msg) {
      const set = handlers.get(msg.type)
      if (!set) return
      for (const handler of Array.from(set)) {
        handler(msg)
      }
    },
  }
}

function deliver(bridge: TestBridge, msg: InboundMessage) {
  act(() => {
    bridge.emit(msg)
  })
}

describe('useChromeSlotRegistry', () => {
  afterEach(() => {
    document.body.innerHTML = ''
    vi.restoreAllMocks()
  })

  it('mount adds item; unmount removes it', () => {
    const bridge = makeBridge()
    const { result, rerender } = renderHook(
      ({ slug }) => useChromeSlotRegistry(bridge, slug),
      { initialProps: { slug: 'groceries' as string | null } },
    )

    deliver(bridge, {
      type: 'hearth.chrome.mount',
      slot: 'top',
      surface: 'app',
      payload: { kind: 'button', id: 'add', label: 'Add' },
    })
    rerender({ slug: 'groceries' })

    expect(result.current.topItems).toHaveLength(1)
    expect(result.current.topItems[0]?.id).toBe('add')
    expect(result.current.hasChromeSlots).toBe(true)

    deliver(bridge, { type: 'hearth.chrome.unmount', slot: 'top', surface: 'app', id: 'add' })
    rerender({ slug: 'groceries' })

    expect(result.current.topItems).toHaveLength(0)
    expect(result.current.hasChromeSlots).toBe(false)
  })

  it('mount with same id replaces payload', () => {
    const bridge = makeBridge()
    const { result, rerender } = renderHook(
      ({ slug }) => useChromeSlotRegistry(bridge, slug),
      { initialProps: { slug: 'groceries' } },
    )

    deliver(bridge, {
      type: 'hearth.chrome.mount',
      slot: 'bottom',
      surface: 'app',
      payload: { kind: 'button', id: 'sort', label: 'Sort' },
    })
    deliver(bridge, {
      type: 'hearth.chrome.mount',
      slot: 'bottom',
      surface: 'app',
      payload: { kind: 'button', id: 'sort', label: 'Sorted', variant: 'accent' },
    })
    rerender({ slug: 'groceries' })

    expect(result.current.bottomItems).toHaveLength(1)
    expect(result.current.bottomItems[0]?.payload).toMatchObject({ label: 'Sorted', variant: 'accent' })
  })

  it('rejects mount beyond cap with hearth.chrome.error', () => {
    const bridge = makeBridge()
    const iframe = document.createElement('iframe')
    iframe.setAttribute('data-plugin-slug', 'groceries')
    document.body.appendChild(iframe)
    const { rerender } = renderHook(
      ({ slug }) => useChromeSlotRegistry(bridge, slug),
      { initialProps: { slug: 'groceries' } },
    )

    for (let i = 0; i < 8; i += 1) {
      deliver(bridge, {
        type: 'hearth.chrome.mount',
        slot: 'top',
        surface: 'app',
        payload: { kind: 'button', id: `b${i}`, label: `B${i}` },
      })
    }
    deliver(bridge, {
      type: 'hearth.chrome.mount',
      slot: 'top',
      surface: 'app',
      payload: { kind: 'button', id: 'b9', label: 'B9' },
    })
    rerender({ slug: 'groceries' })

    expect(bridge.pushToPlugin).toHaveBeenCalledWith(iframe, {
      type: 'hearth.chrome.error',
      slot: 'top',
      surface: 'app',
      reason: 'limit',
    })
  })

  it('clears app slots when active plugin slug becomes null (route change)', () => {
    const bridge = makeBridge()
    const { result, rerender } = renderHook(
      ({ slug }) => useChromeSlotRegistry(bridge, slug),
      { initialProps: { slug: 'groceries' as string | null } },
    )

    deliver(bridge, {
      type: 'hearth.chrome.mount',
      slot: 'top',
      surface: 'app',
      payload: { kind: 'button', id: 'x', label: 'X' },
    })
    rerender({ slug: 'groceries' })
    expect(result.current.topItems).toHaveLength(1)

    rerender({ slug: null })
    expect(result.current.topItems).toHaveLength(0)
  })

  it('invoke posts hearth.chrome.invoke to the active plugin iframe', () => {
    const bridge = makeBridge()
    const iframe = document.createElement('iframe')
    iframe.setAttribute('data-plugin-slug', 'groceries')
    document.body.appendChild(iframe)

    const { result } = renderHook(() => useChromeSlotRegistry(bridge, 'groceries'))

    act(() => {
      result.current.invoke('top', 'add', 'item-1')
    })

    expect(bridge.pushToPlugin).toHaveBeenCalledWith(iframe, {
      type: 'hearth.chrome.invoke',
      slot: 'top',
      surface: 'app',
      id: 'add',
      itemId: 'item-1',
    })
  })
})
