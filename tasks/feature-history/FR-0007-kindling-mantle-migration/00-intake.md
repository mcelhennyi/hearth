# FR-0007 - Intake

| Field | Value |
|------|--------|
| **Title** | Kindling Mantle migration |
| **Requester** | Ian |
| **Target timeline** | Next cross-repo packaging slice after FR-0006 and before relying on standalone plugin development for Planwright-style apps. |
| **Constraints** | Hearth remains canonical deployment host; standalone app development must not depend on a Hearth checkout; app/plugin compliance is expressed by supported Kindling/Mantle package versions; avoid copying Mantle into plugin repos. |
| **Success definition** | 1. Kindling owns the Mantle package source and release/changelog surface. 2. Hearth consumes Mantle from Kindling/package resolution rather than `packages/mantle` as the authoritative source. 3. Generated or existing Kindling-based apps can run standalone and load in Hearth by pinning a compatible `@kindling/mantle` version. |
| **Out of scope** | Redesigning Mantle UI, changing plugin iframe policy, or making Kindling an alternative Hearth host. |
| **Links** | [`docs/design/satellite-repos/kindling.md`](../../../docs/design/satellite-repos/kindling.md), [`FR-0006`](../FR-0006-design-language/README.md), Kindling [`mantle/`](../../../kindling/mantle) |

**Raw details**:

Move the Mantle elements into Kindling, so a Kindling-based app can easily develop standalone from the Hearth project, but when loaded as a plugin it can be compliant by just supporting the correct version of Kindling as a dependency.
