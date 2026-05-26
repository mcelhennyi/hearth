import { listPickerItems } from './layoutDraft'
import { useEditMode } from './EditModeContext'

export function BlockPicker() {
  const edit = useEditMode()
  if (!edit.pickerOpen || !edit.draftLayout || !edit.source) {
    return null
  }

  const items = listPickerItems(edit.draftLayout, edit.source.plugins, edit.source.allTiles)
  if (items.length === 0) {
    return (
      <dialog open className="dashboard-edit-picker" data-testid="dashboard-edit-picker">
        <p>No blocks available to add.</p>
        <button type="button" onClick={edit.closePicker}>
          Close
        </button>
      </dialog>
    )
  }

  return (
    <dialog open className="dashboard-edit-picker" data-testid="dashboard-edit-picker">
      <h3 className="dashboard-edit-picker-title">Add to dashboard</h3>
      <ul className="dashboard-edit-picker-list">
        {items.map((item) => {
          if (item.kind === 'app-shortcut') {
            return (
              <li key={`app-${item.plugin.slug}`}>
                <button
                  type="button"
                  data-testid={`picker-app-${item.plugin.slug}`}
                  onClick={() => edit.addPickerShortcut(item.plugin)}
                >
                  {item.plugin.name}
                </button>
              </li>
            )
          }
          return (
            <li key={`system-${item.tile.id}`}>
              <button
                type="button"
                data-testid={`picker-system-${item.tile.id}`}
                onClick={() => void edit.addPickerSystemTile(item.tile)}
              >
                {item.tile.title}
              </button>
            </li>
          )
        })}
      </ul>
      <button type="button" className="dashboard-edit-picker-close" onClick={edit.closePicker}>
        Close
      </button>
    </dialog>
  )
}
