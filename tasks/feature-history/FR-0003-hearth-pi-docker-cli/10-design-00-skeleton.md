# FR-0003 — Design (level 0, skeleton)

## Purpose

Define **contracts** for a Docker Compose–based Hearth deployment on constrained hosts (Raspberry Pi class): filesystem layout under **`<install-dir>/heart`**, bootstrap **`./install`**, the **`hearth`** admin CLI, and per-plugin **`plugin`** tooling — so a later **admin UI** can call the same operations without re-inventing policy.

## Actors

- **Operator** — human on SSH or local console; may be non-root with `docker` group membership.
- **Bootstrap script** — repo-root **`./install`** (thin shell entry; may delegate to Python — see stack conventions exception note in tickets).
- **`hearth` CLI** — Python package or module invoked from a shim on `PATH`; reads/writes install-local state only under **`heart/`** (and delegated Docker/Compose).
- **Plugin codebase** — Kindling-shaped repo with **`tinder.toml`**, optional **`scripts/install`**, and **`plugin`** executable.
- **Docker Compose** — runtime for hub + plugins in this profile (contrasts with systemd units in [`deployment.md`](../../../docs/design/deployment.md) bare-metal path).

## Public surfaces (skeleton)

| Surface | Kind | Contract (signature / schema sketch) | Owner (logical) |
|---------|------|----------------------------------------|-----------------|
| Install root env | Config | `HEARTH_INSTALL_ROOT` (default: user-chosen at install time) → canonical app dir **`$HEARTH_INSTALL_ROOT/heart`**. | T-FR-0003-02 |
| Version manifest | File | **`heart/VERSION.json`**: `{ "hearth_ref": "<git sha or tag>", "hearth_source": "<clone path or url>", "installed_at": "<iso8601>", "schema": 1 }` | T-FR-0003-02 |
| Plugin registry (local) | File | **`heart/state/plugins.yaml`** (or `.json`): list of `{ slug, source_git, enabled, pinned_ref? }` — MVP; hub DB may supersede later with sync ticket. | T-FR-0003-05 |
| Compose project | Generated | **`heart/compose/docker-compose.yml`** + **`heart/compose/overrides/generated.plugins.yml`** (or single merged file — implementation choice) consumed by `docker compose -p hearth`. | T-FR-0003-05 |
| `hearth` | CLI | Subcommands / flags (see below). Idempotent; no network except documented (`--update`, `plugin --add`). | T-FR-0003-04+ |
| `plugin` | CLI | Per-plugin; forwards to plugin backend admin or edits local plugin state per policy. | T-FR-0003-11 |
| Kindling `install` | Hook | **`scripts/install`** (or documented path in `tinder.toml`) run once on add/update when manifest declares it; exit non-zero aborts with message. | T-FR-0003-10 |

### `hearth` CLI (requested + recommended extras)

**Requested / core**

| Invocation | Behavior |
|------------|----------|
| `hearth --update` | Pull Hearth deploy ref (or re-fetch tarball strategy — **open**), rebuild/pull images, `compose up -d`, run migrations hook if present. |
| `hearth --plugin --add <git-url>` | Clone or submodule into **`heart/plugins/<slug>/`**, validate manifest, run plugin `install` once, register in local registry, regenerate Compose, **start if enabled**. |
| `hearth --plugin enter` | Interactive or `--plugin <slug>`: `cd` or subshell to **`heart/plugins/<slug>`** with env so **`./plugin`** is default admin tool. |

**Recommended additions (power user)**

| Invocation | Behavior |
|------------|----------|
| `hearth --version` / `hearth version` | Print CLI + `VERSION.json`. |
| `hearth status` | Compose `ps` + hub health URL check. |
| `hearth logs [--service …]` | Tail compose services. |
| `hearth start` / `stop` / `restart` | Compose lifecycle. |
| `hearth doctor` | Docker daemon, disk, permissions, compose file presence. |
| `hearth compose -- <args>` | Passthrough `docker compose` with project/env wired. |
| `hearth --plugin list` | List registered plugins and enabled state. |
| `hearth config paths` | Print resolved paths for support. |

**`DESIGN-GAP` (explicit):** Registry-based plugin name resolution (`hearth --plugin --add groceries`) waits on **Hearth relay / trusted registry**; MVP documents the gap and accepts **git URL** only (or local path flag).

### `plugin` CLI (per plugin)

| Flag / arg | Behavior |
|------------|----------|
| `--update` | Update plugin source (git pull / ref bump), rerun `install` if version changed. |
| `--remove` | Disable, remove containers, remove from Compose; optional `--purge` to delete data dir (separate from `--reset`). |
| `--enable` / `--disable` | Toggle enabled; regenerate Compose; **disable** does not delete data. |
| `--start` / `--stop` | Compose service for this slug only. |
| `--reset` | Confirm interactively; wipe **`heart/var/plugins/<slug>/`** (or agreed path), keep code; rerun `install`. |
| `--exit` | Return to previous cwd; if unknown, **`cd ~`**. |
| `-- …` | Passthrough to plugin-defined admin commands (documented in plugin README). |

**Recommended extras:** `--status`, `--logs`, `--doctor` (plugin-specific checks).

## Data in / out

| Input | Output | Storage |
|-------|--------|---------|
| Git URL / path | Cloned plugin tree | **`heart/plugins/<slug>/`** (code) |
| Enabled plugins list | Compose services | **`heart/state/`** + generated compose fragments |
| Runtime DB, uploads | Per-plugin | **`heart/var/plugins/<slug>/`** (mutable); secrets **`heart/var/secrets/`** (mode 0600) — align with existing `var/hearth` semantics where compatible |
| Operator CWD | Restored path | Env `HEARTH_PLUGIN_ENTER_FROM` or shell `pushd` stack for `plugin --exit` |

**Top-level minimalism:** Only **`README.md`**, **`VERSION.json`**, small set of dirs (`bin`, `compose`, `plugins`, `state`, `var`, …) at **`heart/`** root; no loose DB files at top level.

## Sequencing vs existing design

- **`docs/design/deployment.md`**: add a **“Docker profile (Pi)”** section: when Compose is the supervisor, **`hearth` + `./install`** replace the systemd flow for that profile; bare-metal systemd remains for teams that choose it.
- **`T-FR-0001-10`** (bare-metal `install.sh`): after FR-0003, reconcile or split so **one** story is default per target; track overlap in diary — no silent contradiction in authoritative deployment doc.

## Open questions

- **Single-user vs root install:** default to **`docker` group** + install under **`$HOME/heart`** or **`/opt/heart/heart`**? (Ticket: document default + override.)
- **Image build on Pi:** build from source vs pull from registry? (**DESIGN-GAP** for CI publishing — stub in T01.)
- **Hub API duplication:** should `hearth --plugin --add` call hub HTTP or stay file-first until hub exists? MVP recommendation: **file-first**; open ticket for convergence with `T-FR-0001-02` API.

## Process rule (repo-wide)

New **operator-facing** platform features SHOULD expose an equivalent **`hearth`** (or delegated) command **or** carry an explicit **follow-up ticket** for CLI parity — see **`.cursor/rules/stack-conventions.mdc`** (Hearth CLI parity) and **`.claude/rules/development-standards.md`**.
