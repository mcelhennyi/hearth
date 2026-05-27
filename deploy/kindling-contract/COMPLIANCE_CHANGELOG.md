# Kindling Contract Compliance Changelog

## 2026-05-26 — T-FR-0004-16 multi-user identity migration

**Contract area:** Template, Mantle `useUser()`, backend trust helper, generated docs,
and workflow verification.

**Compatibility:** Breaking for child repos that assume one `local` user, omit
roles from Hearth identity, or cache plugin-local identity across account
switches; additive for plugins that already validate Hearth trust headers and
render user state only through Mantle.

**Who must update:** Any generated plugin repo, local Kindling fork, copied
template, or child repo with a protected route that reads
`X-Hearth-User-Id`, `X-Hearth-User-Name`, `X-Hearth-Roles`, `useUser()`, or a
plugin-local session. Multi-user drift is present when `rg -n "local-owner|Local user|local
login|document.cookie|X-Hearth-Roles|useUser\\(\\)" <repo>` finds a hard-coded
single-user assumption, no roles propagation, or a user cache that is not updated
when the active Hearth session changes.

**Required edits:** Treat Hearth identity as multi-user. Keep first admin setup
owned by `/hearth-users/login`; create later accounts through Hearth Settings
rather than plugin-local forms; parse `X-Hearth-Roles` into the generated
`HearthUser.roles` value; ensure every protected route calls
`require_hearth_user()` per request; remove any fallback to a baked-in `local`
identity; update UI code to call `useUser()` and rerender when the shell sends a
new `hearth.user` message; keep public health checks unauthenticated.

**Verification:** Run `kindling validate <plugin-root>`; run backend tests that
sign two different users and prove a protected route returns each user's id,
display name, and roles; run UI/Mantle tests that switch from a first admin to a
second user and assert `useUser()` updates; smoke the Hearth fixture path with
`./develop test tests/api/test_multi_user_e2e.py
tests/test_kindling_plugin_contract.py`.

**Fallback:** Public-only plugins may defer personalized UI, but they must not
ship a local login or a hard-coded `local` account. User-specific reads/writes
should stay unavailable until the plugin validates the multi-user trust headers
and rerenders on session changes.

## 2026-05-26 — T-FR-0004-08 Mantle session and login handoff

**Contract area:** Mantle shell auth, `useUser()` delivery, login UI ownership.

**Compatibility:** Breaking for child repos or local Mantle copies that render a
plugin-local or hub-local password form; additive for plugins that already rely
on Hearth gateway identity and `useUser()`.

**Who must update:** Any child plugin repo, local Kindling fork, or copied
Mantle shell that contains a `LoginScreen` posting to `/api/auth/login`, reads
session identity from a plugin-local cookie, or expects the plugin iframe to
discover user state without a shell `hearth.user` message. Drift is present when
`rg "/api/auth/login|current-password|hearth.user.request" <repo>` finds a local
login form or no `hearth.user` listener/hook exists.

**Required edits:** Replace local password forms with a link to
`/hearth-users/login?next=<encoded-current-path>`; have the shell fetch
`/hearth-users/api/session` with credentials before rendering authenticated
chrome; normalize `user_id`, `display_name`, and `roles` to the Mantle
`{id,name,roles}` user shape; send `{type:"hearth.user", user}` to plugin
iframes on iframe load and in response to `{type:"hearth.user.request"}`;
consume `useUser()` in plugin UI instead of cookies or local login state.

**Verification:** Run the web/Mantle test suite for the child repo; add or keep
tests that mock a 401 session and assert the login link points at
`/hearth-users/login`, mock a 200 session and assert shell chrome renders, and
spy on iframe `postMessage` to confirm the `hearth.user` payload matches
verified claims. For Hearth itself the validation command is
`./develop web npm run test && ./develop web npm run lint && ./develop web npm
run build`.

**Fallback:** Public-only plugins may defer user-specific UI, but they must not
add a password form or issue their own session cookie. If the shell cannot reach
`/hearth-users/api/session`, fail closed by showing only the Hearth Users login
handoff rather than rendering authenticated plugin chrome.

## 2026-05-26 — T-FR-0004-07 gateway trust headers

**Contract area:** Template, Mantle guidance, backend auth helper, generated docs.

**Compatibility:** Breaking for generated plugins that expose protected backend
routes without validating Hearth gateway identity; additive for public-only
plugins.

**Who must update:** Existing child plugin repos scaffolded from Kindling or the
Hearth `deploy/kindling-contract/` mirror with a Python FastAPI backend. Drift is
present when a repo has backend routes that check local cookies, ships a local
login form in plugin UI, or lacks a `require_hearth_user()` dependency that
validates `X-Hearth-User-Id`, `X-Hearth-User-Ts`, and `X-Hearth-User-Sig`.

**Required edits:** Add a trust helper equivalent to
`<plugin_package>/trust.py`; require it on protected FastAPI routes; configure
`HEARTH_USER_SIG_SECRET` in the plugin runtime; keep `/health` or other explicit
public probes unauthenticated; remove default plugin-local login UI; update UI
code to consume `useUser()` from `@kindling/mantle` instead of cookies.

**Verification:** Run `kindling validate <plugin-root>`; run backend tests that
assert protected routes return 401 without Hearth headers, 401 for invalid or
stale signatures, and 200 for a valid HMAC-SHA256 signature over
`user_id + "\n" + ts + "\n" + method + "\n" + path`; smoke `kindling new
test-auth` and confirm its README documents the trust model.

**Fallback:** A child plugin with no protected backend routes may defer the
middleware migration, but it must not introduce plugin-local login. Any route
that reads or mutates user-specific data should stay unavailable behind Hearth
until the trust helper and tests are in place.
