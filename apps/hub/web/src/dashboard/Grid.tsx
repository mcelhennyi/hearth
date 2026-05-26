import type { CSSProperties } from 'react'

import { AppShortcut } from './blocks/AppShortcut'
import { Strip } from './blocks/Strip'
import { SystemBlock } from './blocks/System'
import { Widget } from './blocks/Widget'
import type { DashboardLayout, PluginRegistryEntry, SystemStrip, SystemTile } from './types'
import { systemTileIdFromBlock } from './types'

export type GridProps = {
  layout: DashboardLayout
  tiles: SystemTile[]
  strip: SystemStrip | null
  plugins: PluginRegistryEntry[]
  columns: number
  offline?: boolean
  onStripDismissed: () => void
}

function blockStyle(x: number, y: number, w: number, h: number): CSSProperties {
  return {
    gridColumn: `${x + 1} / span ${w}`,
    gridRow: `${y + 1} / span ${h}`,
  }
}

export function Grid({
  layout,
  tiles,
  strip,
  plugins,
  columns,
  offline = false,
  onStripDismissed,
}: GridProps) {
  const pluginNames = new Map(plugins.map((p) => [p.slug, p.name]))
  const tilesById = new Map(tiles.map((t) => [t.id, t]))

  return (
    <div
      className="dashboard-scroll"
      data-testid="dashboard-scroll"
      data-offline={offline ? 'true' : 'false'}
    >
      {offline ? (
        <p className="dashboard-offline-badge" data-testid="dashboard-offline-badge">
          Offline — showing cached layout
        </p>
      ) : null}
      <div
        className="dashboard-grid"
        data-testid="dashboard-grid"
        style={{ '--hearth-columns': String(columns) } as CSSProperties}
      >
        {strip ? (
          <Strip strip={strip} columns={columns} onDismissed={onStripDismissed} />
        ) : null}
        {layout.blocks.map((block) => {
          const style = blockStyle(block.x, block.y, block.w, block.h)
          if (block.type === 'app-shortcut') {
            const slug = block.plugin ?? ''
            const label = pluginNames.get(slug) ?? slug
            return (
              <div key={block.id} style={style} className="dashboard-block-wrap">
                <AppShortcut block={block} label={label} />
              </div>
            )
          }
          if (block.type === 'system') {
            const tileId = systemTileIdFromBlock(block)
            const tile = tileId ? tilesById.get(tileId) : undefined
            return (
              <div key={block.id} style={style} className="dashboard-block-wrap">
                <SystemBlock block={block} tile={tile} />
              </div>
            )
          }
          if (block.type === 'widget') {
            return (
              <div key={block.id} style={style} className="dashboard-block-wrap">
                <Widget block={block} />
              </div>
            )
          }
          return null
        })}
      </div>
    </div>
  )
}
