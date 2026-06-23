
# Image Generation API

Generate and edit images using state-of-the-art AI models. Supports text-to-image generation and image editing with masks. OpenAI-compatible format.

**Base URL:** `https://api.jarvisclaw.ai/v1`

## Endpoints

### POST /v1/images/generations

Generate images from a text prompt.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| model | string | No | Model identifier (e.g. "openai/gpt-image-1", "google/nano-banana") (default: openai/gpt-image-1) |
| prompt | string | Yes | Text description of the image to generate |
| size | string | No | Image dimensions (e.g. "1024x1024", "1792x1024") (default: 1024x1024) |
| quality | string | No | Image quality ("standard" or "hd") (default: standard) |
| n | integer | No | Number of images to generate (1-4) (default: 1) |

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
      "url": "https://cdn.jarvisclaw.ai/media/media/images/2026/06/23/7423018f.png",
      "source_url": "data:image/png",
      "backed_up": true
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
