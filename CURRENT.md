# CURRENT — T-FR-0006-04 user preferences

**Branch:** `feat/FR-0006-design-language-T-FR-0006-04-user-preferences`  
**Worktree:** `.worktrees/FR-0006-design-language/T-FR-0006-04-user-preferences/`  
**Feature:** FR-0006 design-language

## T-FR-0006-04 complete (TEST / DEV / VAL)

- **API:** `GET/PUT /api/user/preferences` (`theme`: light | dark | system); Alembic `0004_user_preferences`.
- **Web:** `ThemeProvider` (localStorage boot + server reconcile + `hearth.theme` broadcast); `SettingsModal` (dialog; tabs Theme / Plugins / System tiles / Diagnostics / Sign out); Settings triggers in shell chrome.
- **Tests:** 5 pytest (`tests/api/test_user_preferences.py`); Vitest ThemeProvider + SettingsModal (+ App nav count updates); 28 web tests green in Docker.

## Next step

Open PR to `feat/FR-0006-design-language`; after merge, continue W1 frontier (05, 06, 07, …).
