---
title: Lambda 架构
type: concept
tags: [cs, distributed, mature]
sources: [raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md]
created: 2026-05-05
updated: 2026-05-05
summary: Lambda 架构通过批处理层+速度层+服务层的三层并行,既保证历史数据准确又提供实时视图,是大数据时代的经典折中,Kappa 架构主张用流处理统一替代。
---

# Lambda 架构

## 定义

**Lambda 架构(Lambda Architecture)** 是 Nathan Marz(Storm 作者)2011 年提出的大数据处理架构,通过**批处理层 + 速度层 + 服务层**并行运行,既保证历史数据准确(批层重算)又提供实时视图(流层近似)。**Kappa 架构** 是 Jay Kreps(Confluent / Kafka 作者)2014 年提出的简化方案,主张用单一流处理引擎替代两层。

## 核心要点

- **Lambda 三层**
  - **批处理层(Batch Layer)**
    - 定时(每天 / 每小时)对全量历史数据重新计算
    - 输出"批视图(Batch View)"
    - 引擎:Spark / Hadoop MR
    - **特点**:准确、吞吐高、延迟高
  - **速度层(Speed Layer)**
    - 处理最新事件,生成"实时视图(Real-time View)"
    - 引擎:[[流处理]](Storm / Flink / Spark Streaming)
    - **特点**:延迟低、近似准确(可能丢失或重复)
  - **服务层(Serving Layer)**
    - 合并批视图 + 实时视图,对外提供查询
    - 存储:Druid / Cassandra / HBase / 自研
    - 查询时:历史用批视图、最近用实时视图
- **Lambda 优势**
  - **准确性**:批层重新计算,修正速度层误差
  - **容错**:批层是"事实之源",任何错误最终被批校正
  - **实时性**:速度层提供秒级延迟视图
- **Lambda 痛点**
  - **代码重复**:同一逻辑在批和流引擎各写一遍
  - **运维复杂**:两套引擎、两套数据流、两套监控
  - **数据一致性难**:批和流计算结果可能有微小差异
  - **学习曲线**:开发者要懂两套范式
- **Kappa 架构(简化)**
  - 只保留 [[流处理]] 一层
  - 历史数据视为流的"重放"
  - 数据存于持久化日志(Kafka 长保留),需要重算时重放即可
  - **优势**:单一引擎、单一代码、运维简单
  - **挑战**:对流处理引擎要求高(状态管理、精确一次、回放支持)
  - 适合 Flink + Kafka 场景
- **Lambda vs Kappa**

| 维度 | Lambda | Kappa |
|---|---|---|
| 引擎 | 批 + 流 | 仅流 |
| 代码 | 双份 | 单份 |
| 运维复杂度 | 高 | 中 |
| 数据回放 | 批层全量重算 | 流引擎回放 Kafka |
| 适合规模 | 超大规模 + 历史敏感 | 中大规模 + 流为主 |
| 代表生态 | Hadoop + Storm/Flink | Flink + Kafka |

- **现代演进:批流融合**
  - **Apache Flink** 把批视为有界流,同一 API 同一引擎
  - **Apache Beam** 抽象统一编程模型,后端可选 Flink/Spark/Dataflow
  - **Dataflow Model**(Google)论文奠基批流统一
  - **数据湖仓(Lakehouse)**:Delta Lake / Iceberg / Hudi 在湖上加 ACID,批 + 流写入同一表
- **典型实现**
  - **传统 Lambda**:Hadoop(批) + Storm(流) + HBase(服务)
  - **现代 Lambda**:Spark(批) + Flink(流) + Druid/ClickHouse(服务)
  - **Kappa**:Flink + Kafka + ClickHouse
  - **Lakehouse**:Delta Lake on S3 + Spark Structured Streaming
- **何时选择**
  - **优先 Kappa / 批流融合**:新项目、实时为主、规模适中
  - **必须 Lambda**:遗留批系统重投资、超大规模历史数据、批结果有合规要求
- **架构选型考量**
  - **数据量**:PB 级历史 + 实时 → Lambda;TB 级以下 → Kappa 足够
  - **延迟需求**:秒级以内 → 流为主;分钟级 → 批为主
  - **团队能力**:流处理经验是 Kappa 必要条件

## 和其他概念的关系

Lambda / Kappa 是 [[批处理]] 与 [[流处理]] 协同 / 替代的两种顶层架构哲学。它们围绕 [[消息队列]](Kafka)和 [[数据仓库]] / 数据湖构建。

[[一致性模型]] 在两种架构中表现不同:Lambda 通过批层最终修正,Kappa 通过 [[幂等性]] 与精确一次保证。

数据存储依赖 [[列式存储]](Parquet / ORC)与对象存储(S3 / HDFS)。

[[微服务]] 中事件驱动架构本质是 Kappa 思想的应用层映射:以事件流为脉络,各服务订阅 / 处理 / 存档。

[[可观测性三支柱]] 中实时指标聚合通常用 Kappa 风格:Prometheus 采集 → Kafka → Flink → 时序库。

## 参考源

- raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md(数据层)
- raw/计算机/运维知识/云服务/云服务器知识地图.md(实时数据分析)
