# Initializing a new project from this skeleton

This repository is a **process- and tooling-only** template: tickets, AI session context, Cursor or Claude rules, sync scripts, and a manifest for contributing improvements upstream. It does **not** prescribe languages, frameworks, or application architecture.

## Recommended workflow (clone → init → work here)

1. **Clone** this skeleton repository (your future app repo will reuse this clone’s directory).
2. From the clone root, run **`./init-skeleton`** once (see **Environment variables** below if `origin` is not set).
3. After init, **stay in the same directory**: it is now your **project root**. Template sources live in **`.skeleton/`** (git submodule); day-to-day copies of the template files live at the **repo root** and are refreshed with **`./sync-skeleton`**.
4. Point **`origin`** at **your** empty remote (if you have not already), then **`git commit`** the init result.

`./init-skeleton`:

- Adds **`.skeleton/`** as a **git submodule** pointing at the same skeleton URL as `origin` (or `SKELETON_SUBMODULE_URL`), pinned to the commit you had checked out when you ran it.
- Re-materializes every path listed in **`skeleton.manifest`** at the **repo root** (same layout as before init, but root files are now copies you can customize).
- Removes **`SKELETON_REPO`** from the **root** only (that marker stays inside **`.skeleton/`** so the submodule remains identifiable as the canonical template tree).

### Environment variables (`init-skeleton`)

| Variable | Purpose |
|----------|---------|
| **`SKELETON_SUBMODULE_URL`** | Submodule URL if `origin` is missing or should differ from `origin`. |
| **`SKELETON_SUBMODULE_BRANCH`** | Remote branch for `git submodule add -b` (defaults from `git remote show origin` or **`main`**). |

## Syncing template updates (`./sync-skeleton`)

From the **project root** (after init):

1. Fast-forwards the **`.skeleton/`** submodule (`git pull` or `git submodule update --remote` if needed).
2. Deletes every path listed in **`.skeleton/DEPRECATED_PATHS`** from the **project root** (never deletes arbitrary paths under `.skeleton/` itself).
3. Overwrites root files listed in **`skeleton.manifest`** with copies from **`.skeleton/`**.
4. Stages the submodule pointer and updated root files (`git add`); you **`git commit`** when satisfied.

**Agent shortcut:** the **`sync-skeleton`** Cursor skill (`.cursor/skills/sync-skeleton/SKILL.md`) and Claude **`/sync-skeleton`** command (`.claude/commands/sync-skeleton.md`) walk through the same steps — run **`./sync-skeleton`** from the project root, then review **`git status`**.

## Maintainer rules (this skeleton repository)

When **`SKELETON_REPO`** exists at the **root** of this checkout, you are in the **canonical skeleton** tree.

- **Every commit** that changes shipped template files must update **`CHANGELOG.md`** (`[Unreleased]` → **Template**).
- When you **remove or relocate** something consumers may already have at their **project root**, add a line to **`DEPRECATED_PATHS`** (one repo-root-relative path per line) **and** note it under **`[Unreleased]` → Deprecations** in **`CHANGELOG.md`** so `sync-skeleton` can delete stale paths.

Enable git hooks once per clone:

```bash
git config core.hooksPath .githooks
```

Details: **`docs/skeleton-MAINTAINERS.md`**, **`.cursor/rules/skeleton-repo-maintenance.mdc`**.

## Fast path: prompt an agent

Use the **`init-project`** Cursor skill (`.cursor/skills/init-project/SKILL.md` at repo root after init). Example:

> Use the **init-project** skill. I already ran **init-skeleton** (or I am about to). Here are my answers: …

### Copy-paste prompt template

```text
Use the init-project skill after the generic skeleton workflow.

Required:
- Project name (human-readable):
- One-line charter (what this repo is for):
- Default branch name (e.g. main):
- License or visibility (note only):

Desired:
- Primary languages / runtime (agent should not add heavy scaffold until confirmed):
- CI target (e.g. GitHub Actions, none yet):
- Traceability prefix for @PROJ-* style tags in docs:

Constraints:
- Process/tooling only; no fictional product requirements.
- Remind me to run ./sync-skeleton periodically and after skeleton releases.
```

## Contributing tooling improvements upstream

If you improved **generic** process files at the **repo root**, use **`./push-skeleton contribute`** with **`.skeleton-upstream`** or **`SKELETON_UPSTREAM`** pointing at a **local checkout** of the skeleton source repository. Only paths in **`skeleton.manifest`** are copied. See **`push-skeleton help`**.

## Where to look next

| Path | Role |
|------|------|
| `./develop` | Optional **`develop.conf`**; **`help`**, doc preview via Compose, **`local`** = **`./scripts/serve-docs.sh`** (see root **`develop.conf.example`**) |
| `docs/ai-context.md` | Session bootstrap, worktrees, **`FR-NNNN`** / frontier workflow (**§2b–§7**); process SSOT; docs-as-source-of-truth escalation |
| `.cursor/rules/docs-authority-and-escalation.mdc` | Design vs code authority (mirror: `.claude/rules/docs-authority-and-escalation.md`) |
| `tasks/ticket-progress.md` | Active ticket / phase / session beacon |
| `.cursor/skills/feature-request/SKILL.md` | **`FR-NNNN`** intake → design → **`tickets.md`** → optional implement |
| `.cursor/skills/feature-request/reference-templates.md` | Markdown tables / diary / handoff templates |
| `.cursor/skills/identify-frontier` / `develop-frontier` / `finish-feature` / `finish-frontier` | Parallel ticket frontier + integration |
| `.claude/commands/` | Slash commands mirroring those skills (`/feature-request`, …) |
| `.cursor/rules/cursor-claude-doc-sync.mdc` | Keep Cursor + Claude workflow docs aligned |
| `skeleton.manifest` | Declares which files `sync-skeleton` / `push-skeleton` touch |
| `DEPRECATED_PATHS` | Paths removed from consumer root on `sync-skeleton` |
| `CHANGELOG.md` | Human-facing template + deprecation history |
| `.cursor/skills/init-project/SKILL.md` | Post-**`init-skeleton`** customization checklist |
