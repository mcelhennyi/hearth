# Changelog

All notable changes to this **skeleton template** are recorded here. **Consumers** run `./sync-skeleton` from the project root to pull updates from the `.skeleton` submodule and apply removals listed in **`DEPRECATED_PATHS`**.

Maintainers: see **`docs/skeleton-MAINTAINERS.md`** and **`.cursor/rules/skeleton-repo-maintenance.mdc`**.

## [Unreleased]

### Template

- Standardize feature development on repo-local **`.worktrees/FR-NNNN-<slug>/`**: each feature has a `feature/` worktree on **`feat/FR-NNNN-<slug>`**, and each ticket/stage uses a child worktree on a feature-prefixed branch merged back into the feature branch.
- Treat project **`README.md`** as project-owned: remove it from **`skeleton.manifest`**, add **`README.template.md`** for initialization, and update **`init-skeleton`** / **`init-project`** guidance so future syncs do not overwrite consumer READMEs with the skeleton repository README.
- **Feature request skill** (`.cursor/skills/feature-request/SKILL.md`) and **`.claude/commands/feature-request.md`**: document **`./develop`** for doc preview and **VAL** during **`FR-NNNN`** design and implementation; **`reference-templates.md`** adds a **Dev environment** blurb.
- Add **`./develop`**: help menu and commands for doc preview (`up` / `down` / `build` via Docker Compose), host venv (`local` → **`scripts/serve-docs.sh`**), and container `shell` / `run` / `ps`, with optional **`develop.conf`** (from **`develop.conf.example`**; **`DEVELOP_LABEL`**, service name, compose file path). **`sync-skeleton` / `init-skeleton`** set **`+x`** on **`develop`**. **`init-project`** should copy the example, set the label, and adjust compose service keys when the stack file differs.
- Add **`scripts/serve-docs.sh`**: creates `.venv`, installs **`requirements-docs.txt`**, runs **`python -m mkdocs serve`** so docs work without a global **`mkdocs`** on `PATH`.
- Add **`./init-skeleton`** / **`./sync-skeleton`**, submodule nesting workflow, **`DEPRECATED_PATHS`**, maintainer docs, and git hook policy for changelog discipline.
- Ship **`feature-request`**, **`identify-frontier`**, **`develop-frontier`**, **`finish-feature`**, **`finish-frontier`**, **`commit-with-ai-metrics`** Cursor skills, matching **`.claude/commands/`** slash files, **`cursor-claude-doc-sync.mdc`**, and expanded **`docs/ai-context.md`** §2b–§7 / finish-frontier merge notes so the full FR → ticket → parallel frontier workflow is documented in-tree.

### Deprecations (sync removes these paths from consumer project **root**)

When you remove or relocate a path that may already exist in downstream repos, add a line under **`DEPRECATED_PATHS`** (machine list) and summarize the date and reason here.

- *(none — first release of sync deprecations machinery)*

---

## Format reference

- **Template:** bullet user-facing changes to files under this repository (what `sync-skeleton` will copy to consumer roots via `skeleton.manifest`).
- **Deprecations:** every removal must have a **`DEPRECATED_PATHS`** entry (one repo-root-relative path per line, `#` comments allowed) **and** a short note here so humans understand migrations.
