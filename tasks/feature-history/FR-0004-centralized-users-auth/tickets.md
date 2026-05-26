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

## Acceptance for FR-0004 closeout

- Operator logs in once at `/hearth-users/login`; all plugin routes work without per-plugin login UI.
- Kindling-generated plugin documents and enforces trust middleware.
- Settings can point verify at an external URL (stub); builtin can be disabled only with valid external config.
- Design docs and FR-0001-09 scope are aligned via amendment.
