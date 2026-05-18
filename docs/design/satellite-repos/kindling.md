# Kindling — shared templates repo

**Status:** design only. No code yet. Lives at the planned URL `git@github.com:mcelhennyi/kindling.git` and is consumed by Hearth as a submodule under `vendor/kindling/`.

Kindling does for **Hearth plugin authors** what `.skeleton` does for **process and tooling**: it materializes a working starting point. It is the home for things every Hearth project needs and that we refuse to fork-and-paste:

| Subdirectory | What it ships |
|--------------|---------------|
| `templates/plugin-python/` | A scaffold for a Python (FastAPI) + React plugin: `tinder.toml`, `pyproject.toml`, `app/`, `web/` (Vite), test harness, Compose service stub. |
| `templates/plugin-node/`   | A scaffold for a TypeScript-only plugin (Fastify + React). Same `tinder.toml`. |
| `mantle/`                  | The shared shell: React components, theme tokens, hooks (`useMantle`, `useUser`, `useSpark`, `useNotifications`), service worker template, manifest template. Published as `@kindling/mantle`. |
| `spark/`                   | Spark client libraries — `kindling.spark` (Python) and `@kindling/spark` (TS). Mirrors `docs/design/spark-api.md` 1:1. |
| `tinder/`                  | Tinder schema + validator (Python and TS), so plugins can self-check their manifest in CI. |
| `cli/`                     | `kindling` CLI: `kindling new <slug>`, `kindling validate`, `kindling install <slug>` (registers a plugin with a running hub via its API), `kindling publish` (push a release tag). |
| `docs/`                    | Author's-eye docs that mirror the public design surface in Hearth (Spark cookbook, Tinder cheatsheet, Mantle component gallery). |
| `.skeleton/`               | Same process skeleton as Hearth, so Kindling itself follows the FR-NNNN flow. |

## Usage from Hearth

Hearth pulls Kindling in as a submodule at `vendor/kindling/`. The hub web app imports `@kindling/mantle` from the local checkout in dev (via `pnpm` workspace alias) and from a versioned npm-equivalent registry (or a tagged git URL) in CI/production.

Plugins under `apps/<slug>/` are themselves git submodules. A new plugin is created by:

```bash
kindling new groceries
# materializes apps/groceries/ + tinder.toml, registers the plugin with the local hub
./develop up
```

`kindling new` does roughly what `init-skeleton` does for the platform: clones the right template, points `.skeleton`-style submodules where they need to go, and stamps the chosen slug.

Until the public Kindling repository exists, Hearth mirrors the plugin template contract in `deploy/kindling-contract/` so FR-0003 can validate operator flows without inventing an external repo. That mirror must produce a plugin root containing:

| Path | Contract |
|------|----------|
| `tinder.toml` | Minimal Tinder manifest using the plugin slug and a Python backend entrypoint. |
| `scripts/install` | Executable install hook run by `hearth --plugin --add` / update flows; non-zero exit aborts the operation with its stderr/stdout surfaced to the operator. |
| `plugin` | Executable per-plugin admin shim with common lifecycle flags and passthrough to `python -m <plugin>.admin` when invoked as `plugin -- <args>` or with plugin-defined args. |

When Kindling becomes a real submodule, the Hearth mirror should be deleted or converted to fixtures only after equivalent upstream tests prove `kindling new <slug>` still renders these paths.

## Relationship to `.skeleton`

`.skeleton` is **process** (tickets, FR-NNNN flow, AI rules). Kindling is **product surface** (Mantle, Spark client, Tinder validator, plugin templates). A new plugin repo will have **both**: it `init-skeleton`'s the process tree and consumes Kindling's templates for the actual app code.

## Versioning

- Mantle, Spark client, and Tinder schema are versioned together as `@kindling/*` semver. A plugin pins a major.
- `tinder.schema = "1"` lives in `kindling/tinder/schemas/v1.json` and is the authoritative wire format that the hub validates against.
- Breaking changes go through Hearth's amendment process (`docs/ai-context.md`) — the spec lives in Hearth, the implementation lives in Kindling.

## What it is **not**

- A plugin marketplace.
- A Hearth fork or alternative.
- A general React component library — every primitive in Mantle exists because Hearth needs it.

## Bootstrapping order

1. Hearth ticket **`T-FR-0001-04`** scaffolds the Mantle shell stub *inside* `apps/hub/web/` (no Kindling repo yet) so we have something to iterate on.
2. Ticket **`T-FR-0001-07`** lifts that shell out into a fresh Kindling repo, sets up the submodule, and `apps/hub/web/` becomes a thin consumer.
3. Ticket **`T-FR-0001-08`** ships the first plugin (`groceries`) using `kindling new groceries`, exercising the full template path.

Until ticket 07 lands, "Kindling" is the directory `apps/hub/web/src/mantle/` and `apps/hub/api/spark/`. The repo split is a deliberate later step so we don't churn the layout twice.
