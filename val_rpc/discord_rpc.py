"""Push a RpcState to Discord via pypresence (I/O layer)."""

from __future__ import annotations

from pypresence import Presence as _RPC

from .states import RpcState


class DiscordPresence:
    """Thin wrapper over pypresence that speaks RpcState."""

    def __init__(self, client_id: str) -> None:
        self._rpc = _RPC(client_id)

    def connect(self) -> None:
        self._rpc.connect()

    def show(self, state: RpcState, start: float | None = None) -> None:
        self._rpc.update(
            details=state.details,
            state=state.state,
            large_image=state.large_image,
            large_text=state.large_text,
            small_image=state.small_image,
            small_text=state.small_text,
            start=start,
        )

    def clear(self) -> None:
        self._rpc.clear()

    def close(self) -> None:
        self._rpc.close()
