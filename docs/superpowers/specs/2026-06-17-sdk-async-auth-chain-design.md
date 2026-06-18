# SDK 文档补全：异步示例 + 认证兼容性 + 链支持说明

**日期:** 2026-06-17
**范围:** sdk.md, solana.md

## 目标

1. 在 sdk.md 的 Marketplace 部分补充 Python asyncio 和 Go goroutine 异步调用示例
2. 在 sdk.md 初始化部分加认证兼容性表格和链支持说明
3. 在 solana.md 的 Go 代码段加 "Coming Soon" 警告标注

## 改动详情

### 1. sdk.md — 初始化部分加认证与链支持表

位置：`### Initialization` 代码块之后，`## Chat & Streaming` 之前。

新增内容：

```markdown
### Authentication & Chain Support

| Client | API Key | Private Key (x402) | Python 链支持 | Go 链支持 |
|--------|---------|-------------------|--------------|----------|
| ChatClient | ✅ | ✅ | Base + Solana | Base only |
| ImageClient | ✅ | ✅ | Base + Solana | Base only |
| VideoClient | ✅ | ✅ | Base + Solana | Base only |
| AudioClient | ✅ | ✅ | Base + Solana | Base only |
| SearchClient | ✅ | ✅ | Base + Solana | Base only |
| MarketplaceClient | ❌ | ✅ 仅 private key | Base + Solana | Base only |
```

### 2. sdk.md — Marketplace 部分加异步示例

位置：现有 Marketplace code-group `:::` 结束后，`## Balance & Spending` 之前。

新增子节 `### Marketplace (Async / Concurrent)`，包含：
- Python: `jarvisclaw.aio.MarketplaceClient` + `asyncio.gather` 并发调用 prediction/surf/rpc
- Go: goroutine + `sync.WaitGroup` 并发调用同样接口

### 3. solana.md — Go 代码段加 Coming Soon 警告

位置：`## Full example` 下 `::: code-group` 内，Go 代码块之前。

新增：

```markdown
::: warning Go SDK — Coming Soon
Go SDK 暂未支持 Solana 链。以下代码为预期 API 预览，实际使用请等待后续版本。目前 Go 仅支持 Base chain (EVM)。
:::
```

同样在 `## Initialization` 的 Go 代码块前加相同警告。

## 不改动

- async.md — 保持现状
- x402.md — 保持现状
- API Reference 各页 — 不涉及

## 验证

- `npm run docs:build` 编译通过
- 新增表格和代码块渲染正确
