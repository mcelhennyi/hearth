# FR-0003 — Unpark and start implementation (2026-05-10)

## Summary

Operator requested either (a) split FR-0003 into “do now” vs “wait on FR-0002” with a new FR, or (b) **start FR-0003 now**.

**Outcome:** **No split.** Analysis shows FR-0003 does **not** require FR-0002 to be VAL-complete. Option A (2026-05-09) was **scheduling only**. Hub/Mantle/Compose specifics remain **stubs or fixtures** until FR-0001/FR-0002 artifacts exist — already consistent with [`10-design-00-skeleton.md`](../10-design-00-skeleton.md) and ticket notes.

## Actions taken

- [`REGISTRY.md`](../../REGISTRY.md): FR-0003 → **`in-progress`**.
- Feature branch **`feat/FR-0003-hearth-pi-docker-cli`** with repo-root **`CURRENT.md`**.
- [`tasks/ticket-progress.md`](../../../ticket-progress.md) and [`tasks/handoffs/2026-05-10-fr0003-unpark.md`](../../../handoffs/2026-05-10-fr0003-unpark.md) updated.

## Next agent

1. **[T-FR-0003-01](../tickets.md#t-fr-0003-01--design-contract-amend-deployment-for-docker-on-pi)** — amend **`docs/design/deployment.md`** for the Docker-on-Pi profile, or
2. **`/identify-frontier`** if coordinating with other global tickets.

Historical scheduling note: [`2026-05-09-operator-option-a.md`](2026-05-09-operator-option-a.md).
