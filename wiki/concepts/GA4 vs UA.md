---
title: GA4 vs UA
type: concept
tags: [marketing, mature]
sources: [raw/数字营销/]
created: 2026-05-05
updated: 2026-05-05
summary: GA4(Google Analytics 4)与 UA(Universal Analytics)是 Google 分析工具两代产品,2023 年 7 月 1 日 UA 停止收集数据,GA4 强制接管;两者在数据模型、会话定义、事件结构、归因方法、隐私策略五维度有根本差异。
---

# GA4 vs UA

## 定义

GA4(Google Analytics 4)与 UA(Universal Analytics)分别是 Google Analytics 的第四代与第三代产品,前者于 2020 年 10 月正式发布,2023 年 7 月 1 日强制接管数据收集(标准版),2024 年 7 月起 UA 数据全面下线。本概念聚焦两者在底层架构、衡量哲学与实务影响上的差异,是 [[GA4配置]] 之外的对比性视角。

## 五大根本差异

### 1. 数据模型:Event vs Hits

- **UA**:基于 Hits(命中)模型,Hits 分类型(pageview、event、transaction、social),每类型有专门字段。
- **GA4**:全部数据都是 Event(事件),page_view 也是 event,所有 event 共享 25+ 自定义参数。
- **影响**:GA4 灵活性大幅提升,可衡量任意自定义动作;但需重新设计 Tracking Plan。

### 2. 会话定义

- **UA**:30 分钟无活动后会话结束,跨日午夜分裂会话,UTM 变化分裂会话。
- **GA4**:30 分钟无活动结束,午夜不分裂、UTM 变化也不分裂会话——更接近"用户视角"。
- **影响**:GA4 会话数通常比 UA 少,直接对比会"掉数据",需理解口径差异。

### 3. 跨平台与跨设备

- **UA**:Web 和 App 数据分开属性(Property),需通过 Firebase + UA 拼接。
- **GA4**:Web 与 App 在同一属性(Stream)下,跨平台用户旅程天然统一。
- **影响**:解决了 UA 的跨平台跟踪痛点,跨设备分析能力大幅提升。

### 4. 归因模型

- **UA**:默认最终非直接点击(Last Non-Direct),最长 90 天回溯。
- **GA4**:默认数据驱动归因(DDA),基于机器学习按贡献分配,最长 30 天点击+1 天展示。
- **影响**:UA 偏 last-touch,常高估搜索/直接;GA4 更分散,渠道贡献"被稀释",MarTech 团队需重训练判读直觉。

### 5. 隐私与采样

- **UA**:基于 Cookie,受 [[ATT隐私框架]]、ITP、[[Cookie退役]] 严重削弱。
- **GA4**:支持 Consent Mode v2、强制 IP 匿名化、内置数据保留控制(2/14 个月)、支持 BigQuery 免费导出原始数据。
- **影响**:GA4 与隐私法规(GDPR/CCPA)对接更紧,但欧洲多国仍有合规争议(法国、意大利曾判定 GA4 违 GDPR)。

## 主要新增能力(GA4)

1. **预测受众**(Predictive Audiences):购买概率、流失概率内置,可直接用于 Google Ads 投放。
2. **DebugView**:实时调试事件触发与参数,显著提升 GTM 调试体验。
3. **Explore 探索**:漏斗、路径、Cohort、Segment Overlap 等高级分析免费可用(UA 360 才有)。
4. **BigQuery 免费导出**:原始事件级数据每天/小时导出至 BigQuery(原 UA 360 收费)。
5. **更宽松的自定义维度/指标限额**(每属性 50/50)。

## 主要"倒退"(UA 用户的痛点)

1. **bounce rate 概念变化**:GA4 的 Bounce 是 Engagement Rate 的反面,定义不同。
2. **平均会话时长**计算方法变化,与 UA 不可直接对比。
3. **Goal**(目标)概念取消,改为 Conversion Event,设置逻辑大不同。
4. **报表 UI 重新设计**,UA 用户需要长时间适应。
5. **Site Search、Enhanced Ecommerce 等模块**在 GA4 中需要重新配置。

## 迁移最佳实践

1. **双跑期**:UA 不动的同时配置 GA4 接收同样事件,用 6+ 个月并行验证。
2. **重新设计 Tracking Plan**:按 GA4 推荐事件 schema(如 view_item、add_to_cart、purchase)统一命名。
3. **历史数据归档**:UA 数据导出至 BigQuery 或 Looker Studio 保存,7 月后无法在 UA 内访问。
4. **报告模板复刻**:把核心 KPI 报表(渠道、转化、漏斗)在 Looker Studio 用 GA4 数据源重建。
5. **培训受众**:数据分析师、市场、产品全员重新学 GA4 词汇。

## 与其他概念的关系

- 与 [[GA4配置]]:本概念是对比视角,前者是配置实战。
- 与 [[Google Tag Manager]]:GTM 是部署 GA4 的最佳载体。
- 与 [[归因模型]]:GA4 默认 DDA,与 UA 时代多归因模型并存有显著差异。
- 与 [[Marketing Mix Modeling]]:GA4 + BigQuery 是 MMM 数据底层来源。
- 与 [[隐私优先时代]]:GA4 是 Google 应对隐私挑战的核心产品。

## 参考源

- raw/数字营销/02-核心理解层/05-数据驱动/
- Google Analytics Help: GA4 vs UA 官方对比文档
- 业界经典对比:Simo Ahava、Krista Seiden、MeasureSchool 系列博客
