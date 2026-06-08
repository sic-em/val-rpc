from __future__ import annotations

import argparse
import time

import requests

from . import config
from .discord_rpc import DiscordPresence
from .lockfile import LockfileNotFound, read_lockfile
from .presence import override_party
from .states import map_state
from .valorant import ValorantClient


def run(
    interval: int = config.POLL_INTERVAL_SECONDS,
    party_size: int | None = None,
    max_party_size: int | None = None,
) -> None:
    discord = DiscordPresence(config.client_id())
    _retry(discord.connect, "Waiting for Discord")
    print("Connected to Discord. Watching VALORANT…")

    client: ValorantClient | None = None
    match_start: float | None = None
    last: tuple | None = None

    while True:
        try:
            if client is None:
                client = ValorantClient(read_lockfile())
            presence = client.fetch_self_presence()
        except LockfileNotFound:
            client, match_start, last = None, None, _idle(discord, last)
            time.sleep(interval)
            continue
        except requests.RequestException:
            client = None  # client API not ready yet; re-read lockfile next tick
            time.sleep(interval)
            continue

        if presence is None:
            last = _idle(discord, last)
            time.sleep(interval)
            continue

        if party_size is not None or max_party_size is not None:
            presence = override_party(presence, party_size, max_party_size)

        in_match = presence.session_loop_state == "INGAME"
        match_start = match_start or time.time() if in_match else None

        state = map_state(presence)
        key = (state, match_start)
        if key != last:
            discord.show(state, start=match_start)
            print(f"→ {state.details} | {state.state}")
            last = key

        time.sleep(interval)


def _idle(discord: DiscordPresence, last: tuple | None) -> None:
    """Clear the presence once when VALORANT is gone"""
    if last is not None:
        discord.clear()
        print("VALORANT closed — cleared presence.")
    return None


def _retry(action, message: str, delay: int = 10) -> None:
    while True:
        try:
            action()
            return
        except Exception:
            print(f"{message}…")
            time.sleep(delay)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="VALORANT Discord Rich Presence")
    parser.add_argument("--party-size", type=int, help="force the shown party count (N)")
    parser.add_argument("--max-party-size", type=int, help="force the shown party cap (M)")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    try:
        run(party_size=args.party_size, max_party_size=args.max_party_size)
    except KeyboardInterrupt:
        print("\nStopped.")
