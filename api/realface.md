# RealFace & Virtual Portrait API

Enroll real people (with liveness verification) or synthetic characters for consistent identity in AI-generated videos. Creates a reusable `ta_xxx` asset_id for Seedance 2.0 video generation.

**Base URL:** `https://api.jarvisclaw.ai/v1/marketplace/realface`

## Authentication

Both methods are supported (server uses X402OrTokenAuth middleware):

| Method | Header | Description |
|--------|--------|-------------|
| API Key | `Authorization: Bearer sk-...` | Standard API key authentication |
| Private Key (x402) | Automatic via SDK | Agent wallet pays per-call with USDC |

## Endpoints

| Method | Endpoint | Description | Price |
|--------|----------|-------------|-------|
| POST | `/realface/init` | Initialize liveness session | Free (10/hour limit) |
| GET | `/realface/status` | Poll session status | Free |
| POST | `/realface/enroll` | Enroll verified face | $0.01 |
| POST | `/portrait/enroll` | Enroll virtual character | $0.01 |

## How It Works

1. **Init** — Create a liveness session, receive an H5 link
2. **User scans link** — Completes nod + blink challenge on phone camera (120s expiry)
3. **Poll status** — Wait for liveness verification to complete (`pending_validation` -> `active`)
4. **Enroll** — Submit face image + completed session to get a reusable `asset_id`
5. **Generate video** — Pass `asset_id` to Seedance 2.0 / 2.0-fast for identity-consistent output

For virtual characters (illustrations, avatars, 3D renders), skip steps 1-3 and use `/portrait/enroll` directly.

---

## Initialize Liveness Session

`POST /v1/marketplace/realface/init`

Start a phone-based liveness verification session. Returns an H5 link that the subject scans as a QR code to complete the challenge.

### Request

```json
{
  "name": "John Doe"
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Display name for the enrolled identity |

### Response

```json
{
  "object": "realface.init",
  "group_id": "legacy_rf_15458",
  "h5_link": "https://kyc.byteintl.com/?accessKeyId=...&configId=...&bytedToken=...",
  "status": "pending_validation",
  "expires_in_seconds": 120,
  "next_steps": {
    "1": "Have the real person scan h5_link as a QR code on their phone.",
    "2": "They complete a brief liveness check (nod + blink, ~1 minute).",
    "3": "Poll GET /v1/marketplace/realface/status?groupId=… until status === 'active'.",
    "4": "Call POST /v1/marketplace/realface/enroll with x402 payment to upload the face photo and finalize."
  }
}
```

::: warning H5 Link Expiry
The H5 link expires after **120 seconds** (`expires_in_seconds`). If the user doesn't complete the challenge in time, call `/init` again.
:::

---

## Poll Session Status

`GET /v1/marketplace/realface/status`

Check whether the user has completed the liveness challenge.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `groupId` | string | Yes | Group ID from init response |

### Response

```json
{
  "object": "realface.status",
  "group_id": "legacy_rf_15458",
  "status": "active"
}
```

Status values: `pending_validation`, `active`, `expired`, `failed`

---

## Enroll Verified Face

`POST /v1/marketplace/realface/enroll`

After liveness status becomes `active`, submit a reference photo to finalize enrollment. The photo must match the person who completed the liveness challenge.

### Request

```json
{
  "name": "John Doe",
  "image_url": "https://example.com/john-reference.jpg",
  "group_id": "legacy_rf_15458"
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Display name (must match init name) |
| `image_url` | string | Yes | Public HTTPS URL of reference face photo |
| `group_id` | string | Yes | Group ID from completed liveness session |

### Response

```json
{
  "object": "realface.enroll",
  "asset_id": "ta_rf_xyz789",
  "name": "John Doe",
  "group_id": "legacy_rf_15458"
}
```

---

## Enroll Virtual Portrait

`POST /v1/marketplace/portrait/enroll`

Enroll a virtual character (illustration, avatar, 3D render, AI-generated face) without liveness verification. No identity check — use for fictional characters.

### Request

```json
{
  "name": "Cyber Knight",
  "image_url": "https://example.com/character-portrait.png"
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Character name |
| `image_url` | string | Yes | Public HTTPS URL of character image |

### Response

```json
{
  "object": "portrait.enroll",
  "asset_id": "ta_pt_def456",
  "name": "Cyber Knight"
}
```

---

## Code Examples

::: code-group

```bash [cURL]
# 1. Initialize liveness session
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/realface/init \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe"}'

# 2. Poll status (replace group_id with value from init response)
curl "https://api.jarvisclaw.ai/v1/marketplace/realface/status?groupId=legacy_rf_15458" \
  -H "Authorization: Bearer sk-your-api-key"

# 3. Enroll verified face
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/realface/enroll \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "image_url": "https://example.com/john-photo.jpg",
    "group_id": "legacy_rf_15458"
  }'

# Virtual portrait (no liveness needed)
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/portrait/enroll \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cyber Knight",
    "image_url": "https://example.com/character.png"
  }'
```

```python [Python (API Key)]
from jarvisclaw import MarketplaceClient
import time

client = MarketplaceClient(api_key="sk-your-api-key")

# --- RealFace Flow ---

# 1. Initialize liveness session
session = client.call("realface", "/init", method="POST", json={
    "name": "John Doe",
})
print(f"H5 Link (show as QR): {session['h5_link']}")
print(f"Expires in: {session['expires_in_seconds']}s")

# 2. Poll until active (120s max)
group_id = session["group_id"]
while True:
    status = client.call("realface", "/status", params={
        "groupId": group_id,
    })
    if status["status"] == "active":
        print("Liveness verified!")
        break
    elif status["status"] in ("expired", "failed"):
        raise Exception(f"Liveness failed: {status['status']}")
    time.sleep(3)

# 3. Enroll face
asset = client.call("realface", "/enroll", method="POST", json={
    "name": "John Doe",
    "image_url": "https://example.com/john-photo.jpg",
    "group_id": group_id,
})
print(f"Asset ID for Seedance 2.0: {asset['asset_id']}")

# --- Virtual Portrait (skip liveness) ---

portrait = client.call("portrait", "/enroll", method="POST", json={
    "name": "Cyber Knight",
    "image_url": "https://example.com/character.png",
})
print(f"Portrait asset: {portrait['asset_id']}")
```

```python [Python (x402 Agent)]
from jarvisclaw import MarketplaceClient
import time

# x402 agent — pays per call with USDC, no API key needed
client = MarketplaceClient(private_key="0x<agent-wallet-private-key>")

# 1. Initialize liveness session
session = client.call("realface", "/init", method="POST", json={
    "name": "John Doe",
})
print(f"H5 Link (show as QR): {session['h5_link']}")

# 2. Poll status
group_id = session["group_id"]
while True:
    status = client.call("realface", "/status", params={
        "groupId": group_id,
    })
    if status["status"] == "active":
        break
    elif status["status"] in ("expired", "failed"):
        raise Exception(f"Liveness failed: {status['status']}")
    time.sleep(3)

# 3. Enroll
asset = client.call("realface", "/enroll", method="POST", json={
    "name": "John Doe",
    "image_url": "https://example.com/john-photo.jpg",
    "group_id": group_id,
})
print(f"Asset ID: {asset['asset_id']}")

# Virtual portrait
portrait = client.call("portrait", "/enroll", method="POST", json={
    "name": "Cyber Knight",
    "image_url": "https://example.com/character.png",
})
print(f"Portrait: {portrait['asset_id']}")
```

```python [Python (Async)]
from jarvisclaw.aio import MarketplaceClient
import asyncio

async def main():
    client = MarketplaceClient(api_key="sk-your-api-key")

    # 1. Initialize liveness session
    session = await client.call("realface", "/init", method="POST", json={
        "name": "John Doe",
    })
    print(f"H5 Link: {session['h5_link']}")

    # 2. Poll until active
    group_id = session["group_id"]
    while True:
        status = await client.call("realface", "/status", params={
            "groupId": group_id,
        })
        if status["status"] == "active":
            break
        elif status["status"] in ("expired", "failed"):
            raise Exception(f"Liveness failed: {status['status']}")
        await asyncio.sleep(3)

    # 3. Enroll
    asset = await client.call("realface", "/enroll", method="POST", json={
        "name": "John Doe",
        "image_url": "https://example.com/john-photo.jpg",
        "group_id": group_id,
    })
    print(f"Asset ID: {asset['asset_id']}")

asyncio.run(main())
```

```go [Go (API Key)]
package main

import (
	"context"
	"fmt"
	"time"

	jarvisclaw "github.com/api-jarvisclaw/go-sdk"
)

func main() {
	ctx := context.Background()
	mc, _ := jarvisclaw.NewMarketplaceClient(jarvisclaw.WithAPIKey("sk-your-api-key"))

	// 1. Initialize liveness session
	session, err := mc.Post(ctx, "realface", "/init", map[string]string{
		"name": "John Doe",
	})
	if err != nil {
		panic(err)
	}
	groupID := session["group_id"].(string)
	fmt.Printf("H5 Link (show as QR): %s\n", session["h5_link"])

	// 2. Poll until active
	for {
		status, _ := mc.Call(ctx, "realface", "/status",
			jarvisclaw.WithParams(map[string]string{"groupId": groupID}))
		s := status["status"].(string)
		if s == "active" {
			fmt.Println("Liveness verified!")
			break
		}
		if s == "expired" || s == "failed" {
			panic("liveness failed: " + s)
		}
		time.Sleep(3 * time.Second)
	}

	// 3. Enroll face
	asset, err := mc.Post(ctx, "realface", "/enroll", map[string]string{
		"name":      "John Doe",
		"image_url": "https://example.com/john-photo.jpg",
		"group_id":  groupID,
	})
	if err != nil {
		panic(err)
	}
	fmt.Printf("Asset ID: %s\n", asset["asset_id"])
}
```

```go [Go (x402 Agent)]
package main

import (
	"context"
	"fmt"
	"time"

	jarvisclaw "github.com/api-jarvisclaw/go-sdk"
)

func main() {
	ctx := context.Background()

	// x402 agent — pays per call with USDC, no API key needed
	mc, _ := jarvisclaw.NewMarketplaceClient(
		jarvisclaw.WithPrivateKey("0x<agent-wallet-private-key>"),
	)

	// 1. Initialize liveness session
	session, _ := mc.Post(ctx, "realface", "/init", map[string]string{
		"name": "John Doe",
	})
	groupID := session["group_id"].(string)
	fmt.Printf("H5 Link: %s\n", session["h5_link"])

	// 2. Poll status
	for {
		status, _ := mc.Call(ctx, "realface", "/status",
			jarvisclaw.WithParams(map[string]string{"groupId": groupID}))
		if status["status"].(string) == "active" {
			break
		}
		time.Sleep(3 * time.Second)
	}

	// 3. Enroll
	asset, _ := mc.Post(ctx, "realface", "/enroll", map[string]string{
		"name":      "John Doe",
		"image_url": "https://example.com/john-photo.jpg",
		"group_id":  groupID,
	})
	fmt.Printf("Asset ID: %s\n", asset["asset_id"])
}
```

:::

---

## Errors

| Code | Error | Description |
|------|-------|-------------|
| 425 | `liveness_incomplete` | Liveness challenge not yet completed — keep polling |
| 422 | `face_match_failed` | Enrolled photo doesn't match the person who completed liveness |
| 429 | `rate_limited` | Exceeded 10 init sessions per hour |
| 400 | `invalid_image_url` | Image URL is not a valid public HTTPS URL or returned non-200 |
| 400 | `session_expired` | Liveness session expired (120s timeout) |
| 404 | `group_not_found` | Invalid or unknown group_id |

---

## Limitations

- **Seedance only** — Asset IDs only work with Seedance 2.0 and Seedance 2.0-fast models
- **120s H5 link expiry** — Verification link expires quickly; user must scan and complete promptly
- **Public HTTPS only** — `image_url` must be a publicly accessible HTTPS URL (no localhost, no HTTP)
- **No celebrity enrollment** — Cannot enroll public figures without their active participation in the liveness challenge
- **No deletion** — Once enrolled, asset IDs are permanent and cannot be revoked
- **Virtual portraits skip verification** — `/portrait/enroll` does not verify identity; anyone can enroll any image
- **Single face per image** — Reference photo must contain exactly one clearly visible face
- **Consent required** — RealFace is designed for consent-based enrollment only; the enrolled person must complete the liveness challenge themselves
