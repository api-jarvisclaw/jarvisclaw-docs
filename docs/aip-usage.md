# AIP Usage Guide — Agent Intent Protocol

**适用版本:** Python SDK ≥ 2.0.0 (`jarvisclaw`) / Go SDK ≥ 1.3.0 (`github.com/jarvisclaw/go-sdk`)

AIP 已内置于主 SDK，**无需额外安装** `agent-intent-protocol` 包。

---

## 安装

::: code-group
```bash [Python]
pip install jarvisclaw
```
```bash [Go]
go get github.com/jarvisclaw/go-sdk@latest
```
:::

---

## 快速开始

::: code-group
```python [Python]
from jarvisclaw import IntentClient

client = IntentClient(api_key="YOUR_API_KEY")

# 一步到位：解析最优 provider + 执行
result = client.execute(
    intent="chat_completion",
    payload={
        "messages": [{"role": "user", "content": "Hello AIP!"}],
        "temperature": 0.7,
    },
    optimize_for="cost",
    constraints={"max_price_usd": 0.01},
)
print(result)
```
```go [Go]
package main

import (
    "context"
    "fmt"
    jc "github.com/jarvisclaw/go-sdk"
)

func main() {
    client := jc.New("YOUR_API_KEY")
    ctx := context.Background()

    raw, err := client.Execute(ctx, jc.ExecuteRequest{
        Intent:      "chat_completion",
        Preferences: &jc.Preferences{OptimizeFor: "cost"},
        Constraints: &jc.Constraints{MaxPriceUSD: ptr(0.01)},
        Payload: map[string]any{
            "messages":    []map[string]any{{"role": "user", "content": "Hello AIP!"}},
            "temperature": 0.7,
        },
    })
    if err != nil {
        panic(err)
    }
    fmt.Println(string(raw))
}

func ptr[T any](v T) *T { return &v }
```
:::

---

## 使用场景一览

| 场景 | Intent Type | 说明 |
|------|-------------|------|
| AI 聊天 | `chat_completion` | 调用最优 LLM 生成文本 |
| 图片生成 | `image_generation` | DALL-E / Stable Diffusion 等 |
| 视频生成 | `video_generation` | 文本/图片转视频 |
| 语音合成 | `text_to_speech` | TTS 语音输出 |
| 网页搜索 | `web_search` | 实时网络检索 |
| 知识检索 | `knowledge_search` | RAG / 向量检索 |
| Prompt 优化 | `prompt_optimization` | AI 优化你的 prompt ($0.002/次) |
| 工具调用 | `tool_call` | 执行 MCP 注册的工具 |
| 自定义 | `x-{vendor}/{type}` | 供应商自定义 intent |

---

## 场景详解

### 1. AI 聊天 (`chat_completion`)

最常见的场景：Agent 需要 LLM 回复，AIP 自动选择性价比最优的模型。

::: code-group
```python [Python]
from jarvisclaw import IntentClient

client = IntentClient(api_key="YOUR_API_KEY")

# 先解析，查看有哪些可选 provider
matches = client.resolve(
    intent="chat_completion",
    optimize_for="quality",
    constraints={
        "max_price_usd": 0.05,
        "max_latency_ms": 3000,
        "features": ["function_calling", "json_mode"],
    },
)
for m in matches["matches"]:
    print(f"{m['provider_id']}: ${m['price_usd']:.4f}, score={m['score']}")

# 直接执行（自动 resolve → route → settle）
result = client.execute(
    intent="chat_completion",
    payload={
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain quantum computing in 3 sentences."},
        ],
        "temperature": 0.5,
        "max_tokens": 200,
    },
    optimize_for="quality",
    constraints={"max_price_usd": 0.05},
)
print(result["result"])
print(f"Cost: ${result['billing']['amount_usd']}")
```
```go [Go]
ctx := context.Background()
client := jc.New("YOUR_API_KEY")

// Resolve: 查看候选 provider
resp, _ := client.Resolve(ctx, jc.ResolveRequest{
    Intent: "chat_completion",
    Preferences: jc.Preferences{OptimizeFor: "quality"},
    Constraints: jc.Constraints{
        MaxPriceUSD:  ptr(0.05),
        MaxLatencyMS: ptr(3000),
        Features:     []string{"function_calling", "json_mode"},
    },
})
for _, m := range resp.Matches {
    fmt.Printf("%s: $%.4f, score=%.2f\n", m.ProviderID, m.EstimatedPriceUSD, m.Score)
}

// Execute: 一步到位
raw, _ := client.Execute(ctx, jc.ExecuteRequest{
    Intent:      "chat_completion",
    Preferences: &jc.Preferences{OptimizeFor: "quality"},
    Constraints: &jc.Constraints{MaxPriceUSD: ptr(0.05)},
    Payload: map[string]any{
        "messages": []map[string]any{
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain quantum computing in 3 sentences."},
        },
        "temperature": 0.5,
        "max_tokens":  200,
    },
})
fmt.Println(string(raw))
```
:::

---

### 2. 图片生成 (`image_generation`)

::: code-group
```python [Python]
result = client.execute(
    intent="image_generation",
    payload={
        "prompt": "A cyberpunk city at sunset, ultra detailed",
        "size": "1024x1024",
        "style": "vivid",
    },
    optimize_for="quality",
    constraints={"max_price_usd": 0.10},
)
image_url = result["result"]["url"]
```
```go [Go]
raw, _ := client.Execute(ctx, jc.ExecuteRequest{
    Intent:      "image_generation",
    Preferences: &jc.Preferences{OptimizeFor: "quality"},
    Constraints: &jc.Constraints{MaxPriceUSD: ptr(0.10)},
    Payload: map[string]any{
        "prompt": "A cyberpunk city at sunset, ultra detailed",
        "size":   "1024x1024",
        "style":  "vivid",
    },
})
```
:::

---

### 3. 视频生成 (`video_generation`)

::: code-group
```python [Python]
result = client.execute(
    intent="video_generation",
    payload={
        "prompt": "A drone flying over mountains at golden hour",
        "duration_seconds": 5,
        "resolution": "1080p",
    },
    optimize_for="cost",
    constraints={"max_price_usd": 0.50},
)
video_url = result["result"]["url"]
```
```go [Go]
raw, _ := client.Execute(ctx, jc.ExecuteRequest{
    Intent:      "video_generation",
    Preferences: &jc.Preferences{OptimizeFor: "cost"},
    Constraints: &jc.Constraints{MaxPriceUSD: ptr(0.50)},
    Payload: map[string]any{
        "prompt":           "A drone flying over mountains at golden hour",
        "duration_seconds": 5,
        "resolution":       "1080p",
    },
})
```
:::

---

### 4. 语音合成 (`text_to_speech`)

::: code-group
```python [Python]
result = client.execute(
    intent="text_to_speech",
    payload={
        "text": "Welcome to JarvisClaw. Your agent is ready.",
        "voice": "alloy",
        "format": "mp3",
    },
    optimize_for="speed",
)
audio_bytes = result["result"]["audio_base64"]
```
```go [Go]
raw, _ := client.Execute(ctx, jc.ExecuteRequest{
    Intent:      "text_to_speech",
    Preferences: &jc.Preferences{OptimizeFor: "speed"},
    Payload: map[string]any{
        "text":   "Welcome to JarvisClaw. Your agent is ready.",
        "voice":  "alloy",
        "format": "mp3",
    },
})
```
:::

---

### 5. 网页搜索 (`web_search`)

::: code-group
```python [Python]
result = client.execute(
    intent="web_search",
    payload={
        "query": "latest AI research papers 2026",
        "max_results": 5,
    },
    optimize_for="speed",
    constraints={"max_price_usd": 0.005},
)
for item in result["result"]["results"]:
    print(f"- {item['title']}: {item['url']}")
```
```go [Go]
raw, _ := client.Execute(ctx, jc.ExecuteRequest{
    Intent:      "web_search",
    Preferences: &jc.Preferences{OptimizeFor: "speed"},
    Constraints: &jc.Constraints{MaxPriceUSD: ptr(0.005)},
    Payload: map[string]any{
        "query":       "latest AI research papers 2026",
        "max_results": 5,
    },
})
```
:::

---

### 6. 知识检索 (`knowledge_search`)

::: code-group
```python [Python]
result = client.execute(
    intent="knowledge_search",
    payload={
        "query": "how to configure AIP budget limits",
        "namespace": "docs",
        "top_k": 3,
    },
    optimize_for="quality",
)
for chunk in result["result"]["chunks"]:
    print(f"[{chunk['score']:.2f}] {chunk['text'][:100]}")
```
```go [Go]
raw, _ := client.Execute(ctx, jc.ExecuteRequest{
    Intent:      "knowledge_search",
    Preferences: &jc.Preferences{OptimizeFor: "quality"},
    Payload: map[string]any{
        "query":     "how to configure AIP budget limits",
        "namespace": "docs",
        "top_k":     3,
    },
})
```
:::

---

### 7. MCP 工具调用 (`tool_call`)

::: code-group
```python [Python]
result = client.execute(
    intent="tool_call",
    payload={
        "tool_name": "github/create_issue",
        "arguments": {
            "repo": "jarvisclaw/platform",
            "title": "Bug: intent audit missing timestamps",
            "body": "Audit entries lack created_at field",
        },
    },
    optimize_for="speed",
)
print(result["result"])
```
```go [Go]
raw, _ := client.Execute(ctx, jc.ExecuteRequest{
    Intent:      "tool_call",
    Preferences: &jc.Preferences{OptimizeFor: "speed"},
    Payload: map[string]any{
        "tool_name": "github/create_issue",
        "arguments": map[string]any{
            "repo":  "jarvisclaw/platform",
            "title": "Bug: intent audit missing timestamps",
            "body":  "Audit entries lack created_at field",
        },
    },
})
```
:::

---

### 8. Prompt 优化 (`prompt_optimization`)

使用 AI 优化你的 prompt，获得更精准的输出。固定费用 $0.002/次。

::: code-group
```python [Python]
result = client.execute(
    intent="prompt_optimization",
    payload={
        "prompt": "写一个关于AI的文章",
        "model": "gpt-4o",
        "context": "用于技术博客，面向开发者受众",
    },
)
optimized = result["result"]["optimized_prompt"]
suggestions = result["result"]["suggestions"]
print(f"优化后: {optimized}")
for s in suggestions:
    print(f"  💡 {s}")
```
```go [Go]
raw, _ := client.Execute(ctx, jc.ExecuteRequest{
    Intent: "prompt_optimization",
    Payload: map[string]any{
        "prompt":  "写一个关于AI的文章",
        "model":   "gpt-4o",
        "context": "用于技术博客，面向开发者受众",
    },
})
// Returns: {"optimized_prompt": "...", "suggestions": [...]}
fmt.Println(string(raw))
```
:::

::: tip 定价
Prompt 优化固定 $0.002/次，不受 optimize_for 策略影响。
:::

---

## 高级功能

### 预算控制 (`execute_budget`)

对支出设硬上限，超限自动拒绝而非超支：

::: code-group
```python [Python]
result = client.execute_budget(
    intent="chat_completion",
    payload={
        "messages": [{"role": "user", "content": "Write a 2000-word essay"}],
    },
    budget={
        "max_total_usd": 0.50,
        "preferred_payment_method": "balance",
    },
)
print(f"Status: {result['status']}")
print(f"Actual cost: ${result['actual_cost_usd']}")
print(f"Risk level: {result['risk_level']}")
```
```go [Go]
budgetResp, _ := client.ExecuteBudget(ctx, jc.ExecuteBudgetRequest{
    Intent: "chat_completion",
    Budget: jc.Budget{
        MaxTotalUSD:            0.50,
        PreferredPaymentMethod: "balance",
    },
    Payload: map[string]any{
        "messages": []map[string]any{
            {"role": "user", "content": "Write a 2000-word essay"},
        },
    },
})
fmt.Printf("Status: %s, Cost: $%.4f\n", budgetResp.Status, *budgetResp.ActualCostUSD)
```
:::

---

### 审计日志 (`audit`)

查看历史调用记录和支出：

::: code-group
```python [Python]
entries = client.audit()
for e in entries["entries"]:
    print(f"[{e['timestamp']}] {e['event_type']} — {e['request_id']}")
```
```go [Go]
auditResp, _ := client.Audit(ctx)
for _, e := range auditResp.Entries {
    fmt.Printf("[%s] %s — %s\n", e.Timestamp, e.EventType, e.RequestID)
}
```
:::

---

### 查询可用 Provider 和 Intent 类型

::: code-group
```python [Python]
# 查看支持的 intent 类型
types = client.types()
print(types)  # ['chat_completion', 'image_generation', ...]

# 查看所有注册的 provider
providers = client.providers()
for p in providers["providers"]:
    print(f"{p['provider_id']}: {p['model']}")
```
```go [Go]
// 查看支持的 intent 类型
intentTypes, _ := client.ListIntentTypes(ctx)
fmt.Println(intentTypes)

// 查看所有注册的 provider
providers, _ := client.ListProviders(ctx)
for _, p := range providers {
    fmt.Printf("%s: %s\n", p.ProviderID, p.Model)
}
```
:::

---

## 认证方式

| 方式 | 说明 |
|------|------|
| API Key | `Authorization: Bearer <key>` — 标准密钥认证 |
| Wallet Auth | EIP-191 签名 — 加密钱包签名认证 |

::: code-group
```python [Python]
# API Key 认证
client = IntentClient(api_key="jc_live_xxx")

# 自定义 base URL
client = IntentClient(api_key="jc_live_xxx", base_url="https://api.jarvisclaw.ai")
```
```go [Go]
// API Key 认证
client := jc.New("jc_live_xxx")

// 自定义选项
client := jc.New("jc_live_xxx", jc.WithBaseURL("https://api.jarvisclaw.ai"))
```
:::

---

## 错误处理

::: code-group
```python [Python]
from jarvisclaw import IntentClient
from jarvisclaw.exceptions import APIError, BudgetExceededError

client = IntentClient(api_key="YOUR_API_KEY")

try:
    result = client.execute(
        intent="chat_completion",
        payload={"messages": [{"role": "user", "content": "hi"}]},
        constraints={"max_price_usd": 0.001},
    )
except BudgetExceededError as e:
    print(f"Budget exceeded: {e}")
except APIError as e:
    print(f"API error [{e.status_code}]: {e.message}")
```
```go [Go]
raw, err := client.Execute(ctx, jc.ExecuteRequest{
    Intent: "chat_completion",
    Payload: map[string]any{
        "messages": []map[string]any{{"role": "user", "content": "hi"}},
    },
})
if err != nil {
    // 检查具体错误类型
    fmt.Printf("Error: %v\n", err)
    return
}
```
:::

---

## optimize_for 策略说明

| 值 | 行为 |
|----|------|
| `cost` | 选择最便宜的满足约束的 provider |
| `quality` | 选择评分最高的 provider (可能更贵) |
| `speed` | 选择延迟最低的 provider |
| `balance` | 综合考虑价格、质量、延迟 (默认) |

---

## 与 MCP 的关系

AIP 的所有 endpoint 同时作为 MCP Tool 暴露，Agent 可通过 MCP 协议发现和调用 AIP 能力：

```
MCP Tool: jarvisclaw/intent_resolve
MCP Tool: jarvisclaw/intent_execute
MCP Tool: jarvisclaw/intent_execute_budget
MCP Tool: jarvisclaw/intent_audit
```

---

## 相关链接

- [AIP 协议规范](./aip-spec.md)
- [Python SDK 文档](/api/python/)
- [Go SDK 文档](/api/go/)
- [Provider 注册指南](../agent-registry.md)
- [计费说明](../billing.md)
