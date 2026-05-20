---
name: finish-feature
description: >-
  Merges all ticket/stage branches for one FR-NNNN feature into the feature
  integration branch, validates, and opens (or updates) a PR to the default branch
  only after the feature-complete gate in docs/ai-context.md §2d. Never deletes
  remote branches automatically. Use when closing a full FR-NNNN implementation
  on the feature branch workflow.
---

# Finish feature (`FR-NNNN`)

Close **implementation** for a **single** product feature that used a **feature integration branch** — all ticket/stage branches **`feat/FR-NNNN-<slug>/...`** should already merge **into** **`feat/FR-NNNN-<slug>`** (not directly to the default branch). This skill finishes that line and hands off to humans on the **default branch** **only when** **`docs/ai-context.md` §2d** **feature-complete gate** is satisfied.

## Preconditions

- **`FR-NNNN`** and **`<slug>`** known; **`tasks/feature-history/FR-NNNN-<slug>/`** exists with **`tickets.md`**, diaries, and **`handoffs/`** as needed.
- **Feature integration branch** exists on the remote, e.g. **`feat/FR-0007-auth-overhaul`**, and is checked out at **`.worktrees/FR-0007-auth-overhaul/feature/`** (or an explicit equivalent path). Ticket/stage branches exist and are pushed.
- **Integration policy:** Do **not** push to the **default branch** from this skill — only **PR** (or draft PR) for final human review unless the user explicitly overrides.

## 1 — Ensure ticket work is merged into the feature branch

In the feature worktree checkout of **`feat/FR-NNNN-<slug>`** (normally **`.worktrees/FR-NNNN-<slug>/feature/`**):

1. `git fetch origin`
2. `git checkout feat/FR-NNNN-<slug>` and `git pull --ff-only` (or merge) as appropriate.
3. For each feature-prefixed ticket/stage branch (for example **`feat/FR-NNNN-<slug>/T-FR-NNNN-xx-short-name`**) in **dependency-safe** order, `git merge --no-ff <branch> -m "merge: T-FR-NNNN-xx (finish feature FR-NNNN)"`.
4. Resolve conflicts; prefer preserving both intents. Do **not** delete the source ticket/stage branches locally or on the remote.
5. **CURRENT.md:** consolidate repo-root **`CURRENT.md`** on **`feat/FR-NNNN-<slug>`** so it matches merged reality (resolve conflicts by merging prose, not deleting the file). See **`feature-request`** skill **Branch state (`CURRENT.md`)**.

## 2 — Validation on the feature branch

Run the full verification required for all merged **`T-FR-NNNN-xx`** tickets using Docker / Docker Compose / Dev Container / CI images where possible per **`docs/ai-context.md`**. Host-local validation is an exception and must be documented in the finish handoff. Fix forward on the **feature branch** if issues are small; otherwise stop and leave the branch for human triage.

## 3 — Feature-complete gate (before any default-branch PR)

1. Verify every **`### T-FR-NNNN-xx`** in **`tasks/feature-history/FR-NNNN-<slug>/tickets.md`** has **TEST**, **DEV**, and **VAL** = **`done`** in **`tasks/ticket-progress.md`** for that **`FR-NNNN`**.
2. If **not** all **`done`**: `git push -u origin feat/FR-NNNN-<slug>`; append or refresh **`tasks/feature-history/FR-NNNN-<slug>/handoffs/`** with the next frontier — **stop**. Do **not** open **`feat/FR-NNNN-<slug>` → default branch** PR until the gate passes.
3. If all **`done`**: proceed to **§4**.

## 4 — Push feature branch and open PR to the default branch

1. `git push -u origin feat/FR-NNNN-<slug>`
2. Prefer **`gh pr create`** (base = default branch, head **`feat/FR-NNNN-<slug>`**) with a summary linking **`tasks/feature-history/FR-NNNN-<slug>/`** and ticket ids.
3. If a PR already exists, push branch updates and ensure the PR description lists merged tickets.
4. Ensure the description reminds the merger to **delete** repo-root **`CURRENT.md`** when the PR lands on the default branch (unless the repo documents otherwise) — **`feature-request`** skill **Branch state (`CURRENT.md`)**. After merge, **`REGISTRY.md`** should be **`complete`** for this **`FR-NNNN`**; the merger or **`/feature-request-continue`** should run **`feature-request`** **Closeout** hygiene: **`90-closeout.md`**, **retire** this feature from **`tasks/ticket-progress.md` → `Parallel streams`**, and point **Current focus** at the next open ticket.

## 5 — Feature history bookkeeping

1. Append or create **`tasks/feature-history/FR-NNNN-<slug>/handoffs/YYYY-MM-DD-finish-feature.md`** with: merged branches (names + SHAs), PR link, validation summary, **executive summary** of what was integrated, a **suggested next step** for the reviewer, and **options** (e.g. merge vs. request changes) if applicable — same structure as **`feature-request`** **User-facing close (required)**.
2. Update **`tasks/feature-history/FR-NNNN-<slug>/README.md`** with PR link and status.
3. Run **diary consolidation** per **`feature-request`** skill (**`DIARY.md`**, newest-first stack) if not already done for this milestone.

## 6 — Branch hygiene (audit)

- **Never** automatically **`git push origin --delete`** or **`git branch -D`** ticket/stage or feature branches used in this workflow — they are the **audit trail** of how work evolved.
- **Optional:** remove only **local** worktree directories to free disk, after confirming the **remote** branch still exists and the team does not need the local path.

## Relationship to **`finish-frontier`**

| Skill | When |
|-------|------|
| **`finish-feature`** | One **`FR-NNNN`**: ticket/stage branches → **`feat/FR-NNNN-<slug>`** → **PR to default branch** for human merge **only after** **§2d** **feature-complete gate**. |
| **`finish-frontier`** | Multi-ticket integration that merges **directly** into the default branch (integration checkout) per existing policy — still **do not delete remote audit branches** unless a human explicitly asks. |

## See also

- **`feature-request`**, **`develop-frontier`**, **`finish-frontier`**
- **`docs/ai-context.md`** §2d (feature branch workflow)
