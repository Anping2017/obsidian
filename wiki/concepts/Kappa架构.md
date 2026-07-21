---
title: Kappa架构
type: concept
tags: [cs, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: Kappa 架构是 Jay Kreps 提出的数据架构,用单一流处理管道同时承担实时与批处理需求,以替代 Lambda 架构的双管道复杂度。
---

# Kappa架构

## 定义

**Kappa 架构**由 Confluent 联合创始人、前 LinkedIn 首席工程师 Jay Kreps 在 2014 年提出,核心主张是:**用一条流处理管道同时满足实时分析和历史回放需求**,以替代 Lambda 架构中"批 + 流"双管道带来的代码重复、维护负担与一致性难题。

它的关键洞见:**批处理只是流处理的特例**——只要事件存储足够长(如 Kafka 保留几个月),需要回算历史时,把流任务从最早 offset 重新跑一遍即可。

## 核心要点

### 与 Lambda 架构对比

| 维度 | Lambda | Kappa |
|---|---|---|
| 管道数 | 两条(批 + 流) | 一条(流) |
| 代码 | 重复实现两遍 | 单一逻辑 |
| 一致性 | 批与流口径需对齐 | 天然一致 |
| 历史回算 | 走批通路 | 重放流任务 |
| 复杂度 | 高 | 低 |
| 适合场景 | 批处理仍主导 | 流主导 |

### 架构构成

- **不可变事件日志**:[[Apache Kafka]] 是事实标准,所有原始事件落 Kafka 主题
- **流处理引擎**:Flink、Kafka Streams、Spark Structured Streaming
- **服务层**:实时查询数据库(Druid、ClickHouse、Pinot)或物化视图

### 使用前提

- 流处理引擎能保证 **exactly-once** 语义
- 事件日志保留时间足够覆盖业务回溯需求
- 状态管理与 checkpoint 机制成熟

### 重新计算流程

发现逻辑 bug → 修复代码 → 启动新版本任务,从 offset 0 消费 → 写入新表 → 切换查询路由。无需停服,无需另写批任务。

### 实践中的模糊地带

纯 Kappa 在大数据量长历史场景的成本很高,实际工程常呈"近 Kappa":短时间窗用流,极冷数据落湖仓做批。完美的 Kappa 仍稀少。

## 应用场景

- **Uber、LinkedIn、Netflix** 的实时指标平台
- **金融实时风控**:每笔交易毫秒级判定
- **物联网遥测**:数百万设备状态汇聚
- **推荐系统**:特征实时更新

## 局限与陷阱

- **事件日志存储成本**:Kafka 长期保留 PB 级数据 → 存储账单很高
- **流引擎调试难**:状态、时间窗、迟到事件的复杂度不低
- **一次性回算成本**:大规模 reprocessing 仍是几小时甚至几天
- **不是所有场景都适合**:OLAP 复杂多维分析仍偏好批

## 与其他概念的关系

- 直接对比 [[Lambda架构]],解决其复杂度
- 依赖 [[Apache Kafka]] 作为不可变事件日志
- 流处理引擎:[[Apache Flink]]、Kafka Streams
- 与 [[数据湖]] / [[数据仓库]] / [[数据湖仓]] 互补使用
- 一致性依赖 [[exactly-once]] 语义保证
- 与 [[CDC]]、[[事件驱动架构]] 是天然组合

## 参考源

- Jay Kreps, *Questioning the Lambda Architecture* (O'Reilly, 2014)
- Confluent / Apache Kafka 官方文档
