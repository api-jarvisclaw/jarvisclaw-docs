# Responses API

OpenAI Responses API — the next-generation replacement for Chat Completions. Supports streaming, function calling, extended thinking, and multi-turn via `previous_response_id`. Compatible with the official `openai` Python SDK and `openai-go` SDK.

**Base URL:** `https://api.jarvisclaw.ai/v1`

## Authentication

| Method | Header | Description |
|--------|--------|-------------|
| API Key | `Authorization: Bearer sk-...` | Platform signs x402 from your HD wallet automatically |
| Private Key (x402) | Automatic via SDK | Agent signs x402 directly from its own wallet |

See [Agent Payments (x402)](/x402) for full details.

## Endpoint

### POST /v1/responses

Create a model response. The platform routes to Claude, GPT, or Gemini upstream with automatic format conversion.

## Quick Start

::: code-group

```python [Python]
from openai import OpenAI

client = OpenAI(
    api_key="sk-your-api-key",
    base_url="https://api.jarvisclaw.ai/v1"
)

# Simple text response
response = client.responses.create(
    model="anthropic/claude-sonnet-4-20250514",
    input="Explain quantum computing in one paragraph"
)
print(response.output_text)
```

```go [Go]
package main

import (
    "context"
    "fmt"
    "github.com/openai/openai-go"
    "github.com/openai/openai-go/option"
)

func main() {
    client := openai.NewClient(
        option.WithAPIKey("sk-your-api-key"),
        option.WithBaseURL("https://api.jarvisclaw.ai/v1"),
    )

    resp, _ := client.Responses.New(context.Background(),
        openai.ResponseNewParams{
            Model: "anthropic/claude-sonnet-4-20250514",
            Input: openai.ResponseNewParamsInputUnionString(
                "Explain quantum computing in one paragraph",
            ),
        },
    )
    fmt.Println(resp.OutputText)
}
```

```bash [curl]
curl https://api.jarvisclaw.ai/v1/responses \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-sonnet-4-20250514",
    "input": "Explain quantum computing in one paragraph"
  }'
```

:::

## Streaming

::: code-group

```python [Python]
from openai import OpenAI

client = OpenAI(
    api_key="sk-your-api-key",
    base_url="https://api.jarvisclaw.ai/v1"
)

stream = client.responses.create(
    model="anthropic/claude-sonnet-4-20250514",
    input="Write a short story about an AI agent",
    stream=True
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
```

```go [Go]
package main

import (
    "context"
    "fmt"
    "github.com/openai/openai-go"
    "github.com/openai/openai-go/option"
    "github.com/openai/openai-go/responses"
)

func main() {
    client := openai.NewClient(
        option.WithAPIKey("sk-your-api-key"),
        option.WithBaseURL("https://api.jarvisclaw.ai/v1"),
    )

    stream := client.Responses.NewStreaming(context.Background(),
        openai.ResponseNewParams{
            Model: "anthropic/claude-sonnet-4-20250514",
            Input: openai.ResponseNewParamsInputUnionString(
                "Write a short story about an AI agent",
            ),
        },
    )
    defer stream.Close()

    for stream.Next() {
        evt := stream.Current()
        switch evt := evt.AsAny().(type) {
        case responses.ResponseTextDeltaEvent:
            fmt.Print(evt.Delta)
        }
    }
}
```

```bash [curl]
curl https://api.jarvisclaw.ai/v1/responses \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-sonnet-4-20250514",
    "input": "Write a short story about an AI agent",
    "stream": true
  }'
```

:::

## Multi-turn Conversations

Use `previous_response_id` to chain turns without resending full history:

```python
resp1 = client.responses.create(
    model="anthropic/claude-sonnet-4-20250514",
    input="What is the capital of France?"
)

resp2 = client.responses.create(
    model="anthropic/claude-sonnet-4-20250514",
    input=[{"role": "user", "content": [{"type": "input_text", "text": "And what about Germany?"}]}],
    previous_response_id=resp1.id
)
```

## Function Calling

::: code-group

```python [Python]
response = client.responses.create(
    model="anthropic/claude-sonnet-4-20250514",
    input=[{"role": "user", "content": [{"type": "input_text", "text": "What's the weather in Tokyo?"}]}],
    tools=[{
        "type": "function",
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }]
)
```

```go [Go]
resp, _ := client.Responses.New(ctx, openai.ResponseNewParams{
    Model: "anthropic/claude-sonnet-4-20250514",
    Input: openai.ResponseNewParamsInputUnion(openai.ResponseNewParamsInputItemList{
        {Role: "user", Content: []openai.ContentPart{{Type: "input_text", Text: "What's the weather in Tokyo?"}}},
    }),
    Tools: []openai.ToolUnion{{
        Type: "function",
        Function: &openai.FunctionTool{
            Name:        "get_weather",
            Description: "Get current weather for a location",
            Parameters: map[string]any{
                "type":       "object",
                "properties": map[string]any{"location": map[string]any{"type": "string"}},
                "required":   []string{"location"},
            },
        },
    }},
})
```

:::

## Extended Thinking / Reasoning

```python
response = client.responses.create(
    model="anthropic/claude-sonnet-4-20250514",
    input="Solve step by step: what is the 100th prime number?",
    reasoning={"effort": "high"}
)
```

Reasoning content appears as `reasoning` type content in output items when streaming.

## Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| model | string | Yes | Model ID (e.g., `anthropic/claude-sonnet-4-20250514`) |
| input | string or array | Yes | Text prompt or array of input items |
| stream | boolean | No | Stream via SSE (default: false) |
| max_output_tokens | integer | No | Maximum tokens to generate |
| temperature | number | No | Sampling temperature (0-2) |
| top_p | number | No | Nucleus sampling |
| instructions | string | No | System-level instructions |
| tools | array | No | Tool definitions for function calling |
| tool_choice | string/object | No | `"auto"`, `"none"`, `"required"` |
| reasoning | object | No | `{"effort": "low" \| "medium" \| "high"}` |
| previous_response_id | string | No | Chain multi-turn conversations |
| store | boolean | No | Store response for retrieval |
| metadata | object | No | Arbitrary key-value pairs |

## Streaming Events

| Event Type | Description |
|------------|-------------|
| `response.created` | Response object created |
| `response.in_progress` | Processing started |
| `response.output_item.added` | New output item started |
| `response.content_part.added` | New content part started |
| `response.output_text.delta` | Text chunk |
| `response.content_part.done` | Content part finished |
| `response.output_item.done` | Output item finished |
| `response.completed` | Response completed with usage |

## See Also

- [Anthropic Messages API](/api/anthropic-messages) — Native Anthropic protocol (use `anthropic` SDK directly)
- [Chat Completions API](/api/chat-completions) — Legacy OpenAI Chat format
- [Models](/models) — Full model list
