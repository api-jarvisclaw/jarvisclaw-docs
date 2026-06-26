# Trading Markets API

Real-time price data for traditional markets. 1,746+ equities across 12 global exchanges with ~400ms oracle cadence. Plus 500+ crypto pairs, 30+ forex pairs, and commodities. Stocks $0.001/call; crypto/FX/commodities free.

## Authentication

Both methods are supported — all requests settle via x402 on-chain:

| Method | Header | Description |
|--------|--------|-------------|
| API Key | `Authorization: Bearer sk-...` | Platform signs x402 from your HD wallet automatically |
| Private Key (x402) | Automatic via SDK | Agent signs x402 directly from its own wallet |

See [Agent Payments (x402)](/x402) for full details on how both methods work.

## Base URL

```
https://api.jarvisclaw.ai/v1/marketplace/markets
```

## Pricing

| Asset Class | Price per Request |
|-------------|-------------------|
| Stocks | $0.001 |
| Crypto | Free |
| Forex | Free |
| Commodities | Free |

## Coverage

| Asset Class | Coverage | Update Cadence |
|-------------|----------|----------------|
| Equities | 1,746+ symbols across 12 exchanges | ~400ms |
| Crypto | 500+ trading pairs | Real-time |
| Forex | 30+ currency pairs | Real-time |
| Commodities | Gold, silver, oil, natural gas, and more | Real-time |

## Endpoints

| Method | Endpoint | Description | Price |
|--------|----------|-------------|-------|
| GET | `/stocks/:market/price/:symbol` | Stock price snapshot | $0.001 |
| GET | `/crypto/price/:pair` | Crypto price | Free |
| GET | `/fx/price/:pair` | Forex rate | Free |
| GET | `/commodity/price/:symbol` | Commodity price | Free |

---

## Stock Price

`GET /v1/marketplace/markets/stocks/:market/price/:symbol`

Get a real-time price snapshot for a stock on a specific exchange.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `market` | string | Yes | Region code (e.g., `us`, `gb`, `hk`, `jp`) |
| `symbol` | string | Yes | Ticker symbol (e.g., `AAPL`, `TSLA`, `NVDA`) |

### Response

```json
{
  "symbol": "AAPL",
  "category": "stocks/us",
  "price": 298.17143,
  "confidence": 0.14916,
  "publishTime": 1781812821,
  "timestamp": "2026-06-18T20:00:21.000Z",
  "assetType": "equity",
  "feedId": "0x49f6b65cb1de6b10eaf75e7c03ca029c306d0357e91b5311b175084a5ad55688",
  "source": "pyth"
}
```

---

## Crypto Price

`GET /v1/marketplace/markets/crypto/price/:pair`

Get real-time price for a cryptocurrency trading pair.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pair` | string | Yes | Trading pair with dash separator (e.g., `BTC-USD`, `ETH-USD`, `SOL-USD`) |

### Response

```json
{
  "symbol": "BTC-USD",
  "category": "crypto",
  "price": 63680.33,
  "confidence": 38.42,
  "publishTime": 1781957129,
  "timestamp": "2026-06-20T12:05:29.000Z",
  "assetType": "crypto",
  "feedId": "0xe62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43",
  "source": "pyth"
}
```

---

## Forex Rate

`GET /v1/marketplace/markets/fx/price/:pair`

Get real-time foreign exchange rate.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pair` | string | Yes | Currency pair with dash separator (e.g., `EUR-USD`, `GBP-USD`, `USD-JPY`) |

### Response

```json
{
  "pair": "EUR-USD",
  "rate": 1.0847,
  "bid": 1.0846,
  "ask": 1.0848,
  "change_24h": -0.12,
  "timestamp": "2025-06-01T15:30:00Z"
}
```

---

## Commodity Price

`GET /v1/marketplace/markets/commodity/price/:symbol`

Get real-time commodity price.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | string | Yes | Commodity symbol in Pyth feed format (e.g., `XAU-USD`, `XAG-USD`, `WTI-USD`, `NATGAS-USD`) |

### Response

```json
{
  "symbol": "XAU-USD",
  "price": 2345.60,
  "unit": "USD/oz",
  "change_24h": 0.85,
  "timestamp": "2025-06-01T15:30:00Z"
}
```

---

## Examples

::: code-group

```bash [cURL]
# Stock price (NVDA on US market) — $0.001
curl "https://api.jarvisclaw.ai/v1/marketplace/markets/stocks/us/price/NVDA" \
  -H "Authorization: Bearer sk-your-api-key"

# Crypto price (free)
curl "https://api.jarvisclaw.ai/v1/marketplace/markets/crypto/price/ETH-USD" \
  -H "Authorization: Bearer sk-your-api-key"

# Forex rate (free)
curl "https://api.jarvisclaw.ai/v1/marketplace/markets/fx/price/USD-JPY" \
  -H "Authorization: Bearer sk-your-api-key"

# Commodity price (free)
curl "https://api.jarvisclaw.ai/v1/marketplace/markets/commodity/price/WTI-USD" \
  -H "Authorization: Bearer sk-your-api-key"
```

```python [Python (API Key)]
import requests

BASE = "https://api.jarvisclaw.ai/v1/marketplace/markets"
HEADERS = {"Authorization": "Bearer sk-your-api-key"}

# Stock price — $0.001 per call
resp = requests.get(f"{BASE}/stocks/us/price/AAPL", headers=HEADERS)
aapl = resp.json()
print(f"AAPL: ${aapl['price']} (source: {aapl['source']})")

# Crypto price (free)
resp = requests.get(f"{BASE}/crypto/price/BTC-USD", headers=HEADERS)
btc = resp.json()
print(f"BTC: ${btc['price']:,.2f} (source: {btc['source']})")

# Forex rate (free)
resp = requests.get(f"{BASE}/fx/price/EUR-USD", headers=HEADERS)
fx = resp.json()
print(f"EUR/USD: {fx['rate']} (bid: {fx['bid']}, ask: {fx['ask']})")

# Commodity price (free)
resp = requests.get(f"{BASE}/commodity/price/XAU-USD", headers=HEADERS)
gold = resp.json()
print(f"Gold: ${gold['price']}/{gold['unit'].split('/')[1]}")

# Multi-stock portfolio check
portfolio = ["AAPL", "NVDA", "TSLA", "MSFT", "GOOGL"]
for symbol in portfolio:
    resp = requests.get(f"{BASE}/stocks/us/price/{symbol}", headers=HEADERS)
    data = resp.json()
    print(f"  {data['symbol']}: ${data['price']} (confidence: {data['confidence']})")
```

```python [Python (x402 Agent)]
from jarvisclaw import MarketplaceClient

# x402 agent — pays $0.001 per stock call with USDC automatically
client = MarketplaceClient(private_key="0x<agent-wallet-private-key>")

# Stock price (auto-pays $0.001 via x402)
aapl = client.call("markets", "/stocks/us/price/AAPL")
print(f"AAPL: ${aapl['price']}")

# Crypto (free — no x402 payment triggered)
btc = client.call("markets", "/crypto/price/BTC-USD")
print(f"BTC: ${btc['price']:,.2f}")

# Forex (free)
eur = client.call("markets", "/fx/price/EUR-USD")
print(f"EUR/USD: {eur['rate']}")

# Commodity (free)
gold = client.call("markets", "/commodity/price/XAU-USD")
print(f"Gold: ${gold['price']}/oz")

# Agent portfolio monitoring loop
import time
while True:
    nvda = client.call("markets", "/stocks/us/price/NVDA")
    if nvda["price"] > 150:
        print(f"NVDA alert: ${nvda['price']}")
        break
    time.sleep(60)
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

    // Stock price
    stock, _ := mc.Call(ctx, "markets", "/stocks/us/price/NVDA")
    fmt.Printf("NVDA: $%.2f (confidence: %.5f)\n", stock["price"].(float64), stock["confidence"].(float64))

    // Crypto price (free)
    crypto, _ := mc.Call(ctx, "markets", "/crypto/price/BTC-USD")
    fmt.Printf("BTC-USD: $%.2f (source: %s)\n", crypto["price"].(float64), crypto["source"].(string))

    // Forex rate (free)
    fx, _ := mc.Call(ctx, "markets", "/fx/price/EUR-USD")
    fmt.Printf("EUR-USD: %.4f\n", fx["rate"].(float64))

    // Commodity price (free)
    commodity, _ := mc.Call(ctx, "markets", "/commodity/price/XAU-USD")
    fmt.Printf("Gold: $%.2f %s\n", commodity["price"].(float64), commodity["unit"].(string))
}
```

```go [Go (x402 Agent)]
package main

import (
    "context"
    "fmt"
    "time"

    jc "github.com/api-jarvisclaw/go-sdk"
)

func main() {
    ctx := context.Background()

    // x402 agent — auto-pays $0.001 per stock call with USDC
    mc, err := jc.NewMarketplaceClient(
        jc.WithPrivateKey("0x<agent-wallet-private-key>"),
    )
    if err != nil {
        panic(err)
    }

    // Stock price (x402 pays automatically)
    stock, _ := mc.Call(ctx, "markets", "/stocks/us/price/AAPL")
    fmt.Printf("AAPL: $%.2f\n", stock["price"].(float64))

    // Crypto (free — no payment needed)
    btc, _ := mc.Call(ctx, "markets", "/crypto/price/BTC-USD")
    fmt.Printf("BTC: $%.2f\n", btc["price"].(float64))

    // Agent price monitoring
    for {
        nvda, _ := mc.Call(ctx, "markets", "/stocks/us/price/NVDA")
        if nvda["price"].(float64) > 150 {
            fmt.Printf("NVDA alert: $%.2f\n", nvda["price"].(float64))
            break
        }
        time.Sleep(60 * time.Second)
    }
}
```

:::

---

## Supported Markets

| Code | Region | Notable Symbols |
|------|--------|-----------------|
| `us` | United States | AAPL, NVDA, TSLA, MSFT, GOOGL, AMZN |
| `gb` | United Kingdom | SHEL, AZN, HSBA, ULVR |
| `de` | Germany | SAP, SIE, ALV, BAS |
| `fr` | France | MC, OR, SAN, AIR |
| `nl` | Netherlands | ASML, INGA, PHIA |
| `ie` | Ireland | CRH, KYGA, SKG |
| `lu` | Luxembourg | ARCE, SES, RTL |
| `hk` | Hong Kong | 0700, 9988, 0005, 1299 |
| `jp` | Japan | 7203, 6758, 9984, 6861 |
| `kr` | South Korea | 005930, 000660, 035420 |
| `cn` | China | 600519, 601318, 000858 |
| `ca` | Canada | RY, TD, SHOP, ENB |

---

## Errors

| Code | Error | Description |
|------|-------|-------------|
| 404 | `symbol_not_found` | Ticker symbol doesn't exist on the specified exchange |
| 404 | `market_not_supported` | Exchange code not in the 12 supported markets |
| 503 | `market_closed` | Exchange is currently closed; last available price returned with this warning |
| 400 | `invalid_pair` | Trading pair format is invalid (use dash separator: `BTC-USD`) |
| 429 | `rate_limited` | Too many requests — back off and retry |

---

## Limitations

- **Trading hours only** — Stock prices are live during market hours; returns last closing price with `503` status when market is closed
- **No historical OHLC** — Only current price snapshots; no candle data or historical time series
- **12 exchanges only** — Limited to the listed exchanges; other markets are not covered
- **~400ms is not HFT** — Oracle cadence is suitable for monitoring and display, not high-frequency trading strategies
- **Read-only** — Price data only; no order placement, execution, or portfolio management
- **USD denomination** — All prices are returned in USD unless the pair/exchange implies otherwise
- **Dash separator required** — Pairs use dash format (`BTC-USD`, `EUR-USD`), not slash (`BTC/USD`)
- **No pre/post-market** — Only regular trading session data for equities
