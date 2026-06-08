# val-rpc

Discord Rich Presence for VALORANT. Reads the local Riot Client **lockfile** API on
Windows, decodes the player's presence, and mirrors it to your Discord profile.

## Architecture (layered, one concern per module)

```
lockfile.py    read the Riot lockfile        -> Lockfile (host/port/password)
valorant.py    local client API I/O          -> Presence
presence.py    decode the base64 `private`    (pure)
assets.py      queue/map names + asset keys   (pure)
states.py      Presence -> RpcState           (pure, the core — fully tested)
discord_rpc.py push RpcState via pypresence   (I/O)
main.py        poll loop wiring it together
```

The mapping (`states.py`) is pure and unit-tested, so behaviour is verifiable on any
machine without VALORANT running (`pytest`).

## Setup

Images are served directly from `media.valorant-api.com` (maps, modes, ranks,
player cards) — Discord renders external URLs, so **no art assets need uploading**.
The only uploaded asset is an optional `valorant` logo used as a last-resort
fallback. The Discord application ID is baked into `config.py`
(override with `VALRPC_CLIENT_ID`).

On the Windows PC where VALORANT runs:
```powershell
pip install -r requirements.txt
python -m val_rpc.main
```
Both VALORANT and the Discord desktop app must be open.

### Party size override

Force the party count shown on Discord (`N of M`). Real party is unchanged.
```powershell
python -m val_rpc.main --party-size 5 --max-party-size 5   # always show "5 of 5"
python -m val_rpc.main --max-party-size 4                   # keep real N, force M=4
```
`N` is clamped to `M`. Applies in both the lobby and the queue.

## Dev loop

- mac: edit → `git push`
- Windows: `git pull` → `python -m val_rpc.main`

## Test

```bash
pytest
```
