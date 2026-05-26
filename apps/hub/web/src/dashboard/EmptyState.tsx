// Dashboard empty state — docs/design/dashboard.md § Empty state (DG-U4).
// Ticket: T-FR-0006-08.

import { useSettings } from '../shell/SettingsContext'

/** Centered empty dashboard when layout.blocks is empty. */
export function EmptyState() {
  const { openSettings } = useSettings()

  return (
    <section className="dashboard-empty" data-testid="dashboard-empty-state" aria-labelledby="dashboard-empty-headline">
      <img
        src="/logo.svg"
        alt=""
        width={64}
        height={64}
        className="dashboard-empty-icon"
        aria-hidden
      />
      <h2 id="dashboard-empty-headline" className="dashboard-empty-headline">
        Your dashboard is empty.
      </h2>
      <p className="dashboard-empty-body">
        Enable plugins in Settings to populate your home grid.
      </p>
      <button
        type="button"
        className="dashboard-empty-cta"
        onClick={() => openSettings('plugins')}
      >
        Open Settings
      </button>
    </section>
  )
}
