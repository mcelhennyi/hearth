import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'

const srcDir = dirname(fileURLToPath(import.meta.url))
const shellSource = readFileSync(join(srcDir, 'App.tsx'), 'utf8')

describe('Mantle shell plugin agnosticism', () => {
  it('does not hardcode prototype plugin routes', () => {
    expect(shellSource).not.toMatch(/\/groceries/)
    expect(shellSource).not.toMatch(/\/recipes/)
    expect(shellSource).not.toMatch(/\/ideas/)
    expect(shellSource).not.toMatch(/Groceries/)
    expect(shellSource).not.toMatch(/Recipes/)
  })
})
