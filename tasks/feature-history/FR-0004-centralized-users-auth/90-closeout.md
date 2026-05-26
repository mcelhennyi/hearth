# FR-0004 closeout — Centralized users auth

**Status update 2026-05-26:** This closeout remains a draft until the
multi-user correction is integrated. [**PR #56**](https://github.com/mcelhennyi/hearth/pull/56)
is a feature-branch preview only; FR-0004 should not merge to **`main`** until
`T-FR-0004-11` through `T-FR-0004-16` are merged to
`feat/FR-0004-centralized-users-auth`, full feature validation passes, and the
parent orchestrator reruns `finish-feature`.

## Executive summary

FR-0004 ships Hearth-owned multi-user identity as a built-in `hearth-users`
plugin and routes plugin access through the gateway trust contract. Operators
create the first admin, add later users in Settings, Caddy verifies sessions
through hub `/api/auth/verify`, plugins receive signed `X-Hearth-User-*`
identity headers, Kindling-generated backends enforce the gateway trust
middleware, and Mantle plugin frames receive the same verified user through
`hearth.user`.

## Delivered surfaces

| Surface | Location |
|---------|----------|
| Built-in users plugin | `apps/builtin/hearth-users/` |
| Hub auth verify and provider settings | `apps/hub/api/app/routes/auth.py`, `apps/hub/api/app/auth_verify.py`, `apps/hub/api/app/routes/settings.py` |
| Gateway auth routes | `apps/hub/api/proxy/caddy.py`, `deploy/hearth-install/hearth_install/plugin_compose.py` |
| Mantle session/login/user bridge | `apps/hub/web/src/App.tsx`, `apps/hub/web/src/mantle/PluginFrame.tsx`, `kindling/mantle/useUser.ts` |
| Kindling trust template | `deploy/kindling-contract/hearth_kindling_contract/templates/plugin-python/` |
| Downstream compliance notes | `deploy/kindling-contract/COMPLIANCE_CHANGELOG.md`, `.skeleton/docs/ai-context.md` |
| Optional local-account bootstrap | `var/hearth/secrets/hearth-users-default-password` or `$HEARTH_USERS_BOOTSTRAP_PASSWORD_FILE` |

## Tickets

| Ticket | Summary | Status |
|--------|---------|--------|
| `T-FR-0004-01` | Design amendments and audit alignment | TEST / DEV / VAL **done** |
| `T-FR-0004-02` | Built-in `hearth-users` scaffold | TEST / DEV / VAL **done** |
| `T-FR-0004-03` | Password setup, session, verify API | TEST / DEV / VAL **done** |
| `T-FR-0004-04` | Hub verify alias and provider settings base | TEST / DEV / VAL **done** |
| `T-FR-0004-05` | Caddy auth gate and header injection | TEST / DEV / VAL **done** |
| `T-FR-0004-06` | Spark session capabilities and built-in registry rules | TEST / DEV / VAL **done** |
| `T-FR-0004-07` | Kindling trust middleware template and compliance changelog | TEST / DEV / VAL **done** |
| `T-FR-0004-08` | Mantle login handoff and `hearth.user` bridge | TEST / DEV / VAL **done** |
| `T-FR-0004-09` | External auth provider stub and settings UI | TEST / DEV / VAL **done** |
| `T-FR-0004-10` | Gateway identity capstone contract | TEST / DEV / VAL **done** |
| `T-FR-0004-11` | Multi-user design amendment and migration plan | TEST / DEV / VAL **done** |
| `T-FR-0004-12` | Multi-user schema, migration, and auth API | TEST / DEV / VAL **done** |
| `T-FR-0004-13` | First-admin setup and username login UI | TEST / DEV / VAL **done** |
| `T-FR-0004-14` | Real-user claims through session, Spark, gateway, and Mantle | TEST / DEV / VAL **done** |
| `T-FR-0004-15` | Admin user management API and settings UI | TEST / DEV / VAL **done** |
| `T-FR-0004-16` | Multi-user E2E and compliance changelog refresh | TEST / DEV / VAL **done** in ticket branch; merge and parent validation pending |

## Validation

- Latest integrated feature validation before T16: `./develop test` — 349
  passed, 3 skipped, 8 warnings; web test/build passed; targeted Settings lint
  passed. Full web lint remains blocked by pre-existing non-FR-0004 lint debt
  recorded in `tasks/ticket-progress.md`.
- T16 ticket-branch validation: `./develop test` — 351 passed, 3 skipped, 10
  warnings; `./develop web npm run test` — 15 files / 66 tests passed;
  `./develop web npm run build` — passed; install-layout smoke passed.
- T16 adds a stitched multi-user E2E proof: first admin setup, second user
  creation, login as each user, hub verify/signing, and a generated Kindling
  protected route seeing the active user's id, display name, and roles.
- Real Pi/iPhone walkthrough remains a manual environment exception until the
  parent finish-feature run has a Pi target available; automated coverage now
  covers login handoff, session fetch, iframe user payload, and protected plugin
  user switching.

## Deferred / follow-up

| Item | Tracking |
|------|----------|
| Full custom user service / OIDC provider | Future FR; FR-0004 only ships an external verify URL stub. |
| Real-device iPhone login-once walkthrough for the final integrated branch | Manual validation follow-up when the Pi/iPhone environment is available. |
| Refresh closeout with merge SHA | After the feature PR lands on `main`. |

## Suggested next step

Merge `T-FR-0004-16` into `feat/FR-0004-centralized-users-auth`, run full
feature validation, then rerun `finish-feature` only if every FR-0004 ticket row
is TEST / DEV / VAL **done**.

## Options

| Option | When |
|--------|------|
| Hold PR #56 | Use until the multi-user T16 branch is merged and feature validation passes. |
| Request changes | Use if real-device validation or operator UX wants another pass before `main`. |
| Start FR-0005 | Use after PR review begins; FR-0005 remote-build work is already designed. |

## Audit

- **Merge commit:** *pending*
- **Feature branch:** `feat/FR-0004-centralized-users-auth` @ `d253d00` before PR URL refresh; retained on remote.
- **Feature PR:** [PR #56](https://github.com/mcelhennyi/hearth/pull/56)
- **Handoff:** [`handoffs/2026-05-26-finish-feature.md`](handoffs/2026-05-26-finish-feature.md)
