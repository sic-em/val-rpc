from __future__ import annotations

import time

import requests

from . import config
from .discord_rpc import DiscordPresence
from .lockfile import LockfileNotFound, read_lockfile
from .states import map_state
from .valorant import ValorantClient


def run(interval: int = config.POLL_INTERVAL_SECONDS) -> None:
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


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nStopped.")
