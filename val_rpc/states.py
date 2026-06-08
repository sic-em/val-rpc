from __future__ import annotations

from dataclasses import dataclass

from .assets import (
    LOGO_KEY,
    map_asset_key,
    map_name,
    mode_asset_key,
    player_card_image,
    queue_name,
    rank_asset_key,
    rank_name,
)
from .presence import Presence

_RANGE_FLOWS = {"ShootingRange", "SkillTest"}


def _small(p: Presence) -> tuple[str, str]:
    """Small image + text: rank in ranked queues, otherwise the mode icon."""
    if p.queue_id == "competitive" and p.competitive_tier > 0:
        return rank_asset_key(p.competitive_tier), rank_name(p.competitive_tier)
    return mode_asset_key(p.queue_id), queue_name(p.queue_id)


def _menu_large(p: Presence) -> str:
    """Menu background: the player's equipped card, falling back to the logo."""
    return player_card_image(p.player_card_id) if p.player_card_id else LOGO_KEY


@dataclass(frozen=True)
class RpcState:
    details: str
    state: str
    large_image: str
    large_text: str = "VALORANT"
    small_image: str | None = None
    small_text: str | None = None


def map_state(p: Presence) -> RpcState:
    if p.session_loop_state == "INGAME":
        return _ingame(p)
    if p.session_loop_state == "PREGAME":
        return _agent_select(p)
    return _menus(p)


def _menus(p: Presence) -> RpcState:
    if p.provisioning_flow in _RANGE_FLOWS:
        return RpcState(details="The Range", state="Practice", large_image=LOGO_KEY)

    small_image, small_text = _small(p)
    if p.party_state == "MATCHMAKING":
        return RpcState(
            details=queue_name(p.queue_id),
            state=f"In Queue · {p.party_size} of {p.max_party_size}",
            large_image=_menu_large(p),
            small_image=small_image,
            small_text=small_text,
        )

    party = "Idle" if p.is_idle else f"Party · {p.party_size} of {p.max_party_size}"
    return RpcState(
        details=f"Main Menu · {queue_name(p.queue_id)}",
        state=party,
        large_image=_menu_large(p),
        small_image=small_image,
        small_text=small_text,
    )


def _agent_select(p: Presence) -> RpcState:
    where = f"Agent Select · {map_name(p.match_map)}" if p.match_map else "Agent Select"
    small_image, small_text = _small(p)
    return RpcState(
        details=queue_name(p.queue_id),
        state=where,
        large_image=map_asset_key(p.match_map),
        small_image=small_image,
        small_text=small_text,
    )


def _ingame(p: Presence) -> RpcState:
    mode = (
        "Custom Game" if p.provisioning_flow == "CustomGame" else queue_name(p.queue_id)
    )
    mp = map_name(p.match_map)
    small_image, small_text = _small(p)
    return RpcState(
        details=f"{mode} · {mp}" if mp else mode,
        state=f"{p.ally_score} : {p.enemy_score}",
        large_image=map_asset_key(p.match_map),
        small_image=small_image,
        small_text=small_text,
    )
