# Prediction Markets API

Real-time prediction market data via Predexon. 58 endpoints across 11 categories: Polymarket (26), Kalshi (3), dFlow (3), Binance Futures (2), Cross-Venue Matching (8), Sports (4), Limitless/Opinion/Predict.Fun (6), UMA Oracle (2), Wallet Identity (3).

**Base URL:** `https://api.jarvisclaw.ai/v1/marketplace/prediction`

::: tip Surf also has prediction data
The [Crypto Data (Surf)](/api/crypto-data) API includes 17 prediction market endpoints under `/v1/marketplace/surf/prediction-market/*` at $0.0075/call. This Predexon service is a dedicated prediction-only provider with more endpoints (58 vs 17), deeper data (orderbooks, candlesticks, leaderboards), and lower pricing ($0.001/call GET).
:::

## Pricing

| Endpoint Type | Price | Description |
|---------------|-------|-------------|
| GET endpoints | $0.001/request | Market listings, events, pricing, candlesticks, volume |
| POST / Wallet | $0.005/request | Wallet positions, PnL, identity queries, cross-venue search |

## All Endpoints (58)

### Polymarket (26 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /polymarket/markets | List active markets with filtering and pagination |
| GET /polymarket/market/{id} | Get single market details by condition ID |
| GET /polymarket/events | List events (grouped markets) |
| GET /polymarket/event/{slug} | Get event details by slug |
| GET /polymarket/categories | List all available categories |
| GET /polymarket/pricing/{conditionId} | Current best bid/ask pricing |
| GET /polymarket/pricing/history/{conditionId} | Historical price snapshots |
| GET /polymarket/candlesticks/{conditionId} | OHLCV candlestick data |
| GET /polymarket/volume/{conditionId} | Volume history |
| GET /polymarket/volume/aggregate | Aggregate platform volume stats |
| GET /polymarket/orderbook/{conditionId} | Full order book depth |
| GET /polymarket/trades/{conditionId} | Recent trades list |
| GET /polymarket/trades/live | Live trade feed (most recent across all markets) |
| GET /polymarket/positions/{address} | Wallet open positions |
| GET /polymarket/positions/history/{address} | Historical position changes |
| GET /polymarket/pnl/{address} | Wallet realized + unrealized PnL |
| GET /polymarket/wallet/{address} | Combined wallet summary (positions + PnL) |
| GET /polymarket/leaderboard | Top traders by PnL |
| GET /polymarket/leaderboard/volume | Top traders by volume |
| GET /polymarket/activity/{address} | Recent wallet activity (buys/sells/redemptions) |
| GET /polymarket/rewards/{address} | Liquidity rewards earned |
| GET /polymarket/related/{conditionId} | Related markets by topic |
| GET /polymarket/comments/{conditionId} | Market comments/discussion |
| GET /polymarket/resolution/{conditionId} | Resolution details (for resolved markets) |
| GET /polymarket/liquidity/{conditionId} | Liquidity provider stats |
| GET /polymarket/stats | Platform-wide statistics |

### Kalshi (3 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /kalshi/markets | List Kalshi markets with category/status filter |
| GET /kalshi/market/{ticker} | Get market details by ticker |
| GET /kalshi/events | List Kalshi events |

### dFlow (3 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /dflow/markets | List dFlow prediction markets |
| GET /dflow/market/{id} | Get dFlow market details |
| GET /dflow/orderbook/{id} | dFlow order book |

### Binance Futures (2 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /binance/long-short | Long/short ratio for futures pairs |
| GET /binance/open-interest | Open interest history |

### Cross-Venue Matching (8 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /markets/search | Search across all venues by keyword |
| GET /markets/trending | Trending markets across all venues |
| GET /markets/new | Newly created markets |
| GET /markets/resolving-soon | Markets resolving within 24-72h |
| GET /markets/highest-volume | Highest volume markets cross-venue |
| GET /markets/compare/{topic} | Compare pricing across venues for same topic |
| GET /markets/categories | Unified category list across all venues |
| GET /markets/arbitrage | Price discrepancies between venues |

### Sports (4 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /sports/markets | Sports prediction markets (all venues) |
| GET /sports/events | Upcoming sporting events with markets |
| GET /sports/leagues | Supported leagues and sports |
| GET /sports/live | Live in-play markets |

### Limitless / Opinion / Predict.Fun (6 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /limitless/markets | List Limitless markets |
| GET /limitless/market/{id} | Limitless market details |
| GET /opinion/markets | List Opinion markets |
| GET /opinion/market/{id} | Opinion market details |
| GET /predictfun/markets | List Predict.Fun markets |
| GET /predictfun/market/{id} | Predict.Fun market details |

### UMA Oracle (2 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /uma/assertions | UMA optimistic oracle assertions |
| GET /uma/disputes | Active UMA disputes |

### Wallet Identity (3 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /wallet/identity/{address} | Resolve wallet to known trader identity |
| GET /wallet/portfolio/{address} | Cross-venue prediction portfolio |
| GET /wallet/history/{address} | Trade history across all venues |

---

## Detailed Endpoint Reference

### GET /polymarket/markets

List active Polymarket prediction markets with filtering and pagination.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Results per page. Default: `20`, Max: `100` |
| `offset` | integer | No | Pagination offset. Default: `0` |
| `category` | string | No | Filter: `politics`, `crypto`, `sports`, `science`, `culture`, `business`, `tech` |
| `status` | string | No | Filter: `active`, `resolved`, `all`. Default: `active` |
| `sort` | string | No | Sort by: `volume`, `liquidity`, `newest`, `ending_soon`. Default: `volume` |

#### Response

```json
{
  "markets": [
    {
      "id": "0x1234abcd...",
      "question": "Will AI pass the Turing test by 2027?",
      "yes_price": 0.72,
      "no_price": 0.28,
      "volume": 1250000,
      "liquidity": 340000,
      "end_date": "2027-12-31",
      "category": "tech",
      "created_at": "2025-06-01T10:00:00Z"
    }
  ],
  "total": 1432
}
```

---

### GET /polymarket/wallet/{address}

Get wallet positions and PnL for a Polymarket address.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | string | Yes | Ethereum wallet address (0x-prefixed, path parameter) |

#### Response

```json
{
  "address": "0xAbC123def456...",
  "positions": [
    {
      "market_id": "0x1234abcd...",
      "question": "Will AI pass the Turing test by 2027?",
      "side": "yes",
      "shares": 500,
      "avg_price": 0.65,
      "current_price": 0.72,
      "unrealized_pnl": 35.00
    }
  ],
  "total_value": 2450.00,
  "realized_pnl": 180.50,
  "open_positions": 3
}
```

---

### GET /kalshi/markets

List active Kalshi prediction markets.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Results per page. Default: `20`, Max: `100` |
| `offset` | integer | No | Pagination offset. Default: `0` |
| `category` | string | No | Filter: `economics`, `politics`, `weather`, `tech`, `finance`, `sports` |
| `status` | string | No | Market status: `open`, `closed`, `settled`. Default: `open` |
| `series_ticker` | string | No | Filter by series (e.g., `KXBTC`, `KXINX`, `KXFED`) |

#### Response

```json
{
  "markets": [
    {
      "ticker": "KXUSRECESSION-26",
      "title": "US recession in 2026?",
      "yes_price": 0.28,
      "no_price": 0.72,
      "volume": 4200000,
      "close_time": "2026-12-31T23:59:00Z",
      "category": "economics"
    }
  ],
  "total": 847
}
```

---

### GET /markets/search

Search for markets across all providers by keyword or topic.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | Yes | Search query string |
| `providers` | string | No | Comma-separated: `polymarket`, `kalshi`, `dflow`, `limitless`. Default: all |
| `limit` | integer | No | Max results. Default: `20`, Max: `50` |
| `status` | string | No | Filter by market status |

#### Response

```json
{
  "results": [
    {
      "provider": "polymarket",
      "id": "0x5678efgh...",
      "question": "Will Bitcoin exceed $200K by end of 2026?",
      "yes_price": 0.41,
      "volume": 3800000
    },
    {
      "provider": "kalshi",
      "ticker": "KXBTC-200K-26",
      "title": "Bitcoin above $200K before 2027?",
      "yes_price": 0.38,
      "volume": 1200000
    }
  ],
  "total": 14
}
```

---

### GET /markets/arbitrage

Find price discrepancies for the same topic across different venues.

#### Response

```json
{
  "opportunities": [
    {
      "topic": "Bitcoin above $200K by 2027",
      "polymarket_yes": 0.41,
      "kalshi_yes": 0.38,
      "spread": 0.03,
      "polymarket_id": "0x5678efgh...",
      "kalshi_ticker": "KXBTC-200K-26"
    }
  ]
}
```

---

### GET /polymarket/leaderboard

Top traders ranked by realized PnL.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `period` | string | No | Time period: `24h`, `7d`, `30d`, `all`. Default: `30d` |
| `limit` | integer | No | Number of traders. Default: `25`, Max: `100` |

#### Response

```json
{
  "traders": [
    {
      "address": "0xabc...",
      "pnl": 125000.50,
      "volume": 2400000,
      "win_rate": 0.68,
      "trades": 342
    }
  ],
  "period": "30d"
}
```

---

## Errors

| HTTP Code | Error Code | Description | Resolution |
|-----------|------------|-------------|------------|
| 400 | `invalid_address` | Wallet address format is invalid | Use 0x + 40 hex characters |
| 404 | `market_not_found` | Market ID does not exist or has been delisted | Fetch /markets to get current active IDs |
| 404 | `market_closed` | Market has resolved and is no longer active | Check end_date field; query active markets |
| 429 | `rate_limited` | Too many requests | Max 100 req/min per key |

### Error Response Format

```json
{
  "error": {
    "code": "market_not_found",
    "message": "No market found with ID '0x123...'. It may have been delisted or resolved."
  }
}
```

## Code Examples

::: code-group

```bash [cURL]
# List Polymarket markets (politics category)
curl "https://api.jarvisclaw.ai/v1/marketplace/prediction/polymarket/markets?limit=5&category=politics" \
  -H "Authorization: Bearer sk-your-api-key"

# Get wallet positions and PnL
curl "https://api.jarvisclaw.ai/v1/marketplace/prediction/polymarket/wallet/0xAbC123def456" \
  -H "Authorization: Bearer sk-your-api-key"

# List Kalshi markets (economics category)
curl "https://api.jarvisclaw.ai/v1/marketplace/prediction/kalshi/markets?limit=5&category=economics" \
  -H "Authorization: Bearer sk-your-api-key"

# Search markets across all providers
curl "https://api.jarvisclaw.ai/v1/marketplace/prediction/markets/search?q=bitcoin+2026&providers=polymarket,kalshi" \
  -H "Authorization: Bearer sk-your-api-key"

# Get cross-venue arbitrage opportunities
curl "https://api.jarvisclaw.ai/v1/marketplace/prediction/markets/arbitrage" \
  -H "Authorization: Bearer sk-your-api-key"

# Polymarket leaderboard (30d)
curl "https://api.jarvisclaw.ai/v1/marketplace/prediction/polymarket/leaderboard?period=30d&limit=10" \
  -H "Authorization: Bearer sk-your-api-key"
```

```python [Python (API Key)]
from jarvisclaw import MarketplaceClient

client = MarketplaceClient(api_key="sk-your-api-key")

# List Polymarket markets
markets = client.call("prediction", "/polymarket/markets", method="GET", params={
    "limit": 10,
    "category": "politics",
})
for m in markets["markets"]:
    print(f"{m['question']}: YES {m['yes_price']:.0%} / NO {m['no_price']:.0%}")

# Get wallet PnL
wallet = client.call("prediction", "/polymarket/wallet/0xAbC123def456", method="GET")
print(f"Total PnL: ${wallet['realized_pnl']:.2f}")

# List Kalshi markets
kalshi = client.call("prediction", "/kalshi/markets", method="GET", params={
    "limit": 10,
    "category": "economics",
})
for m in kalshi["markets"]:
    print(f"{m['title']}: YES {m['yes_price']:.0%}")

# Search across providers
results = client.call("prediction", "/markets/search", method="GET", params={
    "q": "bitcoin 2026",
    "providers": "polymarket,kalshi",
    "limit": 10,
})
for r in results["results"]:
    print(f"[{r['provider']}] {r.get('question', r.get('title'))}: YES {r['yes_price']}")

# Arbitrage opportunities
arb = client.call("prediction", "/markets/arbitrage", method="GET")
for opp in arb["opportunities"]:
    print(f"{opp['topic']}: spread {opp['spread']:.1%}")
```

```python [Python (x402 Agent)]
from jarvisclaw import MarketplaceClient

# Base chain (EVM) — pays per-call via USDC
client = MarketplaceClient(private_key="0x<evm-private-key>")

# Or Solana
# client = MarketplaceClient(private_key="<solana-bs58-keypair>")

# List Polymarket markets
markets = client.call("prediction", "/polymarket/markets", method="GET", params={
    "limit": 10,
    "category": "crypto",
})
for m in markets["markets"]:
    print(f"{m['question']}: YES {m['yes_price']:.0%} / NO {m['no_price']:.0%}")

# Get wallet PnL
wallet = client.call("prediction", "/polymarket/wallet/0xAbC123def456", method="GET")
print(f"Total PnL: ${wallet['realized_pnl']:.2f}")

# List Kalshi markets
kalshi = client.call("prediction", "/kalshi/markets", method="GET", params={
    "limit": 10,
    "category": "economics",
})
for m in kalshi["markets"]:
    print(f"{m['title']}: YES {m['yes_price']:.0%}")

# Search across all venues
results = client.call("prediction", "/markets/search", method="GET", params={
    "q": "US election 2026",
    "providers": "polymarket,kalshi",
    "limit": 10,
})
for r in results["results"]:
    print(f"[{r['provider']}] YES {r['yes_price']}")
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
	mc, _ := jc.NewMarketplaceClient(jc.WithAPIKey("sk-your-api-key"))

	// List Polymarket markets
	markets, _ := mc.Call(ctx, "prediction", "/polymarket/markets", jc.WithParams(map[string]any{
		"limit":    10,
		"category": "politics",
	}))
	fmt.Println("Polymarket markets:", markets)

	// Get wallet positions
	wallet, _ := mc.Call(ctx, "prediction", "/polymarket/wallet/0xAbC123def456", nil)
	fmt.Println("Wallet:", wallet)

	// List Kalshi markets
	kalshi, _ := mc.Call(ctx, "prediction", "/kalshi/markets", jc.WithParams(map[string]any{
		"limit":    10,
		"category": "economics",
	}))
	fmt.Println("Kalshi markets:", kalshi)

	// Cross-venue search
	results, _ := mc.Call(ctx, "prediction", "/markets/search", jc.WithParams(map[string]any{
		"q":         "bitcoin 2026",
		"providers": "polymarket,kalshi",
		"limit":     10,
	}))
	fmt.Println("Search results:", results)
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
	// x402 Agent wallet — pays per-call via USDC on Base
	mc, _ := jc.NewMarketplaceClient(jc.WithPrivateKey("0x<evm-private-key>"))

	// List Polymarket markets
	markets, _ := mc.Call(ctx, "prediction", "/polymarket/markets", jc.WithParams(map[string]any{
		"limit":    10,
		"category": "politics",
	}))
	fmt.Println("Polymarket markets:", markets)

	// Get wallet positions
	wallet, _ := mc.Call(ctx, "prediction", "/polymarket/wallet/0xAbC123def456", nil)
	fmt.Println("Wallet:", wallet)

	// List Kalshi markets
	kalshi, _ := mc.Call(ctx, "prediction", "/kalshi/markets", jc.WithParams(map[string]any{
		"limit":    10,
		"category": "economics",
	}))
	fmt.Println("Kalshi markets:", kalshi)

	// Arbitrage opportunities
	arb, _ := mc.Call(ctx, "prediction", "/markets/arbitrage", nil)
	fmt.Println("Arbitrage:", arb)
}
```

:::

## Limitations

- **Read-only** — cannot place orders or execute trades
- **No WebSocket** — poll endpoints for updates; data refreshes every ~5s
- **Ethereum addresses only** — wallet lookups require full `0x`-prefixed addresses, ENS not resolved
- **Sports markets delayed** — may lag up to 60s due to upstream rate limits
- **Cross-venue matching best-effort** — not all markets have counterparts on other venues
- **Price format differs by venue** — Polymarket: decimals (0.00-1.00), Kalshi: cents (0-100)
- **Rate limit** — 100 requests/minute per API key
- **Leaderboard cache** — updated every 15 minutes, not real-time
