# Agent Economy (AIP)

The Agent Intent Protocol lets autonomous agents discover optimal AI providers, manage budgets, and pay only for what they use — all through a single API.

## How It Works

```
Agent declares intent → AIP finds best provider → Agent calls model → Treasury tracks spending
```

1. **Intent Resolution** (free) — declare what you need, get ranked providers
2. **Execute** — call the recommended model with your API key or x402 payment
3. **Wallet Management** — check balance, set limits, track spending pools

## Quick Start

### Find the Best Model (Free, No Auth)

::: code-group

```bash [curl]
curl -X POST https://api.jarvisclaw.ai/v1/intent/resolve \
  -H "Content-Type: application/json" \
  -d '{
    "intent": "chat_completion",
    "constraints": { "max_price_usd": 0.01 },
    "preferences": { "optimize_for": "cost" }
  }'
```

```python [Python]
from jarvisclaw import Agent

agent = Agent(api_key="sk-YOUR-KEY")

# One line: find best model + call it
result = agent.ask("Explain quantum computing", budget=0.01, optimize="cost")
print(result)
```

```go [Go]
import jc "github.com/api-jarvisclaw/go-sdk"

c, _ := jc.NewClient(jc.WithAPIKey("sk-YOUR-KEY"))
text, _ := c.Ask(ctx, "Explain quantum computing",
    jc.AskOptions{Budget: 0.01, Optimize: "cost"})
fmt.Println(text)
```

:::

### Response

```json
{
  "matches": [
    {
      "provider_id": "deepseek-chat",
      "score": 0.95,
      "estimated_price_usd": 0.0003,
      "endpoint": "/v1/chat/completions",
      "model": "deepseek-chat",
      "reason": "lowest cost: $0.000300/req"
    }
  ],
  "intent_type": "chat_completion",
  "total_available": 45
}
```

### Use the Recommended Model

```bash
curl https://api.jarvisclaw.ai/v1/chat/completions \
  -H "Authorization: Bearer sk-YOUR-KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "deepseek-chat", "messages": [{"role": "user", "content": "Hello!"}]}'
```

## Intent Types

| Intent | Description | Example Models |
|--------|-------------|----------------|
| `chat_completion` | Text generation / chat | GPT-4o, Claude, DeepSeek |
| `image_generation` | Image creation | DALL-E, Flux, Midjourney |
| `video_generation` | Video synthesis | Sora, Seedance, Kling |
| `text_to_speech` | TTS audio | TTS-1, ElevenLabs |
| `web_search` | Web browsing | Surf (83 endpoints) |
| `knowledge_search` | Semantic search | Exa |

## Optimization Strategies

| Strategy | Behavior |
|----------|----------|
| `cost` | Cheapest model that meets constraints |
| `quality` | Highest quality score (benchmark-based) |
| `latency` | Fastest response time (P95 measured) |

## Constraints

```json
{
  "constraints": {
    "max_price_usd": 0.01,
    "max_latency_ms": 3000,
    "features": ["function_calling", "vision", "streaming"]
  }
}
```

## Authentication

Intent resolution (`/v1/intent/resolve`) is **free and unauthenticated** — any agent can discover providers.

For execution and wallet management, three auth methods are supported:

| Method | Header | Use Case |
|--------|--------|----------|
| API Key | `Authorization: Bearer sk-xxx` | SDK users, developers |
| x402 Payment | `X-PAYMENT-SIGNATURE: <signed>` | Autonomous agents (zero registration) |
| Session Cookie | (automatic) | Dashboard users |

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/v1/intent/resolve` | None (free) | Resolve intent to ranked providers |
| POST | `/v1/intent/execute` | Required | Resolve + execute in one call |
| GET | `/v1/intent/types` | None | List supported intent types |
| GET | `/v1/providers` | None | List all registered providers |
