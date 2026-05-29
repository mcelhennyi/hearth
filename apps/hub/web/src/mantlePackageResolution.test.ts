import { describe, expect, it } from 'vitest'

describe('Kindling Mantle package resolution', () => {
  it('resolves Mantle styles from the Kindling workspace package', () => {
    const resolved = import.meta.resolve('@kindling/mantle/styles.css')

    expect(resolved).toContain('/kindling/mantle/')
    expect(resolved).not.toContain('/packages/mantle/')
  })
})
