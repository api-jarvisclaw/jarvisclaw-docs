# DEX Trading (0x Swap)

Execute token swaps across decentralized exchanges with best-price routing. Powered by 0x aggregation protocol.

## Base URL

```
/v1/marketplace/dex/*
```

## Pricing

**FREE** — No JarvisClaw fees. You only pay on-chain gas costs for submitted transactions.

## Supported Chains

| Chain | Chain ID |
|-------|----------|
| Ethereum | 1 |
| Base | 8453 |
| Polygon | 137 |
| Arbitrum | 42161 |
| Optimism | 10 |

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/marketplace/dex/price` | Indicative swap price (no commitment) |
| GET | `/v1/marketplace/dex/quote` | Firm quote with EIP-712 signature data |
| POST | `/v1/marketplace/dex/gasless/submit` | Submit a gasless swap |
| GET | `/v1/marketplace/dex/gasless/status/:tradeHash` | Track gasless swap status |

## Get Price

`GET /v1/marketplace/dex/price`

Get an indicative price for a token swap without committing to a trade.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainId` | integer | Yes | Target chain ID |
| `sellToken` | string | Yes | Token address to sell |
| `buyToken` | string | Yes | Token address to buy |
| `sellAmount` | string | Yes | Amount to sell (in base units) |
| `taker` | string | No | Taker wallet address |

### Response

```json
{
  "buyAmount": "1000000000000000000",
  "sellAmount": "3200000000",
  "price": "0.0032",
  "sources": [
    {"name": "Uniswap_V3", "proportion": "0.8"},
    {"name": "SushiSwap", "proportion": "0.2"}
  ],
  "estimatedGas": "150000"
}
```

## Get Quote

`GET /v1/marketplace/dex/quote`

Get a firm quote with transaction data ready for signing. Includes EIP-712 typed data for gasless swaps.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainId` | integer | Yes | Target chain ID |
| `sellToken` | string | Yes | Token address to sell |
| `buyToken` | string | Yes | Token address to buy |
| `sellAmount` | string | Yes | Amount to sell (in base units) |
| `taker` | string | Yes | Taker wallet address |

### Response

```json
{
  "buyAmount": "1000000000000000000",
  "sellAmount": "3200000000",
  "to": "0x...exchange_proxy",
  "data": "0x...",
  "value": "0",
  "gas": "150000",
  "gasPrice": "20000000000",
  "permit2": {
    "eip712": { ... }
  }
}
```

## Submit Gasless Swap

`POST /v1/marketplace/dex/gasless/submit`

Submit a signed gasless swap. The relayer pays gas on your behalf.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainId` | integer | Yes | Target chain ID |
| `trade` | object | Yes | Quote object from `/quote` |
| `signature` | string | Yes | EIP-712 signature from taker |

### Response

```json
{
  "tradeHash": "0xabc123...",
  "status": "submitted"
}
```

## Track Gasless Swap

`GET /v1/marketplace/dex/gasless/status/:tradeHash`

Poll the status of a submitted gasless swap.

### Response

```json
{
  "tradeHash": "0xabc123...",
  "status": "confirmed",
  "txHash": "0xdef456...",
  "blockNumber": 18500000
}
```

Status values: `submitted`, `pending`, `confirmed`, `failed`

## Examples

::: code-group

```python [Python]
import requests

BASE = "https://api.jarvisclaw.ai/v1/marketplace/dex"
HEADERS = {
    "Authorization": "Bearer sk-your-api-key",
}

USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"

# Get indicative price for 1000 USDC -> WETH on Ethereum
resp = requests.get(f"{BASE}/price", headers=HEADERS, params={
    "chainId": 1,
    "sellToken": USDC,
    "buyToken": WETH,
    "sellAmount": "1000000000",  # 1000 USDC (6 decimals)
})
price = resp.json()
print(f"Buy amount: {price['buyAmount']} wei")

# Get firm quote
resp = requests.get(f"{BASE}/quote", headers=HEADERS, params={
    "chainId": 1,
    "sellToken": USDC,
    "buyToken": WETH,
    "sellAmount": "1000000000",
    "taker": "0xYourWalletAddress",
})
quote = resp.json()
```

```bash [cURL]
# Get swap price (USDC -> WETH on Ethereum)
curl "https://api.jarvisclaw.ai/v1/marketplace/dex/price?\
chainId=1&\
sellToken=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48&\
buyToken=0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2&\
sellAmount=1000000000" \
  -H "Authorization: Bearer sk-your-api-key"

# Check gasless swap status
curl "https://api.jarvisclaw.ai/v1/marketplace/dex/gasless/status/0xabc123" \
  -H "Authorization: Bearer sk-your-api-key"
```

:::

## Notes

- Token addresses must be checksummed or lowercase — not mixed case
- `sellAmount` is always in the token's smallest unit (e.g., 6 decimals for USDC, 18 for ETH)
- Gasless swaps require Permit2 approval for the sell token
- Quotes are valid for approximately 30 seconds
- Slippage protection is built into the quote — no additional slippage parameter needed
