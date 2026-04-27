# FR-0001 — ticket DAG

```mermaid
graph TD
  T01[T-FR-0001-01<br/>Repo scaffold &amp; dev loop]
  T02[T-FR-0001-02<br/>Hub API skeleton &amp; SQLite registry]
  T03[T-FR-0001-03<br/>Tinder loader &amp; manifest schema]
  T04[T-FR-0001-04<br/>Mantle PWA shell &amp; iframe embed]
  T05[T-FR-0001-05<br/>Caddy generation &amp; local TLS]
  T06[T-FR-0001-06<br/>Spark v1 broker &amp; client libs]
  T07[T-FR-0001-07<br/>Kindling repo &amp; CLI]
  T08[T-FR-0001-08<br/>groceries reference plugin]
  T09[T-FR-0001-09<br/>Auth, VAPID, Web Push + ntfy]
  T10[T-FR-0001-10<br/>Pi/Mac mini install.sh + backup]

  T01 --> T02
  T01 --> T04
  T01 --> T05
  T02 --> T03
  T02 --> T06
  T03 --> T05
  T04 --> T05
  T03 --> T07
  T04 --> T07
  T06 --> T07
  T07 --> T08
  T02 --> T09
  T04 --> T09
  T05 --> T10
  T08 --> T10
  T09 --> T10
```

Eligibility (a ticket is eligible when all `Deps:` are VAL `done`):

| When… | These become eligible in parallel |
|-------|-----------------------------------|
| `T-FR-0001-01` VAL done | `T-FR-0001-02`, `T-FR-0001-04`, `T-FR-0001-05` |
| `T-FR-0001-02` VAL done | `T-FR-0001-03`, `T-FR-0001-06` |
| `T-FR-0001-03` VAL done | `T-FR-0001-05` (already eligible from T01 too — needs both), `T-FR-0001-07` (needs T03+T04+T06) |
| `T-FR-0001-04`+`-06` VAL done (with `-03`) | `T-FR-0001-07` |
| `T-FR-0001-07` VAL done | `T-FR-0001-08` |
| `T-FR-0001-02`+`-04` VAL done | `T-FR-0001-09` |
| `T-FR-0001-05`+`-08`+`-09` VAL done | `T-FR-0001-10` (closeout) |

Frontier batches (suggested):

1. **T01** (sequential — sets the floor)
2. **T02 ‖ T04 ‖ T05-prep** (Caddy work that doesn't need T03 yet)
3. **T03 ‖ T06**
4. **T05** (finalize once T03 lands)
5. **T07 ‖ T09**
6. **T08**
7. **T10** (closeout)

Dependencies are intentionally generous. The narrowest critical path is T01 → T02 → T03 → T07 → T08 → T10.
