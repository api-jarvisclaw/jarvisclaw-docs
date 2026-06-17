# Framework Integrations

Use JarvisClaw with popular AI agent frameworks. Since our API is OpenAI-compatible, integration is straightforward — one line of config in most cases.

## Packages

| Framework | Package | Install |
|-----------|---------|---------|
| LangChain | [langchain-jarvisclaw](https://pypi.org/project/langchain-jarvisclaw/) | `pip install langchain-jarvisclaw` |
| CrewAI | [crewai-jarvisclaw](https://pypi.org/project/crewai-jarvisclaw/) | `pip install crewai-jarvisclaw` |
| AutoGen (AG2) | [autogen-jarvisclaw](https://pypi.org/project/autogen-jarvisclaw/) | `pip install autogen-jarvisclaw` |

All packages support both API key and x402 wallet payment modes.

## LangChain

`langchain-jarvisclaw` extends `ChatOpenAI` with built-in x402 support.

::: code-group

```python [API Key]
from langchain_jarvisclaw import ChatJarvisClaw

chat = ChatJarvisClaw(api_key="sk-...", model="gpt-5.4")
response = chat.invoke("Explain quantum computing")
print(response.content)
```

```python [x402 Wallet]
from langchain_jarvisclaw import ChatJarvisClaw

# Pay per request with USDC — no signup needed
chat = ChatJarvisClaw(wallet_private_key="0x...", model="gpt-5.4")
response = chat.invoke("Explain quantum computing")
```

```python [Chains & Agents]
from langchain_core.prompts import ChatPromptTemplate
from langchain_jarvisclaw import ChatJarvisClaw

chat = ChatJarvisClaw(api_key="sk-...", model="anthropic/claude-sonnet-4.6")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a coding expert."),
    ("human", "{question}"),
])

chain = prompt | chat
result = chain.invoke({"question": "How to reverse a linked list?"})
```

```python [Streaming]
chat = ChatJarvisClaw(api_key="sk-...", model="gpt-5.4", streaming=True)

for chunk in chat.stream("Tell me a story"):
    print(chunk.content, end="", flush=True)
```

:::

### Discovery (no auth)

```python
from langchain_jarvisclaw import ChatJarvisClaw

# List all models with USD pricing
models = ChatJarvisClaw.list_models()
for m in models[:5]:
    print(f"{m['model']}: ${m['input_per_m_token_usd']}/M tokens")

# Find free models
free = ChatJarvisClaw.free_models()

# Platform health
health = ChatJarvisClaw.health()
```

## CrewAI

`crewai-jarvisclaw` provides a `JarvisClawLLM` that plugs directly into CrewAI agents.

::: code-group

```python [Basic]
from crewai import Agent, Task, Crew
from crewai_jarvisclaw import JarvisClawLLM

llm = JarvisClawLLM(model="gpt-5.4", api_key="sk-...")

researcher = Agent(
    role="Senior Researcher",
    goal="Find cutting-edge AI developments",
    backstory="Expert at synthesizing information",
    llm=llm,
)

task = Task(
    description="Research the latest advances in AI agents",
    expected_output="A summary of top 3 developments",
    agent=researcher,
)

crew = Crew(agents=[researcher], tasks=[task])
result = crew.kickoff()
```

```python [x402 Wallet]
from crewai_jarvisclaw import JarvisClawLLM

# No account needed — pay from wallet
llm = JarvisClawLLM(
    model="anthropic/claude-sonnet-4.6",
    wallet_private_key="0x...",
)
```

```python [No Package Needed]
# CrewAI uses LiteLLM — you can also configure directly:
from crewai import LLM

llm = LLM(
    model="openai/gpt-5.4",
    base_url="https://api.jarvisclaw.ai/v1",
    api_key="sk-...",
)
```

:::

## AutoGen (AG2)

`autogen-jarvisclaw` provides config helpers for AutoGen's `config_list` format.

::: code-group

```python [Single Model]
from autogen import ConversableAgent
from autogen_jarvisclaw import jarvisclaw_config

assistant = ConversableAgent(
    name="assistant",
    system_message="You are a helpful AI assistant.",
    llm_config={"config_list": [jarvisclaw_config(model="gpt-5.4", api_key="sk-...")]},
)

user = ConversableAgent(name="user", human_input_mode="NEVER", llm_config=False)
user.initiate_chat(assistant, message="What's the capital of France?")
```

```python [Multi-Model Fallback]
from autogen import ConversableAgent
from autogen_jarvisclaw import jarvisclaw_config_list

# AutoGen tries models in order — automatic fallback
configs = jarvisclaw_config_list(
    models=["gpt-5.4", "anthropic/claude-sonnet-4.6", "deepseek/deepseek-chat"],
    api_key="sk-...",
)

assistant = ConversableAgent(
    name="assistant",
    llm_config={"config_list": configs},
)
```

```python [Multi-Agent]
from autogen import ConversableAgent, GroupChat, GroupChatManager
from autogen_jarvisclaw import jarvisclaw_config

config = {"config_list": [jarvisclaw_config(model="gpt-5.4", api_key="sk-...")]}

researcher = ConversableAgent(name="researcher", system_message="Research topics.", llm_config=config)
writer = ConversableAgent(name="writer", system_message="Write summaries.", llm_config=config)
critic = ConversableAgent(name="critic", system_message="Review for accuracy.", llm_config=config)

group_chat = GroupChat(agents=[researcher, writer, critic], messages=[], max_round=6)
manager = GroupChatManager(groupchat=group_chat, llm_config=config)
researcher.initiate_chat(manager, message="Research quantum computing in 2026")
```

```python [No Package Needed]
# AutoGen is OpenAI-compatible — direct config also works:
config_list = [{
    "model": "gpt-5.4",
    "api_key": "sk-...",
    "base_url": "https://api.jarvisclaw.ai/v1",
}]
```

:::

## Eliza (ai16z)

Eliza agents can use JarvisClaw as their model provider. Add to your character config:

```json
{
  "modelProvider": "openai",
  "settings": {
    "model": "gpt-5.4",
    "apiKey": "sk-...",
    "baseURL": "https://api.jarvisclaw.ai/v1"
  }
}
```

## Any OpenAI-Compatible Framework

Since JarvisClaw is fully OpenAI-compatible, any framework that lets you set `base_url` works out of the box:

```python
# Generic pattern — works with any OpenAI-compatible client
base_url = "https://api.jarvisclaw.ai/v1"
api_key = "sk-..."
```

No special adapter needed. Our packages just add x402 wallet payment support and convenience methods.
