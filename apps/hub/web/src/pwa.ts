export function registerServiceWorker(): void {
  if (!('serviceWorker' in navigator)) {
    return
  }

  void navigator.serviceWorker.register('/sw.js')
}
