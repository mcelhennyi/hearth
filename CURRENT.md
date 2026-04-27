## Current Branch

- Branch: `feat/FR-0002-iphone-pwa-prototype-T-FR-0002-03-web-push`
- Status: `complete`
- Parent integration branch: `feat/FR-0002-iphone-pwa-prototype`
- Ticket: `T-FR-0002-03` (Web Push round-trip)

## TEST / DEV / VAL Outcome

- TEST: Added API tests in `apps/hub/api/tests/` for VAPID deterministic-claims validation, `410 Gone` pruning, and integration-level `/api/push/test` behavior with mocked `pywebpush`.
- DEV: Implemented FastAPI at `apps/hub/api/` (`/api/health`, `/api/push/subscribe`, `/api/push/test`), VAPID generator at `scripts/gen-vapid.py`, Caddy `/api/*` proxying, and Mantle UI + SW push handling.
- VAL: Containerized commands passed:
  - `./develop api pytest`
  - `./develop web npm run test`
  - `./develop web npm run lint`
  - `./develop web npm run build`
  - `./develop vapid-gen`
  - `./develop up -d && curl -sk --resolve hearth.local:443:127.0.0.1 https://hearth.local/api/health && ./develop down`

## Context Carryover

- `T-FR-0002-01` and `T-FR-0002-02` are already merged in the feature branch.
- This branch uses the hyphenated ticket suffix because slash-ref namespace is occupied by `feat/FR-0002-iphone-pwa-prototype`.
