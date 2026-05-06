---
title: GraphQL
type: concept
tags: [cs, web, api, frontend, mature]
sources: [raw/计算机/开发学习/语言/HTML/, raw/计算机/开发学习/框架/]
created: 2026-05-05
updated: 2026-05-05
summary: GraphQL 是 Facebook 2015 年开源的 API 查询语言,通过强类型 Schema、客户端按需取数、单端点入口,解决 REST 的过取/欠取问题。
---

# GraphQL

## 定义

**GraphQL** 是 Facebook 2012 年内部开发、2015 年开源的 API 查询语言与运行时。客户端用类似 JSON 的查询语法**精确声明所需字段**,服务器返回结构完全匹配的数据。它定位为 [[RESTful API]] 的替代,核心解决移动端"一次需要拉取多个资源、字段冗余浪费流量"的痛点。

## 核心要点

### 1. 三种操作

- **Query**:读取数据,等价 GET
- **Mutation**:写入/更新,等价 POST/PUT/DELETE
- **Subscription**:订阅推送,基于 [[WebSocket]] 或 [[SSE]]

```graphql
query {
  user(id: "1") {
    name
    posts(first: 5) {
      title
    }
  }
}
```

### 2. Schema 与类型系统

服务端用 SDL(Schema Definition Language)定义类型:

```graphql
type User {
  id: ID!
  name: String!
  posts: [Post!]!
}
```

强类型让编辑器获得自动补全、字段引用追踪,与 [[TypeScript类型系统]] 天然契合(GraphQL Code Generator 自动生成 TS 类型)。

### 3. 解析器(Resolver)

每个字段对应一个 resolver 函数,运行时按 AST 解析顺序调用。N+1 问题靠 DataLoader 批量+缓存解决。

### 4. 解决的问题

| REST 痛点 | GraphQL 方案 |
|---|---|
| 过取(over-fetch):多余字段 | 客户端按需选字段 |
| 欠取(under-fetch):多个端点 | 单查询聚合 |
| 版本管理混乱 | 弃用字段而非新增版本 |
| 文档与实现脱节 | Schema 即文档 |

### 5. 代价

- 服务器复杂度上升(查询深度限制、复杂度限制、缓存难)
- HTTP 层缓存失效(都是 POST /graphql)
- 学习曲线高于 REST
- 不适合简单 CRUD 场景

### 6. 生态

- **Apollo**:客户端+服务端全栈,React 生态首选
- **Relay**:Facebook 官方,Fragment 优先,适合大型 SPA
- **urql**:轻量替代
- **Hasura/PostGraphile**:数据库直接生成 GraphQL API

### 7. 联邦(Federation)

Apollo Federation 让多个微服务的 Schema 合并为统一图,每个 [[微服务]] 拥有自己的子图,网关编排。是大规模场景下的核心能力。

## 关系

- 对比:[[RESTful API]] 是资源中心,GraphQL 是字段中心
- 替代:某些场景下取代 REST,但不取代所有
- 配合:[[微服务]] 架构下 Federation 解决聚合
- 类型:与 [[TypeScript类型系统]] 协同
- 订阅:基于 [[WebSocket]]/[[SSE]]
- 网关:常作为 [[API网关模式]] 的实现

## 参考源

- raw/计算机/开发学习/语言/HTML/04-知识拓展层/技术生态集成/04-3 前后端数据交互.md
