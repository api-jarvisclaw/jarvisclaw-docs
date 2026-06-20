
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

#### Response

```json
{
  "id": "47c11cc4-e210-4501-8e12-28269a665575",
  "created": 1717200000,
  "data": [
    {
      "url": "https://cdn.jarvisclaw.ai/media/media/images/2026/06/20/aef2a95d.png",
      "source_url": "data:image/png",
      "backed_up": true
    }
  ],
  "price": {
    "amount": "0.021000",
    "currency": "USD"
  }
}
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
curl -X POST https://api.jarvisclaw.ai/v1/images/generations \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-image-1",
    "prompt": "A futuristic cityscape at sunset with flying cars",
    "size": "1024x1024",
    "quality": "hd"
  }'
```

```python [Python (API Key)]
from openai import OpenAI

client = OpenAI(
    base_url="https://api.jarvisclaw.ai/v1",
    api_key="sk-your-api-key",
)

response = client.images.generate(
    model="openai/gpt-image-1",
    prompt="A futuristic cityscape at sunset with flying cars",
    size="1024x1024",
    quality="hd",
    n=1,
)

print(response.data[0].url)
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
