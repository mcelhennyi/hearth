# FR-0004 design audit — 2026-05-26

## Verdict

Ready with small plan adjustments. The original parking gates are satisfied in `tasks/ticket-progress.md`, and `T-FR-0004-01` remains complete. The next dependency-valid implementation ticket is `T-FR-0004-02`.

## Adjustments made

- Unparked FR-0004 and marked it `in-progress`.
- Documented the built-in plugin exception: `hearth-users` lives under `apps/builtin/hearth-users/`, not as a normal external app under `apps/<slug>/`.
- Closed stale auth design gaps for Web Push ownership, session cookie path/name, and signature shape.
- Added `X-Hearth-User-Ts` and clarified that the hub verify alias signs identity headers while Caddy strips spoofed inbound headers and copies only verified response headers upstream.
- Added a Kindling child-repo compliance changelog requirement: any Kindling contract/template/runtime change must include an AI-readable migration entry for downstream plugin repos.
- Added FR-0004 nodes to the global DAG and marked `T-FR-0004-01` triad done.

## Frontier

Eligible ticket: `T-FR-0004-02` — Built-in `hearth-users` plugin scaffold.

Feature branch/worktree: `feat/FR-0004-centralized-users-auth` at `.worktrees/FR-0004-centralized-users-auth/feature/`.

Ticket branch/worktree: `feat/FR-0004-centralized-users-auth/T-FR-0004-02-hearth-users-scaffold` at `.worktrees/FR-0004-centralized-users-auth/T-FR-0004-02-hearth-users-scaffold/`.
