# Handoff — FR-0001 merged to `main` (2026-05-21)

## Executive summary

[**PR #30**](https://github.com/mcelhennyi/hearth/pull/30) merged **`feat/FR-0001-hearth-platform`** into **`main`** at **`0811ed27304dc76b9e4a98bf8ed8b568dcdf7196`**. Post-merge closeout removed repo-root **`CURRENT.md`** (feature-branch artifact; must not stay on `main`).

## Validation at merge

- **238** tests passed on the feature branch before merge (3 skipped).
- Pi operator path: groceries proxy + PWA SW allowlist included in merge.

## Suggested next step

Pi: `git pull` on `main`, `hearth pwa build`, `hearth restart caddy`, confirm Groceries UI in hub tab. Then resume **FR-0004** or start **FR-0005** ticketing.

## Options

| Option | When |
|--------|------|
| Pi + iPhone VAL | Groceries tab, push, cert — optional session |
| **FR-0004** | Set `in-progress` in `REGISTRY.md` and staff `T-FR-0004-02` |
| **FR-0005** | Remote-build profile if deploy velocity wins |

## Audit

- **Merge:** `0811ed2` — 2026-05-21T04:57:52Z
- **Closeout:** [`90-closeout.md`](../90-closeout.md)
- **Pre-merge handoff:** [`2026-05-21-finish-feature.md`](2026-05-21-finish-feature.md)
