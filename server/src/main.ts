import { defineRoom, defineServer, matchMaker, Room, type Client } from "@colyseus/core";
import { WebSocketTransport } from "@colyseus/ws-transport";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";

type Subject = { id: string; name: string; ready: boolean; lastActivity: number };
type HostSnapshot = {
  started?: boolean;
  phase?: string;
  players?: Array<{ id?: string; alive?: boolean; dead?: boolean; contained?: boolean; breath?: number; shield?: number; [key: string]: unknown }>;
  [key: string]: unknown;
};
const CODE_CHANNEL = "$anima-room-codes";
const LETTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
type LeaderboardPeriod = "daily" | "weekly" | "allTime";
type ScoreRecord = { id: string; matchId: string; subject: string; score: number; createdAt: number };
const LEADERBOARD_FILE = resolve(process.env.LEADERBOARD_FILE || "data/leaderboard.json");
const MAX_SCORE_RECORDS = 10_000;
function saveLeaderboard(records: ScoreRecord[]) {
  mkdirSync(dirname(LEADERBOARD_FILE), { recursive: true });
  writeFileSync(LEADERBOARD_FILE, JSON.stringify(records.slice(-MAX_SCORE_RECORDS)), "utf8");
}
function loadLeaderboard(): ScoreRecord[] {
  if (process.env.LEADERBOARD_PURGE_ON_START === "true") { saveLeaderboard([]); console.log("Leaderboard archive purged at startup."); return []; }
  try {
    if (!existsSync(LEADERBOARD_FILE)) return [];
    const value: unknown = JSON.parse(readFileSync(LEADERBOARD_FILE, "utf8"));
    return Array.isArray(value) ? value.filter((r): r is ScoreRecord => !!r && typeof r.id === "string" && typeof r.matchId === "string" && typeof r.subject === "string" && Number.isFinite(r.score) && Number.isFinite(r.createdAt)).slice(-MAX_SCORE_RECORDS) : [];
  } catch (error) { console.error("Could not read leaderboard archive:", error); return []; }
}
let scoreArchive = loadLeaderboard();
function scoreForSubject(player: { id?: unknown; stats?: unknown }, winnerId: string | null) {
  const stats = player.stats && typeof player.stats === "object" ? player.stats as Record<string, unknown> : {};
  const points = (key: string) => Math.max(0, Math.min(10_000, Number(stats[key]) || 0));
  const breakout = Number(stats.breakoutOrder);
  return Math.min(100_000, points("roundsSurvived") * 2 + points("hits") * 3 + points("specialAttacks") * 2 + points("evades") * 4 + points("eai") * 2 + (breakout === 1 ? 10 : breakout === 2 ? 5 : 0) + (player.id === winnerId ? 20 : 0));
}
function leaderboardRows(period: LeaderboardPeriod) {
  const now = Date.now(), cutoff = period === "daily" ? now - 86_400_000 : period === "weekly" ? now - 604_800_000 : 0;
  return scoreArchive.filter((record) => record.createdAt >= cutoff).sort((a, b) => b.score - a.score || a.createdAt - b.createdAt).slice(0, 10);
}
function recordFinishedTrial(snapshot: HostSnapshot, roomCode: string) {
  if (!Array.isArray(snapshot.players)) return;
  const matchId = String(snapshot.trialId || (roomCode + "-" + Date.now())).slice(0, 100);
  if (scoreArchive.some((record) => record.matchId === matchId)) return;
  const players = snapshot.players as Array<{ id?: unknown; name?: unknown; alive?: unknown; stats?: unknown }>;
  const survivors = players.filter((p) => p.alive === true), winnerId = survivors.length === 1 ? String(survivors[0].id || "") : null;
  const createdAt = Date.now();
  for (const player of players) {
    if (typeof player.id !== "string") continue;
    const subject = String(player.name || "SUBJECT").replace(/[\u0000-\u001f\u007f]/g, "").trim().slice(0, 24) || "SUBJECT";
    scoreArchive.push({ id: (matchId + ":" + player.id).slice(0, 160), matchId, subject, score: scoreForSubject(player, winnerId), createdAt });
  }
  scoreArchive = scoreArchive.slice(-MAX_SCORE_RECORDS);
  try { saveLeaderboard(scoreArchive); } catch (error) { console.error("Could not save leaderboard archive:", error); }
  LeaderboardRoom.publishAll();
}


class TrialRoom extends Room {
  maxClients = 8;
  privateCode = "";
  private hostSessionId: string | null = null;
  private publicMatch = false;
  private expectedHostSessionId: string | undefined;
  private subjects = new Map<string, Subject>();
  private rosterTimer: ReturnType<typeof setInterval> | undefined;
  private combatIntentWindows = new Map<string, { startedAt: number; count: number }>();
  private lastHostSnapshot: HostSnapshot | null = null;

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
      if (payload.state.started && !this.hasStarted && (this.subjects.size < 2 || [...this.subjects.values()].some((subject) => !subject.ready))) return;
      const previousPhase = this.lastHostSnapshot?.phase;
      this.hasStarted = !!payload.state.started;
      if (payload.hostState && typeof payload.hostState === "object") {
        const snapshot = JSON.parse(JSON.stringify(payload.hostState)) as HostSnapshot;
        if (payload.state.phase === "ended" && previousPhase !== "ended") recordFinishedTrial(snapshot, this.privateCode);
        this.lastHostSnapshot = snapshot;
      }
      for (const member of this.clients) if (member !== client) member.send("game-state", payload.state);
    });
    this.onMessage("client-input", (client, payload: { message?: unknown }) => {
      if (!payload?.message || client.sessionId === this.hostSessionId) return;
      const message = payload.message as { type?: unknown; action?: unknown };
      if (message.type === "realtime-combat") {
        if (!this.hasStarted || !["face", "attack", "special", "dash"].includes(String(message.action))) return;
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
      const replacement = this.clients.find((member) => member.sessionId !== client.sessionId);
      this.hostSessionId = replacement?.sessionId || null;
      if (this.lastHostSnapshot && Array.isArray(this.lastHostSnapshot.players)) {
        const departed = this.lastHostSnapshot.players.find((player: { id?: string }) => player.id === client.sessionId);
        if (departed && this.lastHostSnapshot.started && this.lastHostSnapshot.phase !== "ended") {
          departed.alive = false;
          departed.dead = true;
          departed.contained = false;
          departed.breath = 0;
          departed.shield = 0;
        } else {
          this.lastHostSnapshot.players = this.lastHostSnapshot.players.filter((player: { id?: string }) => player.id !== client.sessionId);
        }
      }
      if (replacement) replacement.send("host-role", { host: true, state: this.lastHostSnapshot });
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

class LeaderboardRoom extends Room {
  static instances = new Set<LeaderboardRoom>();
  maxClients = 500;
  onCreate() {
    this.setPrivate(false);
    LeaderboardRoom.instances.add(this);
    this.onMessage("fetch", (client, payload: { period?: unknown } = {}) => {
      const period = this.period(payload.period);
      client.send("leaderboard-data", { period, rows: leaderboardRows(period), updatedAt: Date.now() });
    });
  }
  onJoin(client: Client) { client.send("leaderboard-data", { period: "daily", rows: leaderboardRows("daily"), updatedAt: Date.now() }); }
  onDispose() { LeaderboardRoom.instances.delete(this); }
  static publishAll() { for (const room of this.instances) room.broadcast("leaderboard-updated", { updatedAt: Date.now() }); }
  private period(value: unknown): LeaderboardPeriod { return value === "weekly" || value === "allTime" ? value : "daily"; }
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
    leaderboard: defineRoom(LeaderboardRoom),
  },
});

const port = Number(process.env.PORT || 2567);
server.listen(port).then(() => console.log(`Anima Colyseus server listening on ${port}`));
