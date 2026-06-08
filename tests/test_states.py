import base64
import json

from val_rpc.presence import Presence
from val_rpc.states import map_state


def presence(**fields) -> Presence:
    blob = base64.b64encode(json.dumps(fields).encode()).decode()
    return Presence.from_private(blob)


def test_lobby():
    s = map_state(presence(sessionLoopState="MENUS", queueId="competitive", partySize=2, maxPartySize=5))
    assert s.details == "Main Menu · Competitive"
    assert s.state == "Party · 2 of 5"
    assert s.large_image == "valorant"  # no player card -> logo fallback


def test_idle_lobby():
    s = map_state(presence(sessionLoopState="MENUS", queueId="unrated", isIdle=True))
    assert s.state == "Idle"


def test_queue():
    s = map_state(presence(sessionLoopState="MENUS", partyState="MATCHMAKING",
                           queueId="competitive", partySize=5, maxPartySize=5))
    assert s.details == "Competitive"
    assert s.state == "In Queue · 5 of 5"
    assert s.small_image.endswith("/gamemodes/96bd3920-4f36-d026-2b28-c683eb0bcac5/displayicon.png")


def test_range():
    s = map_state(presence(sessionLoopState="MENUS", provisioningFlow="ShootingRange"))
    assert s.details == "The Range"


def test_agent_select():
    s = map_state(presence(sessionLoopState="PREGAME", queueId="competitive",
                           partyOwnerMatchMap="/Game/Maps/Ascent/Ascent"))
    assert s.details == "Competitive"
    assert s.state == "Agent Select · Ascent"
    assert s.large_image.endswith("/maps/7eaecc1b-4337-bbf6-6ab9-04b8f06b3319/splash.png")


def test_ingame_competitive():
    s = map_state(presence(sessionLoopState="INGAME", queueId="competitive",
                           partyOwnerMatchMap="/Game/Maps/Triad/Triad",
                           partyOwnerMatchScoreAllyTeam=7, partyOwnerMatchScoreEnemyTeam=5))
    assert s.details == "Competitive · Haven"
    assert s.state == "7 : 5"
    assert s.large_image.endswith("/maps/2bee0dc9-4ffe-519b-1cbd-7fbe763a6047/splash.png")


def test_ingame_tdm_hurm_map():
    s = map_state(presence(sessionLoopState="INGAME", queueId="hurm",
                           partyOwnerMatchMap="/Game/Maps/HURM/HURM_Yard/HURM_Yard"))
    assert s.details == "Team Deathmatch · Piazza"


def test_ingame_custom():
    s = map_state(presence(sessionLoopState="INGAME", provisioningFlow="CustomGame",
                           queueId="", partyOwnerMatchMap="/Game/Maps/Bonsai/Bonsai"))
    assert s.details == "Custom Game · Split"


def test_unknown_map_falls_back_to_segment():
    s = map_state(presence(sessionLoopState="INGAME", queueId="unrated",
                           partyOwnerMatchMap="/Game/Maps/Future/Future"))
    assert s.details == "Unrated · Future"


def test_competitive_shows_rank_small_image():
    s = map_state(presence(sessionLoopState="MENUS", queueId="competitive",
                           competitiveTier=19))
    assert s.small_image.endswith("/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/19/largeicon.png")
    assert s.small_text == "Diamond 2"


def test_unranked_competitive_shows_mode_icon():
    s = map_state(presence(sessionLoopState="MENUS", queueId="competitive",
                           competitiveTier=0))
    assert s.small_image.endswith("/gamemodes/96bd3920-4f36-d026-2b28-c683eb0bcac5/displayicon.png")


def test_player_card_is_menu_large_image():
    s = map_state(presence(sessionLoopState="MENUS", queueId="unrated",
                           playerCardId="abc-123"))
    assert s.large_image == "https://media.valorant-api.com/playercards/abc-123/smallart.png"


def test_nested_schema_parsing():
    # Patch 12.10+ nests fields under *PresenceData objects.
    s = map_state(Presence.from_raw({
        "isIdle": False,
        "matchPresenceData": {"sessionLoopState": "MENUS", "queueId": "competitive",
                              "provisioningFlow": "Invalid", "matchMap": ""},
        "partyPresenceData": {"partyState": "DEFAULT", "partySize": 1, "maxPartySize": 5},
        "playerPresenceData": {"competitiveTier": 19, "playerCardId": "card-9"},
    }))
    assert s.details == "Main Menu · Competitive"
    assert s.small_image.endswith("/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/19/largeicon.png")
    assert s.large_image.endswith("/playercards/card-9/smallart.png")
