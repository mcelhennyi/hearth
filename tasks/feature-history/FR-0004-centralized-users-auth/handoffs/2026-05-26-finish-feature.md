# FR-0004 finish-feature handoff

Date: 2026-05-26

**Superseded 2026-05-26:** Product corrected FR-0004 to require multi-user local auth before closeout. Treat this handoff as the completed single-account slice only; continue with `T-FR-0004-11` through `T-FR-0004-16`.

Feature branch: `feat/FR-0004-centralized-users-auth`

Feature PR: [PR #56](https://github.com/mcelhennyi/hearth/pull/56) → `main`

## Executive summary

FR-0004's first slice is complete on the feature branch. It adds the built-in `hearth-users` identity provider, hub verify/signing, Caddy auth gates for plugin routes, Mantle login/session/user delivery, Kindling trust middleware, external verify URL settings, and a capstone test proving a generated plugin accepts only gateway-verified identity. It is not final FR-0004 closeout until the multi-user extension lands.

## Merged branches

| Ticket | Branch |
|--------|--------|
| `T-FR-0004-02` | `feat/FR-0004-centralized-users-auth-T-FR-0004-02-hearth-users-scaffold` |
| `T-FR-0004-03` | `feat/FR-0004-centralized-users-auth-T-FR-0004-03-users-session-verify` |
| `T-FR-0004-04` | `feat/FR-0004-centralized-users-auth-T-FR-0004-04-auth-verify-provider` |
| `T-FR-0004-05` | `feat/FR-0004-centralized-users-auth-T-FR-0004-05-caddy-auth-request` |
| `T-FR-0004-06` | `feat/FR-0004-centralized-users-auth-T-FR-0004-06-spark-session-rules` |
| `T-FR-0004-07` | `feat/FR-0004-centralized-users-auth-T-FR-0004-07-kindling-trust-template` |
| `T-FR-0004-08` | `feat/FR-0004-centralized-users-auth-T-FR-0004-08-mantle-login-use-user` |
| `T-FR-0004-09` | `feat/FR-0004-centralized-users-auth-T-FR-0004-09-external-auth-settings` |
| `T-FR-0004-10` | `feat/FR-0004-centralized-users-auth-T-FR-0004-10-plugin-trust-e2e` |

## Validation

- `./develop test` — 277 passed, 3 skipped, 4 warnings.
- `./develop web npm run test` — 4 files passed, 12 tests passed.
- `./develop web npm run build` — passed.
- `./develop web npm run lint` — passed.

## Suggested next step

Review [PR #56](https://github.com/mcelhennyi/hearth/pull/56); the merger should remove repo-root `CURRENT.md` from `main` and refresh `90-closeout.md` with the merge SHA after landing.

## Options

| Option | When |
|--------|------|
| Merge PR | Human review accepts FR-0004. |
| Request changes | Review finds auth UX, trust header, or install-route concerns. |
| Continue next FR | Start FR-0005 while FR-0004 waits in PR review. |
