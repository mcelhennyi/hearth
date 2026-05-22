// mantle.chrome — mount/unmount chrome slots via postMessage (T-FR-0006-14).
// Spec: docs/design/mantle-ui.md § Declaring chrome slots.

import type { ChromePayload, ChromeSlot, ChromeSurface } from "../types";
import { postToParent } from "./post";

export type ChromeMountOptions = {
  slot: ChromeSlot;
  surface: ChromeSurface;
  payload: ChromePayload;
};

export const chrome = {
  /**
   * Register a chrome control in the shell. Returns `unmount` which posts
   * `hearth.chrome.unmount` for the same slot/surface/id.
   */
  mount(options: ChromeMountOptions): () => void {
    const { slot, surface, payload } = options;
    postToParent({
      type: "hearth.chrome.mount",
      slot,
      surface,
      payload,
    });
    return () => {
      postToParent({
        type: "hearth.chrome.unmount",
        slot,
        surface,
        id: payload.id,
      });
    };
  },
};
