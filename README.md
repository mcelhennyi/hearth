# Project skeleton

A **stack-agnostic** template for new repositories: AI session flow, ticket tracking, Cursor and Claude rules, and a manifest so generic tooling improvements can flow back to a parent template.

This tree is **process and tooling only**. It does not choose languages, frameworks, runtimes, or product architecture. You add those after the repo exists.

---

## Contents

| Area | Purpose |
|------|---------|
| [`docs/`](docs/) | Authoritative process docs; start with [`docs/ai-context.md`](docs/ai-context.md) |
| [`tasks/`](tasks/) | Ticket progress, handoffs, feature history, and lessons |
| [`.cursor/`](.cursor/) | Cursor rules and skills (including **`init-project`**) |
| [`.claude/`](.claude/) | Claude Code rules and conventions |
| [`INIT.MD`](INIT.MD) | Full bootstrap: agent prompt, copy steps, upstream sync |
| [`skeleton.manifest`](skeleton.manifest) | Paths allowed for `./push-skeleton contribute` |
| [`push-skeleton`](push-skeleton) | Script to contribute generic changes upstream |

---

## Quick start

1. **New repo:** Follow **[`INIT.MD`](INIT.MD)** — materialize this folder into your repository root (or a monorepo subfolder if you adjust paths in `docs/ai-context.md`).
2. **Root `README.md`:** Replace the placeholder at the repo root with your project: purpose, scope, how to build and run **after** you pick a stack, and where to find product or API docs.
3. **Day to day:** Keep process documentation under `docs/` and delivery state under `tasks/` (especially **`tasks/ticket-progress.md`**).

Prefer driving setup with the **`init-project`** Cursor skill once it exists under `.cursor/skills/init-project/` — see **`INIT.MD`** for a copy-paste prompt template.

---

## Contributing improvements upstream

If this skeleton came from a parent template and you want to push **generic** changes back (wording, skills, manifest entries — not product secrets or app code):

1. Set **`.skeleton-upstream`** or **`SKELETON_UPSTREAM`** to the absolute path of the canonical skeleton repository.
2. Run **`./push-skeleton contribute`** from your project root.
3. Only paths listed in **`skeleton.manifest`** are copied. Upstream maintainers should review and strip anything project-specific before merging.

Details and safety notes: **[`INIT.MD`](INIT.MD)** (section *Contributing tooling improvements upstream*).

---

## License

The repository that **hosts** this skeleton chooses the license. This template does not impose one; set `LICENSE` and root `README` accordingly when you publish or fork.
