---
title: API 版本管理
type: concept
tags: [cs, web, api, mature]
sources: [raw/计算机/开发学习/]
created: 2026-05-05
updated: 2026-05-05
summary: API 版本管理是后端在不破坏既有客户端的前提下演进接口的工程实践,主流策略包括 URL/Header/Query 版本、加法不减法、Deprecation 头、并行支持期。
---

# API 版本管理

## 定义

**API 版本管理(API Versioning)** 是后端服务在演进接口时,**不破坏已部署客户端**的工程实践。Web API 一旦发布,移动 App 旧版本、第三方集成、合作伙伴系统会持续调用很久。版本管理是契约稳定性与持续创新之间的平衡机制。

## 核心要点

### 1. 何时需要新版本?

**破坏性变更(Breaking Change)**:

- 删除字段或端点
- 改字段类型(string → int)
- 重命名字段
- 改语义(库存包含/不含预订)
- 改鉴权方式

**非破坏性(向后兼容)** —— 不需新版本:

- 新增字段(客户端忽略未知字段)
- 新增端点
- 新增可选请求参数
- 优化性能

### 2. 版本号策略

#### URL Path

```
/v1/users
/v2/users
```

- 优点:直观、容易缓存、浏览器友好
- 缺点:URL 不再代表唯一资源、迁移工作量大
- 应用:GitHub、Stripe、AWS

#### URL Subdomain

```
https://api.v1.example.com/users
```

少见,更适合大版本。

#### Header

```
GET /users
X-API-Version: 2
Accept: application/vnd.example.v2+json
```

- 优点:URL 干净
- 缺点:浏览器/curl 需配头,文档复杂
- 应用:GitHub(同时支持)、Atlassian

#### Query

```
/users?api-version=2
```

简单但不优雅,适合内部 API。

#### 内容协商

```
Accept: application/vnd.example+json;version=2
```

REST 纯粹主义者推崇,实践中麻烦。

### 3. 渐进式变更最佳实践

1. **加法不减法(Additive)**:新增字段不删除旧字段
2. **Deprecation 期**:旧字段加 `Sunset` / `Deprecation` 响应头,日志告知客户端
3. **N-1 支持**:始终支持当前 + 上一版,3-12 个月迁移期
4. **变更日志**:Changelog 公开发布

```
HTTP/1.1 200 OK
Deprecation: Sun, 11 Nov 2025 23:59:59 GMT
Sunset: Sun, 11 Feb 2026 23:59:59 GMT
Link: <https://api/v2/users>; rel="successor-version"
```

### 4. SemVer 语义化版本

主版本.次版本.补丁(`2.5.3`)

- **主版本**:破坏性变更
- **次版本**:向后兼容新功能
- **补丁**:向后兼容修复

API 通常只暴露主版本号(v1、v2),内部用 SemVer 跟踪小版本。

### 5. GraphQL 的不同思路

[[GraphQL]] 倡导**无版本**:

- 客户端按需取字段,新增字段不影响
- 字段标 `@deprecated` 而不删除
- Schema 持续演化,而非 v1 → v2 大跨步

实践中仍可能有 schema breaking change,需协调。

### 6. RESTful 成熟度模型(Richardson Maturity Model)

| Level | 描述 |
|---|---|
| 0 | RPC over HTTP(单端点) |
| 1 | 多资源 |
| 2 | HTTP 动词 + 状态码语义 |
| 3 | HATEOAS / Hypermedia(响应中带链接) |

详见 [[Hypermedia API]]。HATEOAS 让客户端少硬编码 URL,部分缓解版本痛点,但实践复杂度高。

### 7. 客户端 SDK 策略

公开 API 可发布官方 SDK(JS/Python/Go/Ruby...),封装版本细节。SDK 自身按 SemVer 管理,API 升级在 SDK 内吸收。

### 8. 微服务内部

[[微服务]] 之间通信(常 [[gRPC]] / 内部 REST):

- 强类型契约([[gRPC]] proto 字段编号)
- 同步上线,版本紧凑
- 服务网格做流量切分(Canary 渐进)

### 9. 真实案例

- **Stripe**:URL 不变,Header 指定日期版本(`Stripe-Version: 2024-11-20`),细粒度
- **GitHub**:v3 是 REST,v4 是 GraphQL
- **AWS**:每个服务独立 SDK 版本
- **Google**:Discovery Document 描述 API 版本与字段

## 关系

- 风格:[[RESTful API]]、[[GraphQL]]、[[gRPC]]
- 架构:[[微服务]]、[[API网关模式]]
- 头部:HTTP `Deprecation` / `Sunset`(参考 [[HTTP协议]])
- 进阶:[[Hypermedia API]](HATEOAS)
- 工具:OpenAPI / Swagger / GraphQL Inspector

## 参考源

- raw/计算机/开发学习/语言/HTML/04-知识拓展层/技术生态集成/04-3 前后端数据交互.md
