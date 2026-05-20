import { useEffect, useState } from 'react'

export type PluginNavEntry = {
  slug: string
  name: string
  showInTabBar: boolean
  order: number
}

type RegistryPlugin = {
  slug?: string
  name?: string
  state?: string
  ui?: {
    nav?: {
      show_in_tab_bar?: boolean
      order?: number
    }
  }
}

function toNavEntry(plugin: RegistryPlugin): PluginNavEntry | null {
  if (!plugin.slug || plugin.state !== 'enabled') {
    return null
  }
  return {
    slug: plugin.slug,
    name: plugin.name ?? plugin.slug,
    showInTabBar: plugin.ui?.nav?.show_in_tab_bar ?? true,
    order: plugin.ui?.nav?.order ?? 0,
  }
}

export function usePlugins(): PluginNavEntry[] {
  const [plugins, setPlugins] = useState<PluginNavEntry[]>([])

  useEffect(() => {
    let cancelled = false

    async function load(): Promise<void> {
      try {
        const response = await fetch('/api/plugins')
        if (!response.ok) {
          return
        }
        const payload = (await response.json()) as RegistryPlugin[] | { plugins?: RegistryPlugin[] }
        const rows = Array.isArray(payload) ? payload : (payload.plugins ?? [])
        const entries = rows
          .map(toNavEntry)
          .filter((entry): entry is PluginNavEntry => entry !== null && entry.showInTabBar)
          .sort((a, b) => a.order - b.order || a.name.localeCompare(b.name))
        if (!cancelled) {
          setPlugins(entries)
        }
      } catch {
        // Registry API not available yet (T-FR-0001-02); hub-only chrome.
      }
    }

    void load()
    return () => {
      cancelled = true
    }
  }, [])

  return plugins
}
