# Wallet & Treasury API

The Wallet API gives agents and developers programmatic access to balance, spending history, pool allocation, and limits — enabling autonomous financial management.

## Overview

Your JarvisClaw wallet has three balance sources:

| Source | Description |
|--------|-------------|
| **Platform Quota** | Prepaid credits (top-up via dashboard) |
| **HD Wallet (USDC)** | On-chain Base + Solana USDC |
| **Subscription** | Monthly plan quota (if active) |

## Check Balance

::: code-group

```bash [curl]
curl https://api.jarvisclaw.ai/v1/wallet/balance \
  -H "Authorization: Bearer sk-YOUR-KEY"
```

```python [Python]
from jarvisclaw import Agent

agent = Agent(api_key="sk-YOUR-KEY")
bal = agent.balance()
print(f"Total: ${bal['total_usd']}")
print(f"Quota: {bal['quota']} units (${bal['quota_usd']})")
```

```go [Go]
bal, _ := c.WalletBalance(ctx)
fmt.Printf("Total: %s USD\n", bal.TotalUSD)
```

:::

### Response

```json
{
  "quota": 850000,
  "quota_usd": "1.7000",
  "hd_wallet": {
    "base_usdc": "12.54",
    "solana_usdc": "3.20"
  },
  "subscription": {
    "active": true,
    "remaining_quota": 500000
  },
  "total_usd": "17.4400"
}
```

## Pool Allocation (Treasury)

Your balance is logically split into pools for autonomous budget management:

| Pool | Default % | Purpose |
|------|-----------|---------|
| Operations | 60% | Day-to-day API calls |
| Insurance | 15% | Retry buffer for upstream failures |
| Savings | 15% | Reserved for expansion |
| Dividends | 10% | Owner withdrawal |

```bash
curl https://api.jarvisclaw.ai/v1/wallet/pools \
  -H "Authorization: Bearer sk-YOUR-KEY"
```

```json
{
  "allocation": {
    "operations": 0.60,
    "insurance": 0.15,
    "savings": 0.15,
    "dividends": 0.10
  },
  "pool_balances": {
    "operations": "10.4640",
    "insurance": "2.6160",
    "savings": "2.6160",
    "dividends": "1.7440"
  }
}
```

## Spending Limits

Get and set autonomous spending limits:

```bash
# Get current limits
curl https://api.jarvisclaw.ai/v1/wallet/limits \
  -H "Authorization: Bearer sk-YOUR-KEY"

# Update limits
curl -X PUT https://api.jarvisclaw.ai/v1/wallet/limits \
  -H "Authorization: Bearer sk-YOUR-KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "daily_max_usd": 30.0,
    "per_request_max_usd": 0.5,
    "monthly_max_usd": 200.0,
    "auto_pause_below_usd": 5.0
  }'
```

## Transaction History

```bash
curl "https://api.jarvisclaw.ai/v1/wallet/history?page=1&page_size=20" \
  -H "Authorization: Bearer sk-YOUR-KEY"
```

```json
{
  "transactions": [
    {
      "id": 12345,
      "amount_quota": -300,
      "category": "inference",
      "model": "deepseek-chat",
      "use_time_seconds": 2,
      "created_at": 1718700000
    }
  ],
  "total": 1234,
  "page": 1
}
```

## Treasury SDK (Go)

For agents that need full financial autonomy — multi-pool management, rule engines, circuit breakers:

```bash
go get github.com/api-jarvisclaw/agent-treasury-go
```

```go
import "github.com/api-jarvisclaw/agent-treasury-go/treasury"

provider := treasury.NewJarvisClawProvider("https://api.jarvisclaw.ai", "sk-YOUR-KEY")
t := treasury.New(treasury.Config{
    AgentID: "my-trading-bot",
    Allocation: treasury.PoolAllocation{
        Operations: 0.70,
        Insurance:  0.10,
        Savings:    0.10,
        Dividends:  0.10,
    },
}, provider)

// Check budget before spending
ok, _ := t.ApproveSpend(0.003, "inference")
if ok {
    // make the API call
    t.Spend(0.003, "inference", "deepseek-chat")
}

// Autopilot: circuit breaker pauses spending if success rate drops
snapshot := t.Snapshot()
fmt.Printf("Operations pool: $%.4f\n", snapshot.Pools["operations"])
```

## API Reference

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/v1/wallet/balance` | Required | Unified balance (quota + HD + subscription) |
| GET | `/v1/wallet/history` | Required | Paginated transaction log |
| GET | `/v1/wallet/limits` | Required | Current spending limits |
| PUT | `/v1/wallet/limits` | Required | Update spending limits |
| GET | `/v1/wallet/pools` | Required | Pool allocation + balances |
