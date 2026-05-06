---
title: Hypermedia API
type: concept
tags: [cs, web, api, mature]
sources: [raw/计算机/开发学习/语言/HTML/04-知识拓展层/技术生态集成/]
created: 2026-05-05
updated: 2026-05-05
summary: Hypermedia API(HATEOAS)在响应中嵌入下一步可执行链接,让客户端动态发现而非硬编码 URL,是 REST 成熟度模型最高级,实践复杂但 HTMX 让其复兴。
---

# Hypermedia API

## 定义

**Hypermedia API** 指响应中**嵌入可执行的链接**(next, edit, delete...)和操作描述,让客户端不需要硬编码 URL,而是按服务器引导动态导航。在 Roy Fielding 的 [[RESTful API]] 论文中,这就是 **HATEOAS(Hypermedia As The Engine Of Application State)** 约束,被视为 REST 的最高境界(Richardson 成熟度模型 Level 3)。

## 核心要点

### 1. 示例对比

#### 非 HATEOAS(常见)

```json
{
  "id": 42,
  "balance": 100,
  "status": "ACTIVE"
}
```

客户端必须硬编码:`POST /accounts/42/withdraw`、`POST /accounts/42/deposit`...

#### HATEOAS(HAL 风格)

```json
{
  "id": 42,
  "balance": 100,
  "status": "ACTIVE",
  "_links": {
    "self":     { "href": "/accounts/42" },
    "withdraw": { "href": "/accounts/42/withdraw", "method": "POST" },
    "deposit":  { "href": "/accounts/42/deposit",  "method": "POST" },
    "close":    { "href": "/accounts/42/close",    "method": "POST" }
  }
}
```

客户端读 `_links`,无需知道 URL 模板;服务器可以重命名路径而不破坏客户端。

### 2. Richardson Maturity Model

| Level | 描述 | 比喻 |
|---|---|---|
| 0 | RPC over HTTP(单端点 POST) | 沼泽 |
| 1 | 多资源 URL | 部分 REST |
| 2 | HTTP 动词 + 状态码语义 | 多数"REST API" 在此 |
| 3 | HATEOAS / Hypermedia | 真正 RESTful |

### 3. 主流格式

- **HAL**(Hypertext Application Language):简洁,广泛
- **JSON:API**:既有规范,过滤/分页/关系完整
- **Siren**:更结构化,带 actions
- **JSON Hyper-Schema**:与 JSON Schema 联动
- **Mason**、**Collection+JSON**:历史尝试

### 4. 实践挑战

为什么 HATEOAS 实践少?

- 客户端开发更复杂(动态发现 vs 硬编码)
- 文档更难写(URL 不再固定)
- 工具链支持弱(对比 OpenAPI 的成熟)
- 性能开销(更多元数据)
- 移动客户端难以充分利用(代码已编译)

实践中"REST API"多半停在 Level 2,文档 + 客户端 SDK 解决导航问题。

### 5. HTMX 的复兴

[[HTMX]](2020+)让 Hypermedia 思路在前端复兴。服务器返回 HTML 片段,响应头/属性指示客户端如何更新 DOM:

```html
<button hx-post="/like" hx-swap="outerHTML">Like</button>
<!-- 服务器返回:<span>Liked!</span> -->
```

客户端无 JS 状态,服务器 HTML 即应用状态。HATEOAS 在 HTML over wire 范式中天然成立。

### 6. GraphQL 与 Hypermedia 关系

[[GraphQL]] 不是 hypermedia,但 schema 提供类似的"自描述"。客户端通过 introspection 发现可查询字段,与 HATEOAS 精神部分重合,执行模型不同。

### 7. 适用与不适用

**适用**:

- 长生命周期 API,服务器需自由演化
- API 探索式使用(开发者控制台)
- 微浏览器/IoT 通用客户端

**不适用**:

- 高频调用、性能敏感
- 客户端少且自有(直接硬编码更简单)
- 文档驱动的公开 API(OpenAPI 更实际)

### 8. 真实使用

- GitHub API v3(部分 link header)
- PayPal API(HATEOAS 标准化)
- 部分政府开放数据 API
- HTMX 应用

## 关系

- 起源:Roy Fielding REST 论文
- 风格:[[RESTful API]] 最高成熟度
- 替代:OpenAPI 文档驱动
- 复兴:[[HTMX]] HTML over wire
- 标准:HAL、JSON:API

## 参考源

- raw/计算机/开发学习/语言/HTML/04-知识拓展层/技术生态集成/04-3 前后端数据交互.md
