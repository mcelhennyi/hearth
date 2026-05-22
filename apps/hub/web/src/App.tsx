// REWORK-REQUIRED RW-U2 — Settings chrome route missing (mantle-ui.md). Partial: modal only.
import { useEffect, useMemo, useState, useSyncExternalStore } from 'react'
import { Route, Routes, useLocation } from 'react-router-dom'

import { DashboardView } from './dashboard/DashboardView'
import { EditChrome, EditModeProvider } from './dashboard/edit'
import { isMantleEmbedMode } from './mantle/embedMode'
import { InstallPrompt, PluginFrame } from './mantle'
import { MantleEmbedApp } from './MantleEmbedApp'
import { usePlugins } from './usePlugins'
import { AppModeTopBar } from './shell/AppModeTopBar'
import { MantleBottomBar } from './shell/MantleBottomBar'
import { SettingsModal, SettingsTrigger } from './shell/SettingsModal'
import { SettingsProvider } from './shell/SettingsContext'
import { useChromeSlotRegistry } from './shell/useChromeSlotRegistry'
import { usePostMessageBridge } from './shell/usePostMessageBridge'
import { ThemeProvider } from './theme/ThemeProvider'

function useDesktopLayout(): boolean {
  return useSyncExternalStore(
    (onStoreChange) => {
      const mediaQuery = window.matchMedia('(min-width: 768px)')
      mediaQuery.addEventListener('change', onStoreChange)
      return () => mediaQuery.removeEventListener('change', onStoreChange)
    },
    () => window.matchMedia('(min-width: 768px)').matches,
  )
}

function activePluginSlug(pathname: string, pluginSlugs: string[]): string | null {
  const match = pathname.match(/^\/([^/]+)/)
  if (!match) return null
  const slug = match[1]
  return pluginSlugs.includes(slug) ? slug : null
}

function App() {
  if (isMantleEmbedMode()) {
    return <MantleEmbedApp />
  }

  const location = useLocation()
  const isDesktop = useDesktopLayout()
  const plugins = usePlugins()
  const pluginSlugs = useMemo(() => plugins.map((p) => p.slug), [plugins])
  const activeSlug = activePluginSlug(location.pathname, pluginSlugs)
  const activePlugin = activeSlug ? plugins.find((p) => p.slug === activeSlug) : undefined
  const isAppMode = activeSlug !== null
  const isDashboard = !isAppMode

  const bridge = usePostMessageBridge()
  const chrome = useChromeSlotRegistry(bridge, activeSlug)
  const [pluginTitle, setPluginTitle] = useState<string | null>(null)

  useEffect(() => {
    setPluginTitle(null)
  }, [activeSlug])

  useEffect(() => {
    const unsub = bridge.subscribe('hearth.title', (msg) => {
      document.title = `${msg.title} — Hearth`
      if (activeSlug) setPluginTitle(msg.title)
    })
    return unsub
  }, [bridge, activeSlug])

  const shellClass = [
    'shell',
    'min-h-svh',
    'bg-[var(--hearth-bg)]',
    'font-sans',
    'text-[var(--hearth-fg)]',
    chrome.hasChromeSlots ? 'has-chrome-slots' : '',
    isAppMode ? 'shell--app-mode' : '',
    isDesktop ? 'shell--desktop' : '',
  ]
    .filter(Boolean)
    .join(' ')

  const appBarTitle = pluginTitle ?? activePlugin?.name ?? activeSlug ?? 'Hearth'

  return (
    <SettingsProvider>
      <ThemeProvider bridge={bridge}>
        <EditModeProvider>
        <div className={shellClass}>
          {isAppMode ? (
            <AppModeTopBar
              isDesktop={isDesktop}
              title={appBarTitle}
              isDashboard={false}
              topItems={chrome.topItems}
              onChromeInvoke={(id, itemId) => chrome.invoke('top', id, itemId)}
            />
          ) : isDesktop ? (
            <header aria-label="Mantle top bar" className="top-bar border-b border-[var(--hearth-surface)] bg-[var(--hearth-surface)]">
              <nav className="top-bar__inner mx-auto flex h-16 w-full max-w-6xl items-center gap-3 px-6">
                <div className="top-bar__brand">
                  <img src="/logo.svg" alt="" className="h-6 w-6" aria-hidden />
                  <span className="font-semibold">Hearth</span>
                </div>
                <span className="top-bar-spacer" />
                <div className="top-bar__actions">
                  {isDashboard ? <EditChrome isDashboard={isDashboard} /> : null}
                  <button type="button" className="user-btn" aria-label="Account">
                    User
                  </button>
                  <SettingsTrigger variant="desktop-top" className="top-btn" />
                </div>
              </nav>
            </header>
          ) : (
            <header className="top-bar border-b border-[var(--hearth-surface)] bg-[var(--hearth-bg)] px-4 pb-3 pt-[calc(0.75rem+var(--hearth-safe-top))]">
              <div className="top-bar__inner flex w-full items-center gap-3">
                <h2 className="top-bar__title min-w-0 flex-1 text-lg font-semibold">Hearth</h2>
                {isDashboard ? <EditChrome isDashboard={isDashboard} /> : null}
              </div>
            </header>
          )}

          <Routes>
            <Route path="/" element={<DashboardView />} />
            {plugins.map((plugin) => (
              <Route
                key={plugin.slug}
                path={`/${plugin.slug}`}
                element={
                  <PluginFrame
                    slug={plugin.slug}
                    name={plugin.name}
                    active={activeSlug === plugin.slug}
                    bridge={bridge}
                  />
                }
              />
            ))}
          </Routes>

          <InstallPrompt />

          <MantleBottomBar
            isDesktop={isDesktop}
            isAppMode={isAppMode}
            plugins={plugins}
            bottomItems={chrome.bottomItems}
            onChromeInvoke={(id, itemId) => chrome.invoke('bottom', id, itemId)}
          />

          <SettingsModal isDesktop={isDesktop} />
        </div>
        </EditModeProvider>
      </ThemeProvider>
    </SettingsProvider>
  )
}

export default App
