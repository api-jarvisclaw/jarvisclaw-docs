---
outline: deep
---

# Video Generation API

Generate AI videos from text prompts or images. Three input modes: text-to-video, image-to-video (animate a photo), and character-consistent video (via RealFace/Virtual Portrait asset_id). Models: Sora 2 (4/8/12s, $0.10/s), Seedance 1.5 Pro ($0.46/5s, image-to-video only), Seedance 2.0 Fast ($1.19/5s, supports RealFace), Seedance 2.0 Pro ($1.49/5s, highest quality). Async workflow: submit → poll → get MP4 URL.

**Base URL:** `https://api.jarvisclaw.ai/v1`

## Endpoints

### POST /v1/videos/generations

Submit a video generation job.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| model | string | No | Video model ID (default: `xai/grok-imagine-video`). See Available Models below |
| prompt | string | Yes | Text description of the video to generate |
| duration_seconds | integer | No | Duration to bill for. Must respect model's max (Seedance: 5-15s, Sora: discrete {4,8,12}s). Default: model default |
| image_url | string | No | Seed image URL for image-to-video. For `azure/sora-2` the image is resized server-side and must not contain a human face. Mutually exclusive with `real_face_asset_id` |
| real_face_asset_id | string | No | Character/face reference asset (`ta_xxxxxx`) from Virtual Portrait or RealFace. Seedance 2.0/2.0-fast only. Mutually exclusive with `image_url` |
| resolution | string | No | `360p` / `480p` / `540p` / `720p` / `1080p` / `1K` / `2K` / `4K`. Seedance only — defaults to `720p`. Higher resolutions cost more tokens upstream |
| aspect_ratio | string | No | `adaptive` / `16:9` / `9:16` / `1:1` / `4:3` / `3:4` / `21:9` / `9:21`. Seedance only — ignored by Grok |
| generate_audio | boolean | No | Synced audio track. Seedance default: `true` for text-to-video, `false` for image/face-conditioned. Pass explicitly to override. Ignored by Grok |
| seed | integer | No | Reproducibility seed (Seedance). Same seed + prompt + params ≈ same clip |
| watermark | boolean | No | Embed upstream Seedance watermark. Off by default at the gateway |
| return_last_frame | boolean | No | Also return the last frame as a still — useful for chaining clips. Seedance only |

#### Request Examples

```json
// Text-to-video
{
  "model": "bytedance/seedance-2.0-pro",
  "prompt": "A cat playing piano in a dimly lit jazz bar",
  "duration_seconds": 5
}

// Image-to-video (animate a photo)
{
  "model": "bytedance/seedance-2.0-pro",
  "prompt": "Person waving hello and smiling",
  "image_url": "https://example.com/person-photo.jpg",
  "duration_seconds": 5
}

// With RealFace character (enrolled person)
{
  "model": "bytedance/seedance-2.0-fast",
  "prompt": "Person giving a presentation in a modern office",
  "real_face_asset_id": "ta_f85b20b9394e47be9502d819bee7929c",
  "duration_seconds": 5
}
```

#### Response

```json
{
  "id": "bytedance:video_ae260c45bdb7453c8bbe5a47",
  "object": "video.generation.job",
  "status": "queued",
  "model": "bytedance/seedance-2.0-pro",
  "duration_seconds": 5,
  "price": {
    "amount": "1.275372",
    "currency": "USD"
  },
  "payment_status": "verified",
  "created": 1717200000,
  "poll_url": "/v1/videos/generations/bytedance%3Avideo_ae260c45bdb7453c8bbe5a47?model=...&sig=..."
}
```

### GET /v1/videos/generations/:id

Poll video generation job status. Call every 5-10s until status is "completed" or "failed". Jobs remain retrievable for 48 hours after submission.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes | Job ID returned from the generation request |

#### Response (in progress)

```json
{
  "id": "bytedance:video_ae260c45bdb7453c8bbe5a47",
  "status": "in_progress",
  "created_at": 1717200000,
  "model": "bytedance/seedance-2.0-pro",
  "progress": 65,
  "elapsed_seconds": 42
}
```

#### Response (completed)

```json
{
  "id": "bytedance:video_ae260c45bdb7453c8bbe5a47",
  "object": "video.generation.job",
  "status": "completed",
  "model": "bytedance/seedance-2.0-pro",
  "created": 1717200000,
  "data": [
    {
      "url": "https://cdn.jarvisclaw.ai/media/media/videos/2026/06/20/video_ae260c45-15b82b3e.mp4",
      "source_url": "https://ark-acg-ap-southeast-1.tos-ap-southeast-1.volces.com/...",
      "duration_seconds": 5,
      "request_id": "video_ae260c45bdb7453c8bbe5a47",
      "backed_up": true
    }
  ],
  "usage": {
    "total_tokens": 108900,
    "token_source": "upstream"
  },
  "price": {
    "amount": "1.275372",
    "currency": "USD"
  }
}
```

## Pricing

### Base Price (720p default)

| Model | Price | Notes |
|-------|-------|-------|
| azure/sora-2 | $0.10/sec | 720p + synced audio, 4/8/12s clips |
| bytedance/seedance-1.5-pro | $0.46/5s | Image-to-video only, no RealFace support |
| bytedance/seedance-2.0-fast | $1.19/5s | 60-80s generation, supports RealFace |
| bytedance/seedance-2.0-pro | $1.49/5s | Highest quality, supports RealFace |
| Virtual Portrait enrollment | $0.01 (one-time) | See /docs/api/realface |
| RealFace enrollment | $0.01 (one-time) | See /docs/api/realface |

### Resolution Multiplier (Seedance)

Higher resolutions consume more tokens upstream. Approximate cost examples for Seedance 2.0 Pro:

| Resolution | Duration | Estimated Cost |
|------------|----------|----------------|
| 720p | 5s | ~$1.49 |
| 720p | 15s | ~$4.47 |
| 4K | 5s | ~$14.35 |
| 4K | 15s | ~$43.04 |

::: tip
4K generation costs approximately 9.6× the 720p base price due to upstream token scaling. Use `720p` for drafts and iterate before committing to high-resolution renders.
:::
## Code Examples

::: code-group

```bash [cURL]
# Text-to-video
curl -X POST https://api.jarvisclaw.ai/v1/videos/generations \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"model": "bytedance/seedance-2.0-pro", "prompt": "A cat playing piano in a jazz bar", "duration_seconds": 5}'

# Image-to-video (animate a photo)
curl -X POST https://api.jarvisclaw.ai/v1/videos/generations \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"model": "bytedance/seedance-2.0-pro", "prompt": "Person walks forward", "image_url": "https://example.com/photo.jpg", "duration_seconds": 5}'

# With RealFace character
curl -X POST https://api.jarvisclaw.ai/v1/videos/generations \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"model": "bytedance/seedance-2.0-fast", "prompt": "Person presenting", "real_face_asset_id": "ta_xxx", "duration_seconds": 5}'

# Poll status
curl https://api.jarvisclaw.ai/v1/videos/generations/vg_abc123 \
  -H "Authorization: Bearer sk-your-api-key"
```

```python [Python (API Key)]
from jarvisclaw import VideoClient

video = VideoClient(api_key="sk-your-api-key")

# ─── Blocking mode (SDK auto-polls, default 10min timeout) ───
job = video.generate("A cat playing piano in a jazz bar",
    model="bytedance/seedance-2.0-pro", duration=5)
print(f"Video URL: {job.url}")

# Image-to-video (animate a photo)
job = video.generate("Person waving hello",
    model="bytedance/seedance-2.0-pro",
    image_url="https://example.com/photo.jpg", duration=5)
print(f"Video URL: {job.url}")

# ─── Non-blocking mode (fire and forget) ───
job = video.generate("Ocean waves at sunset", wait=False)
print(f"Submitted: {job.id}")

# ... later (within 48 hours) ...
result = video.wait(job.id)
print(f"Video URL: {result.url}")

# ─── Timeout-safe pattern ───
job = video.generate("Flower blooming timelapse", poll_timeout=180)
if job.status == "timeout":
    # NOT lost — just retry later
    print(f"Progress: {job.raw.get('progress')}%")
    result = video.wait(job.id)  # continue polling
    print(result.url)
```
```python [Python (x402 Agent)]
from jarvisclaw import VideoClient

# ─── Base chain (EVM) — USDC on Base ───
video = VideoClient(private_key="0x<evm-private-key>")

# ─── Solana — USDC SPL on Solana mainnet ───
# video = VideoClient(private_key="<solana-bs58-keypair>")

# SDK auto-detects chain from key format

# Blocking (auto-polls until done, no charge until "completed")
job = video.generate("A cat playing piano in a jazz bar",
    model="bytedance/seedance-2.0-pro", duration=5)
print(f"Video URL: {job.url}")

# Non-blocking (submit and retrieve later)
job = video.generate("Ocean waves at sunset", wait=False)
print(f"Job ID: {job.id}")  # Save this

# Retrieve anytime within 48 hours
result = video.wait(job.id)
print(f"Video URL: {result.url}")

# Timeout-safe: progress is preserved
job = video.generate("Flower timelapse", poll_timeout=180)
if job.status == "timeout":
    print(f"Progress: {job.raw.get('progress')}%")
    result = video.wait(job.id)
    print(result.url)
```

```go [Go (API Key)]
package main

import (
    "context"
    "fmt"
    "time"
    jc "github.com/api-jarvisclaw/go-sdk"
)

func main() {
    ctx := context.Background()
    vc, _ := jc.NewVideoClient(jc.WithAPIKey("sk-your-api-key"))

    // Text-to-video (blocking — Generate waits by default)
    job, _ := vc.Generate(ctx, "A cat playing piano in a jazz bar",
        jc.WithVideoModel("bytedance/seedance-2.0-pro"), jc.WithDuration(5))
    fmt.Printf("Video URL: %s\n", job.URL)

    // Non-blocking mode
    job, _ = vc.Generate(ctx, "Ocean waves at sunset",
        jc.WithVideoModel("bytedance/seedance-2.0-fast"),
        jc.WithDuration(5), jc.WithWait(false))
    fmt.Printf("Job ID: %s\n", job.ID)

    // Poll manually
    for job.Status != "completed" {
        time.Sleep(10 * time.Second)
        job, _ = vc.Status(ctx, job.ID)
    }
    fmt.Printf("Video URL: %s\n", job.URL)

    // For image-to-video and RealFace, use cURL or the Python SDK —
    // the Go VideoClient.Generate() does not yet accept image_url
    // or real_face_asset_id parameters.
}
```

```go [Go (x402 Agent)]
package main

import (
    "context"
    "fmt"
    "time"
    jc "github.com/api-jarvisclaw/go-sdk"
)

func main() {
    ctx := context.Background()
    // x402 Agent wallet — pays per-call via USDC on Base (Chain ID 8453)
    vc, _ := jc.NewVideoClient(jc.WithPrivateKey("0x<evm-private-key>"))

    // Text-to-video (blocking — Generate waits by default)
    job, _ := vc.Generate(ctx, "A cat playing piano",
        jc.WithVideoModel("bytedance/seedance-2.0-pro"), jc.WithDuration(5))
    fmt.Printf("Video URL: %s\n", job.URL)

    // Non-blocking mode
    job, _ = vc.Generate(ctx, "Ocean waves at sunset",
        jc.WithVideoModel("bytedance/seedance-2.0-fast"),
        jc.WithDuration(5), jc.WithWait(false))
    fmt.Printf("Job ID: %s\n", job.ID)

    // Poll manually
    for job.Status != "completed" {
        time.Sleep(10 * time.Second)
        job, _ = vc.Status(ctx, job.ID)
    }
    fmt.Printf("Video URL: %s\n", job.URL)

    // For image-to-video and RealFace, use cURL or the Python SDK —
    // the Go VideoClient.Generate() does not yet accept image_url
    // or real_face_asset_id parameters.
}
```

:::
## Errors

| Code | Name | Description | Resolution |
|------|------|-------------|------------|
| 400 | invalid_model | Requested video model not available | Use one of: bytedance/seedance-2.0-pro, bytedance/seedance-2.0-fast, bytedance/seedance-1.5-pro, azure/sora-2 |
| 400 | invalid_asset_id | real_face_asset_id format invalid or not found | Enroll via /v1/marketplace/realface/enroll first to get a valid ta_xxx ID |
| 400 | model_asset_incompatible | real_face_asset_id used with Seedance 1.5 Pro (unsupported) | Use Seedance 2.0 Fast or 2.0 Pro for RealFace generation |
| 408 | generation_timeout | Video generation exceeded maximum time (5 minutes) | Retry the request — upstream may be under heavy load |
| 404 | job_not_found | Job ID does not exist or has expired (48h) | Job results are available for 48 hours after submission. After that, re-submit. |

## Limitations

- Seedance 1.5 Pro does NOT support real_face_asset_id — use 2.0 Fast or 2.0 Pro for character-consistent video
- image_url and real_face_asset_id are mutually exclusive — use one or the other, not both
- Generation takes 60-180 seconds — use async polling, not synchronous waiting
- Maximum duration: Seedance 5-15s per clip, Sora 4/8/12s per clip
- Output resolution fixed at 720p (1280x720) — no 1080p or 4K
- RealFace enrollment required separately via /docs/api/realface before using real_face_asset_id
- Job results (MP4 URLs) are retrievable for 48 hours after submission — even if your client disconnects
- Status sync lag: upstream may report "in_progress" for a few minutes after actual completion — keep polling, do not cancel early
## Guides

### Async Polling & Timeout Handling

Video generation is asynchronous — you submit a job, then poll until it completes. Jobs are retained for 48 hours, so even if your client times out, you can always come back and retrieve the result later.

#### Submit and poll (basic pattern)

Submit the generation request, get a job ID, poll every 5-10 seconds until status is "completed". The response includes progress (0-100) and elapsed_seconds to monitor generation.

```python
# ── Python (recommended: SDK handles all of this) ──
from jarvisclaw import VideoClient

video = VideoClient(api_key="sk-your-key")

# Blocking mode — SDK auto-polls until done (up to 10 min)
job = video.generate("A sunset over the ocean", duration=5)
print(job.url)  # MP4 URL
```

```bash
# ── cURL (manual polling) ──
# Step 1: Submit
curl -X POST https://api.jarvisclaw.ai/v1/videos/generations \
  -H "Authorization: Bearer sk-your-key" \
  -H "Content-Type: application/json" \
  -d '{"model": "bytedance/seedance-2.0-fast", "prompt": "A sunset over the ocean", "duration_seconds": 5}'
# → {"id": "vg_abc123", "status": "queued"}

# Step 2: Poll every 5-10s
curl https://api.jarvisclaw.ai/v1/videos/generations/vg_abc123 \
  -H "Authorization: Bearer sk-your-key"
# → {"id": "vg_abc123", "status": "in_progress", "progress": 65, "elapsed_seconds": 42}
# ... keep polling ...
# → {"id": "vg_abc123", "status": "completed", "url": "https://...mp4"}
```
#### Non-blocking mode (fire and forget)

Submit the job without waiting. Save the job ID, do other work, then check back later.

```python
from jarvisclaw import VideoClient

video = VideoClient(api_key="sk-your-key")

# Submit without waiting
job = video.generate("Cat on the moon", wait=False)
print(f"Job submitted: {job.id}")  # Save this ID

# ... minutes or hours later ...
result = video.wait(job.id)  # Blocks until ready
print(result.url)

# Or just check once (non-blocking)
result = video.status(job.id)
if result.status == "completed":
    print(result.url)
else:
    print(f"Still working: {result.raw.get('progress', '?')}%")
```

#### Timeout handling (status sync lag)

Upstream providers may report "in_progress" for several minutes after actual completion (status sync lag). If your poll times out, DO NOT re-submit — the job is still valid.

```python
from jarvisclaw import VideoClient

video = VideoClient(api_key="sk-your-key")

# Try with a shorter timeout for fast feedback
job = video.generate("Timelapse of flowers blooming",
    poll_timeout=180)  # 3 min timeout

if job.status == "timeout":
    # Job is NOT lost! Just poll again later
    print(f"Still generating, job ID: {job.id}")
    print(f"Progress: {job.raw.get('progress', 'unknown')}%")
    print(f"Elapsed: {job.raw.get('elapsed_seconds', '?')}s")

    # Come back anytime within 48h:
    result = video.wait(job.id, poll_timeout=600)
    print(result.url)

# ── Important notes ──
# 1. Never re-submit on timeout — you'll pay twice
# 2. Jobs survive client disconnects — 48h retention
# 3. Billing only occurs when you successfully poll "completed"
# 4. If progress stays at 0% for 5+ minutes, contact support
```
### RealFace Video (Real Person)

Generate videos featuring a real person with consistent identity. The person must complete a one-time liveness check (~60 seconds) to verify their identity.

See [RealFace API](/api/realface) for full enrollment documentation.

### Virtual Portrait (AI Character)

Create a consistent AI character identity without any real person. Upload any character image (illustration, 3D render, AI face) and reuse it across videos.

See [RealFace API](/api/realface) for full enrollment documentation.

### Image-to-Video (Animate a Photo)

Take any static image (photo, illustration, screenshot) and animate it into a video clip.

```bash
curl -X POST https://api.jarvisclaw.ai/v1/videos/generations \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"model": "bytedance/seedance-2.0-pro", "prompt": "The person turns and smiles at the camera", "image_url": "https://example.com/portrait.jpg", "duration_seconds": 5}'
```

```python
from jarvisclaw import VideoClient

video = VideoClient(private_key="0x<evm-private-key>")

job = video.generate("The person turns and smiles at the camera",
    model="bytedance/seedance-2.0-pro",
    image_url="https://example.com/portrait.jpg",
    duration=5)
print(f"Job submitted: {job.id}")

import time
while job.status != "completed":
    time.sleep(10)
    job = video.status(job.id)
print(f"Video URL: {job.url}")
```
