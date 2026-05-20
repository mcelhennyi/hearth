# FR-0001 — layered design

The shared design surface — Spark, Tinder, Mantle, deployment, notifications, roadmap — is **authoritative** at `docs/design/...` so it is reachable without entering this folder.

This subdirectory holds **FR-0001-specific** notes that belong to the feature line, not the shared spec:

| Doc | Purpose |
|-----|---------|
| [`charter.md`](charter.md) | FR-0001 charter expanded — stakeholders, MVP rationale, non-goals reasoning |
| [`open-questions.md`](open-questions.md) | Live open-question log for this FR (Q1…Q16 + new ones as they appear) |

**Hub boundary:** Hearth ships no plugin application code; see [`docs/design/architecture/overview.md`](../../../../docs/design/architecture/overview.md#1b-plugin-agnosticism-hub-boundary) and Kindling bootstrap in [`docs/design/satellite-repos/kindling.md`](../../../../docs/design/satellite-repos/kindling.md).

For everything else, follow the pointer:

| Topic | Authoritative doc |
|-------|-------------------|
| System architecture, components, data flow | [`docs/design/architecture/overview.md`](../../../../docs/design/architecture/overview.md) |
| Plugin contract (Tinder) | [`docs/design/plugin-contract.md`](../../../../docs/design/plugin-contract.md) |
| Inter-app API (Spark) | [`docs/design/spark-api.md`](../../../../docs/design/spark-api.md) |
| Mantle PWA shell + theme tokens | [`docs/design/mantle-ui.md`](../../../../docs/design/mantle-ui.md) |
| Home dashboard (grid, app vs widget plugins) | [`docs/design/dashboard.md`](../../../../docs/design/dashboard.md) |
| Deployment (Caddy, install, iPhone trust, backup) | [`docs/design/deployment.md`](../../../../docs/design/deployment.md) |
| Notifications (Web Push + ntfy) | [`docs/design/notifications.md`](../../../../docs/design/notifications.md) |
| Roadmap | [`docs/design/roadmap.md`](../../../../docs/design/roadmap.md) |
| Kindling templates repo | [`docs/design/satellite-repos/kindling.md`](../../../../docs/design/satellite-repos/kindling.md) |
| Ember relay (Phase 2 sketch) | [`docs/design/satellite-repos/ember.md`](../../../../docs/design/satellite-repos/ember.md) |

When a shared doc and an FR-0001-specific note disagree, the shared doc wins. Move resolved per-FR notes into the shared docs and amend per `docs/ai-context.md`.
