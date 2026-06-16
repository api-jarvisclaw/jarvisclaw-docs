# RealFace & Virtual Portrait

Phone-based liveness verification and virtual character enrollment. Generates verified `asset_id` tokens for use with Seedance 2.0 video generation.

## Base URLs

```
/v1/marketplace/realface/*    — Liveness verification
/v1/marketplace/portrait/*    — Virtual character enrollment
```

## Endpoints

| Method | Endpoint | Description | Price |
|--------|----------|-------------|-------|
| POST | `/v1/marketplace/realface/init` | Initialize liveness session | Free (10/hour limit) |
| GET | `/v1/marketplace/realface/status` | Poll session completion | Free |
| POST | `/v1/marketplace/realface/enroll` | Finalize enrollment | $0.01 |
| POST | `/v1/marketplace/portrait/enroll` | Enroll virtual character | $0.01 |

## How It Works

1. **Init** — Create a liveness session, get a verification URL
2. **User completes challenge** — Nod + blink on phone camera
3. **Poll status** — Wait for liveness completion
4. **Enroll** — Finalize and receive an `asset_id`
5. **Use asset_id** — Pass to Seedance 2.0 for identity-consistent video generation

## Initialize Liveness

`POST /v1/marketplace/realface/init`

Start a phone-based liveness verification session.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `redirect_url` | string | No | URL to redirect after liveness completion |
| `webhook_url` | string | No | URL for completion callback |

### Response

```json
{
  "session_id": "rf_sess_abc123",
  "verification_url": "https://verify.jarvisclaw.ai/liveness/rf_sess_abc123",
  "qr_code_url": "https://verify.jarvisclaw.ai/qr/rf_sess_abc123.png",
  "expires_at": "2025-06-01T12:10:00Z"
}
```

## Poll Status

`GET /v1/marketplace/realface/status`

Check whether the user has completed the liveness challenge.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `session_id` | string | Yes | Session ID from init |

### Response

```json
{
  "session_id": "rf_sess_abc123",
  "status": "completed",
  "liveness_score": 0.98
}
```

Status values: `pending`, `in_progress`, `completed`, `expired`, `failed`

## Finalize Enrollment

`POST /v1/marketplace/realface/enroll`

After liveness is completed, finalize enrollment to generate an `asset_id`.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `session_id` | string | Yes | Completed liveness session ID |
| `label` | string | No | Optional label for the asset |

### Response

```json
{
  "asset_id": "asset_rf_xyz789",
  "label": "John's face",
  "created_at": "2025-06-01T12:05:00Z",
  "liveness_verified": true
}
```

## Virtual Portrait Enrollment

`POST /v1/marketplace/portrait/enroll`

Enroll a virtual character (illustration, avatar, 3D render) without liveness verification.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image_url` | string | Yes | URL of the character image |
| `label` | string | No | Optional label for the asset |

### Response

```json
{
  "asset_id": "asset_pt_def456",
  "label": "Anime character",
  "created_at": "2025-06-01T12:05:00Z",
  "liveness_verified": false
}
```

## Examples

::: code-group

```python [Python]
import requests
import time

BASE_RF = "https://api.jarvisclaw.ai/v1/marketplace/realface"
BASE_PT = "https://api.jarvisclaw.ai/v1/marketplace/portrait"
HEADERS = {
    "Authorization": "Bearer sk-your-api-key",
    "Content-Type": "application/json",
}

# --- RealFace Flow ---

# 1. Initialize liveness session
resp = requests.post(f"{BASE_RF}/init", headers=HEADERS, json={
    "webhook_url": "https://yourapp.com/webhook/liveness",
})
session = resp.json()
print(f"Send this URL to user: {session['verification_url']}")

# 2. Poll until completed
while True:
    resp = requests.get(f"{BASE_RF}/status", headers=HEADERS, params={
        "session_id": session["session_id"],
    })
    status = resp.json()
    if status["status"] == "completed":
        break
    time.sleep(3)

# 3. Enroll to get asset_id
resp = requests.post(f"{BASE_RF}/enroll", headers=HEADERS, json={
    "session_id": session["session_id"],
    "label": "User face",
})
asset_id = resp.json()["asset_id"]
print(f"Asset ID for Seedance: {asset_id}")

# --- Virtual Portrait ---

resp = requests.post(f"{BASE_PT}/enroll", headers=HEADERS, json={
    "image_url": "https://example.com/character.png",
    "label": "Game character",
})
print(f"Portrait asset: {resp.json()['asset_id']}")
```

```bash [cURL]
# Initialize liveness
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/realface/init \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"webhook_url": "https://yourapp.com/webhook"}'

# Poll status
curl "https://api.jarvisclaw.ai/v1/marketplace/realface/status?session_id=rf_sess_abc123" \
  -H "Authorization: Bearer sk-your-api-key"

# Enroll after completion
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/realface/enroll \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "rf_sess_abc123", "label": "User face"}'

# Virtual portrait enrollment
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/portrait/enroll \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/avatar.png", "label": "Avatar"}'
```

:::

## Notes

- Liveness challenge requires user to perform nod and blink gestures on phone camera
- Init sessions expire after 10 minutes
- Rate limit on init: 10 sessions per hour per API key
- `asset_id` is permanent and can be reused across multiple Seedance 2.0 generations
- Virtual portraits do not require liveness — use for illustrated/animated characters
- RealFace is designed for consent-based enrollment only
