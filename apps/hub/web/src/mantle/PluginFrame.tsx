// PluginFrame — sandboxed iframe for an app plugin at /<slug>/.
//
// All frames stay mounted when inactive (display:none) to preserve plugin state.
// postMessage protocol (mantle-ui.md §"postMessage protocol"):
//   shell → plugin: {type:"hearth.theme", tokens}
//                   {type:"hearth.user", user}
//                   {type:"hearth.online", online}
//   plugin → shell: {type:"hearth.title", title}
//                   {type:"hearth.toast", level, message}
//                   {type:"hearth.nav", path}
//                   {type:"hearth.haptic", style}
//                   {type:"hearth.chrome.mount", …}
//                   {type:"hearth.chrome.unmount", …}

import { useCallback, useEffect, useRef } from 'react'

export interface HearthUser {
  id: string
  name?: string
  roles?: string[]
}

export interface PluginFrameProps {
  slug: string
  name: string
  active: boolean
  user: HearthUser
}

export function PluginFrame({ slug, name, active, user }: PluginFrameProps) {
  const iframeRef = useRef<HTMLIFrameElement | null>(null)

  const postUser = useCallback(() => {
    iframeRef.current?.contentWindow?.postMessage({ type: 'hearth.user', user }, window.location.origin)
  }, [user])

  useEffect(() => {
    function handleMessage(event: MessageEvent) {
      if (event.origin !== window.location.origin) return
      if (event.source !== iframeRef.current?.contentWindow) return
      if (!event.data || typeof event.data !== 'object') return
      if ((event.data as { type?: unknown }).type === 'hearth.user.request') {
        postUser()
      }
    }

    window.addEventListener('message', handleMessage)
    return () => window.removeEventListener('message', handleMessage)
  }, [postUser])

  return (
    <main
      className="mx-auto min-h-[60svh] w-full max-w-6xl px-0 pb-28 pt-0 md:pb-16"
      style={active ? undefined : { display: 'none' }}
      aria-hidden={!active}
    >
      <iframe
        ref={iframeRef}
        title={name}
        src={`/${slug}/?embed=1`}
        onLoad={postUser}
        // sandbox allows scripts and same-origin so the plugin can call its own API;
        // forms are allowed for plugin UI; popups are blocked to keep nav in shell.
        sandbox="allow-scripts allow-same-origin allow-forms"
        className="h-[70svh] w-full rounded-none border-0 bg-[var(--hearth-bg)] md:rounded-lg md:border md:border-[var(--hearth-surface)]"
      />
    </main>
  )
}
