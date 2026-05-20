import { describe, expect, it } from 'vitest'

import shellSource from './App.tsx?raw'

describe('Mantle shell plugin agnosticism', () => {
  it('does not hardcode prototype plugin routes', () => {
    expect(shellSource).not.toMatch(/\/groceries/)
    expect(shellSource).not.toMatch(/\/recipes/)
    expect(shellSource).not.toMatch(/\/ideas/)
    expect(shellSource).not.toMatch(/Groceries/)
    expect(shellSource).not.toMatch(/Recipes/)
  })
})
