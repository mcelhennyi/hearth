# Current branch state

**Branch:** `feat/FR-0001-hearth-platform`
**Status:** All 10 T-FR-0001-xx tickets done — feature-complete gate met

## Merged

- T-FR-0001-01: repo scaffold + Compose dev loop
- T-FR-0001-02: Hub API skeleton + SQLite registry
- T-FR-0001-03: Tinder loader and manifest schema
- T-FR-0001-04: Mantle PWA shell + iframe embed
- T-FR-0001-05: Caddy fragment gen + reload hook
- T-FR-0001-06: Spark v1 broker + client libs
- T-FR-0001-07: Kindling repo + CLI
- T-FR-0001-08: groceries reference plugin (submodule apps/groceries/, 210 tests)
- T-FR-0001-09: Auth, VAPID, Web Push + ntfy
- T-FR-0001-10: bare-metal install.sh, systemd/launchd units, hearth backup/restore (235 tests)

## Test count

235 passed, 3 skipped (all HEARTH_INTEGRATION=1 gated)

## Next step

**`/finish-feature`** — open PR `feat/FR-0001-hearth-platform` → `main`.
Write `tasks/feature-history/FR-0001-hearth-platform/90-closeout.md`.
Update REGISTRY.md FR-0001 → `done`.
Remove CURRENT.md when PR merges to main.

## Manual VAL deferred (not blocking gate — same as T05/T09 pattern)

- T05: iPhone device PWA walkthrough (certificate trust + home screen)
- T08: iPhone PWA walkthrough for groceries plugin
- T09: real Web Push notification on iPhone
