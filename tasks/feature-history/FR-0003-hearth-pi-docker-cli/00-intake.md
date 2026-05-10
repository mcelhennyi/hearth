# FR-0003 — Intake

| Field | Value |
|------|--------|
| **Title** | Hearth Pi Docker CLI, `./install`, and per-plugin `plugin` tool |
| **Requester** (optional) | Product (via Cursor `/feature-request`) |
| **Target timeline** (optional) | After FR-0002 prototype learnings; may parallel early design-only work with FR-0002 |
| **Constraints** | Install tree **`<install-dir>/heart`**; minimal top-level clutter (data in subdirs); Pi + Docker Compose; subsequent updates via **`hearth --update`**; Kindling plugins get **`install`** + **`plugin`**; mirror **CLI parity** rule in Cursor + Claude docs |
| **Success definition** (1–3 bullets) | (1) Fresh clone on Pi: **`./install`** prepares the host (including Docker where required), lays out **`heart/`** with README + version manifest, generates/merges Compose for hub + **enabled** plugins, and starts the stack. (2) **`hearth`** exposes the requested plugin and stack commands plus a small set of high-value extras (status, logs, doctor, compose passthrough). (3) Each plugin dir has **`plugin`** supporting the listed lifecycle commands, **`plugin --exit`**, and passthrough admin subcommands; templates/docs updated so new Kindling plugins inherit the pattern. |
| **Out of scope** | Full central registry resolution for plugin names; full admin UI implementation (documented follow-up); replacing the existing systemd story entirely (Docker path is **additive**). |
| **Links** | [`10-design-00-skeleton.md`](10-design-00-skeleton.md), [`docs/design/deployment.md`](../../../docs/design/deployment.md), [`docs/design/plugin-contract.md`](../../../docs/design/plugin-contract.md) |

**Raw details** (prose the user or PM provided):

- Client app analogous to **`docker`** for managing the **installed** Hearth instance (Compose-backed “daemon” on Pi).
- Repo-root **`./install`**: first-time setup; later updates **`hearth --update`**.
- Install must ensure system readiness (**Docker**), place files, run Compose including **installed and enabled** plugins.
- Commands: **`hearth --plugin --add <git | future registry name>`**, **`hearth --plugin enter`** (cwd / subshell into plugin for follow-on **`plugin`** commands).
- Per-plugin: **`install`** script (once), **`plugin`** at **`<install-dir>/heart/plugins/<slug>/plugin`**, README + version doc like the root.
- **`plugin`**: `--update`, `--remove`, `--enable`, `--disable`, `--start`, `--stop`, `--reset` (confirm), `--exit`, plus **`-- <plugin-specific admin>`**.
- Future: admin UI uses the same operations.
- Rule: new features that belong in this tool should gain CLI (or tracked follow-up) as other features land.

**Naming note:** Request text uses “heart” in places; product name is **Hearth**; install directory basename is **`heart`** per request (see skeleton for `HEARTH_INSTALL_ROOT` / `heart`).
