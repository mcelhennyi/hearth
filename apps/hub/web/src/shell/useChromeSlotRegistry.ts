// Chrome slot registry — mount/unmount via postMessage bridge (T-FR-0006-06).
// Spec: docs/design/mantle-ui.md §"Declaring chrome slots".

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import { CHROME_SLOT_MAX_ITEMS } from './chromeConstants'
import type {
  Bridge,
  ChromePayload,
  ChromeSlot,
  ChromeSurface,
  InboundChromeMountMessage,
  InboundChromeUnmountMessage,
} from './types'

export interface ChromeRegistryEntry {
  id: string
  payload: ChromePayload
}

type SlotKey = `${ChromeSurface}:${ChromeSlot}`

function slotKey(surface: ChromeSurface, slot: ChromeSlot): SlotKey {
  return `${surface}:${slot}`
}

function isValidChromePayload(payload: unknown): payload is ChromePayload {
  if (!payload || typeof payload !== 'object') return false
  const p = payload as { kind?: unknown; id?: unknown; label?: unknown }
  if (p.kind === 'button') {
    return typeof p.id === 'string' && typeof p.label === 'string'
  }
  if (p.kind === 'menu') {
    return (
      typeof p.id === 'string' &&
      typeof p.label === 'string' &&
      Array.isArray((p as { items?: unknown }).items)
    )
  }
  return false
}

function findPluginIframe(slug: string | null): HTMLIFrameElement | null {
  if (!slug) return null
  return document.querySelector<HTMLIFrameElement>(`iframe[data-plugin-slug="${slug}"]`)
}

export interface ChromeSlotRegistry {
  topItems: ChromeRegistryEntry[]
  bottomItems: ChromeRegistryEntry[]
  hasChromeSlots: boolean
  invoke: (slot: ChromeSlot, id: string, itemId?: string) => void
}

export function useChromeSlotRegistry(bridge: Bridge, activePluginSlug: string | null): ChromeSlotRegistry {
  const [slots, setSlots] = useState<Map<SlotKey, ChromeRegistryEntry[]>>(() => new Map())
  const activeSlugRef = useRef(activePluginSlug)
  activeSlugRef.current = activePluginSlug

  const pushChromeError = useCallback(
    (surface: ChromeSurface, slot: ChromeSlot, reason: 'limit' | 'invalid_payload') => {
      const frame = findPluginIframe(activeSlugRef.current)
      if (!frame) return
      bridge.pushToPlugin(frame, { type: 'hearth.chrome.error', slot, surface, reason })
    },
    [bridge],
  )

  const applyMount = useCallback(
    (msg: InboundChromeMountMessage) => {
      if (!isValidChromePayload(msg.payload)) {
        pushChromeError(msg.surface, msg.slot, 'invalid_payload')
        return
      }
      const key = slotKey(msg.surface, msg.slot)
      setSlots((prev) => {
        const next = new Map(prev)
        const list = [...(next.get(key) ?? [])]
        const index = list.findIndex((e) => e.id === msg.payload.id)
        if (index >= 0) {
          list[index] = { id: msg.payload.id, payload: msg.payload }
        } else if (list.length >= CHROME_SLOT_MAX_ITEMS) {
          pushChromeError(msg.surface, msg.slot, 'limit')
          return prev
        } else {
          list.push({ id: msg.payload.id, payload: msg.payload })
        }
        next.set(key, list)
        return next
      })
    },
    [pushChromeError],
  )

  const applyUnmount = useCallback((msg: InboundChromeUnmountMessage) => {
    const key = slotKey(msg.surface, msg.slot)
    setSlots((prev) => {
      const next = new Map(prev)
      const list = (next.get(key) ?? []).filter((e) => e.id !== msg.id)
      if (list.length === 0) next.delete(key)
      else next.set(key, list)
      return next
    })
  }, [])

  const clearAppSurface = useCallback(() => {
    setSlots((prev) => {
      const next = new Map(prev)
      next.delete(slotKey('app', 'top'))
      next.delete(slotKey('app', 'bottom'))
      return next
    })
  }, [])

  useEffect(() => {
    const unsubMount = bridge.subscribe('hearth.chrome.mount', applyMount)
    const unsubUnmount = bridge.subscribe('hearth.chrome.unmount', applyUnmount)
    return () => {
      unsubMount()
      unsubUnmount()
    }
  }, [bridge, applyMount, applyUnmount])

  // Implicit unmount when leaving a plugin route (mantle-ui.md lifecycle).
  useEffect(() => {
    if (!activePluginSlug) clearAppSurface()
  }, [activePluginSlug, clearAppSurface])

  const topItems = useMemo(
    () => (activePluginSlug ? (slots.get(slotKey('app', 'top')) ?? []) : []),
    [slots, activePluginSlug],
  )
  const bottomItems = useMemo(
    () => (activePluginSlug ? (slots.get(slotKey('app', 'bottom')) ?? []) : []),
    [slots, activePluginSlug],
  )

  const hasChromeSlots = topItems.length > 0 || bottomItems.length > 0

  const invoke = useCallback(
    (slot: ChromeSlot, id: string, itemId?: string) => {
      const frame = findPluginIframe(activeSlugRef.current)
      if (!frame) return
      bridge.pushToPlugin(frame, {
        type: 'hearth.chrome.invoke',
        slot,
        surface: 'app',
        id,
        ...(itemId !== undefined ? { itemId } : {}),
      })
    },
    [bridge],
  )

  return { topItems, bottomItems, hasChromeSlots, invoke }
}
