# Fatale Breathe: Genesis multiplayer server

The browser build uses Colyseus for private room codes, public matchmaking, room membership, lobby readiness, activity tracking, and message delivery. During this beta integration the room host's browser still resolves the existing game rules and publishes the shared arena state. The room keeps a private latest snapshot so it can promote another connected player if the host leaves; pending round, purge, fight-intro, and special-attack timers resume from their saved deadlines.

## Run locally

From this folder:

```powershell
npm install
npm run dev
```

The server listens on port `2567` by default. Serve the repository root (for example, with `python -m http.server 8000`) and open it in two browser sessions to try Create Room / Join Room, or use Quick Join in both sessions. The server waits for at least two public queue members, groups up to eight, and gives the group a separate room. Each player must press Ready before the room host can initiate the trial. An unready subject with no pointer, keyboard, or click activity for 30 seconds is returned to the landing screen with a Rejoin Public Lobby button.

Solo Practice remains local and continues to use bots.

## Hosting

GitHub Pages can host the static browser game, but it cannot run the Colyseus Node.js server. Deploy this `server` folder to a Node-capable host, allow WebSocket connections, and set `window.ANIMA_SERVER_URL` to the host's secure `wss://` address in `network-config.js` before publishing the site. For local browser testing, temporarily set the checked-in `network-config.js` value to `ws://localhost:2567`; restore the production `wss://` value before publishing.

This host-relay setup preserves the existing game implementation. For public competitive play, move round resolution and hidden Breath thresholds to the server in a later hardening pass; clients currently receive the shared public state from the elected room host.

## Shared trial leaderboard

Completed online rooms publish one score record per subject to the public `leaderboard` room. The browser requests the top ten scores for a rolling 24-hour period, rolling seven-day period, or all time. The server calculates points from the host’s final trial report and stores records in `data/leaderboard.json` relative to the server working directory. Set `LEADERBOARD_FILE` to a persistent disk path on the hosting provider so records survive restarts. Keep the service on one server instance for this JSON-backed beta archive; a scaled deployment should use a shared database.

To clear beta records, set `LEADERBOARD_PURGE_ON_START=true` for one restart, then remove that variable immediately afterward. Leaving it enabled clears the archive on every restart. During beta, scores rely on the elected room host’s report because match resolution remains in the browser; a server-authoritative game simulation is needed before treating the archive as cheat-proof competition.
