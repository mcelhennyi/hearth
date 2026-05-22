// @PROJ-U-* — @kindling/mantle postMessage contract types (FR-0006).
//
// Aligned with apps/hub/web/src/shell/types.ts (T-FR-0006-03). Plugins and the
// vanilla bridge import these shapes; the shell is authoritative at runtime.
//
// Source of truth: docs/design/mantle-ui.md.

/** A button slot item registered via `hearth.chrome.mount`. */
export type ChromeButton = {
  kind: "button";
  id: string;
  label: string;
  icon?: string;
  variant?: "default" | "accent";
  busy?: boolean;
  disabled?: boolean;
};

/** A menu slot item registered via `hearth.chrome.mount`. */
export type ChromeMenu = {
  kind: "menu";
  id: string;
  label: string;
  icon?: string;
  items: Array<{
    id: string;
    label: string;
    icon?: string;
    disabled?: boolean;
  }>;
};

export type ChromePayload = ChromeButton | ChromeMenu;
export type ChromeSlot = "top" | "bottom";
export type ChromeSurface = "app" | "dashboard";

/** Plugin iframe lifecycle state as reported by the shell. */
export type FrameState =
  | "mounted"
  | "loading"
  | "slow"
  | "error"
  | "offline";

/** Resolved theme palette pushed via `hearth.theme`. Keys mirror mantle-ui.md. */
export type ThemeTokens = {
  mode: "light" | "dark";
  bg: string;
  surface: string;
  fg: string;
  muted: string;
  accent: string;
  accentFg: string;
};

export type ToastLevel = "info" | "success" | "warning" | "error";
export type HapticStyle = "selection" | "impact" | "notification";

/** Messages the plugin sends to the shell (parent). */
export type InboundMessage =
  | { type: "hearth.title"; title: string }
  | { type: "hearth.ready" }
  | { type: "hearth.toast"; level: ToastLevel; message: string }
  | { type: "hearth.nav"; path: string }
  | { type: "hearth.haptic"; style: HapticStyle }
  | { type: "hearth.notify"; payload: unknown }
  | {
      type: "hearth.chrome.mount";
      slot: ChromeSlot;
      surface: ChromeSurface;
      payload: ChromePayload;
    }
  | {
      type: "hearth.chrome.unmount";
      slot: ChromeSlot;
      surface: ChromeSurface;
      id: string;
    };

/** Messages the shell pushes into the plugin iframe. */
export type OutboundMessage =
  | { type: "hearth.theme"; tokens: ThemeTokens }
  | { type: "hearth.user"; user: { id: string; name?: string; avatarUrl?: string } | null }
  | { type: "hearth.online"; online: boolean }
  | { type: "hearth.frame.state"; state: FrameState }
  | {
      type: "hearth.chrome.resize";
      slot: ChromeSlot;
      rect: { width: number; height: number };
    }
  | {
      type: "hearth.chrome.invoke";
      slot: ChromeSlot;
      surface: ChromeSurface;
      id: string;
      itemId?: string;
    }
  | {
      type: "hearth.chrome.error";
      slot: ChromeSlot;
      surface: ChromeSurface;
      reason: "limit" | "unknown_slot" | "invalid_payload";
    };

export type InboundType = InboundMessage["type"];
export type OutboundType = OutboundMessage["type"];

export type OutboundPayload<T extends OutboundType> = Extract<
  OutboundMessage,
  { type: T }
>;

/** Same-origin guard used by the vanilla bridge message listener. */
export function isSameOriginMessage(event: MessageEvent): boolean {
  return event.origin === window.location.origin;
}

/** Validates shell → plugin payloads at the trust boundary. */
export function isOutboundMessage(value: unknown): value is OutboundMessage {
  if (!value || typeof value !== "object") return false;
  const candidate = value as { type?: unknown };
  if (typeof candidate.type !== "string") return false;
  switch (candidate.type) {
    case "hearth.theme":
    case "hearth.user":
    case "hearth.online":
    case "hearth.frame.state":
    case "hearth.chrome.resize":
    case "hearth.chrome.invoke":
    case "hearth.chrome.error":
      return true;
    default:
      return false;
  }
}
