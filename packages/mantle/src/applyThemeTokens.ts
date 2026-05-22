// Maps ThemeTokens to --hearth-* custom properties on :root (mantle-ui.md §"Theme tokens").

import type { ThemeTokens } from "./types";

const TOKEN_KEYS: Array<keyof Omit<ThemeTokens, "mode">> = [
  "bg",
  "surface",
  "fg",
  "muted",
  "accent",
  "accentFg",
];

const CSS_VAR: Record<keyof Omit<ThemeTokens, "mode">, string> = {
  bg: "--hearth-bg",
  surface: "--hearth-surface",
  fg: "--hearth-fg",
  muted: "--hearth-muted",
  accent: "--hearth-accent",
  accentFg: "--hearth-accent-fg",
};

export function applyThemeTokens(
  tokens: ThemeTokens,
  root: HTMLElement = document.documentElement,
): void {
  for (const key of TOKEN_KEYS) {
    root.style.setProperty(CSS_VAR[key], tokens[key]);
  }
  root.dataset.hearthTheme = tokens.mode;
}
