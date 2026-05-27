# FR-0007 - Design (level 0, skeleton)

## Purpose

Make Kindling the developer-facing source of truth for Mantle so plugin/app repositories can run outside the Hearth monorepo and still satisfy Hearth plugin UI contracts by depending on a compatible `@kindling/mantle` release.

## Actors

- **Hearth hub**: canonical runtime host and deployment path.
- **Kindling repo**: SDK/template/package owner for Mantle, Spark, Tinder, and plugin scaffolds.
- **Kindling-based app/plugin repo**: standalone app codebase that can run in local development and be mounted into Hearth as a plugin.
- **Downstream agent/maintainer**: updates existing plugin repos using Kindling changelog instructions.

## Public surfaces (skeleton)

| Surface | Kind | Contract (signature / schema sketch) | Owner (logical) |
|---------|------|----------------------------------------|-----------------|
| `@kindling/mantle` | npm package | React components, hooks, token CSS, vanilla bridge, and package exports currently proven by FR-0006. Package version is the plugin compliance handle. | Kindling |
| `kindling/mantle/` | source directory | Authoritative package source for `@kindling/mantle`; includes tests, changelog, package metadata, and build config. | Kindling |
| Hearth Mantle consumption | workspace/package dependency | Hearth imports `@kindling/mantle` through Kindling workspace/submodule during local dev and from a versioned package or tagged source in CI/production. | Hearth |
| Kindling templates | generated repo contract | Templates add `@kindling/mantle` dependency, dev scripts, Vite wiring, token CSS imports, and validation commands for standalone plugin development. | Kindling |
| Plugin compliance | validation rule | Plugin is compliant when its manifest and package dependency declare a Mantle/Kindling major accepted by the target Hearth host. | Hearth + Kindling |
| Kindling changelog | downstream migration doc | Every package/template compatibility change states who must update, required edits, verification, and fallback. | Kindling |

## Data in / out

| Input | Output | Storage |
|-------|--------|---------|
| FR-0006 private Hearth package at `packages/mantle/` | Kindling-owned Mantle source and package release surface at `kindling/mantle/` | Kindling repo, pinned by Hearth submodule or package lock |
| Plugin repo dependency constraints | Compatibility pass/fail and standalone dev install | Plugin `package.json`, `tinder.toml`, lockfile |
| Kindling changelog entry | Downstream migration checklist | Kindling `CHANGELOG.md`; optional Hearth handoff pointer |

## Open questions

- Whether `@kindling/mantle` first becomes a private git/package dependency or is published publicly as part of this FR.
- Whether Hearth keeps `packages/mantle/` as a temporary compatibility fixture for one release or removes it in the same migration. **T-FR-0007-02 decision:** remove it when `kindling/mantle/` becomes authoritative; T-FR-0007-03 rewires Hearth consumption.
- Exact package manager workspace shape once the Kindling submodule is initialized in the Hearth checkout.
