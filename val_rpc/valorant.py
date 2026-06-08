"""Local VALORANT client API access (I/O layer)."""

from __future__ import annotations

import requests
import urllib3

from .lockfile import Lockfile
from .presence import Presence

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ValorantClient:
    """Talks to the local Riot Client API exposed via the lockfile."""

    def __init__(self, lockfile: Lockfile, session: requests.Session | None = None) -> None:
        self._lock = lockfile
        self._http = session or requests.Session()
        self._http.auth = ("riot", lockfile.password)
        self._http.verify = False
        self._puuid: str | None = None

    def _get(self, path: str) -> dict:
        resp = self._http.get(f"{self._lock.base_url}{path}", timeout=5)
        resp.raise_for_status()
        return resp.json()

    @property
    def puuid(self) -> str:
        if self._puuid is None:
            self._puuid = self._get("/chat/v1/session")["puuid"]
        return self._puuid

    def fetch_self_presence(self) -> Presence | None:
        """Return the local player's decoded presence, or None if unavailable."""
        for entry in self._get("/chat/v4/presences").get("presences", []):
            if entry.get("puuid") == self.puuid and entry.get("private"):
                return Presence.from_private(entry["private"])
        return None
