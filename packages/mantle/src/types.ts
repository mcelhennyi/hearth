// @PROJ-U-* — @kindling/mantle placeholder types (FR-0006 T-FR-0006-10 scaffold).
//
// These are intentionally minimal stubs so dependents (apps/hub/web shell,
// downstream plugin packages) can `import type { ... } from "@kindling/mantle/types"`
// today. The postMessage contract and chrome surface are fully refined in
// T-FR-0006-03 (postMessage protocol) and T-FR-0006-12 (hooks). When those
// tickets land they tighten / replace these declarations.
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

/** Plugin iframe lifecycle state as reported by the shell. */
export type FrameState = "Mounted" | "Loading" | "Slow" | "Error" | "Offline";

/** Resolved theme palette pushed via `hearth.theme`. Values mirror tokens.css. */
export type ThemeTokens = {
  mode: "light" | "dark";
  bg: string;
  surface: string;
  fg: string;
  muted: string;
  accent: string;
  accentFg: string;
  error: string;
};

/** Messages the shell pushes into the plugin iframe. */
export type InboundMessage =
  | { type: "hearth.theme"; tokens: ThemeTokens }
  | { type: "hearth.user"; user: { id: string; name?: string } | null }
  | { type: "hearth.online"; online: boolean }
  | { type: "hearth.frame.state"; state: FrameState }
  | { type: "hearth.chrome.resize"; slot: string; rect: { width: number; height: number } }
  | { type: "hearth.chrome.invoke"; slot: string; surface: string; id: string; itemId?: string }
  | { type: "hearth.chrome.error"; slot: string; surface: string; reason: string };

/** Messages a plugin sends out to the shell. */
export type OutboundMessage =
  | { type: "hearth.title"; title: string }
  | { type: "hearth.ready" }
  | { type: "hearth.toast"; level: "info" | "warn" | "error" | "success"; message: string }
  | { type: "hearth.nav"; path: string }
  | { type: "hearth.haptic"; style: "selection" | "impact" | "notification" }
  | { type: "hearth.notify"; payload: unknown }
  | {
      type: "hearth.chrome.mount";
      slot: string;
      surface: string;
      payload: ChromeButton | ChromeMenu;
    }
  | { type: "hearth.chrome.unmount"; slot: string; surface: string; id?: string };
