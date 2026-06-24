# Chat Completions API

OpenAI-compatible chat completions endpoint supporting 200+ models across all major providers. Supports streaming, function calling, vision, and structured outputs.

**Base URL:** `https://api.jarvisclaw.ai/v1`

## Endpoints

### POST /v1/chat/completions

Create a chat completion.

#### Headers

| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | `Bearer sk-your-api-key` |
| Content-Type | Yes | Must be `application/json` |
| PAYMENT-SIGNATURE | Conditional | Base64-encoded x402 payment payload (required after 402, x402 v2) |

#### Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| model | string | Yes | Model ID (e.g., `openai/gpt-5.5`) |
| messages | array | Yes | Array of message objects |
| max_tokens | integer | No | Maximum tokens to generate (default: 1024) |
| max_completion_tokens | integer | No | Max output tokens including reasoning (for o-series / reasoning models) |
| temperature | number | No | Sampling temperature (0-2) |
| top_p | number | No | Nucleus sampling parameter |
| top_k | integer | No | Top-K sampling (provider-dependent) |
| stream | boolean | No | Stream partial responses via SSE (default: false) |
| stream_options | object | No | `{"include_usage": true}` to receive token counts in stream |
| stop | string or array | No | Stop sequence(s) |
| n | integer | No | Number of completions to generate (default: 1) |
| frequency_penalty | number | No | Penalize repeated tokens (-2.0 to 2.0) |
| presence_penalty | number | No | Penalize tokens already present (-2.0 to 2.0) |
| tools | array | No | List of tool/function definitions for function calling |
| tool_choice | string or object | No | Controls tool use: `"auto"`, `"none"`, or specific tool |
| parallel_tool_calls | boolean | No | Whether to run tool calls in parallel (default: true) |
| response_format | object | No | `{"type": "json_object"}` or `{"type": "json_schema", "json_schema": {...}}` |
| seed | number | No | Deterministic sampling seed |
| reasoning_effort | string | No | `"low"`, `"medium"`, or `"high"` — controls thinking depth (o-series models) |
| logprobs | boolean | No | Return log probabilities of output tokens |
| top_logprobs | integer | No | Number of top logprobs per token (0-20) |
| prompt_cache | boolean | No | Enable prompt caching on Anthropic models |
| logit_bias | object | No | Token ID to bias value mapping (-100 to 100) |
| user | string | No | Unique end-user identifier |
| service_tier | string | No | Upstream service level (e.g., `"default"`, `"flex"`). Filtered by default; requires channel-level `allow_service_tier` |
| modalities | array | No | Output modalities: `["text"]` or `["text", "audio"]` |
| audio | object | No | Audio output config: `{"voice": "alloy", "format": "wav"}`. Requires `modalities` to include `"audio"` |
| store | boolean | No | Whether to store this request for model distillation/evals (OpenAI). Default: allowed to pass through |
| metadata | object | No | Arbitrary key-value metadata attached to the request |
| prediction | object | No | Predicted output for speculative decoding (OpenAI) |
| web_search_options | object | No | Web search configuration for grounded responses (Claude/xAI) |

#### Provider-Specific Parameters

These parameters are transparently forwarded to the upstream provider when applicable:

| Parameter | Provider | Description |
|-----------|----------|-------------|
| enable_thinking | Qwen | Enable extended thinking mode |
| think | Ollama | Enable thinking/reasoning output |
| enable_search | Qwen | Enable web search augmentation |
| search_parameters | xAI (Grok) | Search configuration for grounded responses |
| vl_high_resolution_images | Qwen-VL | Enable high-resolution image processing |
| reasoning_split | Minimax | Control reasoning output splitting |

#### Message Object

| Field | Type | Description |
|-------|------|-------------|
| role | string | One of: `system`, `user`, `assistant`, `tool` |
| content | string or array | The message content (string or content parts for vision) |
| name | string | Optional name for the participant |
| tool_calls | array | Tool calls made by the assistant (assistant messages only) |
| tool_call_id | string | ID of the tool call this message responds to (tool messages only) |

#### Request Example

```json
{
  "model": "anthropic/claude-sonnet-4.6",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain quantum computing in simple terms."}
  ],
  "max_tokens": 1024,
  "temperature": 0.7,
  "stream": true
}
```

#### Response Example

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1717200000,
  "model": "anthropic/claude-sonnet-4.6",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Quantum computing uses quantum bits (qubits)..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 24,
    "completion_tokens": 156,
    "total_tokens": 180
  }
}
```

#### Usage Fields

| Field | Always present | Notes |
|-------|---------------|-------|
| prompt_tokens | yes | Full prompt size; cache reads already folded in |
| completion_tokens | yes | Output tokens; includes thinking/reasoning for all providers |
| total_tokens | yes | Sum of prompt + completion |
| prompt_tokens_details.cached_tokens | when cache hit | Prompt tokens read from cache (OpenAI convention) |
| prompt_tokens_details.cached_creation_tokens | when cache write | Prompt tokens written to cache this turn (BlockRun extension) |
| cache_read_input_tokens | when cache hit | Same as `prompt_tokens_details.cached_tokens` — Anthropic/Bedrock native label |
| cache_creation_input_tokens | when cache write | Same as `prompt_tokens_details.cached_creation_tokens` — Anthropic/Bedrock native label |
| completion_tokens_details.reasoning_tokens | when reasoning | OpenAI GPT-5.x / o-series only; forwarded verbatim. Not available for Anthropic/Bedrock (thinking tokens already included in `completion_tokens`) |

**Protocol naming convention:**

- **Claude native** `/v1/messages`: `usage.input_tokens`, `usage.output_tokens`, `usage.cache_creation_input_tokens`, `usage.cache_read_input_tokens`
- **OpenAI-compat** `/v1/chat/completions`: `usage.prompt_tokens_details.cached_tokens` (reads), `usage.prompt_tokens_details.cached_creation_tokens` (writes), `usage.completion_tokens_details.reasoning_tokens` (reasoning)

**Enabling prompt caching on Anthropic models:** Pass `"prompt_cache": true` in the request body, or embed `cache_control` blocks in your message content directly — both are honored.

#### Payment Required (402)

When you first make a request without payment (x402 mode), you'll receive:

```json
{
  "error": "Payment Required",
  "message": "This endpoint requires x402 payment",
  "price": {
    "amount": "0.001000",
    "currency": "USD",
    "breakdown": {
      "inputCost": "0.000012",
      "outputCost": "0.000600",
      "margin": "0%"
    }
  },
  "paymentInfo": {
    "network": "base",
    "asset": "USDC",
    "x402Version": 2
  }
}
```

The `X-Payment-Required` header contains the full payment requirements. 402 is the normal flow, not an error — the first request returns a price quote. Sign it and retry with the `PAYMENT-SIGNATURE` header to get your completion. The SDKs do this round-trip automatically.

## Pricing

| Model | Price (per 1M tokens) | Notes |
|-------|----------------------|-------|
| openai/gpt-5.5 | $5.00 / $30.00 | Input / Output pricing |
| anthropic/claude-sonnet-4.6 | $3.00 / $15.00 | Input / Output pricing |
| google/gemini-2.5-pro | $2.50 / $15.00 | Input / Output pricing |
| deepseek/deepseek-chat | $0.55 / $2.19 | Input / Output pricing |
| xai/grok-4.3 | $3.00 / $15.00 | Input / Output pricing |

## Code Examples

::: code-group

```bash [cURL]
curl -X POST https://api.jarvisclaw.ai/v1/chat/completions \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-sonnet-4.6",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "stream": true
  }'
```

```python [Python (API Key)]
from openai import OpenAI

client = OpenAI(
    base_url="https://api.jarvisclaw.ai/v1",
    api_key="sk-your-api-key",
)

# Simple completion
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4.6",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing."},
    ],
)
print(response.choices[0].message.content)

# Streaming
stream = client.chat.completions.create(
    model="anthropic/claude-sonnet-4.6",
    messages=[{"role": "user", "content": "Tell me a joke."}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

```python [Python (x402 Agent)]
from jarvisclaw import ChatClient

# ─── Option A: Base chain (EVM) ───
# Hex private key → USDC on Base (Chain ID 8453)
chat = ChatClient(private_key="0x<evm-private-key>")

# ─── Option B: Solana ───
# Base58 keypair → USDC SPL on Solana mainnet
# chat = ChatClient(private_key="<solana-bs58-keypair>")

# SDK auto-detects chain from key format — no config needed

# Simple completion (smart route — auto-selects best model)
response = chat.complete("Explain quantum computing.")
print(response)

# With explicit model
response = chat.complete("Explain quantum computing.", model="anthropic/claude-sonnet-4.6")
print(response)

# Streaming
for chunk in chat.stream("Tell me a joke.", model="openai/gpt-5.4-mini"):
    print(chunk, end="")
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
    cc, _ := jc.NewChatClient(jc.WithAPIKey("sk-your-api-key"))

    // Simple completion
    response, _ := cc.Complete(ctx, "Explain quantum computing.",
        jc.WithChatModel("anthropic/claude-sonnet-4.6"))
    fmt.Println(response)

    // Streaming
    stream, _ := cc.Stream(ctx, "Tell me a joke.", jc.WithChatModel("openai/gpt-5.4-mini"))
    for chunk := range stream.Channel() {
        fmt.Print(chunk)
    }
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
    cc, _ := jc.NewChatClient(jc.WithPrivateKey("0x<evm-private-key>"))

    // Simple completion (smart route — auto-selects best model)
    response, _ := cc.Complete(ctx, "Explain quantum computing.")
    fmt.Println(response)

    // With explicit model
    response, _ = cc.Complete(ctx, "Explain quantum computing.",
        jc.WithChatModel("anthropic/claude-sonnet-4.6"))
    fmt.Println(response)

    // Streaming
    stream, _ := cc.Stream(ctx, "Tell me a joke.", jc.WithChatModel("openai/gpt-5.4-mini"))
    for chunk := range stream.Channel() {
        fmt.Print(chunk)
    }
}
```

:::
---
