# Music Generation

`POST /v1/audio/generations`

Generate original music tracks from text prompts with optional lyrics.

## Request

```json
{
  "model": "minimax-music-2.5",
  "prompt": "upbeat electronic dance track with synth leads",
  "instrumental": false,
  "lyrics": "[verse]\nLost in the neon glow...",
  "duration_seconds": 120
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | Music model ID (`minimax-music-2.5`) |
| `prompt` | string | Yes | Description of the desired music style, mood, and genre |
| `instrumental` | boolean | No | Generate instrumental only (no vocals). Default: `false` |
| `lyrics` | string | No | Song lyrics with structure tags (`[verse]`, `[chorus]`, `[bridge]`) |
| `duration_seconds` | integer | No | Track duration in seconds (max 180). Default: `60` |

## Pricing

| Item | Cost |
|------|------|
| Per track (up to 3 minutes) | $0.1575 |

## Response

```json
{
  "id": "music-gen-abc123",
  "object": "audio.generation",
  "created": 1700000000,
  "data": [
    {
      "url": "https://cdn.jarvisclaw.ai/audio/music-gen-abc123.mp3",
      "duration_seconds": 120
    }
  ]
}
```

## Examples

::: code-group

```python [Python]
import requests

resp = requests.post(
    "https://api.jarvisclaw.ai/v1/audio/generations",
    headers={
        "Authorization": "Bearer sk-your-api-key",
        "Content-Type": "application/json",
    },
    json={
        "model": "minimax-music-2.5",
        "prompt": "chill lo-fi hip hop beat with jazzy piano and vinyl crackle",
        "instrumental": True,
        "duration_seconds": 90,
    },
)

data = resp.json()
print(f"Track URL: {data['data'][0]['url']}")
```

```bash [cURL]
curl -X POST https://api.jarvisclaw.ai/v1/audio/generations \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "minimax-music-2.5",
    "prompt": "epic orchestral soundtrack with rising strings and dramatic percussion",
    "instrumental": true,
    "duration_seconds": 180
  }'
```

:::

## Lyrics Format

Use structure tags to guide song composition:

```
[intro]
(instrumental intro)

[verse]
Walking through the city lights
Every shadow comes alive

[chorus]
We are the dreamers tonight
Reaching for the satellite

[bridge]
Time slows down, the world fades out

[outro]
(fade out)
```

## Notes

- Generation takes 30-90 seconds depending on duration
- Audio URL expires after 24 hours — download promptly
- Output format: MP3, 44.1kHz stereo
- Maximum track duration: 3 minutes (180 seconds)
- When `lyrics` is provided and `instrumental` is `false`, the model generates vocals matching the lyrics
