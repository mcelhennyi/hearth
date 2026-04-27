---
name: plugin-idea
description: >-
  Creates or updates native Hearth plugin idea design pages that can later become
  standalone .skeleton-initialized plugin repos mounted as submodules. Use when
  the user invokes /plugin-idea or asks to capture, design, or scaffold a native
  plugin idea.
---

# Plugin idea

Create a docs-first native plugin idea that can later graduate into an `FR-NNNN`, be generated from `.skeleton` + Kindling, and be mounted in Hearth as a git submodule under `apps/<slug>/`.

## Inputs

Infer what you can from the user. Ask only for missing essentials:

- Plugin slug (`kebab-case`) and human name.
- One-paragraph charter.
- Whether this is idea backlog, proposed phase, or ready for `FR-NNNN`.
- Expected capabilities, permissions, data ownership, and backup behavior.
- Future repo URL if the user wants an actual submodule now; without a URL, document the submodule plan only.

## Read first

Before writing, read:

- `docs/design/native-plugin-ideas.md`
- `docs/design/plugin-contract.md`
- `docs/design/satellite-repos/kindling.md`
- `docs/design/roadmap.md`

## Write artifacts

1. Create or update `docs/design/plugin-ideas/<slug>.md`.
2. Add or update a row in `docs/design/native-plugin-ideas.md` pointing to the idea.
3. If the idea changes platform direction, update `docs/design/roadmap.md` conservatively.
4. Do **not** allocate an `FR-NNNN` unless the user asks to graduate the idea into the feature-request workflow.

Use this page shape:

```markdown
# Native plugin idea — <name>

**Status:** <idea backlog | later phase | ready for FR>.  
**Proposed slug:** `<slug>`.  
**Mount point:** `apps/<slug>/` as a git submodule when implemented.

## Charter
...

## Why this belongs as a plugin
...

## Tinder sketch
...

## Data and backup
...

## Native repo/submodule plan
...

## Open questions
...

## Non-goals
...
```

## Submodule policy

Only run `git submodule add <repo-url> apps/<slug>` when the user provides a real repository URL and explicitly asks to add it now. Otherwise, write the intended submodule path and creation commands in the design page.

Native plugin repos should be initialized with `.skeleton` for process and Kindling for app scaffolding when those tools are available.

## Verification

For docs-only changes, read the edited pages for broken relative links and run the repo's doc build if available. If no doc build exists, say so in the closeout.
