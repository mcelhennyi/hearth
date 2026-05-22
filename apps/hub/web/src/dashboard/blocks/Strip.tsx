import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import type { SystemStrip } from '../types'

type Props = {
  strip: SystemStrip
  columns: number
  onDismissed: () => void
}

export function Strip({ strip, columns, onDismissed }: Props) {
  const navigate = useNavigate()
  const [dismissing, setDismissing] = useState(false)

  async function dismiss(): Promise<void> {
    setDismissing(true)
    try {
      await fetch(`/api/system/strips/${strip.id}/dismiss`, { method: 'POST' })
      onDismissed()
    } finally {
      setDismissing(false)
    }
  }

  return (
    <div
      className="dashboard-block dashboard-block--strip"
      data-testid={`strip-${strip.id}`}
      style={{ gridColumn: `1 / span ${columns}` }}
      role="region"
      aria-label={strip.title}
    >
      <div className="dashboard-strip-text">
        <strong>{strip.title}</strong>
        <span>{strip.body}</span>
      </div>
      {strip.action?.nav ? (
        <button
          type="button"
          className="dashboard-strip-action"
          onClick={() => navigate(strip.action!.nav)}
        >
          Learn more
        </button>
      ) : null}
      <button
        type="button"
        className="dashboard-strip-dismiss"
        aria-label="Dismiss"
        disabled={dismissing}
        onClick={() => void dismiss()}
      >
        Dismiss
      </button>
    </div>
  )
}
