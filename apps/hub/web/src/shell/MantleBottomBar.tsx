import { NavLink } from 'react-router-dom'

import type { PluginNavEntry } from '../usePlugins'
import { ChromeSlot } from './ChromeSlot'
import type { ChromeRegistryEntry } from './useChromeSlotRegistry'
import { HomeNavIcon } from './HomeNavIcon'
import { iconForPlugin } from './pluginNavIcons'
import { SettingsTrigger } from './SettingsModal'

type Props = {
  isDesktop: boolean
  isAppMode: boolean
  plugins: PluginNavEntry[]
  bottomItems: ChromeRegistryEntry[]
  onChromeInvoke: (slotId: string, itemId: string) => void
}

function navTabClass(isActive: boolean, isDesktop: boolean): string {
  const base = isDesktop ? 'nav-tab nav-tab--desktop' : 'nav-tab'
  return isActive ? `${base} is-active` : base
}

function PluginLauncherTab({ plugin, isDesktop }: { plugin: PluginNavEntry; isDesktop: boolean }) {
  const visual = iconForPlugin(plugin.slug)
  return (
    <NavLink
      to={`/${plugin.slug}`}
      role="tab"
      className={({ isActive }) => navTabClass(isActive, isDesktop)}
      aria-label={plugin.name}
    >
      <span className="tab-icon" style={{ background: visual.gradient }} aria-hidden>
        {visual.emoji}
      </span>
      <span className="tab-label">{plugin.name}</span>
    </NavLink>
  )
}

function PinnedHomeTab({ isDesktop }: { isDesktop: boolean }) {
  return (
    <NavLink
      to="/"
      end
      className={({ isActive }) => `${navTabClass(isActive, isDesktop)} nav-tab--home`}
      aria-label="Home"
    >
      <span className="tab-icon tab-icon--home" aria-hidden>
        <HomeNavIcon />
      </span>
      <span className="tab-label">Home</span>
    </NavLink>
  )
}

/** Fixed bottom bar — docs/design/mantle-ui.md § Bottom bar */
export function MantleBottomBar({ isDesktop, isAppMode, plugins, bottomItems, onChromeInvoke }: Props) {
  const settingsVariant = isDesktop ? 'desktop-bottom' : 'mobile-icon'

  if (isAppMode) {
    return (
      <nav
        aria-label="Shell navigation"
        className={`bottom-bar bottom-bar--app bottom-bar--fixed${isDesktop ? ' bottom-bar--desktop' : ''}`}
      >
        <div className="nav-pinned nav-pinned--start">
          <PinnedHomeTab isDesktop={isDesktop} />
        </div>
        <ChromeSlot
          slot="bottom"
          items={bottomItems}
          isDesktop={isDesktop}
          onInvoke={(id, itemId) => onChromeInvoke(id, itemId)}
        />
        <div className="nav-pinned nav-pinned--end">
          <SettingsTrigger
            variant={settingsVariant}
            className={
              isDesktop
                ? 'bottom-settings'
                : 'nav-tab nav-tab--settings flex min-h-11 min-w-11 items-center justify-center'
            }
            aria-label="Settings"
          />
        </div>
      </nav>
    )
  }

  return (
    <nav
      aria-label="Main navigation"
      className={`bottom-bar bottom-bar--fixed${isDesktop ? ' bottom-bar--desktop' : ''}`}
    >
      <div className="nav-pinned nav-pinned--start">
        <PinnedHomeTab isDesktop={isDesktop} />
      </div>
      <div className="nav-quick-access" aria-label="Quick access to apps">
        <div className="nav-scroll" role="tablist">
          {plugins.map((plugin) => (
            <PluginLauncherTab key={plugin.slug} plugin={plugin} isDesktop={isDesktop} />
          ))}
        </div>
      </div>
      <div className="nav-pinned nav-pinned--end">
        <SettingsTrigger
          variant={settingsVariant}
          className={isDesktop ? 'bottom-settings' : 'nav-tab nav-tab--settings'}
          aria-label="Settings"
        />
      </div>
    </nav>
  )
}
