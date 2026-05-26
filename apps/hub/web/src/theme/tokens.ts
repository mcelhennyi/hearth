// Theme token maps for Mantle shell — docs/design/mantle-ui.md § Theme tokens.
// Ticket: T-FR-0006-04.

import type { ThemeTokens } from '../shell/types'

export type ThemePreference = 'light' | 'dark' | 'system'

export const THEME_STORAGE_KEY = 'hearth.theme.preference'

export const LIGHT_TOKENS: ThemeTokens = {
  bg: '#fafafa',
  surface: '#ffffff',
  fg: '#111111',
  muted: '#6b7280',
  accent: '#ff6a3d',
  accentFg: '#0f1115',
  mode: 'light',
}

export const DARK_TOKENS: ThemeTokens = {
  bg: '#0f1115',
  surface: '#161a22',
  fg: '#e6e6e6',
  muted: '#9aa3b2',
  accent: '#ff6a3d',
  accentFg: '#0f1115',
  mode: 'dark',
}

export function resolveEffectiveMode(preference: ThemePreference): 'light' | 'dark' {
  if (preference === 'system') {
    if (typeof window.matchMedia === 'function') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    }
    return 'dark'
  }
  return preference
}

export function tokensForPreference(preference: ThemePreference): ThemeTokens {
  return resolveEffectiveMode(preference) === 'light' ? LIGHT_TOKENS : DARK_TOKENS
}

export function applyTokensToDocument(tokens: ThemeTokens): void {
  const root = document.documentElement
  root.style.setProperty('--hearth-bg', tokens.bg)
  root.style.setProperty('--hearth-surface', tokens.surface)
  root.style.setProperty('--hearth-fg', tokens.fg)
  root.style.setProperty('--hearth-muted', tokens.muted)
  root.style.setProperty('--hearth-accent', tokens.accent)
  root.style.setProperty('--hearth-accent-fg', tokens.accentFg)
  root.dataset.hearthTheme = tokens.mode

  const meta = document.querySelector('meta[name="theme-color"]')
  if (meta) {
    meta.setAttribute('content', tokens.bg)
  }
}

export function readStoredPreference(): ThemePreference | null {
  try {
    const raw = localStorage.getItem(THEME_STORAGE_KEY)
    if (raw === 'light' || raw === 'dark' || raw === 'system') {
      return raw
    }
  } catch {
    // Private browsing / disabled storage — fall through.
  }
  return null
}

export function writeStoredPreference(preference: ThemePreference): void {
  try {
    localStorage.setItem(THEME_STORAGE_KEY, preference)
  } catch {
    // Best-effort; server still holds preference.
  }
}
