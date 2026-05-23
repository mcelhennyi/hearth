// Plugin iframe lifecycle state machine (mantle-ui.md §"Plugin frame states", T-FR-0006-05).
//
// Drives shell overlays and pushes `hearth.frame.state` to the plugin when reachable.

import { useCallback, useEffect, useRef, useState, type RefObject } from 'react'

import type { Bridge, FrameState } from './types'

const SLOW_AFTER_MS = 5_000
const SLOW_RELOAD_AFTER_MS = 15_000

export interface UsePluginFrameStateOptions {
  slug: string
  pluginName: string
  frameRef: RefObject<HTMLIFrameElement | null>
  bridge: Bridge
  active: boolean
}

export interface UsePluginFrameStateResult {
  state: FrameState
  errorDetail: string | null
  showSlowReload: boolean
  reload: () => void
  tryAgain: () => void
}

function pluginSrc(slug: string): string {
  return `/${slug}/?embed=1`
}

export function usePluginFrameState({
  slug,
  pluginName,
  frameRef,
  bridge,
  active,
}: UsePluginFrameStateOptions): UsePluginFrameStateResult {
  const [state, setState] = useState<FrameState>(() =>
    typeof navigator !== 'undefined' && !navigator.onLine ? 'offline' : 'loading',
  )
  const [errorDetail, setErrorDetail] = useState<string | null>(null)
  const [showSlowReload, setShowSlowReload] = useState(false)
  const [generation, setGeneration] = useState(0)

  const hasLoadedRef = useRef(false)
  const hasAckRef = useRef(false)
  const stateRef = useRef(state)
  stateRef.current = state

  const pushFrameState = useCallback(
    (next: FrameState) => {
      const frame = frameRef.current
      if (!frame?.contentWindow) return
      bridge.pushToPlugin(frame, { type: 'hearth.frame.state', state: next })
    },
    [bridge, frameRef],
  )

  const applyState = useCallback(
    (next: FrameState, detail: string | null = null) => {
      stateRef.current = next
      setState(next)
      setErrorDetail(detail)
      if (next !== 'slow') setShowSlowReload(false)
      pushFrameState(next)
    },
    [pushFrameState],
  )

  const tryMounted = useCallback(() => {
    // A browser load event can still fire for proxy error pages; require a same-frame
    // plugin ack before dropping the shell overlay.
    if (hasLoadedRef.current && hasAckRef.current) {
      applyState('mounted')
    }
  }, [applyState])

  const reload = useCallback(() => {
    const frame = frameRef.current
    if (!frame) return
    hasLoadedRef.current = false
    hasAckRef.current = false
    setShowSlowReload(false)
    if (!navigator.onLine) {
      applyState('offline')
      return
    }
    applyState('loading')
    frame.src = pluginSrc(slug)
    setGeneration((g) => g + 1)
  }, [applyState, frameRef, slug])

  const tryAgain = useCallback(() => {
    if (!navigator.onLine) return
    reload()
  }, [reload])

  // Probe plugin root for HTTP errors (mantle-ui.md — proxy 4xx/5xx → error).
  useEffect(() => {
    if (!active) return
    let cancelled = false

    async function probe(): Promise<void> {
      if (!navigator.onLine) {
        if (!cancelled) applyState('offline')
        return
      }
      try {
        let response = await fetch(pluginSrc(slug), { method: 'HEAD', cache: 'no-store' })
        if (response.status === 405) {
          response = await fetch(pluginSrc(slug), { method: 'GET', cache: 'no-store' })
        }
        if (cancelled) return
        if (response.status >= 400) {
          applyState('error', `HTTP ${response.status}`)
        }
      } catch (err) {
        if (cancelled) return
        if (!navigator.onLine) {
          applyState('offline')
          return
        }
        const message = err instanceof Error ? err.message : 'Network error'
        applyState('error', message)
      }
    }

    void probe()
    return () => {
      cancelled = true
    }
  }, [active, slug, generation, applyState])

  // Timers: 5 s → slow (no load); 15 s → Reload affordance in slow.
  useEffect(() => {
    if (!active || !navigator.onLine) return

    const slowTimer = window.setTimeout(() => {
      if (!hasLoadedRef.current && stateRef.current !== 'error' && stateRef.current !== 'offline') {
        applyState('slow')
      }
    }, SLOW_AFTER_MS)

    const reloadTimer = window.setTimeout(() => {
      if (stateRef.current === 'slow') {
        setShowSlowReload(true)
      }
    }, SLOW_RELOAD_AFTER_MS)

    return () => {
      window.clearTimeout(slowTimer)
      window.clearTimeout(reloadTimer)
    }
  }, [active, generation, applyState])

  // iframe load / error + plugin ack (hearth.title | hearth.ready).
  useEffect(() => {
    const frame = frameRef.current
    if (!frame || !active) return

    hasLoadedRef.current = false
    hasAckRef.current = false

    if (!navigator.onLine) {
      applyState('offline')
      return
    }
    applyState('loading')

    function onLoad() {
      hasLoadedRef.current = true
      tryMounted()
    }

    function onError() {
      applyState('error', `${pluginName} failed to load`)
    }

    frame.addEventListener('load', onLoad)
    frame.addEventListener('error', onError)

    const unsubTitle = bridge.subscribe(
      'hearth.title',
      () => {
        hasAckRef.current = true
        tryMounted()
      },
      { frame },
    )
    const unsubReady = bridge.subscribe(
      'hearth.ready',
      () => {
        hasAckRef.current = true
        tryMounted()
      },
      { frame },
    )

    return () => {
      frame.removeEventListener('load', onLoad)
      frame.removeEventListener('error', onError)
      unsubTitle()
      unsubReady()
    }
  }, [active, bridge, frameRef, pluginName, generation, applyState, tryMounted])

  // Online / offline transitions while this frame is active.
  useEffect(() => {
    if (!active) return

    function onOnline() {
      if (stateRef.current === 'offline') {
        reload()
      }
      const frame = frameRef.current
      if (frame?.contentWindow) {
        bridge.pushToPlugin(frame, { type: 'hearth.online', online: true })
      }
    }

    function onOffline() {
      applyState('offline')
      const frame = frameRef.current
      if (frame?.contentWindow) {
        bridge.pushToPlugin(frame, { type: 'hearth.online', online: false })
      }
    }

    window.addEventListener('online', onOnline)
    window.addEventListener('offline', onOffline)
    return () => {
      window.removeEventListener('online', onOnline)
      window.removeEventListener('offline', onOffline)
    }
  }, [active, applyState, bridge, frameRef, reload])

  return { state, errorDetail, showSlowReload, reload, tryAgain }
}
