import { useNavigate } from 'react-router-dom'

import type { LayoutBlock } from '../types'

type Props = {
  block: LayoutBlock
  label: string
}

const SHORTCUT_COLORS: Record<string, string> = {
  groceries: 'linear-gradient(145deg, #4ade80, #16a34a)',
  default: 'linear-gradient(145deg, #ff6a3d, #b83a14)',
}

export function AppShortcut({ block, label }: Props) {
  const navigate = useNavigate()
  const slug = block.plugin ?? ''
  const iconBg = SHORTCUT_COLORS[slug] ?? SHORTCUT_COLORS.default
  const initial = label.charAt(0).toUpperCase()

  return (
    <button
      type="button"
      className="dashboard-block dashboard-block--app-shortcut"
      data-testid={`block-app-${slug}`}
      aria-label={`Open ${label}`}
      onClick={() => navigate(`/${slug}`)}
    >
      <span className="dashboard-app-icon" style={{ background: iconBg }} aria-hidden>
        {initial}
      </span>
      <span className="dashboard-app-label">{label}</span>
    </button>
  )
}
