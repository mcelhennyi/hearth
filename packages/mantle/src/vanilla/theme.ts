// mantle.theme — subscribe to shell theme pushes and apply :root CSS variables.
// Spec: docs/design/mantle-ui.md § Theme tokens; T-FR-0006-14.

import { isAllowedMessageOrigin } from "../bridge";
import type { InboundPayload, ThemeTokens } from "../types";
import { isInboundMessage } from "../types";
import { applyThemeTokens as applyRootTokens } from "../applyThemeTokens";

export { applyRootTokens as applyThemeTokens };

export type ThemeSubscriber = (tokens: ThemeTokens) => void;

function onThemeMessage(
  event: MessageEvent,
  handler: (msg: InboundPayload<"hearth.theme">) => void,
): void {
  if (!isAllowedMessageOrigin(event.origin)) return;
  if (!isInboundMessage(event.data) || event.data.type !== "hearth.theme") return;
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
        applyRootTokens(msg.tokens);
        cb(msg.tokens);
      });
    }
    window.addEventListener("message", listener);
    return () => window.removeEventListener("message", listener);
  },
};
