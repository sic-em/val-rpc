"""Runtime configuration."""

from __future__ import annotations

import os

POLL_INTERVAL_SECONDS = 15

# Discord application ID (public, not a secret). Override with VALRPC_CLIENT_ID.
DEFAULT_CLIENT_ID = "1202725698406453248"


def client_id() -> str:
    return os.environ.get("VALRPC_CLIENT_ID", DEFAULT_CLIENT_ID)
