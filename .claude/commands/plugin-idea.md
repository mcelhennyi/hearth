---
description: >-
  Create or update a native Hearth plugin idea design page that can later become
  a .skeleton-initialized plugin repo mounted as a submodule.
---

# /plugin-idea

Follow the Cursor project skill **`plugin-idea`** (`.cursor/skills/plugin-idea/SKILL.md`).

## What this is

- A docs-first workflow for native plugin ideas.
- The output is a design page under **`docs/design/plugin-ideas/<slug>.md`** plus an index row in **`docs/design/native-plugin-ideas.md`**.
- The idea may later graduate into **`/feature-request`** and become an `FR-NNNN`.
- A real plugin repository should be initialized with **`.skeleton`**, scaffolded from **Kindling**, and added to Hearth as a git submodule at **`apps/<slug>/`**.

## Submodule rule

Do not run `git submodule add` unless the user provides a concrete repository URL and explicitly asks to add it now. Without a URL, document the intended submodule path and commands in the design page.

## Read first

- **`docs/design/native-plugin-ideas.md`**
- **`docs/design/plugin-contract.md`**
- **`docs/design/satellite-repos/kindling.md`**
- **`docs/design/roadmap.md`**
