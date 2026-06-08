from __future__ import annotations

import base64
import json
from dataclasses import dataclass


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

    @classmethod
    def from_raw(cls, raw: dict) -> "Presence":
        return cls(
            session_loop_state=raw.get("sessionLoopState", ""),
            provisioning_flow=raw.get("provisioningFlow", ""),
            party_state=raw.get("partyState", ""),
            queue_id=raw.get("queueId", ""),
            match_map=raw.get("partyOwnerMatchMap", "") or raw.get("matchMap", ""),
            current_team=raw.get("partyOwnerMatchCurrentTeam", "") or "",
            ally_score=raw.get("partyOwnerMatchScoreAllyTeam", 0),
            enemy_score=raw.get("partyOwnerMatchScoreEnemyTeam", 0),
            party_size=raw.get("partySize", 1),
            max_party_size=raw.get("maxPartySize", 5),
            party_accessibility=raw.get("partyAccessibility", "CLOSED"),
            is_idle=raw.get("isIdle", False),
            competitive_tier=raw.get("competitiveTier", 0),
        )

    @classmethod
    def from_private(cls, private_b64: str) -> "Presence":
        return cls.from_raw(json.loads(base64.b64decode(private_b64)))
