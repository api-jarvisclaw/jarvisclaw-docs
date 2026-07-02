# API Reference

Base URL: `https://api.jarvisclaw.ai/v1`

Authentication: `Authorization: Bearer sk-your-api-key` or `PAYMENT-SIGNATURE` (x402)

## AI Models

| API | Endpoint | Billing |
|-----|----------|---------|
| [Responses API](/api/responses) | POST `/v1/responses` | Per token |
| [Anthropic Messages](/api/anthropic-messages) | POST `/v1/messages` | Per token |
| [Chat Completions](/api/chat-completions) | POST `/v1/chat/completions` | Per token |
| [Image Generation](/api/image-generation) | POST `/v1/images/generations` | Per image |
| [Video Generation](/api/video-generation) | POST `/v1/videos/generations` | Per video |
| [Music Generation](/api/music-generation) | POST `/v1/audio/generations` | Per track |
| [Audio & TTS](/api/audio) | POST `/v1/audio/speech` | Per token |
| [Web Search](/api/web-search) | POST `/v1/search` | Per call |

## Marketplace Services

| API | Endpoint | Billing |
|-----|----------|---------|
| [Prediction Markets](/api/prediction-markets) | `/v1/marketplace/prediction/*` | Per call |
| [DEX Trading (0x)](/api/dex-trading) | `/v1/marketplace/dex/*` | Free |
| [Compute (Sandbox)](/api/compute) | `/v1/marketplace/compute/*` | Per call |
| [Crypto Data (Surf)](/api/crypto-data) | `/v1/marketplace/surf/*` | Per call |
| [Phone & Voice](/api/phone-voice) | `/v1/marketplace/phone/*` | Per call |
| [Trading Markets](/api/trading-markets) | `/v1/marketplace/markets/*` | Per call |
| [RealFace & Portrait](/api/realface) | `/v1/marketplace/realface/*` | Per call |

## Reference

| Page | Description |
|------|-------------|
| [Errors](/api/errors) | Error codes and handling |
| [Models](/models) | Available models list |
| [Security](/security) | Auth, encryption, rate limiting |
