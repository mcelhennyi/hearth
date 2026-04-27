# Native plugin ideas

**Status:** idea backlog. Items here are not committed scope until they graduate into an `FR-NNNN` feature request.

Hearth plugins are intended to be real apps, not folders of copied code. A native plugin idea should be able to become a standalone repository, receive the project process skeleton, consume Kindling templates, and mount back into Hearth as a git submodule under `apps/<slug>/`.

## Plugin-first ecosystem

Hearth should push as much functionality as practical behind the plugin interface. The hub stays small and stable: discovery, routing, identity handoff, lifecycle, Spark, and narrowly-scoped platform capabilities. Product categories such as remote access, backup, notifications, workflows, analytics, and AI helpers should become native plugins whenever they can be expressed through that contract.

This is an open-source ecosystem bet. A category should be able to support multiple competing implementations without requiring a hub fork: hosted vs self-hosted relay providers, different backup providers, different automation engines, or community-maintained upgrades. If a feature needs privileged platform support, define the smallest Spark/Tinder surface the hub must expose, then keep provider-specific behavior in the plugin.

## Native plugin shape

| Concern | Direction |
|---------|-----------|
| Repository | One git repository per plugin. Initialize it with `.skeleton` so the plugin has the same AI workflow, docs, tickets, and handoff structure as Hearth. |
| Scaffold | Use Kindling (`kindling new <slug>`) when available, or the closest current plugin template before Kindling exists. |
| Mount point | Add the plugin to Hearth as a submodule at `apps/<slug>/`. The hub discovers it through the plugin's `tinder.toml`. |
| Contract | The plugin must satisfy the Tinder contract in [`plugin-contract.md`](plugin-contract.md), including capabilities, permissions, lifecycle hooks, and backup metadata when it owns durable data. |
| Ownership | The plugin owns its code and data model. Hearth owns discovery, routing, identity handoff, lifecycle, and cross-plugin calls. |

Future creation flow:

```bash
# inside Hearth
git submodule add <plugin-repo-url> apps/<slug>
git submodule update --init --recursive apps/<slug>

# inside the plugin repo
./init-skeleton
kindling new <slug>
```

Until the repository and template exist, a plugin idea should start as a design page under `docs/design/plugin-ideas/<slug>.md`. Use the local `/plugin-idea` workflow to create that page.

## Idea index

| Idea | Phase | Summary |
|------|-------|---------|
| [`remote-access`](plugin-ideas/remote-access.md) | Later phase | Native plugin that manages secure remote user/device access through a relay once Ember relay functionality exists. |
| [`system-backup`](plugin-ideas/system-backup.md) | Later phase | Native backup plugin that snapshots hub and plugin data, encrypts with the system password, and uploads to a cloud provider. |

## Graduation criteria

An idea is ready to become an `FR-NNNN` when it has:

1. A one-paragraph charter and explicit non-goals.
2. A Tinder manifest sketch with capabilities, permissions, and backup behavior.
3. A clear submodule plan: repository name, target path under `apps/`, and whether Kindling can scaffold it.
4. Acceptance criteria that can be ticketed without changing the core platform contract silently.
