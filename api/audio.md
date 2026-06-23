# Audio

Text-to-speech and speech-to-text endpoints.

## Text to Speech

`POST /v1/audio/speech`

Convert text to spoken audio.

### Request

```json
{
  "model": "auto/tts",
  "input": "Hello, welcome to JarvisClaw!",
  "voice": "sarah"
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | TTS model ID (`auto/tts`, `elevenlabs/flash-v2.5`, `elevenlabs/v3`, `elevenlabs/multilingual-v2`, `elevenlabs/turbo-v2.5`) |
| `input` | string | Yes | Text to convert to speech (max 4096 chars) |
| `voice` | string | Yes | Voice alias. ElevenLabs voices: `sarah`, `george`, `charlie`, `charlotte`, `aria`. Query available voices via `GET /v1/audio/voices`. |
| `response_format` | string | No | Audio format: `mp3` (default), `opus`, `aac`, `flac` |
| `speed` | float | No | Speed multiplier (0.25 to 4.0). Default: `1.0` |

### Response

Returns JSON with a `data[].url` field pointing to the generated audio file.

```json
{
  "created": 1782225665,
  "model": "elevenlabs/flash-v2.5",
  "data": [
    {
      "url": "https://cdn.jarvisclaw.ai/media/media/audios/2026/06/23/QshFG9Df.mp3",
      "format": "mp3",
      "characters": 74
    }
  ]
}
```

Download the audio from `data[0].url`. The file is hosted on CDN and available for 48 hours.

### Example

::: code-group

```python [Raw HTTP]
import requests

BASE = "https://api.jarvisclaw.ai/v1"
HEADERS = {"Authorization": "Bearer sk-your-api-key", "Content-Type": "application/json"}

# Generate speech — returns JSON with audio URL
resp = requests.post(f"{BASE}/audio/speech", headers=HEADERS, json={
    "model": "auto/tts",
    "input": "Hello, welcome to JarvisClaw!",
    "voice": "sarah",
})
data = resp.json()
audio_url = data["data"][0]["url"]

# Download the audio file
audio = requests.get(audio_url)
with open("output.mp3", "wb") as f:
    f.write(audio.content)
```

```python [JarvisClaw SDK (API Key)]
from jarvisclaw import AudioClient

audio = AudioClient(api_key="sk-your-api-key")

# Text-to-speech
result = audio.speech("Hello, welcome to JarvisClaw!", voice="sarah")

# Save to file
with open("output.mp3", "wb") as f:
    f.write(result.content)

print(result.content_type)  # e.g. "audio/mpeg"
```

```python [JarvisClaw SDK (x402 Agent)]
from jarvisclaw import AudioClient

# ─── Option A: Base chain (EVM) ───
audio = AudioClient(private_key="0x<evm-private-key>")

# ─── Option B: Solana ───
# audio = AudioClient(private_key="<solana-bs58-keypair>")

# Text-to-speech with explicit model
result = audio.speech("Hello, welcome to JarvisClaw!", model="auto/tts", voice="sarah")

with open("output.mp3", "wb") as f:
    f.write(result.content)
```

```go [Go (API Key)]
package main

import (
    "context"
    "fmt"
    "os"
    jc "github.com/api-jarvisclaw/go-sdk"
)

func main() {
    ctx := context.Background()
    ac, _ := jc.NewAudioClient(jc.WithAPIKey("sk-your-api-key"))

    // Text-to-speech
    result, _ := ac.Speech(ctx, "Hello, welcome to JarvisClaw!",
        jc.WithVoice("sarah"))

    // Save to file
    os.WriteFile("output.mp3", result.Data, 0644)
    fmt.Printf("Content-Type: %s\n", result.ContentType)
}
```

```go [Go (x402 Agent)]
package main

import (
    "context"
    "fmt"
    "os"
    jc "github.com/api-jarvisclaw/go-sdk"
)

func main() {
    ctx := context.Background()

    // x402 Agent wallet — pays per-call via USDC on Base (Chain ID 8453)
    ac, _ := jc.NewAudioClient(jc.WithPrivateKey("0x<evm-private-key>"))

    // Text-to-speech
    result, _ := ac.Speech(ctx, "Hello, welcome to JarvisClaw!",
        jc.WithVoice("sarah"))

    os.WriteFile("output.mp3", result.Data, 0644)
    fmt.Printf("Content-Type: %s\n", result.ContentType)
}
```

```bash [cURL]
# Returns JSON with audio URL (not raw bytes)
curl https://api.jarvisclaw.ai/v1/audio/speech \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"model": "auto/tts", "input": "Hello!", "voice": "sarah"}'
# → {"data": [{"url": "https://cdn.jarvisclaw.ai/.../audio.mp3", "format": "mp3"}]}

# Then download the audio file from the URL:
curl -o output.mp3 "https://cdn.jarvisclaw.ai/.../audio.mp3"
```

:::

## Speech to Text (Transcription)

`POST /v1/audio/transcriptions`

Transcribe audio files to text.

### Request (multipart/form-data)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | file | Yes | Audio file (mp3, mp4, mpeg, mpga, m4a, wav, webm) |
| `model` | string | Yes | STT model ID (`whisper-1`) |
| `language` | string | No | ISO-639-1 language code (improves accuracy) |
| `response_format` | string | No | `json` (default), `text`, `srt`, `verbose_json`, `vtt` |
| `temperature` | float | No | Sampling temperature (0-1) |

### Response

```json
{
  "text": "Hello, this is a transcription of the audio file."
}
```

### Example

::: code-group

```python [OpenAI SDK]
from openai import OpenAI

client = OpenAI(
    base_url="https://api.jarvisclaw.ai/v1",
    api_key="sk-your-api-key",
)

with open("recording.mp3", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
    )
    print(transcript.text)
```

```python [JarvisClaw SDK (API Key)]
from jarvisclaw import AudioClient

audio = AudioClient(api_key="sk-your-api-key")

# Transcribe audio file
text = audio.transcribe("recording.mp3", model="whisper-1")
print(text)

# With language hint for better accuracy
text = audio.transcribe("recording.mp3", model="whisper-1", language="en")
print(text)
```

```python [JarvisClaw SDK (x402 Agent)]
from jarvisclaw import AudioClient

# x402 Agent wallet — pays per-call via USDC on Base
audio = AudioClient(private_key="0x<evm-private-key>")

# Transcribe audio file
text = audio.transcribe("recording.mp3", model="whisper-1")
print(text)
```

```bash [cURL]
curl https://api.jarvisclaw.ai/v1/audio/transcriptions \
  -H "Authorization: Bearer sk-your-api-key" \
  -F file="@recording.mp3" \
  -F model="whisper-1"
```

:::

## Music Generation

`POST /v1/audio/music`

Generate music from a text prompt using the JarvisClaw SDK.

### Example

::: code-group

```python [JarvisClaw SDK (API Key)]
from jarvisclaw import AudioClient

audio = AudioClient(api_key="sk-your-api-key")

# Generate music from a prompt
result = audio.music("upbeat electronic track with synth bass", model="auto/music")

# Save the generated music
with open("track.mp3", "wb") as f:
    f.write(result.content)

# Instrumental only (no vocals)
result = audio.music("calm piano jazz", instrumental=True)
with open("jazz.mp3", "wb") as f:
    f.write(result.content)
```

```python [JarvisClaw SDK (x402 Agent)]
from jarvisclaw import AudioClient

audio = AudioClient(private_key="0x<evm-private-key>")

# Generate music (waits for completion by default)
result = audio.music("epic orchestral battle theme", wait=True)
with open("epic.mp3", "wb") as f:
    f.write(result.content)
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

    // Generate music
    result, _ := ac.Music(ctx, "upbeat electronic track with synth bass")
    fmt.Printf("Music URL: %s\n", result.URL)
    fmt.Printf("Job ID: %s, Status: %s\n", result.ID, result.Status)
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

    // x402 Agent wallet
    ac, _ := jc.NewAudioClient(jc.WithPrivateKey("0x<evm-private-key>"))

    result, _ := ac.Music(ctx, "calm piano jazz")
    fmt.Printf("Music URL: %s\n", result.URL)
}
```

:::

## Notes

- Maximum audio file size: 25 MB
- Supported audio formats: mp3, mp4, mpeg, mpga, m4a, wav, webm
- For long audio, split into segments under 25 MB each
