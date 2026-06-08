from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Lockfile:
    name: str
    pid: int
    port: int
    password: str
    protocol: str

    @property
    def base_url(self) -> str:
        return f"{self.protocol}://127.0.0.1:{self.port}"


def default_lockfile_path() -> Path:
    local = os.environ.get("LOCALAPPDATA", "")
    return Path(local) / "Riot Games" / "Riot Client" / "Config" / "lockfile"


class LockfileNotFound(Exception):
    pass


def read_lockfile(path: Path | None = None) -> Lockfile:
    path = path or default_lockfile_path()
    if not path.exists():
        raise LockfileNotFound(f"lockfile not found at {path} — is VALORANT running?")

    name, pid, port, password, protocol = path.read_text().strip().split(":")
    return Lockfile(
        name=name, pid=int(pid), port=int(port), password=password, protocol=protocol
    )
