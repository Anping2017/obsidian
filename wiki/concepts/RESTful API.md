---
title: RESTful API
type: concept
tags: [cs, programming, mature]
sources:
  - raw/计算机/开发学习/语言/PHP/04-高级应用层/API开发/01-RESTful API设计.md
  - raw/计算机/开发学习/系统/Odoo/外部集成和接口/自定义 RESTful API 接口.md
  - raw/计算机/开发学习/系统/Wordpress/03-应用开发层/03-高级功能/REST API开发.md
created: 2026-05-05
updated: 2026-05-05
summary: REST 是基于 HTTP 的 API 设计风格,以资源为中心,用统一接口和无状态约束构建可扩展、可缓存的 Web 服务。
---

# RESTful API

## 定义

**REST(REpresentational State Transfer,表述性状态转移)**是 Roy Fielding 在 2000 年博士论文中提出的 Web 架构风格。**RESTful API** 是遵循 REST 约束的 API 设计:把"系统中的事物"抽象为**资源(Resource)**,用 URL 标识,用 [[HTTP协议]]方法(GET/POST/PUT/DELETE)操作,用 JSON/XML 表示其状态。

REST 不是协议、不是标准,是一组**架构约束**。严格符合所有约束的 API 才是真正的 RESTful;Web 上多数 API 是"REST-ish"。

## 核心要点

### 六大约束(Fielding 原文)

1. **客户端-服务器(Client-Server)**:关注点分离,前后端可独立演化
2. **无状态(Stateless)**:每次请求自含全部上下文,服务器不保存会话
3. **可缓存(Cacheable)**:响应必须显式声明可否缓存
4. **统一接口(Uniform Interface)**:核心约束,后述
5. **分层系统(Layered System)**:客户端不知道是直连还是经过代理/CDN
6. **按需代码(Code-on-Demand,可选)**:服务器可发送脚本(如 JS)给客户端

### 统一接口的四个子约束

- **资源标识**:每个资源有唯一 URI,如 /users/42
- **资源表述**:JSON、XML、HTML 等多种表示
- **自描述消息**:每个请求/响应包含足够元信息(Content-Type、状态码)
- **HATEOAS**(Hypermedia as the Engine of Application State):响应中包含相关资源的链接,客户端通过链接驱动状态转移。这是最少被工业实现的约束

### 资源 URL 设计原则

- **名词不动词**:`/users` 而非 `/getUsers`
- **复数形式**:`/users/42` 而非 `/user/42`
- **层级反映关系**:`/users/42/orders/8`
- **过滤、排序、分页**用查询字符串:`/users?status=active&sort=created&page=2`
- **避免动词**:动作映射到 HTTP 方法

### 方法语义对照(Richardson 成熟度模型)

| 操作 | URL | 方法 |
|---|---|---|
| 列表 | /articles | GET |
| 详情 | /articles/42 | GET |
| 创建 | /articles | POST |
| 整体更新 | /articles/42 | PUT |
| 部分更新 | /articles/42 | PATCH |
| 删除 | /articles/42 | DELETE |

### 状态码使用规范

- 200 成功(GET、整体更新)
- 201 已创建(POST 后)
- 204 无内容(DELETE 成功)
- 400 客户端请求错误
- 401 未认证
- 403 已认证但无权
- 404 资源不存在
- 409 冲突(乐观锁失败)
- 422 实体不可处理(校验失败)
- 429 限流
- 500 / 502 / 503 服务端问题

### 版本控制

- URL 版本:/api/v1/users(简单直观,最常见)
- Header 版本:Accept: application/vnd.myapi.v1+json(优雅但不易调试)
- 查询字符串:?version=1

### 认证授权

- **Basic Auth**:Base64 用户名密码,需 HTTPS
- **Bearer Token / JWT**:Authorization: Bearer <token>
- **OAuth 2.0**:第三方授权
- **API Key**:简单场景

### REST vs RPC vs GraphQL

| | REST | gRPC | GraphQL |
|---|---|---|---|
| 风格 | 资源 | 过程 | 查询 |
| 协议 | HTTP/1.1 + JSON | HTTP/2 + Protobuf | HTTP + JSON |
| 性能 | 中 | 高 | 中 |
| 灵活查询 | 弱 | 弱 | 强(客户端选字段) |
| 缓存 | HTTP 缓存原生 | 弱 | 弱 |
| 调试 | 浏览器/curl 友好 | 需工具 | GraphiQL |

REST 是默认选择;gRPC 适合内部服务高性能;GraphQL 适合前端定制查询的复杂场景(Facebook、GitHub API v4)。

### 常见反模式

- 在 URL 中放动词("/getUserById?id=42")
- 把所有错误返回 200 + 自定义 error 字段
- 不用复数,资源名混乱
- 改 PATCH 为 POST(违反幂等约定)
- 不分页,直接返回上千行

## 和其他概念的关系

REST 建立在[[HTTP协议]]语义之上,合理利用 HTTP 缓存、状态码、方法。它是[[微服务]]间通信的最常见风格,也是开放平台 API(GitHub、Stripe、Twilio)的事实标准。

GraphQL、gRPC 是 REST 的补充而非替代:面向不同场景。BFF(Backend For Frontend)、API Gateway 在 REST 之上聚合多个服务。

[[设计模式]]中,REST 类似把所有交互"模型化"为 CRUD;复杂业务流程(如订单流转)硬塞 REST 会扭曲,常用动作(action)子资源 + RPC-style 端点折中处理。

## 参考源

- raw/计算机/开发学习/语言/PHP/04-高级应用层/API开发/01-RESTful API设计.md
- raw/计算机/开发学习/系统/Odoo/外部集成和接口/自定义 RESTful API 接口.md
- raw/计算机/开发学习/系统/Wordpress/03-应用开发层/03-高级功能/REST API开发.md
