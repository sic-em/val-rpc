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

1. **Discord application** — create one at
   https://discord.com/developers/applications, copy its **Application ID**.
2. **Art assets** — under *Rich Presence → Art Assets*, upload images named by key:
   - `valorant` (logo)
   - `map_<name>` e.g. `map_ascent`, `map_haven`, `map_piazza`
   - `mode_<queueId>` e.g. `mode_competitive`, `mode_deathmatch`, `mode_hurm`
3. **Install** (on the Windows PC where VALORANT runs):
   ```powershell
   pip install -r requirements.txt
   ```
4. **Run** (VALORANT and Discord both open):
   ```powershell
   $env:VALRPC_CLIENT_ID = "your-application-id"
   python -m val_rpc.main
   ```

## Dev loop

- mac: edit → `git push`
- Windows: `git pull` → `python -m val_rpc.main`

## Test

```bash
pytest
```
