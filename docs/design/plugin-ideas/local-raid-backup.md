# Native plugin idea — local RAID backup

**Status:** later-phase idea, not MVP scope.  
**Proposed slug:** `local-raid-backup`.  
**Mount point:** `apps/local-raid-backup/` as a git submodule when implemented.

## Charter

Create a native Hearth plugin that performs local-first backups to user-managed RAID storage on the same network or directly attached storage. The plugin discovers or registers backup targets, validates target health, schedules encrypted snapshots of hub and plugin-declared data, and supports guided restore from local backup sets without requiring a cloud provider.

## Why this belongs as a plugin

Backup strategy is product policy and hardware-specific implementation, not core platform behavior. Keeping RAID backup in a plugin allows multiple backup implementations to coexist (local RAID, cloud, hybrid) while the hub stays focused on discovery, identity handoff, lifecycle, and Spark boundaries.

The hub should expose only the shared surfaces all backup plugins need: installed plugin registry, Tinder backup metadata, lifecycle coordination, and secure secret handling. RAID adapter logic, retention policy UX, and storage diagnostics belong in this plugin.

## Tinder sketch

```toml
[plugin]
slug = "local-raid-backup"
name = "Local RAID Backup"
version = "0.1.0"
hearth_min = "0.1.0"
description = "Encrypted local backup to RAID-backed storage."

[entrypoint]
backend = { kind = "python", module = "local_raid_backup.app:create_app", port_env = "HEARTH_PLUGIN_PORT" }
ui = { kind = "static", path = "web/dist" }

[capabilities.local_backup]
methods = ["configure_target", "validate_target", "run", "status", "restore_plan"]
events = ["started", "completed", "failed", "target_degraded"]

[permissions]
spark_call = ["hub.plugins.*", "hub.backup.*", "hub.settings.*"]
spark_publish = ["local-raid-backup.*"]
spark_subscribe = ["hub.plugin.installed", "hub.plugin.removed"]
fs_paths = ["plugins/local-raid-backup"]
network = "lan"

[backup]
include = ["plugins/local-raid-backup/state.sqlite"]
exclude = ["plugins/local-raid-backup/cache/"]

[ui.nav]
label = "Local Backup"
icon = "hard-drive"
order = 81
```

## Data and backup

The plugin should manage metadata and scheduling state locally while treating backup payloads as encrypted artifacts:

| Data | Backup behavior |
|------|-----------------|
| Target definitions (NAS path, mount id, RAID profile label) | Include in plugin backup. |
| Retention policy and schedules | Include in plugin backup. |
| Snapshot manifests, checksums, and restore indexes | Include in plugin backup. |
| Temporary staging artifacts and transfer buffers | Exclude from plugin backup. |
| Raw credentials/secrets for mounted shares | Keep in hub-managed secrets storage; do not include in plugin backup paths. |

Backups written to RAID targets should be encrypted before write, and restore should validate checksums plus manifest compatibility before data is applied.

## Native repo/submodule plan

When this idea graduates, create a standalone plugin repository and mount it into Hearth:

```bash
# create the plugin repo separately, then inside Hearth
git submodule add <local-raid-backup-repo-url> apps/local-raid-backup
git submodule update --init --recursive apps/local-raid-backup

# inside apps/local-raid-backup
./init-skeleton
kindling new local-raid-backup
```

The plugin repo should keep its own `.skeleton` process artifacts and test matrix for target validation and restore safety. Hearth should track only the submodule pointer and any platform contract changes needed for backup lifecycle coordination.

## Open questions

- Do we support only mounted local filesystems first, or also SMB/NFS target discovery in the first release?
- What minimum RAID health signals should block backup execution (`degraded`, `rebuild`, `unknown`)?
- Should retention be policy-based (hourly/daily/weekly) only, or include storage-cap usage targets?
- How should local backup encryption keys be derived and rotated without weakening recovery ergonomics?
- Should this plugin later compose with `system-backup` as a shared backup engine, or remain independent?

## Non-goals

- Replacing the host OS RAID management stack.
- Managing cloud backup provider integrations.
- Running arbitrary filesystem backups outside Hearth-owned data roots in the first version.
- Silent restore over live plugin state without validation and operator confirmation.
- Acting as a full NAS management UI.
