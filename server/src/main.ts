import { defineRoom, defineServer, matchMaker, Room, type Client } from "@colyseus/core";
import { WebSocketTransport } from "@colyseus/ws-transport";

type Subject = { id: string; name: string; ready: boolean; lastActivity: number };
const CODE_CHANNEL = "$anima-room-codes";
const LETTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";

class TrialRoom extends Room {
  maxClients = 8;
  privateCode = "";
  private hostSessionId: string | null = null;
  private publicMatch = false;
  private expectedHostSessionId: string | undefined;
  private subjects = new Map<string, Subject>();
  private rosterTimer: ReturnType<typeof setInterval> | undefined;
  private combatIntentWindows = new Map<string, { startedAt: number; count: number }>();

  async onCreate(options: { publicMatch?: boolean; expectedHostSessionId?: string } = {}) {
    this.publicMatch = !!options.publicMatch;
    this.expectedHostSessionId = options.expectedHostSessionId;
    this.privateCode = await this.allocateCode();
    this.roomId = this.privateCode;
    this.setPrivate(true);

    this.onMessage("identify", (client, payload: { name?: string }) => {
      const subject = this.subjects.get(client.sessionId);
      if (!subject) return;
      subject.name = String(payload?.name || "SUBJECT").slice(0, 12);
      this.sendRoomInfo(client);
      this.broadcastRoster();
    });
    this.onMessage("ready", (client, payload: { ready?: boolean }) => {
      const subject = this.subjects.get(client.sessionId);
      if (!subject || this.hasStarted) return;
      subject.ready = !!payload?.ready;
      subject.lastActivity = Date.now();
      this.broadcastRoster();
    });
    this.onMessage("activity", (client) => {
      const subject = this.subjects.get(client.sessionId);
      if (subject) subject.lastActivity = Date.now();
    });
    this.onMessage("host-state", (client, payload) => {
      if (client.sessionId !== this.hostSessionId || !payload?.state) return;
      if (payload.state.started && (this.subjects.size < 2 || [...this.subjects.values()].some((subject) => !subject.ready))) return;
      this.hasStarted = !!payload.state.started;
      for (const member of this.clients) if (member !== client) member.send("game-state", payload.state);
    });
    this.onMessage("client-input", (client, payload: { message?: unknown }) => {
      if (!payload?.message || client.sessionId === this.hostSessionId) return;
      const message = payload.message as { type?: unknown; action?: unknown };
      if (message.type === "realtime-combat") {
        if (!this.hasStarted || !["attack", "special", "dash"].includes(String(message.action))) return;
        const now = Date.now();
        const window = this.combatIntentWindows.get(client.sessionId);
        if (!window || now - window.startedAt >= 1000) {
          this.combatIntentWindows.set(client.sessionId, { startedAt: now, count: 1 });
        } else {
          if (window.count >= 10) return;
          window.count++;
        }
      }
      this.clients.find((member) => member.sessionId === this.hostSessionId)
        ?.send("host-input", { from: client.sessionId, message: payload.message });
    });
    this.onMessage("host-input", (client, payload: { message?: unknown }) => {
      if (client.sessionId !== this.hostSessionId || !payload?.message) return;
      this.broadcast("host-input", { from: client.sessionId, message: payload.message });
    });

    this.rosterTimer = setInterval(() => this.kickIdleSubjects(), 1000);
  }

  private hasStarted = false;

  onAuth() {
    return !this.hasStarted;
  }

  async onJoin(client: Client, options: { name?: string; expectedHost?: boolean } = {}) {
    if (options.expectedHost || client.sessionId === this.expectedHostSessionId || (!this.expectedHostSessionId && !this.hostSessionId)) {
      this.hostSessionId = client.sessionId;
    }
    this.subjects.set(client.sessionId, {
      id: client.sessionId,
      name: String(options.name || "SUBJECT").slice(0, 12),
      ready: false,
      lastActivity: Date.now(),
    });
    this.sendRoomInfo(client);
    this.broadcast("subject-joined", { id: client.sessionId, name: String(options.name || "SUBJECT").slice(0, 12) });
    this.broadcastRoster();
  }

  onLeave(client: Client) {
    this.subjects.delete(client.sessionId);
    this.combatIntentWindows.delete(client.sessionId);
    if (client.sessionId === this.hostSessionId) {
      this.hostSessionId = this.clients[0]?.sessionId || null;
      if (this.hostSessionId) this.clients[0].send("host-role", { host: true });
    }
    this.broadcastRoster();
  }

  onDispose() {
    if (this.rosterTimer) clearInterval(this.rosterTimer);
    void this.presence.srem(CODE_CHANNEL, this.privateCode);
  }

  private async allocateCode(): Promise<string> {
    const active = new Set(await this.presence.smembers(CODE_CHANNEL));
    let code = "";
    do {
      code = Array.from({ length: 6 }, () => LETTERS[Math.floor(Math.random() * LETTERS.length)]).join("");
    } while (active.has(code));
    await this.presence.sadd(CODE_CHANNEL, code);
    return code;
  }

  private sendRoomInfo(client: Client) {
    client.send("room-info", {
      code: this.privateCode,
      host: client.sessionId === this.hostSessionId,
      publicMatch: this.publicMatch,
      roster: [...this.subjects.values()].map(({ lastActivity, ...subject }) => subject),
    });
  }

  private broadcastRoster() {
    const roster = [...this.subjects.values()].map(({ lastActivity, ...subject }) => subject);
    const allReady = roster.length >= 2 && roster.every((subject) => subject.ready);
    this.broadcast("lobby-roster", { roster, allReady, hostSessionId: this.hostSessionId });
  }

  private kickIdleSubjects() {
    if (this.hasStarted) return;
    const cutoff = Date.now() - 30_000;
    for (const client of [...this.clients]) {
      const subject = this.subjects.get(client.sessionId);
      if (subject && !subject.ready && subject.lastActivity < cutoff) {
        client.send("idle-kicked", { message: "You were returned to the public lobby after 30 seconds without activity." });
        void client.leave(4001);
      }
    }
  }
}

/** Hidden public queue. It waits for at least two subjects, batches up to eight,
 * then creates a separate unlisted match room and issues seat reservations. */
class PublicQueueRoom extends Room {
  maxClients = 500;
  private queueTimer: ReturnType<typeof setInterval> | undefined;
  private creatingMatch = false;

  onCreate() {
    this.queueTimer = setInterval(() => void this.processQueue(), 500);
    this.onMessage("confirm", (client) => {
      if (client.userData?.reserved) void client.leave();
    });
  }

  onJoin(client: Client, options: { name?: string } = {}) {
    client.userData = { options: { name: String(options.name || "SUBJECT").slice(0, 12) }, queuedAt: Date.now(), reserved: false };
    this.sendQueueCounts();
  }

  onLeave() { this.sendQueueCounts(); }

  onDispose() { if (this.queueTimer) clearInterval(this.queueTimer); }

  private sendQueueCounts() {
    const waiting = this.clients.filter((client) => !client.userData?.reserved);
    waiting.forEach((client) => client.send("clients", waiting.length));
  }

  private async processQueue() {
    if (this.creatingMatch) return;
    const waiting = this.clients.filter((client) => !client.userData?.reserved);
    if (waiting.length < 2) { this.sendQueueCounts(); return; }
    const oldest = Math.min(...waiting.map((client) => client.userData.queuedAt));
    if (waiting.length < 8 && Date.now() - oldest < 4000) return;
    this.creatingMatch = true;
    try {
      const group = [...waiting];
      for (let i = group.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [group[i], group[j]] = [group[j], group[i]];
      }
      const selected = group.slice(0, 8);
      const room = await matchMaker.createRoom("game", {
        publicMatch: true,
        expectedHostSessionId: selected[0].sessionId,
      });
      await matchMaker.reserveMultipleSeatsFor(room, selected.map((client, index) => ({
        sessionId: client.sessionId,
        options: { ...client.userData.options, expectedHost: index === 0 },
        auth: client.auth,
      })));
      selected.forEach((client) => {
        client.userData.reserved = true;
        client.send("seat", matchMaker.buildSeatReservation(room, client.sessionId));
      });
      this.sendQueueCounts();
    } catch (error) {
      const message = error instanceof Error ? error.message : "Match creation failed";
      this.clients.filter((client) => !client.userData?.reserved).forEach((client) => client.send("queue-error", { message }));
    } finally {
      this.creatingMatch = false;
    }
  }
}

const server = defineServer({
  transport: new WebSocketTransport(),
  rooms: {
    game: defineRoom(TrialRoom),
    queue: defineRoom(PublicQueueRoom),
  },
});

const port = Number(process.env.PORT || 2567);
server.listen(port).then(() => console.log(`Anima Colyseus server listening on ${port}`));
