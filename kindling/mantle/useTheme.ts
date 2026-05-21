// useTheme — returns the active Mantle theme token set.
//
// Token names mirror the CSS custom properties defined in mantle-ui.md §"Theme tokens".
// Plugins consume these via var(--hearth-*) in CSS; this hook lets shell code
// read and push the current palette via the hearth.theme postMessage.

export type ThemeMode = 'dark' | 'light'

export interface HearthThemeTokens {
  '--hearth-bg': string
  '--hearth-surface': string
  '--hearth-fg': string
  '--hearth-muted': string
  '--hearth-accent': string
  '--hearth-accent-fg': string
  '--hearth-radius-sm': string
  '--hearth-radius-md': string
  '--hearth-radius-lg': string
  '--hearth-font-sans': string
  '--hearth-safe-top': string
  '--hearth-safe-bottom': string
}

const DARK_TOKENS: HearthThemeTokens = {
  '--hearth-bg': '#0f1115',
  '--hearth-surface': '#161a22',
  '--hearth-fg': '#e6e6e6',
  '--hearth-muted': '#9aa3b2',
  '--hearth-accent': '#ff6a3d',
  '--hearth-accent-fg': '#0f1115',
  '--hearth-radius-sm': '4px',
  '--hearth-radius-md': '8px',
  '--hearth-radius-lg': '16px',
  '--hearth-font-sans': '-apple-system, Inter, system-ui, sans-serif',
  '--hearth-safe-top': 'env(safe-area-inset-top)',
  '--hearth-safe-bottom': 'env(safe-area-inset-bottom)',
}

const LIGHT_TOKENS: HearthThemeTokens = {
  '--hearth-bg': '#fafafa',
  '--hearth-surface': '#ffffff',
  '--hearth-fg': '#111111',
  '--hearth-muted': '#6b7280',
  '--hearth-accent': '#ff6a3d',
  '--hearth-accent-fg': '#0f1115',
  '--hearth-radius-sm': '4px',
  '--hearth-radius-md': '8px',
  '--hearth-radius-lg': '16px',
  '--hearth-font-sans': '-apple-system, Inter, system-ui, sans-serif',
  '--hearth-safe-top': 'env(safe-area-inset-top)',
  '--hearth-safe-bottom': 'env(safe-area-inset-bottom)',
}

export function useTheme(): { mode: ThemeMode; tokens: HearthThemeTokens } {
  // Prefer the OS preference. A future user-setting toggle will override this via context.
  const prefersDark =
    typeof window !== 'undefined' ? window.matchMedia('(prefers-color-scheme: dark)').matches : true
  const mode: ThemeMode = prefersDark ? 'dark' : 'light'
  return { mode, tokens: mode === 'dark' ? DARK_TOKENS : LIGHT_TOKENS }
}
