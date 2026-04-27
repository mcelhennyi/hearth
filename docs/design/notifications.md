# Notifications

**Authority:** This document defines how Hearth delivers notifications to a user's devices in MVP, and the contract plugins use to ask for one.

There are two delivery channels, both visible to plugins through one Spark capability so plugin code does not pick one or the other.

## Channels

### A — Web Push (default, fully integrated)

- Standard W3C Web Push, including iOS 16.4+ for PWAs added to the Home Screen.
- The hub holds the **VAPID keypair** (generated at install, stored in `var/hearth/secrets/vapid.{pub,priv}`).
- The Mantle service worker subscribes via the browser's PushManager and posts the subscription to `POST /api/push/subscribe`. The hub stores it per-device.
- When a notification needs to fire, the hub signs the request with VAPID and POSTs the encrypted payload to the device's push endpoint (`*.push.apple.com`, `fcm.googleapis.com`, etc.). The push service forwards to the device, the SW receives it and calls `self.registration.showNotification(...)`.
- **Outbound internet from the hub is required** — the only outbound path Hearth needs in MVP. (Inbound stays LAN-only until Ember.)

Pre-reqs:

| Pre-req | Where it's enforced |
|---------|---------------------|
| HTTPS for the PWA | Caddy `tls internal` + iPhone CA trust (see `deployment.md`) |
| PWA installed on the phone | "Add to Home Screen" — Mantle prompts |
| User granted notification permission | Mantle's first-run flow asks |
| Hub can reach push providers | Network policy: hub may make outbound HTTPS to `*.push.apple.com`, `fcm.googleapis.com` |

### B — ntfy (hobbyist fallback, optional)

- For users who don't want their hub talking to Apple/Google: install the [ntfy](https://ntfy.sh) iOS app (or self-host an ntfy server) and have the hub post to a private topic.
- The hub holds an ntfy topic name in `hearth.toml`; plugins still call the same Spark capability — the hub picks the channel based on settings.
- ntfy delivers to the OS notification center on iOS without VAPID, push providers, or PWA install. Trade-offs: ntfy notifications open the ntfy app, not Hearth, and grouping/actions are limited.
- Available in MVP because it is cheap and useful while the user gets the PWA + CA-trust dance done.

A user setting picks one or both. "Both" sends Web Push first and falls back to ntfy if the push fails (e.g. device is silent for >24h and the subscription has been pruned).

## Plugin contract

Plugins do not call push providers. They use Spark:

```python
# inside a plugin
await spark.call("hub", "notify.send", {
    "title":   "Eggs are out",
    "body":    "Pantry shows 0 eggs and a recipe scheduled for tonight.",
    "tag":     "groceries.low-stock.eggs",   # de-dupes; latest wins
    "url":     "/groceries/?focus=eggs",      # what to open on tap
    "urgent":  False,                         # iOS interruption level
    "actions": [                              # optional; SW renders buttons
        {"action": "add", "title": "Add to list"},
        {"action": "snooze", "title": "Snooze 1d"}
    ]
})
```

The hub's `notify.send` handler:

1. Looks up the user's enabled channels.
2. For Web Push: fans out to every active subscription, signs each with VAPID, retires subscriptions that come back `410 Gone`.
3. For ntfy: POSTs to the configured topic with appropriate priority headers.
4. Returns `{ok: true, delivered: ["webpush:device-1", "ntfy"]}` or `{ok: false, error}`.

Action click round-trip: the SW posts back to `/api/push/action?tag=…&action=add`; the hub re-publishes a Spark event `notify.action` so the originating plugin can react.

## Tinder permission

Plugins must declare the capability they want:

```toml
[permissions]
spark_call = ["hub.notify.send", "..."]
```

Plugins without this entry cannot send notifications; the broker rejects with `PERMISSION_DENIED`.

## Quiet hours and rate limit (MVP defaults)

- Default quiet hours: 22:00–07:00 local. Non-urgent notifications queue and re-fire at 07:00 collapsed by `tag`.
- Per-tag rate limit: at most 1/hour unless `urgent: true`.
- Both configurable globally in settings; per-plugin overrides are post-MVP.

## Phase-2 hooks

When **Ember** lands, push subscriptions become device-bound (one Hearth identity, multiple devices anywhere). The hub still owns VAPID; Ember just routes the notification through the relay when the device is off-LAN. Plugin code does not change.
