import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from 'react'

import { writeLayoutCache } from '../layoutCache'
import type { DashboardLayout, PluginRegistryEntry, SystemTile } from '../types'
import { systemTileIdFromBlock } from '../types'
import { findCollidingBlockIds, hasCollisions } from './collisions'
import {
  cloneLayout,
  createShortcutBlock,
  createSystemBlock,
  moveBlockInLayout,
  removeBlockFromLayout,
} from './layoutDraft'
import { handleInboundHaptic } from '../../shell/inboundDefaults'

const LONG_PRESS_MS = 600

export type DashboardEditSource = {
  layout: DashboardLayout
  columns: number
  plugins: PluginRegistryEntry[]
  allTiles: SystemTile[]
  offline: boolean
  onLayoutSaved: (layout: DashboardLayout) => void
}

type EditModeContextValue = {
  active: boolean
  dirty: boolean
  draftLayout: DashboardLayout | null
  collidingIds: Set<string>
  reducedMotion: boolean
  pickerOpen: boolean
  saving: boolean
  source: DashboardEditSource | null
  registerSource: (source: DashboardEditSource | null) => void
  enterEdit: () => void
  cancelEdit: () => void
  saveEdit: () => Promise<void>
  openPicker: () => void
  closePicker: () => void
  removeBlock: (blockId: string) => Promise<void>
  moveBlock: (blockId: string, x: number, y: number) => void
  addPickerShortcut: (plugin: PluginRegistryEntry) => void
  addPickerSystemTile: (tile: SystemTile) => Promise<void>
  bindGridLongPress: (element: HTMLElement | null) => void
}

const EditModeContext = createContext<EditModeContextValue | null>(null)

function useReducedMotion(): boolean {
  const [reduced, setReduced] = useState(false)
  useEffect(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)')
    const update = () => setReduced(mq.matches)
    update()
    mq.addEventListener('change', update)
    return () => mq.removeEventListener('change', update)
  }, [])
  return reduced
}

async function hideSystemTile(tileId: string): Promise<void> {
  await fetch(`/api/system/tiles/${tileId}/hide`, { method: 'POST' })
}

async function restoreSystemTile(tileId: string): Promise<void> {
  await fetch(`/api/system/tiles/${tileId}/restore`, { method: 'POST' })
}

export function EditModeProvider({ children }: { children: ReactNode }) {
  const [source, setSource] = useState<DashboardEditSource | null>(null)
  const [active, setActive] = useState(false)
  const [savedLayout, setSavedLayout] = useState<DashboardLayout | null>(null)
  const [draftLayout, setDraftLayout] = useState<DashboardLayout | null>(null)
  const [pickerOpen, setPickerOpen] = useState(false)
  const [saving, setSaving] = useState(false)
  const reducedMotion = useReducedMotion()
  const longPressTimer = useRef<ReturnType<typeof setTimeout> | null>(null)
  const gridElement = useRef<HTMLElement | null>(null)

  const collidingIds = useMemo(
    () => (draftLayout ? findCollidingBlockIds(draftLayout.blocks) : new Set<string>()),
    [draftLayout],
  )

  const dirty = useMemo(() => {
    if (!active || !savedLayout || !draftLayout) {
      return false
    }
    return JSON.stringify(savedLayout) !== JSON.stringify(draftLayout)
  }, [active, savedLayout, draftLayout])

  const clearLongPress = useCallback(() => {
    if (longPressTimer.current) {
      clearTimeout(longPressTimer.current)
      longPressTimer.current = null
    }
  }, [])

  const enterEdit = useCallback(() => {
    if (!source?.layout || active) {
      return
    }
    handleInboundHaptic('impact')
    setSavedLayout(cloneLayout(source.layout))
    setDraftLayout(cloneLayout(source.layout))
    setActive(true)
    setPickerOpen(false)
  }, [active, source])

  const cancelEdit = useCallback(() => {
    if (dirty && !window.confirm('Discard layout changes?')) {
      return
    }
    setActive(false)
    setDraftLayout(null)
    setSavedLayout(null)
    setPickerOpen(false)
    clearLongPress()
  }, [clearLongPress, dirty])

  const saveEdit = useCallback(async () => {
    if (!draftLayout || !source || hasCollisions(draftLayout.blocks)) {
      return
    }
    setSaving(true)
    try {
      const body = {
        version: draftLayout.version,
        columns: source.columns,
        blocks: draftLayout.blocks,
      }
      const response = await fetch('/api/dashboard/layout', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      if (!response.ok) {
        throw new Error(`PUT layout failed: ${response.status}`)
      }
      const saved = (await response.json()) as DashboardLayout
      await writeLayoutCache(saved)
      source.onLayoutSaved(saved)
      setActive(false)
      setDraftLayout(null)
      setSavedLayout(null)
      setPickerOpen(false)
    } finally {
      setSaving(false)
    }
  }, [draftLayout, source])

  const removeBlock = useCallback(
    async (blockId: string) => {
      if (!draftLayout) {
        return
      }
      const block = draftLayout.blocks.find((b) => b.id === blockId)
      if (!block) {
        return
      }
      if (block.type === 'system') {
        const tileId = systemTileIdFromBlock(block)
        if (tileId) {
          await hideSystemTile(tileId)
        }
      }
      setDraftLayout(removeBlockFromLayout(draftLayout, blockId))
    },
    [draftLayout],
  )

  const moveBlock = useCallback(
    (blockId: string, x: number, y: number) => {
      if (!draftLayout || !source) {
        return
      }
      setDraftLayout(moveBlockInLayout(draftLayout, blockId, x, y, source.columns))
    },
    [draftLayout, source],
  )

  const addPickerShortcut = useCallback(
    (plugin: PluginRegistryEntry) => {
      if (!draftLayout || !source) {
        return
      }
      const block = createShortcutBlock(plugin, draftLayout, source.columns)
      setDraftLayout({
        ...draftLayout,
        blocks: [...draftLayout.blocks, block],
      })
      setPickerOpen(false)
    },
    [draftLayout, source],
  )

  const addPickerSystemTile = useCallback(
    async (tile: SystemTile) => {
      if (!draftLayout || !source) {
        return
      }
      await restoreSystemTile(tile.id)
      const block = createSystemBlock(tile, draftLayout, source.columns)
      setDraftLayout({
        ...draftLayout,
        blocks: [...draftLayout.blocks, block],
      })
      setPickerOpen(false)
    },
    [draftLayout, source],
  )

  const bindGridLongPress = useCallback(
    (element: HTMLElement | null) => {
      gridElement.current = element
    },
    [],
  )

  useEffect(() => {
    const el = gridElement.current
    if (!el || active) {
      return undefined
    }

    function onPointerDown(event: PointerEvent): void {
      if ((event.target as HTMLElement).closest('.dashboard-block-wrap')) {
        return
      }
      clearLongPress()
      longPressTimer.current = setTimeout(() => {
        enterEdit()
      }, LONG_PRESS_MS)
    }

    function onPointerUp(): void {
      clearLongPress()
    }

    el.addEventListener('pointerdown', onPointerDown)
    el.addEventListener('pointerup', onPointerUp)
    el.addEventListener('pointercancel', onPointerUp)
    el.addEventListener('pointerleave', onPointerUp)
    return () => {
      clearLongPress()
      el.removeEventListener('pointerdown', onPointerDown)
      el.removeEventListener('pointerup', onPointerUp)
      el.removeEventListener('pointercancel', onPointerUp)
      el.removeEventListener('pointerleave', onPointerUp)
    }
  }, [active, clearLongPress, enterEdit])

  useEffect(() => {
    if (!active) {
      return undefined
    }
    function onKeyDown(event: KeyboardEvent): void {
      if (event.key === 'Escape') {
        event.preventDefault()
        cancelEdit()
      }
    }
    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [active, cancelEdit])

  const value = useMemo<EditModeContextValue>(
    () => ({
      active,
      dirty,
      draftLayout,
      collidingIds,
      reducedMotion,
      pickerOpen,
      saving,
      source,
      registerSource: setSource,
      enterEdit,
      cancelEdit,
      saveEdit,
      openPicker: () => setPickerOpen(true),
      closePicker: () => setPickerOpen(false),
      removeBlock,
      moveBlock,
      addPickerShortcut,
      addPickerSystemTile,
      bindGridLongPress,
    }),
    [
      active,
      dirty,
      draftLayout,
      collidingIds,
      reducedMotion,
      pickerOpen,
      saving,
      source,
      enterEdit,
      cancelEdit,
      saveEdit,
      removeBlock,
      moveBlock,
      addPickerShortcut,
      addPickerSystemTile,
      bindGridLongPress,
    ],
  )

  return <EditModeContext.Provider value={value}>{children}</EditModeContext.Provider>
}

export function useEditMode(): EditModeContextValue {
  const ctx = useContext(EditModeContext)
  if (!ctx) {
    throw new Error('useEditMode must be used within EditModeProvider')
  }
  return ctx
}
