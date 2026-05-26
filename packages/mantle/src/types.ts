// @PROJ-U-* — @kindling/mantle postMessage contract types (FR-0006 T-FR-0006-12).
//
// Plugin-centric naming (inverse of apps/hub/web/src/shell/types.ts):
//   - InboundMessage  = shell → plugin iframe
//   - OutboundMessage = plugin → shell
//
// Field shapes match the shell bridge (T-FR-0006-03). Source of truth:
// docs/design/mantle-ui.md §"postMessage protocol".

// ---------------------------------------------------------------------------
// Theme + user payloads
// ---------------------------------------------------------------------------

export interface ThemeTokens {
  bg: string;
  surface: string;
  fg: string;
  muted: string;
  accent: string;
  accentFg: string;
  mode: "light" | "dark";
}

export interface UserInfo {
  id: string;
  name?: string;
  avatarUrl?: string;
}

export type FrameState = "mounted" | "loading" | "slow" | "error" | "offline";

// ---------------------------------------------------------------------------
// Chrome slot payloads
// ---------------------------------------------------------------------------

export interface ChromeButton {
  kind: "button";
  id: string;
  label: string;
  icon?: string;
  variant?: "default" | "accent";
  busy?: boolean;
  disabled?: boolean;
}

export interface ChromeMenu {
  kind: "menu";
  id: string;
  label: string;
  icon?: string;
  items: Array<{ id: string; label: string; icon?: string; disabled?: boolean }>;
}

export type ChromePayload = ChromeButton | ChromeMenu;
export type ChromeSlot = "top" | "bottom";
export type ChromeSurface = "app" | "dashboard";
export type ChromeErrorReason = "limit" | "unknown_slot" | "invalid_payload";

export interface ChromeRect {
  width: number;
  height: number;
}

// ---------------------------------------------------------------------------
// Inbound messages (shell → plugin)
// ---------------------------------------------------------------------------

export interface InboundThemeMessage {
  type: "hearth.theme";
  tokens: ThemeTokens;
}

export interface InboundUserMessage {
  type: "hearth.user";
  user: UserInfo | null;
}

export interface InboundOnlineMessage {
  type: "hearth.online";
  online: boolean;
}

export interface InboundFrameStateMessage {
  type: "hearth.frame.state";
  state: FrameState;
}

export interface InboundChromeInvokeMessage {
  type: "hearth.chrome.invoke";
  slot: ChromeSlot;
  surface: ChromeSurface;
  id: string;
  itemId?: string;
}

export interface InboundChromeResizeMessage {
  type: "hearth.chrome.resize";
  slot: ChromeSlot;
  rect: ChromeRect;
}

export interface InboundChromeErrorMessage {
  type: "hearth.chrome.error";
  slot: ChromeSlot;
  surface: ChromeSurface;
  reason: ChromeErrorReason;
}

export type InboundMessage =
  | InboundThemeMessage
  | InboundUserMessage
  | InboundOnlineMessage
  | InboundFrameStateMessage
  | InboundChromeInvokeMessage
  | InboundChromeResizeMessage
  | InboundChromeErrorMessage;

export type InboundType = InboundMessage["type"];

export type InboundPayload<T extends InboundType> = Extract<
  InboundMessage,
  { type: T }
>;

// ---------------------------------------------------------------------------
// Outbound messages (plugin → shell)
// ---------------------------------------------------------------------------

export type ToastLevel = "info" | "success" | "warning" | "error";
export type HapticStyle = "selection" | "impact" | "notification";

export interface OutboundTitleMessage {
  type: "hearth.title";
  title: string;
}

export interface OutboundToastMessage {
  type: "hearth.toast";
  level: ToastLevel;
  message: string;
}

export interface OutboundNavMessage {
  type: "hearth.nav";
  path: string;
}

export interface OutboundHapticMessage {
  type: "hearth.haptic";
  style: HapticStyle;
}

export interface OutboundNotifyMessage {
  type: "hearth.notify";
  payload: unknown;
}

export interface OutboundReadyMessage {
  type: "hearth.ready";
}

export interface OutboundChromeMountMessage {
  type: "hearth.chrome.mount";
  slot: ChromeSlot;
  surface: ChromeSurface;
  payload: ChromePayload;
}

export interface OutboundChromeUnmountMessage {
  type: "hearth.chrome.unmount";
  slot: ChromeSlot;
  surface: ChromeSurface;
  id: string;
}

/** Overlay escape (plugin → shell). Shell rendering deferred; v0 accepts + logs. */
export type OverlayAction = "open" | "close";

export interface OutboundSheetMessage {
  type: "hearth.sheet";
  action: OverlayAction;
  id: string;
  title?: string;
}

export interface OutboundDialogMessage {
  type: "hearth.dialog";
  action: OverlayAction;
  id: string;
  title?: string;
}

export type OutboundMessage =
  | OutboundTitleMessage
  | OutboundToastMessage
  | OutboundNavMessage
  | OutboundHapticMessage
  | OutboundNotifyMessage
  | OutboundReadyMessage
  | OutboundChromeMountMessage
  | OutboundChromeUnmountMessage
  | OutboundSheetMessage
  | OutboundDialogMessage;

export type OutboundType = OutboundMessage["type"];

// ---------------------------------------------------------------------------
// Plugin bridge API
// ---------------------------------------------------------------------------

export interface PluginBridge {
  /** True when running inside a parent shell iframe. */
  readonly embedded: boolean;
  post(msg: OutboundMessage): void;
  subscribe<T extends InboundType>(
    type: T,
    handler: (payload: InboundPayload<T>) => void,
  ): () => void;
  destroy(): void;
}

export function isInboundMessage(value: unknown): value is InboundMessage {
  if (!value || typeof value !== "object") return false;
  const candidate = value as { type?: unknown };
  if (typeof candidate.type !== "string") return false;
  switch (candidate.type) {
    case "hearth.theme":
    case "hearth.user":
    case "hearth.online":
    case "hearth.frame.state":
    case "hearth.chrome.invoke":
    case "hearth.chrome.resize":
    case "hearth.chrome.error":
      return true;
    default:
      return false;
  }
}
