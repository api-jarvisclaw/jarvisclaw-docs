
# Image Generation API

Generate and edit images using state-of-the-art AI models. Supports text-to-image generation and image editing with masks. OpenAI-compatible format.

**Base URL:** `https://api.jarvisclaw.ai/v1`

## Endpoints

### POST /v1/images/generations

Generate images from a text prompt.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| model | string | Yes | Model identifier (see Available Models below) |
| prompt | string | Yes | Text description of the image to generate |
| n | integer | No | Number of images to generate (default: 1) |
| size | string | No | Image dimensions (default: "1024x1024") |
| quality | string | No | "standard" or "hd" (model-dependent) |
| response_format | string | No | Output format: "url" or "b64_json" (default: "url") |
| style | string | No | Image style: "vivid" or "natural" (DALL·E 3 only) |
| user | string | No | Unique identifier for the end-user |
| background | string | No | Background mode: "transparent" or "opaque" (gpt-image-1+) |
| output_format | string | No | File format: "png", "jpeg", "webp" (gpt-image-1+) |
| output_compression | integer | No | Compression level 0–100 for lossy formats (jpeg/webp) |
| moderation | string | No | Content moderation level: "auto" or "low" |
| watermark | boolean | No | Whether to add an invisible watermark (default: true) |

#### Image Editing Parameters

These additional parameters apply to `/v1/images/edits`:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| images | array | Yes | Input image(s) for editing (base64 or URL) |
| mask | string/file | No | Mask image indicating areas to edit (transparent = edit region) |
| input_fidelity | string | No | How closely to follow the input: "low", "medium", "high" |
| partial_images | integer | No | Number of partial/progress images to return during generation |

#### Available Models

| Model ID | Provider | Sizes | Price |
|----------|----------|-------|-------|
| openai/gpt-image-1 | OpenAI | 1024x1024, 1536x1024, 1024x1536 | $0.021 |
| openai/gpt-image-2 | OpenAI | 1024x1024, 1536x1024, 1024x1536 | $0.063 |
| google/nano-banana | Google | 1024x1024 | $0.053 |
| google/nano-banana-pro | Google | 1024x1024, 2048x2048, 4096x4096 | $0.105 |
| zai/cogview-4 | Zhipu AI | 512x512 – 1440x1440 (flexible) | $0.015 |
| xai/grok-imagine-image | xAI | 1024x1024 | $0.021 |
| xai/grok-imagine-image-pro | xAI | 1024x1024 | $0.074 |

#### CogView-4 Sizes

`zai/cogview-4` supports flexible sizes (multiples of 16, max 1440×1440):

| Size | Use Case |
|------|----------|
| 512x512 | Thumbnails, icons |
| 768x768 | Social media |
| 1024x1024 | Standard (default) |
| 768x1344 | Portrait / mobile |
| 1344x768 | Landscape / banner |
| 1440x1440 | High resolution |

#### Hybrid Sync/Async Flow

This endpoint is **hybrid**: fast generations complete synchronously, slow ones switch to an async job you poll.

**Fast path (≤30s — most models):**
Generation finishes inline. The gateway settles payment and returns `200` with the standard `{ created, data: [...] }` body. Charged at this moment only.

**Slow path (>30s — e.g. `openai/gpt-image-2` under load):**
The gateway returns `202` with an async job envelope:

```json
{
  "id": "img_8f3a...",
  "object": "image.generation.job",
  "status": "queued",
  "model": "openai/gpt-image-2",
  "size": "1024x1024",
  "n": 1,
  "price": { "amount": "0.063000", "currency": "USD" },
  "payment_status": "verified",
  "created": 1706000000,
  "poll_url": "/api/v1/images/generations/img_8f3a..."
}
```

Poll `GET {poll_url}` every 2–5s with a payment header signed by the same wallet. Status transitions: `queued` → `in_progress` → `completed` | `failed`.

- `202` running: `{ id, object, status: "queued" | "in_progress", model, payment_status: "verified" }`
- `200` completed (charged here): standard body + `price` + `payment: { status: "settled", tx_hash, network }`
- `200` failed (not charged): `{ id, object, status: "failed", model, error, payment_status: "not_charged" }`

#### Settlement Guarantees

| Guarantee | Meaning |
|-----------|---------|
| `payment_status: "verified"` | Signature/authorization checked only — not a charge |
| Upstream fails (`status: "failed"`) | `payment_status: "not_charged"` — no USDC transferred |
| You never poll | Nothing settles; authorization expires. Not charged |
| Idempotent re-polls | Already-settled job returns same URLs (`payment.status: "already_settled"`) — never double-charged |

#### Request

```json
{
  "model": "openai/gpt-image-1",
  "prompt": "A futuristic cityscape at sunset with flying cars",
  "size": "1024x1024",
  "quality": "hd",
  "n": 1
}
```

#### Response (queued)

Image generation is asynchronous. The initial response returns a job with `status: "queued"` and a `poll_url`. Poll every 5 seconds until `status` becomes `"completed"`.

```json
{
  "id": "1f3d6e67-c286-4ed0-a9c1-683f197a7412",
  "object": "image.generation.job",
  "status": "queued",
  "model": "openai/gpt-image-2",
  "size": "1024x1024",
  "n": 1,
  "price": {
    "amount": "0.063000",
    "currency": "USD"
  },
  "payment_status": "verified",
  "created": 1782225494,
  "poll_url": "/v1/images/generations/1f3d6e67-c286-4ed0-a9c1-683f197a7412"
}
```

#### Polling: GET /v1/images/generations/:id

Poll the `poll_url` with your auth header every 5 seconds.

**In progress:**
```json
{
  "id": "1f3d6e67-c286-4ed0-a9c1-683f197a7412",
  "object": "image.generation.job",
  "status": "in_progress",
  "model": "openai/gpt-image-2"
}
```

**Completed:**
```json
{
  "id": "1f3d6e67-c286-4ed0-a9c1-683f197a7412",
  "object": "image.generation.job",
  "status": "completed",
  "model": "openai/gpt-image-2",
  "created": 1782225464,
  "data": [
    {
      "url": "https://cdn.jarvisclaw.ai/media/media/images/2026/06/23/7423018f.png"
    }
  ],
  "price": {
    "amount": "0.063000",
    "currency": "USD"
  }
}
```

::: tip
Typical generation time is 20-40 seconds. Jobs are retrievable for 48 hours after submission.
:::
```

### POST /v1/images/edits

Edit an image using a mask and prompt.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| image | file | Yes | The original image to edit (PNG, max 4MB) |
| mask | file | No | Mask image indicating areas to edit (transparent = edit area) |
| prompt | string | Yes | Description of the desired edit |
| model | string | No | Model to use for editing (default: openai/gpt-image-1) |
| size | string | No | Output image size (default: 1024x1024) |
| n | integer | No | Number of edited images to generate (default: 1) |

#### Request

```
POST /v1/images/edits
Content-Type: multipart/form-data

image: @photo.png
mask: @mask.png
prompt: "Replace the sky with a starry night"
model: "openai/gpt-image-1"
```

#### Response

```json
{
  "created": 1717200000,
  "data": [
    {
      "url": "https://cdn.jarvisclaw.ai/images/edit_xyz789.png"
    }
  ]
}
```

## Pricing

| Model | Price | Notes |
|-------|-------|-------|
| openai/gpt-image-1 | $0.021/image | 1024x1024, standard quality |
| google/nano-banana | $0.053/image | High-quality artistic generation |
| zai/cogview-4 | $0.015/image | Budget-friendly option |
| xai/grok-imagine-image | $0.021/image | xAI image generation |

## Code Examples

::: code-group

```bash [cURL]
# Step 1: Submit generation request
curl -X POST https://api.jarvisclaw.ai/v1/images/generations \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-image-1",
    "prompt": "A futuristic cityscape at sunset with flying cars",
    "size": "1024x1024",
    "quality": "hd"
  }'
# → {"id": "cbdf0464-...", "status": "queued", "poll_url": "/v1/images/generations/cbdf0464-..."}

# Step 2: Poll every 5s until completed
curl https://api.jarvisclaw.ai/v1/images/generations/cbdf0464-0ca8-476e-8bf9-e0d66dc21efa \
  -H "Authorization: Bearer sk-your-api-key"
# → {"status": "completed", "data": [{"url": "https://cdn.jarvisclaw.ai/...png"}]}
```

```python [Python (API Key)]
import requests
import time

BASE = "https://api.jarvisclaw.ai/v1"
HEADERS = {"Authorization": "Bearer sk-your-api-key", "Content-Type": "application/json"}

# Step 1: Submit
resp = requests.post(f"{BASE}/images/generations", headers=HEADERS, json={
    "model": "openai/gpt-image-1",
    "prompt": "A futuristic cityscape at sunset with flying cars",
    "size": "1024x1024",
    "quality": "hd",
})
job = resp.json()
poll_url = BASE.split("/v1")[0] + job["poll_url"]

# Step 2: Poll until completed (~20-40s)
while True:
    time.sleep(5)
    result = requests.get(poll_url, headers=HEADERS).json()
    if result["status"] == "completed":
        print(result["data"][0]["url"])
        break
```

```python [Python (x402 Agent)]
from jarvisclaw import ImageClient

# ─── Option A: Base chain (EVM) ───
# Hex private key → USDC on Base (Chain ID 8453)
image = ImageClient(private_key="0x<evm-private-key>")

# ─── Option B: Solana ───
# Base58 keypair → USDC SPL on Solana mainnet
# image = ImageClient(private_key="<solana-bs58-keypair>")

# SDK auto-detects chain from key format — no config needed

# Smart route (auto-selects best model)
result = image.generate("A futuristic cityscape at sunset with flying cars", size="1024x1024")
print(result.url)

# With explicit model
result = image.generate("A futuristic cityscape at sunset", model="openai/gpt-image-1", size="1024x1024")
print(result.url)
```

```go [Go (API Key)]
package main

import (
    "context"
    "fmt"
    jc "github.com/api-jarvisclaw/go-sdk"
)

func main() {
    ctx := context.Background()
    ic, _ := jc.NewImageClient(jc.WithAPIKey("sk-your-api-key"))

    // Smart route (auto-selects best model)
    img, _ := ic.Generate(ctx, "A futuristic cityscape at sunset with flying cars",
        jc.WithSize("1024x1024"))
    fmt.Printf("Image URL: %s\n", img.URL)

    // With explicit model
    img, _ = ic.Generate(ctx, "A futuristic cityscape at sunset",
        jc.WithImageModel("openai/gpt-image-1"), jc.WithSize("1024x1024"))
    fmt.Printf("Image URL: %s\n", img.URL)
}
```

```go [Go (x402 Agent)]
package main

import (
    "context"
    "fmt"
    jc "github.com/api-jarvisclaw/go-sdk"
)

func main() {
    ctx := context.Background()

    // x402 Agent wallet — pays per-call via USDC on Base (Chain ID 8453)
    ic, _ := jc.NewImageClient(jc.WithPrivateKey("0x<evm-private-key>"))

    // Smart route (auto-selects best model)
    img, _ := ic.Generate(ctx, "A futuristic cityscape at sunset with flying cars",
        jc.WithSize("1024x1024"))
    fmt.Printf("Image URL: %s\n", img.URL)

    // With explicit model
    img, _ = ic.Generate(ctx, "A futuristic cityscape at sunset",
        jc.WithImageModel("openai/gpt-image-1"), jc.WithSize("1024x1024"))
    fmt.Printf("Image URL: %s\n", img.URL)
}
```

:::
