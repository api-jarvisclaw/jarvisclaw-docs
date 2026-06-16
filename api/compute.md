# Compute (Modal Sandbox)

Run code in ephemeral cloud sandboxes. Each sandbox provides an isolated Linux container with CPU resources for short-lived tasks.

## Endpoints

| Method | Endpoint | Description | Price |
|--------|----------|-------------|-------|
| POST | `/v1/marketplace/compute/sandbox/create` | Create a new sandbox | $0.01 |
| POST | `/v1/marketplace/compute/sandbox/exec` | Execute a command | $0.001 |
| POST | `/v1/marketplace/compute/sandbox/status` | Check sandbox status | $0.001 |
| POST | `/v1/marketplace/compute/sandbox/terminate` | Terminate and cleanup | $0.001 |

## Features

- 5-minute maximum timeout per sandbox
- CPU-only execution (no GPU)
- No persistent storage — data is lost on termination
- Isolated Linux environment per sandbox
- Support for Python, Node.js, Bash, and common CLI tools

## Create Sandbox

`POST /v1/marketplace/compute/sandbox/create`

Creates a new ephemeral sandbox container.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | string | No | Container image. Default: `python:3.11-slim` |
| `timeout` | integer | No | Timeout in seconds (max 300). Default: `300` |

### Response

```json
{
  "sandbox_id": "sb_abc123xyz",
  "status": "running",
  "created_at": "2025-06-01T12:00:00Z",
  "expires_at": "2025-06-01T12:05:00Z"
}
```

## Execute Command

`POST /v1/marketplace/compute/sandbox/exec`

Run a command inside an existing sandbox.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sandbox_id` | string | Yes | Sandbox identifier |
| `command` | string | Yes | Shell command to execute |
| `timeout` | integer | No | Command timeout in seconds (max 60). Default: `30` |

### Response

```json
{
  "exit_code": 0,
  "stdout": "Hello, World!\n",
  "stderr": "",
  "duration_ms": 42
}
```

## Check Status

`POST /v1/marketplace/compute/sandbox/status`

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sandbox_id` | string | Yes | Sandbox identifier |

### Response

```json
{
  "sandbox_id": "sb_abc123xyz",
  "status": "running",
  "created_at": "2025-06-01T12:00:00Z",
  "expires_at": "2025-06-01T12:05:00Z",
  "commands_executed": 3
}
```

## Terminate Sandbox

`POST /v1/marketplace/compute/sandbox/terminate`

Immediately terminate a sandbox and release resources.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sandbox_id` | string | Yes | Sandbox identifier |

### Response

```json
{
  "sandbox_id": "sb_abc123xyz",
  "status": "terminated"
}
```

## Examples

::: code-group

```python [Python]
import requests

BASE = "https://api.jarvisclaw.ai/v1/marketplace/compute/sandbox"
HEADERS = {
    "Authorization": "Bearer sk-your-api-key",
    "Content-Type": "application/json",
}

# Create a sandbox
resp = requests.post(f"{BASE}/create", headers=HEADERS, json={
    "image": "python:3.11-slim",
    "timeout": 120,
})
sandbox_id = resp.json()["sandbox_id"]

# Execute a command
resp = requests.post(f"{BASE}/exec", headers=HEADERS, json={
    "sandbox_id": sandbox_id,
    "command": "python -c \"print('Hello from sandbox!')\"",
})
print(resp.json()["stdout"])

# Terminate when done
requests.post(f"{BASE}/terminate", headers=HEADERS, json={
    "sandbox_id": sandbox_id,
})
```

```bash [cURL]
# Create a sandbox
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/compute/sandbox/create \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"image": "python:3.11-slim", "timeout": 120}'

# Execute a command
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/compute/sandbox/exec \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"sandbox_id": "sb_abc123xyz", "command": "python -c \"print(2+2)\""}'

# Terminate
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/compute/sandbox/terminate \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"sandbox_id": "sb_abc123xyz"}'
```

:::

## Notes

- Sandboxes auto-terminate after the configured timeout (max 5 minutes)
- No network egress from sandboxes — they cannot make outbound requests
- Stdout/stderr output is capped at 1 MB per command execution
- Concurrent sandbox limit: 5 per account
