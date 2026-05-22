import {
  useCallback,
  useEffect,
  useRef,
  useState,
  type CSSProperties,
  type PointerEvent as ReactPointerEvent,
} from 'react'

import { AppShortcut } from '../blocks/AppShortcut'
import { Strip } from '../blocks/Strip'
import { SystemBlock } from '../blocks/System'
import { Widget } from '../blocks/Widget'
import type { DashboardLayout, PluginRegistryEntry, SystemStrip, SystemTile } from '../types'
import { systemTileIdFromBlock } from '../types'
import { findCollidingBlockIds } from './collisions'
import { useEditMode } from './EditModeContext'
import { getGridMetrics, pointerToCell } from './gridMetrics'
import { moveBlockInLayout } from './layoutDraft'

export type EditGridProps = {
  viewLayout: DashboardLayout
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

type DragVisual = {
  blockId: string
  dx: number
  dy: number
}

export function EditGrid({
  viewLayout,
  tiles,
  strip,
  plugins,
  columns,
  offline = false,
  onStripDismissed,
}: EditGridProps) {
  const edit = useEditMode()
  const gridRef = useRef<HTMLDivElement>(null)
  const dragBlockId = useRef<string | null>(null)
  const dragOrigin = useRef<{ x: number; y: number } | null>(null)
  const dragGrabOffset = useRef<{ x: number; y: number } | null>(null)
  const dragStartClient = useRef<{ x: number; y: number } | null>(null)
  const [dragVisual, setDragVisual] = useState<DragVisual | null>(null)

  const layout = edit.active && edit.draftLayout ? edit.draftLayout : viewLayout
  const pluginNames = new Map(plugins.map((p) => [p.slug, p.name]))
  const tilesById = new Map(tiles.map((t) => [t.id, t]))

  const endDrag = useCallback(() => {
    dragBlockId.current = null
    dragOrigin.current = null
    dragGrabOffset.current = null
    dragStartClient.current = null
    setDragVisual(null)
  }, [])

  useEffect(() => {
    edit.bindGridLongPress(edit.active ? null : gridRef.current)
    return () => edit.bindGridLongPress(null)
  }, [edit.active, edit.bindGridLongPress])

  useEffect(() => {
    if (!edit.active) {
      endDrag()
    }
  }, [edit.active, endDrag])

  const onBlockPointerDown = useCallback(
    (blockId: string, event: ReactPointerEvent<HTMLDivElement>) => {
      if (!edit.active) {
        return
      }
      if ((event.target as HTMLElement).closest('.dashboard-edit-remove')) {
        return
      }
      event.preventDefault()
      event.stopPropagation()
      const block = layout.blocks.find((b) => b.id === blockId)
      if (!block || !gridRef.current) {
        return
      }
      const wrapRect = event.currentTarget.getBoundingClientRect()
      dragBlockId.current = blockId
      dragOrigin.current = { x: block.x, y: block.y }
      dragGrabOffset.current = {
        x: event.clientX - wrapRect.left,
        y: event.clientY - wrapRect.top,
      }
      dragStartClient.current = { x: event.clientX, y: event.clientY }
      setDragVisual({ blockId, dx: 0, dy: 0 })
      event.currentTarget.setPointerCapture(event.pointerId)
    },
    [edit.active, layout.blocks],
  )

  const onBlockPointerMove = useCallback((event: ReactPointerEvent<HTMLDivElement>) => {
    if (!dragBlockId.current || !dragStartClient.current) {
      return
    }
    event.preventDefault()
    const start = dragStartClient.current
    setDragVisual({
      blockId: dragBlockId.current,
      dx: event.clientX - start.x,
      dy: event.clientY - start.y,
    })
  }, [])

  const onBlockPointerUp = useCallback(
    (blockId: string, event: ReactPointerEvent<HTMLDivElement>) => {
      if (!edit.active) {
        return
      }
      if (dragBlockId.current === blockId) {
        const block = layout.blocks.find((b) => b.id === blockId)
        const origin = dragOrigin.current
        const grab = dragGrabOffset.current
        const grid = gridRef.current
        if (block && origin && grab && grid) {
          const metrics = getGridMetrics(grid, columns)
          if (metrics) {
            const cell = pointerToCell(
              event.clientX - grab.x,
              event.clientY - grab.y,
              metrics,
              block.w,
              block.h,
            )
            const preview = moveBlockInLayout(layout, blockId, cell.x, cell.y, columns)
            const colliding = findCollidingBlockIds(preview.blocks)
            if (colliding.has(blockId)) {
              edit.moveBlock(blockId, origin.x, origin.y)
            } else {
              edit.moveBlock(blockId, cell.x, cell.y)
            }
          }
        }
        endDrag()
      }
      try {
        event.currentTarget.releasePointerCapture(event.pointerId)
      } catch {
        /* capture may already be released */
      }
    },
    [columns, edit, endDrag, layout],
  )

  const onBlockPointerCancel = useCallback(
    (blockId: string, event: ReactPointerEvent<HTMLDivElement>) => {
      if (dragBlockId.current === blockId) {
        const origin = dragOrigin.current
        if (origin) {
          edit.moveBlock(blockId, origin.x, origin.y)
        }
        endDrag()
      }
      try {
        event.currentTarget.releasePointerCapture(event.pointerId)
      } catch {
        /* capture may already be released */
      }
    },
    [edit, endDrag],
  )

  return (
    <div
      className="dashboard-scroll"
      data-testid="dashboard-scroll"
      data-offline={offline ? 'true' : 'false'}
      data-edit-active={edit.active ? 'true' : 'false'}
    >
      {offline ? (
        <p className="dashboard-offline-badge" data-testid="dashboard-offline-badge">
          Offline — showing cached layout
        </p>
      ) : null}
      <div
        ref={gridRef}
        className={[
          'dashboard-grid',
          edit.active ? 'dashboard-grid--edit' : '',
          edit.active && edit.reducedMotion ? 'dashboard-grid--reduced-motion' : '',
        ]
          .filter(Boolean)
          .join(' ')}
        data-testid="dashboard-grid"
        style={{ '--hearth-columns': String(columns) } as CSSProperties}
      >
        {strip ? (
          <div
            className={[
              'dashboard-strip-edit-wrap',
              edit.active ? 'dashboard-strip-edit-wrap--edit' : '',
            ]
              .filter(Boolean)
              .join(' ')}
            style={blockStyle(0, 0, columns, 1)}
          >
            <Strip strip={strip} columns={columns} onDismissed={onStripDismissed} />
            {edit.active ? (
              <button
                type="button"
                className="dashboard-edit-remove dashboard-edit-remove--strip"
                data-testid="dashboard-edit-remove-strip"
                aria-label="Dismiss strip in edit mode"
                onClick={(e) => {
                  e.stopPropagation()
                  onStripDismissed()
                }}
              >
                ×
              </button>
            ) : null}
          </div>
        ) : null}
        {layout.blocks.map((block) => {
          const isDragging = dragVisual?.blockId === block.id
          const style: CSSProperties = {
            ...blockStyle(block.x, block.y, block.w, block.h),
            ...(isDragging && dragVisual
              ? {
                  transform: `translate(${dragVisual.dx}px, ${dragVisual.dy}px)`,
                  zIndex: 20,
                }
              : {}),
          }
          const colliding = edit.collidingIds.has(block.id)
          const wrapClass = [
            'dashboard-block-wrap',
            edit.active ? 'dashboard-block-wrap--edit' : '',
            edit.active && colliding ? 'dashboard-block-wrap--collision' : '',
            edit.active && isDragging ? 'dashboard-block-wrap--dragging' : '',
          ]
            .filter(Boolean)
            .join(' ')

          let inner = null
          if (block.type === 'app-shortcut') {
            const slug = block.plugin ?? ''
            inner = <AppShortcut block={block} label={pluginNames.get(slug) ?? slug} />
          } else if (block.type === 'system') {
            const tileId = systemTileIdFromBlock(block)
            inner = <SystemBlock block={block} tile={tileId ? tilesById.get(tileId) : undefined} />
          } else if (block.type === 'widget') {
            inner = <Widget block={block} />
          }

          return (
            <div
              key={block.id}
              style={style}
              className={wrapClass}
              data-testid={`dashboard-block-wrap-${block.id}`}
              onPointerDown={(e) => onBlockPointerDown(block.id, e)}
              onPointerMove={onBlockPointerMove}
              onPointerUp={(e) => onBlockPointerUp(block.id, e)}
              onPointerCancel={(e) => onBlockPointerCancel(block.id, e)}
            >
              {edit.active ? (
                <>
                  <button
                    type="button"
                    className="dashboard-edit-remove"
                    data-testid={`dashboard-edit-remove-${block.id}`}
                    aria-label="Remove block"
                    onClick={(e) => {
                      e.stopPropagation()
                      void edit.removeBlock(block.id)
                    }}
                  >
                    ×
                  </button>
                  {block.type === 'widget' ? (
                    <span
                      className="dashboard-edit-resize-handle"
                      data-testid={`dashboard-edit-resize-${block.id}`}
                      aria-hidden
                    />
                  ) : null}
                </>
              ) : null}
              <div className={edit.active ? 'dashboard-edit-block-inner' : undefined}>{inner}</div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
