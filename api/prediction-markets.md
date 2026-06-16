# Prediction Markets

Access prediction market data across Polymarket and Kalshi with 58 endpoints for markets, positions, and analytics.

## Base URL

```
/v1/marketplace/prediction/*
```

## Pricing

| Operation | Price |
|-----------|-------|
| GET requests (read) | $0.001 |
| POST requests / wallet queries | $0.005 |

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/polymarket/markets` | List Polymarket markets |
| GET | `/polymarket/markets/:id` | Get market details |
| GET | `/polymarket/wallet/:address` | Wallet positions & PnL |
| GET | `/kalshi/markets` | List Kalshi markets |
| GET | `/kalshi/markets/:ticker` | Get market details |
| GET | `/markets/search` | Cross-venue market search |

## Polymarket Markets

`GET /v1/marketplace/prediction/polymarket/markets`

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | Filter: `active`, `resolved`, `all`. Default: `active` |
| `category` | string | No | Category filter (e.g., `politics`, `crypto`, `sports`) |
| `limit` | integer | No | Results per page. Default: `20` |
| `offset` | integer | No | Pagination offset. Default: `0` |
| `sort` | string | No | Sort by: `volume`, `liquidity`, `newest`. Default: `volume` |

### Response

```json
{
  "markets": [
    {
      "id": "0xabc123",
      "question": "Will BTC reach $100k by end of 2025?",
      "category": "crypto",
      "status": "active",
      "outcomes": ["Yes", "No"],
      "prices": [0.72, 0.28],
      "volume": 5200000,
      "liquidity": 850000,
      "end_date": "2025-12-31T23:59:59Z"
    }
  ],
  "total": 1523,
  "limit": 20,
  "offset": 0
}
```

## Polymarket Wallet

`GET /v1/marketplace/prediction/polymarket/wallet/:address`

Get wallet positions and profit/loss for a Polymarket address.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | string | Yes | Wallet address (path parameter) |

### Response

```json
{
  "address": "0x1234...abcd",
  "total_pnl": 1250.00,
  "positions": [
    {
      "market_id": "0xabc123",
      "question": "Will BTC reach $100k by end of 2025?",
      "outcome": "Yes",
      "shares": 500,
      "avg_price": 0.65,
      "current_price": 0.72,
      "unrealized_pnl": 35.00
    }
  ]
}
```

## Kalshi Markets

`GET /v1/marketplace/prediction/kalshi/markets`

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | Filter: `open`, `closed`, `settled`. Default: `open` |
| `series_ticker` | string | No | Filter by series (e.g., `KXBTC`) |
| `limit` | integer | No | Results per page. Default: `20` |
| `cursor` | string | No | Pagination cursor |

### Response

```json
{
  "markets": [
    {
      "ticker": "KXBTC-25DEC31-T100000",
      "title": "Bitcoin above $100,000 on December 31?",
      "status": "open",
      "yes_price": 72,
      "no_price": 28,
      "volume": 125000,
      "close_time": "2025-12-31T23:59:59Z"
    }
  ],
  "cursor": "next_page_token"
}
```

## Cross-Venue Search

`GET /v1/marketplace/prediction/markets/search`

Search across all supported prediction market venues.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | Yes | Search query |
| `venue` | string | No | Filter by venue: `polymarket`, `kalshi`, or omit for all |
| `status` | string | No | Market status filter |
| `limit` | integer | No | Max results. Default: `20` |

### Response

```json
{
  "results": [
    {
      "venue": "polymarket",
      "id": "0xabc123",
      "question": "Will BTC reach $100k by end of 2025?",
      "yes_price": 0.72,
      "volume": 5200000
    },
    {
      "venue": "kalshi",
      "id": "KXBTC-25DEC31-T100000",
      "question": "Bitcoin above $100,000 on December 31?",
      "yes_price": 0.72,
      "volume": 125000
    }
  ]
}
```

## Examples

::: code-group

```python [Python]
import requests

BASE = "https://api.jarvisclaw.ai/v1/marketplace/prediction"
HEADERS = {
    "Authorization": "Bearer sk-your-api-key",
}

# Search prediction markets
resp = requests.get(f"{BASE}/markets/search", headers=HEADERS, params={
    "q": "bitcoin 100k",
})
print(resp.json())

# List active Polymarket markets by volume
resp = requests.get(f"{BASE}/polymarket/markets", headers=HEADERS, params={
    "status": "active",
    "sort": "volume",
    "limit": 10,
})
for market in resp.json()["markets"]:
    print(f"{market['question']} — Yes: {market['prices'][0]}")

# Check wallet positions
resp = requests.get(
    f"{BASE}/polymarket/wallet/0x1234abcd",
    headers=HEADERS,
)
print(f"Total PnL: ${resp.json()['total_pnl']}")
```

```bash [cURL]
# Search across all venues
curl "https://api.jarvisclaw.ai/v1/marketplace/prediction/markets/search?q=election" \
  -H "Authorization: Bearer sk-your-api-key"

# List Polymarket markets
curl "https://api.jarvisclaw.ai/v1/marketplace/prediction/polymarket/markets?status=active&limit=5" \
  -H "Authorization: Bearer sk-your-api-key"

# Get Kalshi market details
curl "https://api.jarvisclaw.ai/v1/marketplace/prediction/kalshi/markets/KXBTC-25DEC31-T100000" \
  -H "Authorization: Bearer sk-your-api-key"
```

:::

## Notes

- 58 total endpoints across Polymarket and Kalshi
- All prices are in probability format (0.00 to 1.00 for Polymarket, 0-100 cents for Kalshi)
- Market data refreshes every 5 seconds
- Wallet queries may take longer due to on-chain data aggregation
- Read-only API — order placement is not supported
