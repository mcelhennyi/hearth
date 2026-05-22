# @kindling/mantle

Mantle UI primitives, hooks, design tokens, and a vanilla (non-React) bridge for plugins running inside the Hearth shell iframe.

Published from the [hearth](https://github.com/mcelhennyi/hearth) monorepo (`packages/mantle`). See [CHANGELOG](./CHANGELOG.md) for release notes.

## Install

```bash
pnpm add @kindling/mantle
# or: npm install @kindling/mantle
```

Requires **React 18+** for the component and hook exports. The vanilla bridge and types work without React.

## Minimal React plugin example

Import styles once in your plugin entry, wrap the app in `MantleProvider`, and use shell-aware hooks:

```tsx
// src/main.tsx
import "@kindling/mantle/styles.css";
import "@kindling/mantle/components.css";

import { MantleProvider, Page, PageHeader, Card, Button, useTheme } from "@kindling/mantle";

function GroceriesHome() {
  const { theme } = useTheme();
  return (
    <Page>
      <PageHeader title="Groceries" />
      <Card>
        <p>Current theme: {theme.mode}</p>
        <Button variant="accent">Add item</Button>
      </Card>
    </Page>
  );
}

export function App() {
  return (
    <MantleProvider>
      <GroceriesHome />
    </MantleProvider>
  );
}
```

For the full plugin UI contract (chrome slots, frame states, overlay escape, non-React plugins), see Kindling's **[Plugin UI system](https://github.com/mcelhennyi/kindling/blob/main/docs/design/plugin-ui-system.md)** design doc. Hearth shell behavior is specified in [`docs/design/mantle-ui.md`](../../docs/design/mantle-ui.md).

## Exports

| Import path | Purpose |
|-------------|---------|
| `@kindling/mantle` | React components, hooks, `MantleProvider`, bridge helpers |
| `@kindling/mantle/styles.css` | Design tokens (`--hearth-*`) |
| `@kindling/mantle/components.css` | Component layout and variants |
| `@kindling/mantle/vanilla` | `mantle.theme` and `mantle.chrome` for non-React plugins |
| `@kindling/mantle/vanilla/mantle.iife` | Script-tag IIFE bundle |
| `@kindling/mantle/types` | Pure TypeScript types (no runtime) |

## Vanilla (non-React) snippet

```html
<link rel="stylesheet" href="/node_modules/@kindling/mantle/src/tokens.css" />
<script src="/node_modules/@kindling/mantle/dist/vanilla/mantle.iife.js"></script>
<script>
  mantle.theme.subscribe(({ tokens }) => {
    document.documentElement.style.setProperty("--hearth-bg", tokens.bg);
  });
  mantle.chrome.mount({ slot: "top", items: [{ kind: "button", id: "add", label: "Add" }] });
</script>
```

## Build from source

```bash
pnpm --filter @kindling/mantle build
pnpm --filter @kindling/mantle test
pnpm --filter @kindling/mantle publish:dry-run
```

In Docker (hearth dev loop): `./develop web sh -lc 'cd /workspace && pnpm --filter @kindling/mantle test'`.

## Publishing (maintainers)

Versioning is **manual** — bump `version` in `package.json` and add a [CHANGELOG](./CHANGELOG.md) entry before tagging.

1. Merge mantle changes to the integration branch and confirm **kindling-mantle CI** is green (`npm publish --dry-run` in `.github/workflows/kindling-mantle-ci.yml`).
2. Tag the commit: `git tag kindling-mantle-v0.1.0 && git push origin kindling-mantle-v0.1.0`
3. **kindling-mantle publish** workflow runs `npm publish --access=public` when the tag is pushed.

The tag suffix must match `package.json` `version` (e.g. tag `kindling-mantle-v0.1.0` → `"version": "0.1.0"`).

**Registry setup:** create an npm automation token with publish access to the `@kindling` scope and add it as repository secret **`NPM_TOKEN`**. Without that secret, CI dry-run still passes; the publish workflow fails at the publish step until configured.

## Authoritative design docs

- Shell + iframe contract: [`docs/design/mantle-ui.md`](../../docs/design/mantle-ui.md)
- Plugin UI system (Kindling): [plugin-ui-system.md](https://github.com/mcelhennyi/kindling/blob/main/docs/design/plugin-ui-system.md)
- Feature history: [`tasks/feature-history/FR-0006-design-language/`](../../tasks/feature-history/FR-0006-design-language/)

## License

MIT — see [`LICENSE`](./LICENSE).
