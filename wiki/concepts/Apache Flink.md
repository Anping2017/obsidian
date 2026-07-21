---
title: Apache Flink
type: concept
tags: [cs, distributed, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: Apache Flink 是开源的分布式流处理引擎,以事件时间、强状态管理、exactly-once 与毫秒级延迟著称,是实时数据管道与流式分析的事实标准之一。
---

# Apache Flink

## 定义

**Apache Flink** 是发源于柏林工业大学 Stratosphere 项目、2014 年捐赠给 Apache 基金会的**分布式流处理引擎**。它把"批是流的特例"作为核心抽象,提供:

- **真流式**(逐条处理,而非微批)
- **事件时间(Event Time)**为第一公民
- **有状态计算**:大状态 + Checkpoint + Savepoint
- **Exactly-Once** 端到端语义
- **流批一体** 的 DataStream / Table / SQL API

Flink 与 [[Apache Kafka]] 配合,构成实时数据管道的事实组合;在低延迟、强状态场景上,优于微批的 [[Apache Spark]] Structured Streaming。

## 核心要点

### 架构

```
JobManager(协调者)
   ├── 任务调度
   ├── 检查点(Checkpoint)协调
   └── 故障恢复

TaskManager(工作者)
   ├── 执行算子
   ├── 本地状态(RocksDB)
   └── 与其他 TM 数据 Shuffle
```

部署目标:Kubernetes(Flink Operator)、YARN、Mesos、Standalone。

### 事件时间与 Watermark

- **事件时间**:事件本身发生的时间(嵌入数据),不受网络延迟干扰
- **处理时间**:算子接收到事件的时间
- **Watermark**:"我相信事件时间 ≤ T 的事件都到了" → 触发窗口计算
- **AllowedLateness**:对迟到事件的容忍窗口

事件时间是 Flink 与 Kafka Streams、Spark Streaming 拉开差距的核心能力——金融、IoT、用户行为分析必须按事件时间口径。

### 窗口

| 类型 | 描述 |
|---|---|
| Tumbling | 不重叠固定大小(每 5 分钟) |
| Sliding | 重叠(每 5 分钟,1 分钟步进) |
| Session | 基于不活跃间隔自动分组(用户会话) |
| Global | 无边界,自定义触发 |

### 状态管理

- **Keyed State**:按 key 分区(每用户累计金额)
- **Operator State**:每算子实例本地(Kafka offset)
- **State Backend**:Memory / FileSystem / RocksDB / 远程(S3)
- **Checkpoint**:周期把状态快照到外部存储,故障 5-30 秒内恢复
- **Savepoint**:手动快照,用于版本升级、跨集群迁移、A/B 切换

### Exactly-Once

跨外部系统的端到端"恰好一次":Kafka offset、内部状态、外部 Sink(Kafka / JDBC / Hudi)通过两阶段提交协议一起原子提交,无重复无丢失。

### Flink SQL

最近重大演进——把流处理写成 SQL:

```sql
SELECT user_id,
       TUMBLE_START(order_time, INTERVAL '1' HOUR) AS window_start,
       SUM(amount) AS total
FROM orders
GROUP BY user_id, TUMBLE(order_time, INTERVAL '1' HOUR);
```

数据分析师不必写 Java 即可上手,推动 Flink 从"工程师工具"扩展到"数据工程师工具"。

### 复杂事件处理(CEP)

`Pattern.begin("login_fail").times(3).within(Time.minutes(5)).next("login_success")` —— 风控、欺诈检测、运维异常检测的天然抽象。

## 典型应用

- **实时风控**:转账事件 → 历史模式对比 → 毫秒判定 → 拦截或放行
- **实时推荐**:用户行为 → 特征更新 → 召回排序实时刷新
- **实时数仓**:Debezium + Kafka + Flink + ClickHouse/StarRocks → 秒级 BI
- **实时大屏**:电商 GMV、直播间数据
- **CEP**:欺诈检测、监控告警
- **代表用户**:阿里巴巴(双 11 实时大屏)、Uber、Netflix、Lyft、字节跳动

## 局限与陷阱

- **运维复杂**:Checkpoint、Savepoint、State Backend、Watermark 调优都有学习曲线
- **PyFlink 性能**:Python API 比 Java/Scala 慢一档,Scala API 自 1.16 起淡出
- **资源占用**:JobManager + TaskManager + State Backend,小作业显得"重"
- **大状态成本**:RocksDB + S3 长期存储费用可观
- **延迟与吞吐权衡**:为追毫秒延迟,常需牺牲一些吞吐与压缩
- **不是所有场景都该流化**:OLAP 多维分析、离线训练仍偏向 [[Apache Spark]]

## 与其他概念的关系

- 与 Kafka 的组合见 [[Kafka Streams与Flink]]

- 与 [[Apache Kafka]] 深度配合:Kafka 提供事件日志,Flink 做计算
- 是 [[Kappa架构]] 与 [[Lambda架构]] 中流通路的主力引擎
- 与 [[Apache Spark]] Streaming 互为参照:真流 vs 微批,各占场景
- 与 Kafka Streams 同为流处理框架,定位差异:平台 vs 库
- 与 [[流处理]] / [[批处理]] 概念紧密绑定
- 输出常入 [[数据仓库]] / [[数据湖]] / [[Lakehouse架构]]
- 调度可由 [[Apache Airflow]] 触发,运行在 [[Kubernetes]]
- 与 [[事件驱动架构]]、[[事件溯源]] 是天然组合

## 参考源

- Flink 官方文档 https://flink.apache.org/
- *Stream Processing with Apache Flink* (O'Reilly, Fabian Hueske & Vasiliki Kalavri)
- Apache Flink 社区 FLIP(Flink Improvement Proposals)
