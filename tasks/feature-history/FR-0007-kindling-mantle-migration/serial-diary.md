# FR-0007 - Serial diary

## 2026-05-27 (session) - Codex

**Stage:** intake, design skeleton, tickets

**Recap (plain English):** Allocated FR-0007 for moving Mantle ownership into Kindling. The key decision is that Hearth remains the canonical host, while Kindling becomes the package/source owner for `@kindling/mantle`; standalone app repos should depend on a compatible Kindling/Mantle version rather than importing from Hearth paths. Split implementation into six tickets: **Contract and transition docs** ([T-FR-0007-01](tickets.md#t-fr-0007-01--contract-and-transition-docs)), **Move Mantle package source to Kindling** ([T-FR-0007-02](tickets.md#t-fr-0007-02--move-mantle-package-source-to-kindling)), **Rewire Hearth to consume Kindling Mantle** ([T-FR-0007-03](tickets.md#t-fr-0007-03--rewire-hearth-to-consume-kindling-mantle)), **Standalone Kindling app template support** ([T-FR-0007-04](tickets.md#t-fr-0007-04--standalone-kindling-app-template-support)), **Mantle version compliance validation** ([T-FR-0007-05](tickets.md#t-fr-0007-05--mantle-version-compliance-validation)), and **Downstream app proof and migration note** ([T-FR-0007-06](tickets.md#t-fr-0007-06--downstream-app-proof-and-migration-note)).

**Validation:** `git diff --check` passed. `./develop build` is not available in this repo. Docker `mkdocs build --strict` reached the build but failed on seven pre-existing warnings outside this FR; non-strict Docker `mkdocs build` passed.
