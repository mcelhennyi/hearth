# Documentation style

Conventions for **documentation** and **traceability**. **Stack-specific** rules (language formatters, frameworks) live in **`.cursor/rules/stack-conventions.mdc`** once defined.

## Authority

- **`docs/design/`** is authoritative for behavior and architecture **when those documents exist**. If code and docs disagree, **fix the code** unless the design is provably wrong — then use the amendment process in **`docs/ai-context.md`** (`DESIGN-GAP`, `DESIGN-FLAW`, `CODE-DEFECT`).

## Traceability

- Non-trivial units (services, modules, handlers) carry **`@PROJ-<AREA>-<NUMBER>`** in a short comment or docstring **for stacks where inline tags make sense**.
- Replace **`PROJ`** with your project prefix (set during **`init-project`**).
- **Areas:** define a small set for your product (examples: `API`, `AUTH`, `DATA`, `UI`, `JOB`).

## Ticket IDs (map to `FR-NNNN`)

Implementation ticket **definitions** (headings, phases, **Deps:**) live in **`tasks/feature-history/FR-NNNN-<slug>/tickets.md`**. **`tasks/ticket-progress.md`** tracks **TEST / DEV / VAL** for each id. **`docs/design/tickets-initial.md`** is the **global index + DAG** (links and mermaid), not the home for **`###`** ticket sections.

| Part | Meaning |
|------|---------|
| **`T-`** | Literal prefix (implementation ticket). |
| **`FR-NNNN`** | Four-digit feature id as in **`tasks/feature-history/REGISTRY.md`**. |
| **`-xx`** | Two-digit sequence within that feature (`01`, `02`, …). |

**Full id:** **`T-FR-NNNN-xx`**.

**Reserved:** **`FR-0000`** — repository / platform bootstrap; starter definitions may live in **`tasks/feature-history/FR-0000-bootstrap/tickets.md`**.

**Branches / worktrees:** Prefer slugs that include the full ticket id, e.g. **`feat/T-FR-0007-01-auth-api`**, worktree **`worktrees/T-FR-0007-01-auth-api/`**.

**`Deps:`** list other tickets by **full id** or `none`.

**Mermaid triad nodes:** For **`T-FR-NNNN-xx`**, node ids **`TFR` + `NNNN` + `_` + `xx` + `_` + `TEST|DEV|VAL`**. When a ticket is fully complete, add the corresponding `class … triadDone` line in **`docs/design/tickets-initial.md`** (see that file).

## Writing rules for Cursor / Claude

1. **Prefer pointers over duplication** — Link to `docs/design/...` instead of restating full diagrams in tickets.
2. **Tables for conventions** — When listing options, use markdown tables.
3. **Mermaid for architecture** — Use `mermaid` blocks for graphs; keep diagrams **small** and versioned with the owning doc.
4. **No scope creep in comments** — Comments summarize; design decisions live in `docs/design/`.
5. **Amendments** — Use the HTML comment block format from **`docs/ai-context.md`** when revising authoritative sections.

## Code tie-backs

- Link from code to **`docs/design/...`** where behavior is specified.
- Do not embed secrets or customer-specific data in examples committed to git.
