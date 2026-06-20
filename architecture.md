# JarvisClaw 业务架构与支付流向

## 系统概览

JarvisClaw 是一个 AI API 路由平台，聚合 40+ 上游 AI 供应商，通过 x402 协议实现链上微支付结算。

```
┌─────────────────────────────────────────────────────────────────────┐
│                        JarvisClaw Platform                          │
│                                                                     │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────────┐   │
│  │ AI Models │  │Prediction │  │  Image &  │  │    Video &    │   │
│  │   API     │  │Market API │  │  Search   │  │    Audio      │   │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └──────┬────────┘   │
│        └───────────────┴───────────────┴───────────────┘            │
│                              │                                      │
│                    ┌─────────┴─────────┐                            │
│                    │   BlockRun (x402)  │                            │
│                    │   上游供应商        │                            │
│                    └───────────────────┘                            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 三种用户模式

### 模式 A：Agent x402 直付（Machine-to-Machine）

**适用场景**：AI Agent 自动调用，无需注册账号

```
┌──────────┐                    ┌──────────────┐                ┌──────────┐
│  Agent   │  ① 请求（无auth）   │  JarvisClaw  │                │ BlockRun │
│  钱包    │ ──────────────────→ │              │                │  (上游)  │
│          │  ② 返回 402        │              │                │          │
│          │ ←────────────────── │              │                │          │
│          │  ③ 签名x402付款     │              │                │          │
│          │ ──────────────────→ │              │                │          │
│          │                    │ ④ Facilitator │                │          │
│          │                    │   验证签名    │                │          │
│          │                    │ ⑤ Settle      │                │          │
│          │                    │  Agent→JC1   │                │          │
│          │                    │  (先收钱)    │  ⑥ HD-Pay x402  │          │
│          │                    │              │ ──────────────→ │          │
│          │  ⑦ 返回数据        │              │ ←────────────── │          │
│          │ ←────────────────── │              │                │          │
└──────────┘                    └──────────────┘                └──────────┘
```

**资金流向**：
```
Agent 钱包 ──$0.01──→ JC1 (收费钱包)

HD-Pay 钱包池 (轮转选择) ──$0.01──→ BlockRun
```

**特点**：
- 无需注册、无需 API Key
- Settle-then-Forward：先收 Agent 的钱，再付上游（与 BlockRun 对 HD-Pay 的模式对等）
- 上游失败 → Agent 已付款（通过重试机制尽力交付）
- SDK：`pip install jarvisclaw`

---

### 模式 B：USDC 预充值（HD 钱包结算）

**适用场景**：Crypto 原生用户，直接充 USDC

```
┌──────────┐                    ┌──────────────┐                ┌──────────┐
│   用户   │  ① 充值 USDC       │  JarvisClaw  │                │ BlockRun │
│  外部    │  到 HD 子钱包       │              │                │  (上游)  │
│  钱包    │ ──────────────────→ │ HD 子钱包    │                │          │
│          │                    │              │                │          │
│          │  ② API Key 调用    │              │                │          │
│          │ ──────────────────→ │              │                │          │
│          │                    │ ③ HD→JC1     │                │          │
│          │                    │   x402结算    │                │          │
│          │                    │              │  ④ HD-Pay x402    │          │
│          │                    │              │ ──────────────→ │          │
│          │  ⑤ 返回数据        │              │ ←────────────── │          │
│          │ ←────────────────── │              │                │          │
└──────────┘                    └──────────────┘                └──────────┘
```

**资金流向**：
```
用户外部钱包 ──充值──→ 用户 HD 子钱包 ──x402──→ JC1 (收费钱包)

                              HD-Pay 钱包池 (轮转选择) ──x402──→ BlockRun
```

**特点**：
- 用户充 USDC 到 HD 子钱包
- 实际结算走链上 x402（HD 子钱包 → JC1）
- 前端显示的余额 = HD 钱包链上 USDC 余额（实时）

---

### 模式 C：法币充值（Airwallex）

**适用场景**：普通用户，信用卡/支付宝充值

```
┌──────────┐                    ┌──────────────┐                ┌──────────┐
│   用户   │  ① Airwallex 付款  │  JarvisClaw  │                │ BlockRun │
│          │ ──────────────────→ │              │                │  (上游)  │
│          │                    │ ② JC4 ERC20   │                │          │
│          │                    │   转到HD钱包  │                │          │
│          │                    │              │                │          │
│          │                    │              │                │          │
│          │  ④ API Key 调用    │              │                │          │
│          │ ──────────────────→ │              │                │          │
│          │                    │ ⑤ HD→JC1 x402│                │          │
│          │                    │              │  ⑥ HD-Pay x402    │          │
│          │                    │              │ ──────────────→ │          │
│          │  ⑦ 返回数据        │              │ ←────────────── │          │
│          │ ←────────────────── │              │                │          │
└──────────┘                    └──────────────┘                └──────────┘
```

**资金流向**：
```
用户 ──法币──→ Airwallex ──法币──→ JC 银行账户
                                        │
JC4 (资金池) ──ERC20 USDC──→ 用户 HD 子钱包 ──x402──→ JC1 (收费钱包)

                                        HD-Pay 钱包池 ──x402──→ BlockRun
```

**特点**：
- 用户只看到余额（实际是 HD 钱包 USDC 余额）
- JC4 先把等额 USDC 转到用户 HD 钱包
- JC4 转账失败 → 余额不变，等待人工处理
- 前端显示余额 = HD 钱包链上 USDC（无独立 quota 系统）

---

## 钱包体系

```
┌─────────────────────────────────────────────────────────────────┐
│                      JarvisClaw 钱包体系                         │
├─────────┬────────────────────────────────────────────────────────┤
│         │                                                        │
│   JC1   │  收费钱包 (0xf348c3...)                                │
│         │  - 收 Agent x402 付款                                  │
│         │  - 收 HD 子钱包 x402 结算                              │
│         │  - 私钥离线冷存储                                      │
│         │                                                        │
├─────────┼────────────────────────────────────────────────────────┤
│         │                                                        │
│  HD-Pay │  上游结算 HD 钱包池 (100 个子地址)                      │
│  (原JC2)│  - 派生路径: m/44'/60'/0'/0/{0-99}                    │
│         │  - 付 BlockRun 上游 x402                               │
│         │  - 每钱包独立 HTTP/2 连接 + 熔断器 + 自适应并发         │
│         │  - 种子: BLOCKRUN_HD_MNEMONIC 环境变量                  │
│         │  - BlockRun 按 wallet address 加白                     │
│         │                                                        │
├─────────┼────────────────────────────────────────────────────────┤
│         │                                                        │
│   JC3   │  返佣钱包                                              │
│         │  - 收 BlockRun 7折返佣 (额外30%)                       │
│         │  - 不跟 JC1/HD-Pay 混                                  │
│         │                                                        │
├─────────┼────────────────────────────────────────────────────────┤
│         │                                                        │
│   JC4   │  资金池钱包                                            │
│         │  - 法币充值后 ERC20 转给用户 HD 钱包                   │
│         │  - 需要 USDC + ETH (gas)                               │
│         │  - 私钥分片: JC4_SHARD_A + JC4_SHARD_B                │
│         │                                                        │
├─────────┼────────────────────────────────────────────────────────┤
│         │                                                        │
│ HD-User │  用户 HD 子钱包 (BIP-44 派生)                          │
│         │  - 每用户一个独立地址                                  │
│         │  - 用于 x402 结算到 JC1                                │
│         │  - 种子分片: CRYPTO_SEED_SHARD_A/B                     │
│         │                                                        │
├─────────┼────────────────────────────────────────────────────────┤
│         │                                                        │
│Facilita-│  Facilitator 钱包                                      │
│  tor    │  - 付 gas 执行链上结算                                 │
│         │  - 只需少量 ETH                                        │
│         │                                                        │
└─────────┴────────────────────────────────────────────────────────┘
```

---

## 资金流向总图

```
                    ┌─────────────────┐
                    │   法币用户       │
                    │  (Airwallex)    │
                    └────────┬────────┘
                             │ 法币
                             ↓
                    ┌─────────────────┐
                    │   JC 银行账户    │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │   JC4 资金池     │
                    │   (USDC+ETH)    │
                    └────────┬────────┘
                             │ ERC20 transfer
                             ↓
┌──────────┐        ┌─────────────────┐        ┌─────────────────┐
│  Agent   │        │ HD-User 子钱包   │        │  USDC 用户      │
│  钱包    │        │  (每用户独立)    │        │  (直接充值)     │
└────┬─────┘        └────────┬────────┘        └────────┬────────┘
     │                       │                          │
     │ x402                  │ x402                     │ x402
     │                       │                          │
     └───────────────────────┴──────────────────────────┘
                             │
                             ↓
                    ┌─────────────────┐
                    │   JC1 收费钱包   │
                    │  (所有收入汇集)  │
                    └─────────────────┘

                    ┌─────────────────┐
                    │  HD-Pay 钱包池   │
                    │  (100 个子地址)  │
                    └────────┬────────┘
                             │ x402 (轮转选择)
                             ↓
                    ┌─────────────────┐
                    │    BlockRun     │
                    │   (上游供应商)   │
                    └────────┬────────┘
                             │ 7折返佣 (30%)
                             ↓
                    ┌─────────────────┐
                    │   JC3 返佣钱包   │
                    └─────────────────┘
```

---

## 结算时序（三种模式对比）

| 步骤 | 模式 A (Agent x402) | 模式 B (USDC 充值) | 模式 C (法币充值) |
|------|--------------------|--------------------|-------------------|
| 认证 | PAYMENT-SIGNATURE | API Key | API Key |
| 用户→JC1 | x402 直付 (Settle先收钱) | HD→JC1 x402 | HD→JC1 x402 |
| HD-Pay→上游 | HD-Pay x402 付 BlockRun | HD-Pay x402 付 BlockRun | HD-Pay x402 付 BlockRun |
| 计费 | 链上实时 | 链上 x402 结算 | 链上 x402 结算 |
| 失败处理 | 已付款（重试交付） | HD 余额不足拒绝 | HD 余额不足拒绝 |
| 用户看到 | 钱包余额减少 | HD 钱包余额减少 | HD 钱包余额减少 |

---

## x402 Seller 定价机制

### 定价流程（按模型类型区分）

**Token 模型（Chat/Completion）：**
```
Agent 请求 → 从模型广场读取 model_price（上游同步）→ 估算 token 用量 → 加 markup → 返回 402 报价
```

**非 Token 模型（Video/Image/Music）— 上游探测模式：**
```
① Agent → JarvisClaw: POST /v1/videos/generations (无 auth)
② JarvisClaw → BlockRun: 转发原始请求（不带签名）
③ BlockRun → JarvisClaw: 返回 402 + 真实 amount（如 1191053 = $1.19）
④ JarvisClaw → Agent: 返回 402（amount = 上游真实价格 × (1 + markup%)）
⑤ Agent → JarvisClaw: 签名 x402 付款 + 重发请求
⑥ JarvisClaw (HD-Pay) → BlockRun: 签名 x402 付上游
⑦ BlockRun → JarvisClaw → Agent: 返回数据
```

**设计原则：**
- **永不亏本**：非 token 模型先问上游真实价格再报价
- **上游什么价，我们什么价 + markup**：价格来源于上游，不手动维护
- **零缓存风险**：每次请求实时探测（多一跳 ~100ms，对于 video/image 可接受）
- **优雅降级**：探测失败时 fallback 到本地估算价格

### 价格来源优先级

```
1. 上游 402 探测（非 token 模型）— 实时精确
2. ratio_setting.GetModelPrice()（token 模型）— 从上游定期同步
3. setting.GetSmartRouteFixedPrices()（DB 配置）— 后台可配
4. blockrunFixedPrices（hardcoded）— 最终兜底
```

### Markup 配置

- 环境变量：`X402_MARKUP_PERCENT`（默认 3）
- 含义：`最终报价 = 上游成本 × (1 + markup/100)`
- 示例：上游 $1.19 → 报价 $1.23（3% markup）

### 模型类型识别

| URL 路径 | 定价方式 |
|---------|---------|
| `/v1/chat/completions` | Token 估算 |
| `/v1/images/generations` | 上游 402 探测 |
| `/v1/videos/generations` | 上游 402 探测 |
| `/v1/audio/generations` | 上游 402 探测 |
| `/v1/audio/speech` | Token 估算 |

---

## 安全机制

| 机制 | 说明 |
|------|------|
| Settle-then-Forward | Agent 付款先结算再服务，与上游模式对等 |
| 每日限额 | 合并限额 $1000/天 (x402 总消费) |
| 钱包冻结 | 可冻结单个用户钱包 |
| 紧急停止 | 一键停止所有 x402 支付 |
| 大额告警 | > $100 单笔交易推送 TG |
| 余额预警 | HD-Pay/JC4 余额低于阈值告警 |
| Gas 监控 | Base 链 gas 异常告警 |
| 密钥分片 | 所有私钥 XOR 分片存储 |
| Facilitator HA | CDP Pool (3 nodes, priority + round-robin) |
| 动态 feePayer | Solana feePayer 从 CDP /supported 自动同步 |
| Loss Log | 上游 5xx 导致资金损失自动记录 + TG 告警 |
| Response 清洗 | 自动 strip txHash/credits/payment 敏感信息 |
| Payment Validation | x402 payment option 白名单验证 (network/payTo/amount) |
| Refund Guard | 防双重退款 (blockrun_x402_already_refunded atomic flag) |
| Circuit Breaker | GOAWAY 触发钱包级熔断，防雪崩重试 |
| Adaptive Concurrency | 动态调整每钱包并发上限，防连接过载 |

---

## 双链结算（Base + Solana）

HD 钱包 x402 结算支持 Base (EVM) 和 Solana 双链，自动 fallback：

```
用户请求 → 查用户 deposit addresses
  → 只有 EVM: settle on Base (EIP-712 签名)
  → 只有 Solana: settle on Solana (SPL Transfer + CDP feePayer 代付 gas)
  → 两条链都有: 先 Base，余额不足 → fallback Solana
  → 都不够: abort "insufficient balance on all chains"
```

**Solana 结算流程：**
- SLIP-0010 HD 派生 Ed25519 密钥
- 构建 SPL Token TransferChecked 交易
- CDP facilitator 作为 feePayer 代付 gas（地址从 /supported 动态获取）
- 获取真实 blockhash（调 Solana mainnet RPC）
- Partial-sign → CDP co-sign + submit

---

## 智能路由（Smart Route）

虚拟模型自动路由到最优上游模型：

| 虚拟模型 | 路由逻辑 | 目标模型示例 |
|---------|---------|------------|
| `auto` | Prompt 复杂度分析 → 6 tier | SIMPLE→gpt-5.4-mini, COMPLEX→gemini-3.1-pro |
| `auto/free` | 只选免费模型 | gemini-flash-lite, deepseek-chat |
| `auto/eco` | 性价比优先 | deepseek-chat, gpt-5.4-mini |
| `auto/premium` | 质量优先 | claude-opus-4.8, gpt-5.5 |
| `auto/video` | 视频特征分析 | seedance-2.0, seedance-2.0-fast |
| `auto/image` | 图片需求分析 | gpt-image-2, dall-e-3 |
| `auto/music` | 音乐风格分析 | minimax/music-2.5+ |
| `auto/tts` | 语言检测 | elevenlabs/flash-v2.5 (EN), multilingual-v2 (多语言) |
| `auto/search` | 搜索聚合 | xai/grok-4.3 + Exa sources |

**路由配置：**
- 后台 UI 可视化管理每个 tier 的模型
- AI 路由顾问：选一个模型分析当前可用模型 → 推荐最优路由配置
- 管理员审批后生效，支持手动覆盖

---

## 上游模型自动同步

```
启动 → 30 分钟定时任务 → 调 BlockRun /v1/models
  → 检测新模型 → 自动加入 channel models 字段
  → 检测废弃模型 → 标记待处理
  → 无需代码变更
```

**配置：**
- `CHANNEL_UPSTREAM_MODEL_UPDATE_TASK_ENABLED=true`（默认开启）
- BlockRun channel 自动启用 `UpstreamModelUpdateAutoSyncEnabled`
- 所有 `auto/*` 虚拟模型在 channel 创建时自动注册

---

## Marketplace 代理

```
/v1/marketplace/{service}/*path → 查 DB 服务配置 → x402 付 BlockRun → 转发响应
```

| 服务 | 网关路径 | 上游 pathPrefix | 端点数 | 定价方式 |
|------|---------|----------------|--------|----------|
| surf | /v1/marketplace/surf/* | /surf | 83+ | GET $0.001, POST $0.005 |
| exa | /v1/marketplace/exa/* | /exa | 4 | GET $0.001, POST $0.01 |
| prediction | /v1/marketplace/prediction/* | /pm | 17+ | GET $0.001, POST $0.005 |
| realface | /v1/marketplace/realface/* | /realface | 3 | GET免费, POST由上游402定价 ($0.01/enroll) |
| portrait | /v1/marketplace/portrait/* | /portrait | 3 | GET免费, POST由上游402定价 ($0.01/enroll) |

**Marketplace 计费逻辑：**

```
请求进入 → X402OrTokenAuth (认证)
  ├─ 有 API Key → TokenAuth → MarketplaceProxy
  ├─ 有 PAYMENT-SIGNATURE → handleX402Payment (免费端点跳过settle)
  └─ 无 auth → 免费端点走TokenAuth / 付费端点返回402

MarketplaceProxy:
  → 读 DB 的 get_cost / post_cost
  → 请求上游
  → 上游返回 200 且 costUSD > 0 → HD settle 收费
  → 上游返回 402 且 costUSD > 0 或 POST → 走 x402 付款流
  → 上游返回 402 且 costUSD == 0 且 GET → 跳过（免费查询）
  → 成功后记录日志 (LogTypeMarketplace = 7)
```

**免费端点保护：**
- `get_cost = 0` 的端点（如 realface/status、realface/init）不收费
- `post_cost = 0` 的 POST 端点允许上游 402 驱动定价（如 realface/enroll）
- 对 x402 payer 访问免费端点：验证签名但跳过 settle，不收钱

**x402 双层结算：**
1. Agent/HD 用户付 JarvisClaw（seller middleware 或 HD settle）
2. HD-Pay 付 BlockRun（marketplace proxy 内部）
3. 两层独立，BlockRun 只认 HD-Pay 的 payment

---

## BlockRun 高并发架构（WalletPool）

### 问题

单钱包单连接打 BlockRun，高并发下触发 HTTP/2 GOAWAY (ENHANCE_YOUR_CALM)，导致请求批量失败。

### 解决方案

单 Channel 内部维护 **100 个 HD 钱包池**，每个钱包独立 HTTP/2 连接 + 熔断器 + 自适应并发控制。

```
┌────────────────────────────────────────────────────────────┐
│  Channel #1 (BlockRun)                                     │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  WalletPool: 100 个 HD 钱包 (m/44'/60'/0'/0/{0-99}) │  │
│  │                                                      │  │
│  │  每个 Wallet:                                        │  │
│  │    • 独立 HTTP/2 连接 (DialTLSContext)               │  │
│  │    • CircuitBreaker (GOAWAY → 5s-60s cooldown)       │  │
│  │    • Semaphore (cap=100, 自适应调整)                  │  │
│  │    • Per-model in-flight 计数                        │  │
│  │                                                      │  │
│  │  Select(model) → 跳过熔断 → 选最少在飞 → CAS acquire │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  请求流程:                                                 │
│    Select(model) → 签名(entry.PrivateKey) →                │
│    发送(entry.Client) → 成功: OnSuccess / 失败: OnGOAWAY   │
│    → defer Release(entry, model)                          │
└────────────────────────────────────────────────────────────┘
         │ × 100 独立 HTTP/2 连接
         ▼
┌────────────────────────┐
│   BlockRun Gateway     │
│   (Cloudflare 前置)    │
│                        │
│   100 wallet 各自      │
│   per-model rate limit │
└────────────────────────┘
```

### 自适应机制

| 信号 | 动作 |
|------|------|
| GOAWAY | 该钱包: 熔断 5s, 并发容量 -20% |
| 429 | 该钱包+模型: 冷却 retry_after 秒 |
| 连续无错 1min | 该钱包: 并发容量 +5% (上限 200) |
| 半开探测成功 ×3 | 恢复该钱包为正常状态 |

### 容量规划

| 部署模式 | 钱包分配 | 总并发 |
|----------|---------|--------|
| 单节点 | 100 钱包 (≤50 活跃) | ~5,000 |
| 4 节点集群 | 25 钱包/节点 | ~10,000 |

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `BLOCKRUN_HD_MNEMONIC` | HD 种子助记词 | 空（禁用 pool） |
| `BLOCKRUN_POOL_SIZE` | 钱包数量 | 100 |

### 降级策略

```
Pool 启用 + HD seed 配置 → 多钱包模式
Pool 未启用 (无 HD seed) → fallback 单钱包 (BASE_CHAIN_WALLET_KEY)
所有钱包熔断 → 返回 503 (后续可扩展到 fallback 直连 provider)
```

---

## 异步任务轮询（Video/Image）

视频和图片生成是异步的：POST 提交 → 后台轮询 → 用户 GET 取结果。

**流程：**
```
用户: POST /v1/videos/generations
  → BlockRun 返回 402 → HD settle + HD-Pay付款 → 202 Accepted
  → 返回 { id, status: "in_progress", poll_url }
  → 后台 StartPoller（每5秒轮询 BlockRun）

后台 Poller:
  → GET poll_url (带 PAYMENT-SIGNATURE 证明身份，不额外扣费)
  → status == "in_progress" → 继续
  → status == "completed" → 存结果到 jobstore
  → status == "failed" / 超时 → 记录失败

用户: GET /v1/videos/generations/{id}
  → 查 jobstore → 返回缓存结果（无额外计费）
```

**计费时机：**
- **POST 提交时收费一次**（HD settle + HD-Pay 付 BlockRun）
- **后续 poll 不再收费**（签名只做身份验证）
- **用户 GET 取结果不收费**（从本地 jobstore 返回）

**超时保护：**
- MaxAttempts: 100 次（video）/ 60 次（image）
- Timeout: 500s（video）/ 300s（image）
- 超时后标记 job 为 failed

**Jobstore 双层存储（pkg/jobstore）：**
- Hot: 内存 map（本实例快速读取）
- Cold: Valkey/Redis（跨实例恢复、持久化 24h）
- Recovery: 实例重启后从 Valkey 恢复未完成 job 继续轮询

---

## 媒体 CDN（Cloudflare Workers + R2）

```
用户请求 API → EC2 返回 cdn.jarvisclaw.ai URL
用户请求媒体 → Cloudflare Edge → R2 缓存 / BlockRun CDN fallback

EC2 零媒体带宽。
```

**架构：**
```
┌──────────┐         ┌──────────────────┐         ┌───────────┐
│  用户    │  API    │  EC2 (Go 服务)    │         │ BlockRun  │
│          │ ──────→ │ 只返回 JSON       │         │   CDN     │
│          │ ←────── │ 含 cdn URL        │         │           │
│          │         └──────────────────┘         │           │
│          │                                      │           │
│          │  媒体   ┌──────────────────┐         │           │
│          │ ──────→ │ cdn.jarvisclaw.ai │         │           │
│          │ ←────── │ (CF Worker + R2)  │ ──────→ │           │
└──────────┘         └──────────────────┘         └───────────┘
                            │
                     ┌──────┴──────┐
                     │  R2 Bucket  │
                     │ (12h 缓存)  │
                     └─────────────┘
```

**配置：** 后台 → 系统设置 → CDN Base URL → `https://cdn.jarvisclaw.ai`

---

## 计费日志体系

所有消费记录统一写入 `logs` 表，通过 `type` 字段区分：

| Type | 值 | 来源 | 内容 |
|------|---|------|------|
| Consume | 2 | LLM relay 层 | token 用量、模型、x402 金额 |
| Marketplace | 7 | marketplace proxy | 服务名、sub_path、tx_hash、USDC 金额 |
| Error | 5 | relay 错误处理 | 失败请求 |
| Refund | 6 | 退款操作 | 退款金额 |

**LLM 计费（BlockRun channel）：**
- `blockrun_x402_pre_deducted` context flag 防止 relay 层按 token ratio 重复计费
- HD settle 后设置此 flag → PostTextConsumeQuota 只记日志不按 token 再算一遍
- x402 seller 付款同理（`x402_seller_paid` flag）

**Marketplace 计费：**
- HD settle 成功后写入 `LogTypeMarketplace = 7`
- 记录：service_id、sub_path、tx_hash、USDC 金额、markup
- 前端 Usage Logs 页面支持 "Marketplace" 筛选

---

## 技术栈

| 组件 | 技术 |
|------|------|
| 后端 | Go 1.22+, Gin, GORM |
| 前端 | React 19, TypeScript, Tailwind, shadcn/ui |
| 数据库 | Aurora Serverless v2 PostgreSQL |
| 缓存 | AWS Valkey Serverless (Redis 兼容) |
| 支付 | x402 协议 (EIP-3009 TransferWithAuthorization) |
| 链 | Base Mainnet (8453) + Solana Mainnet |
| 资产 | USDC — Base (0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913) / Solana (EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v) |
| Facilitator | CDP (api.cdp.coinbase.com) — 3 node pool |
| 法币 | Airwallex |
| 媒体 CDN | Cloudflare Workers + R2 (cdn.jarvisclaw.ai) |
| LB | AWS ALB |
| CI/CD | GitHub Actions → Docker → GHCR |
| SDK | Python (PyPI `jarvisclaw`), Go (`github.com/api-jarvisclaw/go-sdk`) |
| 上游 | BlockRun (blockrun-llm-go v0.17.0) — 80+ AI 模型 |


---

## AIP — Agent Intent Protocol

AIP 是平台面向 AI Agent 的智能路由层，让 Agent 通过声明意图（而非指定模型）获取最优 provider，支持 x402 零注册支付。

### 架构总览

```
┌─────────────────────────────────────────────────────────────┐
│                     AIP Layer (独立路由组)                    │
│                                                             │
│  POST /v1/intent/resolve → IntentEngine → 多维评分 → 排序   │
│  GET  /v1/intent/resolve → ResolveUsage (API 用法说明)      │
│  POST /v1/intent/execute → Resolve + Forward 一步执行       │
│  GET  /v1/intent/types   → Registry 查询支持的意图类型       │
│  GET  /v1/providers      → Registry 查询所有 provider       │
│                                                             │
│  认证: X402OrTokenAuth (x402签名 或 Token 双模式)           │
│  计费: x402 per-request settle ─ 不走 quota/token ratio     │
└─────────────────────────────────────────────────────────────┘
         │                              │
         ▼                              ▼
┌──────────────────────┐      ┌─────────────────────┐
│  IntentEngine        │      │  Executor           │
│                      │      │                     │
│  • Scorer            │      │  • Internal mode    │
│    - price   0.70    │      │    (relay 本平台)   │
│    - quality 0.15    │      │  • External mode    │
│    - latency 0.10    │      │    (proxy 外部URL)  │
│    - reliability 0.05│      │                     │
│    (默认 cost 策略)   │      │  ForwardRequest()   │
│  • Registry          │      │  → 复用 relay 或    │
│    (pricing cache +  │      │     HTTP proxy      │
│     marketplace, 5m) │      │                     │
└──────────────────────┘      └─────────────────────┘
```

### 路由隔离

AIP 路由通过 `SetAIPRouter()` 独立注册在 `/v1/intent/*` 和 `/v1/providers` 路径下：

```go
// router/aip-router.go
func SetAIPRouter(router *gin.Engine) {
    // Public (no auth)
    intentPublic := router.Group("/v1/intent")
    intentPublic.Use(middleware.RouteTag("aip"))
    intentPublic.Use(middleware.GlobalAPIRateLimit())
    {
        intentPublic.POST("/resolve", aipController.Resolve)
        intentPublic.GET("/resolve", aipController.ResolveUsage)
        intentPublic.GET("/types", aipController.ListTypes)
    }

    // Authenticated (x402 or token)
    intentAuth := router.Group("/v1/intent")
    intentAuth.Use(middleware.RouteTag("aip"))
    intentAuth.Use(middleware.X402DiscoveryProbeShortCircuit())
    intentAuth.Use(middleware.X402OrTokenAuth())
    {
        intentAuth.POST("/execute", aipController.Execute)
    }

    router.GET("/v1/providers", middleware.RouteTag("aip"),
        middleware.GlobalAPIRateLimit(), aipController.ListProviders)

    // Wallet routes (session + x402 + token authenticated)
    walletGroup := router.Group("/v1/wallet")
    walletGroup.Use(middleware.RouteTag("aip"))
    walletGroup.Use(middleware.UnifiedAuth())
    {
        walletGroup.GET("/balance", walletController.GetBalance)
        walletGroup.GET("/history", walletController.GetHistory)
        walletGroup.GET("/limits", walletController.GetLimits)
        walletGroup.PUT("/limits", walletController.UpdateLimits)
        walletGroup.GET("/pools", walletController.GetPools)
    }
}
```

- **零侵入**：不修改现有 `/v1/chat/completions` 等路径
- **双模认证**：`X402OrTokenAuth` 同时支持 x402 签名和 Token 认证
- **x402 Discovery**：`X402DiscoveryProbeShortCircuit` 允许 GET /execute 返回 402 发现信息
- **Wallet 子系统**：统一认证下的余额、历史、限额、资金池查询

### 支付流程（x402）

```
Agent 发送 POST /v1/intent/execute
  → X402DiscoveryProbeShortCircuit: GET 请求直接返回 402 + 支付信息
  → X402OrTokenAuth 检查 X-PAYMENT 头 或 Bearer Token
  → 验证签名 (EIP-712 typed data)
  → 验证金额 ≥ 该 intent 定价
  → 放行到 Execute controller
  → Resolve → ForwardRequest → 结算
  → 失败 → 不 settle，Agent 不被扣款
```

**先执行后结算**：Agent 只为成功的请求付费。

### Intent Engine 评分

四维加权评分（`service/aip/scorer.go`），根据 `optimize_for` 策略调整权重：

| 策略 | price 权重 | quality 权重 | latency 权重 | reliability 权重 |
|------|-----------|-------------|-------------|-----------------|
| cost (默认) | 0.70 | 0.15 | 0.10 | 0.05 |
| quality | 0.15 | 0.55 | 0.15 | 0.15 |
| latency | 0.15 | 0.15 | 0.60 | 0.10 |

评分细节：
- **price**: 对数归一化，$0.0001→0.95, $0.01→0.65, $1→0.35，免费模型=1.0
- **quality**: 真实数据(popularity 40% + success_rate 30% + completion_ratio 30%) 与启发式混合（70%/30%）
- **latency**: 线性归一化，P95 0s→1.0, 30s→0.0
- **reliability**: 成功率（来自 ModelMetricsCollector）

### Provider Registry

`ProviderRegistry`（`service/aip/registry.go`）从两个数据源自动刷新，TTL 5 分钟：

1. **Pricing Cache**：从 `model/pricing.go` 获取已配置模型的价格信息（ratio/per-call）
2. **Marketplace**：从 `marketplace_providers` 表获取外部 provider 注册信息

支持：
- 按 `intent_type` 过滤（chat_completion, image_generation, video_generation, text_to_speech, web_search, knowledge_search）
- 按 `features` 过滤（function_calling, vision, streaming 等）
- 实时 metrics（P95 latency、success rate，来自 ModelMetricsCollector）
- Internal mode（复用 relay 本平台 channel）与 External mode（proxy 到外部 URL）

### 与现有系统的关系

```
现有系统 (TokenAuth + quota)          AIP 系统 (x402 / Token 双模)
─────────────────────────             ─────────────────────────────
/v1/chat/completions                  /v1/intent/resolve (免费)
/v1/images/generations                /v1/intent/execute (x402/Token)
/v1/marketplace/*                     /v1/intent/types (免费)
                                      /v1/providers (免费)
                                      /v1/wallet/* (UnifiedAuth)

共享: channels 表作为上游连接池
不共享: 认证、计费、路由逻辑
```

### API 端点汇总

| Method | Path | Auth | 描述 |
|--------|------|------|------|
| GET | `/v1/intent/resolve` | 无 (免费) | 返回 API 用法说明 |
| POST | `/v1/intent/resolve` | 无 (免费) | 声明意图，返回排序后的 provider 列表 |
| POST | `/v1/intent/execute` | x402 签名 / Token | 解析意图 + 执行 + 结算，一步完成 |
| GET | `/v1/intent/execute` | 无 | x402 Discovery Probe，返回 402 + 支付信息 |
| GET | `/v1/intent/types` | 无 (免费) | 列出支持的意图类型 |
| GET | `/v1/providers` | 无 (免费) | 列出所有注册的 provider |
| GET | `/v1/wallet/balance` | UnifiedAuth | 查询钱包余额 |
| GET | `/v1/wallet/history` | UnifiedAuth | 查询交易历史 |
| GET | `/v1/wallet/limits` | UnifiedAuth | 查询消费限额 |
| PUT | `/v1/wallet/limits` | UnifiedAuth | 更新消费限额 |
| GET | `/v1/wallet/pools` | UnifiedAuth | 查询资金池 |

---
