"""Print the local player's raw decoded presence — for inspecting fields."""

from __future__ import annotations

import json

from .lockfile import read_lockfile
from .valorant import ValorantClient


def main() -> None:
    raw = ValorantClient(read_lockfile()).fetch_self_raw()
    print(json.dumps(raw, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
