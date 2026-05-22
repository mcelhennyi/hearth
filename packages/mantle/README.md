# @kindling/mantle

Mantle UI primitives, hooks, design tokens, and a vanilla (non-React) bridge for plugins running inside the Hearth shell.

> Components, hooks, and overlays land in T-FR-0006-11..13; the **vanilla bridge** (T-FR-0006-14) is implemented. Published from the [hearth repo](https://github.com/mcelhennyi/hearth).

## Quickstart

```bash
pnpm add @kindling/mantle
```

```ts
// Tokens as CSS (import once in your plugin entry):
import "@kindling/mantle/styles.css"; // or "@kindling/mantle/tokens"

// React surface (post T-FR-0006-11/12):
import { /* Page, Button, useTheme, ... */ } from "@kindling/mantle";

// Non-React bridge:
import { mantle } from "@kindling/mantle/vanilla";

mantle.theme.subscribe((tokens) => {
  console.log("theme", tokens.mode);
});

const unmount = mantle.chrome.mount({
  slot: "top",
  surface: "app",
  payload: { kind: "button", id: "add", label: "Add" },
});
// later: unmount();
```

```html
<!-- Script-tag plugins (no bundler): -->
<script src="/node_modules/@kindling/mantle/dist/vanilla/mantle.iife.js"></script>
<script>
  mantle.theme.subscribe(() => {});
</script>
```

```ts
// Pure types (no runtime):
import type { ChromeButton, FrameState, ThemeTokens } from "@kindling/mantle/types";
```

## What it provides (target surface)

- **Tokens** — `--hearth-*` CSS custom properties (dark default; light via `prefers-color-scheme`).
- **React components** — `Page`, `PageHeader`, `Card`, `Section`, `List`, `EmptyState`, `Button`, `IconButton`, `Input`, `TextArea`, `Select`, `Switch`, `Sheet`, `Toast`, `Dialog`.
- **React hooks** — `useMantle`, `useUser`, `useTheme`, `useSpark`, `useHaptics`, `useNotifications`, `useChromeSlot`.
- **Vanilla bridge** — imperative `chrome` and `theme` adapters for non-React plugins.
- **Types** — `ChromeButton`, `ChromeMenu`, `FrameState`, `ThemeTokens`, and the postMessage envelopes.

## Authoritative design docs

- Shell + plugin contract: [`docs/design/mantle-ui.md`](../../docs/design/mantle-ui.md)
- Plugin UI system (Kindling side): [`kindling/docs/design/plugin-ui-system.md`](../../kindling/docs/design/plugin-ui-system.md) (when present in your checkout)
- Feature design: [`tasks/feature-history/FR-0006-design-language/`](../../tasks/feature-history/FR-0006-design-language/)

## Build

```bash
pnpm --filter @kindling/mantle build       # ESM + CJS + .d.ts + vanilla IIFE via tsup
pnpm --filter @kindling/mantle typecheck   # tsc --noEmit
```

## License

MIT — see [`LICENSE`](./LICENSE).
