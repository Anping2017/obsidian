---
title: Actix 与 Axum(Rust Web 框架)
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Actix 与 Axum 是 Rust 生态最流行的两个 Web 框架,前者基于 Actor 模型与极致性能著称,后者由 Tokio 团队推出、与 Tower 中间件生态深度整合,二者代表 Rust Web 开发的两条主流路径。
---

# Actix 与 Axum(Rust Web 框架)

## 定义

**Actix Web** 与 **Axum** 是 Rust 语言 Web 框架的两大主力:
- **Actix Web**(2017,Nikolay Kim):基于 Actor 并发模型的异步框架,长期占据 TechEmpower 性能榜首
- **Axum**(2021,Tokio 团队):基于 [[Rust Trait系统]] 与 Tower 中间件生态的现代框架,与 Tokio 异步运行时深度整合

二者代表 Rust 在高性能 Web 服务、AI 推理、边缘计算、加密/区块链后端等场景的主流选择。

## 共同基础:Tokio 与 Hyper

Rust 异步生态以 Tokio 运行时 + Hyper HTTP 库为基础:
- **Tokio**:基于 Future trait 的异步运行时,M:N 调度,数十万并发任务
- **Hyper**:Rust HTTP 1/2 实现,被几乎所有框架使用
- **Tower**:服务抽象与中间件层,Axum/Hyper 共用

这意味着:Actix 与 Axum 性能差距极小,选择更多取决于工程哲学。

## Actix Web 特点

**Actor 并发模型**

借鉴 Erlang/Akka:
- 每个 Actor 独立处理消息
- 消息传递实现并发
- 内部 Actix 库(actor)与 Web 层组合

**极致性能**

TechEmpower 多年榜首,部分原因:
- 早期实现细节优化深
- 高效的请求路由
- 零拷贝 I/O 优化

**Extractor + 同步友好 API**

```rust
async fn greet(name: web::Path<String>) -> impl Responder {
    format!("Hello {}!", name)
}

HttpServer::new(|| App::new().route("/{name}", web::get().to(greet)))
    .bind("127.0.0.1:8080")?
    .run().await
```

## Axum 特点

**Tower 中间件生态共享**

Axum 完全建立在 Tower 之上:
- 与 Hyper、tonic(gRPC)、Tower-HTTP 中间件互通
- ServiceBuilder 链式组装中间件
- 标准化重试、超时、限流、CORS、压缩

**类型驱动的 Extractor**

利用 [[Rust Trait系统]] 把请求各部分(JSON、Path、Query、Header)抽取为参数:

```rust
async fn create_user(
    State(db): State<DbPool>,
    Json(payload): Json<CreateUser>,
) -> impl IntoResponse {
    // ...
}
```

类型不匹配在编译期就报错,这是 Axum 最大优势。

**与 Tokio 生态深度整合**

Axum 由 Tokio 团队主导,与 Tokio、Tower、Hyper 同步发布,生态最连贯。

## Actix vs Axum 对比

| 维度 | Actix Web | Axum |
|---|---|---|
| 并发模型 | Actor + async | 纯 async |
| 性能 | 极高 | 极高(差距 < 5%) |
| 类型安全 | 良好 | 优秀(更严格) |
| 中间件 | 内置 + actix-* | Tower 全生态 |
| 错误处理 | thiserror 风 | 类型 IntoResponse |
| 学习曲线 | 中 | 中 |
| 生态成熟度 | 长期主流 | 新兴主流 |
| 维护 | 单作者主导 | Tokio 团队 |
| 适合 | 长期项目 | 现代项目 |

2023 年起,Axum 因生态整合优势超越 Actix 成为新项目首选,但 Actix 仍是性能榜首的标杆。

## 与其他语言框架对比

| 维度 | Axum | Gin | FastAPI | Spring Boot |
|---|---|---|---|---|
| 语言 | Rust | Go | Python | Java |
| 内存 | 极低 | 极低 | 中 | 高 |
| CPU | 极高效 | 高 | 中 | 中 |
| 启动 | 毫秒 | 毫秒 | 秒 | 秒 |
| 类型安全 | 编译期 | 静态 | 运行时 | 编译期 |
| 学习曲线 | 高 | 低 | 低 | 中 |
| 生态 | 中 | 中 | 中 | 极大 |
| 适合 | 极致性能/安全 | 中等性能服务 | 数据/AI | 企业 |

Rust Web 框架的优势:**编译期保证 + 零运行时开销 + 内存安全**,代价是开发速度比 Go/Python 慢 30-50%。

## 适用场景

**最适合**

- 加密 / 区块链后端
- 高频交易 / 实时系统
- AI 推理服务前端([[Whisper语音识别]] 服务等)
- 边缘函数(Cloudflare Workers Rust SDK)
- 嵌入式 / IoT 后端
- 替代 C++ 写关键路径

**不太适合**

- CRUD 业务系统(Go/Python 更快交付)
- 团队 Rust 经验少
- 需要快速试错的 MVP
- 大量动态元编程的 SaaS

## 中间件与生态

**通用 Tower 中间件(Axum 受益)**

- tower-http:CORS、Compression、Trace、Auth
- tower::limit:并发限制
- tower::timeout:超时
- tower::retry:重试策略
- tower::balance:负载均衡

**Actix 专属**

- actix-cors、actix-session、actix-files
- actix-web-actors:WebSocket Actor

**通用 Rust 库**

- sqlx、Diesel、SeaORM:[[关系型数据库]] ORM
- redis-rs:Redis 客户端
- serde:序列化(JSON、TOML、YAML)
- tracing:结构化日志
- jsonwebtoken:[[JWT]] 认证

## 性能数据

TechEmpower Round 22(2024)前 10 中:
- Rust 框架占多席(Actix、Drogon-rs、Axum)
- 单机 200 万 QPS 量级
- 内存 < 50MB
- P99 < 1ms

Rust Web 框架是当前性能极限的代表。

## 局限

- 编译时间长(对比 Go)
- 借用检查器学习陡峭
- 异步生态相对年轻
- 没有 Spring 那种"开箱即用"
- 团队招聘 Rust 工程师贵且少
- 元编程依赖宏(macro)调试困难

## 何时该选 Rust Web 框架

**应该选**

- 性能/延迟是核心 KPI
- 长期运行服务,运维成本敏感
- 已有 Rust 团队
- 安全要求极高(金融、密码学)

**不该选**

- 业务逻辑复杂多变,语法摩擦影响迭代
- 团队没 Rust 经验
- 需要丰富 ORM、Admin 等"自动化"生态

## 和其他概念的关系

Actix/Axum 是 Rust 在云原生 / 高性能后端的核心工具。它们继承了 [[Rust所有权]] 和 [[Rust Trait系统]] 的零成本抽象哲学,与 [[Go goroutine与channel]] 共同构成系统级语言异步模型的两条路径(M:N async vs CSP)。

在 [[微服务]] 体系下,Rust 服务通常担任性能瓶颈角色——AI 推理代理、加密网关、API 限流层、消息中间件改写等。它们与 [[Kubernetes]]、[[Docker容器]]、[[Prometheus]] 监控的整合已成熟,但生态深度仍不及 [[Spring Boot]]。

## 参考源

- raw/计算机/
- 相关:[[Rust所有权]]、[[Rust Trait系统]]、[[Gin与Echo]]
