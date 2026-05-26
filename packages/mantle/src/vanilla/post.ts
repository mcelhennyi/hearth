// Plugin → shell postMessage helper (T-FR-0006-14).
//
// Outbound from the iframe uses the same target origin as the shell bridge so
// cross-origin parents never receive plugin traffic.

import type { OutboundMessage } from "../types";

export function postToParent(msg: OutboundMessage): void {
  if (typeof window === "undefined") return;
  if (window.parent === window) return;
  window.parent.postMessage(msg, window.location.origin);
}
