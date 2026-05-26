// Maps ThemeTokens to --hearth-* custom properties on :root (mantle-ui.md §"Theme tokens").

import type { ThemeTokens } from "./types";

const TOKEN_KEYS: Array<keyof ThemeTokens> = [
  "bg",
  "surface",
  "fg",
  "muted",
  "accent",
  "accentFg",
  "mode",
];

const CSS_VAR: Record<keyof ThemeTokens, string> = {
  bg: "--hearth-bg",
  surface: "--hearth-surface",
  fg: "--hearth-fg",
  muted: "--hearth-muted",
  accent: "--hearth-accent",
  accentFg: "--hearth-accent-fg",
  mode: "--hearth-mode",
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
