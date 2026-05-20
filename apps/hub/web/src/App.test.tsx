import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { beforeEach, describe, expect, it } from 'vitest'
import App from './App'

function setBreakpoint(width: number): void {
  window.matchMedia = ((query: string) => ({
    matches: query === '(min-width: 768px)' ? width >= 768 : false,
    media: query,
    onchange: null,
    addEventListener: () => undefined,
    removeEventListener: () => undefined,
    addListener: () => undefined,
    removeListener: () => undefined,
    dispatchEvent: () => false,
  })) as typeof window.matchMedia
}

describe('Mantle layout breakpoint behavior', () => {
  beforeEach(() => {
    window.history.replaceState({}, '', '/')
  })

  it('shows bottom tabs under 768px', () => {
    setBreakpoint(390)
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>,
    )

    expect(screen.getByLabelText('Mantle bottom tabs')).toBeInTheDocument()
    expect(screen.queryByLabelText('Mantle top bar')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Send test notification' })).toBeInTheDocument()
  })

  it('shows top bar at and above 768px', () => {
    setBreakpoint(768)
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>,
    )

    expect(screen.getByLabelText('Mantle top bar')).toBeInTheDocument()
    expect(screen.queryByLabelText('Mantle bottom tabs')).not.toBeInTheDocument()
  })
})
