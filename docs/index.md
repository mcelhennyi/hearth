<p align="center">
  <img alt="Hearth logo" src="design/logo.svg" width="132" />
</p>

# Hearth

**Local-first home productivity** on a machine you control: one URL, a shared shell, small lifestyle plugins, and an **iPhone PWA** on the Home Screen.

---

## Elevator pitch

Hearth is a **self-hosted hub** for a Raspberry Pi, Mac mini, or similar always-on box. It gives everyday apps—groceries, scheduling, recipes, idea capture—a **shared home** behind a single local HTTPS entrypoint, with **Mantle** for chrome and PWAs, **Tinder** manifests for plugins, and **Spark** for typed app-to-app traffic.

The bottleneck for “home software” is rarely the UI sketch—it is **integration**: TLS that works on an iPhone, routing, identity, notifications, and a consistent shell. Hearth productizes that layer so plugins stay small and composable.

---

## At a glance

### What the hub provides

- **One entrypoint** (for example `https://hearth.home.arpa/`) for every enabled plugin.
- **Mantle** — shared React shell, theme, auth surfaces, PWA manifest + service worker (from Kindling).
- **Tinder** — manifest format for routes, capabilities, dependencies, and permissions.
- **Spark** — discovery, RPC, pub/sub, and dashboard updates between apps.
- **Caddy** by default for **local TLS** so PWAs, service workers, and Web Push behave on a LAN.

Links: [Architecture](design/architecture/overview.md) · [Plugin contract](design/plugin-contract.md) · [Spark API](design/spark-api.md) · [Deployment](design/deployment.md)

### Product status

- **Design-led:** interfaces and workflow are specified under `docs/design/`; code follows the spec.
- **Active prototype track:** FR-0002 focuses on Caddy + `tls internal`, Mantle shell, and iPhone CA trust before the full platform MVP.
- **Parked platform MVP:** FR-0001 resumes after FR-0002 closes and any DESIGN-FLAW feedback is folded in.

Links: [Roadmap](design/roadmap.md) · [Tickets (initial DAG)](design/tickets-initial.md) · [AI / ticket workflow](ai-context.md)

### Process and traceability

- Tickets, worktrees, and frontier workflow live in **`docs/ai-context.md`** and `tasks/`.
- Escalation tags: `DESIGN-GAP`, `DESIGN-FLAW`, `CODE-DEFECT` (see design docs and AI context).

Link: [Documentation style](design/documentation-style.md)

---

## Where to go next

- **Big picture:** [Architecture overview](design/architecture/overview.md)
- **Plugins:** [Plugin contract](design/plugin-contract.md) · [Native plugin ideas](design/native-plugin-ideas.md)
- **UI:** [Mantle UI](design/mantle-ui.md)
- **Ops:** [Deployment](design/deployment.md) · [Notifications](design/notifications.md)
- **Satellites:** [Kindling](design/satellite-repos/kindling.md) · [Ember](design/satellite-repos/ember.md)
- **Process:** [AI workflow](ai-context.md) · [Skeleton maintainers](skeleton-MAINTAINERS.md)

---
**Prev:** — | **Next:** [AI workflow](ai-context.md)
