import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import App from './App'

vi.mock('./usePlugins', async (importOriginal) => {
  const actual = await importOriginal<typeof import('./usePlugins')>()
  return { ...actual, usePlugins: vi.fn(() => []) }
})

describe('Mantle embed mode (plugin iframe)', () => {
  beforeEach(() => {
    window.history.replaceState({}, '', '/groceries?embed=1')
  })

  it('does not render shell chrome or a nested plugin iframe', async () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>,
    )

    expect(screen.queryByLabelText('Mantle top bar')).not.toBeInTheDocument()
    expect(screen.queryByLabelText('Mantle bottom tabs')).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Send test notification' })).not.toBeInTheDocument()
    expect(document.querySelector('iframe')).not.toBeInTheDocument()
  })
})
