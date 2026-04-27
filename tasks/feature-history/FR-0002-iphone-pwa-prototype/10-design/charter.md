# FR-0002 — charter

## What we are buying with this FR

Time. Specifically, the time we'd otherwise spend building the plugin loader, Tinder schema, Spark broker, and Kindling split before discovering one of the five iPhone-PWA risks bites us.

The reason FR-0001 has ten tickets is that the platform is real. The reason we don't start with `T-FR-0001-01` is that *every* FR-0001 ticket assumes the iPhone PWA story works. If `tls internal` certs fail on iOS Safari, every Mantle test we write is wrong; if Web Push doesn't reach the iPhone from a Pi behind a home router, the `notify.send` capability is theatre. We pay one feature's worth of effort to find out, then resume FR-0001 with calibrated assumptions.

## What "succeed" means

Concretely, the same five-step demo from FR-0002's README runs on a real iPhone, end-to-end, on Mac mini and on Pi 4, with a written record of every friction point. *Succeed* does **not** mean "everything was clean" — it means we can answer **yes/no** to each of the five risks and either:

- continue FR-0001 unchanged, or
- amend FR-0001 docs (`mantle-ui.md`, `deployment.md`, `notifications.md`) per the `docs/ai-context.md` amendment process and then continue.

## What "fail" looks like

If a risk turns out to be unmovable inside reasonable scope (e.g. iOS Safari refuses to register an SW served from a `tls internal` cert no matter what we do), the FR-0002 closeout produces a recommendation to redesign the relevant FR-0001 piece — for example, switching to a Tailscale-issued cert, or moving the iPhone to use Ember from day-one. That's a **DESIGN-FLAW** against FR-0001 and goes through the amendment process before FR-0001 work resumes.

## What we are intentionally not doing

- Building anything that won't be reused. The static Mantle shell, VAPID handling, and Caddy config from this FR feed directly into FR-0001 tickets `T-FR-0001-04`, `T-FR-0001-05`, and `T-FR-0001-09`.
- Time-boxing. The point is to learn, not to look fast. The closeout report is the deliverable, not "we shipped it in a weekend."
- Generalizing. The shell has bottom tabs that go nowhere; the test-notification button is a button. No plugin loader, no Tinder, no Spark.
