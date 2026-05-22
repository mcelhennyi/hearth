import { afterEach, describe, expect, it, vi } from "vitest";

import { createPluginBridge, isAllowedMessageOrigin } from "./bridge";
import { deliverFromShell, mockEmbeddedParent } from "./test-utils";

describe("createPluginBridge", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("isAllowedMessageOrigin rejects cross-origin", () => {
    expect(isAllowedMessageOrigin(window.location.origin)).toBe(true);
    expect(isAllowedMessageOrigin("https://evil.example")).toBe(false);
  });

  it("ignores cross-origin inbound messages", () => {
    const bridge = createPluginBridge();
    const handler = vi.fn();
    bridge.subscribe("hearth.theme", handler);

    deliverFromShell(
      {
        type: "hearth.theme",
        tokens: {
          bg: "#000",
          surface: "#111",
          fg: "#fff",
          muted: "#888",
          accent: "#f60",
          accentFg: "#000",
          mode: "dark",
        },
      },
      "https://evil.example",
    );

    expect(handler).not.toHaveBeenCalled();
    bridge.destroy();
  });

  it("subscribe/unsubscribe dispatches only matching type", () => {
    const bridge = createPluginBridge();
    const theme = vi.fn();
    const user = vi.fn();
    const unsubTheme = bridge.subscribe("hearth.theme", theme);
    bridge.subscribe("hearth.user", user);

    deliverFromShell({ type: "hearth.user", user: { id: "u1" } });
    expect(theme).not.toHaveBeenCalled();
    expect(user).toHaveBeenCalledTimes(1);

    unsubTheme();
    deliverFromShell({
      type: "hearth.theme",
      tokens: {
        bg: "#000",
        surface: "#111",
        fg: "#fff",
        muted: "#888",
        accent: "#f60",
        accentFg: "#000",
        mode: "light",
      },
    });
    expect(theme).not.toHaveBeenCalled();
    expect(user).toHaveBeenCalledTimes(1);
    bridge.destroy();
  });

  it("post sends to parent with same-origin target when embedded", () => {
    const { postMessage, restore } = mockEmbeddedParent();
    const bridge = createPluginBridge();
    expect(bridge.embedded).toBe(true);

    bridge.post({ type: "hearth.title", title: "Groceries" });

    expect(postMessage).toHaveBeenCalledWith(
      { type: "hearth.title", title: "Groceries" },
      window.location.origin,
    );
    restore();
    bridge.destroy();
  });

  it("post is a no-op when not embedded", () => {
    const { postMessage, restore } = mockEmbeddedParent();
    restore();
    const bridge = createPluginBridge();
    expect(bridge.embedded).toBe(false);
    bridge.post({ type: "hearth.ready" });
    expect(postMessage).not.toHaveBeenCalled();
    bridge.destroy();
  });
});
