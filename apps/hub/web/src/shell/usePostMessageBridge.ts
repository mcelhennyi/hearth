// usePostMessageBridge — single owner of the Mantle ↔ plugin iframe postMessage channel.
//
// Spec: docs/design/mantle-ui.md §"postMessage protocol" and §"Declaring chrome slots".
// Ticket: T-FR-0006-03.
//
// Security:
//   - The single `window.addEventListener('message', …)` listener enforces a strict
//     same-origin guard: `event.origin === window.location.origin`. Cross-origin or
//     malformed messages are silently dropped. The shell never trusts payload shape
//     beyond the discriminator check in `isInboundMessage`.
//
// Lifecycle:
//   - The listener mounts once per `usePostMessageBridge()` call (the shell should
//     call it exactly once in the App root). Subscribers register via `subscribe`
//     and receive a `()=>void` unsubscribe. Subscribers added/removed during dispatch
//     do not affect the in-flight notification (we snapshot the listener set per
//     dispatched message).
//
// Targeting outbound:
//   - `pushToPlugin(frame, msg)` posts to that iframe's contentWindow only.
//   - `broadcastToAllPlugins(msg)` enumerates every <iframe> currently in the DOM.
//     Both call `postMessage(msg, window.location.origin)` — the same-origin target
//     mirrors the inbound guard so plugins on other origins (none today) get nothing.

import { useEffect, useMemo, useRef } from 'react'

import { handleInboundHaptic, handleInboundToast } from './inboundDefaults'
import type { Bridge, InboundMessage, InboundPayload, InboundType, OutboundMessage } from './types'
import { isInboundMessage } from './types'

type AnyHandler = (payload: InboundMessage) => void

type ListenerEntry = {
  handler: AnyHandler
  frame?: HTMLIFrameElement
}

export function usePostMessageBridge(): Bridge {
  // Map<type, Set<handler>>. Refs keep identity stable across re-renders so consumers
  // can subscribe in their own effects without the bridge tearing down between renders.
  const listenersRef = useRef<Map<InboundType, Set<ListenerEntry>>>(new Map())

  useEffect(() => {
    function onMessage(event: MessageEvent) {
      // Trust boundary: same-origin only.
      if (event.origin !== window.location.origin) return
      if (!isInboundMessage(event.data)) return
      const msg = event.data
      if (msg.type === 'hearth.toast') handleInboundToast(msg)
      else if (msg.type === 'hearth.haptic') handleInboundHaptic(msg.style)
      const handlers = listenersRef.current.get(msg.type)
      if (!handlers || handlers.size === 0) return
      // Snapshot so subscribe/unsubscribe during dispatch is safe.
      for (const entry of Array.from(handlers)) {
        if (entry.frame) {
          const expected = entry.frame.contentWindow
          if (!expected || event.source !== expected) continue
        }
        try {
          entry.handler(msg)
        } catch (err) {
          // Bridge must not break on a faulty subscriber.

          console.error('[hearth bridge] subscriber threw for', msg.type, err)
        }
      }
    }

    window.addEventListener('message', onMessage)
    return () => window.removeEventListener('message', onMessage)
  }, [])

  // The Bridge object is stable for the component lifetime so consumers can pass
  // it through context / props without churning effects.
  return useMemo<Bridge>(() => {
    function subscribe<T extends InboundType>(
      type: T,
      handler: (payload: InboundPayload<T>) => void,
      options?: { frame?: HTMLIFrameElement },
    ): () => void {
      let set = listenersRef.current.get(type)
      if (!set) {
        set = new Set()
        listenersRef.current.set(type, set)
      }
      const entry: ListenerEntry = { handler: handler as AnyHandler, frame: options?.frame }
      set.add(entry)
      return () => {
        const current = listenersRef.current.get(type)
        if (!current) return
        current.delete(entry)
        if (current.size === 0) listenersRef.current.delete(type)
      }
    }

    function pushToPlugin(frame: HTMLIFrameElement, msg: OutboundMessage): void {
      const target = frame.contentWindow
      if (!target) return
      target.postMessage(msg, window.location.origin)
    }

    function broadcastToAllPlugins(msg: OutboundMessage): void {
      const frames = document.querySelectorAll('iframe')
      frames.forEach((frame) => {
        pushToPlugin(frame, msg)
      })
    }

    return { subscribe, pushToPlugin, broadcastToAllPlugins }
  }, [])
}
