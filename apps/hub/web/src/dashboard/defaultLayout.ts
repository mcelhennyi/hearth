import { findNextPlacement } from './edit/layoutDraft'
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

/** Append 1×1 shortcuts for enabled apps missing from a non-empty saved layout. */
export function mergeMissingAppShortcuts(
  layout: DashboardLayout,
  pluginSlugs: string[],
): DashboardLayout {
  if (pluginSlugs.length === 0) {
    return layout
  }
  const onGrid = new Set(
    layout.blocks
      .filter((b) => b.type === 'app-shortcut' && b.plugin)
      .map((b) => b.plugin as string),
  )
  const missing = pluginSlugs.filter((slug) => !onGrid.has(slug))
  if (missing.length === 0) {
    return layout
  }

  let draft = layout
  const blocks = [...layout.blocks]
  for (const slug of missing) {
    const { x, y } = findNextPlacement(draft, 1, 1, layout.columns)
    blocks.push({
      id: `default-shortcut-${slug}`,
      type: 'app-shortcut',
      plugin: slug,
      x,
      y,
      w: 1,
      h: 1,
    })
    draft = { ...draft, blocks }
  }
  return { ...layout, blocks }
}

export function withDefaultShortcuts(
  layout: DashboardLayout,
  pluginSlugs: string[],
): DashboardLayout {
  if (pluginSlugs.length === 0) {
    return layout
  }
  if (layout.blocks.length === 0) {
    return {
      ...layout,
      blocks: defaultShortcutBlocks(pluginSlugs, layout.columns),
    }
  }
  return mergeMissingAppShortcuts(layout, pluginSlugs)
}
