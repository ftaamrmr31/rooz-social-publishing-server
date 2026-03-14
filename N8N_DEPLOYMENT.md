# Coolify Deployment Guide — n8n

A step-by-step, beginner-friendly guide to deploy
[n8n](https://n8n.io/) as a standalone Docker application on
[Coolify](https://coolify.io/) running on a Hostinger VPS (1 CPU · 4 GB RAM · 50 GB disk).

n8n is a self-hostable workflow-automation tool.
It runs as a single Docker container from the official image `n8nio/n8n`.

---

## 1. Prerequisites

| Item | Value |
|---|---|
| VPS OS | Ubuntu 22.04 LTS (recommended) |
| Coolify installed | `https://<your-vps-ip>:8000` (Coolify default port) |
| n8n Docker image | `n8nio/n8n` (official, no build required) |
| App port | `5678` |

> **Note:** n8n is deployed as a **separate Coolify application** — completely
> independent from the Rooz Social Publishing Server.

---

## 2. Create a New Application in Coolify

1. Open the Coolify dashboard.
2. Go to **Projects** → **+ New Project** → name it `n8n` (or `automation`).
3. Inside the project click **+ New Resource** → **Application**.
4. When asked for a source, choose **Docker Image** (not Git Repository).
5. Enter the image name: `n8nio/n8n`
6. Leave the tag as `latest` (or pin to a specific version, e.g. `1.85.0`, for stability).
7. Click **Continue**.

---

## 3. Exact Coolify Settings

| Setting | Value |
|---|---|
| **Deployment type** | Docker Image |
| **Image** | `n8nio/n8n` |
| **Tag** | `latest` (or a pinned version, e.g. `1.85.0`) |
| **Exposed port (container)** | `5678` |
| **Published port (host)** | leave empty — let Coolify's reverse-proxy handle routing |
| **Health check path** | `/healthz` |
| **Health check interval** | `30` seconds |
| **Health check timeout** | `10` seconds |
| **Restart policy** | `unless-stopped` |

> **Tip:** Leaving the "Published port" empty lets Coolify's built-in
> Traefik/Caddy proxy route HTTPS traffic to n8n automatically — no manual
> firewall rule needed for port 5678.

---

## 4. Environment Variables

Set all of these in **Application → Environment Variables** in Coolify.
They are stored encrypted and injected at container start.

```env
# ----- Core -----
N8N_HOST=n8n.yourdomain.com
N8N_PORT=5678
N8N_PROTOCOL=https

# ----- Webhook / public URL -----
# Must match the domain Coolify proxies to this container
WEBHOOK_URL=https://n8n.yourdomain.com/

# ----- Authentication -----
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=ChangeMeToAStrongPassword!

# ----- Encryption key (generate once, keep secret) -----
# Run: openssl rand -hex 32
N8N_ENCRYPTION_KEY=replace-with-a-64-char-random-hex-string

# ----- Timezone -----
GENERIC_TIMEZONE=Asia/Tehran

# ----- Data / persistence -----
# Where n8n stores workflows, credentials, and execution history
N8N_USER_FOLDER=/home/node/.n8n

# ----- Performance (lightweight settings for 1 CPU / 4 GB RAM) -----
# Limit concurrent workflow executions to avoid OOM
EXECUTIONS_DATA_MAX_AGE=72
EXECUTIONS_DATA_PRUNE=true

# ----- Logging -----
N8N_LOG_LEVEL=warn
```

> **Security rule:** Never commit real passwords or the encryption key to Git.
> Set them only inside Coolify's encrypted environment variable panel.
> If you lose `N8N_ENCRYPTION_KEY`, all saved credentials become unreadable.

---

## 5. Persistent Volume

n8n stores **workflows, credentials, and execution history** inside the
container at `/home/node/.n8n`. Without a volume this data is lost on every
redeploy.

In Coolify → **Application → Volumes**, add:

| Container path | Host path |
|---|---|
| `/home/node/.n8n` | `/data/n8n` |

Create the directory on the host before the first deploy:

```bash
sudo mkdir -p /data/n8n
sudo chown -R 1000:1000 /data/n8n   # n8n runs as UID 1000
```

---

## 6. Domain Configuration

### Option A — Subdomain with TLS (recommended)

1. Log in to your DNS provider and add an **A record**:
   - **Name:** `n8n`
   - **Value:** `<your-vps-ip>`
2. In Coolify → **Application → Domains**, enter: `n8n.yourdomain.com`
3. Coolify automatically provisions a Let's Encrypt TLS certificate.
4. Set `N8N_HOST`, `N8N_PROTOCOL`, and `WEBHOOK_URL` to match (see Section 4).

### Option B — IP-only (development/testing)

Use `http://<your-vps-ip>:5678` — no domain or TLS required.
Set `N8N_PROTOCOL=http` and `WEBHOOK_URL=http://<your-vps-ip>:5678/`.

---

## 7. Authentication Settings

n8n ships with built-in Basic Auth.
The environment variables below (already listed in Section 4) enable it:

```env
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=ChangeMeToAStrongPassword!
```

After your first login, n8n will prompt you to create an **owner account**
(email + password). This replaces Basic Auth as the primary login going
forward. You can then set:

```env
N8N_BASIC_AUTH_ACTIVE=false
```

and rely on n8n's built-in user management instead.

---

## 8. Webhook / Public URL Settings

Webhooks are URLs that external services call to trigger your n8n workflows.
n8n must know its own public address to generate correct webhook URLs.

```env
WEBHOOK_URL=https://n8n.yourdomain.com/
```

- **Must** end with a trailing slash.
- **Must** match exactly the domain Coolify proxies to the container.
- Test a webhook trigger URL from the n8n UI after deployment to confirm it is reachable.

---

## 9. Basic Security Recommendations

| Recommendation | Why |
|---|---|
| Use a strong, unique `N8N_BASIC_AUTH_PASSWORD` (16+ chars) | Prevents brute-force on the login page |
| Generate a random `N8N_ENCRYPTION_KEY` with `openssl rand -hex 32` | Protects stored credentials at rest |
| Enable HTTPS via Coolify's automatic Let's Encrypt (Section 6) | Encrypts credentials in transit |
| Keep `N8N_LOG_LEVEL=warn` in production | Avoids leaking workflow data in logs |
| Back up `/data/n8n` daily with a `cron` job | Protects workflows and credentials against disk failure |
| Enable Coolify's **Firewall** to block port `5678` directly | Force all traffic through the HTTPS reverse-proxy |

Example daily backup cron (run `crontab -e` on the VPS):

```bash
0 2 * * * mkdir -p /backups && tar -czf /backups/n8n-$(date +\%F).tar.gz /data/n8n && \
          find /backups -name "n8n-*.tar.gz" -mtime +7 -delete
```

---

## 10. Lightweight Settings for a Small VPS (1 CPU / 4 GB RAM)

| Setting | Value | Why |
|---|---|---|
| `EXECUTIONS_DATA_PRUNE=true` | `true` | Deletes old execution history; keeps SQLite small |
| `EXECUTIONS_DATA_MAX_AGE` | `72` (hours) | Keep only the last 3 days of execution logs |
| Coolify → Resource Limits → Memory | `512m` | Prevents n8n from consuming all RAM |
| Coolify → Resource Limits → CPU | `0.4` | Combined with the FastAPI app's limit (`0.4`) stays within 1 CPU total |
| n8n execution mode | `regular` (default) | No separate worker process; fine for 1 CPU |
| Avoid installing large n8n community nodes | — | Each node adds startup time and RAM |

> With both the FastAPI app (≤512 MB) and n8n (≤512 MB) running, the VPS
> still has ~1 GB free for Coolify itself and the OS — well within the 4 GB limit.

---

## 11. Post-Deployment Test Checklist

After Coolify reports the container as **Running**, run these checks
(replace `n8n.yourdomain.com` with your actual domain or `<vps-ip>:5678`):

### 11.1 Health check endpoint
```bash
curl -s https://n8n.yourdomain.com/healthz
# Expected: "OK"  (plain text, HTTP 200)
```

### 11.2 UI is reachable
Open in your browser:
```
https://n8n.yourdomain.com
```
You should see the n8n login screen or the setup wizard.

### 11.3 Create owner account
1. Complete the setup wizard (name, email, password).
2. You land on the n8n canvas — deployment is successful.

### 11.4 Create a simple test workflow
1. Click **+ New Workflow**.
2. Add a **Webhook** trigger node.
3. Copy the **Test URL** shown in the node.
4. From your terminal, call it:
   ```bash
   curl -s -X POST "<test-webhook-url>"
   # Expected: the Webhook node shows "Waiting for test event..."
   # then reports the received request after you send the curl
   ```

### 11.5 Verify TLS
```bash
curl -v https://n8n.yourdomain.com/healthz 2>&1 | grep "SSL certificate verify ok"
```

### 11.6 Check persistent storage survived a restart
1. Create a simple workflow and save it.
2. In Coolify, restart the n8n container.
3. After it comes back up, confirm the workflow is still present.

### 11.7 Verify webhook URL is correct
1. In a workflow, add a **Webhook** trigger, activate the workflow (toggle top-right).
2. The **Production URL** shown should start with `https://n8n.yourdomain.com/webhook/`.
3. If it shows `localhost` or `127.0.0.1`, recheck `WEBHOOK_URL` in env vars.

---

## 12. Troubleshooting

| Symptom | Fix |
|---|---|
| Container keeps restarting | Check **Logs** in Coolify; usually a missing env var or wrong volume permissions (`chown 1000:1000 /data/n8n`) |
| `/healthz` returns 502 | n8n hasn't started yet — wait 30s and retry; it can be slow on first boot |
| "Encryption key missing" error | `N8N_ENCRYPTION_KEY` is not set — add it in Coolify env vars |
| Webhook URL shows `localhost` | `WEBHOOK_URL` is not set or doesn't match the public domain |
| Credentials lost after redeploy | Volume not mounted — follow **Section 5** above |
| Login page not appearing | Basic auth not active and owner account not created yet — check logs |
| Out-of-memory crash | Lower `EXECUTIONS_DATA_MAX_AGE`, add memory limit in Coolify, or prune old executions manually |
