# UI design HTML mocks

Mirrors **`.cursor/rules/ui-design-mockups.mdc`**. Keep both files aligned.

## Required before UI implementation

When the user asks to **create or update UI design** — screens, flows, layout, chrome, plugin surfaces, dashboard tiles, or any **visible** behavior in **`docs/design/`** — produce **static HTML mockups** that convey the **exact look and feel** **before** React/Mantle/app implementation or UI **DEV** tickets.

**Authority split:** **`docs/design/…` markdown** = logical (behavior, contracts). **`docs/design/mockups/`** HTML/CSS = layout and visual design language. Link mocks from design docs; **no ASCII layout diagrams** in markdown for spatial reference.

### Deliverables

1. **HTML** under **`docs/design/mockups/`** (browser-openable; desktop + phone variants when responsive behavior matters; shared **`.css`** when reused).
2. **Link** mocks from the owning **`docs/design/…`** doc; maintain **`docs/design/mockups/README.md`** index.
3. Then tickets / implementation.

### Exemptions

Non-UI-only design, prose-only edits, or an **explicit** user waiver documented in intake/diary.

### Audit / feature-request

- **`/audit-design`:** visible UI without mocks → not ticket-ready.
- **`/feature-request` Stages 1..N:** complete mocks (or documented waiver) before UI-leaning tickets.

See **`docs/design/documentation-style.md`** and **`feature-request`** skill.
