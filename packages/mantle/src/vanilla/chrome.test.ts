// T-FR-0006-14 — mantle.chrome.mount / unmount round-trip (jsdom).

import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { chrome, mantle } from "./index";

describe("mantle.chrome", () => {
  let postMessage: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    postMessage = vi.fn();
    Object.defineProperty(window, "parent", {
      configurable: true,
      value: { postMessage },
    });
  });

  afterEach(() => {
    Object.defineProperty(window, "parent", {
      configurable: true,
      value: window,
    });
  });

  it("mount posts hearth.chrome.mount with same-origin target", () => {
    const unmount = chrome.mount({
      slot: "top",
      surface: "app",
      payload: { kind: "button", id: "add", label: "Add", variant: "accent" },
    });

    expect(postMessage).toHaveBeenCalledTimes(1);
    expect(postMessage).toHaveBeenCalledWith(
      {
        type: "hearth.chrome.mount",
        slot: "top",
        surface: "app",
        payload: { kind: "button", id: "add", label: "Add", variant: "accent" },
      },
      window.location.origin,
    );

    unmount();

    expect(postMessage).toHaveBeenCalledTimes(2);
    expect(postMessage).toHaveBeenCalledWith(
      {
        type: "hearth.chrome.unmount",
        slot: "top",
        surface: "app",
        id: "add",
      },
      window.location.origin,
    );
  });

  it("mount menu payload round-trips unmount id", () => {
    const unmount = chrome.mount({
      slot: "bottom",
      surface: "dashboard",
      payload: {
        kind: "menu",
        id: "more",
        label: "More",
        items: [{ id: "a", label: "Action" }],
      },
    });

    expect(postMessage.mock.calls[0][0].payload.kind).toBe("menu");
    unmount();
    expect(postMessage.mock.calls[1][0].id).toBe("more");
  });

  it("is exposed on mantle.chrome", () => {
    expect(mantle.chrome).toBe(chrome);
    expect(typeof mantle.chrome.mount).toBe("function");
  });
});
