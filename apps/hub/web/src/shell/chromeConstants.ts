// Chrome slot limits — docs/design/mantle-ui.md §"Declaring chrome slots" (DG-U6).
import type { ChromeSlot } from './types'

/** Max registrations per (slot, surface); excess mounts receive hearth.chrome.error. */
export const CHROME_SLOT_MAX_ITEMS = 8

/** Visible items before overflow ⋯ menu collapses the rest. */
export const CHROME_VISIBLE_CAP: Record<ChromeSlot, number> = {
  top: 3,
  bottom: 4,
}
