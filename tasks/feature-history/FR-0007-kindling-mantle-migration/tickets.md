# FR-0007 - Tickets

## Feature-complete gate

FR-0007 is complete when every ticket below has TEST, DEV, and VAL marked `done` in [`tasks/ticket-progress.md`](../../ticket-progress.md), Kindling owns the Mantle package surface, Hearth consumes that surface without treating `packages/mantle/` as authoritative, and one standalone Kindling-based app/plugin proves the dependency/compliance path.

### T-FR-0007-01 - Contract and transition docs

**Title:** Contract and transition docs

**Deps:** none

| Phase | Acceptance |
|-------|------------|
| **TEST** | A doc-oriented test or review checklist fails until the Kindling design states package ownership, compatibility, and transition rules. |
| **DEV** | Update `docs/design/satellite-repos/kindling.md`, FR docs, and tracker language so FR-0006 private Hearth package -> Kindling-owned package is explicit. |
| **VAL** | Docker MkDocs build passes or strict-mode warnings are recorded; links resolve for the new FR artifacts. |

### T-FR-0007-02 - Move Mantle package source to Kindling

**Title:** Move Mantle package source to Kindling

**Deps:** T-FR-0007-01

| Phase | Acceptance |
|-------|------------|
| **TEST** | Kindling package tests/build fail until `@kindling/mantle` source and package metadata exist under Kindling. |
| **DEV** | Move `packages/mantle/` source, tests, README, changelog, package metadata, and release config into Kindling-owned package layout. |
| **VAL** | Kindling Mantle package build, typecheck, test, and pack dry-run pass in the container/dev environment where available. |

### T-FR-0007-03 - Rewire Hearth to consume Kindling Mantle

**Title:** Rewire Hearth to consume Kindling Mantle

**Deps:** T-FR-0007-02

| Phase | Acceptance |
|-------|------------|
| **TEST** | Hearth hub web tests fail if imports resolve to a deleted/stale Hearth-local Mantle package instead of Kindling/package resolution. |
| **DEV** | Update pnpm/workspace/package config, submodule assumptions, and hub web imports so Hearth consumes `@kindling/mantle` from Kindling locally and from a pinned package/tag in CI/production. |
| **VAL** | Hearth web build/tests and package install run through `./develop` or documented container equivalent. |

### T-FR-0007-04 - Standalone Kindling app template support

**Title:** Standalone Kindling app template support

**Deps:** T-FR-0007-02

| Phase | Acceptance |
|-------|------------|
| **TEST** | A generated Kindling app template cannot run standalone until its package dependency, CSS imports, and dev harness are wired. |
| **DEV** | Update Kindling plugin/app templates to depend on `@kindling/mantle`, import Mantle tokens/components, and run standalone without a Hearth checkout while preserving plugin-mode behavior. |
| **VAL** | `kindling new` or equivalent template render plus standalone web tests/build pass for at least one template. |

### T-FR-0007-05 - Mantle version compliance validation

**Title:** Mantle version compliance validation

**Deps:** T-FR-0007-01, T-FR-0007-04

| Phase | Acceptance |
|-------|------------|
| **TEST** | Validation fails for a plugin/app declaring an unsupported `@kindling/mantle` major or missing the required Kindling compatibility metadata. |
| **DEV** | Add manifest/package validation so Hearth/Kindling can report whether a plugin supports the target Mantle/Kindling version before install or release. |
| **VAL** | Positive and negative validation cases pass; error messages tell plugin authors which dependency range to use. |

### T-FR-0007-06 - Downstream app proof and migration note

**Title:** Downstream app proof and migration note

**Deps:** T-FR-0007-03, T-FR-0007-04, T-FR-0007-05

| Phase | Acceptance |
|-------|------------|
| **TEST** | A selected standalone app/plugin cannot both run standalone and load into Hearth until the migrated dependency path is complete. |
| **DEV** | Update one downstream app/plugin proof path, preferably Planwright or the current reference plugin, to consume Kindling Mantle without Hearth-relative imports. |
| **VAL** | Standalone build/test and Hearth-hosted plugin smoke test pass; Kindling changelog/handoff records required downstream edits and fallback. |
