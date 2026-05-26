/** Dashboard layout and system API shapes — docs/design/dashboard.md */

export type BlockType = 'app-shortcut' | 'widget' | 'system'

export type LayoutBlock = {
  id: string
  type: BlockType
  x: number
  y: number
  w: number
  h: number
  plugin?: string
  surface?: string
}

export type DashboardLayout = {
  version: number
  columns: number
  blocks: LayoutBlock[]
  updated_at?: string | null
}

export type SystemTile = {
  id: string
  title: string
  body: string
  action?: { nav: string }
  hidden_by_user: boolean
  suppressed: boolean
}

export type SystemStrip = {
  id: string
  title: string
  body: string
  action?: { nav: string }
  dismissed: boolean
}

export type PluginRegistryEntry = {
  slug: string
  name: string
  state: string
  kind: string
}

/** Extract tile id from layout block id (`default-system-<tileId>`). */
export function systemTileIdFromBlock(block: LayoutBlock): string | null {
  if (block.type !== 'system') {
    return null
  }
  const prefix = 'default-system-'
  if (block.id.startsWith(prefix)) {
    return block.id.slice(prefix.length)
  }
  if (block.id.startsWith('system-')) {
    return block.id.slice('system-'.length)
  }
  return block.id
}
