# FR-0004 closeout — Centralized users auth

**Status update 2026-05-26:** This closeout is superseded by the multi-user correction. [**PR #56**](https://github.com/mcelhennyi/hearth/pull/56) remains the feature branch preview, but FR-0004 should not merge to **`main`** until `T-FR-0004-11` through `T-FR-0004-16` land and this closeout is refreshed.

## Executive summary

FR-0004 ships Hearth-owned identity as a built-in `hearth-users` plugin and routes plugin access through the gateway trust contract. Operators log in once, Caddy verifies sessions through hub `/api/auth/verify`, plugins receive signed `X-Hearth-User-*` identity headers, Kindling-generated backends enforce the gateway trust middleware, and Mantle plugin frames receive the same verified user through `hearth.user`.

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

## Validation

- `./develop test` — 277 passed, 3 skipped, 4 warnings.
- `./develop web npm run test` — 4 files passed, 12 tests passed.
- `./develop web npm run build` — passed.
- `./develop web npm run lint` — passed.
- Ticket-level Caddy sidecar probe during T04 returned 401 without session and 200 with signed headers after login.
- Real iPhone PWA login-once walkthrough remains a manual environment exception; automated Mantle contract tests cover login handoff, session fetch, and iframe user payload.

## Deferred / follow-up

| Item | Tracking |
|------|----------|
| Full custom user service / OIDC provider | Future FR; FR-0004 only ships an external verify URL stub. |
| Real-device iPhone login-once walkthrough for the final integrated branch | Manual validation follow-up when the Pi/iPhone environment is available. |
| Refresh closeout with merge SHA | After the feature PR lands on `main`. |

## Suggested next step

Open and review the feature PR to `main`; after merge, refresh this closeout with the merge SHA and remove repo-root `CURRENT.md` from `main`.

## Options

| Option | When |
|--------|------|
| Merge PR | Use when human review accepts the full centralized auth line. |
| Request changes | Use if real-device validation or operator UX wants another pass before `main`. |
| Start FR-0005 | Use after PR review begins; FR-0005 remote-build work is already designed. |

## Audit

- **Merge commit:** *pending*
- **Feature branch:** `feat/FR-0004-centralized-users-auth` @ `d253d00` before PR URL refresh; retained on remote.
- **Feature PR:** [PR #56](https://github.com/mcelhennyi/hearth/pull/56)
- **Handoff:** [`handoffs/2026-05-26-finish-feature.md`](handoffs/2026-05-26-finish-feature.md)
