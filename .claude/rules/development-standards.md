# Development standards

Use with **`docs/ai-context.md`**. This file mirrors Cursor-facing rules for Claude Code sessions.

## Code style

- **Stack-specific rules:** **`.cursor/rules/stack-conventions.mdc`** once the project chooses languages and frameworks.

## Comments and documentation

- Prefer short module-level notes that point to **`docs/design/...`** where behavior is specified.
- Use the traceability prefix defined in **`docs/design/documentation-style.md`** (default pattern **`@PROJ-<AREA>-<NUMBER>`** until customized).

## Tie backs to documentation

- Escalation tags (**DESIGN-GAP**, **DESIGN-FLAW**, **CODE-DEFECT**) follow **`docs/ai-context.md`**.

## Testing environment

- When **`.devcontainer/`** or CI images exist, run verification (**VAL**) there as tickets specify.

## Worktrees and session beacon

- **Implementation tickets** (**`T-FR-NNNN-xx`**) may use a **dedicated** git worktree under **`worktrees/<slug>/`**.
- Keep **`tasks/ticket-progress.md` → Current focus** updated (**Active ticket**, **Branch / worktree**, **Session status**).

## Subagents (large work)

- **Ahead of large work:** Prefer delegation before broad exploration or multi-file refactors. Follow **`docs/ai-context.md` §1b**.
- **Per ticket:** **TEST → DEV → VAL** serially in **one** worktree unless the team directs otherwise.
- **Parallel tickets:** **`/develop-frontier`** — one subagent per **ticket id**; then **`/finish-feature`** (per **`FR-NNNN`**, **`docs/ai-context.md` §2d**) or **`/finish-frontier`** as the team chose.

## Feature request and frontier (compose)

- **`/feature-request`** / **`.cursor/skills/feature-request/SKILL.md`** — **`FR-NNNN`** design and **`tickets.md`**; does **not** replace **`/identify-frontier`** / **`/develop-frontier`** / **`/finish-feature`** / **`/finish-frontier`**.
- **Spoken “identify (FR)”** = registry + intake; **`/identify-frontier`** = parallel **tickets** only **after** canonical **`### T-FR-NNNN-xx`** sections exist.
- **Registry races:** push **`REGISTRY.md`** + minimal stub to **`main` immediately** after allocating **`FR-NNNN`** (**`docs/ai-context.md` §2b**).

## Ticket completion

- When **VAL** is `done`, run **commit → push → PR** per team policy.
- Update **`docs/design/tickets-initial.md`** when your process marks triads complete.
- Optional metrics footer: **`/commit-with-metrics`** — **`.cursor/skills/commit-with-ai-metrics/SKILL.md`**.

## Session end

- Leave **`tasks/ticket-progress.md`** truthful for the next contributor.
