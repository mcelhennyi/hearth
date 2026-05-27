# FR-0004 finish-feature handoff

Date: 2026-05-26

**Updated 2026-05-27:** Product corrected FR-0004 to require multi-user local
auth before closeout. That multi-user wave is now complete through
`T-FR-0004-16`; PR #56 is ready for human review/merge to `main`.

Feature branch: `feat/FR-0004-centralized-users-auth`

Feature PR: [PR #56](https://github.com/mcelhennyi/hearth/pull/56) → `main`

## Executive summary

FR-0004 is complete on the feature branch. It adds the built-in multi-user
`hearth-users` identity provider, hub verify/signing, Caddy auth gates for
plugin routes, Mantle login/session/user delivery, Kindling trust middleware,
external verify URL settings, admin user management, and stitched E2E proof
that a protected generated plugin sees the active user.

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
| `T-FR-0004-11` | `feat/FR-0004-centralized-users-auth-T-FR-0004-11-multi-user-design` |
| `T-FR-0004-12` | `feat/FR-0004-centralized-users-auth-T-FR-0004-12-multi-user-auth-api` |
| `T-FR-0004-13` | `feat/FR-0004-centralized-users-auth-T-FR-0004-13-first-admin-login-ui` |
| `T-FR-0004-14` | `feat/FR-0004-centralized-users-auth-T-FR-0004-14-real-user-claims` |
| `T-FR-0004-15` | `feat/FR-0004-centralized-users-auth-T-FR-0004-15-admin-user-management` |
| `T-FR-0004-16` | `feat/FR-0004-centralized-users-auth-T-FR-0004-16-multi-user-e2e-compliance` |

## Validation

- `./develop test` — 351 passed, 3 skipped, 10 warnings.
- `./develop web npm run test` — 15 files passed, 66 tests passed.
- `./develop web npm run build` — passed.
- `./install --skip-docker-check --skip-compose-up --hearth-ref T-FR-0004-16-smoke /private/tmp/hearth-t16-install-smoke-feature` — passed.
- Full `./develop web npm run lint` remains blocked by pre-existing non-FR-0004 lint debt in FR-0006 dashboard/shell/theme files; no T16 web source files were touched.

## Suggested next step

Review and merge [PR #56](https://github.com/mcelhennyi/hearth/pull/56). When
it lands on `main`, remove repo-root `CURRENT.md` and refresh `90-closeout.md`
with the merge SHA.

## Options

| Option | When |
|--------|------|
| Merge PR #56 | Human review accepts the completed FR-0004 feature branch. |
| Request changes | Review finds auth UX, trust header, or install-route concerns. |
| Continue next FR | Start FR-0005 while FR-0004 waits in PR review. |
