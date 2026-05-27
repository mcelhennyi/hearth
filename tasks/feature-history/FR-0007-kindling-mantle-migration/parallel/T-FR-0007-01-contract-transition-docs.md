# T-FR-0007-01 - Contract and transition docs

## 2026-05-27 - Ticket completion

**Branch:** `feat/FR-0007-kindling-mantle-migration-T-FR-0007-01-contract-transition-docs`

**Recap:** Completed the foundation docs contract for moving Mantle ownership from Hearth's temporary FR-0006 `packages/mantle/` package into Kindling. The Kindling satellite design now spells out ownership of source, tests, package metadata, changelog, and release path; Hearth's local submodule/workspace consumption versus pinned CI/production consumption; the rule that plugin repos depend on `@kindling/mantle` instead of Hearth-relative paths; compatibility as a supported Kindling/Mantle version range; and the transitional status of `packages/mantle/`.

**Validation:** `git diff --check` passed. `./develop docs build --strict` is not a valid wrapper invocation in this repo. Direct Docker MkDocs strict build reached the site build but failed on seven pre-existing repo-wide warnings; non-strict Docker MkDocs build passed.

**Next:** Merge this ticket branch into `feat/FR-0007-kindling-mantle-migration`, then rerun `/identify-frontier`. The expected next eligible ticket is `T-FR-0007-02`.
