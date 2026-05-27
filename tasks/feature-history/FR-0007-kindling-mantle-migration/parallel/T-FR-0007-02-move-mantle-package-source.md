# T-FR-0007-02 - Move Mantle package source to Kindling

## 2026-05-27 - Ticket completion

**Branch:** `feat/FR-0007-kindling-mantle-migration-T-FR-0007-02-move-mantle-package-source`

**Kindling branch:** `feat/FR-0007-mantle-package-source` @ `da8eaab`

**Recap:** Moved `@kindling/mantle` source, tests, README, changelog, package metadata, and build config from Hearth `packages/mantle/` into the Kindling submodule at `kindling/mantle/`. Updated Kindling docs and changelog to state that Mantle now lives in Kindling, and removed the Hearth-local package source tree so it is no longer treated as authoritative.

**Validation:** Initial host-local validation was discarded after user correction. Revalidated inside the Docker web tooling container: cleaned generated artifacts, ran `npm install --no-package-lock`, enabled pnpm via Corepack, ran `NPM_CONFIG_CACHE=.npm-cache npm run test` (37 tests passed), and ran `NPM_CONFIG_CACHE=.npm-cache npm run pack:dry-run` (tarball dry-run succeeded). `git diff --check` passed in the parent worktree.

**Next:** Merge this ticket branch into `feat/FR-0007-kindling-mantle-migration`, then rerun `/identify-frontier`. Expected next eligible tickets are `T-FR-0007-03` and `T-FR-0007-04`.
