// Renders plugin chrome slot items (buttons/menus) with visible caps and overflow.
// Spec: docs/design/mantle-ui.md §"Declaring chrome slots" (T-FR-0006-06).

import { useId, useState } from 'react'

import { CHROME_VISIBLE_CAP } from './chromeConstants'
import type { ChromeRegistryEntry } from './useChromeSlotRegistry'
import type { ChromePayload, ChromeSlot } from './types'

export interface ChromeSlotProps {
  slot: ChromeSlot
  items: ChromeRegistryEntry[]
  isDesktop: boolean
  onInvoke: (id: string, itemId?: string) => void
}

function ChromeIcon({ icon }: { icon?: string }) {
  if (!icon) return null
  // v0: render icon string as label glyph (lucide names or short emoji/text).
  return <span className="chrome-btn__icon" aria-hidden="true">{icon.length <= 2 ? icon : icon.slice(0, 1)}</span>
}

function ChromeButtonView({
  payload,
  showLabel,
  onActivate,
}: {
  payload: Extract<ChromePayload, { kind: 'button' }>
  showLabel: boolean
  onActivate: () => void
}) {
  const classes = [
    'chrome-btn',
    payload.variant === 'accent' ? 'chrome-btn--accent' : '',
    showLabel && payload.label ? 'chrome-btn--label' : '',
  ]
    .filter(Boolean)
    .join(' ')

  return (
    <button
      type="button"
      className={classes}
      title={payload.label}
      aria-label={payload.label}
      disabled={payload.disabled}
      onClick={onActivate}
    >
      <ChromeIcon icon={payload.icon} />
      {showLabel && payload.label ? <span className="chrome-btn__text">{payload.label}</span> : null}
      {payload.busy ? <span className="chrome-btn__busy" aria-hidden="true" /> : null}
    </button>
  )
}

function ChromeMenuView({
  payload,
  showLabel,
  onInvokeItem,
}: {
  payload: Extract<ChromePayload, { kind: 'menu' }>
  showLabel: boolean
  onInvokeItem: (itemId: string) => void
}) {
  const menuId = useId()
  const [open, setOpen] = useState(false)

  return (
    <div className="chrome-menu">
      <button
        type="button"
        className={`chrome-btn ${showLabel ? 'chrome-btn--label' : ''}`}
        aria-label={payload.label}
        aria-haspopup="menu"
        aria-expanded={open}
        aria-controls={menuId}
        onClick={() => setOpen((v) => !v)}
      >
        <ChromeIcon icon={payload.icon} />
        {showLabel ? <span className="chrome-btn__text">{payload.label}</span> : null}
      </button>
      {open ? (
        <ul id={menuId} className="chrome-menu__list" role="menu">
          {payload.items.map((item) => (
            <li key={item.id} role="none">
              <button
                type="button"
                role="menuitem"
                className="chrome-menu__item"
                disabled={item.disabled}
                onClick={() => {
                  setOpen(false)
                  onInvokeItem(item.id)
                }}
              >
                {item.label}
              </button>
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  )
}

function ChromeItemView({
  entry,
  showLabel,
  onInvoke,
}: {
  entry: ChromeRegistryEntry
  showLabel: boolean
  onInvoke: (id: string, itemId?: string) => void
}) {
  const { payload } = entry
  if (payload.kind === 'button') {
    return (
      <ChromeButtonView
        payload={payload}
        showLabel={showLabel}
        onActivate={() => onInvoke(payload.id)}
      />
    )
  }
  return (
    <ChromeMenuView
      payload={payload}
      showLabel={showLabel}
      onInvokeItem={(itemId) => onInvoke(payload.id, itemId)}
    />
  )
}

function OverflowMenu({
  overflow,
  showLabel,
  onInvoke,
}: {
  overflow: ChromeRegistryEntry[]
  showLabel: boolean
  onInvoke: (id: string, itemId?: string) => void
}) {
  const menuId = useId()
  const [open, setOpen] = useState(false)

  return (
    <div className="chrome-menu chrome-menu--overflow">
      <button
        type="button"
        className="chrome-btn"
        aria-label="More actions"
        aria-haspopup="menu"
        aria-expanded={open}
        aria-controls={menuId}
        onClick={() => setOpen((v) => !v)}
      >
        <span aria-hidden="true">⋯</span>
      </button>
      {open ? (
        <ul id={menuId} className="chrome-menu__list" role="menu">
          {overflow.map((entry) => {
            const label =
              entry.payload.kind === 'button' ? entry.payload.label : entry.payload.label
            return (
              <li key={entry.id} role="none">
                {entry.payload.kind === 'button' ? (
                  <button
                    type="button"
                    role="menuitem"
                    className="chrome-menu__item"
                    disabled={entry.payload.disabled}
                    onClick={() => {
                      setOpen(false)
                      onInvoke(entry.payload.id)
                    }}
                  >
                    {label}
                  </button>
                ) : (
                  entry.payload.items.map((item) => (
                    <button
                      key={`${entry.id}:${item.id}`}
                      type="button"
                      role="menuitem"
                      className="chrome-menu__item"
                      disabled={item.disabled}
                      onClick={() => {
                        setOpen(false)
                        onInvoke(entry.payload.id, item.id)
                      }}
                    >
                      {item.label}
                    </button>
                  ))
                )}
              </li>
            )
          })}
        </ul>
      ) : null}
    </div>
  )
}

export function ChromeSlot({ slot, items, isDesktop, onInvoke }: ChromeSlotProps) {
  const cap = CHROME_VISIBLE_CAP[slot]
  const visible = items.slice(0, cap)
  const overflow = items.slice(cap)
  const showLabel = isDesktop && slot === 'bottom'

  if (items.length === 0) return null

  const className = slot === 'top' ? 'chrome-slot chrome-slot--top' : 'plugin-bottom-slots'

  return (
    <div className={className} aria-label={slot === 'top' ? 'Plugin actions' : 'Plugin bottom chrome slots'}>
      {visible.map((entry) => (
        <ChromeItemView
          key={entry.id}
          entry={entry}
          showLabel={showLabel}
          onInvoke={onInvoke}
        />
      ))}
      {overflow.length > 0 ? (
        <OverflowMenu overflow={overflow} showLabel={showLabel} onInvoke={onInvoke} />
      ) : null}
    </div>
  )
}
