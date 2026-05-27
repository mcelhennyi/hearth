import { cleanupOutdatedCaches, precacheAndRoute } from 'workbox-precaching'
import type { PrecacheEntry } from 'workbox-precaching'
import { clientsClaim } from 'workbox-core'

interface PushMessageEvent extends Event {
  data?: {
    json(): unknown
  }
  waitUntil(promise: Promise<unknown>): void
}

interface NotificationClickEvent extends Event {
  notification: Notification & { data?: unknown }
  waitUntil(promise: Promise<unknown>): void
}

interface ServiceWorkerRuntime {
  __WB_MANIFEST: Array<string | PrecacheEntry>
  skipWaiting(): void
  addEventListener(type: 'push', listener: (event: PushMessageEvent) => void): void
  addEventListener(type: 'notificationclick', listener: (event: NotificationClickEvent) => void): void
  registration: {
    showNotification(title: string, options?: NotificationOptions): Promise<void>
  }
  clients: {
    openWindow(url: string): Promise<unknown>
  }
}

const sw = globalThis as unknown as ServiceWorkerRuntime

sw.skipWaiting()
clientsClaim()
cleanupOutdatedCaches()
precacheAndRoute(sw.__WB_MANIFEST)

sw.addEventListener('push', (event: PushMessageEvent) => {
  const payload = event.data?.json() as { title?: string; body?: string; url?: string } | undefined
  const title = payload?.title ?? 'Hearth'
  const body = payload?.body ?? 'You have a new update.'
  const url = payload?.url ?? '/'

  event.waitUntil(
    sw.registration.showNotification(title, {
      body,
      data: { url },
      badge: '/logo.svg',
      icon: '/logo.svg',
    }),
  )
})

sw.addEventListener('notificationclick', (event: NotificationClickEvent) => {
  event.notification.close()
  const targetUrl = (event.notification.data?.url as string | undefined) ?? '/'
  event.waitUntil(sw.clients.openWindow(targetUrl))
})
