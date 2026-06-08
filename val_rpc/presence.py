from __future__ import annotations

import base64
import json
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Presence:
    """The fields of the base64 `private` blob that we actually use."""

    session_loop_state: str  # MENUS | PREGAME | INGAME
    provisioning_flow: str  # Matchmaking | CustomGame | SkillTest | ...
    party_state: str  # DEFAULT | MATCHMAKING | ...
    queue_id: str  # competitive | unrated | "" | ...
    match_map: str  # "/Game/Maps/Ascent/Ascent" or ""
    current_team: str  # Blue | Red | ""
    ally_score: int
    enemy_score: int
    party_size: int
    max_party_size: int
    party_accessibility: str  # OPEN | CLOSED
    is_idle: bool
    competitive_tier: int  # 0 = unranked, else tier index (e.g. 24 = Immortal 1)
    player_card_id: str  # equipped player card UUID

    @classmethod
    def from_raw(cls, raw: dict) -> "Presence":
        # Patch 12.10+ nests fields; older patches were flat. Fall back to `raw`.
        match = raw.get("matchPresenceData", raw)
        party = raw.get("partyPresenceData", raw)
        player = raw.get("playerPresenceData", raw)

        return cls(
            session_loop_state=match.get("sessionLoopState", ""),
            provisioning_flow=match.get("provisioningFlow", ""),
            party_state=party.get("partyState", ""),
            queue_id=match.get("queueId", "") or raw.get("queueId", ""),
            match_map=match.get("matchMap", "") or party.get("partyOwnerMatchMap", ""),
            current_team=party.get("partyOwnerMatchCurrentTeam", ""),
            ally_score=party.get("partyOwnerMatchScoreAllyTeam", 0),
            enemy_score=party.get("partyOwnerMatchScoreEnemyTeam", 0),
            party_size=party.get("partySize", 1),
            max_party_size=party.get("maxPartySize", 5),
            party_accessibility=party.get("partyAccessibility", "CLOSED"),
            is_idle=raw.get("isIdle", False),
            competitive_tier=player.get("competitiveTier", 0),
            player_card_id=player.get("playerCardId", ""),
        )

    @classmethod
    def from_private(cls, private_b64: str) -> "Presence":
        return cls.from_raw(json.loads(base64.b64decode(private_b64)))


def override_party(
    p: Presence, size: int | None = None, max_size: int | None = None
) -> Presence:
    """Force the displayed party size. Unset fields keep the real value;
    the current size is clamped so it never exceeds the max."""
    new_max = max_size if max_size is not None else p.max_party_size
    new_size = size if size is not None else p.party_size
    return replace(p, party_size=min(new_size, new_max), max_party_size=new_max)
