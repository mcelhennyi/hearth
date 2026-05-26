// Built-in shell handlers for inbound postMessage types that do not need subscribers yet.
// Spec: docs/design/mantle-ui.md §"postMessage protocol" (DG-U11 toast/haptic stubs).

import type { HapticStyle, InboundToastMessage } from './types'

/** DG-U11 v0: accept toasts and log until shell-side Toast UI exists. */
export function handleInboundToast(msg: InboundToastMessage): void {
  const line = `[hearth.toast] ${msg.level}: ${msg.message}`
  switch (msg.level) {
    case 'error':
      console.error(line)
      break
    case 'warning':
      console.warn(line)
      break
    default:
      console.info(line)
  }
}

const HAPTIC_MS: Record<HapticStyle, number | number[]> = {
  selection: 10,
  impact: 25,
  notification: [30, 50, 30],
}

/** iOS/Android Vibration API when present; no-op elsewhere (mantle-ui.md). */
export function handleInboundHaptic(style: HapticStyle): void {
  if (typeof navigator === 'undefined' || typeof navigator.vibrate !== 'function') return
  navigator.vibrate(HAPTIC_MS[style])
}
