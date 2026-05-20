# FR-0001 — open questions

Live log. Move resolved entries into `serial-diary.md` once the resolution lands in code or in `docs/design/...`.

| ID | Question | Default for MVP | Status |
|----|----------|-----------------|--------|
| Q1 | Plugin embed strategy: iframe vs module federation | **iframe** for MVP; federation Phase 3 | resolved-for-MVP |
| Q2 | Spark transport: Unix sockets vs HTTP-on-loopback | **Unix sockets** | resolved-for-MVP |
| Q3 | Plugin distribution: git submodule vs OCI image vs tarball | **git submodule** under `apps/<slug>/` (with drop-in `var/hearth/plugins.d/` as escape hatch) | resolved-for-MVP |
| Q4 | Auth in MVP: basic auth required vs no-auth on LAN | **Auth required**; `HEARTH_TRUST_LAN=1` to opt out | open |
| Q5 | Dashboard route: `/` (hub at root) vs `/dashboard/` | **`/`** | resolved-for-MVP |
| Q6 | Default proxy: nginx vs Caddy | **Caddy** (auto local TLS for iPhone PWA); nginx supported | resolved-for-MVP |
| Q7 | Notifications default channel: Web Push vs ntfy vs both | **Both with Web Push primary**; user can switch in settings | resolved-for-MVP |
| Q8 | iPhone CA install flow: profile install vs `mkcert -install` over USB | **Profile install via temporary HTTP server** (`./develop ca-export`), guided in dashboard | resolved-for-MVP |
| Q9 | Hostname: `hearth.home.arpa` (local DNS) vs IP-only | **`hearth.home.arpa`** via local DNS (for example Pi-hole or router DNS); IP fallback documented | resolved-for-MVP |
| Q10 | First reference plugin: groceries vs idea-catcher | **groceries** — exercises persistence, Spark events, Mantle list primitives best | resolved-for-MVP |
| Q11 | Where does VAPID keypair live and rotate? | `var/hearth/secrets/vapid.{pub,priv}`; rotation invalidates subscriptions, deferred to Phase 2 | open |
| Q12 | Plugin process language for `groceries` — Python or Node? | **Python**, to dogfood the default Kindling template | resolved-for-MVP |
| Q13 | Dashboard user layout in FR-0001 MVP: auto grid only vs full edit mode | **Auto grid** of `app-shortcut` blocks; **edit mode + `PUT /layout` in P2** per `dashboard.md` | resolved-for-MVP |
| Q14 | Widget plugin enable in MVP | **Install/validate only**; `enable` returns 501 until P3 widget hosting | resolved-for-MVP |
| Q15 | Demo plugin git remote vs Tinder slug | **Remote:** `github.com/mcelhennyi/grocery-list`; **slug/mount:** `groceries` / `apps/groceries/` | resolved-for-MVP |
| Q16 | Hub ships plugin code? | **No** — hub/registry/Mantle only; plugins external; Kindling bootstraps from `.skeleton` + owns `.skeleton/` submodule | resolved-for-MVP |

Add new questions as `Qn` in chronological order. Do not renumber.
