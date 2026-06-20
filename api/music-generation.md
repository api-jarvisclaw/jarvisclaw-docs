
# Music Generation API

Generate AI-composed music tracks from text prompts. Supports instrumental and vocal tracks with custom lyrics. Powered by MiniMax Music models.

**Base URL:** `https://api.jarvisclaw.ai/v1`

## Endpoints

### POST /v1/audio/generations

Generate a music track from a text prompt.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| model | string | Yes | Model identifier (`auto/music`, `minimax/music-2.5+`) |
| prompt | string | Yes | Description of the music to generate (genre, mood, tempo) |
| instrumental | boolean | No | Generate instrumental only (no vocals) (default: false) |
| lyrics | string | No | Custom lyrics for the track (ignored if instrumental is true) |
| duration_seconds | integer | No | Target duration in seconds (max 180) (default: 180) |

#### Request

```json
{
  "model": "auto/music",
  "prompt": "Upbeat electronic dance track with synth arpeggios and driving bass",
  "instrumental": true,
  "duration_seconds": 120
}
```

#### Response

```json
{
  "data": [
    {
      "url": "https://cdn.jarvisclaw.ai/audio/mus_abc123.mp3",
      "duration_seconds": 118,
      "lyrics": null
    }
  ]
}
```

## Pricing

| Model | Price | Notes |
|-------|-------|-------|
| auto/music | $0.1575/track | Auto-routes to best available |
| minimax/music-2.5+ | $0.1575/track | Up to ~3 minutes output |

## Code Examples

::: code-group

```bash [cURL]
curl -X POST https://api.jarvisclaw.ai/v1/audio/generations \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto/music",
    "prompt": "Chill lo-fi hip hop beat with rain sounds",
    "instrumental": true,
    "duration_seconds": 120
  }'
```

```python [Python (API Key)]
from jarvisclaw import AudioClient

audio = AudioClient(api_key="sk-your-api-key")

# Smart route (auto-selects best model)
result = audio.music("Chill lo-fi hip hop beat with rain sounds", instrumental=True)
print(f"Track URL: {result.url}")

# With explicit model
result = audio.music("Chill lo-fi hip hop beat with rain sounds",
    model="auto/music", instrumental=True)
print(f"Track URL: {result.url}")
```

```python [Python (x402 Agent)]
from jarvisclaw import AudioClient

# ─── Option A: Base chain (EVM) ───
# Hex private key → USDC on Base (Chain ID 8453)
audio = AudioClient(private_key="0x<evm-private-key>")

# ─── Option B: Solana ───
# Base58 keypair → USDC SPL on Solana mainnet
# audio = AudioClient(private_key="<solana-bs58-keypair>")

# SDK auto-detects chain from key format — no config needed

# Smart route (auto-selects best model)
result = audio.music("Chill lo-fi hip hop beat with rain sounds", instrumental=True)
print(f"Track URL: {result.url}")

# With explicit model
result = audio.music("Chill lo-fi hip hop beat",
    model="auto/music", instrumental=True)
print(f"Track URL: {result.url}")
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
    ac, _ := jc.NewAudioClient(jc.WithAPIKey("sk-your-api-key"))

    // Smart route (auto-selects best model)
    result, _ := ac.Music(ctx, "Chill lo-fi hip hop beat with rain sounds",
        jc.WithInstrumental(true))
    fmt.Printf("Track URL: %s\n", result.URL)

    // With explicit model
    result, _ = ac.Music(ctx, "Chill lo-fi hip hop beat with rain sounds",
        jc.WithAudioModel("auto/music"), jc.WithInstrumental(true))
    fmt.Printf("Track URL: %s\n", result.URL)
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
    ac, _ := jc.NewAudioClient(jc.WithPrivateKey("0x<evm-private-key>"))

    // Smart route (auto-selects best model)
    result, _ := ac.Music(ctx, "Chill lo-fi hip hop beat with rain sounds",
        jc.WithInstrumental(true))
    fmt.Printf("Track URL: %s\n", result.URL)

    // With explicit model
    result, _ = ac.Music(ctx, "Chill lo-fi hip hop beat",
        jc.WithAudioModel("auto/music"), jc.WithInstrumental(true))
    fmt.Printf("Track URL: %s\n", result.URL)
}
```

:::
