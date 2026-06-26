# Phone & Voice API

AI-powered outbound voice calls (Bland.ai) and wallet-owned phone numbers (Twilio). Make conversational AI calls with real-time transcripts, buy/manage dedicated US/CA numbers, and perform carrier/fraud lookups. Outbound only, no SMS.

**Base URLs:**
- Phone numbers & lookups: `https://api.jarvisclaw.ai/v1/marketplace/phone`
- Voice calls: `https://api.jarvisclaw.ai/v1/marketplace/voice`

## Authentication

Both methods are supported — all requests settle via x402 on-chain:

| Method | Header | Description |
|--------|--------|-------------|
| API Key | `Authorization: Bearer sk-...` | Platform signs x402 from your HD wallet automatically |
| Private Key (x402) | Automatic via SDK | Agent signs x402 directly from its own wallet |

See [Agent Payments (x402)](/x402) for full details on how both methods work.

## Pricing

| Endpoint | Price | Description |
|----------|-------|-------------|
| POST `/v1/marketplace/voice/call` | $0.54/call | Initiate AI voice call (max 30 min) |
| GET `/v1/marketplace/voice/call/:call_id` | Free | Retrieve call status/transcript |
| POST `/v1/marketplace/phone/numbers/buy` | $5.00/number | Lease a phone number (30-day) |
| POST `/v1/marketplace/phone/numbers/renew` | $5.00/number | Extend lease by 30 days |
| POST `/v1/marketplace/phone/numbers/list` | $0.001/request | List owned numbers |
| POST `/v1/marketplace/phone/numbers/release` | Free | Release a number |
| POST `/v1/marketplace/phone/lookup` | $0.01/request | Carrier identification |
| POST `/v1/marketplace/phone/lookup/fraud` | $0.05/request | Fraud risk + SIM swap detection |

## Endpoints

### POST /v1/marketplace/voice/call

Initiate an outbound AI voice call. The AI agent handles the conversation using the provided task/system prompt. Powered by Bland.ai. Requires a leased phone number as caller ID.

::: tip Quick Start Cost
Total for first call: $5.54 USDC ($5.00 for a 30-day number + $0.54 per call). Polling for the transcript is free.
:::

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `to` | string | Yes | Destination phone number (E.164 format, e.g., `+14155551234`) |
| `from` | string | Yes | Caller ID — must be a number leased via `/phone/numbers/buy` and owned by your wallet |
| `task` | string | Yes | Instructions for the AI voice agent (plain English system prompt) |
| `voice` | string | No | Voice preset (e.g., `maya`, `josh`). Default: `maya` |
| `max_duration` | integer | No | Max call duration in minutes. Default: `5`, max: `30` |
| `first_sentence` | string | No | Override the AI's opening line |
| `wait_for_greeting` | boolean | No | Wait for callee to speak first. Default: `true` |

#### Request Example

```json
{
  "to": "+12025551234",
  "from": "+14155551234",
  "task": "Hi, this is Maya from JarvisClaw. Confirm tomorrow at 3pm and ask the recipient to press 1 to confirm or 2 to reschedule. Keep it under 60 seconds.",
  "voice": "maya",
  "max_duration": 5
}
```

#### Response Example

```json
{
  "call_id": "0721a3f8-9ae6-...",
  "status": "success",
  "poll_url": "https://api.jarvisclaw.ai/v1/marketplace/voice/call/0721a3f8-...",
  "message": "Call initiated. Poll poll_url for status, transcript, and recording."
}
```

#### Error: No Owned Number

If `from` is not a number owned by your wallet:

```json
{
  "error": "Forbidden",
  "message": "You do not own +14155551234. Your wallet (0x...) doesn't own any active numbers. Buy one at POST /api/v1/phone/numbers/buy."
}
```

---

### GET /v1/marketplace/voice/call/:call_id

Retrieve the full transcript, status, and metadata for a completed call. No payment required.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `call_id` | string | Yes | Call ID (path parameter) |

#### Response Example

```json
{
  "status": "completed",
  "call_length": 0.75,
  "answered_by": "human",
  "from": "+14155551234",
  "to": "+12025551234",
  "concatenated_transcript": "AI: Hi, this is Maya from JarvisClaw...\nHuman: Yes, hello?...",
  "recording_url": "https://..."
}
```

Call statuses: `initiated`, `ringing`, `in_progress`, `completed`, `failed`, `no_answer`, `busy`

---

### POST /lookup

Identify the carrier and line type for a phone number.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `phoneNumber` | string | Yes | Phone number in E.164 format |

#### Request Example

```json
{
  "phoneNumber": "+14155551234"
}
```

#### Response Example

```json
{
  "phone_number": "+14155551234",
  "calling_country_code": "1",
  "country_code": "US",
  "national_format": "(415) 555-1234",
  "line_type_intelligence": {
    "carrier_name": "T-Mobile",
    "type": "mobile",
    "mobile_country_code": "310",
    "mobile_network_code": "260"
  },
  "caller_name": null,
  "sim_swap": null
}
```

---

### POST /lookup/fraud

Assess fraud risk and identify suspicious indicators for a phone number.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `phoneNumber` | string | Yes | Phone number in E.164 format |

#### Request Example

```json
{
  "phoneNumber": "+14155551234"
}
```

#### Response Example

```json
{
  "phone_number": "+14155551234",
  "calling_country_code": "1",
  "country_code": "US",
  "national_format": "(415) 555-1234",
  "line_type_intelligence": {
    "carrier_name": "T-Mobile",
    "type": "mobile"
  },
  "call_forwarding": {
    "call_forwarding_enabled": false
  },
  "sim_swap": {
    "last_sim_swap": null,
    "swapped_in_period": false
  }
}
```

Risk levels: `low` (0-25), `medium` (26-50), `high` (51-75), `critical` (76-100)

---

### POST /numbers/buy

Lease a dedicated phone number for use as a caller ID on outbound calls.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `country` | string | Yes | ISO country code (`US` or `CA`) |
| `areaCode` | string | No | Preferred area code (e.g., `415`) |

#### Request Example

```json
{
  "country": "US",
  "areaCode": "415"
}
```

#### Response Example

```json
{
  "phone_number": "+14155559876",
  "expires_at": "2026-07-20T00:00:00.000Z",
  "chain": "base",
  "message": "Number provisioned for 30 days..."
}
```

---

### POST /numbers/list

List all phone numbers currently leased to your account.

#### Request Example

```json
{}
```

#### Response Example

```json
{
  "numbers": [],
  "count": 0
}
```

## Errors

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 400 | `invalid_phone_number` | Phone number is not valid E.164 format |
| 404 | `number_not_owned` | The `from` number is not leased to your account |
| 404 | `call_not_found` | No call found with the specified `call_id` |
| 409 | `number_unavailable` | Requested number or area code has no availability |
| 500 | `call_failed` | Voice call could not be connected (carrier/network issue) |

### Error Response Format

```json
{
  "error": {
    "code": "invalid_phone_number",
    "message": "The phone number '+1415555' is not valid E.164 format. Expected format: +14155551234"
  }
}
```

## Code Examples

::: code-group

```bash [cURL]
# 1. Buy a phone number ($5.00)
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/phone/numbers/buy \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"country": "US", "areaCode": "415"}'

# 2. Initiate a voice call ($0.54) — note: /v1/marketplace/voice/ (separate service)
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/voice/call \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+12025551234",
    "from": "+14155551234",
    "task": "Confirm the dental appointment for Tuesday at 2 PM. Keep it under 60 seconds.",
    "voice": "maya",
    "max_duration": 5
  }'

# 3. Get call transcript (free)
curl https://api.jarvisclaw.ai/v1/marketplace/voice/call/0721a3f8-9ae6-... \
  -H "Authorization: Bearer sk-your-api-key"

# Carrier lookup
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/phone/lookup \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"phoneNumber": "+14155551234"}'

# Fraud risk check
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/phone/lookup/fraud \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"phoneNumber": "+14155551234"}'

# List owned numbers
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/phone/numbers/list \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{}'
```

```python [Python (API Key)]
import requests

PHONE_BASE = "https://api.jarvisclaw.ai/v1/marketplace/phone"
VOICE_BASE = "https://api.jarvisclaw.ai/v1/marketplace/voice"
HEADERS = {
    "Authorization": "Bearer sk-your-api-key",
    "Content-Type": "application/json",
}

# 1. Buy a number
resp = requests.post(f"{PHONE_BASE}/numbers/buy", headers=HEADERS, json={
    "country": "US",
    "areaCode": "415",
})
number = resp.json()
print(f"Leased: {number['phone_number']}, expires: {number['expires_at']}")

# 2. Initiate an AI voice call (separate service: /marketplace/voice)
resp = requests.post(f"{VOICE_BASE}/call", headers=HEADERS, json={
    "to": "+12025551234",
    "from": number["phone_number"],
    "task": "Confirm the dental appointment for Tuesday at 2 PM.",
    "voice": "maya",
    "max_duration": 5,
})
call = resp.json()
print(f"Call initiated: {call['call_id']}")

# 3. Poll transcript (free)
resp = requests.get(f"{VOICE_BASE}/call/{call['call_id']}", headers=HEADERS)
result = resp.json()
print(f"Status: {result['status']}, Duration: {result.get('call_length')} min")
print(f"Answered by: {result.get('answered_by')}")
print(f"Transcript: {result.get('concatenated_transcript', '')[:200]}")

# Carrier lookup
resp = requests.post(f"{PHONE_BASE}/lookup", headers=HEADERS, json={
    "phoneNumber": "+14155551234",
})
info = resp.json()
lt = info.get("line_type_intelligence", {})
print(f"Carrier: {lt.get('carrier_name')}, Type: {lt.get('type')}")

# Fraud risk assessment
resp = requests.post(f"{PHONE_BASE}/lookup/fraud", headers=HEADERS, json={
    "phoneNumber": "+14155551234",
})
risk = resp.json()
print(f"SIM swap: {risk.get('sim_swap')}")
print(f"Call forwarding: {risk.get('call_forwarding')}")

# List owned numbers
resp = requests.post(f"{PHONE_BASE}/numbers/list", headers=HEADERS, json={})
print(f"Numbers: {resp.json()}")
```

```python [Python (x402 Agent)]
from jarvisclaw import MarketplaceClient

# x402 Agent wallet — pays per-call via USDC
client = MarketplaceClient(private_key="0x<evm-private-key>")

# 1. Buy a number
number = client.call("phone", "/numbers/buy", method="POST", json={
    "country": "US",
    "areaCode": "415",
})
print(f"Leased: {number['phone_number']}")

# 2. Voice call (note: separate 'voice' service)
call = client.call("voice", "/call", method="POST", json={
    "to": "+12025551234",
    "from": number["phone_number"],
    "task": "Confirm appointment for Tuesday at 2 PM.",
    "voice": "maya",
    "max_duration": 5,
})
print(f"Call initiated: {call['call_id']}")

# 3. Get transcript (free)
transcript = client.call("voice", f"/call/{call['call_id']}")
print(f"Status: {transcript['status']}")
print(f"Transcript: {transcript.get('concatenated_transcript', '')[:200]}")

# Carrier lookup
info = client.call("phone", "/lookup", method="POST", json={
    "phoneNumber": "+14155551234",
})
lt = info.get("line_type_intelligence", {})
print(f"Carrier: {lt.get('carrier_name')}, Type: {lt.get('type')}")
print(f"Risk: {risk['risk_level']} (score: {risk['risk_score']})")

# Buy a number
number = client.call("phone", "/numbers/buy", method="POST", json={
    "country": "US",
    "area_code": "415",
})
print(f"Leased: {number['number']}")

# List owned numbers
numbers = client.call("phone", "/numbers/list", method="POST", json={})
for num in numbers["numbers"]:
    print(f"  {num['number']} — expires {num['expires_at']}")
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

    // 1. Buy a number
    number, _ := mc.Post(ctx, "phone", "/numbers/buy", map[string]interface{}{
        "country":  "US",
        "areaCode": "415",
    })
    fmt.Printf("Leased: %s\n", number["phone_number"])

    // 2. Voice call (note: 'voice' service, not 'phone')
    call, _ := mc.Post(ctx, "voice", "/call", map[string]interface{}{
        "to":           "+12025551234",
        "from":         number["phone_number"],
        "task":         "Confirm dental appointment Tuesday at 2 PM.",
        "voice":        "maya",
        "max_duration": 5,
    })
    fmt.Printf("Call initiated: %s\n", call["call_id"])

    // 3. Get transcript (free)
    transcript, _ := mc.Get(ctx, "voice", fmt.Sprintf("/call/%s", call["call_id"]))
    fmt.Printf("Status: %s, Answered by: %s\n", transcript["status"], transcript["answered_by"])

    // Carrier lookup
    info, _ := mc.Post(ctx, "phone", "/lookup", map[string]interface{}{
        "phoneNumber": "+14155551234",
    })
    fmt.Printf("Country: %s\n", info["country_code"])
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

    // x402 Agent wallet — pays per-call via USDC on Base
    mc, _ := jc.NewMarketplaceClient(jc.WithPrivateKey("0x<evm-private-key>"))

    // 1. Buy a number
    number, _ := mc.Post(ctx, "phone", "/numbers/buy", map[string]interface{}{
        "country":  "US",
        "areaCode": "415",
    })
    fmt.Printf("Leased: %s\n", number["phone_number"])

    // 2. Voice call ('voice' service)
    call, _ := mc.Post(ctx, "voice", "/call", map[string]interface{}{
        "to":           "+12025551234",
        "from":         number["phone_number"],
        "task":         "Confirm dental appointment Tuesday at 2 PM.",
        "voice":        "maya",
        "max_duration": 5,
    })
    fmt.Printf("Call initiated: %s\n", call["call_id"])

    // 3. Get transcript (free)
    transcript, _ := mc.Get(ctx, "voice", fmt.Sprintf("/call/%s", call["call_id"]))
    fmt.Printf("Status: %s\n", transcript["status"])
}
```
```

:::

## Limitations

- **Outbound only** — inbound call handling and receiving calls is not supported
- **No SMS** — phone numbers are voice-only, SMS is not available
- **30-minute max call duration** — calls are automatically terminated at 1800 seconds
- **US/CA default** — numbers outside US and Canada require KYC verification
- **English only** — voice AI currently supports English language conversations only
- **30-day lease** — phone numbers auto-renew monthly unless cancelled
- **E.164 format required** — all phone numbers must include country code (e.g., `+14155551234`)
- **Caller ID** — the `from` field must be a number you've leased, or it will be omitted (calls show as unknown)
