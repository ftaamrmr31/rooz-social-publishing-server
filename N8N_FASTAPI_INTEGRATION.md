# n8n ↔ Rooz Social Publishing Server — Integration Guide

A practical, beginner-friendly guide for connecting
[n8n](https://n8n.io/) (your automation engine) with the
**Rooz Social Publishing Server** FastAPI backend running on the same
Hostinger VPS through Coolify.

No overengineering. No extra infrastructure. Just two containers talking to
each other on a small VPS.

---

## 1. Integration Architecture

```
┌─────────────────────────────────────────────────┐
│                  Hostinger VPS                   │
│                                                   │
│   ┌───────────────┐       ┌───────────────────┐  │
│   │     n8n        │──────▶│  Rooz FastAPI app │  │
│   │ (automation)  │ HTTP  │  (product backend) │  │
│   │ port 5678     │       │   port 8000        │  │
│   └───────────────┘       └───────────────────┘  │
│          │                         │              │
│     Coolify reverse-proxy (Traefik/Caddy)         │
└─────────────────────────────────────────────────┘
           │                         │
    n8n.yourdomain.com      api.yourdomain.com
```

### Roles

| Service | Role |
|---|---|
| **Rooz Social Publishing Server** (FastAPI) | **Product backend** — stores publish jobs in SQLite, sends messages to Telegram, manages users |
| **n8n** | **Automation engine** — triggers workflows on a schedule or on demand, calls the FastAPI API, orchestrates multi-step publishing logic |

Think of FastAPI as the database and messaging layer, and n8n as the brain that
decides *when* and *what* to publish.

---

## 2. Recommended Internal Communication

There are two ways n8n can reach the FastAPI app:

### Option A — Public domain URL (simplest MVP ✅ recommended)

Use the public HTTPS domain Coolify assigned to the FastAPI app:

```
https://api.yourdomain.com
```

**Pros:** Works immediately, no Coolify network config, always HTTPS.  
**Cons:** Traffic leaves the VPS to the public internet and comes back (tiny overhead on a small VPS).

### Option B — Internal Docker network URL

When both containers are in the same Coolify project/network, n8n can reach
FastAPI directly using the internal service name:

```
http://rooz-app:8000
```

> The exact service name depends on what you named the application inside
> Coolify. Check **Application → Settings → Internal hostname** in Coolify.

**Pros:** Faster, no public hop, no TLS overhead internally.  
**Cons:** Requires both services to be on the same Coolify network; slightly
more setup.

### MVP recommendation

**Start with Option A (public domain URL)**. It works out of the box and
requires zero extra Coolify configuration. Switch to Option B later if you
notice latency or want to keep traffic private.

---

## 3. FastAPI Endpoints Available for n8n

Base URL: `https://api.yourdomain.com` (replace with your actual domain)

| Method | Path | What it does |
|---|---|---|
| `GET` | `/health` | Returns server status — use this to confirm the app is running before other calls |
| `POST` | `/api/publish` | Creates a new publish job (saved to database) |
| `GET` | `/api/publish` | Returns all saved publish jobs |
| `POST` | `/api/publish/telegram/send-now` | Sends a message directly to Telegram immediately |

### 3.1 GET /health

```
GET https://api.yourdomain.com/health
```

Response `200 OK`:
```json
{
  "status": "ok",
  "service": "Rooz Social Publishing Server"
}
```

### 3.2 POST /api/publish

Creates and stores a publish job in the database with status `pending`.

```
POST https://api.yourdomain.com/api/publish
Content-Type: application/json
```

Request body:
```json
{
  "platform": "telegram",
  "content": "Hello world from n8n!"
}
```

Response `200 OK`:
```json
{
  "id": 1,
  "platform": "telegram",
  "content": "Hello world from n8n!",
  "status": "pending",
  "created_at": "2026-03-14T10:00:00"
}
```

### 3.3 GET /api/publish

Returns all saved publish jobs as a JSON array.

```
GET https://api.yourdomain.com/api/publish
```

Response `200 OK`:
```json
[
  {
    "id": 1,
    "platform": "telegram",
    "content": "Hello world from n8n!",
    "status": "pending",
    "created_at": "2026-03-14T10:00:00"
  }
]
```

### 3.4 POST /api/publish/telegram/send-now

Sends a message directly to Telegram **right now** (bypasses the database queue).

```
POST https://api.yourdomain.com/api/publish/telegram/send-now
Content-Type: application/json
```

Request body:
```json
{
  "content": "🚀 Automated message from n8n!"
}
```

Response `200 OK`:
```json
{
  "success": true,
  "platform": "telegram",
  "result": { ... }
}
```

---

## 4. First Workflow to Build in n8n

This step-by-step example sends a Telegram message and saves a publish job —
all from a single n8n workflow.

### Step 1 — Create a new workflow

1. Open `https://n8n.yourdomain.com` and log in.
2. Click **+ New Workflow** → name it `"Publish to Telegram"`.

### Step 2 — Add a Manual Trigger node

1. Click **+** (Add node) → search for **Manual Trigger**.
2. Add it to the canvas.
3. This lets you run the workflow by clicking a button — perfect for testing.

### Step 3 — Add a Set node (prepare the payload)

1. Click **+** after the Manual Trigger → search for **Set**.
2. Add it and configure:

| Field | Value |
|---|---|
| **Mode** | `Manual Mapping` |
| **platform** | `telegram` |
| **content** | `Hello from n8n! Posted at {{ $now }}` |

This node prepares the data you will POST to the API.

### Step 4 — Add an HTTP Request node (create publish job)

1. Click **+** after the Set node → search for **HTTP Request**.
2. Configure it:

| Field | Value |
|---|---|
| **Method** | `POST` |
| **URL** | `https://api.yourdomain.com/api/publish` |
| **Body Content Type** | `JSON` |
| **Body** | `{ "platform": "{{ $json.platform }}", "content": "{{ $json.content }}" }` |
| **Header: Content-Type** | `application/json` |

3. Click **Test step** and confirm you get a `200 OK` with a job `id` in the response.

### Step 5 (optional) — Add a second HTTP Request node (send now to Telegram)

1. Click **+** after the first HTTP Request → add another **HTTP Request**.
2. Configure it:

| Field | Value |
|---|---|
| **Method** | `POST` |
| **URL** | `https://api.yourdomain.com/api/publish/telegram/send-now` |
| **Body Content Type** | `JSON` |
| **Body** | `{ "content": "{{ $('Set').item.json.content }}" }` |
| **Header: Content-Type** | `application/json` |

### Step 6 — Check the output

1. Click **Execute Workflow**.
2. Click each node to see its output on the right panel.
3. The first HTTP Request should return a publish job with `"status": "pending"`.
4. The second HTTP Request should return `"success": true`.
5. Check your Telegram channel — the message should appear.

### Step 7 — Activate the workflow

When ready, flip the **Active** toggle (top right).
You can change the trigger to **Schedule** to run automatically (see Section 9).

---

## 5. Exact HTTP Request Node Configuration

### 5.1 Health check (use to test connectivity)

| Setting | Value |
|---|---|
| Method | `GET` |
| URL | `https://api.yourdomain.com/health` |
| Authentication | None |
| Headers | *(none required)* |

Expected response:
```json
{ "status": "ok", "service": "Rooz Social Publishing Server" }
```

### 5.2 Create a publish job

| Setting | Value |
|---|---|
| Method | `POST` |
| URL | `https://api.yourdomain.com/api/publish` |
| Body Content Type | `JSON` |
| Authentication | None |
| Headers | `Content-Type: application/json` |

JSON body:
```json
{
  "platform": "telegram",
  "content": "Your message text here"
}
```

Expected response:
```json
{
  "id": 42,
  "platform": "telegram",
  "content": "Your message text here",
  "status": "pending",
  "created_at": "2026-03-14T12:00:00"
}
```

### 5.3 Send directly to Telegram

| Setting | Value |
|---|---|
| Method | `POST` |
| URL | `https://api.yourdomain.com/api/publish/telegram/send-now` |
| Body Content Type | `JSON` |
| Authentication | None |
| Headers | `Content-Type: application/json` |

JSON body:
```json
{
  "content": "🔔 Automated alert from n8n"
}
```

Expected response:
```json
{
  "success": true,
  "platform": "telegram",
  "result": { "ok": true, "result": { ... } }
}
```

### 5.4 Get all publish jobs

| Setting | Value |
|---|---|
| Method | `GET` |
| URL | `https://api.yourdomain.com/api/publish` |
| Authentication | None |
| Headers | *(none required)* |

Expected response:
```json
[
  {
    "id": 1,
    "platform": "telegram",
    "content": "Hello world",
    "status": "pending",
    "created_at": "2026-03-14T10:00:00"
  }
]
```

---

## 6. Example Payloads

### 6.1 Create a publish job — basic

```json
{
  "platform": "telegram",
  "content": "Good morning! 🌅 Today's update is ready."
}
```

### 6.2 Create a publish job — with dynamic n8n expression

In the n8n HTTP Request body field:
```json
{
  "platform": "telegram",
  "content": "📢 New post at {{ $now.toFormat('yyyy-MM-dd HH:mm') }}"
}
```

### 6.3 Send directly to Telegram — short alert

```json
{
  "content": "🚨 Alert: something needs your attention!"
}
```

### 6.4 Send directly to Telegram — multi-line message

```json
{
  "content": "📋 Daily Summary\n\n✅ Jobs created: 5\n✅ Messages sent: 3\n\n— Rooz Bot"
}
```

> **Tip:** Use `\n` for newlines in Telegram messages.

---

## 7. Debugging and Troubleshooting

### 7.1 HTTP 400 Bad Request

**Cause:** The JSON body is missing a required field or has the wrong type.

**Fix:**
- Confirm the body contains both `"platform"` and `"content"` for `/api/publish`.
- Confirm the body contains `"content"` for `/api/publish/telegram/send-now`.
- Check for typos — field names are case-sensitive.
- In the n8n node, switch **Body** to `JSON` (not `Form Data`).

### 7.2 HTTP 500 Internal Server Error

**Cause:** Usually a missing Telegram configuration or an unhandled exception.

**Fix:**
- Check Coolify → FastAPI app → **Logs** for the Python traceback.
- Confirm `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are set in Coolify env vars.
- Test the Telegram endpoint manually with `curl` first (see DEPLOYMENT.md).

### 7.3 Wrong URL / 404 Not Found

**Cause:** The URL in the n8n HTTP Request node is incorrect.

**Fix:**
- Confirm the FastAPI app is reachable: open `https://api.yourdomain.com/health` in a browser.
- Check for extra or missing slashes — correct: `/api/publish`, not `/api/publish/`.
- If using internal URL, check the Coolify internal hostname is correct.

### 7.4 Container not reachable (connection refused / timeout)

**Cause:** The FastAPI container is down or the domain is not resolving.

**Fix:**
- In Coolify, check the FastAPI application status is **Running**.
- Run `curl -s https://api.yourdomain.com/health` from your VPS SSH session.
- If using internal URL, make sure both services are in the same Coolify network.

### 7.5 Telegram config missing (400 from `/telegram/send-now`)

**Cause:** `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID` env var is not set.

**Fix:**
- In Coolify → FastAPI application → **Environment Variables**, add:
  ```
  TELEGRAM_BOT_TOKEN=<your-token>
  TELEGRAM_CHAT_ID=<your-chat-id>
  ```
- Redeploy the FastAPI container after saving.
- To get a bot token: message [@BotFather](https://t.me/BotFather) on Telegram.
- To get chat ID: message [@userinfobot](https://t.me/userinfobot) on Telegram.

### 7.6 Swagger docs work but API call from n8n fails

**Cause:** Swagger (`/docs`) uses the browser's session; n8n calls the API
directly. The issue is usually a missing `Content-Type` header in n8n.

**Fix:**
- In the n8n HTTP Request node, ensure **Body Content Type** is set to `JSON`.
- This automatically adds the `Content-Type: application/json` header.

### 7.7 n8n workflow runs but no Telegram message arrives

**Cause:** The publish job was created (`/api/publish`) but the send-now
endpoint was not called, or the Telegram token is wrong.

**Fix:**
- In n8n, click the second HTTP Request node and check its output for errors.
- Make sure the second node calls `/api/publish/telegram/send-now`, not `/api/publish`.
- Verify `TELEGRAM_BOT_TOKEN` points to a working bot and the bot has been added to your channel/group.

---

## 8. Security Recommendations

| Recommendation | Why |
|---|---|
| **Do not expose n8n publicly without authentication** | Anyone who can reach n8n can trigger workflows and call your API |
| **Keep Basic Auth or owner account active on n8n** (see N8N_DEPLOYMENT.md §7) | First line of defense |
| **Always use HTTPS** for both the n8n UI and API calls | Prevents credentials and payloads from being intercepted |
| **Do not hardcode `TELEGRAM_BOT_TOKEN` in n8n workflow nodes** | Workflow JSON can be exported and shared; tokens embedded in it will leak |
| **Use n8n Credentials instead of hardcoded secrets** | Go to **Credentials → + Add Credential → Header Auth** and reference it in HTTP Request nodes via **Authentication → Predefined Credential** |
| **Restrict FastAPI to internal-only if possible** (Option B in Section 2) | If n8n is the only caller, there is no need for the API to be publicly accessible |
| **Add an API key header to FastAPI calls from n8n** | Even a simple shared secret in a custom header (`X-API-Key`) greatly reduces unauthorized access risk |
| **Keep `N8N_LOG_LEVEL=warn`** | Avoids logging request bodies (which may contain message content) in n8n logs |

### How to store secrets in n8n Credentials

1. In n8n, go to **Settings → Credentials → + Add Credential**.
2. Choose **Header Auth**.
3. Set **Name:** `Rooz API Key`, **Header Name:** `X-API-Key`, **Header Value:** `<your-secret>`.
4. In each HTTP Request node, set **Authentication → Predefined Credential → Rooz API Key**.

> On the FastAPI side, add an API key check middleware when you are ready.
> For now, keeping FastAPI internal (Docker network only) provides similar protection.

---

## 9. Suggested Next Workflow Ideas

### 9.1 Auto-publish Telegram from pending jobs

**Trigger:** Schedule (every 10 minutes)  
**Logic:**
1. `HTTP Request GET /api/publish` → get all jobs.
2. `Filter` node → keep only jobs with `"status": "pending"`.
3. `HTTP Request POST /api/publish/telegram/send-now` for each pending job.

### 9.2 Scheduled daily summary post

**Trigger:** Schedule (daily at 09:00)  
**Logic:**
1. `Set` node → compose a daily summary message.
2. `HTTP Request POST /api/publish/telegram/send-now` → send it.

### 9.3 AI-generated content before publishing

**Trigger:** Manual or Schedule  
**Logic:**
1. `HTTP Request` → call OpenAI / Groq API with a prompt.
2. `Set` node → extract the generated text from the response.
3. `HTTP Request POST /api/publish` → save the AI content as a pending job.
4. `HTTP Request POST /api/publish/telegram/send-now` → send it immediately.

> n8n has a built-in **OpenAI** node — use it instead of a raw HTTP Request
> for cleaner configuration.

### 9.4 Webhook-triggered publishing

**Trigger:** Webhook (external system pushes to n8n)  
**Logic:**
1. External tool (CMS, Zapier, another app) sends a POST to the n8n webhook URL.
2. n8n receives the payload and calls `/api/publish` with the content.
3. Optionally forward to Telegram immediately.

### 9.5 Future social media expansion

When the FastAPI backend adds Instagram, TikTok, or YouTube endpoints, the n8n
workflow pattern stays identical — only the `"platform"` value in the payload
changes:

```json
{ "platform": "instagram", "content": "Caption text here" }
{ "platform": "tiktok",    "content": "Video description" }
{ "platform": "youtube",   "content": "Video title and description" }
```

n8n can fan out to multiple platforms in parallel using the **Split In Batches**
or **Merge** nodes — no code changes required.

---

## Quick Reference

| Task | n8n node | URL |
|---|---|---|
| Check API is alive | HTTP Request GET | `https://api.yourdomain.com/health` |
| Save a publish job | HTTP Request POST | `https://api.yourdomain.com/api/publish` |
| List all publish jobs | HTTP Request GET | `https://api.yourdomain.com/api/publish` |
| Send to Telegram now | HTTP Request POST | `https://api.yourdomain.com/api/publish/telegram/send-now` |
| Browse API docs | Browser | `https://api.yourdomain.com/docs` |
