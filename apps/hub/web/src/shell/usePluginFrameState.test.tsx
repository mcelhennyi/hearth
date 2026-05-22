// Tests for plugin frame state machine (T-FR-0006-05).
// Spec: docs/design/mantle-ui.md §"Plugin frame states".

import { act, render, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import type { Bridge } from './types'
import { usePostMessageBridge } from './usePostMessageBridge'
import { usePluginFrameState } from './usePluginFrameState'

function mountBridge(): Bridge {
  let captured: Bridge | null = null
  function Harness({ onReady }: { onReady: (b: Bridge) => void }) {
    const bridge = usePostMessageBridge()
    onReady(bridge)
    return null
  }
  render(<Harness onReady={(b) => { captured = b }} />)
  if (!captured) throw new Error('bridge not initialised')
  return captured
}

function mockContentWindow(): Window & { postMessage: ReturnType<typeof vi.fn> } {
  return { postMessage: vi.fn() } as unknown as Window & { postMessage: ReturnType<typeof vi.fn> }
}

function deliverFromFrame(frame: HTMLIFrameElement, data: unknown) {
  const source = frame.contentWindow
  if (!source) throw new Error('iframe has no contentWindow')
  const event = new MessageEvent('message', {
    data,
    origin: window.location.origin,
    source,
  })
  act(() => {
    window.dispatchEvent(event)
  })
}

function setupIframe(slug: string, contentWindow: Window = mockContentWindow()): HTMLIFrameElement {
  const iframe = document.createElement('iframe')
  iframe.title = 'test'
  iframe.src = `/${slug}/?embed=1`
  Object.defineProperty(iframe, 'contentWindow', {
    configurable: true,
    value: contentWindow,
  })
  document.body.appendChild(iframe)
  return iframe
}

describe('usePluginFrameState', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({ ok: true, status: 200 }),
    )
    Object.defineProperty(navigator, 'onLine', { configurable: true, value: true, writable: true })
  })

  afterEach(() => {
    vi.useRealTimers()
    vi.unstubAllGlobals()
    document.body.innerHTML = ''
  })

  it('starts in loading when online', async () => {
    const bridge = mountBridge()
    const iframe = setupIframe('groceries')
    const frameRef = { current: iframe }

    const { result } = renderHook(() =>
      usePluginFrameState({
        slug: 'groceries',
        pluginName: 'Groceries',
        frameRef,
        bridge,
        active: true,
      }),
    )

    await act(async () => {
      await Promise.resolve()
    })
    expect(result.current.state).toBe('loading')
  })

  it('enters offline when navigator.onLine is false on mount', async () => {
    Object.defineProperty(navigator, 'onLine', { configurable: true, value: false })
    const bridge = mountBridge()
    const iframe = setupIframe('groceries')
    const frameRef = { current: iframe }

    const { result } = renderHook(() =>
      usePluginFrameState({
        slug: 'groceries',
        pluginName: 'Groceries',
        frameRef,
        bridge,
        active: true,
      }),
    )

    await act(async () => {
      await Promise.resolve()
    })
    expect(result.current.state).toBe('offline')
  })

  it('transitions to slow after 5s without iframe load', async () => {
    const bridge = mountBridge()
    const iframe = setupIframe('groceries')
    const frameRef = { current: iframe }

    const { result } = renderHook(() =>
      usePluginFrameState({
        slug: 'groceries',
        pluginName: 'Groceries',
        frameRef,
        bridge,
        active: true,
      }),
    )

    await act(async () => {
      await Promise.resolve()
    })
    act(() => {
      vi.advanceTimersByTime(5_000)
    })
    expect(result.current.state).toBe('slow')
  })

  it('offers Reload in slow state after 15s', async () => {
    const bridge = mountBridge()
    const iframe = setupIframe('groceries')
    const frameRef = { current: iframe }

    const { result } = renderHook(() =>
      usePluginFrameState({
        slug: 'groceries',
        pluginName: 'Groceries',
        frameRef,
        bridge,
        active: true,
      }),
    )

    act(() => {
      vi.advanceTimersByTime(15_000)
    })
    expect(result.current.state).toBe('slow')
    expect(result.current.showSlowReload).toBe(true)
  })

  it('transitions to mounted on load plus hearth.ready within 5s', async () => {
    const bridge = mountBridge()
    const pluginWindow = mockContentWindow()
    const iframe = setupIframe('groceries', pluginWindow)
    const frameRef = { current: iframe }

    const { result } = renderHook(() =>
      usePluginFrameState({
        slug: 'groceries',
        pluginName: 'Groceries',
        frameRef,
        bridge,
        active: true,
      }),
    )

    await act(async () => {
      await Promise.resolve()
    })

    act(() => {
      iframe.dispatchEvent(new Event('load'))
      deliverFromFrame(iframe, { type: 'hearth.ready' })
    })

    expect(result.current.state).toBe('mounted')
    expect(pluginWindow.postMessage).toHaveBeenCalledWith(
      { type: 'hearth.frame.state', state: 'mounted' },
      window.location.origin,
    )
  })

  it('transitions to error on iframe error event', async () => {
    const bridge = mountBridge()
    const iframe = setupIframe('groceries')
    const frameRef = { current: iframe }

    const { result } = renderHook(() =>
      usePluginFrameState({
        slug: 'groceries',
        pluginName: 'Groceries',
        frameRef,
        bridge,
        active: true,
      }),
    )

    await act(async () => {
      await Promise.resolve()
    })

    act(() => {
      iframe.dispatchEvent(new Event('error'))
    })

    expect(result.current.state).toBe('error')
    expect(result.current.errorDetail).toContain('failed to load')
  })

  it('transitions to error when fetch probe returns 502', async () => {
    vi.mocked(fetch).mockResolvedValueOnce({ ok: false, status: 502 } as Response)
    const bridge = mountBridge()
    const iframe = setupIframe('groceries')
    const frameRef = { current: iframe }

    const { result } = renderHook(() =>
      usePluginFrameState({
        slug: 'groceries',
        pluginName: 'Groceries',
        frameRef,
        bridge,
        active: true,
      }),
    )

    await act(async () => {
      await Promise.resolve()
    })

    expect(result.current.state).toBe('error')
    expect(result.current.errorDetail).toBe('HTTP 502')
  })

  it('pushes hearth.frame.state on state changes when contentWindow exists', async () => {
    const bridge = mountBridge()
    const pluginWindow = mockContentWindow()
    const iframe = setupIframe('groceries', pluginWindow)
    const frameRef = { current: iframe }

    renderHook(() =>
      usePluginFrameState({
        slug: 'groceries',
        pluginName: 'Groceries',
        frameRef,
        bridge,
        active: true,
      }),
    )

    await act(async () => {
      await Promise.resolve()
    })

    expect(pluginWindow.postMessage).toHaveBeenCalledWith(
      { type: 'hearth.frame.state', state: 'loading' },
      window.location.origin,
    )
  })

  it('ignores hearth.title from a different iframe', async () => {
    const bridge = mountBridge()
    const iframe = setupIframe('groceries', mockContentWindow())
    const other = setupIframe('other', mockContentWindow())
    const frameRef = { current: iframe }

    const { result } = renderHook(() =>
      usePluginFrameState({
        slug: 'groceries',
        pluginName: 'Groceries',
        frameRef,
        bridge,
        active: true,
      }),
    )

    await act(async () => {
      await Promise.resolve()
    })

    act(() => {
      iframe.dispatchEvent(new Event('load'))
      deliverFromFrame(other, { type: 'hearth.title', title: 'Other' })
    })

    expect(result.current.state).toBe('loading')
  })
})
