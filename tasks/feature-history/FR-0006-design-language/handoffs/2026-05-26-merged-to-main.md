# FR-0006 merged-to-main handoff

**Date:** 2026-05-26
**Merge:** [PR #46](https://github.com/mcelhennyi/hearth/pull/46) -> `main` @ `25e3381`
**Feature branch:** `feat/FR-0006-design-language` @ `121706e`

## Executive summary

FR-0006 is merged to `main`. The post-merge hygiene removes repo-root `CURRENT.md`, refreshes closeout references from PR-pending to merged, and keeps the feature branch retained on the remote for audit.

## Validation

| Suite | Result |
|-------|--------|
| `./develop test` | 287 passed, 3 skipped |
| `kindling-mantle CI` | passed on pushed conflict-fix head |
| `hearth-install-smoke` | passed on PR #46 |

## Suggested next step

Configure **`NPM_TOKEN`**, push tag **`kindling-mantle-v0.1.0`**, then staff the partner Mantle adoption work in kindling and grocery-list.

## Options

| Option | When |
|--------|------|
| Publish `@kindling/mantle` | Once npm credentials are ready |
| Staff grocery FR-0002 | To consume the merged Mantle design language |
| Resume FR-0004 or FR-0005 | If platform auth or remote-build deployment is the next priority |
