import { describe, expect, it } from 'vitest'

import { pointerToCell, type GridMetrics } from './gridMetrics'

const METRICS: GridMetrics = {
  rect: { left: 0, top: 0, width: 400, height: 800 } as DOMRect,
  gap: 8,
  cellWidth: 94,
  cellHeight: 94,
  columns: 4,
}

describe('pointerToCell', () => {
  it('accounts for grid gap between columns and rows', () => {
    const first = pointerToCell(10, 10, METRICS, 1, 1)
    expect(first).toEqual({ x: 0, y: 0 })

    const secondCol = pointerToCell(102, 10, METRICS, 1, 1)
    expect(secondCol).toEqual({ x: 1, y: 0 })

    const secondRow = pointerToCell(10, 102, METRICS, 1, 1)
    expect(secondRow).toEqual({ x: 0, y: 1 })
  })

  it('clamps to grid bounds for wide blocks', () => {
    const cell = pointerToCell(1000, 1000, METRICS, 2, 1)
    expect(cell.x).toBeLessThanOrEqual(METRICS.columns - 2)
    expect(cell.y).toBeGreaterThanOrEqual(0)
  })
})
