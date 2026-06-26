# Embeddings API

Generate vector embeddings for text inputs. Useful for semantic search, clustering, and RAG (Retrieval-Augmented Generation) pipelines. OpenAI-compatible format.

**Base URL:** `https://api.jarvisclaw.ai/v1`

## Authentication

Both methods are supported — all requests settle via x402 on-chain:

| Method | Header | Description |
|--------|--------|-------------|
| API Key | `Authorization: Bearer sk-...` | Platform signs x402 from your HD wallet automatically |
| Private Key (x402) | Automatic via SDK | Agent signs x402 directly from its own wallet |

See [Agent Payments (x402)](/x402) for full details on how both methods work.

## Endpoint

### POST /v1/embeddings

Generate embeddings for one or more text inputs.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| model | string | Yes | Embedding model ID (e.g. `text-embedding-3-small`, `text-embedding-3-large`, `text-embedding-ada-002`) |
| input | string \| array | Yes | Text to embed — a single string or array of strings. Each string max ~8191 tokens |
| encoding_format | string | No | Output format: `float` (default) or `base64` |
| dimensions | integer | No | Desired output dimensionality (only supported by `text-embedding-3-*` models). Truncates the embedding to this size |
| user | string | No | Unique user identifier for abuse monitoring |
| seed | integer | No | Deterministic seed for reproducible embeddings (model-dependent) |
| temperature | float | No | Sampling temperature (model-dependent, rarely used for embeddings) |
| top_p | float | No | Nucleus sampling parameter (model-dependent) |
| frequency_penalty | float | No | Frequency penalty (model-dependent) |
| presence_penalty | float | No | Presence penalty (model-dependent) |

#### Request

```json
{
  "model": "text-embedding-3-small",
  "input": "The quick brown fox jumps over the lazy dog",
  "dimensions": 512
}
```

#### Response

```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "index": 0,
      "embedding": [0.0023064255, -0.009327292, ...]
    }
  ],
  "model": "text-embedding-3-small",
  "usage": {
    "prompt_tokens": 9,
    "total_tokens": 9
  }
}
```

#### Batch Request (multiple inputs)

```json
{
  "model": "text-embedding-3-large",
  "input": [
    "First document to embed",
    "Second document to embed",
    "Third document to embed"
  ],
  "dimensions": 1024
}
```

### Examples

::: code-group

```python [OpenAI SDK]
from openai import OpenAI

client = OpenAI(
    base_url="https://api.jarvisclaw.ai/v1",
    api_key="sk-your-api-key",
)

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Hello world",
    dimensions=512,
)

print(response.data[0].embedding[:5])  # First 5 dimensions
print(f"Total tokens: {response.usage.total_tokens}")
```

```python [JarvisClaw SDK (API Key)]
from jarvisclaw import EmbeddingClient

embed = EmbeddingClient(api_key="sk-your-api-key")

# Single text
result = embed.create("Hello world", model="text-embedding-3-small", dimensions=512)
print(result.data[0].embedding[:5])

# Batch
results = embed.create(
    ["First doc", "Second doc", "Third doc"],
    model="text-embedding-3-large",
    dimensions=1024,
)
for item in results.data:
    print(f"[{item.index}] dim={len(item.embedding)}")
```

```bash [cURL]
curl https://api.jarvisclaw.ai/v1/embeddings \
  -H "Authorization: Bearer sk-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-embedding-3-small",
    "input": "Hello world",
    "dimensions": 512
  }'
```

:::

## Available Models

| Model | Dimensions | Max Input | Price |
|-------|-----------|-----------|-------|
| `text-embedding-3-small` | 1536 (adjustable) | 8191 tokens | $0.02 / 1M tokens |
| `text-embedding-3-large` | 3072 (adjustable) | 8191 tokens | $0.13 / 1M tokens |
| `text-embedding-ada-002` | 1536 (fixed) | 8191 tokens | $0.10 / 1M tokens |

## Rerank

### POST /v1/rerank

Re-rank a list of documents by relevance to a query. Useful for improving retrieval quality in RAG pipelines.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| model | string | Yes | Rerank model ID (e.g. `rerank-v3.5`, `jina-reranker-v2`) |
| query | string | Yes | The search query to rank documents against |
| documents | array | Yes | List of documents (strings or objects) to rerank |
| top_n | integer | No | Number of top results to return (default: all documents) |
| max_chunks_per_doc | integer | No | Maximum chunks per document for long-document reranking |
| return_documents | boolean | No | Whether to include the document text in results (default: true) |
| overlap_tokens | integer | No | Token overlap between chunks when splitting long documents |

#### Request

```json
{
  "model": "rerank-v3.5",
  "query": "What is deep learning?",
  "documents": [
    "Deep learning is a subset of machine learning...",
    "The weather today is sunny and warm...",
    "Neural networks consist of layers of nodes..."
  ],
  "top_n": 2
}
```

#### Response

```json
{
  "object": "list",
  "results": [
    {
      "index": 0,
      "relevance_score": 0.95,
      "document": { "text": "Deep learning is a subset of machine learning..." }
    },
    {
      "index": 2,
      "relevance_score": 0.82,
      "document": { "text": "Neural networks consist of layers of nodes..." }
    }
  ],
  "model": "rerank-v3.5",
  "usage": {
    "total_tokens": 42
  }
}
```

#### Example

```python
from openai import OpenAI
import httpx

# Rerank is not in the standard OpenAI SDK — use httpx directly
resp = httpx.post(
    "https://api.jarvisclaw.ai/v1/rerank",
    headers={"Authorization": "Bearer sk-your-api-key"},
    json={
        "model": "rerank-v3.5",
        "query": "What is deep learning?",
        "documents": [
            "Deep learning is a subset of machine learning...",
            "The weather is nice today",
            "Neural networks use backpropagation",
        ],
        "top_n": 2,
    },
)
results = resp.json()["results"]
for r in results:
    print(f"[{r['index']}] score={r['relevance_score']:.3f}")
```
