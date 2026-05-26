# Built-in Platform Plugins

`apps/builtin/<slug>/` is the sole Hearth repository exception to plugin agnosticism.

Built-ins use Tinder manifests, Spark-facing boundaries, and normal gateway routes, but they
ship with Hearth because they provide platform services that should not live inside the hub
monolith. External plugins still belong in separate repositories mounted under `apps/<slug>/`
or installed from drop-in paths.

`hearth-users` supports an optional first-run bootstrap password file at
`var/hearth/secrets/hearth-users-default-password` (or
`$HEARTH_USERS_BOOTSTRAP_PASSWORD_FILE`). This file lives under ignored runtime
state and seeds the `local` user only when no user exists; it is not a password
reset mechanism.
