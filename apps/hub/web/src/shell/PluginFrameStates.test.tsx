import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

import { PluginFrameStates } from './PluginFrameStates'

describe('PluginFrameStates', () => {
  it('renders nothing when mounted', () => {
    const { container } = render(
      <PluginFrameStates
        state="mounted"
        pluginName="Groceries"
        errorDetail={null}
        showSlowReload={false}
        onReload={vi.fn()}
        onTryAgain={vi.fn()}
      />,
    )
    expect(container.firstChild).toBeNull()
  })

  it('shows slow subtitle and reload when requested', () => {
    render(
      <PluginFrameStates
        state="slow"
        pluginName="Groceries"
        errorDetail={null}
        showSlowReload
        onReload={vi.fn()}
        onTryAgain={vi.fn()}
      />,
    )
    expect(screen.getByText(/Still loading Groceries/)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Reload' })).toBeInTheDocument()
  })

  it('shows offline card with Try again', () => {
    const onTryAgain = vi.fn()
    render(
      <PluginFrameStates
        state="offline"
        pluginName="Groceries"
        errorDetail={null}
        showSlowReload={false}
        onReload={vi.fn()}
        onTryAgain={onTryAgain}
      />,
    )
    screen.getByRole('button', { name: 'Try again' }).click()
    expect(onTryAgain).toHaveBeenCalledTimes(1)
  })

  it('shows error card with details', () => {
    render(
      <PluginFrameStates
        state="error"
        pluginName="Groceries"
        errorDetail="HTTP 503"
        showSlowReload={false}
        onReload={vi.fn()}
        onTryAgain={vi.fn()}
      />,
    )
    expect(screen.getByText(/Groceries failed to load/)).toBeInTheDocument()
    expect(screen.getByText('HTTP 503')).toBeInTheDocument()
  })
})
