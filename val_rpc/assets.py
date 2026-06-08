"""Static lookups: names + valorant-api.com image URLs (no I/O).

Discord renders external image URLs directly, so every image is a CDN URL —
nothing needs to be uploaded to the Discord application's art assets.
"""

from __future__ import annotations

CDN = "https://media.valorant-api.com"
COMPETITIVE_TIERS_UUID = "03621f52-342b-cf4e-4f86-9350a49c6d04"

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

# internal map path -> (display name, uuid) from valorant-api.com
MAPS: dict[str, tuple[str, str]] = {
    "/Game/Maps/Ascent/Ascent": ("Ascent", "7eaecc1b-4337-bbf6-6ab9-04b8f06b3319"),
    "/Game/Maps/Bonsai/Bonsai": ("Split", "d960549e-485c-e861-8d71-aa9d1aed12a2"),
    "/Game/Maps/Canyon/Canyon": ("Fracture", "b529448b-4d60-346e-e89e-00a4c527a405"),
    "/Game/Maps/Duality/Duality": ("Bind", "2c9d57ec-4431-9c5e-2939-8f9ef6dd5cba"),
    "/Game/Maps/Foxtrot/Foxtrot": ("Breeze", "2fb9a4fd-47b8-4e7d-a969-74b4046ebd53"),
    "/Game/Maps/Infinity/Infinity": ("Abyss", "224b0a95-48b9-f703-1bd8-67aca101a61f"),
    "/Game/Maps/Jam/Jam": ("Lotus", "2fe4ed3a-450a-948b-6d6b-e89a78e680a9"),
    "/Game/Maps/Juliett/Juliett": ("Sunset", "92584fbe-486a-b1b2-9faa-39b0f486b498"),
    "/Game/Maps/Pitt/Pitt": ("Pearl", "fd267378-4d1d-484f-ff52-77821ed10dc2"),
    "/Game/Maps/Port/Port": ("Icebox", "e2ad5c54-4114-a870-9641-8ea21279579a"),
    "/Game/Maps/Rook/Rook": ("Corrode", "1c18ab1f-420d-0d8b-71d0-77ad3c439115"),
    "/Game/Maps/Triad/Triad": ("Haven", "2bee0dc9-4ffe-519b-1cbd-7fbe763a6047"),
    "/Game/Maps/HURM/HURM_Alley/HURM_Alley": ("District", "690b3ed2-4dff-945b-8223-6da834e30d24"),
    "/Game/Maps/HURM/HURM_Bowl/HURM_Bowl": ("Kasbah", "12452a9d-48c3-0b02-e7eb-0381c3520404"),
    "/Game/Maps/HURM/HURM_Helix/HURM_Helix": ("Drift", "2c09d728-42d5-30d8-43dc-96a05cc7ee9d"),
    "/Game/Maps/HURM/HURM_HighTide/HURM_HighTide": ("Glitch", "d6336a5a-428f-c591-98db-c8a291159134"),
    "/Game/Maps/HURM/HURM_Yard/HURM_Yard": ("Piazza", "de28aa9b-4cbe-1003-320e-6cb3ec309557"),
    "/Game/Maps/Poveglia/Range": ("The Range", "ee613ee9-28b7-4beb-9666-08db13bb2244"),
    "/Game/Maps/PovegliaV2/RangeV2": ("The Range", "5914d1e0-40c4-cfdd-6b88-eba06347686c"),
}

# queueId -> game mode icon uuid (several queues share the Standard icon)
_STANDARD = "96bd3920-4f36-d026-2b28-c683eb0bcac5"
MODE_UUIDS: dict[str, str] = {
    "competitive": _STANDARD,
    "unrated": _STANDARD,
    "swiftplay": _STANDARD,
    "newmap": _STANDARD,
    "": _STANDARD,
    "spikerush": "e921d1e6-416b-c31f-1291-74930c330b7b",
    "deathmatch": "a8790ec5-4237-f2f0-e93b-08a8e89865b2",
    "ggteam": "a4ed6518-4741-6dcb-35bd-f884aecdc859",
    "hurm": "e086db66-47fd-e791-ca81-06a645ac7661",
    "onefa": "4744698a-4513-dc96-9c22-a9aa437e4a58",
    "snowball": "57038d6d-49b1-3a74-c5ef-3395d9f23a97",
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

# Fallback when no map/card context (only image uploaded to the Discord app).
LOGO_KEY = "valorant"


def queue_name(queue_id: str) -> str:
    return QUEUE_NAMES.get(queue_id, queue_id.capitalize() or "Custom")


def map_name(map_path: str) -> str:
    if map_path in MAPS:
        return MAPS[map_path][0]
    # Unknown / new map: fall back to the last path segment.
    return map_path.rsplit("/", 1)[-1] if map_path else ""


def map_image(map_path: str) -> str:
    """Map splash URL, or the logo fallback when no map is set."""
    if map_path in MAPS:
        return f"{CDN}/maps/{MAPS[map_path][1]}/splash.png"
    return LOGO_KEY


def mode_image(queue_id: str) -> str:
    """Game mode icon URL."""
    return f"{CDN}/gamemodes/{MODE_UUIDS.get(queue_id, _STANDARD)}/displayicon.png"


def rank_name(tier: int) -> str:
    return RANK_NAMES.get(tier, "Unranked")


def rank_image(tier: int) -> str:
    """Rank tier icon URL."""
    return f"{CDN}/competitivetiers/{COMPETITIVE_TIERS_UUID}/{tier}/largeicon.png"


def player_card_image(card_id: str) -> str:
    """Equipped player card square art URL."""
    return f"{CDN}/playercards/{card_id}/smallart.png"
