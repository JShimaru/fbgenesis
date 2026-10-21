# Fatale Breathe: Genesis
A real-time multiplayer survival arena set in a dark sci-fi universe where human lifespan is measured in breaths. Survive the **Anima Protocol.**

**Fatale Breathe: Genesis** is a browser-based grid survival arena prototype and prequel to the *Fatale Breathe* series. Subjects wake inside a sterile research facility, break out of containment, and fight to survive as the arena grows more dangerous. The game introduces the Anima Protocol and hints at the larger world through its observation feed, visual anomalies, and field guide.

The game runs on desktop and mobile browsers. Movement is grid-based and immediate: tap a destination or use the arrow keys. Each four-second pulse allows four normal steps; steps after the first cost five Breath. A destination beyond the remaining range advances the subject as far as the pulse allows, without using Dash. Dash moves three squares in the last direction for three Breath, once per pulse. Stillness recovery restores eight Breath per tick up to a 25-point reserve cap; moving three squares reopens recovery. Combat is real-time. ATTACK follows the subject’s facing and can be used three times per pulse with a 0.4-second cooldown between strikes; each follow-up strike costs two additional Breath, while damage remains based on the original random roll. The first two squares deal full damage and the third deals half. A three-pip meter shows strikes remaining and announces when they replenish. On desktop, use ATTACK, SPECIAL, and DASH or A, S, and D. Choose an attack square and press FIRE/Enter, or tap the same square twice quickly. Tap SPECIAL twice (or press S again) to launch; specials telegraph their area, allow two casts per pulse, and have a 1.5-second cooldown. Specials route around computer stations. Spectres pursue the nearest subject at least one square per pulse, with their pace capped at one less than that subject’s movement when possible. The mist begins at round 10 and deals up to eight Breath per exposure tick. Hidden collapse thresholds range from −12 to −30, with −30 as the absolute floor. The interface keeps Breath values hidden and represents condition through the aura. Solo practice uses bots; private rooms and Quick Join use the Colyseus relay server. The game layout adapts to desktop and mobile screens.

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
