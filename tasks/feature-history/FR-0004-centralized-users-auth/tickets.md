# Tickets — FR-0004 Centralized users auth

**Feature id:** **`FR-0004`**
**Canonical ids:** **`T-FR-0004-xx`**
**DAG:** [`20-tickets-dag.md`](20-tickets-dag.md)
**Progress tracker:** [`tasks/ticket-progress.md`](../../ticket-progress.md)

---

### T-FR-0004-01 — Design amendments: centralized auth architecture

**Title:** Design amendments: centralized auth architecture
**Deps:** `none`

#### Purpose

Promote FR-0004 design into authoritative `docs/design/`:

- Update [`architecture/overview.md`](../../../docs/design/architecture/overview.md) §8 — built-in plugin, gateway verify, external provider hook.
- Add `builtin` flag to [`plugin-contract.md`](../../../docs/design/plugin-contract.md).
- Update [`deployment.md`](../../../docs/design/deployment.md) — Caddy `auth_request`, public vs protected routes.
- Update [`mantle-ui.md`](../../../docs/design/mantle-ui.md) — login at `/hearth-users/`, trust headers.
- Update [`satellite-repos/kindling.md`](../../../docs/design/satellite-repos/kindling.md) — Kindling changes must carry a dense child-repo compliance changelog entry.
- Document FR-0001 **`T-FR-0001-09`** split (identity → FR-0004; push stays unless Q1 closed).

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Doc review checklist | Peer/agent checklist: every public surface in `10-design-00-skeleton.md` appears in design docs; no contradiction with Spark-only app traffic rule. |
| **DEV** | Amend design docs | Amendment blocks per `docs/ai-context.md` where required. |
| **VAL** | `./develop build` if docs site present; links resolve. | |

---

### T-FR-0004-02 — Built-in hearth-users plugin scaffold

**Title:** Built-in hearth-users plugin scaffold
**Deps:** `T-FR-0004-01`

#### Purpose

Create `apps/builtin/hearth-users/` (platform-plugin layout):

- `tinder.toml` with `builtin = true` (schema addition from T01).
- FastAPI `create_app` stub, static Vite UI placeholder.
- Hub install path registers plugin as built-in on first boot without treating it as a normal external `apps/<slug>/` plugin.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Manifest validates | `kindling validate` or hub tinder tests pass; builtin cannot be uninstalled via API. |
| **DEV** | Scaffold | Plugin serves `GET /health`; UI shows placeholder login; platform path is documented as the sole exception to plugin agnosticism. |
| **VAL** | Enabled in dev Compose; reachable at `/hearth-users/`. | |

---

### T-FR-0004-03 — Users plugin: password, session, verify API

**Title:** Users plugin: password, session, verify API
**Deps:** `T-FR-0004-02`

#### Purpose

Implement identity per [`10-design-01-gateway-and-trust.md`](10-design-01-gateway-and-trust.md):

- Argon2id password storage; first-run set password.
- Session cookie; `POST /login`, `POST /logout`, `GET /api/session`.
- `GET /api/verify` returns 200/401 claims for edge auth; hub alias normalizes those claims into signed upstream headers.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Plugin pytest | Bad password, lockout, session expiry, verify 200/401 vectors. |
| **DEV** | Implement | SQLite under `var/hearth/plugins/hearth-users/`. |
| **VAL** | Manual login sets cookie; verify returns 200 when session present. | |

---

### T-FR-0004-04 — Hub auth verify alias and provider settings

**Title:** Hub auth verify alias and provider settings
**Deps:** `T-FR-0004-03`

#### Purpose

- `GET /api/auth/verify` — delegates to active provider (builtin plugin loopback or external URL).
- Settings model `auth.provider`, `auth.external_verify_url`.
- Generate `HEARTH_USER_SIG_SECRET`, sign `X-Hearth-User-*` headers with timestamp freshness, and distribute the secret to plugins at supervisor start.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Hub API tests | Builtin forward; external mock server; misconfig → 503; signed headers include `X-Hearth-User-Ts`. |
| **DEV** | Implement | Settings CRUD; secret generation on install. |
| **VAL** | Verify endpoint callable from Caddy sidecar in Compose. | |

---

### T-FR-0004-05 — Caddy auth_request and header injection

**Title:** Caddy auth_request and header injection
**Deps:** `T-FR-0004-04`

#### Purpose

Extend proxy fragment generator:

- `auth_request /api/auth/verify` (or internal URI) on plugin routes.
- Strip inbound browser-supplied `X-Hearth-*` headers, then inject only hub-verified `X-Hearth-User-Id`, `X-Hearth-User-Ts`, `X-Hearth-User-Sig`, optional name/roles on success.
- 302 to `/hearth-users/login?next=` for HTML; 401 JSON for APIs.

**Note:** Requires existing Caddy generation from FR-0001/FR-0003; coordinate in VAL diary if stubbed.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Golden Caddyfile fragments | Unauthed → redirect; authed → upstream with headers. |
| **DEV** | Renderer + reload hook | Integration curl through Caddy. |
| **VAL** | Plugin route without cookie redirects to login. | |

---

### T-FR-0004-06 — Spark session capabilities and builtin registry rules

**Title:** Spark session capabilities and builtin registry rules
**Deps:** `T-FR-0004-03`

#### Purpose

- Spark methods: `session.current`, events `login`/`logout`.
- Registry: `builtin` plugins skip uninstall; disable policy when external provider active.
- Hub may call `hearth-users` for dashboard “who am I”.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Spark tests | Permission boundaries; builtin uninstall rejected. |
| **DEV** | Implement | Audit log entries for auth events. |
| **VAL** | `spark.call("hearth-users", "session.current")` from hub works. | |

---

### T-FR-0004-07 — Kindling template: trust middleware and no local login

**Title:** Kindling template: trust middleware and no local login
**Deps:** `T-FR-0004-01`, `T-FR-0004-04`

#### Purpose

Update Kindling `templates/plugin-python/` (and TS if present):

- `require_hearth_user()` dependency / middleware.
- README section “Authentication”.
- Dense child-repo compliance changelog entry for this Kindling contract change.
- Remove default login components from template.
- `kindling new` smoke test uses headers in pytest.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Template test | Generated plugin rejects missing headers on protected route. |
| **DEV** | Template + docs | Published in Kindling repo or vendor path per FR-0001-07 policy; updates the compliance changelog so existing plugins can be brought forward. |
| **VAL** | `kindling new test-auth` installs and documents trust model. | |

---

### T-FR-0004-08 — Mantle shell: login via hearth-users and useUser contract

**Title:** Mantle shell: login via hearth-users and useUser contract
**Deps:** `T-FR-0004-03`, `T-FR-0004-05`

#### Purpose

- Shell fetches session from `/hearth-users/api/session` or hub BFF.
- `useUser()` + `hearth.user` postMessage match verified claims.
- No duplicate login form in hub web app.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Vitest | Mock session; postMessage payload shape. |
| **DEV** | Implement in hub web / Mantle | Login link targets `/hearth-users/login`. |
| **VAL** | iPhone PWA: login once, plugin iframe receives user. | |

---

### T-FR-0004-09 — External auth provider stub and operator settings UI

**Title:** External auth provider stub and operator settings UI
**Deps:** `T-FR-0004-04`

#### Purpose

- Settings UI: builtin vs external verify URL.
- Hub forwards verify to external; maps response to same header contract.
- Fail closed if external unreachable.
- Document “custom user service” follow-up FR (no full OIDC in this ticket).

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Contract tests | Mock external verify 200/401; builtin disabled → 503. |
| **DEV** | Settings UI + hub logic | |
| **VAL** | Toggle recorded; verify uses external URL in integration test. | |

---

### T-FR-0004-10 — E2E: plugin trusts gateway identity

**Title:** E2E: plugin trusts gateway identity
**Deps:** `T-FR-0004-05`, `T-FR-0004-07`, `T-FR-0004-08`

#### Purpose

Capstone: minimal fixture plugin (`auth-fixture` or extend groceries-stub):

- Protected API returns 401 without gateway headers in unit test; 200 through Caddy with session.
- Playwright: unauthenticated visit → login → plugin shows user name from `useUser()`.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | E2E suite | Automated in CI Compose profile. |
| **DEV** | Fixture + tests | |
| **VAL** | Documented walkthrough in `serial-diary.md`. | |

---

### T-FR-0004-11 — Multi-user design amendment and migration plan

**Title:** Multi-user design amendment and migration plan
**Deps:** `T-FR-0004-10`

#### Purpose

Amend FR-0004 from single local account to multi-user local identity:

- Promote the multi-user model into FR-0004 design docs and authoritative `docs/design/` notes where they still say "single local user".
- Define `users` schema fields: stable opaque id, unique normalized username, display name, roles, disabled flag, password hash, timestamps.
- Define migration from the landed single `local` account into the first admin user.
- Define first-run semantics: first account is `admin,user`; later accounts default to `user`.
- Define admin safety rules: final enabled admin cannot be disabled or demoted.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Design checklist | Every existing single-user statement is classified as updated, intentionally deferred, or ticketed. |
| **DEV** | Amend docs | FR docs, design docs, and ticket DAG reflect multi-user behavior and migration. |
| **VAL** | Frontier-ready | `tickets.md`, `20-tickets-dag.md`, and `tasks/ticket-progress.md` expose follow-on tickets for `/develop-frontier`. |

---

### T-FR-0004-12 — Users plugin: multi-user schema, migration, and auth API

**Title:** Users plugin: multi-user schema, migration, and auth API
**Deps:** `T-FR-0004-11`

#### Purpose

Replace the single `local` account with a multi-user account model in `hearth-users`:

- SQLite migration from the existing single-user table/session data.
- `POST /api/setup` creates the first admin account with username, display name, and password.
- `POST /login` requires username + password and creates a session for that user id.
- Sessions, `/api/session`, `/api/verify`, and audit records return the stored user id/display name/roles.
- Disabled users cannot log in; existing sessions for disabled users fail verify.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Plugin pytest | Migration, username uniqueness, first admin setup, multi-user login, disabled-user verify, and lockout vectors fail before implementation. |
| **DEV** | Implement schema/API | Backward-compatible migration; no password-only login remains. |
| **VAL** | Focused auth tests | `./develop test tests/builtin/test_hearth_users.py` passes with multi-user coverage. |

---

### T-FR-0004-13 — Hearth Users UI: first admin setup and username login

**Title:** Hearth Users UI: first admin setup and username login
**Deps:** `T-FR-0004-12`

#### Purpose

Make the built-in provider UI match multi-user behavior:

- First-run setup asks for username, display name, and password.
- Existing installs show username + password login.
- The page remains self-contained and Mantle-aligned when served through `/hearth-users/`.
- `next` redirect remains local-only and works after setup/login.
- Clear errors for duplicate usernames, disabled accounts, wrong password, and lockout.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | HTML/API tests | Served login HTML contains username fields in the correct modes and posts the expected JSON shape. |
| **DEV** | Implement provider UI | No inert placeholder; no password-only form. |
| **VAL** | Browser/manual | Pi/local browser: create first admin, log out, log in with username, redirect back to Hearth. |

---

### T-FR-0004-14 — Session, Spark, gateway, and Mantle claims use real users

**Title:** Session, Spark, gateway, and Mantle claims use real users
**Deps:** `T-FR-0004-12`

#### Purpose

Carry multi-user claims through every existing FR-0004 contract:

- Hub `/api/auth/verify` signs the actual user id, display name, and roles from `hearth-users`.
- Caddy continues stripping inbound `X-Hearth-*` and forwarding only hub-signed claims.
- Spark `hearth-users.session.current`, audit events, and login/logout topics include the actual user id.
- Mantle `useUser()` and `hearth.user` postMessage receive the same user id/display name/roles.
- Kindling trust helpers continue validating signatures without assuming `local`.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Cross-contract tests | Hub verify, Spark, Mantle, and Kindling tests prove two different users produce different claims. |
| **DEV** | Update claim plumbing | Remove hardcoded `local`/`Local user` assumptions from runtime paths. |
| **VAL** | Focused combined validation | Auth, Spark, gateway, and web tests pass in Docker wrappers. |

---

### T-FR-0004-15 — Admin user management API and settings UI

**Title:** Admin user management API and settings UI
**Deps:** `T-FR-0004-12`, `T-FR-0004-14`

#### Purpose

Give the first admin a safe way to manage additional local users:

- Admin-only APIs: list users, create user, update display name, reset password, disable/enable user, update roles.
- Settings UI under Hearth account/auth surfaces those APIs without exposing password hashes.
- Enforce final-admin safety: cannot disable or demote the last enabled admin.
- Write audit events for create/update/disable/reset operations.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | API/web tests | Non-admins are denied; admins can create and disable users; final-admin safety is enforced. |
| **DEV** | API + UI | Settings page manages users; no direct DB editing required for normal operation. |
| **VAL** | Manual flow | Create second user, log in as second user, verify admin-only controls are hidden/denied. |

---

### T-FR-0004-16 — Multi-user E2E and compliance changelog refresh

**Title:** Multi-user E2E and compliance changelog refresh
**Deps:** `T-FR-0004-13`, `T-FR-0004-14`, `T-FR-0004-15`

#### Purpose

Close the multi-user extension with end-to-end proof and child-repo guidance:

- E2E: create first admin, create second user, log in as each, and verify a protected plugin sees the correct user.
- Update Kindling dense compliance changelog with multi-user drift detection and required child repo changes.
- Update FR-0004 closeout/handoffs so PR #56 is no longer described as complete until the multi-user wave lands.
- Refresh Pi operator instructions for first-admin setup and adding later users.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | E2E + compliance checks | Fixture plugin proves user switching; Kindling changelog contains AI-readable migration instructions. |
| **DEV** | Polish docs/tests | Closeout and operator docs reflect multi-user reality. |
| **VAL** | Full validation | `./develop test`, web test/lint/build, and install smoke pass; Pi walkthrough recorded if available. |

---

## Acceptance for FR-0004 closeout

- Operator creates the first admin account at `/hearth-users/login`, can add at least one additional local user, and each user can log in without per-plugin login UI.
- Plugin routes receive the correct signed identity for the active user, including stable user id, display name, and roles.
- Admin user management prevents disabling or demoting the final enabled admin.
- Kindling-generated plugin documents and enforces trust middleware.
- Settings can point verify at an external URL (stub); builtin can be disabled only with valid external config.
- Design docs and FR-0001-09 scope are aligned via amendment.
