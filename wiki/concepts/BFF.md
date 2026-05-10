---
title: BFF Backend for Frontend
type: concept
tags: [cs, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: BFF 是为特定前端(Web、iOS、Android)定制专属后端聚合层的架构模式,解决多端差异化需求与微服务粒度失配问题,Netflix、SoundCloud 推广后成为主流。
---

# BFF Backend for Frontend

## 定义

**BFF(Backend for Frontend)** 是一种由 Sam Newman 在 SoundCloud 实践后总结的架构模式,字面意为"前端专属后端"。在客户端与下游 [[微服务]] / 数据源之间插入一层薄的聚合服务,**每种前端**(Web、iOS App、Android App、智能电视、Watch 等)对应**一个**专属 BFF。BFF 负责按该端的视图模型聚合、裁剪、改写下游 API,把多端差异化逻辑从前端搬到后端、从公共网关搬到端专属层。

## 核心要点

### 1. 解决的问题

通用 [[API网关]] 或 One-Size-Fits-All API 在多端场景下会暴露三个矛盾:

- **粒度失配**:微服务追求高内聚低耦合,API 偏细粒度;前端一屏要十几个调用,移动端首屏过慢
- **载荷过大**:Web 可以拿大 JSON,Watch、Wearable 想要极简;裁剪逻辑塞前端浪费流量
- **演进不同步**:iOS 上线慢,改 API 必须向后兼容;Web 当晚发版,需要新字段

BFF 让每个前端拥有"贴身定制"的 API 形状与发版节奏。

### 2. 部署形态

```
[Web] → BFF-Web ─┐
[iOS] → BFF-iOS ─┼→ [Microservice A / B / C / Search / Auth]
[Android] → BFF-Android ─┘
```

每个 BFF 由对应前端团队自己拥有(Conway 定律),与下游领域服务由 platform 团队拥有形成正交。

### 3. 与相邻概念区分

- **API 网关**:统一入口,做认证、限流、路由,**所有前端共享**;BFF 是网关下游/旁边的**端专属**层
- **GraphQL**:用 schema 让客户端按需查询字段,某种程度替代了"裁剪载荷"的诉求,可看作"通用 BFF";但 BFF 仍能承担鉴权聚合、第三方调用编排
- **聚合服务(Aggregator)**:概念近似,但 Aggregator 通常业务领域聚合,BFF 强调**为前端体验聚合**

### 4. 实施要点

- 保持 BFF **薄**:聚合 / 改写 / 裁剪 / 协议适配,**不放业务规则**(否则业务逻辑跨 BFF 重复)
- 与对应客户端**同语言**优先(Node 服务 Web、Kotlin 服务 Android),便于团队复用模型
- 每个 BFF 独立部署、独立监控,失败不应跨端蔓延
- 提供良好的下游 client SDK 和服务发现,降低 BFF 编排成本

## 典型应用

- **Netflix**:为 Apple TV、Roku、PS、iOS、Web 各端做端专属 Edge 服务,后演化为 [[GraphQL]] Federation
- **SoundCloud**:Sam Newman 最早提出 BFF 命名场景
- **Spotify、Atlassian、ThoughtWorks**:将 BFF 列入官方架构指南

## 局限与陷阱

- **代码重复**:多个 BFF 可能重复鉴权、重复编排,需抽公共 SDK / 共享库
- **团队边界**:谁拥有 BFF?客户端团队还是后端团队?权属不清会变成"无主之地"
- **维护成本**:N 个前端就是 N 套 BFF,小团队负担重;此时考虑通用网关 + GraphQL 替代
- **"BFF 长肥"**:抵不住业务逻辑往里塞,几年后变成单体,需定期审视边界

## 与其他概念的关系

- 上游入口:[[API网关]] 通常在 BFF 之前
- 下游来源:[[微服务]] 是 BFF 聚合的对象
- 替代方案:[[GraphQL]]、[[REST]] over Aggregator
- 协作模式:[[Conway定律]] 解释为什么按前端组织
- 关联模式:[[API网关模式]]、[[CQRS]]
- 部署形态:常用 [[Serverless]] 或容器化 [[Kubernetes]]

## 参考源

- Sam Newman, *Backends For Frontends* (2015)
- Microsoft Learn, Cloud Design Patterns: Backends for Frontends
- ThoughtWorks Tech Radar
