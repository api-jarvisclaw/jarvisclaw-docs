# Trading Markets

Real-time market data for stocks, crypto, forex, and commodities. Read-only price snapshots with ~400ms oracle cadence.

## Base URL

```
/v1/marketplace/markets/*
```

## Endpoints

| Method | Endpoint | Description | Price |
|--------|----------|-------------|-------|
| GET | `/v1/marketplace/markets/stocks/:market/price/:symbol` | Stock price | $0.001 |
| GET | `/v1/marketplace/markets/crypto/price/:pair` | Crypto price | Free |
| GET | `/v1/marketplace/markets/fx/price/:pair` | Forex rate | Free |
| GET | `/v1/marketplace/markets/commodity/price/:symbol` | Commodity price | Free |

## Coverage

| Asset Class | Coverage |
|-------------|----------|
| Equities | 1,746+ symbols across 12 exchanges |
| Crypto | 500+ trading pairs |
| Forex | 30+ currency pairs |
| Commodities | Gold, silver, oil, natural gas, and more |

## Stock Price

`GET /v1/marketplace/markets/stocks/:market/price/:symbol`

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

## Crypto Price

`GET /v1/marketplace/markets/crypto/price/:pair`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pair` | string | Yes | Trading pair (e.g., `BTC-USD`, `ETH-USD`, `SOL-USD`) |

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

## Forex Rate

`GET /v1/marketplace/markets/fx/price/:pair`

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pair` | string | Yes | Currency pair (e.g., `EUR-USD`, `GBP-USD`, `USD-JPY`) |

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

## Commodity Price

`GET /v1/marketplace/markets/commodity/price/:symbol`

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

## Examples

::: code-group

```python [Python]
import requests

BASE = "https://api.jarvisclaw.ai/v1/marketplace/markets"
HEADERS = {
    "Authorization": "Bearer sk-your-api-key",
}

# Get AAPL stock price
resp = requests.get(f"{BASE}/stocks/nasdaq/price/AAPL", headers=HEADERS)
print(f"AAPL: ${resp.json()['price']}")

# Get BTC price (free)
resp = requests.get(f"{BASE}/crypto/price/BTC-USD", headers=HEADERS)
btc = resp.json()
print(f"BTC: ${btc['price']} ({btc['change_24h']}%)")

# Get EUR/USD forex rate (free)
resp = requests.get(f"{BASE}/fx/price/EUR-USD", headers=HEADERS)
print(f"EUR/USD: {resp.json()['rate']}")

# Get gold price (free)
resp = requests.get(f"{BASE}/commodity/price/GOLD", headers=HEADERS)
print(f"Gold: ${resp.json()['price']}/oz")
```

```bash [cURL]
# Stock price
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

:::

## Supported Exchanges

| Code | Exchange |
|------|----------|
| `nasdaq` | NASDAQ |
| `nyse` | New York Stock Exchange |
| `lse` | London Stock Exchange |
| `hkex` | Hong Kong Exchange |
| `tse` | Tokyo Stock Exchange |
| `sse` | Shanghai Stock Exchange |
| `szse` | Shenzhen Stock Exchange |
| `asx` | Australian Securities Exchange |
| `tsx` | Toronto Stock Exchange |
| `bse` | Bombay Stock Exchange |
| `nse` | National Stock Exchange of India |
| `fra` | Frankfurt Stock Exchange |

## Notes

- All data is read-only price snapshots — no order placement
- Oracle cadence: ~400ms refresh rate
- Stock prices are delayed 15 minutes for non-premium feeds
- Crypto, forex, and commodity prices are real-time
- Trading pair format uses dash separator (e.g., `BTC-USD`, not `BTC/USD`)
- All prices are in USD unless otherwise specified
