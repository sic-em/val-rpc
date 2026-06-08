"""Static lookups: queue names, map names, Discord asset keys (no I/O)."""

from __future__ import annotations

# queueId -> human display name
QUEUE_NAMES: dict[str, str] = {
    "competitive": "Competitive",
    "unrated": "Unrated",
    "swiftplay": "Swiftplay",
    "spikerush": "Spike Rush",
    "deathmatch": "Deathmatch",
    "ggteam": "Escalation",
    "hurm": "Team Deathmatch",
    "onefa": "Replication",
    "snowball": "Snowball Fight",
    "newmap": "New Map",
    "": "Custom",
}

# internal map path -> display name (from valorant-api.com)
MAP_NAMES: dict[str, str] = {
    "/Game/Maps/Ascent/Ascent": "Ascent",
    "/Game/Maps/Bonsai/Bonsai": "Split",
    "/Game/Maps/Canyon/Canyon": "Fracture",
    "/Game/Maps/Duality/Duality": "Bind",
    "/Game/Maps/Foxtrot/Foxtrot": "Breeze",
    "/Game/Maps/Infinity/Infinity": "Abyss",
    "/Game/Maps/Jam/Jam": "Lotus",
    "/Game/Maps/Juliett/Juliett": "Sunset",
    "/Game/Maps/Pitt/Pitt": "Pearl",
    "/Game/Maps/Port/Port": "Icebox",
    "/Game/Maps/Rook/Rook": "Corrode",
    "/Game/Maps/Triad/Triad": "Haven",
    "/Game/Maps/HURM/HURM_Alley/HURM_Alley": "District",
    "/Game/Maps/HURM/HURM_Bowl/HURM_Bowl": "Kasbah",
    "/Game/Maps/HURM/HURM_Helix/HURM_Helix": "Drift",
    "/Game/Maps/HURM/HURM_HighTide/HURM_HighTide": "Glitch",
    "/Game/Maps/HURM/HURM_Yard/HURM_Yard": "Piazza",
    "/Game/Maps/Poveglia/Range": "The Range",
    "/Game/Maps/PovegliaV2/RangeV2": "The Range",
}

# competitive tier index -> rank display name
RANK_NAMES: dict[int, str] = {
    0: "Unranked",
    3: "Iron 1", 4: "Iron 2", 5: "Iron 3",
    6: "Bronze 1", 7: "Bronze 2", 8: "Bronze 3",
    9: "Silver 1", 10: "Silver 2", 11: "Silver 3",
    12: "Gold 1", 13: "Gold 2", 14: "Gold 3",
    15: "Platinum 1", 16: "Platinum 2", 17: "Platinum 3",
    18: "Diamond 1", 19: "Diamond 2", 20: "Diamond 3",
    21: "Ascendant 1", 22: "Ascendant 2", 23: "Ascendant 3",
    24: "Immortal 1", 25: "Immortal 2", 26: "Immortal 3",
    27: "Radiant",
}

# Discord Rich Presence asset keys (names of images uploaded to the Discord app)
LOGO_KEY = "valorant"


def queue_name(queue_id: str) -> str:
    return QUEUE_NAMES.get(queue_id, queue_id.capitalize() or "Custom")


def map_name(map_path: str) -> str:
    if map_path in MAP_NAMES:
        return MAP_NAMES[map_path]
    # Unknown / new map: fall back to the last path segment.
    return map_path.rsplit("/", 1)[-1] if map_path else ""


def map_asset_key(map_path: str) -> str:
    """Asset image key for a map, e.g. 'map_ascent'. Falls back to the logo."""
    name = map_name(map_path)
    return f"map_{name.lower().replace(' ', '_')}" if name else LOGO_KEY


def mode_asset_key(queue_id: str) -> str:
    """Asset image key for a game mode icon, e.g. 'mode_competitive'."""
    return f"mode_{queue_id}" if queue_id else "mode_custom"


def rank_name(tier: int) -> str:
    return RANK_NAMES.get(tier, "Unranked")


def rank_asset_key(tier: int) -> str:
    """Asset image key for a rank tier icon, e.g. 'rank_19'."""
    return f"rank_{tier}"


def player_card_image(card_id: str) -> str:
    """External CDN URL for the equipped player card's tall art."""
    return f"https://media.valorant-api.com/playercards/{card_id}/largeart.png"
