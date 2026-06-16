# Trading Markets API

Real-time price data for traditional markets. 1,746+ equities across 12 global exchanges with ~400ms oracle cadence. Plus 500+ crypto pairs, 30+ forex pairs, and commodities. Stocks $0.001/call; crypto/FX/commodities free.

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
| `market` | string | Yes | Exchange code (e.g., `nasdaq`, `nyse`, `lse`, `hkex`) |
| `symbol` | string | Yes | Ticker symbol (e.g., `AAPL`, `TSLA`, `NVDA`) |

### Response

```json
{
  "symbol": "AAPL",
  "market": "nasdaq",
  "price": 189.45,
  "change": 2.15,
  "change_percent": 1.15,
  "volume": 52340000,
  "timestamp": "2025-06-01T15:30:00Z"
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
  "pair": "BTC-USD",
  "price": 67432.15,
  "bid": 67430.00,
  "ask": 67434.30,
  "change_24h": 2.34,
  "volume_24h": 28500000000,
  "timestamp": "2025-06-01T15:30:00Z"
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
| `symbol` | string | Yes | Commodity symbol (e.g., `GOLD`, `SILVER`, `WTI`, `NATGAS`) |

### Response

```json
{
  "symbol": "GOLD",
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
# Stock price (NVDA on NASDAQ) — $0.001
curl "https://api.jarvisclaw.ai/v1/marketplace/markets/stocks/nasdaq/price/NVDA" \
  -H "Authorization: Bearer sk-your-api-key"

# Crypto price (free)
curl "https://api.jarvisclaw.ai/v1/marketplace/markets/crypto/price/ETH-USD" \
  -H "Authorization: Bearer sk-your-api-key"

# Forex rate (free)
curl "https://api.jarvisclaw.ai/v1/marketplace/markets/fx/price/USD-JPY" \
  -H "Authorization: Bearer sk-your-api-key"

# Commodity price (free)
curl "https://api.jarvisclaw.ai/v1/marketplace/markets/commodity/price/WTI" \
  -H "Authorization: Bearer sk-your-api-key"
```

```python [Python (API Key)]
import requests

BASE = "https://api.jarvisclaw.ai/v1/marketplace/markets"
HEADERS = {"Authorization": "Bearer sk-your-api-key"}

# Stock price — $0.001 per call
resp = requests.get(f"{BASE}/stocks/nasdaq/price/AAPL", headers=HEADERS)
aapl = resp.json()
print(f"AAPL: ${aapl['price']} ({aapl['change_percent']:+.2f}%)")

# Crypto price (free)
resp = requests.get(f"{BASE}/crypto/price/BTC-USD", headers=HEADERS)
btc = resp.json()
print(f"BTC: ${btc['price']:,.2f} (24h: {btc['change_24h']:+.2f}%)")

# Forex rate (free)
resp = requests.get(f"{BASE}/fx/price/EUR-USD", headers=HEADERS)
fx = resp.json()
print(f"EUR/USD: {fx['rate']} (bid: {fx['bid']}, ask: {fx['ask']})")

# Commodity price (free)
resp = requests.get(f"{BASE}/commodity/price/GOLD", headers=HEADERS)
gold = resp.json()
print(f"Gold: ${gold['price']}/{gold['unit'].split('/')[1]}")

# Multi-stock portfolio check
portfolio = ["AAPL", "NVDA", "TSLA", "MSFT", "GOOGL"]
for symbol in portfolio:
    resp = requests.get(f"{BASE}/stocks/nasdaq/price/{symbol}", headers=HEADERS)
    data = resp.json()
    print(f"  {data['symbol']}: ${data['price']} ({data['change_percent']:+.2f}%)")
```

```python [Python (x402 Agent)]
from jarvisclaw import Client

# x402 agent — pays $0.001 per stock call with USDC automatically
client = Client(private_key="0x<agent-wallet-private-key>")

# Stock price (auto-pays $0.001 via x402)
aapl = client.get("/v1/marketplace/markets/stocks/nasdaq/price/AAPL")
print(f"AAPL: ${aapl['price']}")

# Crypto (free — no x402 payment triggered)
btc = client.get("/v1/marketplace/markets/crypto/price/BTC-USD")
print(f"BTC: ${btc['price']:,.2f}")

# Forex (free)
eur = client.get("/v1/marketplace/markets/fx/price/EUR-USD")
print(f"EUR/USD: {eur['rate']}")

# Commodity (free)
gold = client.get("/v1/marketplace/markets/commodity/price/GOLD")
print(f"Gold: ${gold['price']}/oz")

# Agent portfolio monitoring loop
import time
while True:
    nvda = client.get("/v1/marketplace/markets/stocks/nasdaq/price/NVDA")
    if nvda["price"] > 150:
        print(f"NVDA alert: ${nvda['price']}")
        break
    time.sleep(60)
```

```go [Go (API Key)]
package main

import (
    "fmt"

    jarvisclaw "github.com/api-jarvisclaw/go-sdk"
)

func main() {
    client := jarvisclaw.NewClient(jarvisclaw.WithAPIKey("sk-your-api-key"))

    // Stock price
    var stock struct {
        Symbol        string  `json:"symbol"`
        Price         float64 `json:"price"`
        Change        float64 `json:"change"`
        ChangePercent float64 `json:"change_percent"`
        Volume        int64   `json:"volume"`
    }
    err := client.GetJSON("/v1/marketplace/markets/stocks/nasdaq/price/NVDA", nil, &stock)
    if err != nil {
        panic(err)
    }
    fmt.Printf("%s: $%.2f (%+.2f%%)
", stock.Symbol, stock.Price, stock.ChangePercent)

    // Crypto price (free)
    var crypto struct {
        Pair      string  `json:"pair"`
        Price     float64 `json:"price"`
        Change24h float64 `json:"change_24h"`
    }
    _ = client.GetJSON("/v1/marketplace/markets/crypto/price/BTC-USD", nil, &crypto)
    fmt.Printf("%s: $%.2f (24h: %+.2f%%)
", crypto.Pair, crypto.Price, crypto.Change24h)

    // Forex rate (free)
    var fx struct {
        Pair string  `json:"pair"`
        Rate float64 `json:"rate"`
    }
    _ = client.GetJSON("/v1/marketplace/markets/fx/price/EUR-USD", nil, &fx)
    fmt.Printf("%s: %.4f
", fx.Pair, fx.Rate)

    // Commodity price (free)
    var commodity struct {
        Symbol string  `json:"symbol"`
        Price  float64 `json:"price"`
        Unit   string  `json:"unit"`
    }
    _ = client.GetJSON("/v1/marketplace/markets/commodity/price/GOLD", nil, &commodity)
    fmt.Printf("%s: $%.2f %s
", commodity.Symbol, commodity.Price, commodity.Unit)
}
```

```go [Go (x402 Agent)]
package main

import (
    "fmt"
    "time"

    jarvisclaw "github.com/api-jarvisclaw/go-sdk"
)

func main() {
    // x402 agent — auto-pays $0.001 per stock call with USDC
    client, err := jarvisclaw.NewClient(
        jarvisclaw.WithPrivateKey("0x<agent-wallet-private-key>"),
    )
    if err != nil {
        panic(err)
    }

    // Stock price (x402 pays automatically)
    var stock struct {
        Symbol string  `json:"symbol"`
        Price  float64 `json:"price"`
    }
    _ = client.GetJSON("/v1/marketplace/markets/stocks/nasdaq/price/AAPL", nil, &stock)
    fmt.Printf("AAPL: $%.2f
", stock.Price)

    // Crypto (free — no payment needed)
    var btc struct {
        Price float64 `json:"price"`
    }
    _ = client.GetJSON("/v1/marketplace/markets/crypto/price/BTC-USD", nil, &btc)
    fmt.Printf("BTC: $%.2f
", btc.Price)

    // Agent price monitoring
    for {
        var nvda struct {
            Price float64 `json:"price"`
        }
        _ = client.GetJSON("/v1/marketplace/markets/stocks/nasdaq/price/NVDA", nil, &nvda)
        if nvda.Price > 150 {
            fmt.Printf("NVDA alert: $%.2f
", nvda.Price)
            break
        }
        time.Sleep(60 * time.Second)
    }
}
```

:::

---

## Supported Exchanges

| Code | Exchange | Region |
|------|----------|--------|
| `nasdaq` | NASDAQ | US |
| `nyse` | New York Stock Exchange | US |
| `lse` | London Stock Exchange | UK |
| `hkex` | Hong Kong Exchange | HK |
| `tse` | Tokyo Stock Exchange | JP |
| `sse` | Shanghai Stock Exchange | CN |
| `szse` | Shenzhen Stock Exchange | CN |
| `asx` | Australian Securities Exchange | AU |
| `tsx` | Toronto Stock Exchange | CA |
| `bse` | Bombay Stock Exchange | IN |
| `nse` | National Stock Exchange of India | IN |
| `fra` | Frankfurt Stock Exchange | DE |

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
