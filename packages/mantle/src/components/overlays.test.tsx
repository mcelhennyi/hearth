import { render, screen } from "@testing-library/react";
import type { ReactNode } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { MantleProvider } from "../MantleProvider";
import { createPluginBridge } from "../bridge";
import { mockEmbeddedParent } from "../test-utils";
import { Dialog } from "./Dialog";
import { Sheet } from "./Sheet";
import { Toast } from "./Toast";

function wrapper(bridge = createPluginBridge()) {
  return function MantleTestWrapper({ children }: { children: ReactNode }) {
    return <MantleProvider bridge={bridge}>{children}</MantleProvider>;
  };
}

describe("@kindling/mantle overlays (T-FR-0006-13)", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("Sheet open/close emits hearth.sheet postMessage when embedded", () => {
    const { postMessage, restore } = mockEmbeddedParent();
    const bridge = createPluginBridge();

    const { rerender } = render(
      <Sheet open id="prefs" title="Preferences">
        <p>Sheet body</p>
      </Sheet>,
      { wrapper: wrapper(bridge) },
    );

    expect(postMessage).toHaveBeenCalledWith(
      { type: "hearth.sheet", action: "open", id: "prefs", title: "Preferences" },
      window.location.origin,
    );
    expect(screen.getByText("Sheet body")).toBeInTheDocument();

    rerender(
      <Sheet open={false} id="prefs" title="Preferences">
        <p>Sheet body</p>
      </Sheet>,
    );
    expect(postMessage).toHaveBeenLastCalledWith(
      { type: "hearth.sheet", action: "close", id: "prefs", title: "Preferences" },
      window.location.origin,
    );

    restore();
    bridge.destroy();
  });

  it("Dialog open/close emits hearth.dialog postMessage when embedded", () => {
    const { postMessage, restore } = mockEmbeddedParent();
    const bridge = createPluginBridge();

    const { rerender } = render(
      <Dialog open id="confirm" title="Delete item?">
        <p>Are you sure?</p>
      </Dialog>,
      { wrapper: wrapper(bridge) },
    );

    expect(postMessage).toHaveBeenCalledWith(
      { type: "hearth.dialog", action: "open", id: "confirm", title: "Delete item?" },
      window.location.origin,
    );

    rerender(
      <Dialog open={false} id="confirm" title="Delete item?">
        <p>Are you sure?</p>
      </Dialog>,
    );
    expect(postMessage).toHaveBeenLastCalledWith(
      { type: "hearth.dialog", action: "close", id: "confirm", title: "Delete item?" },
      window.location.origin,
    );

    restore();
    bridge.destroy();
  });

  it("Toast renders without throwing and console-logs (DG-U11 stub)", () => {
    const logSpy = vi.spyOn(console, "log").mockImplementation(() => {});
    const { postMessage, restore } = mockEmbeddedParent();
    const bridge = createPluginBridge();

    expect(() =>
      render(<Toast level="success" message="Saved" />, { wrapper: wrapper(bridge) }),
    ).not.toThrow();

    expect(logSpy).toHaveBeenCalledWith("[mantle Toast]", {
      level: "success",
      message: "Saved",
    });
    expect(postMessage).toHaveBeenCalledWith(
      { type: "hearth.toast", level: "success", message: "Saved" },
      window.location.origin,
    );

    logSpy.mockRestore();
    restore();
    bridge.destroy();
  });
});
