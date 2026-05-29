# T-FR-0007-04 - Standalone Kindling app template support

## 2026-05-29 - Ticket completion

**Branch:** `feat/FR-0007-kindling-mantle-migration-T-FR-0007-04-standalone-kindling-template`

**Kindling branch:** `feat/FR-0007-standalone-kindling-template`

**TEST:** Rendered `kindling new standalone-demo --template react` inside the Docker Python test container, then ran generated-app `npm install --no-package-lock` inside the Docker Node tooling container. It failed with `npm ERR! 404 '@kindling/mantle@^0.1.0' is not in this registry`, proving the generated React template could not install standalone while Mantle is Kindling-local and unpublished.

**DEV:** Updated Kindling's React template renderer to resolve local `kindling/mantle/` when present. Rendered React templates now keep the canonical package name `@kindling/mantle`, depend on the local Kindling Mantle package through a generated `file:` dependency, and run a generated `preinstall` harness that installs/builds local Mantle before the app installs. The sample React app imports Mantle token/component CSS and wraps Mantle hooks below `MantleProvider` so standalone mode renders with a `standalone` theme fallback while plugin mode still receives Hearth bridge messages.

**VAL:** All installs/tests/builds ran inside Docker:

- `docker compose -f deploy/compose/docker-compose.yml run --rm --no-deps hearth-test kindling/scripts/tests/test_plugin_templates.py` — `5 passed, 1 skipped`.
- Rendered `standalone-demo` via the Docker Python test container.
- `docker compose -f deploy/compose/docker-compose.yml run --rm --no-deps web sh -lc 'cd /workspace/.tmp/t04-val/standalone-demo && npm install --no-package-lock && npm run typecheck && npm run build'` — local Mantle build succeeded, generated app typecheck passed, Vite build emitted `web/dist/`.

**Notes:** The generated app install reported two moderate npm audit findings in transitive frontend tooling; no audit fix was applied because this ticket is limited to Kindling template/standalone wiring.

**Next:** Merge this ticket branch into `feat/FR-0007-kindling-mantle-migration` after the parallel frontier owner reconciles T03/T04 shared files. `T-FR-0007-05` becomes eligible once T04 is merged and T03 remains independent for Hearth consumption wiring.
