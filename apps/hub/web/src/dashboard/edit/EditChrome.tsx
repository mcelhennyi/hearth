import { useEditMode } from './EditModeContext'

type Props = {
  isDesktop: boolean
  isDashboard: boolean
}

/** Top-bar edit controls — docs/design/dashboard.md § Edit mode */
export function EditChrome({ isDesktop, isDashboard }: Props) {
  const edit = useEditMode()

  if (!isDashboard) {
    return null
  }

  if (edit.active) {
    return (
      <div className="dashboard-edit-chrome" data-testid="dashboard-edit-chrome">
        {edit.collidingIds.size > 0 ? (
          <p className="dashboard-edit-collision-banner" data-testid="dashboard-edit-collision-banner" role="alert">
            Two blocks are overlapping; resolve before saving.
          </p>
        ) : null}
        <div className="dashboard-edit-chrome-actions">
          <button
            type="button"
            className="dashboard-edit-btn dashboard-edit-btn--add"
            data-testid="dashboard-edit-add"
            aria-label="Add block"
            onClick={edit.openPicker}
          >
            +
          </button>
          <button
            type="button"
            className="dashboard-edit-btn"
            data-testid="dashboard-edit-cancel"
            onClick={edit.cancelEdit}
          >
            Cancel
          </button>
          <button
            type="button"
            className="dashboard-edit-btn dashboard-edit-btn--primary"
            data-testid="dashboard-edit-done"
            disabled={edit.collidingIds.size > 0 || edit.saving || edit.source?.offline}
            onClick={() => void edit.saveEdit()}
          >
            Done
          </button>
        </div>
      </div>
    )
  }

  return (
    <button
      type="button"
      className="dashboard-edit-enter"
      data-testid="dashboard-edit-enter"
      onClick={edit.enterEdit}
    >
      Edit
    </button>
  )
}
