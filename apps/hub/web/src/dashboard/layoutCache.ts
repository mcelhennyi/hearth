/**
 * Offline cache for GET /api/dashboard/layout — dashboard.md § Offline.
 * IndexedDB store: one record keyed `layout`.
 */

import type { DashboardLayout } from './types'

const DB_NAME = 'hearth-dashboard'
const DB_VERSION = 1
const STORE = 'cache'
const LAYOUT_KEY = 'layout'

function openDb(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION)
    request.onerror = () => reject(request.error ?? new Error('indexedDB open failed'))
    request.onsuccess = () => resolve(request.result)
    request.onupgradeneeded = () => {
      const db = request.result
      if (!db.objectStoreNames.contains(STORE)) {
        db.createObjectStore(STORE)
      }
    }
  })
}

export async function readLayoutCache(): Promise<DashboardLayout | null> {
  if (typeof indexedDB === 'undefined') {
    return null
  }
  const db = await openDb()
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readonly')
    const store = tx.objectStore(STORE)
    const getReq = store.get(LAYOUT_KEY)
    getReq.onerror = () => reject(getReq.error ?? new Error('indexedDB get failed'))
    getReq.onsuccess = () => {
      const value = getReq.result as DashboardLayout | undefined
      resolve(value ?? null)
    }
    tx.oncomplete = () => db.close()
  })
}

export async function writeLayoutCache(layout: DashboardLayout): Promise<void> {
  if (typeof indexedDB === 'undefined') {
    return
  }
  const db = await openDb()
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readwrite')
    const store = tx.objectStore(STORE)
    const putReq = store.put(layout, LAYOUT_KEY)
    putReq.onerror = () => reject(putReq.error ?? new Error('indexedDB put failed'))
    tx.oncomplete = () => {
      db.close()
      resolve()
    }
  })
}
