import { cleanupOutdatedCaches, precacheAndRoute } from 'workbox-precaching'
import { clientsClaim } from 'workbox-core'

declare let self: ServiceWorkerGlobalScope
const sw = self as unknown as any

sw.skipWaiting()
clientsClaim()
cleanupOutdatedCaches()
precacheAndRoute(sw.__WB_MANIFEST)

sw.addEventListener('push', (event: any) => {
  const pushEvent = event
  const payload = pushEvent.data?.json() as { title?: string; body?: string; url?: string } | undefined
  const title = payload?.title ?? 'Hearth'
  const body = payload?.body ?? 'You have a new update.'
  const url = payload?.url ?? '/'

  pushEvent.waitUntil(
    sw.registration.showNotification(title, {
      body,
      data: { url },
      badge: '/logo.svg',
      icon: '/logo.svg',
    }),
  )
})

sw.addEventListener('notificationclick', (event: any) => {
  const clickEvent = event
  clickEvent.notification.close()
  const targetUrl = (clickEvent.notification.data?.url as string | undefined) ?? '/'
  clickEvent.waitUntil(sw.clients.openWindow(targetUrl))
})
