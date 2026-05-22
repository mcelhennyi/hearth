# CURRENT — feat/FR-0006-design-language-T-FR-0006-15-mantle-publish

**Branch:** `feat/FR-0006-design-language-T-FR-0006-15-mantle-publish`  
**Worktree:** `.worktrees/FR-0006-design-language/T-FR-0006-15-mantle-publish/`  
**Feature:** FR-0006 design-language  
**Ticket:** T-FR-0006-15 — `@kindling/mantle` publish

## Status

TEST / DEV / VAL **done** (2026-05-21).

## Delivered

| Phase | Acceptance |
|-------|------------|
| **TEST** | `src/publish.test.ts` runs `npm publish --dry-run`; CI workflow `.github/workflows/kindling-mantle-ci.yml` runs test + dry-run on PR/push. |
| **DEV** | Publish workflow on tag `kindling-mantle-v*`, `CHANGELOG.md` v0.1.0, README install + React example + Kindling `plugin-ui-system.md` link, `publish:dry-run` / `prepublishOnly` scripts. |
| **VAL** | README documents tag-driven publish and `NPM_TOKEN` requirement; dry-run validated locally via `./develop web`. |

## Blockers (operator)

- **`NPM_TOKEN`** GitHub secret must be set with npm publish access to `@kindling` before the first tag push publishes `@kindling/mantle@0.1.0`.
- Confirm `@kindling` npm org exists and the hearth bot/user is a member with publish rights.

## Next step

Open PR into `feat/FR-0006-design-language`. After merge, tag `kindling-mantle-v0.1.0` to publish. Then run **`/finish-feature`** if FR-0006 §2d gate is satisfied (all 15 tickets VAL-done).
