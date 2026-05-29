# T-FR-0007-03 - Rewire Hearth to consume Kindling Mantle

## 2026-05-29 - Ticket completion

**Branch:** `feat/FR-0007-kindling-mantle-migration-T-FR-0007-03-rewire-hearth-kindling-mantle`

**Scope:** Rewired Hearth hub web package resolution so local development consumes `@kindling/mantle` from the Kindling submodule workspace instead of the deleted Hearth-local `packages/mantle/` package.

**TEST:** Ran the package-resolution check inside the Docker web tooling container:

```bash
./develop web sh -lc 'corepack enable && corepack prepare pnpm@9.15.4 --activate && cd /workspace && pnpm --filter web exec node -e "console.log(import.meta.resolve(\"@kindling/mantle\"))"'
```

It failed with `ERR_MODULE_NOT_FOUND`, proving hub web did not resolve `@kindling/mantle` after the Hearth-local package removal. A broader `pnpm --filter web run build` also failed in the container before the fix, but that surfaced missing Workbox direct dependencies rather than the Mantle resolution edge, so the focused resolver failure is the ticket's TEST signal.

**DEV:** Added `kindling/mantle` to the pnpm workspace, added `@kindling/mantle` as a hub web workspace dependency, imported Mantle tokens via `@kindling/mantle/styles.css`, and added a Vitest guard that resolves the Mantle style export from `/kindling/mantle/` and rejects `/packages/mantle/`. Added direct Workbox dependencies and the WebWorker lib entry needed for the existing service worker build in the same containerized validation path.

**VAL:** All validation ran through the Docker web tooling wrapper:

```bash
./develop web sh -lc 'corepack enable && corepack prepare pnpm@9.15.4 --activate && cd /workspace && pnpm install'
./develop web sh -lc 'corepack enable && corepack prepare pnpm@9.15.4 --activate && cd /workspace && pnpm --filter web exec node -e "const resolved = import.meta.resolve(\"@kindling/mantle/styles.css\"); console.log(resolved); if (!resolved.includes(\"/kindling/mantle/\") || resolved.includes(\"/packages/mantle/\")) process.exit(1)"'
./develop web sh -lc 'corepack enable && corepack prepare pnpm@9.15.4 --activate && cd /workspace && pnpm --filter web run test'
./develop web sh -lc 'corepack enable && corepack prepare pnpm@9.15.4 --activate && cd /workspace && pnpm --filter web run build'
```

Results: install completed across 3 workspace projects; resolver printed `file:///workspace/kindling/mantle/src/tokens.css`; Vitest passed 16 files / 61 tests; web build completed and generated the PWA service worker.

**Docs validation:** `docker compose -f deploy/compose/docker-compose.yml run --rm --no-deps docs build` passed in the docs container with the repository's pre-existing MkDocs nav/link warnings.

**Notes:** Docker Compose printed pre-existing orphan container warnings for unrelated services. Tests still print pre-existing React `act(...)` warnings in several cases, but the suite exits successfully. Optional `pnpm --filter web run lint` was run inside `./develop web` and remains blocked by pre-existing React Hooks / Fast Refresh / `any` lint findings across App, dashboard edit, shell, service worker, and theme files; those are outside the Mantle consumption wiring scope.
