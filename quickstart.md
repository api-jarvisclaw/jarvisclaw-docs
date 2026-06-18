
# Quick Start

## 1. Create an API Key

Go to the API Keys page and create a new key. Copy it — you won't be able to see it again.

## 2. Set the Base URL

Point your OpenAI-compatible client at our endpoint:

```
https://api.jarvisclaw.ai/v1
```

## 3. Make Your First Request

Use any OpenAI-compatible SDK or plain HTTP. Set model to "auto" to let Smart Router choose the best model.

::: code-group

```python [Python]
from jarvisclaw import ChatClient

chat = ChatClient(api_key="sk-your-api-key")

# Simple — one string in, one string out
print(chat.complete("Hello!"))

# Streaming
for chunk in chat.stream("Tell me a joke"):
    print(chunk, end="")
```

```javascript [Node.js]
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'https://api.jarvisclaw.ai/v1',
  apiKey: 'sk-your-api-key',
});

const response = await client.chat.completions.create({
  model: 'auto',
  messages: [{ role: 'user', content: 'Hello!' }],
  stream: true,
});
for await (const chunk of response) {
  process.stdout.write(chunk.choices[0]?.delta?.content || '');
}
```

```bash [cURL]
curl https://api.jarvisclaw.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-your-api-key" \
  -d '{"model": "auto", "messages": [{"role": "user", "content": "Hello!"}]}'
```

```go [Go]
import jarvisclaw "github.com/api-jarvisclaw/go-sdk"

client, _ := jarvisclaw.NewChatClient(jarvisclaw.WithAPIKey("sk-your-api-key"))

// Simple chat
text, _ := client.Complete(ctx, "Hello!")
fmt.Println(text)

// Streaming
stream, _ := client.Stream(ctx, "Tell me a joke")
for chunk := range stream.Channel() {
    fmt.Print(chunk)
}
```

:::
