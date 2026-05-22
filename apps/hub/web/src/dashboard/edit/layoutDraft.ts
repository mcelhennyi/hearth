import type { DashboardLayout, LayoutBlock, PluginRegistryEntry, SystemTile } from '../types'
import { systemTileIdFromBlock } from '../types'

export function cloneLayout(layout: DashboardLayout): DashboardLayout {
  return {
    ...layout,
    blocks: layout.blocks.map((b) => ({ ...b })),
  }
}

export function clampBlockOrigin(
  block: LayoutBlock,
  x: number,
  y: number,
  columns: number,
): { x: number; y: number } {
  const maxX = Math.max(0, columns - block.w)
  const maxY = Math.max(0, 64 - block.h)
  return {
    x: Math.min(Math.max(0, x), maxX),
    y: Math.min(Math.max(0, y), maxY),
  }
}

export function moveBlockInLayout(
  layout: DashboardLayout,
  blockId: string,
  x: number,
  y: number,
  columns: number,
): DashboardLayout {
  const next = cloneLayout(layout)
  next.columns = columns
  const block = next.blocks.find((b) => b.id === blockId)
  if (!block) {
    return next
  }
  const origin = clampBlockOrigin(block, x, y, columns)
  block.x = origin.x
  block.y = origin.y
  return next
}

export function removeBlockFromLayout(layout: DashboardLayout, blockId: string): DashboardLayout {
  const next = cloneLayout(layout)
  next.blocks = next.blocks.filter((b) => b.id !== blockId)
  return next
}

export function pluginSlugsOnGrid(layout: DashboardLayout): Set<string> {
  const slugs = new Set<string>()
  for (const block of layout.blocks) {
    if (block.type === 'app-shortcut' && block.plugin) {
      slugs.add(block.plugin)
    }
  }
  return slugs
}

export function systemTileIdsOnGrid(layout: DashboardLayout): Set<string> {
  const ids = new Set<string>()
  for (const block of layout.blocks) {
    if (block.type === 'system') {
      const tileId = systemTileIdFromBlock(block)
      if (tileId) {
        ids.add(tileId)
      }
    }
  }
  return ids
}

export function findNextPlacement(
  layout: DashboardLayout,
  w: number,
  h: number,
  columns: number,
): { x: number; y: number } {
  const occupied = new Set<string>()
  for (const block of layout.blocks) {
    for (let dy = 0; dy < block.h; dy += 1) {
      for (let dx = 0; dx < block.w; dx += 1) {
        occupied.add(`${block.x + dx},${block.y + dy}`)
      }
    }
  }
  for (let y = 0; y < 32; y += 1) {
    for (let x = 0; x <= columns - w; x += 1) {
      let fits = true
      for (let dy = 0; dy < h && fits; dy += 1) {
        for (let dx = 0; dx < w; dx += 1) {
          if (occupied.has(`${x + dx},${y + dy}`)) {
            fits = false
            break
          }
        }
      }
      if (fits) {
        return { x, y }
      }
    }
  }
  return { x: 0, y: 0 }
}

export function createShortcutBlock(
  plugin: PluginRegistryEntry,
  layout: DashboardLayout,
  columns: number,
): LayoutBlock {
  const { x, y } = findNextPlacement(layout, 1, 1, columns)
  return {
    id: `edit-shortcut-${plugin.slug}-${Date.now()}`,
    type: 'app-shortcut',
    plugin: plugin.slug,
    x,
    y,
    w: 1,
    h: 1,
  }
}

export function createSystemBlock(tile: SystemTile, layout: DashboardLayout, columns: number): LayoutBlock {
  const { x, y } = findNextPlacement(layout, 1, 1, columns)
  return {
    id: `default-system-${tile.id}`,
    type: 'system',
    x,
    y,
    w: 1,
    h: 1,
  }
}

export type PickerItem =
  | { kind: 'app-shortcut'; plugin: PluginRegistryEntry }
  | { kind: 'system'; tile: SystemTile }

export function listPickerItems(
  layout: DashboardLayout,
  plugins: PluginRegistryEntry[],
  allTiles: SystemTile[],
): PickerItem[] {
  const onGridPlugins = pluginSlugsOnGrid(layout)
  const onGridTiles = systemTileIdsOnGrid(layout)
  const items: PickerItem[] = []
  for (const plugin of plugins) {
    if (!onGridPlugins.has(plugin.slug)) {
      items.push({ kind: 'app-shortcut', plugin })
    }
  }
  for (const tile of allTiles) {
    if (tile.hidden_by_user && !onGridTiles.has(tile.id) && !tile.suppressed) {
      items.push({ kind: 'system', tile })
    }
  }
  return items
}
