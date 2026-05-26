# Kindling — shared templates repo

**Status:** design only. No code yet. Lives at the planned URL `git@github.com:mcelhennyi/kindling.git` and is consumed by Hearth as a submodule under `vendor/kindling/`.

## Bootstrap: skeleton first, then Hearth product surface

Kindling is **not** a greenfield repo. It is created from the same **`.skeleton`** process template Hearth uses, then extended with Hearth-specific directories (Mantle, Spark clients, Tinder schema, plugin templates, CLI).

| Layer | Source | Purpose |
|-------|--------|---------|
| **Process** | **`.skeleton/` git submodule** inside Kindling (same revision policy as Hearth) | FR-NNNN workflow, AI rules, ticket layout, `./develop` patterns |
| **Product** | Kindling-owned dirs (`mantle/`, `spark/`, `tinder/`, `templates/`, `cli/`) | Shared code and scaffolds plugin authors consume |

**Required layout in the Kindling repo:**

```text
kindling/                    # git@github.com:mcelhennyi/kindling.git
  .skeleton/                 # submodule → skeleton process repo (must stay present)
  mantle/
  spark/
  tinder/
  templates/
  cli/
  docs/
```

When Kindling is updated, run the same **`./sync-skeleton`** (or equivalent) workflow as Hearth so process files stay aligned. Hearth pins Kindling at `vendor/kindling/`; individual plugins pin Kindling (or published `@kindling/*` packages) in their own repos.

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
| `.skeleton/`               | **Git submodule** (required): same process skeleton as Hearth; Kindling follows the FR-NNNN flow and stays syncable via `./sync-skeleton`. |

## Usage from Hearth

Hearth pulls Kindling in as a submodule at `vendor/kindling/`. The hub web app imports `@kindling/mantle` from the local checkout in dev (via `pnpm` workspace alias) and from a versioned npm-equivalent registry (or a tagged git URL) in CI/production.

Plugins under `apps/<slug>/` are **separate git repositories** (submodules in Hearth). Hearth does **not** ship plugin source. A new plugin is created by:

```bash
# From a clean directory or the user's projects folder — not inside apps/hub/
kindling new groceries --remote git@github.com:mcelhennyi/grocery-list.git
cd grocery-list   # or the chosen directory name
# … develop, test, push …

# In the Hearth repo (after the remote exists):
git submodule add https://github.com/mcelhennyi/grocery-list.git apps/groceries
kindling install groceries   # or hub POST /api/plugins/install
./develop up
```

`kindling new`:

1. Clones `templates/plugin-python/` (or `plugin-node/`) into a **new repo**.
2. Runs **`init-skeleton`** (or equivalent) so the plugin repo gets its own **`.skeleton/`** submodule and process tree.
3. Wires **Kindling** consumption (`@kindling/mantle`, Spark/Tinder libs) per template.
4. Stamps `tinder.toml` with the chosen slug.
5. Optionally registers with a running hub via `kindling install`.

The first reference plugin for FR-0001 is **`groceries`**, developed in **[`mcelhennyi/grocery-list`](https://github.com/mcelhennyi/grocery-list)** and mounted at `apps/groceries/` in Hearth only as a submodule (**T-FR-0001-08**).

Until the public Kindling repository exists, Hearth mirrors the plugin template contract in `deploy/kindling-contract/` so FR-0003 can validate operator flows without inventing an external repo. That mirror must produce a plugin root containing:

| Path | Contract |
|------|----------|
| `tinder.toml` | Minimal Tinder manifest using the plugin slug and a Python backend entrypoint. |
| `scripts/install` | Executable install hook run by `hearth --plugin --add` / update flows; non-zero exit aborts the operation with its stderr/stdout surfaced to the operator. |
| `plugin` | Executable per-plugin admin shim with common lifecycle flags and passthrough to `python -m <plugin>.admin` when invoked as `plugin -- <args>` or with plugin-defined args. |

When Kindling becomes a real submodule, the Hearth mirror should be deleted or converted to fixtures only after equivalent upstream tests prove `kindling new <slug>` still renders these paths.

## Relationship to `.skeleton`

`.skeleton` is **process** (tickets, FR-NNNN flow, AI rules). Kindling is **product surface** (Mantle, Spark client, Tinder validator, plugin templates) **plus** its own `.skeleton/` submodule so Kindling's own FR-NNNN work matches Hearth.

A **new plugin repo** has **both**:

1. **`.skeleton/`** — process (from `kindling new` / `init-skeleton`).
2. **Kindling packages** — Mantle, Spark, Tinder (from template, not copied from `apps/hub/`).

Hearth has `.skeleton/` + `vendor/kindling/` + `apps/hub/` only. It must not grow plugin app trees except as **submodule pointers** under `apps/<slug>/`.

## Versioning

- Mantle, Spark client, and Tinder schema are versioned together as `@kindling/*` semver. A plugin pins a major.
- `tinder.schema = "1"` lives in `kindling/tinder/schemas/v1.json` and is the authoritative wire format that the hub validates against.
- Breaking changes go through Hearth's amendment process (`docs/ai-context.md`) — the spec lives in Hearth, the implementation lives in Kindling.

## Child-repo compliance changelog

Every change to the Kindling repo that affects generated plugin repos, templates, shared runtime packages, Tinder schema, Spark clients, Mantle APIs, or required development workflow must update a dense, AI-readable changelog entry before it is considered complete.

The changelog entry must give a downstream agent enough information to update child repos without rereading the whole Kindling diff:

| Field | Required content |
|-------|------------------|
| **Contract area** | Template, Mantle, Spark, Tinder, CLI, workflow, or docs. |
| **Compatibility** | Breaking, additive, deprecation, migration-only, or docs-only. |
| **Who must update** | Which child repos are affected and how to detect applicability. |
| **Required edits** | File patterns, symbols, manifests, commands, or config keys to change. |
| **Verification** | Exact tests, `kindling validate`, smoke checks, or manual checks that prove compliance. |
| **Fallback** | What an older child repo may safely do until migrated, if anything. |

This is a product-surface requirement, not release-note fluff: agents maintaining existing plugins such as `grocery-list` should be able to consume the changelog as a migration checklist.

## What it is **not**

- A plugin marketplace.
- A Hearth fork or alternative.
- A general React component library — every primitive in Mantle exists because Hearth needs it.

## Bootstrapping order

1. Hearth ticket **`T-FR-0001-04`** scaffolds the Mantle shell stub *inside* `apps/hub/web/` (no Kindling repo yet) so we have something to iterate on.
2. Ticket **`T-FR-0001-07`** lifts that shell out into a fresh Kindling repo, sets up the submodule, and `apps/hub/web/` becomes a thin consumer.
3. Ticket **`T-FR-0001-08`** scaffolds the first plugin in **[`grocery-list`](https://github.com/mcelhennyi/grocery-list)** via `kindling new groceries`, pushes to that remote, and adds `apps/groceries/` as a submodule in Hearth—exercising the full template path without vendoring plugin code into the hub tree.

Until ticket 07 lands, "Kindling" is the directory `apps/hub/web/src/mantle/` and `apps/hub/api/spark/`. The repo split is a deliberate later step so we don't churn the layout twice.
