# n8n First Workflow — Publish to Telegram via Rooz API

A complete, step-by-step guide for building your first n8n workflow that
sends content to the **Rooz Social Publishing Server** and publishes it to
Telegram.

No prior n8n experience required. Every node is explained from scratch.

---

## Workflow Overview

```
[Manual Trigger]
       │
       ▼
[Set Node — prepare content]
       │
       ▼
[HTTP Request — POST /api/publish]
       │
       ▼
[HTTP Request — POST /api/publish/telegram/send-now]
       │
       ▼
[Done — check output panel]
```

**What this workflow does:**

1. You click a button to start it.
2. A Set node prepares the platform and message content.
3. The first HTTP Request saves a publish job to the database.
4. The second HTTP Request sends the message live to Telegram.
5. You see the result in the n8n output panel.

**Time to build:** ~10 minutes  
**Difficulty:** Beginner  
**VPS impact:** Minimal — two lightweight HTTP calls

---

## Prerequisites

Before building the workflow, confirm these are working:

- [ ] n8n is running at `https://n8n.yourdomain.com`
- [ ] FastAPI is running at `https://api.yourdomain.com`
- [ ] `GET https://api.yourdomain.com/health` returns `{"status": "ok"}`
- [ ] `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are set in Coolify env vars
- [ ] Your Telegram bot has been added to your channel or group

> **Quick test:** Open `https://api.yourdomain.com/health` in your browser.
> If you see `{"status": "ok"}`, the API is reachable.

---

## Step-by-Step: Building the Workflow

### Step 1 — Create a New Workflow

1. Log in to n8n at `https://n8n.yourdomain.com`.
2. Click **+ New Workflow** in the top-right corner.
3. Name it: `Publish to Telegram`.
4. Click **Save** (top right).

You now have a blank canvas.

---

### Step 2 — Add the Manual Trigger Node

The Manual Trigger lets you start the workflow by clicking a button.
It is the simplest trigger for testing.

**How to add it:**

1. Click the **+** button in the centre of the canvas (or the **Add first step** button).
2. In the search box, type `Manual`.
3. Select **Manual Trigger**.

**Configuration:**

No configuration needed. The Manual Trigger has no settings.

It will look like this on the canvas:
```
[ ▶ Manual Trigger ]
```

> **Why Manual Trigger?**  
> It is the safest way to test a workflow. You control exactly when it runs.
> Once the workflow works, you can replace it with a Schedule or Webhook trigger.

---

### Step 3 — Add the Set Node

The Set node prepares the data (payload) that will be sent to the API.
Think of it as filling in a form before submitting it.

**How to add it:**

1. Click the **+** icon that appears to the right of the Manual Trigger node.
2. In the search box, type `Set`.
3. Select **Set**.

**Configuration:**

Inside the Set node, set the **Mode** to **Manual Mapping**, then add two fields:

| Field Name | Type | Value |
|---|---|---|
| `platform` | String | `telegram` |
| `content` | String | `Hello from n8n! 🚀 Sent at {{ $now.toFormat('yyyy-MM-dd HH:mm') }}` |

**How to add a field:**

1. Click **+ Add field**.
2. Set **Name** to `platform`, **Type** to `String`, **Value** to `telegram`.
3. Click **+ Add field** again.
4. Set **Name** to `content`, **Type** to `String`, **Value** to the message above.

**Why this node?**

Having a Set node at the top means you only need to change the message content
in one place. The HTTP Request nodes downstream pick up these values automatically.

**After configuring**, the Set node output will look like:
```json
{
  "platform": "telegram",
  "content": "Hello from n8n! 🚀 Sent at 2026-03-14 09:00"
}
```

---

### Step 4 — Add the First HTTP Request Node (Save Publish Job)

This node calls `POST /api/publish` to save the job to the FastAPI database
with status `pending`.

**How to add it:**

1. Click the **+** icon to the right of the Set node.
2. Search for `HTTP Request`.
3. Select **HTTP Request**.

**Configuration:**

| Setting | Value |
|---|---|
| **Method** | `POST` |
| **URL** | `https://api.yourdomain.com/api/publish` |
| **Authentication** | None |
| **Body Content Type** | `JSON` |
| **Specify Body** | `Using Fields Below` |

**Body fields to add:**

Click **+ Add field** twice:

| Name | Value |
|---|---|
| `platform` | `{{ $json.platform }}` |
| `content` | `{{ $json.content }}` |

> The `{{ $json.platform }}` syntax reads the value from the previous Set node.
> This is called an **expression** in n8n.

**How to enter an expression:**

1. Click the field value box.
2. Click the small **Expression** toggle that appears on the right side.
3. Type `{{ $json.platform }}` (n8n autocompletes it).

**Expected response from the API:**

```json
{
  "id": 1,
  "platform": "telegram",
  "content": "Hello from n8n! 🚀 Sent at 2026-03-14 09:00",
  "status": "pending",
  "created_at": "2026-03-14T09:00:00"
}
```

The job `id` confirms the job was saved to the database.

---

### Step 5 — Add the Second HTTP Request Node (Send to Telegram Now)

This node calls `POST /api/publish/telegram/send-now` to deliver the message
directly to your Telegram channel.

**How to add it:**

1. Click the **+** icon to the right of the first HTTP Request node.
2. Search for `HTTP Request`.
3. Select **HTTP Request**.

**Configuration:**

| Setting | Value |
|---|---|
| **Method** | `POST` |
| **URL** | `https://api.yourdomain.com/api/publish/telegram/send-now` |
| **Authentication** | None |
| **Body Content Type** | `JSON` |
| **Specify Body** | `Using Fields Below` |

**Body fields to add:**

| Name | Value |
|---|---|
| `content` | `{{ $('Set').item.json.content }}` |

> **Why `$('Set').item.json.content` instead of `$json.content`?**  
> After the first HTTP Request, `$json` refers to the API response (which has
> `id`, `status`, etc.). To get the original content from the Set node,
> you reference it by node name: `$('Set').item.json.content`.

**Expected response from the API:**

```json
{
  "success": true,
  "platform": "telegram",
  "result": {
    "ok": true,
    "result": {
      "message_id": 42,
      "chat": { "id": -1001234567890, "type": "channel" },
      "text": "Hello from n8n! 🚀 Sent at 2026-03-14 09:00"
    }
  }
}
```

The `"success": true` confirms the Telegram message was delivered.

---

### Step 6 — Save and Test the Workflow

**Save:**

Click **Save** in the top-right corner (or press `Ctrl+S` / `Cmd+S`).

**Test:**

1. Click the **Manual Trigger** node to select it.
2. Click the **Execute** button (▶) that appears in the node panel.
   — OR —
   Click **Execute Workflow** in the top toolbar.
3. Watch each node light up green as it executes.

**Reading the output:**

- Click any node on the canvas after execution.
- The right panel shows **Input** and **Output** tabs.
- Green = success, Red = error.

---

### Step 7 — Verify in Telegram

After the workflow runs successfully:

1. Open your Telegram channel or group.
2. You should see the message: `Hello from n8n! 🚀 Sent at <timestamp>`.

If the message appears, your workflow is working end-to-end.

---

## Complete Node Configuration Reference

### Node 1 — Manual Trigger

| Setting | Value |
|---|---|
| Node type | Manual Trigger |
| Configuration | *(none required)* |

---

### Node 2 — Set

| Setting | Value |
|---|---|
| Node type | Set |
| Mode | Manual Mapping |

Fields:

```
platform = telegram
content  = Hello from n8n! 🚀 Sent at {{ $now.toFormat('yyyy-MM-dd HH:mm') }}
```

---

### Node 3 — HTTP Request (Save Job)

| Setting | Value |
|---|---|
| Node type | HTTP Request |
| Method | POST |
| URL | `https://api.yourdomain.com/api/publish` |
| Body Content Type | JSON |
| Body field: `platform` | `{{ $json.platform }}` |
| Body field: `content` | `{{ $json.content }}` |

Sends this JSON to the API:
```json
{
  "platform": "telegram",
  "content": "Hello from n8n! 🚀 Sent at 2026-03-14 09:00"
}
```

---

### Node 4 — HTTP Request (Send to Telegram)

| Setting | Value |
|---|---|
| Node type | HTTP Request |
| Method | POST |
| URL | `https://api.yourdomain.com/api/publish/telegram/send-now` |
| Body Content Type | JSON |
| Body field: `content` | `{{ $('Set').item.json.content }}` |

Sends this JSON to the API:
```json
{
  "content": "Hello from n8n! 🚀 Sent at 2026-03-14 09:00"
}
```

---

## Example Payloads

### Creating a publish job (Node 3 body)

Simple message:
```json
{
  "platform": "telegram",
  "content": "Good morning! ☀️ Daily update is live."
}
```

With emoji and line breaks:
```json
{
  "platform": "telegram",
  "content": "📢 New announcement\n\nCheck out our latest update.\n\n— Rooz Team"
}
```

With dynamic timestamp (n8n expression in the Set node):
```json
{
  "platform": "telegram",
  "content": "⏰ Scheduled post at {{ $now.toFormat('HH:mm') }} — Today's content is ready!"
}
```

### Sending directly to Telegram (Node 4 body)

Short alert:
```json
{
  "content": "🚨 Action required: please check the dashboard."
}
```

Formatted message:
```json
{
  "content": "📋 Weekly Summary\n\n✅ Posts published: 7\n✅ Telegram messages sent: 12\n\n— Rooz Bot"
}
```

---

## Expected API Responses

### POST /api/publish — success

```json
{
  "id": 1,
  "platform": "telegram",
  "content": "Hello from n8n!",
  "status": "pending",
  "created_at": "2026-03-14T09:00:00"
}
```

### POST /api/publish/telegram/send-now — success

```json
{
  "success": true,
  "platform": "telegram",
  "result": {
    "ok": true,
    "result": {
      "message_id": 42,
      "text": "Hello from n8n!"
    }
  }
}
```

### POST /api/publish/telegram/send-now — Telegram not configured

```json
{
  "detail": "TELEGRAM_BOT_TOKEN is not set"
}
```

HTTP status: `400 Bad Request`

---

## How to Test the Workflow

### Test 1 — Confirm the API is reachable

Before running the full workflow, test each node individually:

1. Click the first **HTTP Request** node (save job).
2. In the node settings, click **Test step**.
3. You should see a response with `"status": "pending"` and an `"id"`.

If it fails here, the URL is wrong or the API is down.

### Test 2 — Confirm Telegram is configured

1. Click the second **HTTP Request** node (send to Telegram).
2. Click **Test step**.
3. You should see `"success": true`.

If you see `400` with `"TELEGRAM_BOT_TOKEN is not set"`, the env vars need to
be added in Coolify (see Troubleshooting below).

### Test 3 — Run the full workflow

1. Click **Execute Workflow** in the toolbar.
2. All four nodes should turn green.
3. Check your Telegram channel for the message.

---

## Troubleshooting

### Problem: Node 3 returns HTTP 400

**Symptom:** First HTTP Request fails with `400 Bad Request`.

**Likely cause:** The JSON body is missing `platform` or `content`, or the
field names are misspelled.

**Fix:**
- Open Node 3 settings.
- Confirm **Body Content Type** is `JSON` (not `Form Data`).
- Confirm both `platform` and `content` fields are present.
- Confirm the expressions `{{ $json.platform }}` and `{{ $json.content }}` resolve
  to non-empty strings — click the **Test step** button and check the **Input** tab.

---

### Problem: Node 4 returns HTTP 400 — Telegram not configured

**Symptom:** Second HTTP Request fails with `{"detail": "TELEGRAM_BOT_TOKEN is not set"}`.

**Fix:**
1. In Coolify, open the FastAPI application.
2. Go to **Environment Variables**.
3. Add:
   ```
   TELEGRAM_BOT_TOKEN=<your bot token from @BotFather>
   TELEGRAM_CHAT_ID=<your channel or group chat ID>
   ```
4. Click **Save** and **Redeploy**.
5. Re-run the workflow.

> **How to get a bot token:** Message [@BotFather](https://t.me/BotFather) on Telegram → `/newbot`.  
> **How to get a chat ID:** Add your bot to a channel as admin, then send a message and use `https://api.telegram.org/bot<TOKEN>/getUpdates`.

---

### Problem: Node 3 or 4 returns HTTP 500

**Symptom:** Request returns `500 Internal Server Error`.

**Fix:**
- In Coolify, open the FastAPI application → **Logs**.
- Look for a Python traceback near the time of the error.
- Common causes: database write failure, Telegram API rate limit, malformed content.

---

### Problem: "Connection refused" or timeout

**Symptom:** n8n cannot reach the API at all.

**Fix:**
- Open `https://api.yourdomain.com/health` in a browser.
- If it does not load, the FastAPI container is down → check Coolify → **Applications** → status.
- Confirm the URL in the HTTP Request nodes starts with `https://`, not `http://`.
- Check for a typo in the domain name.

---

### Problem: Node 4 sends a different message than expected

**Symptom:** Telegram receives an empty message or the wrong text.

**Fix:**
- Open Node 4.
- Check the expression for `content`: it should be `{{ $('Set').item.json.content }}`.
- If you used `{{ $json.content }}` instead, it reads from the API response (Node 3 output),
  which does not contain the exact same content string — change it to reference the Set node.

---

### Problem: Workflow runs but Telegram receives nothing

**Symptom:** Node 4 returns `"success": true` but no Telegram message arrives.

**Fix:**
- Confirm the bot is a member (admin) of the target channel or group.
- Confirm `TELEGRAM_CHAT_ID` is the correct ID (use negative IDs for groups: `-1001234567890`).
- Send a test message via `curl`:
  ```bash
  curl -s -X POST https://api.yourdomain.com/api/publish/telegram/send-now \
    -H "Content-Type: application/json" \
    -d '{"content": "curl test"}'
  ```

---

### Problem: Swagger `/docs` works but n8n HTTP Request fails

**Symptom:** You can test the endpoint in the browser at `/docs`, but the n8n
HTTP Request node returns an error.

**Fix:**
- Swagger runs in your browser session; n8n calls the API programmatically.
- Confirm **Body Content Type** in the HTTP Request node is set to `JSON`.
  This sets the `Content-Type: application/json` header automatically.
- Without this header, FastAPI rejects the request with `422 Unprocessable Entity`.

---

## Common Mistakes

| Mistake | How to avoid it |
|---|---|
| Using `$json.content` in Node 4 instead of `$('Set').item.json.content` | After Node 3 runs, `$json` is the API response. Reference the Set node explicitly. |
| Forgetting to set Body Content Type to JSON | Always set it to `JSON` for POST requests with a JSON body. |
| Using `http://` instead of `https://` | Always use the HTTPS domain Coolify assigned. |
| Hardcoding the Telegram token inside the workflow | Store it in Coolify env vars instead. |
| Running the workflow before the API is reachable | Always confirm `/health` responds before building workflows. |
| Not saving the workflow before testing | Press `Ctrl+S` or `Cmd+S` before every test run. |

---

## Activating the Workflow

Once the workflow works correctly in test mode:

1. Click the **Active** toggle in the top-right corner of the workflow editor.
2. The toggle turns blue — the workflow is now live.
3. To change the trigger from Manual to automatic, replace the Manual Trigger
   with a **Schedule Trigger** (see next steps below).

---

## Next Steps

### Run on a schedule

Replace the Manual Trigger with a **Schedule Trigger**:

1. Click the Manual Trigger node.
2. Click **Change node** → **Schedule Trigger**.
3. Set interval to `Every 1 hour` (or your preferred schedule).
4. Save and activate.

The workflow will now run automatically without you clicking anything.

### Change the message dynamically

In the Set node, replace the static content with a dynamic expression.
For example, to include today's date:

```
📅 Daily update for {{ $now.toFormat('MMMM dd, yyyy') }}

Your scheduled content goes here.
```

### Add error handling

1. Right-click the second HTTP Request node.
2. Select **Add Error Output**.
3. Connect the error output to a new node (e.g., another Set node + HTTP Request to send
   an alert message to a different Telegram chat).

### Reuse this workflow for other platforms

When the FastAPI backend supports more platforms, only the Set node needs updating:

```json
{ "platform": "instagram", "content": "Caption for Instagram" }
{ "platform": "tiktok",    "content": "TikTok video description" }
```

The HTTP Request nodes stay exactly the same.

---

## Quick Reference Card

| Node | Type | Key settings |
|---|---|---|
| 1 | Manual Trigger | No settings |
| 2 | Set | `platform = telegram`, `content = <your message>` |
| 3 | HTTP Request | `POST https://api.yourdomain.com/api/publish` · JSON body with `platform` + `content` |
| 4 | HTTP Request | `POST https://api.yourdomain.com/api/publish/telegram/send-now` · JSON body with `content` |

**Expressions cheat sheet:**

| Expression | Reads from |
|---|---|
| `{{ $json.platform }}` | Output of the previous node |
| `{{ $('Set').item.json.content }}` | Output of a node named "Set" |
| `{{ $now.toFormat('yyyy-MM-dd HH:mm') }}` | Current timestamp |
| `{{ $runIndex }}` | How many times this node has run in the current execution |

---

## Related Guides

- `N8N_FASTAPI_INTEGRATION.md` — Full integration reference (all endpoints, security, architecture)
- `N8N_DEPLOYMENT.md` — How to deploy and configure n8n on Coolify
- `DEPLOYMENT.md` — How to deploy the FastAPI backend on Coolify
