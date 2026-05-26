import 'fake-indexeddb/auto'
import { beforeEach, describe, expect, it } from 'vitest'

import { readLayoutCache, writeLayoutCache } from './layoutCache'
import type { DashboardLayout } from './types'

const SAMPLE: DashboardLayout = {
  version: 1,
  columns: 4,
  blocks: [{ id: 'b-1', type: 'app-shortcut', plugin: 'groceries', x: 0, y: 0, w: 1, h: 1 }],
}

describe('layoutCache', () => {
  beforeEach(async () => {
    const dbs = await indexedDB.databases()
    await Promise.all(dbs.map((db) => db.name && indexedDB.deleteDatabase(db.name)))
  })

  it('write then read round-trips layout', async () => {
    await writeLayoutCache(SAMPLE)
    const cached = await readLayoutCache()
    expect(cached).toEqual(SAMPLE)
  })

  it('read returns null when empty', async () => {
    expect(await readLayoutCache()).toBeNull()
  })
})
