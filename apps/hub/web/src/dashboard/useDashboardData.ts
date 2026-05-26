import { useCallback, useEffect, useState } from 'react'

import { readLayoutCache, writeLayoutCache } from './layoutCache'
import { withDefaultShortcuts } from './defaultLayout'
import type { DashboardLayout, PluginRegistryEntry, SystemStrip, SystemTile } from './types'

export type DashboardDataState = {
  layout: DashboardLayout | null
  tiles: SystemTile[]
  /** Full catalogue including user-hidden tiles (edit picker). */
  allTiles: SystemTile[]
  strip: SystemStrip | null
  plugins: PluginRegistryEntry[]
  loading: boolean
  offline: boolean
  error: string | null
  refresh: () => void
  setLayout: (layout: DashboardLayout) => void
}

const EMPTY_LAYOUT: DashboardLayout = { version: 1, columns: 4, blocks: [] }

async function fetchJson<T>(url: string): Promise<T | null> {
  const response = await fetch(url)
  if (!response.ok) {
    return null
  }
  return (await response.json()) as T
}

export function useDashboardData(): DashboardDataState {
  const [layout, setLayout] = useState<DashboardLayout | null>(null)
  const [tiles, setTiles] = useState<SystemTile[]>([])
  const [allTiles, setAllTiles] = useState<SystemTile[]>([])
  const [strip, setStrip] = useState<SystemStrip | null>(null)
  const [plugins, setPlugins] = useState<PluginRegistryEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [offline, setOffline] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [tick, setTick] = useState(0)

  const refresh = useCallback(() => setTick((n) => n + 1), [])

  useEffect(() => {
    let cancelled = false

    async function load(): Promise<void> {
      setLoading(true)
      setError(null)
      setOffline(false)

      try {
        const [layoutRes, tilesRes, stripRes, pluginsRes] = await Promise.all([
          fetchJson<DashboardLayout>('/api/dashboard/layout'),
          fetchJson<{ tiles: SystemTile[] }>('/api/system/tiles'),
          fetchJson<{ strip: SystemStrip | null }>('/api/system/strips'),
          fetchJson<PluginRegistryEntry[] | { plugins?: PluginRegistryEntry[] }>('/api/plugins'),
        ])

        if (cancelled) {
          return
        }

        const pluginRows = Array.isArray(pluginsRes)
          ? pluginsRes
          : (pluginsRes?.plugins ?? [])
        const enabledApps = pluginRows.filter((p) => p.state === 'enabled' && p.kind === 'app')
        const appSlugs = enabledApps.map((p) => p.slug)
        setPlugins(enabledApps)

        if (layoutRes) {
          const merged = withDefaultShortcuts(layoutRes, appSlugs)
          setLayout(merged)
          await writeLayoutCache(merged)
        } else {
          const cached = await readLayoutCache()
          if (cached) {
            setLayout(withDefaultShortcuts(cached, appSlugs))
            setOffline(true)
          } else {
            setLayout(withDefaultShortcuts(EMPTY_LAYOUT, appSlugs))
          }
        }

        const catalogue = tilesRes?.tiles ?? []
        setAllTiles(catalogue)
        setTiles(catalogue.filter((t) => !t.hidden_by_user && !t.suppressed))
        setStrip(stripRes?.strip && !stripRes.strip.dismissed ? stripRes.strip : null)
      } catch {
        if (cancelled) {
          return
        }
        const cached = await readLayoutCache()
        if (cached) {
          setLayout(cached)
          setOffline(true)
        } else {
          setLayout(EMPTY_LAYOUT)
          setError('Could not load dashboard.')
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    void load()
    return () => {
      cancelled = true
    }
  }, [tick])

  const applyLayout = useCallback((next: DashboardLayout) => {
    setLayout(next)
    void writeLayoutCache(next)
  }, [])

  return { layout, tiles, allTiles, strip, plugins, loading, offline, error, refresh, setLayout: applyLayout }
}
