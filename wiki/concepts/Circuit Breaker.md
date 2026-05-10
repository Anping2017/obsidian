---
title: Circuit Breaker 熔断器模式
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: 熔断器模式监控对依赖服务的调用,失败率超阈值时主动切断后续调用、快速失败,等冷却期后试探恢复,在分布式系统中防止故障雪崩、保护下游与自身的关键弹性模式。
---

# Circuit Breaker 熔断器模式

## 定义

**Circuit Breaker(熔断器)** 是 Michael Nygard 在《Release It!》(2007)中系统化的弹性设计模式,灵感来自电路熔断器:**故障达到阈值时主动切断回路,保护下游电器;冷却后试探恢复**。

在分布式系统中,它解决的核心问题:**当依赖服务出问题时,如何避免持续发起注定失败的请求,导致连锁雪崩**。

它由 Martin Fowler 在 2014 年的 Bliki 文章中进一步推广,成为 [[微服务]] 必备模式之一。

## 为什么需要

**经典故障雪崩**

服务 A → 服务 B → 数据库

数据库慢了:
1. 服务 B 响应变慢(线程阻塞等数据库)
2. 服务 A 调 B 也慢,A 的线程也阻塞
3. A 的线程池满 → A 自己也不响应
4. 上游服务调 A 超时,继续阻塞
5. 整个调用链所有服务挂

**根因**:每个服务都"忠实"地等待依赖,故障传染。

**熔断器价值**

A 调 B 失败率高时,A 主动停止调 B,**快速返回失败**(返回降级数据或错误)。这样:
- A 自己的线程不被拖死
- B 有恢复时间(无新流量打)
- 系统其他部分可继续工作

## 三态状态机

```
   [Closed] -- 失败超阈值 --> [Open]
       ^                         |
       |                         | 等待 timeout
       |                         v
       +---- 试探成功 -- [Half-Open]
                            |
                            +-- 试探失败 --> [Open]
```

**Closed(闭合,正常)**

- 请求正常通过
- 计数失败次数 / 比率
- 阈值触发 → 进入 Open

**Open(熔断,拒绝)**

- 直接快速失败,不调用下游
- 等待 cooldown 时间(通常 5-60s)
- 时间到 → Half-Open

**Half-Open(半开,试探)**

- 允许少量请求(如 1 个)通过
- 成功 → 回到 Closed
- 失败 → 回到 Open(再 cooldown)

## 关键参数

**失败定义**

- HTTP 5xx
- 超时
- 连接错误
- 自定义业务错误

**失败阈值**

- 绝对数:连续 N 次失败
- 比率:窗口期内 50% 失败
- 滑动窗口:近 10 次中 5 次失败

**Cooldown 时间**

- 短(1-5s):快速试探
- 长(30-60s):给依赖更多恢复时间
- 自适应(指数退避)

**最小请求数**

低流量时少量失败不应触发(噪音):
- 至少 20 次请求才计算比率

## 配套模式

**1. Bulkhead(隔板)**

线程池 / 信号量隔离:
- 调每个依赖的线程独立
- 一个依赖慢不拖垮整体
- 类似船舶舱壁("一舱进水不沉船")

**2. Fallback(降级)**

熔断时返回什么?
- 缓存值
- 默认值
- 简化版结果
- 友好错误信息("服务暂时不可用")

**3. Retry(重试)**

注意:**不是所有失败都该重试**。
- 4xx 客户端错误不应重试(无效请求)
- 5xx 可重试(可能临时)
- 重试次数限(最多 3 次)
- 退避策略(指数 + jitter)
- 与 Circuit Breaker 协同(熔断时不重试)

**4. Timeout(超时)**

每个调用设合理超时:
- 慢依赖立刻失败
- 与熔断器协同——超时算"失败"

**5. Rate Limiter(限流)**

控制下游流量,防止冲击:
- Token Bucket
- Leaky Bucket
- 与熔断器互补

## 实现库

**Java**

- **Hystrix(2012,Netflix)**:经典,2018 年停止维护
- **Resilience4j(2017+)**:Hystrix 继任者,模块化、Java 8+
- **Sentinel(阿里)**:中文社区强,Spring Cloud Alibaba 集成
- **Failsafe**:轻量

**.NET**

- Polly:Retry / Circuit Breaker / Fallback / Bulkhead 全套

**Go**

- sony/gobreaker
- afex/hystrix-go

**Python**

- pybreaker
- circuitbreaker

**JavaScript**

- opossum

## Resilience4j 示例(Java)

```java
CircuitBreakerConfig config = CircuitBreakerConfig.custom()
    .failureRateThreshold(50)              // 50% 失败率熔断
    .waitDurationInOpenState(Duration.ofSeconds(10))
    .slidingWindowSize(10)                  // 滑动窗口 10 请求
    .minimumNumberOfCalls(5)
    .build();

CircuitBreaker cb = CircuitBreaker.of("paymentService", config);

Supplier<Payment> decorated = CircuitBreaker.decorateSupplier(cb, () -> paymentService.charge(order));
Supplier<Payment> withFallback = Decorators.ofSupplier(decorated)
    .withFallback(Arrays.asList(Throwable.class), e -> Payment.pending())
    .decorate();

Payment p = withFallback.get();
```

## 服务网格层熔断

[[服务网格]](Istio / Linkerd)在 Sidecar 层实现熔断,业务代码无需感知:

**Istio DestinationRule**

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: my-service
spec:
  host: my-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        maxRequestsPerConnection: 10
    outlierDetection:           # 离群检测 = 熔断
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```

代码层 + Mesh 层双重熔断在大型系统常见。

## 设计要点

**1. 区分超时与失败**

慢调用比错误更危险——线程被拖住但不算"失败"。需配合 timeout 把慢调用计为失败。

**2. 熔断粒度**

- 服务级(My Service → Payment Service):粗
- 实例级(每个 Pod):细
- 操作级(每个 API endpoint):最细

通常服务+操作级别最实用。

**3. 监控**

熔断器状态、Trip 次数、Fallback 频率应该是仪表盘核心指标。频繁熔断 = 下游可能真的不健康。

**4. 不熔断什么**

- 自家数据库慢:熔断后业务做不了任何事,改慢请求 / 队列降级更合适
- 关键链路:熔断后用户体验崩溃,需慎重(但快速失败 + 友好提示总好过卡死)

**5. 测试**

定期注入故障(混沌工程):
- Chaos Monkey
- 模拟下游 500
- 模拟超时
- 验证熔断生效、Fallback 正确

## 反模式

**1. 熔断器永远 Open**

下游真的死了,所有请求都熔断。这时上游应有更高级降级——切流量到备用区域、返回 503。

**2. Fallback 又调依赖**

Fallback 调另一个依赖,后者也挂 → 又熔断。Fallback 应是简单本地操作。

**3. 熔断器自身是单点**

集中熔断器(Hystrix Dashboard 时代)有单点风险。现代库都是本地熔断器 + 全局监控。

**4. 调用方不感知**

应用代码不知道熔断器存在,行为难以推理。应在 SDK 层显式封装。

## 与限流(Rate Limiter)的区别

| 维度 | Circuit Breaker | Rate Limiter |
|---|---|---|
| 目的 | 保护被调方,加速失败 | 控制流量,保护自己 |
| 触发 | 失败率高 | 流量超阈值 |
| 行为 | 全部拒绝 | 部分拒绝 |
| 状态 | 三态 | 累积 / 滑动 |
| 位置 | 调用方 / Mesh | 调用方 / 网关 |

二者互补:限流保护被调方不被打挂,熔断保护调用方不被拖垮。

## 局限

- 阈值调优困难(误熔断 vs 错过故障)
- Half-Open 试探可能继续打扰恢复中的下游
- 多依赖串联熔断行为复杂
- 与重试、超时、降级协调要小心
- 异步场景(消息队列)不直接适用

## 和其他概念的关系

Circuit Breaker 与 [[微服务]] / [[服务网格]] 体系密不可分,与 Bulkhead、Retry、Timeout、Fallback、Rate Limiter 共同构成"弹性模式"工具集。它在 [[Saga模式]]、[[Outbox模式]] 之外提供另一种分布式可靠性保障。

它的"快速失败"哲学源自 [[设计原则SOLID]] 之外的"Fail Fast"原则——出问题立刻显形,不积累。这与 [[Sentry]]、[[分布式追踪]] 等可观测工具配合,让故障快速被人类发现。

在 [[Kubernetes]] / [[Istio与Linkerd]] 部署中,熔断逐渐从代码下沉到平台层,业务代码越来越轻量,这是 [[微服务]] 演进的一般规律。

## 参考源

- raw/计算机/
- 相关:[[微服务]]、[[服务网格]]、[[Saga模式]]
