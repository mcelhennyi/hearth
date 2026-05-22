// Shell overlays for plugin iframe lifecycle states (mantle-ui.md §"Plugin frame states").

import type { FrameState } from './types'

export interface PluginFrameStatesProps {
  state: FrameState
  pluginName: string
  errorDetail: string | null
  showSlowReload: boolean
  onReload: () => void
  onTryAgain: () => void
  onOpenSettings?: () => void
}

function Spinner() {
  return (
    <div
      className="h-10 w-10 animate-spin rounded-full border-2 border-[var(--hearth-accent)] border-t-transparent"
      role="status"
      aria-label="Loading"
    />
  )
}

export function PluginFrameStates({
  state,
  pluginName,
  errorDetail,
  showSlowReload,
  onReload,
  onTryAgain,
  onOpenSettings,
}: PluginFrameStatesProps) {
  if (state === 'mounted') {
    return null
  }

  const scrimClass =
    'pointer-events-auto absolute inset-0 z-10 flex flex-col items-center justify-center bg-[color-mix(in_srgb,var(--hearth-bg)_88%,transparent)] px-4 pt-[var(--hearth-safe-top)] pb-[var(--hearth-safe-bottom)]'

  if (state === 'loading' || state === 'slow') {
    return (
      <div className={scrimClass} aria-live="polite" aria-busy="true">
        <Spinner />
        <p className="mt-4 text-center text-lg font-medium text-[var(--hearth-fg)]">{pluginName}</p>
        {state === 'slow' && (
          <p className="mt-2 text-center text-sm text-[var(--hearth-muted)]">
            Still loading {pluginName}…
          </p>
        )}
        {showSlowReload && (
          <button
            type="button"
            onClick={onReload}
            className="mt-6 rounded-lg bg-[var(--hearth-accent)] px-4 py-2 text-sm font-medium text-[var(--hearth-accent-fg)]"
          >
            Reload
          </button>
        )}
      </div>
    )
  }

  if (state === 'offline') {
    return (
      <div className={scrimClass} role="status">
        <div className="w-full max-w-sm rounded-2xl border border-[var(--hearth-surface)] bg-[var(--hearth-surface)] p-6 text-center shadow-sm">
          <h2 className="text-lg font-semibold text-[var(--hearth-fg)]">You&apos;re offline</h2>
          <p className="mt-2 text-sm text-[var(--hearth-muted)]">{pluginName}</p>
          <button
            type="button"
            onClick={onTryAgain}
            className="mt-5 rounded-lg bg-[var(--hearth-accent)] px-4 py-2 text-sm font-medium text-[var(--hearth-accent-fg)]"
          >
            Try again
          </button>
        </div>
      </div>
    )
  }

  // error
  return (
    <div className={scrimClass} role="alert">
      <div className="w-full max-w-sm rounded-2xl border border-[var(--hearth-surface)] bg-[var(--hearth-surface)] p-6 text-center shadow-sm">
        <h2 className="text-lg font-semibold text-[var(--hearth-fg)]">{pluginName} failed to load</h2>
        <div className="mt-4 flex flex-wrap justify-center gap-2">
          <button
            type="button"
            onClick={onReload}
            className="rounded-lg bg-[var(--hearth-accent)] px-4 py-2 text-sm font-medium text-[var(--hearth-accent-fg)]"
          >
            Reload
          </button>
          <button
            type="button"
            onClick={onOpenSettings}
            className="rounded-lg border border-[var(--hearth-muted)] px-4 py-2 text-sm text-[var(--hearth-fg)]"
          >
            Open Settings
          </button>
        </div>
        {errorDetail && (
          <details className="mt-4 text-left text-xs text-[var(--hearth-muted)]">
            <summary className="cursor-pointer">Details</summary>
            <p className="mt-2 break-words font-mono">{errorDetail}</p>
          </details>
        )}
      </div>
    </div>
  )
}
