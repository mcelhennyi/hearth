// Full Mantle shell rendered inside a plugin iframe — no chrome, no nested iframes.

import { Route, Routes } from 'react-router-dom'

import { PluginEmbedSurface } from './mantle/PluginEmbedSurface'

export function MantleEmbedApp() {
  return (
    <div className="min-h-svh bg-[var(--hearth-bg)] font-sans text-[var(--hearth-fg)]">
      <Routes>
        <Route path="/:slug/*" element={<PluginEmbedSurface />} />
        <Route path="*" element={<PluginEmbedSurface />} />
      </Routes>
    </div>
  )
}
