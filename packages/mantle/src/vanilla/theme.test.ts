// T-FR-0006-14 — mantle.theme.subscribe (jsdom).

import { afterEach, describe, expect, it, vi } from "vitest";

import type { ThemeTokens } from "../types";
import { applyThemeTokens, mantle, theme } from "./index";

const sampleTokens: ThemeTokens = {
  mode: "dark",
  bg: "#111111",
  surface: "#222222",
  fg: "#eeeeee",
  muted: "#888888",
  accent: "#ff6a3d",
  accentFg: "#000000",
};

function deliverTheme(tokens: ThemeTokens, origin = window.location.origin) {
  window.dispatchEvent(
    new MessageEvent("message", {
      data: { type: "hearth.theme", tokens },
      origin,
    }),
  );
}

describe("mantle.theme", () => {
  afterEach(() => {
    document.documentElement.removeAttribute("style");
  });

  it("applyThemeTokens sets --hearth-* custom properties on :root", () => {
    applyThemeTokens(sampleTokens);
    const root = document.documentElement;
    expect(root.style.getPropertyValue("--hearth-bg")).toBe(sampleTokens.bg);
    expect(root.style.getPropertyValue("--hearth-accent")).toBe(sampleTokens.accent);
    expect(root.style.getPropertyValue("--hearth-mode")).toBe(sampleTokens.mode);
  });

  it("subscribe applies tokens and invokes the callback on hearth.theme", () => {
    const cb = vi.fn();
    const unsub = theme.subscribe(cb);

    deliverTheme(sampleTokens);

    expect(cb).toHaveBeenCalledTimes(1);
    expect(cb).toHaveBeenCalledWith(sampleTokens);
    expect(document.documentElement.style.getPropertyValue("--hearth-fg")).toBe(
      sampleTokens.fg,
    );

    unsub();
    deliverTheme({ ...sampleTokens, fg: "#ffffff" });
    expect(cb).toHaveBeenCalledTimes(1);
  });

  it("rejects cross-origin hearth.theme messages", () => {
    const cb = vi.fn();
    theme.subscribe(cb);

    deliverTheme(sampleTokens, "https://evil.example");

    expect(cb).not.toHaveBeenCalled();
    expect(document.documentElement.style.getPropertyValue("--hearth-bg")).toBe("");
  });

  it("ignores non-theme same-origin messages", () => {
    const cb = vi.fn();
    theme.subscribe(cb);

    window.dispatchEvent(
      new MessageEvent("message", {
        data: { type: "hearth.online", online: true },
        origin: window.location.origin,
      }),
    );

    expect(cb).not.toHaveBeenCalled();
  });

  it("is exposed on mantle.theme", () => {
    expect(mantle.theme).toBe(theme);
    expect(typeof mantle.theme.subscribe).toBe("function");
  });
});
