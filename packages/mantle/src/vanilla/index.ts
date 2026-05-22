// @PROJ-U-* — @kindling/mantle vanilla bridge (FR-0006 T-FR-0006-14).
//
// Imperative adapters for non-React plugins embedded in the Hearth shell iframe.
// Import from `@kindling/mantle/vanilla` or load the IIFE build via script tag.

import { chrome } from "./chrome";
import { theme } from "./theme";

export { applyThemeTokens, theme } from "./theme";
export type { ThemeSubscriber } from "./theme";
export { chrome } from "./chrome";
export type { ChromeMountOptions } from "./chrome";
export { postToParent } from "./post";

/** Namespaced API: `mantle.theme.subscribe`, `mantle.chrome.mount`. */
export const mantle = { theme, chrome };
