# Anthropic Messages API (Native)

Native Anthropic Messages endpoint — use the official `anthropic` Python SDK or `anthropic-sdk-go` directly against JarvisClaw. No format conversion, full feature parity with Claude's native API including prompt caching, extended thinking, and streaming.

**Base URL:** `https://api.jarvisclaw.ai`

## Authentication

| Method | Header | Description |
|--------|--------|-------------|
| API Key | `x-api-key: sk-...` | Anthropic-style header. Platform routes and handles x402 settlement |
| Private Key (x402) | Automatic via SDK | Agent signs x402 directly from its own wallet |

## Endpoint

### POST /v1/messages

Create a message using Anthropic's native protocol. Supports all Claude models.

## Quick Start

::: code-group

```python [Python]
import anthropic

client = anthropic.Anthropic(
    api_key="sk-your-api-key",
    base_url="https://api.jarvisclaw.ai"
)

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain quantum computing in one paragraph"}
    ]
)
print(message.content[0].text)
```

```go [Go]
package main

import (
    "context"
    "fmt"
    "github.com/anthropics/anthropic-sdk-go"
    "github.com/anthropics/anthropic-sdk-go/option"
)

func main() {
    client := anthropic.NewClient(
        option.WithAPIKey("sk-your-api-key"),
        option.WithBaseURL("https://api.jarvisclaw.ai"),
    )

    message, _ := client.Messages.New(context.Background(),
        anthropic.MessageNewParams{
            Model:     "claude-sonnet-4-20250514",
            MaxTokens: 1024,
            Messages: []anthropic.MessageParam{
                anthropic.NewUserMessage(
                    anthropic.NewTextBlock("Explain quantum computing in one paragraph"),
                ),
            },
        },
    )
    fmt.Println(message.Content[0].Text)
}
```

```bash [curl]
curl https://api.jarvisclaw.ai/v1/messages \
  -H "x-api-key: sk-your-api-key" \
  -H "Content-Type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Explain quantum computing in one paragraph"}
    ]
  }'
```

:::

## Streaming

::: code-group

```python [Python]
import anthropic

client = anthropic.Anthropic(
    api_key="sk-your-api-key",
    base_url="https://api.jarvisclaw.ai"
)

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write a short story about an AI agent"}
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

```go [Go]
package main

import (
    "context"
    "fmt"
    "github.com/anthropics/anthropic-sdk-go"
    "github.com/anthropics/anthropic-sdk-go/option"
)

func main() {
    client := anthropic.NewClient(
        option.WithAPIKey("sk-your-api-key"),
        option.WithBaseURL("https://api.jarvisclaw.ai"),
    )

    stream := client.Messages.NewStreaming(context.Background(),
        anthropic.MessageNewParams{
            Model:     "claude-sonnet-4-20250514",
            MaxTokens: 1024,
            Messages: []anthropic.MessageParam{
                anthropic.NewUserMessage(
                    anthropic.NewTextBlock("Write a short story about an AI agent"),
                ),
            },
        },
    )
    defer stream.Close()

    for stream.Next() {
        evt := stream.Current()
        switch evt := evt.AsAny().(type) {
        case anthropic.ContentBlockDeltaEvent:
            if evt.Delta.Type == "text_delta" {
                fmt.Print(evt.Delta.Text)
            }
        }
    }
}
```

```bash [curl]
curl https://api.jarvisclaw.ai/v1/messages \
  -H "x-api-key: sk-your-api-key" \
  -H "Content-Type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "stream": true,
    "messages": [
      {"role": "user", "content": "Write a short story about an AI agent"}
    ]
  }'
```

:::

## Extended Thinking

Enable Claude's internal reasoning for complex tasks:

::: code-group

```python [Python]
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    messages=[
        {"role": "user", "content": "What is the 100th prime number? Think step by step."}
    ]
)

for block in message.content:
    if block.type == "thinking":
        print(f"[Thinking]: {block.thinking}")
    elif block.type == "text":
        print(f"[Answer]: {block.text}")
```

```go [Go]
message, _ := client.Messages.New(ctx, anthropic.MessageNewParams{
    Model:     "claude-sonnet-4-20250514",
    MaxTokens: 16000,
    Thinking: &anthropic.ThinkingConfigParam{
        Type:        "enabled",
        BudgetTokens: 10000,
    },
    Messages: []anthropic.MessageParam{
        anthropic.NewUserMessage(
            anthropic.NewTextBlock("What is the 100th prime number? Think step by step."),
        ),
    },
})
```

:::

## Tool Use (Function Calling)

::: code-group

```python [Python]
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[{
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
        }
    }],
    messages=[
        {"role": "user", "content": "What's the weather in Tokyo?"}
    ]
)

# Handle tool_use blocks in response
for block in message.content:
    if block.type == "tool_use":
        print(f"Tool: {block.name}, Input: {block.input}")
```

```go [Go]
message, _ := client.Messages.New(ctx, anthropic.MessageNewParams{
    Model:     "claude-sonnet-4-20250514",
    MaxTokens: 1024,
    Tools: []anthropic.ToolParam{{
        Name:        "get_weather",
        Description: "Get current weather for a location",
        InputSchema: map[string]any{
            "type": "object",
            "properties": map[string]any{
                "location": map[string]any{"type": "string", "description": "City name"},
            },
            "required": []string{"location"},
        },
    }},
    Messages: []anthropic.MessageParam{
        anthropic.NewUserMessage(
            anthropic.NewTextBlock("What's the weather in Tokyo?"),
        ),
    },
})
```

:::

## System Prompt

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a helpful coding assistant. Always provide working examples.",
    messages=[
        {"role": "user", "content": "How do I read a file in Python?"}
    ]
)
```

## Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| model | string | Yes | Model ID (e.g., `claude-sonnet-4-20250514`) |
| messages | array | Yes | Array of message objects with `role` and `content` |
| max_tokens | integer | Yes | Maximum tokens to generate |
| system | string/array | No | System prompt |
| stream | boolean | No | Stream via SSE (default: false) |
| temperature | number | No | Sampling temperature (0-1) |
| top_p | number | No | Nucleus sampling |
| top_k | integer | No | Top-K sampling |
| stop_sequences | array | No | Custom stop sequences |
| tools | array | No | Tool definitions for function calling |
| tool_choice | object | No | `{"type": "auto"}`, `{"type": "any"}`, `{"type": "tool", "name": "..."}` |
| thinking | object | No | `{"type": "enabled", "budget_tokens": N}` |
| metadata | object | No | `{"user_id": "..."}` for abuse tracking |

## Required Headers

| Header | Value | Description |
|--------|-------|-------------|
| `x-api-key` | `sk-...` | Your API key |
| `anthropic-version` | `2023-06-01` | API version (required for curl, SDKs set automatically) |
| `Content-Type` | `application/json` | Request format |

## Streaming Events

| Event Type | Description |
|------------|-------------|
| `message_start` | Message object with metadata and usage |
| `content_block_start` | New content block (text, tool_use, thinking) |
| `content_block_delta` | Incremental text or JSON delta |
| `content_block_stop` | Content block finished |
| `message_delta` | Stop reason and final usage |
| `message_stop` | Message complete |

## Model Names

When using the native Anthropic endpoint, model names do **not** need the `anthropic/` prefix:

| Model | ID |
|-------|-----|
| Claude Sonnet 4 | `claude-sonnet-4-20250514` |
| Claude Opus 4 | `claude-opus-4-20250514` |
| Claude Haiku 3.5 | `claude-3-5-haiku-20241022` |

See [Models](/models) for the full list.

## See Also

- [Responses API](/api/responses) — OpenAI-compatible Responses format (use `openai` SDK)
- [Chat Completions API](/api/chat-completions) — Legacy OpenAI Chat format
- [Models](/models) — Full model list
