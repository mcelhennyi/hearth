# Kindling — shared templates repo

**Status:** real repo exists and is consumed by Hearth as a submodule, but some Kindling-owned product surface still has temporary Hearth-side source mirrors from earlier FRs.

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

<!-- AMENDMENT: KINDLING-MANTLE-MIGRATION-0001 -->
<!-- Author: Codex session -->
<!-- Date: 2026-05-27 -->
<!-- Reason: FR-0006 shipped a private Hearth-side @kindling/mantle package; FR-0007 makes Kindling the source owner so standalone app repos can depend on Kindling without a Hearth checkout. -->

FR-0007 transitions Mantle from the temporary Hearth-authored package at `packages/mantle/` to a Kindling-owned package source. The target state is:

- Kindling owns the `@kindling/mantle` source, tests, changelog, package metadata, and release path.
- Hearth consumes `@kindling/mantle` from the Kindling submodule/workspace during local development and from a pinned package or tagged source in CI/production.
- Plugin/app repositories depend on `@kindling/mantle`; they never import Mantle from a Hearth-relative path.
- Plugin compliance is versioned: a plugin is compatible with a Hearth host when its declared Kindling/Mantle major range is accepted by that host.

### Mantle ownership contract

| Surface | Owner | Contract |
|---------|-------|----------|
| Mantle source and tests | Kindling | Authoritative source for `@kindling/mantle` lives under Kindling's `mantle/` package workspace, including component/hook/bridge implementation, styles, unit tests, type tests, package build config, and release fixtures. |
| Package metadata | Kindling | `package.json`, package exports, dependency policy, version, publish/tag metadata, and package README/changelog are maintained with the Kindling Mantle source. |
| Release path | Kindling | Kindling publishes or tags `@kindling/mantle` releases. Hearth pins a released package version or immutable tagged source for CI/production rather than treating a Hearth-local package tree as canonical. |
| Local Hearth development | Hearth + Kindling | Hearth may mount the Kindling checkout as a submodule/workspace so local `apps/hub/web` work resolves `@kindling/mantle` without network publishing. This is a development convenience, not ownership. |
| Plugin/app repos | Plugin maintainer + Kindling | Generated and downstream repos declare `@kindling/mantle` as a package dependency. They must not import from `hearth/packages/mantle`, `apps/hub/web/src`, or any other Hearth-relative Mantle path. |
| Compatibility declaration | Hearth + Kindling | A plugin is compatible when its manifest/package metadata declares a supported Kindling/Mantle version range accepted by the target Hearth host. Hearth validation reports the accepted range when the declaration is missing or unsupported. |

### Transition states

| State | Meaning | Allowed use |
|-------|---------|-------------|
| FR-0006 private package | `packages/mantle/` existed in Hearth as the private package proven by FR-0006. | Historical source for the FR-0007 move. Do not copy it into plugin repos or document it as an app dependency. |
| FR-0007 migration | Kindling Mantle source is populated at `kindling/mantle/` and Hearth is being rewired. | Hearth no longer treats `packages/mantle/` as authoritative. New templates and plugin docs still point at `@kindling/mantle`. |
| Target state | Kindling owns Mantle; Hearth consumes the package. | `packages/mantle/` is absent unless restored as an explicit temporary rollback fixture. CI/production uses a pinned Kindling package or immutable tag. |

As of T-FR-0007-02, `kindling/mantle/` is the package source location. Any temporary Hearth-side mirror restored during migration must name the Kindling-owned end state in its README, changelog, or ticket diary and must be removed or downgraded to fixtures before FR-0007 closeout.

As of T-FR-0007-03, Hearth's hub web workspace includes `kindling/mantle/` and declares `@kindling/mantle` as a workspace dependency. Local development and CI builds resolve Mantle through the pinned Kindling submodule SHA; production/release builds may swap that workspace edge for the matching Kindling package artifact or immutable tag, but must keep package imports under `@kindling/mantle` rather than `packages/mantle/`.

### Downstream compatibility rule

Kindling-based plugin/app repos declare the Mantle contract in package metadata and, when available, in Tinder compatibility metadata. The supported range is a Kindling/Mantle major range such as `^1` or `>=1 <2`, not a Hearth git path. Hearth hosts validate that declaration before install or release; Kindling templates stamp the current accepted range by default so standalone development and Hearth-hosted plugin mode use the same package surface.

<!-- /AMENDMENT -->

Hearth pulls Kindling in as a submodule at `kindling/`. The hub web app imports `@kindling/mantle` from the local checkout in dev (via `pnpm` workspace alias) and from a versioned npm-equivalent registry (or a tagged git URL) in CI/production.

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

## What it is **not**

- A plugin marketplace.
- A Hearth fork or alternative.
- A general React component library — every primitive in Mantle exists because Hearth needs it.

## Bootstrapping order

1. Hearth ticket **`T-FR-0001-04`** scaffolds the Mantle shell stub *inside* `apps/hub/web/` (no Kindling repo yet) so we have something to iterate on.
2. Ticket **`T-FR-0001-07`** lifts that shell out into a fresh Kindling repo, sets up the submodule, and `apps/hub/web/` becomes a thin consumer.
3. Ticket **`T-FR-0001-08`** scaffolds the first plugin in **[`grocery-list`](https://github.com/mcelhennyi/grocery-list)** via `kindling new groceries`, pushes to that remote, and adds `apps/groceries/` as a submodule in Hearth—exercising the full template path without vendoring plugin code into the hub tree.

Until ticket 07 lands, "Kindling" is the directory `apps/hub/web/src/mantle/` and `apps/hub/api/spark/`. The repo split is a deliberate later step so we don't churn the layout twice.
