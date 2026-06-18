
# Async & Concurrent Usage

Image, video, and music generation typically takes 30 seconds to 3 minutes. The SDK offers three concurrency patterns so you can keep your application responsive while waiting.

```shell
# pip install jarvisclaw[async]
# All clients support both sync and async usage patterns.
# Choose the style that fits your application.
```

## Non-blocking (wait=False)

Submit a job and get a handle immediately. Poll or block for the result later — useful when you need to do other work in between.

```python
from jarvisclaw import ImageClient, VideoClient, AudioClient

image = ImageClient(private_key="0x...")

# ─── Non-blocking: returns immediately, poll later ───
job = image.generate("A futuristic cityscape", wait=False)
print(f"Job submitted: {job.raw['id']}")

# Do other work while image generates...
import time
time.sleep(10)

# Check status when ready
result = image.status(job.raw["id"])
if result.url:
    print(f"Done: {result.url}")

# Same pattern for video
video = VideoClient(private_key="0x...")
job = video.generate("Ocean waves at sunset", wait=False)
# ... later ...
result = video.status(job.id)

# Music returns a Future-like MusicJob
audio = AudioClient(private_key="0x...")
music_job = audio.music("Lo-fi hip hop beat", wait=False)
# ... do other work ...
result = music_job.result()  # blocks only when you need the result
```

## asyncio (concurrent requests)

Use jarvisclaw.aio clients with asyncio.gather to run multiple requests concurrently in a single thread.

```python
import asyncio
from jarvisclaw.aio import ChatClient, ImageClient, VideoClient, AudioClient

async def main():
    # All async clients support context manager
    async with ChatClient(private_key="0x...") as chat, \
               ImageClient(private_key="0x...") as image:

        # Concurrent chat requests to different models
        responses = await asyncio.gather(
            chat.complete("What is 2+2?", model="openai/gpt-5.4"),
            chat.complete("What is 3+3?", model="anthropic/claude-sonnet-4.6"),
            chat.complete("What is 4+4?", model="google/gemini-2.5-flash"),
        )
        for r in responses:
            print(r)

        # Concurrent image generation
        images = await asyncio.gather(
            image.generate("A cat in space"),
            image.generate("A dog on the moon"),
            image.generate("A bird underwater"),
        )
        for img in images:
            print(img.url)

        # Streaming (async for)
        async for chunk in chat.stream("Tell me a story"):
            print(chunk, end="")

asyncio.run(main())
```

## ThreadPoolExecutor (simple parallelism)

Run sync clients in parallel threads — no asyncio knowledge needed. Good for batch jobs.

```python
from concurrent.futures import ThreadPoolExecutor
from jarvisclaw import ImageClient

image = ImageClient(private_key="0x...")
prompts = ["A cat", "A dog", "A bird", "A fish", "A horse"]

# Simple thread-based parallelism (no asyncio knowledge needed)
with ThreadPoolExecutor(max_workers=5) as pool:
    futures = [pool.submit(image.generate, p) for p in prompts]
    for future in futures:
        result = future.result()
        print(result.url)
```
## Go (goroutines)

Go's goroutines handle concurrency natively — no special async library required.

```go
package main

import (
    "context"
    "fmt"
    "sync"

    jarvisclaw "github.com/api-jarvisclaw/go-sdk"
)

func main() {
    ctx := context.Background()
    image, _ := jarvisclaw.NewImageClient(jarvisclaw.WithPrivateKey("0x..."))

    prompts := []string{"A cat", "A dog", "A bird"}
    results := make([]*jarvisclaw.ImageResponse, len(prompts))

    // Go's goroutines are native async — no special library needed
    var wg sync.WaitGroup
    for i, p := range prompts {
        wg.Add(1)
        go func(i int, p string) {
            defer wg.Done()
            results[i], _ = image.Generate(ctx, p)
        }(i, p)
    }
    wg.Wait()

    for _, r := range results {
        fmt.Println(r.URL)
    }
}
```

::: tip
The async extras are only needed for the asyncio pattern. Install with: `pip install jarvisclaw[async]`
:::
