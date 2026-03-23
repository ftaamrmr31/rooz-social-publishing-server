# Coolify Deployment Guide — Rooz Social Publishing Server

A step-by-step, beginner-friendly guide to deploy this FastAPI application on
[Coolify](https://coolify.io/) running on a Hostinger VPS (1 CPU · 4 GB RAM · 50 GB disk).

---

## 1. Prerequisites

| Item | Value |
|---|---|
| VPS OS | Ubuntu 22.04 LTS (recommended) |
| Coolify installed | `https://<your-vps-ip>:8000` (Coolify default port) |
| Repository | `https://github.com/ftaamrmr31/rooz-social-publishing-server` |
| App port | `8000` |

---

## 2. Add Your Repository Source in Coolify

1. Open the Coolify dashboard in your browser.
2. Go to **Sources** → **+ New Source**.
3. Choose **GitHub** (public repository, no token required for public repos).
4. Repository URL: `https://github.com/ftaamrmr31/rooz-social-publishing-server`
5. Click **Save**.

---

## 3. Create a New Application

1. Go to **Projects** → **+ New Project** → name it `rooz-social`.
2. Inside the project click **+ New Resource** → **Application**.
3. Select **Git Repository** as the source and pick the repo you added above.

---

## 4. Exact Coolify Settings

| Setting | Value |
|---|---|
| **Build Pack** | `Dockerfile` |
| **Branch** | `main` |
| **Dockerfile path** | `./Dockerfile` |
| **Docker Context** | `.` (repository root) |
| **Exposed port (container)** | `8000` |
| **Published port (host)** | `8000` (or leave empty — Coolify will proxy via its reverse-proxy) |
| **Health check path** | `/health` |
| **Health check interval** | `30` seconds |
| **Health check timeout** | `5` seconds |
| **Restart policy** | `unless-stopped` |

> **Tip:** If you plan to run multiple services on the same VPS, leave the
> "Published port" empty and let Coolify's built-in Traefik/Caddy reverse-proxy
> route traffic. This avoids port conflicts.

---

## 5. Environment Variables

Set these in **Application → Environment Variables** inside Coolify.
Copy from `.env.example` and fill in your real values.

```env
# Application
APP_NAME=Rooz Social Publishing Server
APP_VERSION=0.1.0
DEBUG=False
ENVIRONMENT=production

# Server
HOST=0.0.0.0
PORT=8000

# Telegram integration
TELEGRAM_BOT_TOKEN=<your-telegram-bot-token>
TELEGRAM_CHAT_ID=<your-telegram-chat-id>
```

> **Never** commit real tokens to Git. Set them only in Coolify's secret
> environment variable panel — they are encrypted at rest.

---

## 6. Domain Configuration

### Option A — Subdomain (recommended)
Point an A record on your domain to your VPS IP, then enter it in Coolify:

```
api.yourdomain.com
```

Coolify will automatically provision a Let's Encrypt TLS certificate.

### Option B — IP-only (development/testing)
Use `http://<your-vps-ip>:8000` — no domain or TLS required.

---

## 7. Persistent Storage (SQLite)

Because the app uses SQLite (`database.db`), the file lives inside the container
and will be **lost on redeploy** unless you mount a persistent volume.

In Coolify → **Application → Volumes**, add:

| Container path | Host path |
|---|---|
| `/app/database.db` | `/data/rooz/database.db` |

This ensures your data survives container restarts and new deploys.

---

## 8. Lightweight Recommendations for a Small VPS (1 CPU / 4 GB RAM)

| Recommendation | Why |
|---|---|
| Use `python:3.12-slim` base image (already in `Dockerfile`) | Cuts image size by ~60% vs full Python image |
| Set `uvicorn` workers to `1` in the `CMD` | Single CPU — multiple workers add overhead, not speed |
| Add `--timeout-keep-alive 5` to uvicorn | Frees idle connections faster |
| Keep Coolify's **Resource Limits** → CPU at `0.4` and Memory at `512m` | Leaves headroom for n8n, Coolify itself, and the OS |
| Enable Coolify's **Auto-deploy on push** for the `main` branch | Zero-touch deploys without manual clicks |
| Schedule SQLite backups with `cron` on the host (daily `cp /data/rooz/database.db /backups/`) | SQLite has no built-in replication |

Recommended final `CMD` in `Dockerfile` for production:

```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", \
     "--workers", "1", "--timeout-keep-alive", "5"]
```

---

## 9. Post-Deployment Test Checklist

After Coolify reports the deployment as **Running**, run the following tests
(replace `api.yourdomain.com` with your actual domain or IP):

### 9.1 Health check
```bash
curl -s https://api.yourdomain.com/health
# Expected: {"status":"ok","service":"Rooz Social Publishing Server"}
```

### 9.2 API root
```bash
curl -s https://api.yourdomain.com/api/
# Expected: {"message":"Welcome to Rooz Social Publishing Server API"}
```

### 9.3 Create a publish job
```bash
curl -s -X POST https://api.yourdomain.com/api/publish \
  -H "Content-Type: application/json" \
  -d '{"platform":"telegram","content":"Hello from Coolify!"}'
# Expected: {"id":1,"platform":"telegram","content":"...","status":"pending",...}
```

### 9.4 List publish jobs
```bash
curl -s https://api.yourdomain.com/api/publish
# Expected: JSON array of publish jobs
```

### 9.5 Send Telegram message immediately
```bash
curl -s -X POST https://api.yourdomain.com/api/publish/telegram/send-now \
  -H "Content-Type: application/json" \
  -d '{"content":"Test message from production!"}'
# Expected: {"success":true,"platform":"telegram","result":...}
```

### 9.6 Interactive API docs
Open in your browser:
- Swagger UI: `https://api.yourdomain.com/docs`
- ReDoc: `https://api.yourdomain.com/redoc`

### 9.7 Verify TLS (if using a domain)
```bash
curl -v https://api.yourdomain.com/health 2>&1 | grep "SSL certificate verify ok"
```

---

## 10. Troubleshooting

| Symptom | Fix |
|---|---|
| Container keeps restarting | Check **Logs** in Coolify for Python import errors; ensure all env vars are set |
| `/health` returns 502 | The app hasn't started yet — wait 20s and retry; check uvicorn logs |
| Telegram send-now returns 400 | `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID` is missing or wrong |
| Database resets on redeploy | Volume not mounted — follow **Section 7** above |
| Build fails | Run `docker build .` locally to reproduce; check `requirements.txt` |
