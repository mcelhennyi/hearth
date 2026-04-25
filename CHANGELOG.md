# Changelog

All notable changes to this **skeleton template** are recorded here. **Consumers** run `./sync-skeleton` from the project root to pull updates from the `.skeleton` submodule and apply removals listed in **`DEPRECATED_PATHS`**.

Maintainers: see **`docs/skeleton-MAINTAINERS.md`** and **`.cursor/rules/skeleton-repo-maintenance.mdc`**.

## [Unreleased]

### Template

- Add **`./init-skeleton`** / **`./sync-skeleton`**, submodule nesting workflow, **`DEPRECATED_PATHS`**, maintainer docs, and git hook policy for changelog discipline.
- Ship **`feature-request`**, **`identify-frontier`**, **`develop-frontier`**, **`finish-feature`**, **`finish-frontier`**, **`commit-with-ai-metrics`** Cursor skills, matching **`.claude/commands/`** slash files, **`cursor-claude-doc-sync.mdc`**, and expanded **`docs/ai-context.md`** §2b–§7 / finish-frontier merge notes so the full FR → ticket → parallel frontier workflow is documented in-tree.

### Deprecations (sync removes these paths from consumer project **root**)

When you remove or relocate a path that may already exist in downstream repos, add a line under **`DEPRECATED_PATHS`** (machine list) and summarize the date and reason here.

- *(none — first release of sync deprecations machinery)*

---

## Format reference

- **Template:** bullet user-facing changes to files under this repository (what `sync-skeleton` will copy to consumer roots via `skeleton.manifest`).
- **Deprecations:** every removal must have a **`DEPRECATED_PATHS`** entry (one repo-root-relative path per line, `#` comments allowed) **and** a short note here so humans understand migrations.
