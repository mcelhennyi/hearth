# FR-0007 - Kindling Mantle migration

Move Mantle package ownership out of Hearth and into Kindling so app/plugin repositories can develop standalone from a Kindling dependency while still loading into Hearth as compliant plugins.

## Artifact index

| File | Purpose |
|------|---------|
| [`00-intake.md`](00-intake.md) | Request, success criteria, and scope. |
| [`10-design-00-skeleton.md`](10-design-00-skeleton.md) | Public surfaces and ownership boundary. |
| [`10-design-01-migration-plan.md`](10-design-01-migration-plan.md) | Migration sequence, compatibility, and rollback notes. |
| [`20-tickets-dag.md`](20-tickets-dag.md) | Ticket table and dependency DAG. |
| [`tickets.md`](tickets.md) | Canonical ticket definitions. |
| [`serial-diary.md`](serial-diary.md) | Session log. |

## Current state

FR-0006 created a private `@kindling/mantle` package under Hearth at `packages/mantle/`. FR-0007 makes Kindling the package source of truth and changes Hearth, Kindling templates, and downstream plugin validation so standalone development no longer requires reaching into a Hearth checkout.

## Suggested next step

Run `/identify-frontier`, then start **Contract and transition docs** ([`T-FR-0007-01`](tickets.md#t-fr-0007-01--contract-and-transition-docs)) before moving package files.
