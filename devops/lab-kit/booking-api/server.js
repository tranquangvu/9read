// booking-api — lab stand-in for the clinic booking API (DevOps Career Track lab kit).
// Plain Node 22, no framework. Runs with or without Postgres/SQS so every lab can use it.
//   PORT=8080  DATABASE_URL=postgres://...  QUEUE_URL=https://sqs...  APP_VERSION=1.0.0
import http from "node:http";
import pg from "pg";
import { SQSClient, SendMessageCommand } from "@aws-sdk/client-sqs";

const PORT = Number(process.env.PORT || 8080);
const VERSION = process.env.APP_VERSION || "dev";
const db = process.env.DATABASE_URL
  ? new pg.Pool({ connectionString: process.env.DATABASE_URL, max: 5,
      ssl: process.env.DATABASE_SSL === "true" ? { rejectUnauthorized: false } : false })   // RDS: set DATABASE_SSL=true
  : null;
const sqs = process.env.QUEUE_URL ? new SQSClient({}) : null;
const memory = [];           // fallback store when DATABASE_URL is unset
const leak = [];             // grows on /admin/leak (OOM drills)
let draining = false;

const log = (level, msg, extra = {}) =>
  console.log(JSON.stringify({ ts: new Date().toISOString(), level, msg, service: "booking-api", version: VERSION, ...extra }));

async function migrate() {
  if (!db) return log("warn", "DATABASE_URL not set, using in-memory store");
  await db.query(`CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY, patient TEXT NOT NULL, slot TIMESTAMPTZ NOT NULL, created_at TIMESTAMPTZ DEFAULT now())`);
  log("info", "migration ok");
}

const send = (res, code, body) => {
  res.writeHead(code, { "content-type": "application/json" });
  res.end(JSON.stringify(body));
};
const readBody = (req) => new Promise((ok, bad) => {
  let s = ""; req.on("data", (c) => (s += c)); req.on("end", () => { try { ok(s ? JSON.parse(s) : {}); } catch (e) { bad(e); } });
});

const server = http.createServer(async (req, res) => {
  const t0 = Date.now();
  const url = new URL(req.url, "http://x");
  try {
    if (url.pathname === "/healthz") return send(res, 200, { ok: true, version: VERSION });   // liveness: process only
    if (url.pathname === "/readyz") {                                                       // readiness: deps too
      if (draining) return send(res, 503, { ready: false, reason: "draining" });
      if (db) await db.query("SELECT 1");
      return send(res, 200, { ready: true });
    }
    if (url.pathname === "/bookings" && req.method === "GET") {
      const rows = db ? (await db.query("SELECT * FROM bookings ORDER BY id DESC LIMIT 20")).rows : memory.slice(-20).reverse();
      return send(res, 200, rows);
    }
    if (url.pathname === "/bookings" && req.method === "POST") {
      const { patient, slot } = await readBody(req);
      if (!patient || !slot) return send(res, 400, { error: "patient and slot are required" });
      const row = db
        ? (await db.query("INSERT INTO bookings (patient, slot) VALUES ($1, $2) RETURNING *", [patient, slot])).rows[0]
        : { id: memory.length + 1, patient, slot, created_at: new Date().toISOString() };
      if (!db) memory.push(row);
      if (sqs) await sqs.send(new SendMessageCommand({ QueueUrl: process.env.QUEUE_URL, MessageBody: JSON.stringify({ type: "booking.created", booking: row }) }));
      return send(res, 201, row);
    }
    // ---- drill endpoints: enabled only when CHAOS=on, used by the break-and-fix labs ----
    if (process.env.CHAOS === "on" && url.pathname === "/admin/leak") {
      for (let i = 0; i < 50; i++) leak.push(Buffer.alloc(1024 * 1024, 1));            // +50 MiB per call
      return send(res, 200, { leakedMiB: leak.length });
    }
    if (process.env.CHAOS === "on" && url.pathname === "/admin/burn") {
      const end = Date.now() + Number(url.searchParams.get("ms") || 2000); while (Date.now() < end);  // pin one core
      return send(res, 200, { burned: true });
    }
    if (process.env.CHAOS === "on" && url.pathname === "/admin/crash") { log("error", "crash requested"); process.exit(1); }
    send(res, 404, { error: "not found" });
  } catch (err) {
    log("error", "request failed", { path: url.pathname, err: err.message });
    send(res, 500, { error: "internal" });
  } finally {
    log("info", "request", { method: req.method, path: url.pathname, status: res.statusCode, ms: Date.now() - t0 });
  }
});

process.on("SIGTERM", () => {                       // graceful shutdown: fail readiness, finish in-flight, exit
  draining = true; log("info", "SIGTERM received, draining");
  setTimeout(() => server.close(() => { db?.end(); process.exit(0); }), Number(process.env.DRAIN_MS || 5000));
});

// `node server.js migrate` runs the schema migration and exits (ECS run-task / Kubernetes Job / Argo PreSync).
// MIGRATE_ON_START=false makes the server skip it, so only the migration job ever changes the schema.
if (process.argv[2] === "migrate") { await migrate(); await db?.end(); process.exit(0); }
if (process.env.MIGRATE_ON_START !== "false") await migrate();
server.listen(PORT, () => log("info", "listening", { port: PORT }));
