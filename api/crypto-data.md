# Crypto Data API (Surf)

83 endpoints across 12 domains via Surf. Exchange data (16 CEXes), Market Overview (rankings/fear-greed/ETF flows/liquidations/technical signals), On-Chain SQL (80+ ClickHouse tables across 7 networks), Wallet Intelligence (100M+ labeled wallets across 13 networks), Social/CT (Twitter mindshare/KOL tracking), Token Analytics, News, DeFi Protocols, VC Funds, Prediction Markets, and more. Standard $0.0075/call, Premium SQL $0.02/call.

**Base URL:** `https://api.jarvisclaw.ai/v1/marketplace/surf`

::: tip Dedicated Prediction Markets API
This page includes 17 prediction market endpoints via Surf. If you primarily need prediction data, consider the dedicated [Prediction Markets (Predexon)](/api/prediction-markets) service — 58 endpoints, deeper data (orderbooks, candlesticks, leaderboards, arbitrage), and lower pricing ($0.001/call vs $0.0075/call).
:::

## Authentication

Both methods are supported — all requests settle via x402 on-chain:

| Method | Header | Description |
|--------|--------|-------------|
| API Key | `Authorization: Bearer sk-...` | Platform signs x402 from your HD wallet automatically |
| Private Key (x402) | Automatic via SDK | Agent signs x402 directly from its own wallet |

See [Agent Payments (x402)](/x402) for full details on how both methods work.

## Pricing

| Tier | Price | Includes |
|------|-------|----------|
| Standard | $0.0075/call | exchange, market, social, wallet, token, news, fund, search, prediction-market, project, web |
| Premium SQL | $0.02/call | onchain/query, onchain/sql, onchain/schema |

## Exchange (7 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /exchange/markets | Trading pairs catalog — list all available trading pairs |
| GET /exchange/price | CEX ticker price (params: pair, exchange) |
| GET /exchange/perp | Perpetual contract snapshot — OI, funding rate, mark price (params: pair) |
| GET /exchange/depth | Order book depth — bids and asks (params: pair, exchange) |
| GET /exchange/klines | OHLCV candlesticks (params: pair, interval, limit) |
| GET /exchange/funding-history | Funding rate history (params: pair) |
| GET /exchange/long-short-ratio | Long/short ratio (params: pair) |

### Example: Exchange Price

```bash
curl "https://api.jarvisclaw.ai/v1/marketplace/surf/exchange/price?pair=BTC-USDT" \
  -H "Authorization: Bearer sk-your-api-key"
```

```json
{
  "data": [
    {
      "exchange": "binance",
      "pair": "BTC/USDT",
      "last": 63732,
      "bid": 63732,
      "ask": 63732.01,
      "high_24h": 63907.07,
      "low_24h": 62353,
      "volume_24h_base": 11787.64,
      "change_24h_pct": 1.705,
      "timestamp": 1717200000
    }
  ]
}
```

## Market (11 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /market/ranking | Token rankings by market cap (params: limit, category) |
| GET /market/fear-greed | Fear & Greed index |
| GET /market/futures | Futures overview — aggregate futures data |
| GET /market/price | Token price history (params: symbol, interval) |
| GET /market/etf | ETF flow history — BTC/ETH ETF inflows/outflows |
| GET /market/options | Options market data (params: symbol) |
| GET /market/liquidation/exchange-list | Liquidations by exchange |
| GET /market/liquidation/order | Large liquidation orders (params: limit) |
| GET /market/liquidation/chart | Liquidation chart data (params: symbol) |
| GET /market/onchain-indicator | On-chain indicators — NVT, SOPR, MVRV (params: symbol, metric) |
| GET /market/price-indicator | Technical indicators — RSI, MACD, Bollinger (params: symbol, indicator) |

### Example: Fear & Greed

```json
{
  "value": 72,
  "label": "Greed",
  "previous_close": 68,
  "timestamp": 1717200000
}
```

## On-chain (7 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /onchain/bridge/ranking | Bridge ranking — cross-chain bridge volume and TVL |
| GET /onchain/yield/ranking | Yield pool ranking — top DeFi yield opportunities |
| GET /onchain/gas-price | Gas price across chains (params: chain) |
| GET /onchain/tx | Transaction details (params: hash, chain) |
| GET /onchain/schema | ClickHouse schema — available tables and columns |
| POST /onchain/query | Natural-language blockchain query (params: source, question, limit) — see /onchain/sql for raw SQL |
| POST /onchain/sql | Raw SQL query against ClickHouse tables (params: sql) |

### Example: SQL Query

```bash
curl -X POST "https://api.jarvisclaw.ai/v1/marketplace/surf/onchain/sql" \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT from_address, SUM(value/1e18) as total_eth FROM ethereum.transactions WHERE block_time > now() - interval 1 hour GROUP BY from_address ORDER BY total_eth DESC LIMIT 10"}'
```

```json
{
  "columns": ["from_address", "total_eth"],
  "rows": [
    ["0xDef456...", 1250.5],
    ["0x789Abc...", 890.2]
  ],
  "row_count": 2,
  "execution_time_ms": 3200
}
```

## Wallet (6 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /wallet/detail | Wallet profile — labels, portfolio, risk score (params: address) |
| GET /wallet/history | Transaction history (params: address, limit) |
| GET /wallet/net-worth | Net-worth time series (params: address) |
| GET /wallet/transfers | Transfer history (params: address, limit) |
| GET /wallet/protocols | DeFi positions (params: address) |
| GET /wallet/labels/batch | Batch label lookup — max 100 addresses (params: addresses[]) |

### Example: Wallet Detail

```json
{
  "address": "0xBE0eB53F46cd790Cd...",
  "labels": ["Binance", "Hot Wallet"],
  "net_worth_usd": 2500000000,
  "chains": ["ethereum", "bsc", "arbitrum"],
  "risk_score": 12
}
```

## Social (11 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /social/detail | Social analytics — engagement metrics (params: handle) |
| GET /social/ranking | Mindshare ranking — top influencers (params: limit) |
| GET /social/smart-followers/history | Smart followers growth (params: handle) |
| GET /social/mindshare | Token mention share (params: q, interval) |
| GET /social/tweets | Bulk tweet lookup (params: ids) |
| GET /social/tweet/replies | Tweet replies (params: tweet_id, limit) |
| GET /social/user | Twitter profile (params: handle) |
| GET /social/user/followers | User followers (params: handle, limit) |
| GET /social/user/following | User following (params: handle, limit) |
| GET /social/user/posts | Recent tweets (params: handle, limit) |
| GET /social/user/replies | Recent replies (params: handle, limit) |

## Token (4 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /token/tokenomics | Token unlock/vesting schedule (params: symbol) |
| GET /token/dex-trades | DEX trade history (params: address, interval, limit) |
| GET /token/holders | Top holders by balance (params: address, chain, limit) |
| GET /token/transfers | Transfer history (params: address, interval, limit) |

## Fund (3 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /fund/detail | VC fund profile (params: slug) |
| GET /fund/portfolio | Fund holdings (params: slug) |
| GET /fund/ranking | Top VC funds (params: metric, limit, offset) |

## Project (3 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /project/detail | Project profile (params: slug) |
| GET /project/defi/metrics | DeFi protocol metrics (params: metric) |
| GET /project/defi/ranking | DeFi ranking by TVL (params: limit) |

## News (2 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /news/feed | AI-curated news feed (params: symbol, limit) |
| GET /news/detail | Article detail (params: id) |

## Search (11 endpoints)

| Endpoint | Description |
|----------|-------------|
| GET /search/airdrop | Search airdrops (params: q, limit) |
| GET /search/events | Search crypto events (params: q, limit) |
| GET /search/kalshi | Search Kalshi markets (params: q, limit) |
| GET /search/polymarket | Search Polymarket (params: q, limit) |
| GET /search/web | Web search (params: q, limit) |
| GET /search/project | Search crypto projects (params: q, limit) |
| GET /search/news | Search news articles (params: q, limit) |
| GET /search/wallet | Search labeled wallets (params: q, limit) |
| GET /search/fund | Search VC funds (params: q, limit) |
| GET /search/social/people | Search influencers (params: q, limit) |
| GET /search/social/posts | Search social posts (params: q, limit) |

## Prediction Market (17 endpoints)

| Endpoint | Description |
|----------|-------------|
| ~~GET /prediction-market/category-metrics~~ | ~~Category aggregate stats~~ — **removed (410 Gone)** |
| ~~GET /prediction-market/polymarket/ranking~~ | ~~Top Polymarket markets by volume~~ — **removed (410 Gone)** |
| GET /prediction-market/polymarket/trades | Recent trades (params: ticker, limit) |
| GET /prediction-market/polymarket/markets | Browse markets (params: market_slug, limit, category) |
| GET /prediction-market/polymarket/events | Grouped markets by event (params: event_slug, limit) |
| GET /prediction-market/polymarket/prices | Price history (params: condition_id) |
| GET /prediction-market/polymarket/volumes | Volume history (params: condition_id) |
| GET /prediction-market/polymarket/open-interest | Outstanding positions (params: condition_id) |
| GET /prediction-market/polymarket/positions | User positions (params: address) |
| GET /prediction-market/polymarket/activity | Recent activity (params: address, limit) |
| GET /prediction-market/kalshi/ranking | Top Kalshi markets |
| GET /prediction-market/kalshi/markets | Browse Kalshi markets (params: market_ticker, limit, category) |
| GET /prediction-market/kalshi/events | Kalshi events (params: limit) |
| GET /prediction-market/kalshi/prices | Price history (params: ticker) |
| GET /prediction-market/kalshi/trades | Recent trades (params: ticker, limit) |
| GET /prediction-market/kalshi/volumes | Volume history (params: ticker) |
| GET /prediction-market/kalshi/open-interest | Outstanding contracts (params: ticker) |

## Web (1 endpoint)

| Endpoint | Description |
|----------|-------------|
| GET /web/fetch | Fetch + clean web page (params: url) |

## Code Examples

::: code-group

```bash [cURL]
# x402 payment is handled automatically by the SDK
# These examples show the raw HTTP calls — in practice use the SDK

# Get BTC-USDT price
curl "https://api.jarvisclaw.ai/v1/marketplace/surf/exchange/price?pair=BTC-USDT"

# Get market rankings
curl "https://api.jarvisclaw.ai/v1/marketplace/surf/market/ranking?limit=10"

# Get Fear & Greed index
curl "https://api.jarvisclaw.ai/v1/marketplace/surf/market/fear-greed"

# On-chain SQL query
curl -X POST "https://api.jarvisclaw.ai/v1/marketplace/surf/onchain/sql" \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT from_address, SUM(value/1e18) as total_eth FROM ethereum.transactions WHERE block_time > now() - interval 1 hour GROUP BY from_address ORDER BY total_eth DESC LIMIT 10"}'

# Search Polymarket
curl "https://api.jarvisclaw.ai/v1/marketplace/surf/search/polymarket?q=bitcoin&limit=5"
```

```python [Python (x402 Agent)]
from jarvisclaw import MarketplaceClient

# ─── Option A: Base chain (EVM) ───
# Hex private key → USDC on Base (Chain ID 8453)
client = MarketplaceClient(private_key="0x<evm-private-key>")

# ─── Option B: Solana ───
# Base58 keypair → USDC SPL on Solana mainnet
client = MarketplaceClient(private_key="<solana-bs58-keypair>")

# SDK auto-detects chain from key format — no config needed
# All calls below work identically on either chain:

# Get BTC-USDT price
price = client.call("surf", "/exchange/price", params={"pair": "BTC-USDT"})
print(f"BTC: ${price['price']:,.2f} ({price['change_24h']:+.2f}%)")

# Get market rankings
rankings = client.call("surf", "/market/ranking", params={"limit": 10})
for coin in rankings["rankings"]:
    print(f"#{coin['rank']} {coin['symbol']}: ${coin['price']:,.2f}")

# Fear & Greed index
fg = client.call("surf", "/market/fear-greed")
print(f"Fear & Greed: {fg['value']} ({fg['label']})")

# On-chain SQL query (POST)
result = client.call("surf", "/onchain/sql", method="POST",
    json={"sql": "SELECT from_address, SUM(value/1e18) as total_eth FROM ethereum.transactions WHERE block_time > now() - interval '1 hour' GROUP BY from_address ORDER BY total_eth DESC LIMIT 10"})
for row in result["rows"]:
    print(f"  {row[0]}: {row[1]:.4f} ETH")

# Search prediction markets
markets = client.call("surf", "/search/polymarket", params={"q": "bitcoin", "limit": 5})
for m in markets["results"]:
    print(f"  {m['title']} — vol: ${m['volume']:,.0f}")

# Wallet intelligence
wallet = client.call("surf", "/wallet/detail", params={"address": "0xBE0eB53F46cd790Cd..."})
print(f"Labels: {wallet['labels']}, Net worth: ${wallet['net_worth_usd']:,.0f}")
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
    // For Solana, pass a base58 keypair instead of hex EVM key
    mc, _ := jc.NewMarketplaceClient(jc.WithPrivateKey("0x<evm-private-key>"))

    // Get BTC-USDT price
    price, _ := mc.Call(ctx, "surf", "/exchange/price",
        jc.WithParams(map[string]string{"pair": "BTC-USDT"}))
    fmt.Printf("BTC price: %v\n", price["price"])

    // Get market rankings
    rankings, _ := mc.Call(ctx, "surf", "/market/ranking",
        jc.WithParams(map[string]string{"limit": "10"}))
    fmt.Printf("Top coins: %v\n", rankings["rankings"])

    // Fear & Greed index
    fg, _ := mc.Call(ctx, "surf", "/market/fear-greed", nil)
    fmt.Printf("Fear & Greed: %v (%v)\n", fg["value"], fg["label"])

    // On-chain SQL query
    result, _ := mc.Call(ctx, "surf", "/onchain/sql",
        jc.WithMethod("POST"),
        jc.WithJSON(map[string]any{
            "sql": "SELECT from_address, SUM(value/1e18) as total_eth FROM ethereum.transactions WHERE block_time > now() - interval '1 hour' GROUP BY from_address ORDER BY total_eth DESC LIMIT 10",
        }),
    )
    fmt.Printf("Rows: %v\n", result["rows"])

    // Search prediction markets
    markets, _ := mc.Call(ctx, "surf", "/search/polymarket",
        jc.WithParams(map[string]string{"q": "bitcoin", "limit": "5"}))
    fmt.Printf("Markets: %v\n", markets["results"])

    // Wallet intelligence
    wallet, _ := mc.Call(ctx, "surf", "/wallet/detail",
        jc.WithParams(map[string]string{"address": "0xBE0eB53F46cd790Cd..."}))
    fmt.Printf("Labels: %v, Net worth: %v\n", wallet["labels"], wallet["net_worth_usd"])
}
```

:::

## Errors

| Code | Name | Description | Resolution |
|------|------|-------------|------------|
| 400 | invalid_pair | Trading pair format is invalid | Use format: BASE-QUOTE (e.g. BTC-USDT) |
| 400 | invalid_params | Required parameter missing or malformed | Check endpoint documentation for required parameters |
| 400 | sql_syntax_error | On-chain SQL query has syntax errors | Validate SQL syntax; use standard SELECT statements only |
| 402 | payment_required | x402 payment not provided or insufficient balance | Ensure wallet has sufficient USDC balance on Base or Solana |
| 404 | not_found | Resource not found (invalid slug, address, or ID) | Verify the identifier exists |
| 408 | query_timeout | SQL query took too long to execute (>30s) | Add LIMIT clause or simplify the query |
| 429 | rate_limited | Too many requests | Back off and retry with exponential delay |

## Limitations

- Premium SQL queries have a 30-second execution timeout — add LIMIT clauses to complex queries
- Social/CT data covers Twitter/X only — no Reddit, Discord, or Telegram
- Wallet intelligence covers 13 networks — other chains may have incomplete labels
- No WebSocket streaming — all endpoints are request/response (polling)
- On-chain SQL tables updated with ~5 minute delay from chain tip
- Batch label lookup limited to 100 addresses per request
- Prediction market data covers Polymarket and Kalshi only
