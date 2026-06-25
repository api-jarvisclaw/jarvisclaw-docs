# AIP: Agent Intent Protocol Specification

**Version:** 1.0.0-draft  
**Status:** Draft  
**Date:** 2026-06-24  
**Authors:** JarvisClaw Team

---

## Abstract

The Agent Intent Protocol (AIP) is an open protocol that enables AI agents to discover, negotiate with, and pay for services from other AI agents or API providers through declarative intents. Unlike traditional API integration that requires per-service adapters, AIP allows agents to express *what* they need rather than *how* to get it.

AIP combines three capabilities into a single protocol:
1. **Intent Resolution** — semantic matching of agent needs to available providers
2. **Payment Negotiation** — built-in pricing discovery and multi-rail payment (x402, balance, credit)
3. **Execution Orchestration** — risk-scored, budget-constrained request fulfillment

## 1. Design Principles

| Principle | Description |
|-----------|-------------|
| **Intent-First** | Agents declare desired outcomes, not specific endpoints |
| **Payment-Native** | Every call has a payment rail; no free-tier ambiguity |
| **Provider-Agnostic** | Providers register capabilities; protocol handles routing |
| **Risk-Aware** | Built-in risk scoring prevents budget overruns and abuse |
| **MCP-Compatible** | AIP endpoints are also exposed as MCP tools for discoverability |

## 2. Protocol Overview

```
┌──────────────┐         ┌───────────────────────────────┐
│   Agent A    │         │       AIP Gateway             │
│  (Consumer)  │         │                               │
│              │  POST   │  ┌─────────┐  ┌───────────┐  │
│  "I need     │────────▶│  │ Resolve │─▶│ Risk Score│  │
│   GPT-4 chat │         │  └─────────┘  └───────────┘  │
│   under $0.01│         │       │                       │
│   per call"  │         │       ▼                       │
│              │         │  ┌─────────┐  ┌───────────┐  │
│              │◀────────│  │ Route   │─▶│  Execute  │  │
│              │  Result  │  └─────────┘  └───────────┘  │
└──────────────┘         │       │                       │
                         │       ▼                       │
                         │  ┌─────────┐                  │
                         │  │ Settle  │                  │
                         │  └─────────┘                  │
                         └───────────────────────────────┘
```

## 3. Intent Types

AIP defines these core intent types:

| Intent Type | Description | Example Use |
|-------------|-------------|-------------|
| `chat_completion` | Text generation / conversation | Agent needs LLM response |
| `image_generation` | Create images from text | Agent needs DALL-E/SD output |
| `video_generation` | Create video from text/image | Agent needs video content |
| `text_to_speech` | Convert text to audio | Agent needs voice output |
| `web_search` | Search the web | Agent needs real-time info |
| `knowledge_search` | Search domain knowledge bases | Agent needs RAG results |
| `tool_call` | Execute an MCP tool | Agent needs tool execution |

Custom intent types follow the format: `x-{vendor}/{type}` (e.g., `x-jarvisclaw/code_review`).

## 4. Endpoints

### 4.1 Intent Resolution

```
POST /v1/intent/resolve
```

**Purpose:** Find the best provider(s) for a given intent.

**Request:**
```json
{
  "intent": "chat_completion",
  "constraints": {
    "max_price_usd": 0.01,
    "max_latency_ms": 3000,
    "features": ["function_calling", "json_mode"],
    "context_window_min": 128000
  },
  "preferences": {
    "optimize_for": "cost" | "quality" | "speed",
    "preferred_providers": ["openai", "anthropic"],
    "excluded_providers": ["azure"]
  },
  "context": {
    "input_tokens_estimate": 2000,
    "output_tokens_estimate": 500
  }
}
```

**Response:**
```json
{
  "matches": [
    {
      "provider_id": "deepseek-chat",
      "score": 0.95,
      "price_usd": 0.0004,
      "capabilities": ["function_calling", "json_mode"],
      "context_window": 131072,
      "latency_p50_ms": 800
    },
    {
      "provider_id": "gpt-4o-mini",
      "score": 0.88,
      "price_usd": 0.0015,
      "capabilities": ["function_calling", "json_mode"],
      "context_window": 128000,
      "latency_p50_ms": 1200
    }
  ],
  "resolution_id": "res_abc123",
  "expires_at": "2026-06-24T12:05:00Z"
}
```

### 4.2 Intent Execution

```
POST /v1/intent/execute
```

**Purpose:** Resolve + pay + execute in a single call.

**Request:**
```json
{
  "intent": "chat_completion",
  "constraints": { "max_price_usd": 0.05 },
  "preferences": { "optimize_for": "quality" },
  "payload": {
    "messages": [
      {"role": "user", "content": "Explain quantum computing"}
    ],
    "temperature": 0.7
  },
  "payment": {
    "method": "x402",
    "max_amount_usd": 0.05
  }
}
```

**Response:**
```json
{
  "execution_id": "exec_xyz789",
  "provider_used": "claude-sonnet-4-20250514",
  "result": {
    "choices": [
      {
        "message": {
          "role": "assistant",
          "content": "Quantum computing leverages..."
        }
      }
    ]
  },
  "billing": {
    "amount_usd": 0.0089,
    "payment_method": "x402",
    "tx_hash": "0xabc...",
    "breakdown": {
      "input_tokens": 12,
      "output_tokens": 340,
      "provider_cost": 0.0086,
      "platform_fee": 0.0003
    }
  }
}
```

### 4.3 Budget-Constrained Execution

```
POST /v1/intent/execute-budget
```

**Purpose:** Execute with a hard budget cap; fails rather than overspends.

Same as `/execute` but adds:
```json
{
  "budget": {
    "session_limit_usd": 1.00,
    "per_call_limit_usd": 0.05,
    "daily_limit_usd": 10.00
  }
}
```

### 4.4 Provider Registry

```
GET /v1/providers
```

Returns all registered providers with capabilities, pricing, and status.

### 4.5 Wallet Operations

```
GET  /v1/wallet/balance    — Current balance across all payment rails
GET  /v1/wallet/history    — Transaction history
GET  /v1/wallet/limits     — Current budget limits
PUT  /v1/wallet/limits     — Update budget constraints
GET  /v1/wallet/pools      — Available liquidity pools
```

## 5. Payment Rails

AIP supports multiple payment mechanisms through its payment router:

| Rail | Description | Settlement Time | Min Amount |
|------|-------------|-----------------|------------|
| `balance` | Pre-deposited platform balance | Instant | $0.0001 |
| `x402` | On-chain USDC via x402 protocol | ~2s (Base L2) | $0.001 |
| `credit_async` | Post-paid credit line | Deferred | $0.01 |

### 5.1 x402 Payment Flow

```
Agent → AIP Gateway: POST /v1/intent/execute (no payment header)
                   ← 402 Payment Required + price quote
Agent → AIP Gateway: POST /v1/intent/execute + PAYMENT-SIGNATURE header
                   ← 200 OK + result + settlement receipt
```

The `PAYMENT-SIGNATURE` header contains an EIP-712 typed signature authorizing USDC transfer on Base (EIP-155 chain ID 8453).

### 5.2 Payment Negotiation

Agents can probe pricing without executing:
```
POST /v1/intent/resolve → get price estimates
```
Then decide whether to proceed based on budget constraints.

## 6. MCP Integration

AIP is also accessible via MCP (Model Context Protocol) tools, allowing any MCP-compatible client to use AIP:

```
POST /mcp
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "discover_agents",
    "arguments": {"capability": "image_generation", "max_price": 0.05}
  }
}
```

Available MCP tools:
- `list_models` — List available AI models
- `chat` — Call any model (pay-per-use)
- `search_apis` — Find APIs in marketplace
- `get_api_detail` — Get API pricing and schema
- `discover_agents` — Find agents by capability

## 7. Risk Scoring

Every execution passes through a risk scorer before proceeding:

```
Risk Score = f(amount, frequency, sender_reputation, intent_complexity)
```

| Score Range | Action |
|-------------|--------|
| 0.0 – 0.3 | Allow (low risk) |
| 0.3 – 0.7 | Allow with enhanced logging |
| 0.7 – 0.9 | Require additional verification |
| 0.9 – 1.0 | Reject |

## 8. Error Codes

| Code | Meaning |
|------|---------|
| `INTENT_NOT_FOUND` | No provider matches the intent + constraints |
| `BUDGET_EXCEEDED` | Request would exceed budget limits |
| `PAYMENT_FAILED` | Payment rail rejected the transaction |
| `PROVIDER_UNAVAILABLE` | Selected provider is down/unreachable |
| `RISK_REJECTED` | Risk score too high |
| `RESOLUTION_EXPIRED` | Resolution ID expired (5-minute TTL) |

## 9. Comparison with Existing Protocols

| Feature | AIP | x402 | A2A (Google) | MCP |
|---------|-----|------|--------------|-----|
| Intent resolution | ✅ | ❌ | ❌ | ❌ |
| Payment native | ✅ | ✅ | ❌ | ❌ |
| Provider discovery | ✅ | ❌ | ✅ | ✅ (tools/list) |
| Risk scoring | ✅ | ❌ | ❌ | ❌ |
| Budget constraints | ✅ | ❌ | ❌ | ❌ |
| Multi-payment rail | ✅ | USDC only | N/A | N/A |
| Streaming | ✅ (SSE) | ❌ | ✅ | ✅ (SSE) |

## 10. Implementation Status

- **Gateway:** `api.jarvisclaw.ai`
- **MCP Endpoint:** `api.jarvisclaw.ai/mcp`
- **Supported Intents:** 6 core types + extensible
- **Payment Rails:** balance, x402 (Base USDC), credit_async
- **Providers:** 40+ AI models aggregated

## 11. Getting Started

```bash
# 1. Resolve an intent (free, no auth)
curl -X POST https://api.jarvisclaw.ai/v1/intent/resolve \
  -H "Content-Type: application/json" \
  -d '{"intent":"chat_completion","preferences":{"optimize_for":"cost"}}'

# 2. Execute with API key
curl -X POST https://api.jarvisclaw.ai/v1/intent/execute \
  -H "Authorization: Bearer sk-your-key" \
  -H "Content-Type: application/json" \
  -d '{"intent":"chat_completion","payload":{"messages":[{"role":"user","content":"Hello"}]}}'

# 3. Execute with x402 (no account needed)
# First get price from resolve, then sign payment and include header
curl -X POST https://api.jarvisclaw.ai/v1/intent/execute \
  -H "PAYMENT-SIGNATURE: <eip712-signed-usdc-authorization>" \
  -H "Content-Type: application/json" \
  -d '{"intent":"chat_completion","payload":{"messages":[{"role":"user","content":"Hello"}]}}'
```

---

*AIP is an open protocol. Implementations and extensions are welcome.*
