# Spark — app-to-app API

**Authority:** This document defines Spark v1, the only sanctioned channel for inter-plugin traffic in Hearth. Plugins **must not** call each other's HTTP proxy routes directly (Caddy/nginx).

> REWORK-REQUIRED RW-P1 — Wording still says “nginx routes”; **intended state:** “reverse-proxy routes” with Caddy as the default edge per [`deployment.md`](deployment.md).

## Goals

1. **Local-first.** No network hop for two plugins on the same Hearth box.
2. **Typed.** Capabilities are declared in Tinder; methods and event topics are validated.
3. **Observable.** Every call is loggable to the hub's audit trail at `var/hearth/log/spark.jsonl`.
4. **Portable.** Same client API in Python and TypeScript so a plugin can call from server or browser.
5. **Forward-compatible.** Phase 2 swaps the transport for an authenticated cross-host path without breaking plugin code.

## Transport (v1)

- Broker socket: `var/hearth/run/spark.sock` (Unix domain, mode 0660).
- Per-plugin socket: `var/hearth/run/<slug>.sock` (Unix domain, mode 0660).
- Wire format: length-prefixed JSON frames.

```
+-------+-----------------+
| u32 N | N bytes JSON    |
+-------+-----------------+
```

Phase 2 (cross-host via Ember) adds a TLS-wrapped variant with the same JSON envelope, so plugin code is unchanged.

## Frame envelope

```jsonc
{
  "v":   1,
  "id":  "01J0Z…",            // ULID, request/response correlation
  "kind": "call",              // call | reply | error | publish | subscribe | event | ack
  "from": "groceries",         // plugin slug or "hub"
  "to":   "recipes",           // plugin slug for call/reply; topic for publish/event
  "method": "list.items",      // call/reply only
  "topic":  "groceries.list.added",  // publish/event only
  "body":   { /* arbitrary JSON */ },
  "ts":     1730000000.123     // float seconds, server-set on broker hop
}
```

Errors:

```jsonc
{ "v":1, "id":"…", "kind":"error", "code":"PERMISSION_DENIED", "message":"…", "detail":{} }
```

| code | meaning |
|------|---------|
| `UNKNOWN_PLUGIN`        | `to` is not in the registry or not running |
| `UNKNOWN_METHOD`        | method not in target's `capabilities.<surface>.methods` |
| `UNKNOWN_TOPIC`         | topic not in any subscriber's permissions |
| `PERMISSION_DENIED`     | caller's `permissions.spark_call` does not allow |
| `INVALID_BODY`          | target rejected the body (rare; targets may do shape checks) |
| `TIMEOUT`               | target did not reply within `timeout_ms` |
| `INTERNAL`              | catch-all; full trace logged broker-side, message generic |

## Operations

### `call(target, method, body, *, timeout_ms=5000)`
RPC. Caller blocks (or `await`s) until reply or error.

### `publish(topic, body)`
Fire-and-forget. Broker fans out to subscribers whose `permissions.spark_subscribe` matches `topic`.

### `subscribe(topic_pattern, handler)`
Register with broker. Pattern uses `*` as a single-segment wildcard (`groceries.list.*`) and `>` as everything-after (`groceries.>`).

### `unsubscribe(topic_pattern)`
Inverse of `subscribe`.

### `whoami()` / `who_runs(slug)`
Discovery: returns the live capabilities of a plugin (a snapshot of its Tinder `[capabilities.*]`).

## Capability discovery

Capabilities are discovered, not negotiated. The hub holds the canonical list (built from validated Tinder manifests). A plugin asking `spark.who_runs("recipes")` gets back:

```jsonc
{
  "slug": "recipes",
  "version": "0.3.1",
  "capabilities": {
    "list":    { "methods": ["items", "add"], "events": ["added"] },
    "details": { "methods": ["get"],          "events": [] }
  }
}
```

A plugin **may** call methods or subscribe to events not in the surface (e.g. private ones), but the broker rejects them at runtime with `UNKNOWN_METHOD` / `UNKNOWN_TOPIC`. Tinder is the contract.

## Permissions enforcement

Every frame is checked at the broker before it's delivered:

| Check | Source of truth |
|-------|-----------------|
| `from`'s `spark_call` allows `to.method` | Tinder of `from` |
| `from`'s `spark_publish` allows `topic`  | Tinder of `from` |
| Subscriber's `spark_subscribe` allows `topic` | Tinder of the subscriber |
| `to` plugin is `Running`                 | Plugin registry |

Plugins receive an `error` frame on rejection and may log it but **must not** retry indefinitely.

## Client libraries

Both shipped from **Kindling**:

- **Python** — `kindling.spark` — async, mirrors operations 1:1. `await spark.call("recipes", "list.items", {})`.
- **TypeScript** — `@kindling/spark` — usable from a plugin's UI when the plugin proxies through its own backend, **not** directly from browser to broker (browser never speaks Spark).

UI flows look like: browser → plugin's HTTP route → plugin's Python `spark.call(...)` → broker → target plugin.

## Audit log

Broker writes one JSON line per frame to `var/hearth/log/spark.jsonl`:

```jsonc
{"ts":1730000000.123,"id":"01J0Z…","from":"groceries","to":"recipes","kind":"call","method":"list.items","ok":true,"latency_ms":7}
```

Rotated daily; retained 14 days by default. Configurable in hub settings.

## Versioning

- `v: 1` envelope is frozen for FR-0001.
- Adding a new `kind` requires a new `v`. Removing or repurposing fields requires a new major.
- Method-level evolution is the plugin's responsibility (Tinder declares them).

## Widget plugins (deferred)

> DESIGN-GAP DG-S1 — **Widget snapshot RPC:** dashboard widget hosting needs a stable Spark method name (e.g. `widget.snapshot` vs capability-scoped names). Specify in this doc when **P3** widget work is scheduled; see [`dashboard.md`](dashboard.md#widget-plugins-backend-contract-hosting-deferred).

## Phase-2 hooks

When Ember lands, Spark gains:

- `spark.call_remote("<peer-id>/<slug>", method, body)` — TLS-wrapped, e2e-encrypted to a plugin on a different Hearth box.
- A "trusted peers" registry separate from the local plugin registry.

Plugin code does not change for **local** calls.
