// useMantle — shell navigation context for the active plugin.
//
// Provides: activePlugin slug (null = dashboard), setActivePlugin.
// The shell (App.tsx) is the single source of truth; plugins change the active
// slot via hearth.nav postMessage, which the shell translates to a route change.
// Plugins should not call setActivePlugin directly — use react-router NavLink instead.

import { createContext, useContext, useState } from 'react'

export interface MantleContextValue {
  activePlugin: string | null
  setActivePlugin: (slug: string | null) => void
}

export const MantleContext = createContext<MantleContextValue>({
  activePlugin: null,
  setActivePlugin: () => undefined,
})

export function useMantle(): MantleContextValue {
  return useContext(MantleContext)
}

// useMantleState is used by the root App to own the state and pass it to MantleContext.Provider.
export function useMantleState(): MantleContextValue {
  const [activePlugin, setActivePlugin] = useState<string | null>(null)
  return { activePlugin, setActivePlugin }
}
