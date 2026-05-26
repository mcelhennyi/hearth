// ThemeProvider — boot from localStorage, reconcile server prefs, broadcast hearth.theme.
// Spec: docs/design/mantle-ui.md § Theme persistence, § postMessage protocol.
// Ticket: T-FR-0006-04. Uses bridge from shell/usePostMessageBridge (no duplicate listeners).

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from 'react'

import type { Bridge } from '../shell/types'
import {
  applyTokensToDocument,
  readStoredPreference,
  resolveEffectiveMode,
  tokensForPreference,
  writeStoredPreference,
  type ThemePreference,
} from './tokens'

type ThemeContextValue = {
  preference: ThemePreference
  effectiveMode: 'light' | 'dark'
  setPreference: (next: ThemePreference) => Promise<void>
  reconciled: boolean
}

const ThemeContext = createContext<ThemeContextValue | null>(null)

function broadcastTheme(bridge: Bridge, preference: ThemePreference): void {
  const tokens = tokensForPreference(preference)
  applyTokensToDocument(tokens)
  bridge.broadcastToAllPlugins({ type: 'hearth.theme', tokens })
}

export function ThemeProvider({
  bridge,
  children,
}: {
  bridge: Bridge
  children: ReactNode
}) {
  const initial = readStoredPreference() ?? 'system'
  const [preference, setPreferenceState] = useState<ThemePreference>(initial)
  const [reconciled, setReconciled] = useState(false)
  const preferenceRef = useRef(preference)
  preferenceRef.current = preference

  const effectiveMode = resolveEffectiveMode(preference)

  // Apply immediately on boot (localStorage source of truth — avoids flash).
  useEffect(() => {
    broadcastTheme(bridge, preferenceRef.current)
  }, [bridge])

  // Reconcile with server after first paint.
  useEffect(() => {
    let cancelled = false

    async function reconcile(): Promise<void> {
      try {
        const response = await fetch('/api/user/preferences')
        if (!response.ok) return
        const data = (await response.json()) as { theme?: ThemePreference }
        if (cancelled || !data.theme) return
        if (data.theme !== preferenceRef.current) {
          writeStoredPreference(data.theme)
          setPreferenceState(data.theme)
          broadcastTheme(bridge, data.theme)
        }
      } finally {
        if (!cancelled) setReconciled(true)
      }
    }

    void reconcile()
    return () => {
      cancelled = true
    }
  }, [bridge])

  // Live system theme tracking.
  useEffect(() => {
    if (preference !== 'system') return
    const mq = window.matchMedia('(prefers-color-scheme: dark)')
    const onChange = () => broadcastTheme(bridge, 'system')
    mq.addEventListener('change', onChange)
    return () => mq.removeEventListener('change', onChange)
  }, [bridge, preference])

  const setPreference = useCallback(
    async (next: ThemePreference) => {
      writeStoredPreference(next)
      setPreferenceState(next)
      broadcastTheme(bridge, next)
      await fetch('/api/user/preferences', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ theme: next }),
      })
    },
    [bridge],
  )

  const value = useMemo(
    () => ({ preference, effectiveMode, setPreference, reconciled }),
    [preference, effectiveMode, setPreference, reconciled],
  )

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
}

export function useThemePreference(): ThemeContextValue {
  const ctx = useContext(ThemeContext)
  if (!ctx) {
    throw new Error('useThemePreference must be used within ThemeProvider')
  }
  return ctx
}
