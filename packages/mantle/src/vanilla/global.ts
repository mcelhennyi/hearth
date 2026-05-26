// IIFE entry — exposes `window.mantle` for <script>-tag plugins (T-FR-0006-14).

import { mantle } from "./index";

export { mantle };

if (typeof globalThis !== "undefined") {
  (globalThis as typeof globalThis & { mantle: typeof mantle }).mantle = mantle;
}
