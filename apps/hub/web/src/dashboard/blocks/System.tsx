import { useNavigate } from 'react-router-dom'

import type { LayoutBlock, SystemTile } from '../types'
import { systemTileIdFromBlock } from '../types'

type Props = {
  block: LayoutBlock
  tile: SystemTile | undefined
}

const TILE_ICONS: Record<string, string> = {
  'ca-trust': '🔐',
  'hub-healthy': '✓',
  'pi-online': '◉',
}

export function SystemBlock({ block, tile }: Props) {
  const navigate = useNavigate()
  const tileId = systemTileIdFromBlock(block) ?? block.id
  const title = tile?.title ?? tileId
  const body = tile?.body ?? ''
  const icon = TILE_ICONS[tileId] ?? '⚙'

  function handleActivate(): void {
    const nav = tile?.action?.nav
    if (nav) {
      navigate(nav)
    }
  }

  return (
    <button
      type="button"
      className="dashboard-block dashboard-block--system"
      data-testid={`block-system-${tileId}`}
      aria-label={title}
      onClick={handleActivate}
    >
      <span className="dashboard-system-icon" aria-hidden>
        {icon}
      </span>
      <span className="dashboard-system-label">{title}</span>
      {body ? <span className="dashboard-system-body">{body}</span> : null}
    </button>
  )
}
