# Current branch state

Feature: FR-0004 centralized users auth
Ticket: T-FR-0004-04 - Hub auth verify alias and provider settings
Branch: feat/FR-0004-centralized-users-auth-T-FR-0004-04-auth-verify-provider
Worktree: .worktrees/FR-0004-centralized-users-auth/T-FR-0004-04-auth-verify-provider/

## Status

Phase: VAL complete

Merged latest `feat/FR-0004-centralized-users-auth` into this ticket branch after
T-FR-0004-06 landed locally. T06's Spark `session.current`, auth/session audit,
builtin disable rejection, and Tinder session capability/event changes are
preserved. T04's hub verify alias/provider settings work is reapplied on top.

TEST complete. Added red hub API coverage for auth provider settings,
`GET /api/auth/verify`, provider 401 handling, external misconfig, provider
unreachable errors, external mock provider forwarding, and signed
`X-Hearth-User-*` headers.

Targeted red command:

```bash
./develop test tests/api/test_auth_verify_alias.py tests/api/test_settings.py
```

Result: failed during collection because `app.auth_verify` was not implemented.

DEV complete. Implemented:

- Nested auth settings backed by existing `settings` rows: `auth.provider` and
  `auth.external_verify_url`.
- `GET /api/auth/verify` on the hub, delegating to the built-in provider URL or
  configured external URL.
- Fail-closed provider behavior for misconfig, unavailable provider, and invalid
  provider output.
- Persisted `HEARTH_USER_SIG_SECRET` generation and normalized signed
  `X-Hearth-User-*` response headers.
- Plugin Compose generation injects the persisted user signing secret into
  plugin environments at supervisor start.
- Dev Compose `hearth-users` installs `argon2-cffi` so the built-in provider can
  boot for sidecar validation.

Latest green commands:

```bash
./develop test tests/api/test_auth_verify_alias.py tests/api/test_settings.py tests/test_plugin_compose_generation.py
./develop test
docker compose -f deploy/compose/docker-compose.yml exec -T caddy wget -S -O - http://hub:8200/api/auth/verify
```

Results:

- Focused merged slice: 75 passed.
- Full tests after merging T06: 266 passed, 3 skipped.
- Caddy sidecar probe after Compose dependency fix reached hub `/api/auth/verify`
  and failed closed with HTTP 401 without a session.
- Authenticated Caddy sidecar probe returned HTTP 200 with signed
  `X-Hearth-User-*` headers.

## Next

Commit, push, and open a ticket PR against `feat/FR-0004-centralized-users-auth`.
