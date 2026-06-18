# SDK Reference

Complete reference for the JarvisClaw Python and Go SDKs.

## Installation

Install the SDK via pip or go get, then initialize a client with your API key or wallet private key.

::: code-group

```shell [Python]
# Standard installation
pip install jarvisclaw

# With x402 agent support (EVM / Base chain)
pip install jarvisclaw[agent]

# With Solana support
pip install jarvisclaw[solana]

# With async (httpx) support
pip install jarvisclaw[async]

# Everything
pip install jarvisclaw[all]
```

```shell [Go]
go get github.com/api-jarvisclaw/go-sdk
```

:::

### Initialization

::: code-group

```python [Python]
from jarvisclaw import ChatClient, ImageClient, VideoClient

# API Key mode — each client is independent
chat = ChatClient(api_key="sk-your-api-key")
image = ImageClient(api_key="sk-your-api-key")

# Agent (x402) mode — pays from wallet, no API key needed
chat = ChatClient(private_key="0x<your-wallet-private-key>")

# Environment variables also work:
#   JARVISCLAW_API_KEY=sk-...  or  JARVISCLAW_WALLET_KEY=0x...
chat = ChatClient()  # auto-detects from env
```

```go [Go]
import jarvisclaw "github.com/api-jarvisclaw/go-sdk"

// API Key mode
client, _ := jarvisclaw.NewChatClient(jarvisclaw.WithAPIKey("sk-your-api-key"))

// Agent (x402) mode — pays from wallet, no API key needed
client, _ := jarvisclaw.NewChatClient(jarvisclaw.WithPrivateKey("0x<your-wallet-private-key>"))
```

:::

::: info Environment variables
```
JARVISCLAW_API_KEY=sk-...
JARVISCLAW_PRIVATE_KEY=0x...
```
:::

### Timeout & Cancellation

All clients support a `timeout` parameter (in seconds). The server holds the upstream connection open for at most this duration — if the model hasn't finished by then, the request is cancelled server-side.

::: code-group

```python [Python]
from jarvisclaw import ChatClient

# Default timeout is 120s; override per-client or per-call
chat = ChatClient(api_key="sk-...", timeout=300)

# Per-call override
response = chat.complete("Summarize this book...", timeout=600)
```

```go [Go]
// Use context deadline — the SDK forwards it to the server
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
defer cancel()

text, _ := client.Complete(ctx, "Summarize this book...")
```

:::

| Timeout | Behavior |
|---------|----------|
| `timeout=120` | Server waits up to 120 seconds |
| `timeout=300` | Server waits up to 300 seconds |
| Client disconnects | Upstream request auto-cancelled, no charge |

::: tip
For long-running tasks (video, music), the SDK sets sensible defaults internally (video defaults to 900s). You typically only need to adjust timeout for chat completions.
:::

### Authentication & Chain Support

| Client | API Key | Private Key (x402) | Python Chains | Go Chains |
|--------|---------|-------------------|---------------|-----------|
| ChatClient | ✅ | ✅ | Base + Solana | Base only |
| ImageClient | ✅ | ✅ | Base + Solana | Base only |
| VideoClient | ✅ | ✅ | Base + Solana | Base only |
| AudioClient | ✅ | ✅ | Base + Solana | Base only |
| SearchClient | ✅ | ✅ | Base + Solana | Base only |
| MarketplaceClient | ❌ | ✅ Private key only | Base + Solana | Base only |

## Chat & Streaming

Send chat messages and stream responses in real time.

::: code-group

```python [Python]
from jarvisclaw import ChatClient

chat = ChatClient()  # picks up JARVISCLAW_API_KEY from env

# Simple chat — one string in, one string out
response = chat.complete("What is quantum computing?")
print(response)

# Full control — messages array, system prompt, temperature
resp = chat.completion([
    {"role": "system", "content": "You are a helpful tutor."},
    {"role": "user", "content": "Explain gravity simply."}
], model="auto", temperature=0.5)
print(resp.content)
print(f"Tokens used: {resp.usage}")

# Streaming — yields text chunks
for chunk in chat.stream("Tell me a joke"):
    print(chunk, end="", flush=True)

# ─── asyncio — concurrent chat ───
import asyncio
from jarvisclaw.aio import ChatClient as AsyncChatClient

async def main():
    async with AsyncChatClient(private_key="0x...") as chat:
        # Concurrent requests to multiple models
        results = await asyncio.gather(
            chat.complete("Hi", model="openai/gpt-5.4"),
            chat.complete("Hi", model="anthropic/claude-sonnet-4.6"),
            chat.complete("Hi", model="google/gemini-2.5-flash"),
        )
        for r in results:
            print(r)

        # Async streaming
        async for chunk in chat.stream("Tell me a story"):
            print(chunk, end="")

asyncio.run(main())
```

```go [Go]
import jarvisclaw "github.com/api-jarvisclaw/go-sdk"

client, _ := jarvisclaw.NewChatClient(jarvisclaw.WithAPIKey("sk-your-api-key"))

// Simple chat — one string in, one string out
text, _ := client.Complete(ctx, "What is quantum computing?")
fmt.Println(text)

// Full control — messages array, system prompt, temperature
resp, _ := client.Completion(ctx, []jarvisclaw.Message{
    {Role: "system", Content: "You are a helpful tutor."},
    {Role: "user", Content: "Explain gravity simply."},
}, jarvisclaw.WithModel("auto"), jarvisclaw.WithTemperature(0.5))
fmt.Println(resp.Content)
fmt.Printf("Tokens used: %+v\n", resp.Usage)

// Streaming — channel emits text chunks
stream, _ := client.Stream(ctx, "Tell me a joke")
for chunk := range stream {
    fmt.Print(chunk)
}
```

:::

## Images

Generate and edit images. Supports blocking and non-blocking modes.

::: code-group

```python [Python]
from jarvisclaw import ImageClient

image = ImageClient(private_key="0x...")

# ─── Blocking (default) — waits until image is ready ───
result = image.generate("A cat on Mars", size="1024x1024")
print(result.url)            # "https://api.jarvisclaw.ai/media/images/..."
print(result.revised_prompt) # Model's revised prompt (if any)

# Specify model explicitly
result = image.generate("Neon city", model="openai/gpt-image-1", size="1792x1024")
print(result.url)

# ─── Non-blocking — submit and come back later ───
job = image.generate("A futuristic city", wait=False)
print(job.raw["id"])         # "e061906e-..."
print(job.raw["status"])     # "queued"

# Single status check (non-blocking)
result = image.status(job.raw["id"])
print(result.raw.get("status"))  # "in_progress" or "completed"

# Block until done (call anytime after submit)
result = image.wait(job.raw["id"])
print(result.url)  # guaranteed URL

# ─── Edit — always blocking ───
result = image.edit(open("photo.png", "rb"), "Remove the background")
print(result.url)

# ─── asyncio — concurrent generation ───
import asyncio
from jarvisclaw.aio import ImageClient as AsyncImageClient

async def main():
    async with AsyncImageClient(private_key="0x...") as img:
        results = await asyncio.gather(
            img.generate("A sunrise"),
            img.generate("A sunset"),
            img.generate("A moonrise"),
        )
        for r in results:
            print(r.url)

asyncio.run(main())
```

```go [Go]
client, _ := jarvisclaw.NewImageClient(jarvisclaw.WithPrivateKey("0x..."))

// Blocking (default)
img, _ := client.Generate(ctx, "A cat on Mars", jarvisclaw.WithSize("1024x1024"))
fmt.Println(img.URL)

// Non-blocking
job, _ := client.Generate(ctx, "A city", jarvisclaw.WithWait(false))
fmt.Printf("Job: %s\n", job.ID)

// Wait later
result, _ := client.Wait(ctx, job.ID)
fmt.Println(result.URL)
```

:::

## Video

Generate videos from text prompts. Video generation typically takes 1-3 minutes, but upstream status may lag up to 10 minutes. Jobs are retrievable for 48 hours — never discard a job ID on timeout.

::: warning Best Practice
Set poll_timeout to 15 minutes (or use non-blocking mode). If a timeout occurs, the job still exists on our server — call status(job_id) later to retrieve the video. No charge occurs unless the video completes successfully.
:::

::: code-group

```python [Python]
from jarvisclaw import VideoClient

video = VideoClient(private_key="0x...")

# ─── Blocking (default) — waits until ready ───
# Default poll_timeout=900s (15 min). Upstream status may lag 5-10 min.
job = video.generate("A cat walking on a beach", duration=5)
print(job.url)     # MP4 URL
print(job.status)  # "completed"

# ─── Non-blocking — submit and come back later ───
job = video.generate("Ocean waves at sunset", wait=False)
print(job.id)      # "bytedance:video_c6f42c34..."
print(job.status)  # "queued"

# Check status anytime (job retrievable for 48 hours)
result = video.status(job.id)
print(result.status)  # "in_progress" or "completed"
if result.url:
    print(result.url)

# Block until done (call anytime within 48h)
result = video.wait(job.id)
print(result.url)    # guaranteed MP4 URL

# ─── Handling timeouts gracefully ───
# On timeout, job is returned with status="timeout" and ID preserved
job = video.generate("Flower blooming timelapse", poll_timeout=900)
if job.status == "timeout":
    # Status sync lagged — job still exists, retrieve later
    print(f"Timed out, but job exists: {job.id}")
    # Retry anytime within 48 hours:
    result = video.status(job.id)
    if result.url:
        print(f"Video ready: {result.url}")

# ─── Best practices ───
# • poll_timeout=900 (15 min) is the default — usually sufficient
# • Jobs are retrievable for 48 hours after submission
# • Non-blocking + manual polling is safest for production agents
# • No charge if video fails — settlement only on "completed"
```

```go [Go]
client, _ := jarvisclaw.NewVideoClient(jarvisclaw.WithPrivateKey("0x..."))

// Blocking (default) — recommend 15min+ timeout for video
ctx, cancel := context.WithTimeout(context.Background(), 15*time.Minute)
defer cancel()

job, err := client.Generate(ctx, "A cat walking on a beach",
    jarvisclaw.WithDuration(5),
    jarvisclaw.WithPollTimeout(15*time.Minute), // override context deadline for polling
)
if err == nil {
    fmt.Printf("Video URL: %s\n", job.URL)
}

// ─── Handling timeouts gracefully ───
// On timeout, job is still returned (with ID) — retrieve later
if err != nil && job != nil {
    fmt.Printf("Timed out, but job exists: %s\n", job.ID)
    // Retry anytime within 48 hours:
    result, _ := client.Status(context.Background(), job.ID)
    if result.URL != "" {
        fmt.Printf("Video ready: %s\n", result.URL)
    }
}

// ─── Non-blocking — safest for production agents ───
job, _ = client.Generate(ctx, "Ocean waves",
    jarvisclaw.WithWait(false),
)
fmt.Printf("Job %s submitted\n", job.ID)

// Poll manually (job retrievable for 48h)
result, _ := client.Status(ctx, job.ID)
fmt.Printf("Status: %s, URL: %s\n", result.Status, result.URL)

// ─── Best practices ───
// • WithPollTimeout(15*time.Minute) — upstream status can lag 7+ min
// • Jobs retrievable for 48 hours — never discard a job ID on timeout
// • Non-blocking + manual Status() polling is safest for agents
// • No charge if video fails — x402 settlement only on "completed"
```

:::

## Audio

Generate music and speech. Speech is fast (<5s); music takes 1-3 minutes.

::: code-group

```python [Python]
from jarvisclaw import AudioClient

audio = AudioClient(private_key="0x...")

# ─── music() — blocking (takes 1-3 minutes) ───
result = audio.music("An upbeat electronic track")
with open("music.mp3", "wb") as f:
    f.write(result.content)

# ─── music(wait=False) — non-blocking ───
job = audio.music("Lo-fi hip hop beat", wait=False)
print(job.done)  # False — still generating

# Do other work...
# Then get result when needed (blocks from this point)
result = job.result()
with open("lofi.mp3", "wb") as f:
    f.write(result.content)

# ─── speech() — always blocking (fast, <5s) ───
result = audio.speech("Hello world", voice="alloy")
with open("output.mp3", "wb") as f:
    f.write(result.content)

# ─── asyncio — concurrent audio tasks ───
import asyncio
from jarvisclaw.aio import AudioClient as AsyncAudioClient

async def main():
    async with AsyncAudioClient(private_key="0x...") as aud:
        # Concurrent music + speech generation
        music, speech = await asyncio.gather(
            aud.music("Jazz piano"),
            aud.speech("Hello world", voice="nova"),
        )
        # music.content and speech.content are bytes

asyncio.run(main())
```

```go [Go]
client, _ := jarvisclaw.NewAudioClient(jarvisclaw.WithAPIKey("sk-..."))

// Text-to-Speech
data, _ := client.Speech(ctx, "Hello world", jarvisclaw.WithVoice("alloy"))
os.WriteFile("output.mp3", data.Content, 0644)

// Music generation (blocking, 1-3 min)
music, _ := client.Music(ctx, "An upbeat electronic track")
os.WriteFile("music.mp3", music.Content, 0644)
```

:::

## Search

Run web searches, find similar pages, and fetch full page content.

::: code-group

```python [Python]
from jarvisclaw import SearchClient

search = SearchClient()

results = search.query("latest AI news", num_results=5)
for r in results:
    print(f"{r.title}")
    print(f"  {r.url}")
    print(f"  {r.snippet}")

# Find similar pages
similar = search.find_similar("https://example.com/article")

# Get full page content
pages = search.contents(["https://example.com/page1"])
```

```go [Go]
client, _ := jarvisclaw.NewSearchClient(jarvisclaw.WithAPIKey("sk-..."))

resp, _ := client.Query(ctx, "latest AI news", jarvisclaw.WithNumResults(5))
fmt.Println(resp.Summary)            // AI-generated answer
fmt.Printf("Sources used: %d\n", resp.SourcesUsed)
for _, c := range resp.Citations {
    fmt.Printf("  %s — %s\n", c.Title, c.URL)
}
```

:::

## Prediction Markets & Marketplace

Query prediction market data, crypto data (Surf), DEX trading, and more via the unified MarketplaceClient.

::: code-group

```python [Python]
from jarvisclaw import MarketplaceClient

mp = MarketplaceClient(private_key="0x<evm-private-key>")

# ─── Prediction Markets ───
markets = mp.call("prediction", "/polymarket/markets", params={"market_slug": "will-trump-win"})
kalshi = mp.call("prediction", "/kalshi/markets", params={"market_ticker": "KXBTC"})
search = mp.call("prediction", "/markets/search", params={"q": "bitcoin 2026", "limit": "5"})

# ─── Crypto Data (Surf — 83 endpoints) ───

# Exchange (16 CEXes: binance, coinbase, kraken, etc.)
price = mp.call("surf", "/exchange/price", params={"pair": "BTC-USDT"})
klines = mp.call("surf", "/exchange/klines", params={"pair": "ETH-USDT", "interval": "1h", "limit": "24"})
funding = mp.call("surf", "/exchange/funding-history", params={"pair": "BTC-USDT"})

# Market overview
rankings = mp.call("surf", "/market/ranking", params={"limit": "10"})
fear_greed = mp.call("surf", "/market/fear-greed")
etf = mp.call("surf", "/market/etf", params={"symbol": "BTC"})
btc_price = mp.call("surf", "/market/price", params={"symbol": "BTC"})
onchain_ind = mp.call("surf", "/market/onchain-indicator", params={"symbol": "BTC", "metric": "nvt"})
price_ind = mp.call("surf", "/market/price-indicator", params={"indicator": "rsi", "symbol": "BTC"})

# Social / CT intelligence (use handle, not username)
social_ranking = mp.call("surf", "/social/ranking", params={"limit": "10"})
mindshare = mp.call("surf", "/social/mindshare", params={"q": "ETH", "interval": "1d"})
user = mp.call("surf", "/social/user", params={"handle": "VitalikButerin"})
posts = mp.call("surf", "/social/user/posts", params={"handle": "VitalikButerin", "limit": "5"})

# Wallet intelligence (use address)
wallet = mp.call("surf", "/wallet/detail", params={"address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"})
net_worth = mp.call("surf", "/wallet/net-worth", params={"address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"})

# Token analytics (use address+chain, not symbol — except tokenomics)
holders = mp.call("surf", "/token/holders", params={"address": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984", "chain": "ethereum"})
dex_trades = mp.call("surf", "/token/dex-trades", params={"address": "0x6982508145454Ce325dDbE47a25d4ec3d2311933"})
transfers = mp.call("surf", "/token/transfers", params={"address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", "chain": "base"})
tokenomics = mp.call("surf", "/token/tokenomics", params={"symbol": "ARB"})

# VC Fund intelligence (use q for search, metric for ranking)
funds = mp.call("surf", "/fund/ranking", params={"metric": "tier", "limit": "10"})
fund_detail = mp.call("surf", "/fund/detail", params={"q": "a16z"})
portfolio = mp.call("surf", "/fund/portfolio", params={"q": "a16z", "limit": "20"})

# Project / DeFi (metric enum: volume/fee/fees/revenue/tvl/users)
defi_ranking = mp.call("surf", "/project/defi/ranking", params={"metric": "tvl", "limit": "10"})
defi_metrics = mp.call("surf", "/project/defi/metrics", params={"q": "uniswap", "metric": "tvl"})

# On-chain SQL (chain required for gas-price and tx)
gas = mp.call("surf", "/onchain/gas-price", params={"chain": "ethereum"})
sql_result = mp.call("surf", "/onchain/sql", method="POST", json={
    "sql": "SELECT from_address, SUM(value/1e18) as eth FROM ethereum.transactions LIMIT 5"
})

# News
news = mp.call("surf", "/news/feed", params={"limit": "5"})

# Search
web_results = mp.call("surf", "/search/web", params={"q": "bitcoin etf"})
projects = mp.call("surf", "/search/project", params={"q": "uniswap"})

# Web fetch
page = mp.call("surf", "/web/fetch", params={"url": "https://ethereum.org"})

# ─── DEX Trading (0x) ───
quote = mp.call("dex", "/price", params={
    "sellToken": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
    "buyToken": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "sellAmount": "100000000000000000", "chainId": "8453"
})

# ─── Web Search (Exa) ───
exa = mp.call("exa", "/search", method="POST", json={"query": "AI agents 2026", "num_results": 5})

# ─── Blockchain RPC (40+ chains) ───
block = mp.rpc_call("eth", "eth_blockNumber")
slot = mp.rpc_call("sol", "getSlot")
base_block = mp.rpc_call("base", "eth_blockNumber")

# ─── DeFi (DefiLlama) ───
protocols = mp.defi_protocols()
aave = mp.defi_protocol("aave-v3")
```

```go [Go]
mc, _ := jarvisclaw.NewMarketplaceClient(jarvisclaw.WithPrivateKey("0x<evm-private-key>"))

// ─── Prediction Markets ───
markets, _ := mc.Call(ctx, "prediction", "/polymarket/markets",
    jarvisclaw.WithParams(map[string]string{"market_slug": "will-trump-win"}))
kalshi, _ := mc.Call(ctx, "prediction", "/kalshi/markets",
    jarvisclaw.WithParams(map[string]string{"market_ticker": "KXBTC"}))

// ─── Crypto Data (Surf) ───
price, _ := mc.Call(ctx, "surf", "/exchange/price",
    jarvisclaw.WithParams(map[string]string{"pair": "BTC-USDT"}))
rankings, _ := mc.Call(ctx, "surf", "/market/ranking",
    jarvisclaw.WithParams(map[string]string{"limit": "10"}))
fearGreed, _ := mc.Call(ctx, "surf", "/market/fear-greed")
etf, _ := mc.Call(ctx, "surf", "/market/etf",
    jarvisclaw.WithParams(map[string]string{"symbol": "BTC"}))
indicator, _ := mc.Call(ctx, "surf", "/market/onchain-indicator",
    jarvisclaw.WithParams(map[string]string{"symbol": "BTC", "metric": "nvt"}))

// Social (use handle, not username)
user, _ := mc.Call(ctx, "surf", "/social/user",
    jarvisclaw.WithParams(map[string]string{"handle": "VitalikButerin"}))
mindshare, _ := mc.Call(ctx, "surf", "/social/mindshare",
    jarvisclaw.WithParams(map[string]string{"q": "ETH", "interval": "1d"}))

// Token (use address+chain, not symbol)
holders, _ := mc.Call(ctx, "surf", "/token/holders",
    jarvisclaw.WithParams(map[string]string{"address": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984", "chain": "ethereum"}))
tokenomics, _ := mc.Call(ctx, "surf", "/token/tokenomics",
    jarvisclaw.WithParams(map[string]string{"symbol": "ARB"}))

// Fund (use q for search, metric for ranking)
funds, _ := mc.Call(ctx, "surf", "/fund/ranking",
    jarvisclaw.WithParams(map[string]string{"metric": "tier", "limit": "10"}))
fundDetail, _ := mc.Call(ctx, "surf", "/fund/detail",
    jarvisclaw.WithParams(map[string]string{"q": "a16z"}))

// Wallet
wallet, _ := mc.Call(ctx, "surf", "/wallet/detail",
    jarvisclaw.WithParams(map[string]string{"address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"}))

// On-chain
gas, _ := mc.Call(ctx, "surf", "/onchain/gas-price",
    jarvisclaw.WithParams(map[string]string{"chain": "ethereum"}))
sql, _ := mc.Post(ctx, "surf", "/onchain/sql", map[string]any{
    "sql": "SELECT from_address, SUM(value/1e18) as eth FROM ethereum.transactions LIMIT 5"})

// ─── DEX ───
quote, _ := mc.Call(ctx, "dex", "/price",
    jarvisclaw.WithParams(map[string]string{
        "sellToken": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
        "buyToken": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "sellAmount": "100000000000000000", "chainId": "8453"}))

// ─── Exa Search ───
exa, _ := mc.Post(ctx, "exa", "/search", map[string]any{"query": "AI agents", "num_results": 5})

// ─── RPC (40+ chains) ───
block, _ := mc.RPCCall(ctx, "eth", "eth_blockNumber", []any{})
slot, _ := mc.RPCCall(ctx, "sol", "getSlot", []any{})

// ─── DeFi ───
aave, _ := mc.DefiProtocol(ctx, "aave-v3")
```

:::

### Marketplace (Async / Concurrent)

::: code-group

```python [Python — asyncio]
import asyncio
from jarvisclaw.aio import MarketplaceClient

async def main():
    async with MarketplaceClient(private_key="0x...") as mp:
        # Concurrent calls to multiple marketplace endpoints
        polymarket, btc_price, fear_greed = await asyncio.gather(
            mp.call("prediction", "/polymarket/markets",
                    params={"market_slug": "will-trump-win"}),
            mp.call("surf", "/exchange/price",
                    params={"pair": "BTC-USDT"}),
            mp.call("surf", "/market/fear-greed"),
        )
        print(polymarket, btc_price, fear_greed)

        # Concurrent RPC calls
        eth_block, sol_slot = await asyncio.gather(
            mp.rpc_call("eth", "eth_blockNumber"),
            mp.rpc_call("sol", "getSlot"),
        )
        print(f"ETH block: {eth_block}, SOL slot: {sol_slot}")

asyncio.run(main())
```

```go [Go — goroutines]
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "sync"

    jarvisclaw "github.com/api-jarvisclaw/go-sdk"
)

func main() {
    ctx := context.Background()
    mc, _ := jarvisclaw.NewMarketplaceClient(jarvisclaw.WithPrivateKey("0x..."))

    var (
        polymarket, btcPrice, fearGreed json.RawMessage
        wg                              sync.WaitGroup
    )

    wg.Add(3)
    go func() {
        defer wg.Done()
        polymarket, _ = mc.Call(ctx, "prediction", "/polymarket/markets",
            jarvisclaw.WithParams(map[string]string{"market_slug": "will-trump-win"}))
    }()
    go func() {
        defer wg.Done()
        btcPrice, _ = mc.Call(ctx, "surf", "/exchange/price",
            jarvisclaw.WithParams(map[string]string{"pair": "BTC-USDT"}))
    }()
    go func() {
        defer wg.Done()
        fearGreed, _ = mc.Call(ctx, "surf", "/market/fear-greed")
    }()
    wg.Wait()

    fmt.Println(string(polymarket), string(btcPrice), string(fearGreed))
}
```

:::

## Balance & Spending

Check your API key quota or on-chain USDC balance, and track per-session spending.

::: code-group

```python [Python]
from jarvisclaw import ChatClient

client = ChatClient()

# Check balance (API Key mode: server quota; x402 mode: on-chain USDC)
balance = client.get_balance()
print(f"Balance: ${balance:.2f}")

# Session spending (tracked locally by SDK)
print(f"Spent this session: ${client.get_spending():.2f}")

# Wallet address (x402 mode only, None in API Key mode)
if client.address:
    print(f"Wallet: {client.address}")
```

```go [Go]
// Check balance (API Key mode: server quota; x402 mode: on-chain USDC)
balance, _ := client.GetBalance(ctx)
fmt.Printf("Balance: $%.2f\n", balance)

// Wallet address (x402 mode only, empty string in API Key mode)
if addr := client.Address(); addr != "" {
    fmt.Printf("Wallet: %s\n", addr)
}
```

:::

## Error Handling

The SDK raises typed exceptions so you can handle auth, rate-limit, balance, and payment errors distinctly.

::: code-group

```python [Python]
from jarvisclaw import (
    ChatClient, AuthenticationError, RateLimitError,
    InsufficientBalanceError, PaymentError, APIError
)

chat = ChatClient()

try:
    response = chat.complete("Hello")
except AuthenticationError:
    print("Invalid API key — check JARVISCLAW_API_KEY")
except RateLimitError as e:
    print(f"Rate limited — retry after {e.retry_after}s")
except InsufficientBalanceError:
    print("Balance too low — top up at dashboard")
except PaymentError as e:
    print(f"x402 payment failed: {e}")
except APIError as e:
    print(f"API error {e.status_code}: {e.message}")
```

```go [Go]
import "errors"

text, err := client.Complete(ctx, "Hello")
if err != nil {
    var authErr *jarvisclaw.AuthenticationError
    var rateErr *jarvisclaw.RateLimitError
    var balErr  *jarvisclaw.InsufficientBalanceError
    var payErr  *jarvisclaw.PaymentError
    var apiErr  *jarvisclaw.APIError

    switch {
    case errors.As(err, &authErr):
        log.Fatal("Invalid API key")
    case errors.As(err, &rateErr):
        log.Printf("Rate limited — retry after %ds", rateErr.RetryAfter)
    case errors.As(err, &balErr):
        log.Fatal("Balance too low — top up at dashboard")
    case errors.As(err, &payErr):
        log.Fatalf("x402 payment failed: %v", payErr)
    case errors.As(err, &apiErr):
        log.Fatalf("API error %d: %s", apiErr.StatusCode, apiErr.Message)
    }
}
```

:::
