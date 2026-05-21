# Handoff — `/finish-feature` FR-0001 (2026-05-21)

## Executive summary

All **10** `T-FR-0001-xx` tickets are **TEST / DEV / VAL done**. Ticket branches are merged into **`feat/FR-0001-hearth-platform`**. Validation: **238 tests passed** (3 skipped). **[PR #30](https://github.com/mcelhennyi/hearth/pull/30)** is **OPEN** and **MERGEABLE** — not merged to `main` yet.

Since the 2026-05-20 closeout, the feature branch gained **Pi Docker groceries integration**: `hearth --plugin --add` fixes (`groceries.admin`, Dockerfile), generated **`Caddyfile.plugins`**, and Mantle PWA **Workbox `navigateFallbackAllowlist`** so `/groceries/` iframes hit the plugin instead of hub `index.html`.

## Branch state

| Branch | Role |
|--------|------|
| `feat/FR-0001-hearth-platform` | Integration @ `e1daf2e` (+ pending test golden commit) |
| `feat/FR-0001-hearth-platform/T-FR-0001-xx-*` | Audit trail — **not deleted** |

## Validation

```text
./develop test  → 238 passed, 3 skipped
```

## Suggested next step

Merge **PR #30**. After merge: remove **`CURRENT.md`** on `main`, `git pull` on Pi, `hearth pwa build`, clear PWA cache, confirm Groceries tab loads real UI.

## Options

1. **Merge PR #30** — default.
2. **Pi iPhone VAL** — after merge; optional `40-prototype-report` update.
3. **FR-0004** — resume centralized auth after merge + Mantle VAL.
4. **FR-0005** — remote-build / `hearth pwa publish` if deploy velocity is priority.
