# Prompt Coach API

AI-powered prompt optimization service. Analyzes your prompts for clarity, specificity, and effectiveness, then rewrites them for better LLM performance. Returns scored before/after comparisons with actionable improvement suggestions.

## Base URL

```
https://api.jarvisclaw.ai/v1
```

## Authentication

Include your API key in the `Authorization` header:

```
Authorization: Bearer YOUR_API_KEY
```

This endpoint is x402-enabled. Payment of **$0.002 per request** is required via the x402 protocol header, or deducted from your wallet balance.

## Endpoints

### POST /prompt-coach/optimize

Optimize a prompt for better LLM interaction results.

## Pricing

| Endpoint | Price |
|----------|-------|
| `/prompt-coach/optimize` | $0.002 / request |

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | The prompt text to optimize |
| `model` | string | No | Target model the prompt is intended for (informational, helps tailor optimization) |
| `context` | string | No | Additional context about the use case to guide optimization |

## Request

```json
{
  "prompt": "Write me a python script that does web scraping",
  "model": "gpt-4o",
  "context": "I need to scrape product prices from e-commerce sites for price comparison"
}
```

## Response

```json
{
  "success": true,
  "data": {
    "original_prompt": "Write me a python script that does web scraping",
    "optimized_prompt": "Write a Python script using the `requests` and `BeautifulSoup` libraries to scrape product names and prices from an e-commerce product listing page. The script should: 1) Accept a URL as input, 2) Handle pagination, 3) Extract product name, price, and URL into a structured format, 4) Export results to CSV, 5) Include error handling for network timeouts and missing elements. Use type hints and include docstrings.",
    "explanation": "The original prompt was too vague - it didn't specify the scraping target, libraries, output format, or error handling requirements. The optimized version provides concrete structure, specific deliverables, and technical constraints that will produce immediately usable code.",
    "score_before": 25,
    "score_after": 87,
    "suggestions": [
      "Always specify the target data structure and output format",
      "Include error handling requirements explicitly",
      "Mention specific libraries or constraints when relevant",
      "Define scope boundaries (single page vs. pagination, one site vs. multiple)"
    ],
    "model_used": "deepseek/deepseek-chat"
  }
}
```

## Error Response

```json
{
  "error": {
    "message": "invalid request: Key: 'PromptCoachX402Request.Prompt' Error:Field validation for 'Prompt' failed on the 'required' tag",
    "type": "invalid_request_error"
  }
}
```

## Score Interpretation

| Score Range | Meaning |
|-------------|---------|
| 1-25 | Very vague, lacks specificity |
| 26-50 | Basic intent clear, missing important details |
| 51-75 | Good structure, could be more specific |
| 76-90 | Well-crafted, minor improvements possible |
| 91-100 | Excellent, highly specific and actionable |

## Usage Notes

- The service uses an LLM internally to analyze and optimize prompts
- Optimization preserves the original intent while improving clarity and specificity
- The `model` field is informational — it helps the optimizer tailor suggestions for that model's strengths
- Scores are subjective estimates on a 1-100 scale
- Works best with English prompts; other languages are supported but may score lower

## cURL Example

```bash
curl -X POST https://api.jarvisclaw.ai/v1/prompt-coach/optimize \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "make me a website",
    "context": "I want a portfolio site to showcase my photography work"
  }'
```

## SDK Usage

```python
from jarvisclaw import Client

client = Client(api_key="YOUR_API_KEY")

result = client.prompt_coach.optimize(
    prompt="make me a website",
    context="I want a portfolio site to showcase my photography work"
)

print(f"Score: {result.score_before} → {result.score_after}")
print(f"Optimized: {result.optimized_prompt}")
```
