import type { DashboardLayout } from './types'

/** Client-side default shortcuts when API layout is empty but plugins are enabled. */
export function defaultShortcutBlocks(
  pluginSlugs: string[],
  columns = 4,
): DashboardLayout['blocks'] {
  return pluginSlugs.map((slug, index) => ({
    id: `default-shortcut-${slug}`,
    type: 'app-shortcut' as const,
    plugin: slug,
    x: index % columns,
    y: Math.floor(index / columns),
    w: 1,
    h: 1,
  }))
}

export function withDefaultShortcuts(
  layout: DashboardLayout,
  pluginSlugs: string[],
): DashboardLayout {
  if (layout.blocks.length > 0 || pluginSlugs.length === 0) {
    return layout
  }
  return {
    ...layout,
    blocks: defaultShortcutBlocks(pluginSlugs, layout.columns),
  }
}
