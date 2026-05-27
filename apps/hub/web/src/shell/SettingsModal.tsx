// Settings modal — floating panel (desktop) / bottom sheet (mobile via <dialog>).
// Spec: docs/design/mantle-ui.md § Settings modal; mocks: docs/design/mockups/dashboard-*.html
// Ticket: T-FR-0006-04.

import { useEffect, useId, useRef, useState, type FormEvent, type ReactNode } from 'react'

import { useThemePreference } from '../theme/ThemeProvider'
import type { ThemePreference } from '../theme/tokens'
import { useSettings, type SettingsTab } from './SettingsContext'

const TABS: Array<{ id: SettingsTab; label: string }> = [
  { id: 'theme', label: 'Theme' },
  { id: 'account', label: 'Account' },
  { id: 'plugins', label: 'Plugins' },
  { id: 'system-tiles', label: 'System tiles' },
  { id: 'diagnostics', label: 'Diagnostics' },
  { id: 'sign-out', label: 'Sign out' },
]

type CurrentUser = {
  user_id: string
  display_name: string
  roles: string[]
}

type ManagedUser = {
  user_id: string
  username: string
  display_name: string
  roles: string[]
  disabled: boolean
}

async function jsonRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    credentials: 'include',
    ...init,
    headers: init?.body
      ? { 'content-type': 'application/json', ...init.headers }
      : init?.headers,
  })
  if (!response.ok) {
    let detail = 'Request failed.'
    try {
      const payload = (await response.json()) as { detail?: unknown }
      if (typeof payload.detail === 'string') detail = payload.detail
    } catch {
      // Keep the generic message for non-JSON responses.
    }
    throw new Error(detail)
  }
  return (await response.json()) as T
}

function ThemeTab() {
  const { preference, setPreference } = useThemePreference()

  return (
    <fieldset className="space-y-3">
      <legend className="text-sm font-medium text-[var(--hearth-fg)]">Appearance</legend>
      {(['light', 'dark', 'system'] as ThemePreference[]).map((value) => (
        <label key={value} className="flex cursor-pointer items-center gap-3 text-sm">
          <input
            type="radio"
            name="hearth-theme"
            value={value}
            checked={preference === value}
            onChange={() => {
              void setPreference(value)
            }}
            className="h-4 w-4 accent-[var(--hearth-accent)]"
          />
          <span className="capitalize text-[var(--hearth-fg)]">{value}</span>
        </label>
      ))}
    </fieldset>
  )
}

function AccountTab() {
  const [currentUser, setCurrentUser] = useState<CurrentUser | null>(null)
  const [users, setUsers] = useState<ManagedUser[]>([])
  const [message, setMessage] = useState('Loading account...')
  const [isBusy, setIsBusy] = useState(false)

  const isAdmin = currentUser?.roles.includes('admin') ?? false

  async function loadUsers(): Promise<void> {
    const payload = await jsonRequest<{ users: ManagedUser[] }>('/hearth-users/api/admin/users')
    setUsers(payload.users)
  }

  useEffect(() => {
    let cancelled = false

    async function loadAccount(): Promise<void> {
      try {
        const session = await jsonRequest<CurrentUser>('/hearth-users/api/session')
        if (cancelled) return
        setCurrentUser(session)
        if (!session.roles.includes('admin')) {
          setMessage('Admin role required.')
          return
        }
        const payload = await jsonRequest<{ users: ManagedUser[] }>('/hearth-users/api/admin/users')
        if (cancelled) return
        setUsers(payload.users)
        setMessage('')
      } catch (error) {
        if (!cancelled) {
          setMessage(error instanceof Error ? error.message : 'Account settings unavailable.')
        }
      }
    }

    void loadAccount()
    return () => {
      cancelled = true
    }
  }, [])

  async function createUser(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault()
    const form = event.currentTarget
    const data = new FormData(form)
    setIsBusy(true)
    setMessage('Creating user...')
    try {
      await jsonRequest<ManagedUser>('/hearth-users/api/admin/users', {
        method: 'POST',
        body: JSON.stringify({
          username: data.get('username'),
          display_name: data.get('display_name'),
          password: data.get('password'),
          roles: data.get('admin') === 'on' ? ['admin', 'user'] : ['user'],
        }),
      })
      form.reset()
      await loadUsers()
      setMessage('')
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Could not create user.')
    } finally {
      setIsBusy(false)
    }
  }

  async function updateUser(user: ManagedUser, patch: Partial<ManagedUser>): Promise<void> {
    setIsBusy(true)
    setMessage('Updating user...')
    try {
      await jsonRequest<ManagedUser>(`/hearth-users/api/admin/users/${user.user_id}`, {
        method: 'PATCH',
        body: JSON.stringify(patch),
      })
      await loadUsers()
      setMessage('')
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Could not update user.')
    } finally {
      setIsBusy(false)
    }
  }

  async function resetPassword(user: ManagedUser): Promise<void> {
    const password = window.prompt(`New password for ${user.display_name}`)
    if (!password) return
    setIsBusy(true)
    setMessage('Resetting password...')
    try {
      await jsonRequest<ManagedUser>(`/hearth-users/api/admin/users/${user.user_id}/password`, {
        method: 'POST',
        body: JSON.stringify({ password }),
      })
      setMessage('')
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Could not reset password.')
    } finally {
      setIsBusy(false)
    }
  }

  if (!isAdmin) {
    return <p className="text-sm text-[var(--hearth-muted)]">{message}</p>
  }

  return (
    <div className="space-y-5">
      <section className="space-y-3">
        <h3 className="text-base font-semibold text-[var(--hearth-fg)]">User management</h3>
        <form className="grid gap-3 md:grid-cols-2" onSubmit={(event) => void createUser(event)}>
          <label className="grid gap-1 text-sm font-medium text-[var(--hearth-fg)]">
            Username
            <input
              name="username"
              required
              className="rounded-md border border-[var(--hearth-muted)]/30 bg-[var(--hearth-bg)] px-3 py-2"
            />
          </label>
          <label className="grid gap-1 text-sm font-medium text-[var(--hearth-fg)]">
            Display name
            <input
              name="display_name"
              required
              className="rounded-md border border-[var(--hearth-muted)]/30 bg-[var(--hearth-bg)] px-3 py-2"
            />
          </label>
          <label className="grid gap-1 text-sm font-medium text-[var(--hearth-fg)]">
            Initial password
            <input
              name="password"
              type="password"
              minLength={8}
              required
              className="rounded-md border border-[var(--hearth-muted)]/30 bg-[var(--hearth-bg)] px-3 py-2"
            />
          </label>
          <label className="flex items-center gap-2 self-end text-sm text-[var(--hearth-fg)]">
            <input name="admin" type="checkbox" className="h-4 w-4 accent-[var(--hearth-accent)]" />
            Admin
          </label>
          <button
            type="submit"
            disabled={isBusy}
            className="rounded-lg bg-[var(--hearth-accent)] px-4 py-2 text-sm font-medium text-[var(--hearth-accent-fg)] disabled:opacity-60 md:col-span-2"
          >
            Create user
          </button>
        </form>
      </section>

      <section className="space-y-2">
        {users.map((user) => {
          const userIsAdmin = user.roles.includes('admin')
          return (
            <div
              key={user.user_id}
              className="grid gap-2 border-t border-[var(--hearth-muted)]/20 py-3 md:grid-cols-[1fr_auto]"
            >
              <div>
                <p className="font-medium text-[var(--hearth-fg)]">{user.display_name}</p>
                <p className="text-sm text-[var(--hearth-muted)]">
                  {user.username} - {user.roles.join(', ')} -{' '}
                  {user.disabled ? 'disabled' : 'enabled'}
                </p>
              </div>
              <div className="flex flex-wrap gap-2">
                <button
                  type="button"
                  disabled={isBusy}
                  onClick={() => void updateUser(user, { disabled: !user.disabled })}
                  className="rounded-md bg-[var(--hearth-bg)] px-3 py-2 text-sm text-[var(--hearth-fg)] disabled:opacity-60"
                >
                  {user.disabled ? `Enable ${user.display_name}` : `Disable ${user.display_name}`}
                </button>
                <button
                  type="button"
                  disabled={isBusy}
                  onClick={() =>
                    void updateUser(user, {
                      roles: userIsAdmin ? ['user'] : ['admin', 'user'],
                    })
                  }
                  className="rounded-md bg-[var(--hearth-bg)] px-3 py-2 text-sm text-[var(--hearth-fg)] disabled:opacity-60"
                >
                  {userIsAdmin ? `Remove admin from ${user.display_name}` : `Make ${user.display_name} admin`}
                </button>
                <button
                  type="button"
                  disabled={isBusy}
                  onClick={() => void resetPassword(user)}
                  className="rounded-md bg-[var(--hearth-bg)] px-3 py-2 text-sm text-[var(--hearth-fg)] disabled:opacity-60"
                >
                  Reset password
                </button>
              </div>
            </div>
          )
        })}
      </section>

      {message ? <p className="text-sm text-[var(--hearth-muted)]">{message}</p> : null}
    </div>
  )
}

function PluginsTab() {
  return (
    <p className="text-sm text-[var(--hearth-muted)]">
      Plugin enable/disable toggles call <code className="text-xs">POST /api/plugins/&lt;slug&gt;/enable|disable</code>.
      Full list wiring ships with dashboard empty-state follow-ups.
    </p>
  )
}

function SystemTilesTab() {
  return (
    <p className="text-sm text-[var(--hearth-muted)]">
      Show or hide dashboard system tiles via <code className="text-xs">POST /api/system/tiles/&lt;id&gt;/hide|restore</code>.
    </p>
  )
}

function DiagnosticsTab() {
  return (
    <ul className="space-y-2 text-sm text-[var(--hearth-muted)]">
      <li>Hub health: check <code className="text-xs">GET /api/health</code></li>
      <li>CA trust and uptime: use <code className="text-xs">hearth doctor</code> when available (FR-0003)</li>
    </ul>
  )
}

function SignOutTab() {
  async function signOut() {
    await fetch('/api/auth/logout', { method: 'POST' })
    window.location.reload()
  }

  return (
    <div className="space-y-4">
      <p className="text-sm text-[var(--hearth-muted)]">End your session on this device.</p>
      <button
        type="button"
        onClick={() => {
          void signOut()
        }}
        className="rounded-lg bg-[var(--hearth-accent)] px-4 py-2 text-sm font-medium text-[var(--hearth-accent-fg)]"
      >
        Sign out
      </button>
    </div>
  )
}

function TabPanel({ tab }: { tab: SettingsTab }) {
  switch (tab) {
    case 'theme':
      return <ThemeTab />
    case 'account':
      return <AccountTab />
    case 'plugins':
      return <PluginsTab />
    case 'system-tiles':
      return <SystemTilesTab />
    case 'diagnostics':
      return <DiagnosticsTab />
    case 'sign-out':
      return <SignOutTab />
    default:
      return null
  }
}

export function SettingsModal({ isDesktop }: { isDesktop: boolean }) {
  const { isOpen, activeTab, closeSettings, setActiveTab } = useSettings()
  const titleId = useId()
  const dialogRef = useRef<HTMLDialogElement>(null)
  const panelRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return
    if (isOpen && !dialog.open) {
      if (typeof dialog.showModal === 'function') {
        dialog.showModal()
      } else {
        dialog.setAttribute('open', '')
      }
      panelRef.current?.focus()
    } else if (!isOpen && dialog.open) {
      if (typeof dialog.close === 'function') {
        dialog.close()
      } else {
        dialog.removeAttribute('open')
      }
    }
  }, [isOpen])

  useEffect(() => {
    if (!isOpen) return

    function focusablesInPanel(): HTMLElement[] {
      if (!panelRef.current) return []
      return Array.from(
        panelRef.current.querySelectorAll<HTMLElement>(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
        ),
      ).filter((el) => !el.hasAttribute('disabled'))
    }

    function onKeyDown(event: KeyboardEvent) {
      if (event.key === 'Escape') {
        event.preventDefault()
        closeSettings()
        return
      }
      if (event.key !== 'Tab') return
      const focusables = focusablesInPanel()
      if (focusables.length === 0) return
      const first = focusables[0]
      const last = focusables[focusables.length - 1]
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault()
        last.focus()
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault()
        first.focus()
      }
    }
    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [isOpen, closeSettings])

  if (!isOpen) return null

  const panelClass = isDesktop
    ? 'mx-auto my-[10vh] w-full max-w-[640px] max-h-[80vh] rounded-2xl'
    : 'fixed inset-x-0 bottom-0 max-h-[90vh] rounded-t-2xl pt-[var(--hearth-safe-top)]'

  return (
    <dialog
      ref={dialogRef}
      aria-labelledby={titleId}
      className="fixed inset-0 z-50 m-0 h-full w-full max-h-none max-w-none border-0 bg-transparent p-0 backdrop:bg-[color-mix(in_srgb,var(--hearth-bg)_70%,transparent)]"
      onCancel={(event) => {
        event.preventDefault()
        closeSettings()
      }}
      onClick={(event) => {
        if (event.target === dialogRef.current) closeSettings()
      }}
    >
      <div
        ref={panelRef}
        role="document"
        tabIndex={-1}
        className={`flex flex-col overflow-hidden border border-[var(--hearth-muted)]/30 bg-[var(--hearth-surface)] shadow-xl outline-none ${panelClass}`}
        onClick={(event) => event.stopPropagation()}
      >
        <header className="flex shrink-0 items-center justify-between border-b border-[var(--hearth-muted)]/20 px-4 py-3">
          <h2 id={titleId} className="text-lg font-semibold text-[var(--hearth-fg)]">
            Settings
          </h2>
          <button
            type="button"
            aria-label="Close settings"
            onClick={closeSettings}
            className="rounded-md px-2 py-1 text-xl leading-none text-[var(--hearth-muted)] hover:bg-[var(--hearth-bg)]"
          >
            ×
          </button>
        </header>

        <div className="flex min-h-0 flex-1 flex-col md:flex-row">
          <nav
            aria-label="Settings sections"
            className="flex shrink-0 gap-1 overflow-x-auto border-b border-[var(--hearth-muted)]/20 px-2 py-2 md:w-40 md:flex-col md:border-b-0 md:border-r"
          >
            {TABS.map((tab) => (
              <button
                key={tab.id}
                type="button"
                role="tab"
                aria-selected={activeTab === tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`whitespace-nowrap rounded-lg px-3 py-2 text-left text-sm ${
                  activeTab === tab.id
                    ? 'bg-[var(--hearth-accent)] text-[var(--hearth-accent-fg)]'
                    : 'text-[var(--hearth-muted)] hover:bg-[var(--hearth-bg)]'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>

          <div
            role="tabpanel"
            className="min-h-0 flex-1 overflow-y-auto px-4 py-4 pb-[calc(1rem+var(--hearth-safe-bottom))]"
          >
            <TabPanel tab={activeTab} />
          </div>
        </div>

        <footer className="shrink-0 border-t border-[var(--hearth-muted)]/20 px-4 py-3 md:hidden">
          <button
            type="button"
            onClick={closeSettings}
            className="w-full rounded-lg bg-[var(--hearth-bg)] px-4 py-3 text-sm font-medium text-[var(--hearth-fg)]"
          >
            Done
          </button>
        </footer>
      </div>
    </dialog>
  )
}

export function SettingsTrigger({
  variant,
  className,
  children,
  'aria-label': ariaLabel,
}: {
  variant: 'desktop-top' | 'desktop-bottom' | 'mobile-icon'
  className?: string
  children?: ReactNode
  'aria-label'?: string
}) {
  const { openSettings } = useSettings()

  const label =
    variant === 'mobile-icon' ? (
      <span aria-hidden>⚙️</span>
    ) : (
      <>
        <span aria-hidden>⚙️</span> Settings
      </>
    )

  return (
    <button
      type="button"
      aria-haspopup="dialog"
      aria-label={ariaLabel ?? (variant === 'mobile-icon' ? 'Settings' : undefined)}
      className={className}
      onClick={() => openSettings('theme')}
    >
      {children ?? label}
    </button>
  )
}
