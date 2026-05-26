import type { LayoutBlock } from '../types'

/** True when two axis-aligned block rectangles overlap (half-open cells). */
export function blocksOverlap(a: LayoutBlock, b: LayoutBlock): boolean {
  return (
    a.x < b.x + b.w &&
    b.x < a.x + a.w &&
    a.y < b.y + b.h &&
    b.y < a.y + a.h
  )
}

/** Ids of every block participating in at least one overlap pair. */
export function findCollidingBlockIds(blocks: LayoutBlock[]): Set<string> {
  const ids = new Set<string>()
  for (let i = 0; i < blocks.length; i += 1) {
    for (let j = i + 1; j < blocks.length; j += 1) {
      if (blocksOverlap(blocks[i], blocks[j])) {
        ids.add(blocks[i].id)
        ids.add(blocks[j].id)
      }
    }
  }
  return ids
}

export function hasCollisions(blocks: LayoutBlock[]): boolean {
  return findCollidingBlockIds(blocks).size > 0
}
