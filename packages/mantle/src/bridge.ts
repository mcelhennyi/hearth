// Plugin-side postMessage bridge — mirrors apps/hub/web/src/shell/usePostMessageBridge.ts
// with inverted direction (listen for shell pushes, post to parent).
//
// Ticket: T-FR-0006-12. Spec: docs/design/mantle-ui.md §"postMessage protocol".

import type {
  InboundMessage,
  InboundPayload,
  InboundType,
  OutboundMessage,
  PluginBridge,
} from "./types";
import { isInboundMessage } from "./types";

type AnyHandler = (payload: InboundMessage) => void;

function targetOrigin(): string {
  return window.location.origin;
}

/** Same-origin guard used for inbound shell messages. */
export function isAllowedMessageOrigin(origin: string): boolean {
  return origin === targetOrigin();
}

/**
 * Creates a plugin bridge. Call `destroy()` when unmounting (MantleProvider does this).
 * Safe to call outside React — vanilla bridge (T-FR-0006-14) will reuse this module.
 */
export function createPluginBridge(): PluginBridge {
  const listeners = new Map<InboundType, Set<AnyHandler>>();
  const embedded = window.parent !== window;

  function onMessage(event: MessageEvent): void {
    if (!isAllowedMessageOrigin(event.origin)) return;
    if (!isInboundMessage(event.data)) return;
    const msg = event.data;
    const handlers = listeners.get(msg.type);
    if (!handlers || handlers.size === 0) return;
    for (const handler of Array.from(handlers)) {
      try {
        handler(msg);
      } catch (err) {
        console.error("[mantle bridge] subscriber threw for", msg.type, err);
      }
    }
  }

  window.addEventListener("message", onMessage);

  function subscribe<T extends InboundType>(
    type: T,
    handler: (payload: InboundPayload<T>) => void,
  ): () => void {
    let set = listeners.get(type);
    if (!set) {
      set = new Set();
      listeners.set(type, set);
    }
    const wrapped = handler as AnyHandler;
    set.add(wrapped);
    return () => {
      const current = listeners.get(type);
      if (!current) return;
      current.delete(wrapped);
      if (current.size === 0) listeners.delete(type);
    };
  }

  function post(msg: OutboundMessage): void {
    if (!embedded) return;
    window.parent.postMessage(msg, targetOrigin());
  }

  function destroy(): void {
    window.removeEventListener("message", onMessage);
    listeners.clear();
  }

  return { embedded, post, subscribe, destroy };
}
