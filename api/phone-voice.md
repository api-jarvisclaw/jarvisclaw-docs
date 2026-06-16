# Phone & Voice

Initiate AI-powered voice calls, carrier lookups, and fraud detection.

## Base URL

```
/v1/marketplace/phone/*
```

## Endpoints

| Method | Endpoint | Description | Price |
|--------|----------|-------------|-------|
| POST | `/v1/marketplace/phone/voice/call` | Initiate AI voice call | $0.54 |
| GET | `/v1/marketplace/phone/voice/call/:call_id` | Get call transcript | — |
| POST | `/v1/marketplace/phone/lookup` | Carrier identification | $0.01 |
| POST | `/v1/marketplace/phone/lookup/fraud` | Fraud risk assessment | $0.05 |
| POST | `/v1/marketplace/phone/numbers/buy` | Lease a phone number | $5/month |

## Initiate Voice Call

`POST /v1/marketplace/phone/voice/call`

Place an outbound AI voice call. The AI agent handles the conversation using the provided system prompt.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `to` | string | Yes | Destination phone number (E.164 format, e.g., `+14155551234`) |
| `from` | string | No | Caller ID number (must be a leased number) |
| `system_prompt` | string | Yes | Instructions for the AI voice agent |
| `voice` | string | No | Voice preset. Default: `nova` |
| `max_duration` | integer | No | Max call duration in seconds. Default: `300` |
| `webhook_url` | string | No | URL for real-time call events |

### Response

```json
{
  "call_id": "call_abc123",
  "status": "initiated",
  "to": "+14155551234",
  "created_at": "2025-06-01T12:00:00Z"
}
```

## Get Call Transcript

`GET /v1/marketplace/phone/voice/call/:call_id`

Retrieve the full transcript and metadata for a completed call.

### Response

```json
{
  "call_id": "call_abc123",
  "status": "completed",
  "duration_seconds": 45,
  "to": "+14155551234",
  "transcript": [
    {"role": "assistant", "content": "Hello, this is the appointment reminder service..."},
    {"role": "user", "content": "Yes, I'd like to confirm my appointment."},
    {"role": "assistant", "content": "Great, your appointment is confirmed for Tuesday at 2 PM."}
  ],
  "created_at": "2025-06-01T12:00:00Z",
  "ended_at": "2025-06-01T12:00:45Z"
}
```

## Carrier Lookup

`POST /v1/marketplace/phone/lookup`

Identify the carrier and line type for a phone number.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `phone_number` | string | Yes | Phone number in E.164 format |

### Response

```json
{
  "phone_number": "+14155551234",
  "carrier": "T-Mobile",
  "line_type": "mobile",
  "country": "US"
}
```

## Fraud Risk Assessment

`POST /v1/marketplace/phone/lookup/fraud`

Assess fraud risk for a phone number.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `phone_number` | string | Yes | Phone number in E.164 format |

### Response

```json
{
  "phone_number": "+14155551234",
  "risk_score": 15,
  "risk_level": "low",
  "flags": [],
  "carrier": "T-Mobile",
  "line_type": "mobile"
}
```

Risk levels: `low`, `medium`, `high`, `critical`

## Lease Phone Number

`POST /v1/marketplace/phone/numbers/buy`

Lease a phone number for outbound calling.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `country` | string | Yes | ISO country code (e.g., `US`) |
| `area_code` | string | No | Preferred area code |
| `capabilities` | array | No | Required capabilities: `voice`, `sms` |

### Response

```json
{
  "number": "+14155559876",
  "country": "US",
  "capabilities": ["voice"],
  "monthly_cost": 5.00,
  "expires_at": "2025-07-01T12:00:00Z"
}
```

## Examples

::: code-group

```python [Python]
import requests

BASE = "https://api.jarvisclaw.ai/v1/marketplace/phone"
HEADERS = {
    "Authorization": "Bearer sk-your-api-key",
    "Content-Type": "application/json",
}

# Initiate an AI voice call
resp = requests.post(f"{BASE}/voice/call", headers=HEADERS, json={
    "to": "+14155551234",
    "system_prompt": "You are an appointment reminder assistant. Confirm the user's appointment for Tuesday at 2 PM.",
    "voice": "nova",
    "max_duration": 120,
})
call = resp.json()
print(f"Call ID: {call['call_id']}")

# Get transcript after call completes
resp = requests.get(
    f"{BASE}/voice/call/{call['call_id']}",
    headers=HEADERS,
)
transcript = resp.json()
for turn in transcript["transcript"]:
    print(f"{turn['role']}: {turn['content']}")

# Carrier lookup
resp = requests.post(f"{BASE}/lookup", headers=HEADERS, json={
    "phone_number": "+14155551234",
})
print(resp.json())
```

```bash [cURL]
# Initiate a voice call
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/phone/voice/call \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+14155551234",
    "system_prompt": "You are a friendly appointment reminder. Confirm Tuesday 2 PM.",
    "voice": "nova"
  }'

# Get transcript
curl https://api.jarvisclaw.ai/v1/marketplace/phone/voice/call/call_abc123 \
  -H "Authorization: Bearer sk-your-api-key"

# Fraud check
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/phone/lookup/fraud \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+14155551234"}'
```

:::

## Notes

- Outbound calls only — inbound call handling is not supported
- Real-time transcripts available via webhook during the call
- Calls are recorded and transcribed automatically
- Maximum call duration: 5 minutes (300 seconds)
- Phone numbers must be in E.164 format (e.g., `+1` prefix for US)
- Leased numbers renew automatically unless cancelled
