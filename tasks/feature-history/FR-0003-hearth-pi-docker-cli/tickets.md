# Tickets — FR-0003 Hearth Pi Docker CLI

**Feature id:** **`FR-0003`**
**Canonical ids:** **`T-FR-0003-xx`**
**DAG:** [`20-tickets-dag.md`](20-tickets-dag.md)
**Progress tracker:** [`tasks/ticket-progress.md`](../../ticket-progress.md)

Phases follow `docs/ai-context.md`: **TEST → DEV → VAL** per ticket.

---

### T-FR-0003-01 — Design contract: amend deployment for Docker-on-Pi

**Title:** Design contract: amend deployment for Docker-on-Pi
**Deps:** `none`

#### Purpose

Make **`docs/design/deployment.md`** explicitly describe the **Docker Compose on Pi** profile alongside the existing **systemd + bare metal** story: supervisor choice, filesystem mapping from **`hearth/`** to the doc’s `/opt/hearth` / `/var/hearth` concepts, update flow, and **known gaps** (image publishing, rootless Docker).

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Acceptance criteria for doc amendment | Checklist in ticket diary: every bullet in [`10-design-00-skeleton.md`](10-design-00-skeleton.md) maps to a deployment.md subsection or an explicit **DESIGN-GAP** callout. |
| **DEV** | Edit authoritative deployment doc | `deployment.md` gains a **Docker (Pi) profile** with mermaid or table; systemd path labeled alternative; no contradictory “only systemd” wording. |
| **VAL** | Review | Second reader (human or agent) confirms FR-0001 tickets referencing `install.sh` still parse; cross-link FR-0003 README from deployment doc if helpful. |

#### Notes

- **`DESIGN-GAP`:** central registry plugin names — document MVP is git URL only.

---

### T-FR-0003-02 — Install layout: `hearth/`, VERSION.json, README

**Title:** Install layout: `hearth/`, VERSION.json, README
**Deps:** `T-FR-0003-01`

#### Purpose

Specify and scaffold the on-disk layout under **`<install-dir>/hearth`**: minimal top-level entries, subdirs for **`compose/`**, **`plugins/`**, **`state/`**, **`var/`**, **`bin/`**; **`README.md`** operator guide; **`VERSION.json`** schema v1.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Contract test | Automated check (pytest or script) asserts required dirs + manifest parse on a temp tree. |
| **DEV** | Templates / generators | Code or templates under `deploy/hearth-install/` (path TBD in implementation) create the layout idempotently. |
| **VAL** | Doc + example | Feature README links to schema; example `VERSION.json` committed as **`.example`** only if non-secret. |

---

### T-FR-0003-03 — `./install` bootstrap: Docker + layout + first `compose up`

**Title:** `./install` bootstrap: Docker + layout + first `compose up`
**Deps:** `T-FR-0003-02`, `T-FR-0003-05`

#### Purpose

Repo-root **`./install`**: ensure **Docker Engine** (Pi: documented `apt`/`get.docker.com` path or distro matrix), create **`hearth/`** layout, install **`hearth`** shim to `PATH` (symlink or copy), generate compose, run **`docker compose up -d`** for hub + enabled plugins.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Dry-run mode | `./install --dry-run` prints actions without mutating (or uses temp root). |
| **DEV** | Implement bootstrap | Idempotent re-run; clear errors; non-root path documented (`docker` group). |
| **VAL** | ARM smoke | Script succeeds in CI ARM container **or** documented manual Pi run with diary entry. |

#### Notes

- Stack rule: **Bash** only for thin wrapper — heavy logic in **Python**; document in diary if exception needed.

---

### T-FR-0003-04 — `hearth` CLI core: argparse, paths, doctor, compose passthrough

**Title:** `hearth` CLI core: argparse, paths, doctor, compose passthrough
**Deps:** `T-FR-0003-01`, `T-FR-0003-02`

#### Purpose

Implement the **`hearth`** command: resolve install root, load `VERSION.json`, **`hearth doctor`**, **`hearth compose -- <args>`**, **`hearth version`**, global `--help`.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Unit tests | argparse / path resolution tests with temp dirs; doctor fails gracefully without docker. |
| **DEV** | Package + shim | e.g. `apps/hub/cli` or `deploy/hearth-cli/` — pick single home; `bin/hearth` exec. |
| **VAL** | Manual smoke | From a dev container or host: `hearth version`, `hearth doctor`, `hearth compose ps` against a fixture project. |

---

### T-FR-0003-05 — Plugin registry file + Compose fragment generation

**Title:** Plugin registry file + Compose fragment generation
**Deps:** `T-FR-0003-01`, `T-FR-0003-02`

#### Purpose

Maintain **`hearth/state/plugins.yaml`** (or `.json`) and generate **`docker-compose`** fragments so **enabled** plugins receive services, volumes, and env — consistent with `deploy/compose/docker-compose.yml` conventions.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Golden file test | Given fixture registry + plugin dirs, output matches expected compose YAML. |
| **DEV** | Generator | Regenerate on add/enable/disable; validate with `docker compose config`. |
| **VAL** | Integration | `docker compose up` with two fake plugins (fixtures) starts **or** build args documented if images missing. |

---

### T-FR-0003-06 — `hearth --update`

**Title:** `hearth --update`
**Deps:** `T-FR-0003-04`, `T-FR-0003-05`

#### Purpose

Implement **`hearth --update`**: fetch latest Hearth sources (git pull of deploy checkout or documented alternative), refresh plugins per policy, rebuild/pull images, **`compose up -d`**, run DB migrations if hub provides hook.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Mocked git / compose | Tests use temp repo + fake compose binary or subprocess mock. |
| **DEV** | Implement | Idempotent; logs which refs changed. |
| **VAL** | Dry-run on real clone | Human or CI: run twice, second is no-op; diary note. |

---

### T-FR-0003-07 — `hearth --plugin --add` and `list`

**Title:** `hearth --plugin --add` and `list`
**Deps:** `T-FR-0003-04`, `T-FR-0003-05`

#### Purpose

**`hearth --plugin --add <git-url>`**: clone to **`hearth/plugins/<slug>/`**, validate **`tinder.toml`**, run **`scripts/install`** if present, update registry, regenerate compose, start if enabled.

**`hearth --plugin list`**: print table of slug, source, enabled, version/ref.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Fixture plugin | Integration test with minimal valid `tinder.toml` in temp git repo. |
| **DEV** | Commands | Clear errors on invalid slug / clone failure. |
| **VAL** | Manual | Add sample plugin; `list` shows row; hub route optional for MVP. |

#### Notes

- Registry name resolution **out of scope** — error message points to future relay.

---

### T-FR-0003-08 — `hearth --plugin enter`

**Title:** `hearth --plugin enter`
**Deps:** `T-FR-0003-07`

#### Purpose

**`hearth --plugin enter`** (with `--slug` or interactive pick): start subshell or **`exec $SHELL`** with cwd **`hearth/plugins/<slug>`** and env **`HEARTH_PLUGIN_ENTER_FROM=$PWD`** (or stack) so **`plugin --exit`** can restore.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Env contract | Unit test sets env and verifies `plugin --exit` logic in isolation. |
| **DEV** | UX | Works for `bash` and `zsh` documented; falls back to `cd` instructions if non-interactive. |
| **VAL** | Manual | Operator enters, runs `./plugin status`, exits back. |

---

### T-FR-0003-09 — `hearth` stack control: start/stop/restart/status/logs

**Title:** `hearth` stack control: start/stop/restart/status/logs
**Deps:** `T-FR-0003-04`, `T-FR-0003-05`

#### Purpose

Thin commands: **`start`**, **`stop`**, **`restart`**, **`status`** (compose **ps** + **`GET /api/health`** when hub image available), **`logs`** with service filter.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Argument forwarding | Tests assert correct compose subcommand mapping. |
| **DEV** | Implement | Consistent project name / env file. |
| **VAL** | Manual | Against running dev stack or fixture compose. |

---

### T-FR-0003-10 — Kindling contract: `scripts/install` + `plugin` template

**Title:** Kindling contract: `scripts/install` + `plugin` template
**Deps:** `T-FR-0003-01`, `T-FR-0003-02`

#### Purpose

In **Kindling** (or Hearth mirror if Kindling not yet public): document **`scripts/install`** lifecycle; ship **`plugin`** stub implementing common flags and **passthrough** to **`python -m <plugin>.admin`** or similar — exact pattern in Kindling FR / handoff.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | Template renders | `kindling new` (or equivalent) produces `plugin` executable + `scripts/install` hook. |
| **DEV** | Upstream or submodule PR | Link commit URL in diary. |
| **VAL** | Hearth consumes | New plugin from template works with **T-FR-0003-07** add flow. |

---

### T-FR-0003-11 — Per-plugin `plugin` executable: lifecycle + passthrough

**Title:** Per-plugin `plugin` executable: lifecycle + passthrough
**Deps:** `T-FR-0003-07`, `T-FR-0003-10`

#### Purpose

Executable at **`hearth/plugins/<slug>/plugin`**: **`--update`**, **`--remove`**, **`--enable`**, **`--disable`**, **`--start`**, **`--stop`**, **`--reset`** (confirm), **`--exit`**, and **`-- <admin args>`** delegated to plugin.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | CLI tests | pytest with subprocess or click/typer harness for each flag. |
| **DEV** | Shared helper | Optional Python package `hearth_plugin_cli` to dedupe. |
| **VAL** | E2E | From **enter**: run **`plugin --disable`**; compose reflects; re-enable. |

---

### T-FR-0003-12 — Smoke tests + ARM CI for install path

**Title:** Smoke tests + ARM CI for install path
**Deps:** `T-FR-0003-03`, `T-FR-0003-06`, `T-FR-0003-08`, `T-FR-0003-09`, `T-FR-0003-11`

#### Purpose

Automate **`./install --dry-run`**, **`hearth doctor`**, **`hearth --plugin list`**, and a minimal compose config check in CI (ARM runner optional); document Pi VAL checklist.

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | CI green | Workflow file or existing CI extended; skips gracefully on missing docker. |
| **DEV** | Scripts | Single **`scripts/ci/hearth-install-smoke.sh`** or pytest entry. |
| **VAL** | Real hardware note | `serial-diary.md` entry or **`40-pi-val.md`** with timing + model. |

---

### T-FR-0003-13 — Project rules: Hearth CLI parity (Cursor + Claude)

**Title:** Project rules: Hearth CLI parity (Cursor + Claude)
**Deps:** `T-FR-0003-01`

#### Purpose

Add **Hearth CLI parity** discipline: new operator-facing features SHOULD ship **`hearth`/`plugin` surface** or an explicit follow-up ticket — in **`.cursor/rules/stack-conventions.mdc`** and **`.claude/rules/development-standards.md`** (sync per `cursor-claude-doc-sync`).

#### Phases

| Phase | Goal | Exit criteria |
|-------|------|----------------|
| **TEST** | N/A | Rule change only. |
| **DEV** | Edit rules | Both files updated; cross-link to `docs/design/deployment.md` Docker profile once merged. |
| **VAL** | Peer skim | Feature README “Process rule” matches wording. |

---

## Acceptance for FR-0003 closeout

All tickets **`done`** in **`tasks/ticket-progress.md`**, deployment doc and Kindling contract aligned, Pi or ARM CI smoke green, **`90-closeout.md`** written with UI follow-up pointer.
