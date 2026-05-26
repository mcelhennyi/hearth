/** Launcher / shortcut visuals — aligned with docs/design/mockups/dashboard-*.html */

export type PluginNavIcon = {
  emoji: string
  gradient: string
}

export const PLUGIN_NAV_ICONS: Record<string, PluginNavIcon> = {
  groceries: { emoji: '🛒', gradient: 'linear-gradient(145deg, #34d399, #059669)' },
  recipes: { emoji: '📖', gradient: 'linear-gradient(145deg, #fbbf24, #d97706)' },
  ideas: { emoji: '💡', gradient: 'linear-gradient(145deg, #a78bfa, #7c3aed)' },
  scheduler: { emoji: '📅', gradient: 'linear-gradient(145deg, #60a5fa, #2563eb)' },
  chores: { emoji: '🧹', gradient: 'linear-gradient(145deg, #2dd4bf, #0d9488)' },
  photos: { emoji: '📷', gradient: 'linear-gradient(145deg, #f472b6, #db2777)' },
  notes: { emoji: '📝', gradient: 'linear-gradient(145deg, #fde047, #ca8a04)' },
  budget: { emoji: '💰', gradient: 'linear-gradient(145deg, #4ade80, #16a34a)' },
}

const DEFAULT_ICON: PluginNavIcon = {
  emoji: '◆',
  gradient: 'linear-gradient(145deg, #ff6a3d, #b83a14)',
}

export function iconForPlugin(slug: string): PluginNavIcon {
  return PLUGIN_NAV_ICONS[slug] ?? DEFAULT_ICON
}
