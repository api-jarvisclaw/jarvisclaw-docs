# Crypto Data (Surf)

Access real-time and historical cryptocurrency data across 83 endpoints spanning 12 domains. Powered by Surf's comprehensive blockchain data infrastructure.

## Base URL

```
/v1/marketplace/surf/*
```

## Pricing

| Tier | Price | Description |
|------|-------|-------------|
| Standard | $0.0075/call | Most endpoints (REST queries) |
| Premium SQL | $0.02/call | Custom SQL queries on indexed data |

## Domains

| Domain | Description | Example Endpoints |
|--------|-------------|-------------------|
| Exchange | CEX order books, trades, tickers | `/exchange/orderbook`, `/exchange/trades` |
| Market | Prices, OHLCV, market cap | `/market/price`, `/market/ohlcv` |
| Onchain | Gas, transactions, blocks | `/onchain/gas`, `/onchain/transactions` |
| Social | Social metrics, sentiment | `/social/metrics`, `/social/trending` |
| Wallet | Portfolio, balances, history | `/wallet/portfolio`, `/wallet/balances` |
| Token | Token info, holders, supply | `/token/info`, `/token/holders` |
| Perpetuals | Funding rates, open interest | `/perpetuals/funding`, `/perpetuals/oi` |
| DeFi | TVL, yields, protocols | `/defi/tvl`, `/defi/yields` |
| NFT | Collections, sales, floors | `/nft/collections`, `/nft/sales` |
| Derivatives | Options, futures | `/derivatives/options`, `/derivatives/futures` |
| Governance | Proposals, votes | `/governance/proposals` |
| Lending | Rates, utilization | `/lending/rates` |

## Key Endpoints

### Market Price

`GET /v1/marketplace/surf/market/price`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `token` | string | Yes | Token symbol (e.g., `BTC`, `ETH`, `SOL`) |
| `currency` | string | No | Quote currency. Default: `USD` |

### Perpetuals Funding Rates

`GET /v1/marketplace/surf/perpetuals/funding`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | string | Yes | Perpetual symbol (e.g., `BTC-PERP`) |
| `exchange` | string | No | Exchange filter (e.g., `binance`, `bybit`) |

### Exchange Order Book

`GET /v1/marketplace/surf/exchange/orderbook`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | string | Yes | Trading pair (e.g., `BTC/USDT`) |
| `exchange` | string | Yes | Exchange identifier |
| `depth` | integer | No | Order book depth. Default: `20` |

### Onchain Gas Prices

`GET /v1/marketplace/surf/onchain/gas`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | string | Yes | Blockchain (e.g., `ethereum`, `base`, `solana`) |

### Wallet Portfolio

`GET /v1/marketplace/surf/wallet/portfolio`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | string | Yes | Wallet address |
| `chain` | string | Yes | Blockchain network |

### OHLCV (Candlesticks)

`GET /v1/marketplace/surf/market/ohlcv`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | string | Yes | Trading pair (e.g., `BTC/USD`) |
| `interval` | string | Yes | Candle interval (`1m`, `5m`, `1h`, `4h`, `1d`) |
| `limit` | integer | No | Number of candles. Default: `100` |

## Response Example (Market Price)

```json
{
  "token": "BTC",
  "price": 67432.15,
  "currency": "USD",
  "change_24h": 2.34,
  "volume_24h": 28500000000,
  "market_cap": 1325000000000,
  "timestamp": "2025-06-01T12:00:00Z"
}
```

## Examples

::: code-group

```python [Python]
import requests

BASE = "https://api.jarvisclaw.ai/v1/marketplace/surf"
HEADERS = {
    "Authorization": "Bearer sk-your-api-key",
}

# Get BTC price
resp = requests.get(f"{BASE}/market/price", headers=HEADERS, params={
    "token": "BTC",
})
print(resp.json())

# Get ETH gas prices
resp = requests.get(f"{BASE}/onchain/gas", headers=HEADERS, params={
    "chain": "ethereum",
})
print(resp.json())

# Get wallet portfolio
resp = requests.get(f"{BASE}/wallet/portfolio", headers=HEADERS, params={
    "address": "0x1234...abcd",
    "chain": "ethereum",
})
print(resp.json())
```

```bash [cURL]
# Get BTC price
curl "https://api.jarvisclaw.ai/v1/marketplace/surf/market/price?token=BTC" \
  -H "Authorization: Bearer sk-your-api-key"

# Get funding rates
curl "https://api.jarvisclaw.ai/v1/marketplace/surf/perpetuals/funding?symbol=BTC-PERP" \
  -H "Authorization: Bearer sk-your-api-key"

# Get order book
curl "https://api.jarvisclaw.ai/v1/marketplace/surf/exchange/orderbook?symbol=BTC/USDT&exchange=binance" \
  -H "Authorization: Bearer sk-your-api-key"
```

:::

## Notes

- 83 endpoints available across 12 data domains
- All data is real-time or near-real-time (< 5s delay)
- Rate limit: 100 requests/minute per API key
- Premium SQL endpoint accepts arbitrary SQL queries against indexed blockchain data
- Historical data available for most endpoints via `start_time` and `end_time` parameters
