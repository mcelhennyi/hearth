/** Square dashboard grid metrics — docs/design/dashboard.md § Primitive cell */

export type GridMetrics = {
  rect: DOMRect
  gap: number
  cellWidth: number
  cellHeight: number
  columns: number
}

export function getGridMetrics(gridEl: HTMLElement, columns: number): GridMetrics | null {
  const rect = gridEl.getBoundingClientRect()
  if (rect.width <= 0) {
    return null
  }
  const style = getComputedStyle(gridEl)
  const rowGap = parseFloat(style.rowGap)
  const columnGap = parseFloat(style.columnGap)
  const gap =
    Number.isFinite(rowGap) && rowGap > 0
      ? rowGap
      : Number.isFinite(columnGap) && columnGap > 0
        ? columnGap
        : parseFloat(style.gap) || 8
  const cellWidth = (rect.width - gap * (columns - 1)) / columns
  const cellHeight = cellWidth
  return { rect, gap, cellWidth, cellHeight, columns }
}

/** Map viewport coordinates to top-left grid cell for a block of size (blockW × blockH). */
export function pointerToCell(
  clientX: number,
  clientY: number,
  metrics: GridMetrics,
  blockW: number,
  blockH: number,
): { x: number; y: number } {
  const { rect, gap, cellWidth, cellHeight, columns } = metrics
  const strideX = cellWidth + gap
  const strideY = cellHeight + gap
  const relX = clientX - rect.left
  const relY = clientY - rect.top
  const x = Math.floor(relX / strideX)
  const y = Math.floor(relY / strideY)
  const maxX = Math.max(0, columns - blockW)
  const maxY = Math.max(0, 64 - blockH)
  return {
    x: Math.min(Math.max(0, x), maxX),
    y: Math.min(Math.max(0, y), maxY),
  }
}
