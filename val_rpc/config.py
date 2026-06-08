"""Runtime configuration."""

from __future__ import annotations

import os

POLL_INTERVAL_SECONDS = 15


def client_id() -> str:
    cid = os.environ.get("VALRPC_CLIENT_ID")
    if not cid:
        raise SystemExit(
            "Set VALRPC_CLIENT_ID to your Discord application ID "
            "(https://discord.com/developers/applications)."
        )
    return cid
