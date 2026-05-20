# Current branch state

**Branch:** `feat/FR-0001-hearth-platform`
**Status:** T03 + T06 + T09 merged; 181 tests passing; next wave T05/T07

## What was done (this integration)

- Merged T-FR-0001-03 (Tinder loader): Pydantic schema + loader + 17 tests
- Merged T-FR-0001-06 (Spark v1): broker, Python client, TS stub + 23 tests
- Merged T-FR-0001-09 (Auth/Push): argon2id auth, itsdangerous sessions,
  Web Push VAPID, ntfy notify handler + 37 tests
- Revalidated: 181 tests pass via `docker compose hearth-test`
- Updated `docs/design/tickets-initial.md` triadDone for T01–T04, T06, T09

## Next step

Run `/identify-frontier` — eligible next wave:
- **T-FR-0001-05** (Caddy generation + local TLS): unblocked by T-FR-0001-03 VAL
- **T-FR-0001-07** (Kindling repo and CLI): unblocked by T-FR-0001-03 + T-FR-0001-06 VAL

T-FR-0001-08 (groceries reference plugin) blocked by T07.
T-FR-0001-10 (Pi/Mac install + backup) blocked by T09.
