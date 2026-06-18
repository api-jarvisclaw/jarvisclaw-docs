# Chat Completions API

OpenAI-compatible chat completions endpoint supporting 200+ models across all major providers. Supports streaming, function calling, vision, and structured outputs.

**Base URL:** `https://api.jarvisclaw.ai/v1`

## Endpoints

### POST /v1/chat/completions

Create a chat completion.

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| model | string | Yes | Model identifier (e.g. "openai/gpt-5.5", "anthropic/claude-sonnet-4") |
| messages | array | Yes | Array of message objects with role and content |
| max_tokens | integer | No | Maximum number of tokens to generate (default: 4096) |
| temperature | number | No | Sampling temperature (0-2) (default: 1.0) |
| top_p | number | No | Nucleus sampling parameter (default: 1.0) |
| stream | boolean | No | Stream partial responses via SSE (default: false) |
| tools | array | No | List of tool/function definitions for function calling |

#### Request Example

```json
{
  "model": "anthropic/claude-sonnet-4",
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
  "model": "anthropic/claude-sonnet-4",
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

## Pricing

| Model | Price (per 1M tokens) | Notes |
|-------|----------------------|-------|
| openai/gpt-5.5 | $5.00 / $15.00 | Input / Output pricing |
| anthropic/claude-sonnet-4 | $3.00 / $15.00 | Input / Output pricing |
| google/gemini-2.5-pro | $2.50 / $15.00 | Input / Output pricing |
| deepseek/deepseek-r1 | $0.55 / $2.19 | Input / Output pricing |
| xai/grok-3 | $3.00 / $15.00 | Input / Output pricing |

## Code Examples

::: code-group

```bash [cURL]
curl -X POST https://api.jarvisclaw.ai/v1/chat/completions \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-sonnet-4",
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
    model="anthropic/claude-sonnet-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing."},
    ],
)
print(response.choices[0].message.content)

# Streaming
stream = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
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
response = chat.complete("Explain quantum computing.", model="anthropic/claude-sonnet-4")
print(response)

# Streaming
for chunk in chat.stream("Tell me a joke.", model="openai/gpt-5.5"):
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
        jc.WithChatModel("anthropic/claude-sonnet-4"))
    fmt.Println(response)

    // Streaming
    stream, _ := cc.Stream(ctx, "Tell me a joke.", jc.WithChatModel("openai/gpt-5.5"))
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
        jc.WithChatModel("anthropic/claude-sonnet-4"))
    fmt.Println(response)

    // Streaming
    stream, _ := cc.Stream(ctx, "Tell me a joke.", jc.WithChatModel("openai/gpt-5.5"))
    for chunk := range stream.Channel() {
        fmt.Print(chunk)
    }
}
```

:::
---
