# DEX Trading API (0x Swap)

Decentralized exchange trading via 0x protocol. Best-execution routing across 100+ DEXes with Permit2 and Gasless V2. **FREE for all callers** — you only pay on-chain gas fees.

## Base URL

```
https://api.jarvisclaw.ai/v1/marketplace/dex
```

## Pricing

**All DEX endpoints are free.** No JarvisClaw fees — only standard on-chain gas costs for submitted transactions. Gasless swaps eliminate even gas fees for supported tokens.

## Supported Chains

| Chain | Chain ID | Gasless Support |
|-------|----------|-----------------|
| Ethereum | `1` | Yes |
| Base | `8453` | Yes |
| Polygon | `137` | Yes |
| Arbitrum | `42161` | Yes |
| Optimism | `10` | Yes |

## Endpoints

| Method | Endpoint | Description | Price |
|--------|----------|-------------|-------|
| GET | `/price` | Indicative swap price (no commitment) | Free |
| GET | `/quote` | Firm quote with calldata + Permit2 data | Free |
| POST | `/gasless/submit` | Submit a signed gasless swap | Free |
| GET | `/gasless/status/:tradeHash` | Track gasless swap status | Free |

---

## Get Price

`GET /v1/marketplace/dex/price`

Get an indicative price for a token swap without committing. Use for UI display or pre-trade checks.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sellToken` | string | Yes | Token contract address to sell |
| `buyToken` | string | Yes | Token contract address to buy |
| `sellAmount` | string | Yes | Amount to sell in base units (e.g., `1000000` = 1 USDC) |
| `chainId` | integer | Yes | Target chain ID |
| `taker` | string | No | Taker wallet address (improves routing) |


### Response

```json
{
  "chainId": 8453,
  "sellToken": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  "buyToken": "0x4200000000000000000000000000000000000006",
  "sellAmount": "1000000000",
  "buyAmount": "385000000000000000",
  "price": "0.000385",
  "sources": [
    { "name": "Uniswap_V3", "proportion": "0.75" },
    { "name": "Aerodrome", "proportion": "0.25" }
  ],
  "estimatedGas": "145000",
  "gasPrice": "50000000"
}
```


---

## Get Quote

`GET /v1/marketplace/dex/quote`

Get a firm quote with transaction calldata ready for signing. Includes EIP-712 typed data for Permit2 gasless swaps.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sellToken` | string | Yes | Token contract address to sell |
| `buyToken` | string | Yes | Token contract address to buy |
| `sellAmount` | string | Yes | Amount to sell in base units |
| `chainId` | integer | Yes | Target chain ID |
| `takerAddress` | string | Yes | Taker wallet address (required for quote) |

### Response

```json
{
  "chainId": 8453,
  "sellToken": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  "buyToken": "0x4200000000000000000000000000000000000006",
  "sellAmount": "1000000000",
  "buyAmount": "384500000000000000",
  "to": "0xDef1C0ded9bec7F1a1670819833240f027b25EfF",
  "data": "0x415565b0000000000000000000...",
  "value": "0",
  "gas": "185000",
  "gasPrice": "50000000",
  "permit2": {
    "type": "Permit2",
    "hash": "0x1234abcd...",
    "eip712": {
      "types": { "...": "..." },
      "domain": { "...": "..." },
      "message": { "...": "..." },
      "primaryType": "PermitWitnessTransferFrom"
    }
  },
  "validTo": 1717243800
}
```

::: info Quote Expiry
Quotes are valid for **30 seconds**. After expiry, you must request a new quote.
:::


---

## Submit Gasless Swap

`POST /v1/marketplace/dex/gasless/submit`

Submit a signed gasless swap. The relayer pays gas on your behalf — the taker pays nothing beyond the swap amount.

### Request

```json
{
  "trade": {
    "chainId": 8453,
    "sellToken": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "buyToken": "0x4200000000000000000000000000000000000006",
    "sellAmount": "1000000000",
    "buyAmount": "384500000000000000",
    "to": "0xDef1C0ded9bec7F1a1670819833240f027b25EfF",
    "data": "0x415565b0...",
    "permit2": { "...": "..." }
  },
  "signature": "0xabcdef1234567890..."
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `trade` | object | Yes | Full quote object from `/quote` response |
| `signature` | string | Yes | EIP-712 signature from taker wallet |

### Response

```json
{
  "tradeHash": "0x9f8e7d6c5b4a3210...",
  "status": "submitted",
  "createdAt": "2025-06-01T15:30:00Z"
}
```


---

## Track Gasless Swap Status

`GET /v1/marketplace/dex/gasless/status/:tradeHash`

Poll the status of a submitted gasless swap.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tradeHash` | string | Yes | Trade hash from submit response |

### Response

```json
{
  "tradeHash": "0x9f8e7d6c5b4a3210...",
  "status": "confirmed",
  "txHash": "0xabc123def456...",
  "blockNumber": 18500000,
  "gasUsed": "142000"
}
```

Status values: `submitted`, `pending`, `confirmed`, `failed`

---

## Examples

::: code-group

```bash [cURL]
# Get indicative price (1000 USDC -> WETH on Base)
curl "https://api.jarvisclaw.ai/v1/marketplace/dex/price?\
chainId=8453&\
sellToken=0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913&\
buyToken=0x4200000000000000000000000000000000000006&\
sellAmount=1000000000" \
  -H "Authorization: Bearer sk-your-api-key"

# Get firm quote (requires takerAddress)
curl "https://api.jarvisclaw.ai/v1/marketplace/dex/quote?\
chainId=8453&\
sellToken=0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913&\
buyToken=0x4200000000000000000000000000000000000006&\
sellAmount=1000000000&\
takerAddress=0xYourWalletAddress" \
  -H "Authorization: Bearer sk-your-api-key"

# Submit gasless swap
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/dex/gasless/submit \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "trade": { "...quote object..." },
    "signature": "0xYourEIP712Signature..."
  }'

# Check gasless swap status
curl "https://api.jarvisclaw.ai/v1/marketplace/dex/gasless/status/0x9f8e7d6c5b4a3210" \
  -H "Authorization: Bearer sk-your-api-key"
```

```python [Python (API Key)]
import requests
import time

BASE = "https://api.jarvisclaw.ai/v1/marketplace/dex"
HEADERS = {"Authorization": "Bearer sk-your-api-key"}

# Token addresses on Base
USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
WETH_BASE = "0x4200000000000000000000000000000000000006"

# 1. Get indicative price for 1000 USDC -> WETH
resp = requests.get(f"{BASE}/price", headers=HEADERS, params={
    "chainId": 8453,
    "sellToken": USDC_BASE,
    "buyToken": WETH_BASE,
    "sellAmount": "1000000000",  # 1000 USDC (6 decimals)
})
price = resp.json()
print(f"Buy amount: {price['buyAmount']} wei WETH")
print(f"Routed via: {[s['name'] for s in price['sources']]}")

# 2. Get firm quote
resp = requests.get(f"{BASE}/quote", headers=HEADERS, params={
    "chainId": 8453,
    "sellToken": USDC_BASE,
    "buyToken": WETH_BASE,
    "sellAmount": "1000000000",
    "takerAddress": "0xYourWalletAddress",
})
quote = resp.json()

# 3. Sign the EIP-712 permit2 data (requires eth_account)
# signature = sign_eip712(quote["permit2"]["eip712"], private_key)

# 4. Submit gasless swap
resp = requests.post(f"{BASE}/gasless/submit", headers=HEADERS, json={
    "trade": quote,
    "signature": "0x<your-eip712-signature>",
})
trade_hash = resp.json()["tradeHash"]

# 5. Poll status
while True:
    resp = requests.get(f"{BASE}/gasless/status/{trade_hash}", headers=HEADERS)
    status = resp.json()
    if status["status"] == "confirmed":
        print(f"Swap confirmed! TX: {status['txHash']}")
        break
    elif status["status"] == "failed":
        print("Swap failed")
        break
    time.sleep(2)
```

```python [Python (x402 Agent)]
from jarvisclaw import MarketplaceClient

# x402 agent — pays with USDC automatically (DEX endpoints are free anyway)
client = MarketplaceClient(private_key="0x<agent-wallet-private-key>")

USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
WETH_BASE = "0x4200000000000000000000000000000000000006"

# Get price (free — no payment triggered)
price = client.call("dex", "/price", params={
    "chainId": 8453,
    "sellToken": USDC_BASE,
    "buyToken": WETH_BASE,
    "sellAmount": "1000000000",
})
print(f"Price: {price['buyAmount']} wei for 1000 USDC")

# Get firm quote
quote = client.call("dex", "/quote", params={
    "chainId": 8453,
    "sellToken": USDC_BASE,
    "buyToken": WETH_BASE,
    "sellAmount": "1000000000",
    "takerAddress": "0xYourWalletAddress",
})

# Submit gasless (after signing permit2 externally)
result = client.call("dex", "/gasless/submit", method="POST", json={
    "trade": quote,
    "signature": "0x<signed-permit2>",
})
print(f"Trade hash: {result['tradeHash']}")

# Poll status
status = client.call("dex", f"/gasless/status/{result['tradeHash']}")
print(f"Status: {status['status']}")
```

```go [Go (API Key)]
package main

import (
    "context"
    "fmt"
    "time"

    jarvisclaw "github.com/api-jarvisclaw/go-sdk"
)

func main() {
    mc, _ := jarvisclaw.NewMarketplaceClient(jarvisclaw.WithAPIKey("sk-your-api-key"))
    ctx := context.Background()

    usdcBase := "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    wethBase := "0x4200000000000000000000000000000000000006"

    // 1. Get indicative price
    price, err := mc.Call(ctx, "dex", "/price", jarvisclaw.WithParams(map[string]string{
        "chainId":    "8453",
        "sellToken":  usdcBase,
        "buyToken":   wethBase,
        "sellAmount": "1000000000",
    }))
    if err != nil {
        panic(err)
    }
    fmt.Printf("Buy amount: %s wei\n", price["buyAmount"])

    // 2. Get firm quote
    quote, err := mc.Call(ctx, "dex", "/quote", jarvisclaw.WithParams(map[string]string{
        "chainId":      "8453",
        "sellToken":    usdcBase,
        "buyToken":     wethBase,
        "sellAmount":   "1000000000",
        "takerAddress": "0xYourWalletAddress",
    }))
    if err != nil {
        panic(err)
    }

    // 3. Sign permit2 EIP-712 data and submit gasless swap
    // signature := signEIP712(quote["permit2"], privateKey)

    submit, err := mc.Post(ctx, "dex", "/gasless/submit", map[string]interface{}{
        "trade":     quote,
        "signature": "0x<your-eip712-signature>",
    })
    if err != nil {
        panic(err)
    }
    tradeHash := submit["tradeHash"].(string)
    fmt.Printf("Trade hash: %s\n", tradeHash)

    // 4. Poll status
    for {
        status, _ := mc.Call(ctx, "dex",
            fmt.Sprintf("/gasless/status/%s", tradeHash),
        )
        if status["status"] == "confirmed" {
            fmt.Printf("Confirmed! TX: %s\n", status["txHash"])
            break
        }
        time.Sleep(2 * time.Second)
    }
}
```

```go [Go (x402 Agent)]
package main

import (
    "context"
    "fmt"

    jarvisclaw "github.com/api-jarvisclaw/go-sdk"
)

func main() {
    // x402 agent — DEX endpoints are free, but x402 auth still works
    mc, _ := jarvisclaw.NewMarketplaceClient(
        jarvisclaw.WithPrivateKey("0x<agent-wallet-private-key>"),
    )
    ctx := context.Background()

    usdcBase := "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    wethBase := "0x4200000000000000000000000000000000000006"

    // Get price
    price, _ := mc.Call(ctx, "dex", "/price", jarvisclaw.WithParams(map[string]string{
        "chainId":    "8453",
        "sellToken":  usdcBase,
        "buyToken":   wethBase,
        "sellAmount": "1000000000",
    }))
    fmt.Printf("1000 USDC -> %s wei WETH\n", price["buyAmount"])

    // Get quote
    quote, _ := mc.Call(ctx, "dex", "/quote", jarvisclaw.WithParams(map[string]string{
        "chainId":      "8453",
        "sellToken":    usdcBase,
        "buyToken":     wethBase,
        "sellAmount":   "1000000000",
        "takerAddress": "0xYourWalletAddress",
    }))

    // Sign + submit gasless swap
    result, _ := mc.Post(ctx, "dex", "/gasless/submit", map[string]interface{}{
        "trade":     quote,
        "signature": "0x<signed-permit2>",
    })
    fmt.Printf("Submitted: %s\n", result["tradeHash"])
}
```

:::

---

## Errors

| Code | Error | Description |
|------|-------|-------------|
| 400 | `insufficient_liquidity` | Not enough liquidity across available DEXes for this trade |
| 400 | `unsupported_chain` | Chain ID not in supported list (1, 8453, 137, 42161, 10) |
| 410 | `price_expired` | Quote expired (30s lifetime) — request a new one |
| 400 | `invalid_token` | Token address is not a valid contract on the specified chain |
| 400 | `invalid_amount` | Sell amount is zero or exceeds token supply |
| 400 | `invalid_signature` | EIP-712 signature verification failed |
| 404 | `trade_not_found` | Unknown tradeHash in gasless status check |

---

## Limitations

- **5 chains only** — Ethereum (1), Base (8453), Polygon (137), Arbitrum (42161), Optimism (10)
- **Gasless requires Permit2** — Only tokens with Permit2 approval can use gasless swaps (most ERC-20s support this)
- **30s quote expiry** — Quotes are time-sensitive; sign and submit promptly
- **No limit orders** — Only immediate market swaps; no conditional or scheduled orders
- **Price impact on large trades** — Swaps over $100k may experience significant slippage due to DEX liquidity depth
- **Token addresses required** — Use contract addresses, not symbols; verify addresses on the target chain
- **Base units only** — All amounts are in the token's smallest denomination (6 decimals for USDC, 18 for ETH/WETH)
- **No partial fills** — Entire trade executes or reverts; no partial execution
