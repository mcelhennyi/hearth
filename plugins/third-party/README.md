# Third-party Hearth plugins

Reference and partner plugin repositories mounted here as **git submodules**. These are **not** built-in/default hub plugins; they ship and version independently while staying easy to bump from the hearth monorepo during integration work.

| Submodule path | Remote | Plugin slug (`tinder.toml`) |
|----------------|--------|-----------------------------|
| `grocery-list/` | `git@github.com:mcelhennyi/grocery-list.git` | `groceries` |

## Updating a submodule

```bash
cd plugins/third-party/<name>
git fetch origin && git checkout <branch> && git pull
cd ../../..
git add plugins/third-party/<name>
git commit -m "chore: bump <name> submodule"
```

Refresh the plugin’s `.kindling/` submodule inside that repo with `./sync-kindling` before UI work.

## Built-in vs third-party

- **Built-in / first-party** plugins may live under `apps/<slug>/` when they are part of the default hearth distribution.
- **Third-party / reference** plugins belong under `plugins/third-party/` for cross-repo development and design-language integration (FR-0006, kindling FR-0001).
