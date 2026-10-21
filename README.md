# Fatale Breathe: Genesis
A real-time multiplayer survival arena set in a dark sci-fi universe where human lifespan is measured in breaths. Survive the **Anima Protocol.**

**Fatale Breathe: Genesis** is a browser-based grid survival arena prototype and prequel to the *Fatale Breathe* series. Subjects wake inside a sterile research facility, break out of containment, and fight to survive as the arena grows more dangerous. The game introduces the Anima Protocol and hints at the larger world through its observation feed, visual anomalies, and field guide.

The game runs on desktop and mobile browsers. Movement is free and grid-based: tap a reachable square or use the arrow keys to move immediately. Each three-second system pulse allows up to six normal steps and one four-square dash; normal steps after the third drain Breath. The pulse advances the mist and grants recovery only after a subject stays still. Combat uses real-time grid attacks and telegraphed area strikes. Use the ATTACK, SPECIAL, and DASH buttons or A, S, and D. Attack opens a two-square directional target preview; tap the same target twice quickly or use FIRE/Enter to confirm. Tap SPECIAL twice (or press S again) to launch the special. Spectres creep toward the nearest subject no faster than that subject moved, less one square, in the current pulse. It supports solo practice against bots, private rooms joined by code, and a public Quick Join queue. The interface keeps Breath values hidden and represents a subject’s condition through their aura.

## Play

Open the deployed game page, enter a subject name, then choose one of the available options:

- **Solo Practice** starts a local match with practice bots. No multiplayer server is needed.
- **Create Room** makes a private room. Share its room code with other players.
- **Join Room** joins a private room by code.
- **Quick Join** places you in the public matchmaking queue. When at least two people are waiting, the service groups players into a match of up to eight. Lobby members must ready up before the host can start.

Use the **Field Guide** in game for tactical tips and optional lore notes. The arena supports touch controls and keyboard input; the on-screen controls adapt to mobile landscape layouts.

## Run locally

### Solo practice

Serve the static page from the repository root. For example:

```powershell

python -m http.server 8000
```

Then open <http://localhost:8000> in a browser and choose **Solo Practice**.

### Multiplayer

The browser client uses a separate Colyseus server for private rooms, public matchmaking, lobby readiness, and message relay. In a second terminal, start it with:

```powershell
cd server
npm install
npm run dev
```

The server listens on port `2567` by default. For local multiplayer, temporarily set `network-config.js` to `ws://localhost:2567`, open the page in two or more browser sessions, then create/join a room or use Quick Join. The matchmaking queue waits briefly to group players and can form partial matches once at least two players are queued.

To check the server TypeScript configuration:

```powershell
cd server
npm run typecheck
```

## Deployment

GitHub Pages can serve the static game files, but it cannot host the Colyseus server. Publish the repository root as the Pages site, and deploy `server` to a Node.js host that supports WebSockets. The checked-in `network-config.js` points to the beta server at `wss://ptiserver.onrender.com`; keep the production `wss://` address in that file when publishing. Solo Practice works without the server.

## Project layout

- `index.html` — game interface, rendering, controls, solo rules, and browser networking client.
- `network-config.js` — multiplayer server address used by the browser client.
- `server/src/main.ts` — Colyseus private-room, public-queue, readiness, activity, and relay logic.
- `server/package.json` — server development and type-check scripts.

## Multiplayer testing note

This is a beta-testing build. The current multiplayer arrangement elects a browser client as the room host for shared game-state resolution; the Colyseus server manages rooms, relays state and input, and rate-limits combat intents. Real-time combat and Spectre updates are resolved by the elected browser host, so this build is for beta playtesting and is not authoritative against modified clients.
