// mantle.theme — subscribe to shell theme pushes and apply :root CSS variables.
// Spec: docs/design/mantle-ui.md § Theme tokens; T-FR-0006-14.

import type { OutboundPayload, ThemeTokens } from "../types";
import { isOutboundMessage, isSameOriginMessage } from "../types";

const TOKEN_CSS_VARS: Record<keyof ThemeTokens, string> = {
  bg: "--hearth-bg",
  surface: "--hearth-surface",
  fg: "--hearth-fg",
  muted: "--hearth-muted",
  accent: "--hearth-accent",
  accentFg: "--hearth-accent-fg",
  mode: "--hearth-mode",
};

/** Apply resolved tokens to `document.documentElement` inline styles. */
export function applyThemeTokens(tokens: ThemeTokens): void {
  const root = document.documentElement;
  for (const key of Object.keys(TOKEN_CSS_VARS) as Array<keyof ThemeTokens>) {
    root.style.setProperty(TOKEN_CSS_VARS[key], tokens[key]);
  }
}

export type ThemeSubscriber = (tokens: ThemeTokens) => void;

function onThemeMessage(
  event: MessageEvent,
  handler: (msg: OutboundPayload<"hearth.theme">) => void,
): void {
  if (!isSameOriginMessage(event)) return;
  if (!isOutboundMessage(event.data) || event.data.type !== "hearth.theme") return;
  handler(event.data);
}

export const theme = {
  /**
   * Listen for `hearth.theme` from the shell, apply `--hearth-*` on `:root`, and
   * invoke `cb` with the resolved token object. Returns an unsubscribe function.
   */
  subscribe(cb: ThemeSubscriber): () => void {
    function listener(event: MessageEvent) {
      onThemeMessage(event, (msg) => {
        applyThemeTokens(msg.tokens);
        cb(msg.tokens);
      });
    }
    window.addEventListener("message", listener);
    return () => window.removeEventListener("message", listener);
  },
};
