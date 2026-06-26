# Solana Payments (x402)

Pay for API calls with USDC on Solana mainnet. The SDK uses the same x402 protocol as Base chain — only the key format changes.

## Installation

```shell
# Standard (EVM / Base chain support only)
pip install jarvisclaw

# With Solana support
pip install jarvisclaw[solana]
```

## Automatic chain detection

::: info How the SDK picks the chain
- `0x...` — EVM hex key → Base chain (Chain ID 8453), USDC ERC-20
- `bs58` — Solana keypair → Solana mainnet, USDC SPL

No config flag needed — pass the key and the SDK does the rest.
:::

## Solana requirements

- A Solana wallet with USDC (SPL) on mainnet
- Export the full keypair (not just the public key) from Phantom or Solflare
- The exported key will be a base58-encoded string

## Initialization

Pass your Solana keypair string as private_key — the SDK detects Solana automatically.

::: code-group

```python [Python]
from jarvisclaw import ChatClient, ImageClient

# EVM wallet — hex private key (0x...) → Base chain (Chain ID 8453)
chat = ChatClient(private_key="0x<evm-wallet-private-key>")

# Solana wallet — bs58-encoded keypair → Solana mainnet
# SDK auto-detects: if key is base58 and not hex, it uses Solana
chat = ChatClient(private_key="<base58-solana-keypair>")

# Explicit network selection
chat = ChatClient(private_key="<key>", network="solana")
```

```go [Go]
// ⚠️ Coming Soon — Go SDK does not yet support Solana. Code below is an API preview.
// Go currently supports Base chain (EVM) only.

import jarvisclaw "github.com/api-jarvisclaw/go-sdk"

// EVM wallet — hex private key (0x...) → Base chain
client, _ := jarvisclaw.NewChatClient(jarvisclaw.WithPrivateKey("0x<evm-private-key>"))

// Solana wallet — bs58-encoded keypair → Solana mainnet (coming soon)
// SDK auto-detects chain from key format
client, _ := jarvisclaw.NewChatClient(jarvisclaw.WithPrivateKey("<base58-solana-keypair>"))
```

:::

## Full example

All client types work with Solana — chat, image, video, audio. Only the payment layer changes.

::: code-group

```python [Python]
# pip install jarvisclaw[solana]
from jarvisclaw import ChatClient, ImageClient, VideoClient

# Pass your Solana bs58 keypair — SDK detects Solana automatically
chat = ChatClient(private_key="<base58-solana-keypair>")
image = ImageClient(private_key="<base58-solana-keypair>")

# All endpoints work exactly the same — only the payment chain changes
response = chat.complete("Hello from Solana!")
print(response)

# Image generation — paid via Solana USDC (SPL)
img = image.generate("A cyberpunk city at dusk")
print(img.url)

# Check wallet address (shows Solana pubkey)
print(f"Solana wallet: {chat.address}")
```

```go [Go]
// ⚠️ Coming Soon — Go SDK does not yet support Solana. Code below is an API preview.
// Go currently supports Base chain (EVM) only.

package main

import (
    "context"
    "fmt"
    jarvisclaw "github.com/api-jarvisclaw/go-sdk"
)

func main() {
    ctx := context.Background()

    // Pass your Solana bs58 keypair — SDK detects Solana automatically
    chat, _ := jarvisclaw.NewChatClient(
        jarvisclaw.WithPrivateKey("<base58-solana-keypair>"),
    )

    // All endpoints work exactly the same — only the payment chain changes
    text, _ := chat.Complete(ctx, "Hello from Solana!")
    fmt.Println(text)

    // Image generation — paid via Solana USDC (SPL)
    imgClient, _ := jarvisclaw.NewImageClient(
        jarvisclaw.WithPrivateKey("<base58-solana-keypair>"),
    )
    img, _ := imgClient.Generate(ctx, "A cyberpunk city at dusk")
    fmt.Println(img.URL)

    // Check wallet address (shows Solana pubkey)
    fmt.Printf("Solana wallet: %s\n", chat.Address())
}
```

:::

::: warning Note: Rust toolchain
The solders library (Solana keypair signing) requires a Rust compiler during pip install. On most systems this is installed automatically. If the install fails, run: `curl --proto "=https" --tlsv1.2 -sSf https://sh.rustup.rs | sh`
:::

## Chain comparison

| Property | Base | Solana |
|----------|------|--------|
| Key format | `0x...` (hex) | base58 keypair |
| USDC type | ERC-20 | SPL |
| Confirmation time | ~2s | ~0.4s |
| Install command | `pip install jarvisclaw[agent]` | `pip install jarvisclaw[solana]` |

---

## ATA (Associated Token Account) Requirements

Solana SPL tokens (including USDC) require an **Associated Token Account** to exist on-chain before tokens can be transferred. This is different from EVM where any address can receive ERC-20 tokens without setup.

### What this means for x402

- Your Solana wallet must have an initialized USDC ATA before the x402 payment flow can work.
- The platform performs an ATA pre-check before attempting settlement. If no ATA exists, Solana is skipped and the system falls back to Base (if available).
- A failed ATA check does **not** consume gas or incur fees — it's a read-only RPC call.

### How to verify your ATA is ready

```python
from jarvisclaw import ChatClient

client = ChatClient(private_key="<base58-solana-keypair>")
balance = client.get_balance()
print(f"Solana USDC: ${balance:.6f}")
# If this returns a number (even 0), your ATA exists
```

### Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `transaction_simulation_failed` | ATA not initialized | Send any USDC to your wallet first |
| Balance shows 0 but ATA exists | Wallet funded with SOL only | Transfer USDC (SPL) to create the token account |
| Fallback to Base unexpectedly | Solana ATA check failed | Verify ATA exists via Solscan or `get_balance()` |

::: tip
If you use both chains, the platform automatically picks the one with sufficient balance. Fund both for maximum reliability.
:::
