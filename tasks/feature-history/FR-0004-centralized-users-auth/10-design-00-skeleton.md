# FR-0004 — Design (level 0, skeleton)

## Purpose

Hearth is the **only public HTTPS origin** for the home LAN. Caddy terminates TLS and reverse-proxies to the hub (`/`, `/api/*`) and to each enabled plugin (`/<slug>/*`). **Authentication is enforced at the edge** via an `auth_request`-style subrequest; the **built-in `hearth-users` plugin** owns credentials, sessions, and verification. Other plugins **trust** identity injected by the proxy/hub and must not implement standalone login in the default Kindling template.

## Actors

| Actor | Role |
|-------|------|
| **Browser / PWA** | User; holds session cookie scoped to Hearth origin |
| **Caddy (edge)** | TLS, routing, `auth_request` to verify endpoint |
| **Hub API** | Registry, settings, orchestrates verify + header injection policy, marks built-in plugins |
| **`hearth-users` plugin** | Login UI, password hash, session CRUD, `/verify` for edge |
| **Other plugins** | Consume `X-Hearth-*` headers (backend) and `hearth.user` (frontend via Mantle) |
| **Kindling CLI** | Scaffolds plugins with trust middleware + docs |
| **Operator** | Enables/disables built-in users provider; future: points verify URL at external service |

## Public surfaces (skeleton)

| Surface | Kind | Contract (sketch) | Owner |
|---------|------|-------------------|--------|
| `GET/POST /hearth-users/login` | HTTP (plugin UI) | Login form; `POST` sets session cookie | `hearth-users` |
| `POST /hearth-users/logout` | HTTP | Clears session | `hearth-users` |
| `GET /hearth-users/api/session` | HTTP JSON | `{user_id, display_name, roles[]}` or `401` | `hearth-users` |
| `GET /hearth-users/api/verify` | HTTP | **200** + minimal body if session valid; **401** otherwise (Caddy `auth_request` target) | `hearth-users` |
| `GET /api/auth/verify` | HTTP (hub) | **Stable edge alias** — hub forwards to active auth provider (built-in or external URL from settings) | Hub |
| `PUT /api/settings/auth` | HTTP JSON | `{provider: "builtin"\|"external", external_verify_url?: url}` — **external** adapter stub in this FR | Hub |
| Request headers (to plugins) | HTTP | `X-Hearth-User-Id`, `X-Hearth-User-Ts`, `X-Hearth-User-Sig` (HMAC), optional `X-Hearth-Roles` | Hub verify returns signed headers; Caddy strips spoofed inbound headers and copies only verified response headers upstream |
| `hearth.user` postMessage | Shell ↔ iframe | `{id, name, roles}` per [`mantle-ui.md`](../../../docs/design/mantle-ui.md) | Mantle |
| `spark.call("hearth-users", …)` | Spark | `session.current`, `password.set` (admin), `provider.status` | `hearth-users` |
| Kindling `trust_hearth_user` middleware | Python/TS | Validates signature + populates request user; **fails closed** if headers missing on protected routes | Kindling template |

## Data in / out

| Input | Output | Storage |
|-------|--------|---------|
| Local username + password (setup / change) | Session cookie (`HttpOnly`, `Secure`, `SameSite=Lax`) | `var/hearth/plugins/hearth-users/` (plugin-owned SQLite) |
| Session id (cookie) | Verified user claims | Session table in plugin DB |
| Registry: built-in flag | Plugin cannot be uninstalled; disable = stop routing UI only if policy says so | `var/hearth/hearth.db` (hub) |

## Boundaries

```mermaid
graph TB
  Browser --> Caddy
  Caddy -->|"/hearth-users/*"| UsersPlugin[hearth-users plugin]
  Caddy -->|auth_request| HubVerify["/api/auth/verify"]
  HubVerify --> UsersPlugin
  Caddy -->|"/<slug>/*" + headers| PluginN[Other plugins]
  Browser --> Mantle[Mantle shell]
  Mantle -->|iframe| PluginN
```

- Plugins **must not** call each other’s login routes over HTTP (Spark-only for app-to-app).
- **Disable built-in users:** settings switch `provider=external` + `external_verify_url`; hub verify forwards there; same header injection contract. Full custom UI plugin is **follow-up FR**.
- **Built-in plugin exception:** `hearth-users` is a platform-owned plugin bundled with Hearth. It is not a regular first-party app and must live under a platform namespace such as `apps/builtin/hearth-users/`, not `apps/<slug>/`; external/plugin-author code still follows the no-bundled-plugins rule.

## Open questions

| ID | Question | Tag |
|----|----------|-----|
| Q1 | Does Web Push / VAPID stay in hub (`T-FR-0001-09`) or move under `hearth-users`? | Closed for FR-0004 MVP: push stays hub-owned; users plugin owns identity only. |
| Q2 | Cookie name and path: site-wide `/` vs `/hearth-users/` only? | Closed for FR-0004 MVP: `hearth_session`, `Path=/`, `HttpOnly`, `Secure`, `SameSite=Lax`. |
| Q3 | Signature algorithm and key rotation for `X-Hearth-User-Sig` | Closed for MVP in L1: HMAC-SHA256 with timestamp freshness; rotation deferred. |
| Q4 | Minimum roles model for plugins (empty vs `["user"]`) | MVP: first account gets `admin,user`; additional accounts default to `user`; roles are delivered in `X-Hearth-Roles` and `useUser()`. |
| Q5 | Is FR-0004 single-user or multi-user? | Revised 2026-05-26: **multi-user**. The first landed slice is insufficient; tickets `T-FR-0004-11`…`T-FR-0004-16` extend the branch before closeout. |
