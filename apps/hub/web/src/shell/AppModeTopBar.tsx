import { NavLink } from 'react-router-dom'

import { EditChrome } from '../dashboard/edit'
import { ChromeSlot } from './ChromeSlot'
import type { ChromeRegistryEntry } from './useChromeSlotRegistry'
import { SettingsTrigger } from './SettingsModal'

type Props = {
  isDesktop: boolean
  title: string
  isDashboard: boolean
  topItems: ChromeRegistryEntry[]
  onChromeInvoke: (id: string, itemId?: string) => void
}

/** App/plugin top bar — back + title left; actions right (mantle-ui.md). */
export function AppModeTopBar({ isDesktop, title, isDashboard, topItems, onChromeInvoke }: Props) {
  return (
    <header
      aria-label="Mantle top bar"
      className={`top-bar top-bar--app border-b border-[var(--hearth-surface)] ${
        isDesktop ? 'bg-[var(--hearth-surface)]' : 'bg-[var(--hearth-bg)] px-4 pb-3 pt-[calc(0.75rem+var(--hearth-safe-top))]'
      }`}
    >
      <nav
        className={
          isDesktop
            ? 'top-bar__inner mx-auto flex h-16 w-full max-w-6xl items-center gap-3 px-6'
            : 'top-bar__inner flex w-full items-center gap-3'
        }
      >
        <div className="top-bar__leading">
          <NavLink to="/" className="home-back" aria-label="Home">
            ‹
          </NavLink>
          <h1 className="top-bar__title min-w-0 truncate text-lg font-semibold">{title}</h1>
        </div>
        <span className="top-bar-spacer" />
        <div className="top-bar__actions">
          <ChromeSlot slot="top" items={topItems} isDesktop={isDesktop} onInvoke={onChromeInvoke} />
          {isDashboard ? <EditChrome isDashboard /> : null}
          <button type="button" className="user-btn" aria-label="Account">
            User
          </button>
          {isDesktop ? (
            <SettingsTrigger variant="desktop-top" className="top-btn" />
          ) : null}
        </div>
      </nav>
    </header>
  )
}
