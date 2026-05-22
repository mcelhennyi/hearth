import type { LayoutBlock } from '../types'

type Props = {
  block: LayoutBlock
}

/** P3 deferred — placeholder per dashboard.md MVP policy. */
export function Widget({ block }: Props) {
  const label = block.plugin ?? 'Widget'
  return (
    <div
      className="dashboard-block dashboard-block--widget is-placeholder"
      data-testid={`block-widget-${block.id}`}
      data-span-h={block.h}
      aria-label={`${label} widget`}
    >
      <div className="dashboard-widget-inner">
        <span className="dashboard-widget-title">{label}</span>
        <span className="dashboard-widget-metric">Widget support coming soon</span>
      </div>
    </div>
  )
}
