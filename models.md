# Available Models

81 models across 13 providers. Live pricing at [api.jarvisclaw.ai/pricing](https://api.jarvisclaw.ai/pricing).

## Smart Routing

| Route | Description |
|-------|-------------|
| `auto` | Best overall model (balances quality/cost/speed) |
| `auto/premium` | Highest quality available |
| `auto/eco` | Cheapest capable model |
| `auto/free` | Free models only (Nvidia hosted) |
| `auto/image` | Best image generation model |
| `auto/video` | Best video generation model |
| `auto/tts` | Best text-to-speech model |
| `auto/music` | Best music generation model |
| `auto/search` | Web search with citations |

## Free Models (Nvidia Hosted)

Unlimited usage, no cost.

| Model | Context | Tags |
|-------|---------|------|
| `nvidia/qwen3.5-122b-a10b` | 131K | chat, reasoning, coding |
| `nvidia/qwen3-next-80b-a3b-instruct` | 262K | chat, reasoning, coding |
| `nvidia/step-3.7-flash` | 131K | chat, reasoning |
| `nvidia/nemotron-nano-12b-v2-vl` | 131K | chat, reasoning, vision |
| `nvidia/seed-oss-36b` | 131K | chat, coding |
| `nvidia/mistral-large-3-675b` | 131K | chat, reasoning, coding |
| `nvidia/llama-4-maverick` | 131K | chat, reasoning, coding |
| `nvidia/nemotron-nano-9b-v2` | 131K | chat, reasoning |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` | 256K | chat, reasoning, vision |
| `nvidia/mistral-nemotron` | 131K | chat, coding |

## Chat & Reasoning Models

Pricing uses a ratio system where ratio × $2/M tokens = input price, ratio × $2/M × 3 = output price (approximately).

| Model | Context | Ratio | Tags |
|-------|---------|-------|------|
| `openai/gpt-5.5` | 1050K | 2.5 | chat, reasoning, coding, vision |
| `openai/gpt-5.4-pro` | 1050K | 15 | chat, reasoning, coding, vision |
| `openai/gpt-5.4` | 1050K | 1.25 | chat, reasoning, coding, vision |
| `openai/gpt-5.4-mini` | 400K | 0.375 | chat, coding, vision |
| `openai/gpt-5.4-nano` | 1050K | 0.1 | chat |
| `openai/gpt-5.3-codex` | 400K | 0.875 | coding, reasoning, chat |
| `openai/gpt-5.3` | 128K | 0.875 | chat, reasoning, coding, vision |
| `openai/gpt-5.2-pro` | 400K | 10.5 | chat, reasoning, coding, vision |
| `openai/gpt-5.2` | 400K | 0.875 | chat, reasoning, coding, vision |
| `openai/gpt-5-mini` | 200K | 0.125 | chat, coding |
| `openai/gpt-4.1` | 128K | 1 | chat, coding, vision |
| `openai/gpt-4.1-mini` | 128K | 0.2 | chat, coding |
| `openai/gpt-4.1-nano` | 128K | 0.05 | chat |
| `openai/gpt-4o` | 128K | 1.25 | chat, coding, vision |
| `openai/gpt-4o-mini` | 128K | 0.075 | chat, coding |
| `openai/o3` | 200K | 1 | chat, reasoning, coding |
| `openai/o3-mini` | 128K | 0.55 | chat, reasoning, coding |
| `openai/o1` | 200K | 7.5 | chat, reasoning, coding |
| `openai/o4-mini` | 128K | 0.55 | reasoning, coding |
| `anthropic/claude-opus-4.8` | 1000K | 2.5 | chat, coding, reasoning, vision |
| `anthropic/claude-opus-4.7` | 1000K | 2.5 | chat, coding, reasoning, vision |
| `anthropic/claude-opus-4.5` | 200K | 2.5 | chat, coding, reasoning, vision |
| `anthropic/claude-sonnet-4.6` | 200K | 1.5 | chat, coding, reasoning |
| `anthropic/claude-sonnet-4.5` | 200K | 1.5 | chat, coding, reasoning, vision |
| `anthropic/claude-haiku-4.5` | 200K | 0.5 | chat, coding |
| `google/gemini-3.5-flash` | 1048K | 0.25 | chat, reasoning, coding, vision |
| `google/gemini-3.1-pro` | 1048K | 1 | chat, reasoning, coding, vision |
| `google/gemini-3.1-flash-lite` | 1048K | 0.125 | chat, reasoning |
| `google/gemini-3-flash-preview` | 1048K | 0.25 | chat, reasoning, coding, vision |
| `google/gemini-2.5-pro` | 1048K | 0.625 | chat, reasoning, coding, vision |
| `google/gemini-2.5-flash` | 1048K | 0.15 | chat, coding, vision |
| `google/gemini-2.5-flash-lite` | 1048K | 0.05 | chat |
| `deepseek/deepseek-chat` | 1048K | 0.1 | chat, coding |
| `deepseek/deepseek-reasoner` | 1048K | 0.1 | chat, reasoning, coding |
| `deepseek/deepseek-v4-pro` | 1048K | 0.2175 | chat, reasoning, coding |
| `xai/grok-4.3` | 1000K | 0.75 | reasoning, coding, vision, chat |
| `xai/grok-build-0.1` | 256K | 0.75 | coding, chat |
| `moonshot/kimi-k2.7` | 262K | 0.475 | chat, reasoning, coding, vision |
| `minimax/minimax-m3` | 1048K | 0.15 | chat, reasoning, coding |
| `minimax/minimax-m2.7` | 204K | 0.15 | chat, reasoning, coding |
| `zai/glm-5.2` | 1000K | 0.7 | chat, reasoning, coding |
| `zai/glm-5.1` | 200K | 0.7 | chat, reasoning, coding |
| `zai/glm-5` | 200K | 0.3 | chat, reasoning, coding |
| `zai/glm-5-turbo` | 200K | 0.6 | chat, reasoning |

## Image Generation Models

Flat per-image pricing.

| Model | Price/image | Notes |
|-------|-------------|-------|
| `openai/gpt-image-1` | $0.02 | Standard quality |
| `openai/gpt-image-2` | $0.06 | Higher quality |
| `google/nano-banana` | $0.05 | Artistic generation |
| `google/nano-banana-pro` | $0.10 | Premium quality |
| `zai/cogview-4` | $0.015 | Budget option |
| `xai/grok-imagine-image` | $0.02 | xAI generation |
| `xai/grok-imagine-image-pro` | $0.07 | xAI premium |

## Video Generation Models

Flat per-video pricing.

| Model | Price/5s clip | Notes |
|-------|---------------|-------|
| `bytedance/seedance-2.0` | $0.319 | Highest quality, supports RealFace |
| `bytedance/seedance-2.0-fast` | $0.255 | Fast generation, supports RealFace |
| `bytedance/seedance-1.5-pro` | $0.098 | Image-to-video only |
| `azure/sora-2` | $0.10/sec | 720p + audio, 4/8/12s |
| `xai/grok-imagine-video` | $0.05 | xAI video |

## Audio Models

| Model | Type | Notes |
|-------|------|-------|
| `elevenlabs/flash-v2.5` | TTS | Fast speech synthesis |
| `elevenlabs/v3` | TTS | Highest quality |
| `elevenlabs/multilingual-v2` | TTS | Multi-language support |
| `elevenlabs/turbo-v2.5` | TTS | Low latency |
| `elevenlabs/sound-effects` | SFX | Sound effect generation |
| `minimax/music-2.5+` | Music | $0.15/track, up to 3 min |

## Providers

| ID | Provider | Models |
|----|----------|--------|
| 1 | OpenAI | 18 |
| 2 | Anthropic | 5 |
| 3 | Google | 7 |
| 4 | DeepSeek | 3 |
| 5 | Moonshot | 1 |
| 6 | ZAI (智谱) | 5 |
| 7 | xAI | 5 |
| 8 | MiniMax | 3 |
| 9 | Nvidia | 10 (all free) |
| 10 | ElevenLabs | 4 |
| 11 | ByteDance | 3 |
| 12 | Azure | 1 |

Full pricing details and live availability at [api.jarvisclaw.ai/pricing](https://api.jarvisclaw.ai/pricing).
