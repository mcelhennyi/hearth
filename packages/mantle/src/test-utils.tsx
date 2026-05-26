import { act } from "@testing-library/react";
import { vi } from "vitest";

import type { InboundMessage } from "./types";

export function deliverFromShell(
  data: unknown,
  originOverride?: string,
): void {
  const event = new MessageEvent("message", {
    data,
    origin: originOverride ?? window.location.origin,
  });
  act(() => {
    window.dispatchEvent(event);
  });
}

export function mockEmbeddedParent(): {
  postMessage: ReturnType<typeof vi.fn>;
  restore: () => void;
} {
  const postMessage = vi.fn();
  const originalParent = window.parent;
  Object.defineProperty(window, "parent", {
    configurable: true,
    value: { postMessage },
  });
  return {
    postMessage,
    restore: () => {
      Object.defineProperty(window, "parent", {
        configurable: true,
        value: originalParent,
      });
    },
  };
}

export const sampleTheme: InboundMessage & { type: "hearth.theme" } = {
  type: "hearth.theme",
  tokens: {
    bg: "#0f1115",
    surface: "#161a22",
    fg: "#e6e6e6",
    muted: "#9aa3b2",
    accent: "#ff6a3d",
    accentFg: "#0f1115",
    mode: "dark",
  },
};
