import { useEffect, useState } from 'react'

export interface HearthUser {
  id: string
  name?: string
  roles?: string[]
}

export interface HearthUserState {
  user: HearthUser | null
}

interface HearthUserMessage {
  type: 'hearth.user'
  user: HearthUser | null
}

function isUserMessage(value: unknown): value is HearthUserMessage {
  if (!value || typeof value !== 'object') return false
  const candidate = value as { type?: unknown; user?: unknown }
  if (candidate.type !== 'hearth.user') return false
  if (candidate.user === null) return true
  if (!candidate.user || typeof candidate.user !== 'object') return false
  return typeof (candidate.user as { id?: unknown }).id === 'string'
}

export function useUser(): HearthUserState {
  const [user, setUser] = useState<HearthUser | null>(null)

  useEffect(() => {
    function handleMessage(event: MessageEvent) {
      if (isUserMessage(event.data)) {
        setUser(event.data.user)
      }
    }

    window.addEventListener('message', handleMessage)
    window.parent?.postMessage({ type: 'hearth.user.request' }, '*')
    return () => window.removeEventListener('message', handleMessage)
  }, [])

  return { user }
}
