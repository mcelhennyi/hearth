// PluginFrame — sandboxed iframe for an app plugin at /<slug>/.
//
// All frames stay mounted when inactive (display:none) to preserve plugin state.
// Frame lifecycle overlays: shell/PluginFrameStates.tsx (T-FR-0006-05).
// postMessage protocol: shell/usePostMessageBridge.ts (T-FR-0006-03).

import { useRef } from 'react'

import { PluginFrameStates } from '../shell/PluginFrameStates'
import type { Bridge } from '../shell/types'
import { usePluginFrameState } from '../shell/usePluginFrameState'

export interface PluginFrameProps {
  slug: string
  name: string
  active: boolean
  bridge: Bridge
}

export function PluginFrame({ slug, name, active, bridge }: PluginFrameProps) {
  const frameRef = useRef<HTMLIFrameElement>(null)
  const { state, errorDetail, showSlowReload, reload, tryAgain } = usePluginFrameState({
    slug,
    pluginName: name,
    frameRef,
    bridge,
    active,
  })

  function openSettings() {
    window.dispatchEvent(new CustomEvent('hearth:open-settings'))
  }

  return (
    <main
      className="plugin-frame-host relative flex min-h-0 flex-1 flex-col pb-[calc(var(--hearth-bar-h,52px)+var(--hearth-safe-bottom))] pt-0"
      style={active ? undefined : { display: 'none' }}
      aria-hidden={!active}
    >
      <div className="plugin-frame relative min-h-0 flex-1 w-full">
        <iframe
          ref={frameRef}
          title={name}
          data-plugin-slug={slug}
          src={`/${slug}/?embed=1`}
          sandbox="allow-scripts allow-same-origin allow-forms"
          className="h-full w-full rounded-none border-0 bg-[var(--hearth-bg)] md:rounded-lg md:border md:border-[var(--hearth-surface)]"
        />
        {active && (
          <PluginFrameStates
            state={state}
            pluginName={name}
            errorDetail={errorDetail}
            showSlowReload={showSlowReload}
            onReload={reload}
            onTryAgain={tryAgain}
            onOpenSettings={openSettings}
          />
        )}
      </div>
    </main>
  )
}
