# FR-0007 - Migration plan

## Target ownership

Kindling owns Mantle source and publishes or exposes `@kindling/mantle`. Hearth is the canonical host, but it is not the canonical package source. Plugin repos do not import from Hearth paths and do not vendor Mantle source.

## Transition contract checklist

T-FR-0007-01 uses this checklist as the doc-oriented TEST gate: before package files move, each item must be stated in the Kindling satellite design or this FR plan.

- [x] Kindling owns `@kindling/mantle` source, tests, changelog, package metadata, and release path.
- [x] Hearth local development consumes Mantle through the Kindling submodule/workspace, while CI/production uses a pinned package version or immutable tag.
- [x] Plugin/app repos depend on `@kindling/mantle` and never import Hearth-relative Mantle paths.
- [x] Plugin compatibility is declared as a supported Kindling/Mantle version range accepted by the target Hearth host.
- [x] `packages/mantle/` is explicitly transitional: it is the FR-0006 private package source for migration/rollback only, not the authoritative package home after FR-0007.

## Compatibility model

- Hearth declares the accepted `@kindling/mantle` major range for plugins.
- Kindling templates pin a compatible major by default.
- Standalone plugin development uses the same package surface as Hearth-hosted plugin mode.
- Breaking Mantle changes require a Kindling changelog entry that gives downstream agents enough detail to migrate apps without re-auditing the upstream diff.

## Sequence

1. Update the Kindling satellite design and ticket graph so the transition from FR-0006 private Hearth package to Kindling-owned package is explicit.
2. Move package source, tests, package metadata, and changelog from Hearth `packages/mantle/` into Kindling `mantle/` or the equivalent package workspace.
3. Rewire Hearth local development to consume Kindling Mantle through the submodule/workspace alias, with CI/production using a pinned package or tagged source.
4. Update Kindling templates so generated apps install `@kindling/mantle`, import token CSS, run standalone Vite/dev server flows, and keep plugin-mode iframe compliance.
5. Add validation that catches unsupported Mantle/Kindling versions before a plugin is installed or released.
6. Prove the path with one existing standalone app/plugin repository and record migration instructions for downstream projects.

## Rollback

If the Kindling package move blocks Hearth builds, keep the FR-0006 `packages/mantle/` tree as a temporary source mirror for one release while Hearth consumes a git/tagged Kindling package in CI. The rollback must remain explicit and short-lived: new plugin templates still point at `@kindling/mantle`, not Hearth-relative source.

## Non-goals

- No new host runtime in Kindling.
- No per-plugin copy of Mantle components.
- No fake Mantle shim for standalone development.
