# FR-0004 — Serial diary

## 2026-05-26 (session) — T-FR-0004-10 gateway identity capstone

**Stage:** TEST → DEV → VAL for **T-FR-0004-10**

**Recap (plain English):** Added a capstone identity contract test that simulates the real gateway chain: hub `/api/auth/verify` signs user headers for `/sample-plugin/api/me`, Caddy is expected to pass `X-Original-Method` / `X-Original-Uri` to the upstream plugin, and a generated Kindling plugin rejects direct requests but accepts the verified gateway identity. Updated both dev and install Caddy fragment generators to inject those original request headers before `reverse_proxy`, and updated golden Caddy tests.

**Validation:** `./develop test tests/api/test_gateway_identity_contract.py tests/proxy/test_caddy.py tests/test_plugin_compose_generation.py` — 16 passed, 1 skipped, 2 warnings. `./develop test` — 277 passed, 3 skipped, 4 warnings. `./develop web npm run test` — 4 files passed, 12 tests passed. `./develop web npm run build` — passed. `./develop web npm run lint` — passed.

**Next:** Run full feature validation, merge the ticket branch to `feat/FR-0004-centralized-users-auth`, then run `finish-feature` closeout if the §2d gate passes.

## 2026-05-17 (session) — Intake + design L0/L1 + tickets

**Stage:** intake, design skeleton, ticket DAG

**Recap (plain English):** Registered **FR-0004** (`centralized-users-auth`) for a built-in **`hearth-users`** plugin that owns login/session/verify, with Hearth as the single HTTPS gateway (Caddy `auth_request` + injected `X-Hearth-*` headers). Kindling templates will teach plugins not to ship local login. Settings will allow **`auth.provider=external`** later without implementing a full custom UI in this FR. Split from [**Single-user local auth + Web Push + ntfy** (`T-FR-0001-09`)](../../FR-0001-hearth-platform/tickets.md): identity moves here; push may stay hub-owned (**DESIGN-GAP** Q1). Ten tickets **`T-FR-0004-01`…`10`** drafted with parallel waves in [`20-tickets-dag.md`](20-tickets-dag.md).

**Next:** Push registry reservation to `main`; then either amend `docs/design/` via **T-FR-0004-01** or wait for hub/proxy scaffold before **develop-frontier**.

## 2026-05-17 (session) — T-FR-0004-01 design amendments (option A)

**Stage:** design VAL for **T-FR-0004-01**

**Recap (plain English):** Landed authoritative updates: [`architecture/overview.md`](../../../docs/design/architecture/overview.md) §8 + components, [`plugin-contract.md`](../../../docs/design/plugin-contract.md) (`builtin`, `hearth-users` sketch), [`deployment.md`](../../../docs/design/deployment.md) (gateway auth, Caddy `forward_auth`, trust headers, settings), [`mantle-ui.md`](../../../docs/design/mantle-ui.md) (Authentication section). Split [**Single-user local auth + Web Push + ntfy**](../../FR-0001-hearth-platform/tickets.md) (`T-FR-0001-09`) in feature tickets + FR-0001 README. No `./develop` in repo — doc VAL is review-only.

**Next:** Commit/push registry + docs when ready; remain design-only until hub/proxy scaffold exists.

## 2026-05-18 (session) — Feature parked

**Stage:** process / registry

**Recap (plain English):** Set FR-0004 status to **`parked`** in [`REGISTRY.md`](../REGISTRY.md) and [`README.md`](README.md). Implementation blocked until **FR-0002** Pi CA/certificate path is VAL-complete (**`T-FR-0002-01`**, closeout **`T-FR-0002-04`**) and **FR-0001** initial Mantle shell is VAL-complete (**`T-FR-0001-04`**). **`T-FR-0004-02`…`10`** remain unstarted.

**Next:** Finish FR-0002 + FR-0001-04 gates; then flip registry to `design`/`in-progress` and resume with **`T-FR-0004-02`**.
