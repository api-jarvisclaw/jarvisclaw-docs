# Compute API (Modal Sandbox)

Isolated code execution in secure cloud containers via Modal. Create sandboxes, execute arbitrary commands, manage lifecycle. Supports resource limits, network isolation, and automatic cleanup. Designed as a secure runtime for AI agent code execution.

**Base URL:** `https://api.jarvisclaw.ai/v1/marketplace/compute`

## Endpoints

| Method | Endpoint | Description | Price |
|--------|----------|-------------|-------|
| POST | `/sandbox/create` | Create a new isolated sandbox | $0.01 (CPU, ≤300s) |
| POST | `/sandbox/exec` | Execute a command in a sandbox | $0.001/request |
| POST | `/sandbox/status` | Get sandbox status | $0.001/request |
| POST | `/sandbox/terminate` | Terminate and cleanup | $0.001/request |

## Pricing

Two billing modes selected automatically by the requested timeout: short bursts pay a flat rate, long-lived sandboxes pay per hour.

### Burst — timeout ≤ 300s

Flat rate per `sandbox/create`, covers the full short-lived session. Lifecycle ops (`exec`, `status`, `terminate`) at $0.001/request.

| Config | Price | Resources |
|--------|-------|-----------|
| CPU | $0.01/sandbox | Up to 1 vCPU, 1 GiB RAM, 300s lifetime |
| GPU — T4 | $0.05/sandbox | Up to 8 vCPU, 32 GiB RAM, 300s lifetime |
| GPU — L4 | $0.08/sandbox | Up to 8 vCPU, 32 GiB RAM, 300s lifetime |
| GPU — A10G | $0.10/sandbox | Up to 8 vCPU, 32 GiB RAM, 300s lifetime |
| GPU — A100 | $0.20/sandbox | Up to 8 vCPU, 32 GiB RAM, 300s lifetime |
| GPU — H100 | $0.40/sandbox | Up to 8 vCPU, 32 GiB RAM, 300s lifetime |

### Long-lived — timeout > 300s, up to 24h

Per-hour rate × requested duration, billed upfront in one x402 settlement. No refund on early terminate (same as cloud-instance norms). Hours are exact — 90min on T4 = 1.5 × $1.50 = $2.25.

| Config | Per hour | Use cases |
|--------|----------|-----------|
| CPU (1 vCPU / 1 GiB) | $0.10 | Batch jobs, scrapers, schedulers |
| T4 (up to 8 vCPU / 32 GiB) | $1.50 | Light inference, small models |
| L4 (up to 8 vCPU / 32 GiB) | $2.00 | Mid-tier inference |
| A10G (up to 8 vCPU / 32 GiB) | $2.50 | Stable diffusion, 7B inference |
| A100 (up to 8 vCPU / 32 GiB) | $4.00 | Training, 13B–70B inference |
| H100 (up to 8 vCPU / 32 GiB) | $8.00 | Frontier training, low-latency 70B+ |

## POST /sandbox/create

Create a new isolated sandbox container.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | string | No | Docker image. Default: `python:3.11` |
| `timeout` | integer | No | Max sandbox lifetime in seconds. ≤300 = flat rate, >300 = per-hour billing. Default: `300`, Max: `86400` (24h) |

### Request

```json
{
  "image": "python:3.11",
  "timeout": 300
}
```

### Response

```json
{
  "sandbox_id": "sb-x8dagbSASXzZqYzSIO7tdV",
  "status": "running",
  "created_at": "2026-06-20T12:05:12.716280+00:00",
  "config": {
    "image": "python:3.11",
    "timeout": 300,
    "cpu": 1,
    "memory": 512,
    "gpu": null
  }
}
```

## POST /sandbox/exec

Run a command inside an existing sandbox.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sandbox_id` | string | Yes | Sandbox identifier |
| `command` | array | Yes | Command as array (e.g. `["python", "-c", "print(1)"]`) |

### Request

```json
{
  "sandbox_id": "sb-x8dagbSASXzZqYzSIO7tdV",
  "command": ["python", "-c", "import sys; print(sys.version)"]
}
```

### Response

```json
{
  "sandbox_id": "sb-x8dagbSASXzZqYzSIO7tdV",
  "stdout": "3.11.9 (main, Apr  2 2024, 08:25:04) [GCC 12.2.0]\n",
  "stderr": "",
  "returncode": 0
}
```

## POST /sandbox/status

Get current status and metadata of a sandbox.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sandbox_id` | string | Yes | Sandbox identifier |

### Request

```json
{
  "sandbox_id": "sb-x8dagbSASXzZqYzSIO7tdV"
}
```

### Response

```json
{
  "sandbox_id": "sb-x8dagbSASXzZqYzSIO7tdV",
  "status": "running",
  "returncode": null
}
```

## POST /sandbox/terminate

Immediately terminate a sandbox and release all resources.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sandbox_id` | string | Yes | Sandbox identifier |

### Request

```json
{
  "sandbox_id": "sb-x8dagbSASXzZqYzSIO7tdV"
}
```

### Response

```json
{
  "sandbox_id": "sb-x8dagbSASXzZqYzSIO7tdV",
  "status": "terminated"
}
```

## Errors

| HTTP Status | Code | Description |
|-------------|------|-------------|
| 404 | `sandbox_not_found` | The specified sandbox_id does not exist |
| 410 | `sandbox_terminated` | The sandbox has already been terminated |
| 408 | `sandbox_timeout` | The sandbox exceeded its timeout and was auto-terminated |
| 500 | `exec_failed` | Command execution failed due to an internal error |

## Code Examples

::: code-group

```bash [cURL]
# Create a sandbox
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/compute/sandbox/create \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"timeout": 300}'

# Execute a command
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/compute/sandbox/exec \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"sandbox_id": "sb_a1b2c3d4e5", "command": "python -c \"print(2+2)\""}'

# Check status
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/compute/sandbox/status \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"sandbox_id": "sb_a1b2c3d4e5"}'

# Terminate
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/compute/sandbox/terminate \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"sandbox_id": "sb_a1b2c3d4e5"}'
```

```python [Python (API Key)]
import requests

BASE = "https://api.jarvisclaw.ai/v1/marketplace/compute/sandbox"
HEADERS = {
    "Authorization": "Bearer sk-your-api-key",
    "Content-Type": "application/json",
}

# Create a sandbox
resp = requests.post(f"{BASE}/create", headers=HEADERS, json={
    "timeout": 300,
})
sandbox_id = resp.json()["sandbox_id"]
print(f"Created sandbox: {sandbox_id}")

# Execute a command
resp = requests.post(f"{BASE}/exec", headers=HEADERS, json={
    "sandbox_id": sandbox_id,
    "command": "python -c \"import math; print(math.pi)\"",
})
print(resp.json()["stdout"])

# Check status
resp = requests.post(f"{BASE}/status", headers=HEADERS, json={
    "sandbox_id": sandbox_id,
})
print(resp.json()["status"])

# Terminate when done
requests.post(f"{BASE}/terminate", headers=HEADERS, json={
    "sandbox_id": sandbox_id,
})
```

```python [Python (x402 Agent)]
from jarvisclaw import MarketplaceClient

# --- Option A: Base chain (EVM) ---
# Hex private key -> USDC on Base (Chain ID 8453)
client = MarketplaceClient(private_key="0x<evm-private-key>")

# --- Option B: Solana ---
# Base58 keypair -> USDC SPL on Solana mainnet
# client = MarketplaceClient(private_key="<solana-bs58-keypair>")

# SDK auto-detects chain from key format - no config needed

# Create a sandbox
sandbox = client.call("compute", "/sandbox/create", method="POST", json={
    "timeout": 300,
})
print(f"Sandbox ID: {sandbox['sandbox_id']}")

# Execute commands
result = client.call("compute", "/sandbox/exec", method="POST", json={
    "sandbox_id": sandbox["sandbox_id"],
    "command": "pip install numpy && python -c \"import numpy; print(numpy.__version__)\"",
})
print(result["stdout"])

result = client.call("compute", "/sandbox/exec", method="POST", json={
    "sandbox_id": sandbox["sandbox_id"],
    "command": "python -c \"import numpy as np; print(np.random.rand(3))\"",
})
print(result["stdout"])

# Check status
status = client.call("compute", "/sandbox/status", method="POST", json={
    "sandbox_id": sandbox["sandbox_id"],
})
print(f"Commands run: {status['commands_executed']}")

# Terminate
client.call("compute", "/sandbox/terminate", method="POST", json={
    "sandbox_id": sandbox["sandbox_id"],
})
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

    // Create a sandbox
    sandbox, _ := mc.Post(ctx, "compute", "/sandbox/create", map[string]interface{}{
        "timeout": 300,
    })
    fmt.Printf("Sandbox ID: %s\n", sandbox["sandbox_id"])

    // Execute a command
    result, _ := mc.Post(ctx, "compute", "/sandbox/exec", map[string]interface{}{
        "sandbox_id": sandbox["sandbox_id"],
        "command":    "python -c \"print('hello')\"",
    })
    fmt.Printf("Output: %s\n", result["stdout"])

    // Check status
    status, _ := mc.Post(ctx, "compute", "/sandbox/status", map[string]interface{}{
        "sandbox_id": sandbox["sandbox_id"],
    })
    fmt.Printf("Status: %s, Commands: %v\n", status["status"], status["commands_executed"])

    // Terminate
    mc.Post(ctx, "compute", "/sandbox/terminate", map[string]interface{}{
        "sandbox_id": sandbox["sandbox_id"],
    })
}
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

    // x402 Agent wallet - pays per-call via USDC on Base (Chain ID 8453)
    mc, _ := jc.NewMarketplaceClient(jc.WithPrivateKey("0x<evm-private-key>"))

    // Create a sandbox
    sandbox, _ := mc.Post(ctx, "compute", "/sandbox/create", map[string]interface{}{
        "timeout": 300,
    })
    fmt.Printf("Sandbox ID: %s\n", sandbox["sandbox_id"])

    // Execute commands
    result, _ := mc.Post(ctx, "compute", "/sandbox/exec", map[string]interface{}{
        "sandbox_id": sandbox["sandbox_id"],
        "command":    "python -c \"print('agent execution')\"",
    })
    fmt.Printf("Output: %s\n", result["stdout"])

    // Terminate when done
    mc.Post(ctx, "compute", "/sandbox/terminate", map[string]interface{}{
        "sandbox_id": sandbox["sandbox_id"],
    })
}
```

:::

## Limitations

- **24h max timeout** — sandboxes auto-terminate after the configured timeout (max 86400s)
- **Flat-rate for short tasks** — ≤300s gets flat CPU $0.01, longer sessions billed per hour
- **No persistent storage** — all data is lost when the sandbox terminates
- **No inbound connections** — sandboxes cannot receive network traffic from outside
- **10MB max payload** — request and response bodies are capped at 10MB
- **Outbound HTTP allowed** — sandboxes can make outbound requests (pip install, curl, etc.)
