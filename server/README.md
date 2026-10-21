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
