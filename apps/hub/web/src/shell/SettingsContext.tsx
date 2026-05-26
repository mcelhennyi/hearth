// Settings modal open state — T-FR-0006-04.
// Spec: docs/design/mantle-ui.md § Settings modal.
/* eslint-disable react-refresh/only-export-components */

import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from 'react'

export type SettingsTab =
  | 'theme'
  | 'account'
  | 'plugins'
  | 'system-tiles'
  | 'diagnostics'
  | 'sign-out'

type SettingsContextValue = {
  isOpen: boolean
  activeTab: SettingsTab
  openSettings: (tab?: SettingsTab) => void
  closeSettings: () => void
  setActiveTab: (tab: SettingsTab) => void
}

const SettingsContext = createContext<SettingsContextValue | null>(null)

export function SettingsProvider({ children }: { children: ReactNode }) {
  const [isOpen, setIsOpen] = useState(false)
  const [activeTab, setActiveTab] = useState<SettingsTab>('theme')

  const openSettings = useCallback((tab: SettingsTab = 'theme') => {
    setActiveTab(tab)
    setIsOpen(true)
  }, [])

  const closeSettings = useCallback(() => {
    setIsOpen(false)
  }, [])

  const value = useMemo(
    () => ({ isOpen, activeTab, openSettings, closeSettings, setActiveTab }),
    [isOpen, activeTab, openSettings, closeSettings],
  )

  return <SettingsContext.Provider value={value}>{children}</SettingsContext.Provider>
}

export function useSettings(): SettingsContextValue {
  const ctx = useContext(SettingsContext)
  if (!ctx) {
    throw new Error('useSettings must be used within SettingsProvider')
  }
  return ctx
}
