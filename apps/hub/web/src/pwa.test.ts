import { beforeEach, describe, expect, it, vi } from 'vitest'
import { registerServiceWorker } from './pwa'

describe('registerServiceWorker', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('registers /sw.js when service workers are available', () => {
    const register = vi.fn().mockResolvedValue(undefined)
    Object.defineProperty(window.navigator, 'serviceWorker', {
      value: { register },
      configurable: true,
    })

    registerServiceWorker()
    expect(register).toHaveBeenCalledWith('/sw.js')
  })
})
