# Current branch state

**Branch:** `feat/FR-0001-hearth-platform-T-FR-0001-05-caddy-gen`
**Status:** T-FR-0001-05 done; PR open → merge into `feat/FR-0001-hearth-platform`

## What was done (T-FR-0001-05)

- Added `apps/hub/api/proxy/caddy.py`: `render_fragment()` pure renderer,
  `write_fragment()`, `reload_caddy()` (admin API + subprocess fallback),
  `regenerate_and_reload()` async hook for plugin routes
- Added `deploy/caddy/Caddyfile.template`: base config with fragment `import`
- Hooked `regenerate_and_reload` into all four plugin state-changing routes
  (install / enable / disable / uninstall)
- 8 new unit tests in `tests/proxy/test_caddy.py`; 1 integration test skipped
- 189 tests pass, lint clean

## Next step

Merge this PR into `feat/FR-0001-hearth-platform`, then run `/identify-frontier`
for the next eligible tickets:
- **T-FR-0001-07** (Kindling repo and CLI)
- **T-FR-0001-08** (groceries reference plugin — blocked by T07)
- **T-FR-0001-10** (Pi/Mac install + backup)
