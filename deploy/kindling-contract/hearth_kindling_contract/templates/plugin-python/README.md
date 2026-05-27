# {{ plugin_name }}

Generated Hearth plugin scaffold for `{{ plugin_slug }}`.

## Authentication

Hearth owns login through the public gateway and the built-in `hearth-users`
provider. Do not build a local login form in this plugin, and do not read
browser cookies from plugin JavaScript.

Backend routes that need a user should depend on `require_hearth_user()` from
`{{ python_package }}.trust`. The dependency verifies `X-Hearth-User-Id`,
`X-Hearth-User-Ts`, and `X-Hearth-User-Sig` with `HEARTH_USER_SIG_SECRET`,
rejects stale or invalid headers, and returns a `HearthUser`.

```python
from fastapi import Depends
from .trust import HearthUser, require_hearth_user

@app.get("/api/me")
def current_user(user: HearthUser = Depends(require_hearth_user)):
    return {"id": user.id, "name": user.name, "roles": list(user.roles)}
```

Frontend code should use `useUser()` from `@kindling/mantle`, which receives
the shell-provided Hearth user context. Treat the hook as the UI source of
truth and keep session handling out of plugin code.

```tsx
import { useUser } from "@kindling/mantle";

export function UserBadge() {
  const { user } = useUser();
  return <span>{user?.name ?? user?.id ?? "Signed in"}</span>;
}
```
