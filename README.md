# AI-native project skeleton

**Turn an empty repo into a disciplined delivery machine** — without picking your stack for you. This template is **process and tooling only**: tickets, parallel work, Cursor skills, Claude slash commands, docs-as-truth rules, and a **sync loop** so improvements flow downstream and **generic** wins flow back upstream.

If you ship software with humans *and* agents in the loop, this is the **shared operating system** for how work gets defined, executed, and merged.

---

## Why use it

- **Same playbook everywhere.** One intake → design → `tickets.md` → optional parallel **TEST / DEV / VAL** pattern, documented in [`docs/ai-context.md`](docs/ai-context.md). New repo, same muscle memory.
- **Agents that stay on the rails.** Rules and skills encode *authority* (what docs override, how to escalate), not just style — so Cursor and Claude agree on how your repo works.
- **Parallelism without chaos.** **Identify → develop → finish** frontier skills match real dependency graphs; worktrees and handoffs are first-class, not an afterthought.
- **Upgrade path, not a fork trap.** [`./init-skeleton`](INIT.MD) and [`./sync-skeleton`](INIT.MD) materialize from a manifest; deprecations are explicit. Your product `README` stays yours ([`README.template.md`](README.template.md)); the template never overwrites it on sync.
- **Contribute back safely.** [`./push-skeleton contribute`](INIT.MD) copies only [`skeleton.manifest`](skeleton.manifest) paths to a local upstream checkout — no accidental product leakage.

---

## What you get today

| Layer | You ship faster because… |
|--------|---------------------------|
| **Tickets & history** | `tasks/ticket-progress.md`, feature folders under `tasks/feature-history/`, global DAG in `docs/design/tickets-initial.md` |
| **Cursor** | Skills: `init-project`, `feature-request`, `identify-frontier`, `develop-frontier`, `finish-feature`, `finish-frontier`, `sync-skeleton`, `commit-with-ai-metrics` |
| **Claude Code** | Matching commands under `.claude/commands/` and shared rules |
| **Docs** | Traceability style, architecture stub, maintainer changelog discipline |
| **Day-one dev UX** | [`develop`](develop) + [`develop.conf.example`](develop.conf.example), [`scripts/serve-docs.sh`](scripts/serve-docs.sh) for MkDocs without a global install |
| **Hygiene** | Optional `.githooks/pre-commit` for changelog enforcement in the canonical skeleton tree |

---

## Where we’re headed

Short list of **intentional** next horizons (not promises on a date):

- **Optional CI recipes** — lint/test/docs gates you can drop in once the stack exists  
- **Richer “team mode”** — conventions for multi-human ownership on the same ticket graph  
- **Deeper monorepo notes** — path tweaks and examples when `.skeleton` lives beside multiple packages  
- **Stronger metrics story** — beyond commit footers: dashboards or export hooks for agent effort tracking  
- **More stack-specific *optional* packs** — still opt-in, still manifest-driven, never mandatory bloat  

---

## Quick start

1. **Clone this repo** (your app will live in the same tree after init).  
2. Run **`./init-skeleton`** once — see **[`INIT.MD`](INIT.MD)** for env vars and the full bootstrap.  
3. Use the **`init-project`** skill at the repo root, then build your product; run **`./sync-skeleton`** when you want template updates.

**Upstream contributions:** set **`.skeleton-upstream`** / **`SKELETON_UPSTREAM`**, then **`./push-skeleton contribute`**. Details in **`INIT.MD`**.

---

## License

The **host** repository sets the license. This template does not impose one; add `LICENSE` and your project README when you publish.
