/** Detect Mantle running inside a plugin iframe (chromeless embed surface). */

export function isMantleEmbedMode(): boolean {
  if (typeof window === 'undefined') {
    return false
  }
  if (window.self !== window.top) {
    return true
  }
  return new URLSearchParams(window.location.search).has('embed')
}
