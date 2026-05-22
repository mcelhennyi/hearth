import { renderHook, waitFor } from "@testing-library/react";
import type { ReactNode } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { MantleProvider } from "../MantleProvider";
import { createPluginBridge } from "../bridge";
import {
  deliverFromShell,
  mockEmbeddedParent,
  sampleTheme,
} from "../test-utils";
import { useChromeSlot } from "./useChromeSlot";
import { useHaptics } from "./useHaptics";
import { useNotifications } from "./useNotifications";
import { useSpark } from "./useSpark";
import { useTheme } from "./useTheme";
import { useUser } from "./useUser";

function wrapper(bridge = createPluginBridge()) {
  return function MantleTestWrapper({ children }: { children: ReactNode }) {
    return <MantleProvider bridge={bridge}>{children}</MantleProvider>;
  };
}

describe("mantle hooks", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("useTheme subscribes and applies tokens; unsubscribes on unmount", async () => {
    const bridge = createPluginBridge();
    const { result, unmount } = renderHook(() => useTheme(), {
      wrapper: wrapper(bridge),
    });
    expect(result.current.tokens).toBeNull();

    deliverFromShell(sampleTheme);
    await waitFor(() => expect(result.current.tokens?.mode).toBe("dark"));
    expect(document.documentElement.style.getPropertyValue("--hearth-bg")).toBe(
      "#0f1115",
    );

    unmount();
    deliverFromShell({
      ...sampleTheme,
      tokens: { ...sampleTheme.tokens, mode: "light", bg: "#fafafa" },
    });
    expect(result.current.tokens?.mode).toBe("dark");
    bridge.destroy();
  });

  it("useUser tracks hearth.user and stops after unmount", async () => {
    const bridge = createPluginBridge();
    const { result, unmount } = renderHook(() => useUser(), {
      wrapper: wrapper(bridge),
    });

    deliverFromShell({ type: "hearth.user", user: { id: "u1", name: "Ada" } });
    await waitFor(() => expect(result.current?.name).toBe("Ada"));

    unmount();
    deliverFromShell({ type: "hearth.user", user: null });
    expect(result.current?.name).toBe("Ada");
    bridge.destroy();
  });

  it("useChromeSlot mount/update/unmount round-trip via parent postMessage", async () => {
    const { postMessage, restore } = mockEmbeddedParent();
    const bridge = createPluginBridge();
    const onInvoke = vi.fn();

    const { result } = renderHook(
      () => useChromeSlot("top", "app", { onInvoke }),
      { wrapper: wrapper(bridge) },
    );

    result.current.mount({
      kind: "button",
      id: "add",
      label: "Add",
    });
    expect(postMessage).toHaveBeenCalledWith(
      {
        type: "hearth.chrome.mount",
        slot: "top",
        surface: "app",
        payload: { kind: "button", id: "add", label: "Add" },
      },
      window.location.origin,
    );

    result.current.update({
      kind: "button",
      id: "add",
      label: "Add item",
      busy: true,
    });
    expect(postMessage).toHaveBeenLastCalledWith(
      {
        type: "hearth.chrome.mount",
        slot: "top",
        surface: "app",
        payload: {
          kind: "button",
          id: "add",
          label: "Add item",
          busy: true,
        },
      },
      window.location.origin,
    );

    result.current.unmount("add");
    expect(postMessage).toHaveBeenLastCalledWith(
      {
        type: "hearth.chrome.unmount",
        slot: "top",
        surface: "app",
        id: "add",
      },
      window.location.origin,
    );

    deliverFromShell({
      type: "hearth.chrome.invoke",
      slot: "top",
      surface: "app",
      id: "add",
    });
    await waitFor(() => expect(onInvoke).toHaveBeenCalledWith({ id: "add" }));

    restore();
    bridge.destroy();
  });

  it("useHaptics posts hearth.haptic", () => {
    const { postMessage, restore } = mockEmbeddedParent();
    const bridge = createPluginBridge();
    const { result } = renderHook(() => useHaptics(), {
      wrapper: wrapper(bridge),
    });

    result.current("impact");
    expect(postMessage).toHaveBeenCalledWith(
      { type: "hearth.haptic", style: "impact" },
      window.location.origin,
    );
    restore();
    bridge.destroy();
  });

  it("useNotifications posts hearth.notify", () => {
    const { postMessage, restore } = mockEmbeddedParent();
    const bridge = createPluginBridge();
    const { result } = renderHook(() => useNotifications(), {
      wrapper: wrapper(bridge),
    });

    result.current({ title: "Hi" });
    expect(postMessage).toHaveBeenCalledWith(
      { type: "hearth.notify", payload: { title: "Hi" } },
      window.location.origin,
    );
    restore();
    bridge.destroy();
  });

  it("useSpark returns unavailable stub", () => {
    const bridge = createPluginBridge();
    const { result } = renderHook(() => useSpark(), {
      wrapper: wrapper(bridge),
    });
    expect(result.current).toEqual({ available: false });
    bridge.destroy();
  });
});
