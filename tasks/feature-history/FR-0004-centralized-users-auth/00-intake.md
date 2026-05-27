# FR-0004 — Intake

| Field | Value |
|------|--------|
| **Title** | Centralized users auth via built-in plugin and gateway |
| **Requester** | Product (Ian) |
| **Target timeline** | Resumed after FR-0002 Pi certificate VAL + closeout and FR-0001 **`T-FR-0001-04`** Mantle shell VAL; 2026-05-26 audit cleared stale blockers. |
| **Status** | `in-progress` (resumed 2026-05-26) |
| **Constraints** | Built-in plugin (not hub monolith); Caddy as default edge; Kindling starter must teach the contract; Spark remains the only app-to-app channel |
| **Success definition** | (1) All plugin HTTP traffic sits behind Hearth’s reverse proxy with a uniform auth gate. (2) A built-in **`hearth-users`** plugin owns multi-user login, session, and verify APIs. (3) Plugins do not ship their own login UI in the default path; they receive trusted identity via headers and Mantle `useUser()`. (4) Kindling `new` scaffolds include middleware/hooks documented for this model. (5) Hub settings reserve a switch to **disable** the built-in provider in favor of a custom user service (implementation of custom provider is follow-up). |
| **Out of scope** | OAuth/social login; Ember device tokens (Phase 2 — same header contract); implementing the full custom user-service adapter (only configuration + verify URL contract in MVP of this FR) |
| **Links** | [`docs/design/architecture/overview.md`](../../../docs/design/architecture/overview.md) §8 Identity; [`T-FR-0001-09`](../../FR-0001-hearth-platform/tickets.md); [`mantle-ui.md`](../../../docs/design/mantle-ui.md) postMessage + `useUser()` |

**Raw details** (user request):

Upgrade Hearth to manage logins for all plugins so plugins use the Hearth users service for login and authentication/authorization. New apps should learn the pattern via the **Kindling** starter project.

- Hearth acts as the **public gateway** for all applications and provides **reverse proxy** so every plugin sits behind it.
- Implement as a **built-in plugin** (not ad-hoc hub code paths). Later, operators may **disable** the built-in service and plug in their own user service.

**Notes:**

- User wrote “Kindle”; project name is **Kindling** (`@kindling/mantle`, `kindling new <slug>`).
- 2026-05-26 product correction: FR-0004 should support **multiple local users** in this branch. The first shipped slice centralizes a single local account; extension tickets **`T-FR-0004-11`…`T-FR-0004-16`** replace that with user ids, usernames, display names, roles, and admin-owned account management before FR-0004 can close.
