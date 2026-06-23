# Web Search API (Exa)

Neural web search engine designed for AI agents. Semantic ranking via neural embeddings (not just keywords), similar page discovery for competitive research, full-text page content extraction, and AI-grounded answers with source citations. Filter by category: company, research paper, news, PDF, GitHub, LinkedIn profile, financial report.

**Base URL:** `https://api.jarvisclaw.ai/v1/marketplace/exa`

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/search` | Semantic web search with neural ranking |
| POST | `/find-similar` | Find pages similar to a given URL |
| POST | `/contents` | Extract full-text content from URLs |
| POST | `/answer` | AI-grounded answer with source citations |

## Pricing

| Endpoint | Price | Description |
|----------|-------|-------------|
| /search | $0.01/request | Neural semantic search |
| /find-similar | $0.01/request | Similar page discovery |
| /contents | $0.002/URL | Full-text page extraction |
| /answer | $0.01/request | AI answer with citations |

## POST /search

Search the web using neural semantic ranking. Returns results ranked by meaning, not just keyword matching.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Search query (max 10,000 characters) |
| `numResults` | integer | No | Number of results to return. Default: `10` |
| `category` | string | No | Filter by category: `company`, `research paper`, `news`, `pdf`, `github`, `linkedin profile`, `financial report` |
| `startPublishedDate` | string | No | Filter results published after this date (ISO 8601) |
| `endPublishedDate` | string | No | Filter results published before this date (ISO 8601) |

### Request

```json
{
  "query": "latest breakthroughs in protein folding AI models 2026",
  "numResults": 5,
  "category": "research paper",
  "startPublishedDate": "2026-01-01T00:00:00Z"
}
```

### Response

```json
{
  "results": [
    {
      "title": "AlphaFold 3: Predicting All Molecular Interactions",
      "url": "https://example.com/alphafold3-paper",
      "score": 0.95,
      "publishedDate": "2026-03-15T00:00:00Z",
      "author": "DeepMind Research"
    },
    {
      "title": "ESMFold Advances in Zero-Shot Structure Prediction",
      "url": "https://example.com/esmfold-advances",
      "score": 0.89,
      "publishedDate": "2026-02-20T00:00:00Z",
      "author": "Meta AI"
    }
  ],
  "query": "latest breakthroughs in protein folding AI models 2026"
}
```

## POST /find-similar <Badge type="warning" text="Coming Soon" />

Find web pages similar to a given URL. Useful for competitive research, finding related content, and discovering alternatives.

::: warning
This endpoint is not yet available. It will return `404` until enabled. Use `/search` with a descriptive query as an alternative.
:::

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | Source URL to find similar pages for (must be publicly indexable) |
| `numResults` | integer | No | Number of similar results to return. Default: `10` |

### Request

```json
{
  "url": "https://openai.com/research/gpt-4",
  "numResults": 5
}
```

### Response

```json
{
  "results": [
    {
      "title": "Claude 3.5 Sonnet: Technical Report",
      "url": "https://example.com/claude-report",
      "score": 0.92
    },
    {
      "title": "Gemini Ultra: Capabilities and Limitations",
      "url": "https://example.com/gemini-ultra",
      "score": 0.87
    }
  ],
  "sourceUrl": "https://openai.com/research/gpt-4"
}
```

## POST /contents

Extract full-text content from one or more URLs. Returns clean, parsed page text suitable for LLM consumption.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `urls` | string[] | Yes | Array of URLs to extract content from |

### Request

```json
{
  "urls": [
    "https://example.com/article-1",
    "https://example.com/article-2"
  ]
}
```

### Response

```json
{
  "contents": [
    {
      "url": "https://example.com/article-1",
      "title": "Understanding Transformer Architectures",
      "text": "Transformer models have revolutionized natural language processing...",
      "publishedDate": "2026-05-10T00:00:00Z"
    },
    {
      "url": "https://example.com/article-2",
      "title": "Scaling Laws for Neural Language Models",
      "text": "We study empirical scaling laws for language model performance...",
      "publishedDate": "2026-04-22T00:00:00Z"
    }
  ]
}
```

## POST /answer

Get an AI-generated answer to a query, grounded in web sources with citations.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Question to answer (max 10,000 characters) |

### Request

```json
{
  "query": "What are the main differences between GPT-4 and Claude 3.5?"
}
```

### Response

```json
{
  "answer": "GPT-4 and Claude 3.5 differ in several key areas: architecture design, context window size, multimodal capabilities, and safety approaches. GPT-4 supports up to 128k tokens of context while Claude 3.5 Sonnet supports 200k tokens...",
  "sources": [
    {
      "title": "GPT-4 Technical Report",
      "url": "https://example.com/gpt4-report"
    },
    {
      "title": "Claude 3.5 Model Card",
      "url": "https://example.com/claude-model-card"
    }
  ]
}
```

## Errors

| HTTP Status | Code | Description |
|-------------|------|-------------|
| 400 | `query_too_long` | Query exceeds the 10,000 character limit |
| 400 | `invalid_url` | The provided URL is malformed or not a valid web address |
| 422 | `url_unreachable` | The URL could not be fetched (not publicly accessible or blocked) |

## Code Examples

::: code-group

```bash [cURL]
# Semantic search
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/exa/search \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "best open source LLM frameworks 2026",
    "numResults": 5,
    "category": "github"
  }'

# Find similar pages
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/exa/find-similar \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://github.com/langchain-ai/langchain",
    "numResults": 5
  }'

# Extract page contents
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/exa/contents \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example.com/article"]
  }'

# Get AI answer with citations
curl -X POST https://api.jarvisclaw.ai/v1/marketplace/exa/answer \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is retrieval augmented generation and how does it work?"
  }'
```

```python [Python (API Key)]
import requests

BASE = "https://api.jarvisclaw.ai/v1/marketplace/exa"
HEADERS = {
    "Authorization": "Bearer sk-your-api-key",
    "Content-Type": "application/json",
}

# Semantic search
resp = requests.post(f"{BASE}/search", headers=HEADERS, json={
    "query": "best open source LLM frameworks 2026",
    "numResults": 5,
    "category": "github",
})
for result in resp.json()["results"]:
    print(f"{result['title']}: {result['url']}")

# Find similar pages (coming soon — endpoint not yet available)
# resp = requests.post(f"{BASE}/find-similar", headers=HEADERS, json={
#     "url": "https://github.com/langchain-ai/langchain",
#     "numResults": 5,
# })
# for result in resp.json()["results"]:
#     print(f"{result['title']} (score: {result['score']})")

# Extract page contents
resp = requests.post(f"{BASE}/contents", headers=HEADERS, json={
    "urls": ["https://example.com/article-1", "https://example.com/article-2"],
})
for content in resp.json()["contents"]:
    print(f"{content['title']}: {content['text'][:100]}...")

# AI-grounded answer
resp = requests.post(f"{BASE}/answer", headers=HEADERS, json={
    "query": "What is retrieval augmented generation and how does it work?",
})
data = resp.json()
print(data["answer"])
for source in data["sources"]:
    print(f"  Source: {source['url']}")
```

```python [Python (x402 Agent)]
from jarvisclaw import SearchClient

# --- Option A: Base chain (EVM) ---
# Hex private key -> USDC on Base (Chain ID 8453)
search = SearchClient(private_key="0x<evm-private-key>")

# --- Option B: Solana ---
# Base58 keypair -> USDC SPL on Solana mainnet
# search = SearchClient(private_key="<solana-bs58-keypair>")

# SDK auto-detects chain from key format - no config needed

# Semantic search
results = search.query("best open source LLM frameworks 2026", num_results=5)
for r in results:
    print(f"{r.title}: {r.url}")

# Find similar pages (coming soon — not yet available)
# similar = search.find_similar("https://github.com/langchain-ai/langchain", num_results=5)
# for r in similar:
#     print(f"{r.title}: {r.url}")

# Extract page contents
contents = search.contents(["https://example.com/article-1", "https://example.com/article-2"])
for c in contents:
    print(c)
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
    sc, _ := jc.NewSearchClient(jc.WithAPIKey("sk-your-api-key"))

    // Semantic search — returns *SearchResponse
    resp, _ := sc.Query(ctx, "best open source LLM frameworks 2026",
        jc.WithNumResults(5))
    fmt.Printf("Summary: %s\n", resp.Summary)
    fmt.Printf("Sources used: %d\n", resp.SourcesUsed)
    for _, r := range resp.Citations {
        fmt.Printf("  %s: %s\n", r.Title, r.URL)
    }
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
    sc, _ := jc.NewSearchClient(jc.WithPrivateKey("0x<evm-private-key>"))

    // Semantic search — returns *SearchResponse
    resp, _ := sc.Query(ctx, "best open source LLM frameworks 2026",
        jc.WithNumResults(5))
    fmt.Printf("Summary: %s\n", resp.Summary)
    fmt.Printf("Sources used: %d\n", resp.SourcesUsed)
    for _, r := range resp.Citations {
        fmt.Printf("  %s: %s\n", r.Title, r.URL)
    }
}
```

:::

## Limitations

- **10,000 character query max** — queries exceeding this length are rejected with `query_too_long`
- **Public pages only** — cannot access content behind authentication or paywalls
- **100 requests/minute rate limit** — per API key, across all Exa endpoints
- **find-similar requires indexable URL** — the source URL must be publicly accessible and crawlable
- **answer takes 3-8 seconds** — the AI synthesis step adds latency compared to raw search
