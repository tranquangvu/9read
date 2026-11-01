# Clinic platform lab kit

A small, runnable stand-in for the clinic booking platform used by every hands-on lab in the
DevOps Engineer Career Track (`devops/`). It is deliberately framework-free so the infrastructure,
not the app, is what you learn.

| Path | What it is |
|---|---|
| `booking-api/` | Node 22 HTTP API on :8080, distroless image |
| `booking-worker/` | SQS long-poll consumer |
| `booking-web/` | nginx-unprivileged on :8080, static page, proxies `/api/*` to `API_UPSTREAM` |
| `compose.yaml` | Postgres 16 + api + web for local work (`http://localhost:3000`) |
| `fetch.sh` | Downloads these files into `./clinic-app` |

## booking-api

| Endpoint | Purpose |
|---|---|
| `GET /healthz` | Liveness: 200 while the process is up |
| `GET /readyz` | Readiness: checks Postgres; 503 while draining after SIGTERM |
| `GET /bookings`, `POST /bookings` | JSON `{ "patient": "An", "slot": "2026-11-02T09:00" }` |
| `GET /admin/leak` | `CHAOS=on` only: +50 MiB of retained memory per call (OOMKilled drills) |
| `GET /admin/burn?ms=2000` | `CHAOS=on` only: pins one CPU core (latency / HPA drills) |
| `GET /admin/crash` | `CHAOS=on` only: exits 1 (CrashLoopBackOff drills) |

`node server.js migrate` (container command `["server.js","migrate"]`) creates the schema and exits.

| Env var | Default | Meaning |
|---|---|---|
| `PORT` | 8080 | Listen port |
| `DATABASE_URL` | unset → in-memory store | Postgres connection string |
| `DATABASE_SSL` | `false` | Set `true` for RDS |
| `QUEUE_URL` | unset | Send `booking.created` to this SQS queue on POST |
| `APP_VERSION` | `dev` | Echoed by `/healthz` and in every log line |
| `MIGRATE_ON_START` | `true` | `false` = only the migrate job changes the schema |
| `DRAIN_MS` | 5000 | Time between SIGTERM and closing the server |
| `CHAOS` | off | `on` enables the `/admin/*` drill endpoints. Never in prod |

## booking-worker

Env `QUEUE_URL` (required), `WORK_MS` (default 200). Needs `sqs:ReceiveMessage` and `sqs:DeleteMessage`.

## Build for AWS (Graviton)

```bash
docker buildx build --platform linux/arm64 -t $REPO:1.0.0 --push booking-api
```
