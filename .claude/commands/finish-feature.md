---
description: >-
  Merges ticket branches into feat/FR-NNNN-slug, validates, opens PR to main for
  human review; never auto-deletes remote branches. See skill finish-feature.
---

# /finish-feature

Follow the Cursor project skill **`finish-feature`** (`.cursor/skills/finish-feature/SKILL.md`).

**Summary:** For one **`FR-NNNN`**, merge all **`feat/T-FR-NNNN-xx-*`** work into **`feat/FR-NNNN-<slug>`**, run checks, push the feature branch, and **`gh pr create`** (or update PR) targeting **`main`**. Do **not** push **`main`** or delete remote branches unless the user explicitly directs otherwise.

## See also

- **`/develop-frontier`**, **`/finish-frontier`**, **`/feature-request`**
- **`docs/ai-context.md`** §2d
