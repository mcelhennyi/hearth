// Tests for the Mantle postMessage bridge (T-FR-0006-03).
// Spec: docs/design/mantle-ui.md §"postMessage protocol".

import { act, render } from '@testing-library/react'
import { useEffect } from 'react'
import { afterEach, describe, expect, it, vi } from 'vitest'

import type { Bridge, InboundMessage, OutboundMessage } from './types'
import { usePostMessageBridge } from './usePostMessageBridge'

// Tiny harness that exposes the bridge instance to the test.
function Harness({ onReady }: { onReady: (bridge: Bridge) => void }) {
  const bridge = usePostMessageBridge()
  useEffect(() => {
    onReady(bridge)
  }, [bridge, onReady])
  return null
}

function mountBridge(): Bridge {
  let captured: Bridge | null = null
  render(<Harness onReady={(b) => { captured = b }} />)
  if (!captured) throw new Error('bridge not initialised')
  return captured
}

function deliver(data: unknown, originOverride?: string) {
  const event = new MessageEvent('message', {
    data,
    origin: originOverride ?? window.location.origin,
  })
  act(() => {
    window.dispatchEvent(event)
  })
}

describe('usePostMessageBridge', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('rejects cross-origin messages even when payload is valid', () => {
    const bridge = mountBridge()
    const handler = vi.fn()
    bridge.subscribe('hearth.title', handler)

    deliver({ type: 'hearth.title', title: 'Evil' }, 'https://evil.example')

    expect(handler).not.toHaveBeenCalled()
  })

  it('ignores malformed payloads from same origin (no type)', () => {
    const bridge = mountBridge()
    const handler = vi.fn()
    bridge.subscribe('hearth.title', handler)

    deliver({ title: 'noop' })
    deliver(null)
    deliver('a string')

    expect(handler).not.toHaveBeenCalled()
  })

  it('dispatches each inbound type to its subscribers exactly once per message', () => {
    const bridge = mountBridge()
    const titleHandler = vi.fn()
    const toastHandler = vi.fn()
    const navHandler = vi.fn()
    const hapticHandler = vi.fn()
    const mountHandler = vi.fn()
    const unmountHandler = vi.fn()

    bridge.subscribe('hearth.title', titleHandler)
    bridge.subscribe('hearth.toast', toastHandler)
    bridge.subscribe('hearth.nav', navHandler)
    bridge.subscribe('hearth.haptic', hapticHandler)
    bridge.subscribe('hearth.chrome.mount', mountHandler)
    bridge.subscribe('hearth.chrome.unmount', unmountHandler)

    const messages: InboundMessage[] = [
      { type: 'hearth.title', title: 'Groceries' },
      { type: 'hearth.toast', level: 'info', message: 'hi' },
      { type: 'hearth.nav', path: '/groceries' },
      { type: 'hearth.haptic', style: 'selection' },
      {
        type: 'hearth.chrome.mount',
        slot: 'top',
        surface: 'app',
        payload: { kind: 'button', id: 'b1', label: 'Add' },
      },
      { type: 'hearth.chrome.unmount', slot: 'top', surface: 'app', id: 'b1' },
    ]
    for (const m of messages) deliver(m)

    expect(titleHandler).toHaveBeenCalledTimes(1)
    expect(titleHandler).toHaveBeenCalledWith(messages[0])
    expect(toastHandler).toHaveBeenCalledTimes(1)
    expect(toastHandler).toHaveBeenCalledWith(messages[1])
    expect(navHandler).toHaveBeenCalledTimes(1)
    expect(navHandler).toHaveBeenCalledWith(messages[2])
    expect(hapticHandler).toHaveBeenCalledTimes(1)
    expect(hapticHandler).toHaveBeenCalledWith(messages[3])
    expect(mountHandler).toHaveBeenCalledTimes(1)
    expect(mountHandler).toHaveBeenCalledWith(messages[4])
    expect(unmountHandler).toHaveBeenCalledTimes(1)
    expect(unmountHandler).toHaveBeenCalledWith(messages[5])
  })

  it('only invokes subscribers for the matching type', () => {
    const bridge = mountBridge()
    const titleHandler = vi.fn()
    const navHandler = vi.fn()
    bridge.subscribe('hearth.title', titleHandler)
    bridge.subscribe('hearth.nav', navHandler)

    deliver({ type: 'hearth.title', title: 'X' })

    expect(titleHandler).toHaveBeenCalledTimes(1)
    expect(navHandler).not.toHaveBeenCalled()
  })

  it('subscribe with frame option ignores messages from other iframes', () => {
    const bridge = mountBridge()
    const handler = vi.fn()
    const targetWindow = { postMessage: vi.fn() }
    const otherWindow = { postMessage: vi.fn() }
    const target = document.createElement('iframe')
    const other = document.createElement('iframe')
    Object.defineProperty(target, 'contentWindow', { configurable: true, value: targetWindow })
    Object.defineProperty(other, 'contentWindow', { configurable: true, value: otherWindow })
    document.body.appendChild(target)
    document.body.appendChild(other)

    bridge.subscribe('hearth.title', handler, { frame: target })

    act(() => {
      window.dispatchEvent(
        new MessageEvent('message', {
          data: { type: 'hearth.title', title: 'Wrong' },
          origin: window.location.origin,
          source: otherWindow as unknown as MessageEventSource,
        }),
      )
    })
    expect(handler).not.toHaveBeenCalled()

    act(() => {
      window.dispatchEvent(
        new MessageEvent('message', {
          data: { type: 'hearth.title', title: 'Right' },
          origin: window.location.origin,
          source: targetWindow as unknown as MessageEventSource,
        }),
      )
    })
    expect(handler).toHaveBeenCalledTimes(1)

    document.body.removeChild(target)
    document.body.removeChild(other)
  })

  it('unsubscribe stops further dispatch but leaves other subscribers intact', () => {
    const bridge = mountBridge()
    const a = vi.fn()
    const b = vi.fn()
    const unsubA = bridge.subscribe('hearth.title', a)
    bridge.subscribe('hearth.title', b)

    deliver({ type: 'hearth.title', title: 'first' })
    unsubA()
    deliver({ type: 'hearth.title', title: 'second' })

    expect(a).toHaveBeenCalledTimes(1)
    expect(b).toHaveBeenCalledTimes(2)
  })

  it('pushToPlugin posts the message to that iframe contentWindow with same-origin target', () => {
    const bridge = mountBridge()
    const iframe = document.createElement('iframe')
    document.body.appendChild(iframe)
    const post = vi.fn()
    Object.defineProperty(iframe, 'contentWindow', {
      configurable: true,
      get: () => ({ postMessage: post }),
    })

    const msg: OutboundMessage = {
      type: 'hearth.theme',
      tokens: {
        bg: '#000', surface: '#111', fg: '#fff', muted: '#888',
        accent: '#f60', accentFg: '#000', mode: 'dark',
      },
    }
    bridge.pushToPlugin(iframe, msg)

    expect(post).toHaveBeenCalledTimes(1)
    expect(post).toHaveBeenCalledWith(msg, window.location.origin)
    document.body.removeChild(iframe)
  })

  it('logs hearth.toast via console (DG-U11 stub) without requiring subscribers', () => {
    const bridge = mountBridge()
    const info = vi.spyOn(console, 'info').mockImplementation(() => undefined)

    deliver({ type: 'hearth.toast', level: 'success', message: 'Saved' })

    expect(info).toHaveBeenCalledWith('[hearth.toast] success: Saved')
    bridge.subscribe('hearth.toast', vi.fn())
    deliver({ type: 'hearth.toast', level: 'info', message: 'again' })
    expect(info).toHaveBeenCalledTimes(2)
  })

  it('invokes navigator.vibrate for hearth.haptic when available', () => {
    mountBridge()
    const vibrate = vi.fn().mockReturnValue(true)
    Object.defineProperty(navigator, 'vibrate', { configurable: true, value: vibrate })

    deliver({ type: 'hearth.haptic', style: 'impact' })

    expect(vibrate).toHaveBeenCalledWith(25)
  })

  it('hearth.haptic is a no-op when navigator.vibrate is missing', () => {
    mountBridge()
    const original = navigator.vibrate
    // @ts-expect-error — simulate browsers without Vibration API
    delete navigator.vibrate

    expect(() => deliver({ type: 'hearth.haptic', style: 'selection' })).not.toThrow()

    if (original) Object.defineProperty(navigator, 'vibrate', { configurable: true, value: original })
  })

  it.each([
    [
      'hearth.theme',
      {
        type: 'hearth.theme',
        tokens: {
          bg: '#000',
          surface: '#111',
          fg: '#fff',
          muted: '#888',
          accent: '#f60',
          accentFg: '#000',
          mode: 'dark',
        },
      },
    ],
    ['hearth.user', { type: 'hearth.user', user: { id: 'u1', name: 'Ada' } }],
    ['hearth.online', { type: 'hearth.online', online: true }],
    ['hearth.frame.state', { type: 'hearth.frame.state', state: 'loading' }],
    [
      'hearth.chrome.invoke',
      { type: 'hearth.chrome.invoke', slot: 'top', surface: 'app', id: 'add' },
    ],
    [
      'hearth.chrome.resize',
      { type: 'hearth.chrome.resize', slot: 'bottom', rect: { width: 320, height: 48 } },
    ],
  ] as const)('pushToPlugin posts outbound %s with same-origin target', (_label, msg) => {
    const bridge = mountBridge()
    const iframe = document.createElement('iframe')
    document.body.appendChild(iframe)
    const post = vi.fn()
    Object.defineProperty(iframe, 'contentWindow', {
      configurable: true,
      get: () => ({ postMessage: post }),
    })

    bridge.pushToPlugin(iframe, msg)

    expect(post).toHaveBeenCalledWith(msg, window.location.origin)
    document.body.removeChild(iframe)
  })

  it('broadcastToAllPlugins posts to every iframe in the DOM', () => {
    const bridge = mountBridge()
    const postA = vi.fn()
    const postB = vi.fn()
    const a = document.createElement('iframe')
    const b = document.createElement('iframe')
    Object.defineProperty(a, 'contentWindow', { configurable: true, get: () => ({ postMessage: postA }) })
    Object.defineProperty(b, 'contentWindow', { configurable: true, get: () => ({ postMessage: postB }) })
    document.body.appendChild(a)
    document.body.appendChild(b)

    const msg: OutboundMessage = { type: 'hearth.online', online: false }
    bridge.broadcastToAllPlugins(msg)

    expect(postA).toHaveBeenCalledWith(msg, window.location.origin)
    expect(postB).toHaveBeenCalledWith(msg, window.location.origin)
    document.body.removeChild(a)
    document.body.removeChild(b)
  })
})
