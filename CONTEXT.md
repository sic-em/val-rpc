# Context

Glossary of domain terms for val-rpc. Definitions only — no implementation detail.

## Terms

**Party size** — shown as `N of M`.
- `N` (current size): how many players are in the party right now.
- `M` (max size): the party's capacity for the current queue.
Sourced from the presence as `partySize` / `maxPartySize`.

**Party size override** — a user-supplied `N` and/or `M` that replaces the real
values for display only. The real party is unchanged; only what Discord shows
differs. `N` is clamped so it never exceeds `M`.

**State** — what Discord displays for one moment of play, derived from the
presence. One of: In Lobby, In Queue, Agent Select, In Game, The Range.
Determined by `sessionLoopState` × `provisioningFlow` × `queueId`.
