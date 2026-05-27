// Shared postMessage protocol types for the Mantle shell ↔ plugin iframe bridge.
// Spec: docs/design/mantle-ui.md §"postMessage protocol" and §"Declaring chrome slots".
//
// These types are reused by:
//   - apps/hub/web/src/shell/usePostMessageBridge.ts (this feature, T-FR-0006-03)
//   - other shell wiring (T-FR-0006-05 frame state UI, T-FR-0006-06 chrome slots, …)
//   - @kindling/mantle (T-FR-0006-10 / T-FR-0006-12 plugin-side useMantle)
//
// The bridge guarantees:
//   - Only same-origin messages are accepted (`event.origin === window.location.origin`).
//   - Outbound messages target a specific HTMLIFrameElement (or all plugin iframes).
//   - Subscribers see a parsed, narrowed payload per inbound type.

// ---------------------------------------------------------------------------
// Theme + user payloads
// ---------------------------------------------------------------------------

export interface ThemeTokens {
  // CSS custom property values matching the table in mantle-ui.md §"Theme tokens".
  // Keys mirror the `--hearth-*` property names without the `--hearth-` prefix.
  bg: string
  surface: string
  fg: string
  muted: string
  accent: string
  accentFg: string
  // Mode hint so plugins can flip their own colour schemes if they choose.
  mode: 'light' | 'dark'
}

export interface UserInfo {
  id: string
  name?: string
  roles?: string[]
  // Avatar URL is optional; plugins must not require it.
  avatarUrl?: string
}

// Plugin frame lifecycle states (mantle-ui.md §"Plugin frame states", DG-U7).
export type FrameState = 'mounted' | 'loading' | 'slow' | 'error' | 'offline'

// ---------------------------------------------------------------------------
// Chrome slot payloads (mantle-ui.md §"Declaring chrome slots", DG-U6)
// ---------------------------------------------------------------------------

export interface ChromeButton {
  kind: 'button'
  id: string
  label: string
  icon?: string
  variant?: 'default' | 'accent'
  busy?: boolean
  disabled?: boolean
}

export interface ChromeMenu {
  kind: 'menu'
  id: string
  label: string
  icon?: string
  items: Array<{ id: string; label: string; icon?: string; disabled?: boolean }>
}

export type ChromePayload = ChromeButton | ChromeMenu
export type ChromeSlot = 'top' | 'bottom'
export type ChromeSurface = 'app' | 'dashboard'

export interface ChromeRect {
  width: number
  height: number
}

// ---------------------------------------------------------------------------
// Inbound messages (plugin → shell)
// ---------------------------------------------------------------------------

export type ToastLevel = 'info' | 'success' | 'warning' | 'error'
export type HapticStyle = 'selection' | 'impact' | 'notification'

export interface InboundTitleMessage {
  type: 'hearth.title'
  title: string
}

export interface InboundToastMessage {
  type: 'hearth.toast'
  level: ToastLevel
  message: string
}

export interface InboundNavMessage {
  type: 'hearth.nav'
  path: string
}

export interface InboundHapticMessage {
  type: 'hearth.haptic'
  style: HapticStyle
}

export interface InboundNotifyMessage {
  type: 'hearth.notify'
  // Opaque payload forwarded to hub per notifications.md; shape evolves separately.
  payload: unknown
}

export interface InboundReadyMessage {
  type: 'hearth.ready'
}

export interface InboundUserRequestMessage {
  type: 'hearth.user.request'
}

export interface InboundChromeMountMessage {
  type: 'hearth.chrome.mount'
  slot: ChromeSlot
  surface: ChromeSurface
  payload: ChromePayload
}

export interface InboundChromeUnmountMessage {
  type: 'hearth.chrome.unmount'
  slot: ChromeSlot
  surface: ChromeSurface
  id: string
}

export type InboundMessage =
  | InboundTitleMessage
  | InboundToastMessage
  | InboundNavMessage
  | InboundHapticMessage
  | InboundNotifyMessage
  | InboundReadyMessage
  | InboundUserRequestMessage
  | InboundChromeMountMessage
  | InboundChromeUnmountMessage

export type InboundType = InboundMessage['type']

export type InboundPayload<T extends InboundType> = Extract<InboundMessage, { type: T }>

// ---------------------------------------------------------------------------
// Outbound messages (shell → plugin)
// ---------------------------------------------------------------------------

export interface OutboundThemeMessage {
  type: 'hearth.theme'
  tokens: ThemeTokens
}

export interface OutboundUserMessage {
  type: 'hearth.user'
  user: UserInfo | null
}

export interface OutboundOnlineMessage {
  type: 'hearth.online'
  online: boolean
}

export interface OutboundFrameStateMessage {
  type: 'hearth.frame.state'
  state: FrameState
}

export interface OutboundChromeInvokeMessage {
  type: 'hearth.chrome.invoke'
  slot: ChromeSlot
  surface: ChromeSurface
  id: string
  itemId?: string
}

export interface OutboundChromeResizeMessage {
  type: 'hearth.chrome.resize'
  slot: ChromeSlot
  rect: ChromeRect
}

export interface OutboundChromeErrorMessage {
  type: 'hearth.chrome.error'
  slot: ChromeSlot
  surface: ChromeSurface
  reason: 'limit' | 'unknown_slot' | 'invalid_payload'
}

export type OutboundMessage =
  | OutboundThemeMessage
  | OutboundUserMessage
  | OutboundOnlineMessage
  | OutboundFrameStateMessage
  | OutboundChromeInvokeMessage
  | OutboundChromeResizeMessage
  | OutboundChromeErrorMessage

export type OutboundType = OutboundMessage['type']

// ---------------------------------------------------------------------------
// Bridge API (returned by usePostMessageBridge)
// ---------------------------------------------------------------------------

export interface BridgeSubscribeOptions {
  /** When set, the handler runs only for messages whose `event.source` is this iframe's contentWindow. */
  frame?: HTMLIFrameElement
}

export interface Bridge {
  subscribe<T extends InboundType>(
    type: T,
    handler: (payload: InboundPayload<T>) => void,
    options?: BridgeSubscribeOptions,
  ): () => void
  pushToPlugin(frame: HTMLIFrameElement, msg: OutboundMessage): void
  broadcastToAllPlugins(msg: OutboundMessage): void
}

// Type guard used by the bridge to validate inbound payloads at the trust boundary.
// Exported so other shell code (and tests) can reuse it.
export function isInboundMessage(value: unknown): value is InboundMessage {
  if (!value || typeof value !== 'object') return false
  const candidate = value as { type?: unknown }
  if (typeof candidate.type !== 'string') return false
  switch (candidate.type) {
    case 'hearth.title':
    case 'hearth.toast':
    case 'hearth.nav':
    case 'hearth.haptic':
    case 'hearth.notify':
    case 'hearth.ready':
    case 'hearth.user.request':
    case 'hearth.chrome.mount':
    case 'hearth.chrome.unmount':
      return true
    default:
      return false
  }
}
