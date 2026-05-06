---
title: API 网关模式
type: concept
tags: [cs, web, architecture, mature]
sources: [raw/计算机/开发学习/中间层/, raw/计算机/开发学习/新技术/]
created: 2026-05-05
updated: 2026-05-05
summary: API 网关是位于客户端与后端服务之间的统一入口,集中处理路由、鉴权、限流、聚合、协议转换、监控,是微服务架构的核心基础设施。
---

# API 网关模式

## 定义

**API 网关(API Gateway)** 是位于客户端与后端服务之间的**统一入口层**,负责把外部请求路由到内部一个或多个 [[微服务]],并集中处理跨服务的横切关注点:身份验证、限流、缓存、监控、协议转换、聚合。它是微服务架构的标准模式之一,Netflix 在 2013 年的 Zuul 是早期奠基者。

## 核心要点

### 1. 解决的问题

无网关时,客户端直接调多个后端:

- N 个服务地址,客户端要知道全部
- 每个服务独立鉴权、限流(代码重复)
- CORS、HTTPS、压缩等到处配置
- 协议异构([[gRPC]] 内部、[[RESTful API]] 外部)
- 移动端为节省请求需聚合数据

### 2. 网关核心职责

| 职责 | 说明 |
|---|---|
| **路由** | URL/Header → 后端服务 |
| **认证** | [[JWT]] / [[OAuth 2.0]] / API Key 校验 |
| **授权** | 角色/范围检查 |
| **限流** | 每用户/IP/Token 限流 |
| **熔断** | 后端故障时快速失败 |
| **缓存** | 热点响应缓存 |
| **聚合(BFF)** | 一个客户端请求 → 多个后端 → 合并响应 |
| **协议转换** | REST ↔ gRPC ↔ GraphQL ↔ WebSocket |
| **日志/追踪** | 统一接入 OpenTelemetry |
| **请求/响应转换** | 字段重命名、格式转换 |

### 3. 主流网关产品

#### 自建轻量(代码型)

- **[[Express框架]] / Koa / Fastify**:Node 写,简单灵活
- **NestJS**:全功能 Node
- **Spring Cloud Gateway**:Java 生态

#### 配置型(企业)

- **Kong**:Lua + Nginx,插件丰富,社区/企业版
- **Apache APISIX**:Go + Lua,云原生
- **Tyk**:Go,API 管理强
- **AWS API Gateway**:云托管
- **Azure API Management**、**Google Cloud Endpoints / Apigee**

#### 边缘型

- **Cloudflare API Gateway**(基于 Workers)
- **Fastly**(VCL)
- **Vercel Edge Middleware**

#### 服务网格(Service Mesh)

- **Istio Ingress Gateway**(Envoy)
- **Linkerd**

### 4. BFF(Backend for Frontend)模式

变种:**为每个客户端类型(Web、iOS、Android、桌面)单独建网关**,聚合后端服务为该客户端最优 API。

- Web:[[GraphQL]] 或 REST 聚合
- iOS:精简字段,合并请求
- IoT:[[gRPC]] 高效

### 5. 网关与 [[微服务]] 协作

```
Client
   │
   ▼
API Gateway ──→ Auth Service
   │            ↓ 验证 JWT
   ├──→ Order Service
   ├──→ Inventory Service
   └──→ Payment Service
        ↑ 内部互相 gRPC 调用
```

服务间通信可绕过网关(性能),仅外部入口经过网关。

### 6. 反模式与陷阱

- **过度集中逻辑**:网关塞业务,变成"分布式单体"
- **单点故障**:无高可用部署 → 整站挂
- **延迟累加**:每跳 RTT,需精简
- **版本管理**:网关 + 后端服务版本冲突

最佳实践:网关只做横切关注点,业务在服务内。

### 7. 与反向代理区别

| 维度 | 反向代理(Nginx) | API 网关 |
|---|---|---|
| 主要功能 | 转发、负载均衡 | 转发 + 业务逻辑 |
| 协议感知 | TCP/HTTP 层 | API 语义层 |
| 鉴权 | 简单 | 复杂(JWT、OAuth、API Key) |
| 限流 | 简单(基于 IP) | 复杂(基于用户、租户) |
| 监控 | 流量级 | 接口级 |
| 配置 | 静态文件 | 动态(数据库/控制台) |

### 8. 与 GraphQL Federation 对比

[[GraphQL]] Federation 是 GraphQL 原生的网关概念,把多个子图聚合为统一 schema。可视为 GraphQL 专用的 API 网关。

### 9. 安全考量

- 网关是攻击面集中点 → DDoS / WAF 防护
- 解密 TLS → 私钥管理
- 鉴权信息在网关 → 后端可信任(但需防伪造首部)

## 关系

- 配合:[[微服务]] 架构
- 替代:无网关的客户端直连
- 协议:统一对外 [[RESTful API]] / [[GraphQL]] / [[gRPC]]
- 安全:[[OAuth 2.0]] / [[JWT]] / [[Web安全]]
- 部署:Kubernetes Ingress + 网关
- 边缘:[[Edge计算]] 网关下沉

## 参考源

- raw/计算机/开发学习/中间层/iPaaS.md
- raw/计算机/开发学习/中间层/MuleSoft.md
- raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md
