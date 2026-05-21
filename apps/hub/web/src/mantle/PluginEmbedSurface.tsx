// Chromeless plugin surface — rendered inside the shell iframe at /<slug>/?embed=1.
// Must not mount PluginFrame again (that would nest the full shell and duplicate headers).

import { useParams } from 'react-router-dom'

import { usePlugins } from '../usePlugins'

export function PluginEmbedSurface() {
  const { slug } = useParams<{ slug: string }>()
  const plugins = usePlugins()
  const plugin = plugins.find((p) => p.slug === slug)
  const title = plugin?.name ?? slug ?? 'Plugin'

  return (
    <main className="min-h-svh bg-[var(--hearth-bg)] px-4 py-6 text-[var(--hearth-fg)]">
      <h1 className="text-lg font-semibold">{title}</h1>
      <p className="mt-2 text-sm text-[var(--hearth-muted)]">
        Plugin UI loads here when the reverse proxy serves this plugin&apos;s static build at{' '}
        <code className="text-xs">/{slug}/</code>. On Docker-only installs without a plugin service,
        you may see this placeholder instead of the full app.
      </p>
    </main>
  )
}
