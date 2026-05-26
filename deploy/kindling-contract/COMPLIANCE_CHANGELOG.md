# Kindling Contract Compliance Changelog

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
