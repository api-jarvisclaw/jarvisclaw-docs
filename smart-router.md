# Smart Router

Set the model field to a router alias instead of a specific model ID. Smart Router analyses your request and selects the optimal upstream model automatically — no code changes needed when new models are added.

## auto

Smart Router picks the best available model for each request based on capability, latency, and cost.

```python
response = client.chat.completions.create(
    model="auto",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## free

Routes exclusively to free-tier models. Zero token cost — great for development and experimentation.

```python
response = client.chat.completions.create(
    model="free",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## eco

Selects the most cost-efficient paid model that can handle the task. Minimises spend per token.

```python
response = client.chat.completions.create(
    model="eco",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## premium

Routes to the highest-capability model available. Best for complex reasoning and production workloads.

```python
response = client.chat.completions.create(
    model="premium",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## search

Web search with AI-generated summary and source citations. Uses the chat completions endpoint but returns a **custom response format** (not standard OpenAI `choices` array).

### Request

```python
import requests

resp = requests.post("https://api.jarvisclaw.ai/v1/chat/completions",
    headers={"Authorization": "Bearer sk-your-api-key", "Content-Type": "application/json"},
    json={
        "model": "auto/search",
        "messages": [{"role": "user", "content": "What is retrieval augmented generation?"}]
    })
data = resp.json()
```

### Response

::: warning Non-standard format
`auto/search` does NOT return the OpenAI-compatible `{"choices": [{"message": ...}]}` format. It returns a custom search response with `summary`, `sources_used`, and inline citation links.
:::

```json
{
  "query": "What is retrieval augmented generation?",
  "summary": "Retrieval Augmented Generation (RAG) is a technique that...[1](https://example.com)...",
  "citations": [],
  "sources_used": 10,
  "model": "xai/grok-3-mini"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `query` | string | The original query |
| `summary` | string | AI-generated answer with inline `[N](url)` citation links |
| `citations` | array | Reserved (currently empty — citations are inline in summary) |
| `sources_used` | integer | Number of web sources consulted |
| `model` | string | The upstream model used for synthesis |

### Example

```python
import requests

resp = requests.post("https://api.jarvisclaw.ai/v1/chat/completions",
    headers={"Authorization": "Bearer sk-your-api-key", "Content-Type": "application/json"},
    json={
        "model": "auto/search",
        "messages": [{"role": "user", "content": "latest AI agent frameworks 2026"}]
    })

data = resp.json()
print(data["summary"])
print(f"Sources consulted: {data['sources_used']}")
```

## image

Routes to the best available image generation model. See [Image Generation API](/api/image-generation) for full documentation.

```python
import requests

resp = requests.post("https://api.jarvisclaw.ai/v1/images/generations",
    headers={"Authorization": "Bearer sk-your-api-key", "Content-Type": "application/json"},
    json={"model": "auto/image", "prompt": "A cat on Mars", "size": "1024x1024"})
```

## tts

Routes to the best available text-to-speech model. See [Audio API](/api/audio) for full documentation.

```python
import requests

resp = requests.post("https://api.jarvisclaw.ai/v1/audio/speech",
    headers={"Authorization": "Bearer sk-your-api-key", "Content-Type": "application/json"},
    json={"model": "auto/tts", "input": "Hello world!", "voice": "sarah"})
```

## music

Routes to the best available music generation model. See [Music Generation API](/api/music-generation) for full documentation.

```python
import requests

resp = requests.post("https://api.jarvisclaw.ai/v1/audio/generations",
    headers={"Authorization": "Bearer sk-your-api-key", "Content-Type": "application/json"},
    json={"model": "auto/music", "prompt": "Chill lo-fi beat", "instrumental": True})
```

## video

Routes to the best available video generation model. See [Video Generation API](/api/video-generation) for full documentation.

::: warning Duration constraints
`auto/video` may route to `azure/sora-2` which only supports durations of 4, 8, or 12 seconds. Do not pass `duration_seconds: 5` — use 4 instead.
:::

```python
import requests

resp = requests.post("https://api.jarvisclaw.ai/v1/videos/generations",
    headers={"Authorization": "Bearer sk-your-api-key", "Content-Type": "application/json"},
    json={"model": "auto/video", "prompt": "Ocean waves at sunset", "duration_seconds": 4})
```
