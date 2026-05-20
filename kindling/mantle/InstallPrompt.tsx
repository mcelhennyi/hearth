// InstallPrompt — one-time iOS "Add to Home Screen" nudge.
//
// Shown only when:
//   - User agent looks like iOS Safari
//   - App is NOT already running in standalone mode
//   - User has not previously dismissed the prompt (localStorage key)
//
// Matches the install-prompt requirement in mantle-ui.md §"Install prompt".

import { useEffect, useState } from 'react'

const DISMISS_KEY = 'hearth:install-prompt-dismissed'

function isIosSafari(): boolean {
  if (typeof navigator === 'undefined') return false
  const ua = navigator.userAgent
  // iOS Safari: contains "iPhone" or "iPad" AND "Safari" AND NOT "CriOS"/"FxiOS" (Chrome/Firefox on iOS)
  const isIos = /iPhone|iPad/i.test(ua)
  const isSafari = /Safari/i.test(ua) && !/CriOS|FxiOS|EdgiOS/i.test(ua)
  return isIos && isSafari
}

function isStandalone(): boolean {
  if (typeof window === 'undefined') return false
  return (
    window.matchMedia('(display-mode: standalone)').matches ||
    ('standalone' in navigator && Boolean((navigator as Navigator & { standalone?: boolean }).standalone))
  )
}

export function InstallPrompt() {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    if (isIosSafari() && !isStandalone() && !localStorage.getItem(DISMISS_KEY)) {
      setVisible(true)
    }
  }, [])

  function dismiss() {
    localStorage.setItem(DISMISS_KEY, '1')
    setVisible(false)
  }

  if (!visible) return null

  return (
    <div
      role="banner"
      aria-label="Install Hearth prompt"
      className="fixed inset-x-0 bottom-[calc(4rem+var(--hearth-safe-bottom))] z-50 mx-auto max-w-sm rounded-2xl border border-[var(--hearth-surface)] bg-[var(--hearth-surface)] px-4 py-3 shadow-lg"
    >
      <div className="flex items-start justify-between gap-3">
        <p className="text-sm text-[var(--hearth-fg)]">
          Add <strong>Hearth</strong> to your Home Screen for the best experience — tap{' '}
          <span aria-label="Share icon">&#x2b06;</span> then <em>Add to Home Screen</em>.
        </p>
        <button
          type="button"
          onClick={dismiss}
          aria-label="Dismiss install prompt"
          className="shrink-0 rounded-md px-2 py-1 text-xs text-[var(--hearth-muted)] hover:bg-[var(--hearth-bg)]"
        >
          Dismiss
        </button>
      </div>
    </div>
  )
}
