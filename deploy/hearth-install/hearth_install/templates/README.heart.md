# Hearth install (`heart/`)

This directory is the **Docker profile** install root on a Pi-class host. Roles match **`docs/design/deployment.md`** in the Hearth repository (section **Docker profile (Pi)**).

## Layout

| Path | Role |
|------|------|
| `compose/` | Compose project files and generated plugin overrides |
| `plugins/` | Plugin checkouts (`<slug>/` per plugin) |
| `state/` | Machine-local config and generated registry files |
| `var/` | Mutable data: databases, plugin data, logs |
| `bin/` | Operator shims (e.g. `hearth` on `PATH`) |
| `VERSION.json` | Install manifest (schema v1). JSON Schema in the deploy repo: `deploy/hearth-install/schemas/version-1.schema.json`. Example: `deploy/hearth-install/hearth_install/templates/VERSION.json.example`. |
| `README.md` | This file (refreshed from the deploy repo template when the layout generator runs) |

## Regenerate

From a checkout of the Hearth deploy repository:

```bash
python -m hearth_install /path/to/install-root --hearth-ref "$(git rev-parse HEAD)"
```

Pass the **parent** of `heart/` as `install-root` (the tool creates `heart/` under that path).
