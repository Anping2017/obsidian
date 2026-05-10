---
title: Kafka Streams 与 Flink(流处理框架)
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Kafka Streams 是 Kafka 内嵌的轻量流处理库,Flink 是真正实时(毫秒延迟)、强状态管理的分布式流引擎,二者在事件驱动架构、实时分析、风控、CEP 等场景占据不同生态位。
---

# Kafka Streams 与 Flink(流处理框架)

## 定义

**流处理(Stream Processing)** 与批处理对立——数据持续到达,系统持续产出结果(而非"每天跑一次")。它支撑实时风控、推荐系统、监控告警、用户行为分析等场景。

- **Kafka Streams**(2016,Confluent):Kafka 内嵌的 Java 流处理库,部署简单
- **Apache Flink**(2014,Berlin TU → Apache):分布式流处理引擎,毫秒级延迟,强状态管理

二者代表流处理的两条路径——库 vs 平台,简单 vs 强大。[[Apache Spark]] Streaming 是第三选项(微批),三者在不同场景各占优势。

## Kafka Streams

**核心思想**

不是"独立平台",而是"普通 Java 应用 + Streams 库",直接读 Kafka topic、处理、写 Kafka topic。

**示例**

```java
StreamsBuilder builder = new StreamsBuilder();
KStream<String, Order> orders = builder.stream("orders");

KTable<String, Long> userOrderCounts = orders
    .groupBy((key, order) -> order.getUserId())
    .count();

userOrderCounts.toStream().to("user-order-counts", Produced.with(Serdes.String(), Serdes.Long()));

KafkaStreams streams = new KafkaStreams(builder.build(), config);
streams.start();
```

**优势**

- **部署简单**:打包 jar,启动即工作,无需独立集群
- **与 Kafka 紧密**:offset、分区、副本天然集成
- **轻量**:不需 ZooKeeper / Mesos / YARN
- **Exactly-Once 语义**(配合 Kafka transactions)
- **状态存储**:内置 RocksDB,本地维护状态

**局限**

- **限于 JVM**(Java/Scala/Kotlin)
- 复杂窗口、事件时间不及 Flink
- 跨多 Kafka 集群困难
- 不适合 CPU 密集计算

## Apache Flink

**核心思想**

真正的"事件时间"流处理引擎,用 DataStream API 描述计算图,在分布式集群执行。

**示例(Java)**

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
DataStream<Order> orders = env.addSource(new FlinkKafkaConsumer<>("orders", schema, props));

DataStream<UserOrderCount> counts = orders
    .keyBy(Order::getUserId)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new CountAggregator());

counts.addSink(new FlinkKafkaProducer<>("user-counts", schema, props));
env.execute();
```

**关键能力**

- **事件时间(Event Time)**:基于事件本身时间戳处理,与到达时间无关
- **Watermark**:容忍乱序事件
- **State Backend**:内存 / RocksDB / 远程(S3)
- **Savepoint**:有状态作业升级、迁移
- **Exactly-Once**:跨外部系统(Kafka、JDBC)
- **多语言 API**:Java、Scala、Python(PyFlink)
- **SQL**:Flink SQL 标准化

## Flink 架构

```
JobManager(协调者)
   ├── 任务调度
   ├── 检查点协调
   └── 故障恢复

TaskManager(工作者)
   ├── 执行算子
   ├── 本地状态
   └── 与其他 TM 数据 Shuffle
```

可在 Kubernetes、YARN、Mesos、Standalone 部署。

## Kafka Streams vs Flink 对比

| 维度 | Kafka Streams | Flink |
|---|---|---|
| 类型 | 库 | 平台 |
| 部署 | 极简(jar) | 中(集群) |
| 状态 | RocksDB(本地) | RocksDB(本地)+ Checkpoint |
| 延迟 | 毫秒到百毫秒 | 毫秒 |
| Exactly-Once | 支持(限 Kafka) | 全 |
| 事件时间 | 弱 | 强 |
| 复杂事件处理(CEP) | 弱 | 强 |
| SQL | 限定 | 完整 |
| Source / Sink | 仅 Kafka | 数十种(Kafka、JDBC、ES、Pulsar) |
| 学习曲线 | 平 | 陡 |
| 适用 | 简单流逻辑 | 复杂实时系统 |

**经验法则**

- 简单数据流转换、聚合、enrichment → Kafka Streams
- 复杂窗口、CEP、低延迟、跨系统集成 → Flink

## 与 Spark Streaming 对比

| 维度 | Flink | [[Apache Spark]] Streaming |
|---|---|---|
| 模式 | 真正流(逐条) | 微批(秒级) |
| 延迟 | 毫秒 | 秒 |
| 状态 | 强 | 中 |
| 事件时间 | 第一公民 | 支持 |
| 吞吐 | 高 | 极高 |
| 批一体 | 是(批是流的特例) | 是(从批起家) |
| 生态 | 中 | 大 |

近年 Flink 与 Spark 双向学习——Flink 加批支持,Spark Structured Streaming 接近真流。在低延迟、强状态场景 Flink 仍领先。

## 流处理核心概念

**1. 事件时间 vs 处理时间**

- **事件时间**:事件发生时刻(嵌入数据)
- **摄取时间**:进入系统时刻
- **处理时间**:被算子处理时刻

实时分析必须用事件时间——避免时区、网络延迟干扰。

**2. 窗口(Window)**

- **滚动(Tumbling)**:不重叠固定大小(每 5 分钟)
- **滑动(Sliding)**:重叠(每 5 分钟,1 分钟一次)
- **会话(Session)**:基于不活跃间隔自动分组(用户会话)
- **全局(Global)**:无窗口边界,自定义触发

**3. Watermark**

水位线:"我相信事件时间 ≤ T 的所有事件已到达"。
- 触发窗口计算
- 容忍迟到事件(可选 allowedLateness)

**4. State**

- **Keyed State**:按 key 分区(用户的累计金额)
- **Operator State**:每算子实例本地(Kafka offset)
- 可用 RocksDB 持久化(超出内存)

**5. Checkpoint**

定期把所有状态快照到外部存储(S3 / HDFS),故障时恢复。

**6. Savepoint**

手动 Checkpoint,用于:
- 升级 Flink 版本
- 改作业逻辑后恢复
- 跨集群迁移

**7. Exactly-Once**

端到端"恰好一次":Kafka offset、内部状态、外部 Sink 一起提交,无重复无丢失。

## 应用场景

**实时推荐**

用户每次点击 → Flink 更新模型 → 即时生效。

**风控**

转账事件 → Flink 与历史模式对比 → 毫秒级判定 → 拦截或放行。

**实时报表**

电商 GMV 大屏 → Flink 滚动聚合 → 秒级刷新。

**用户行为分析**

会话窗口 → 漏斗、留存、路径 → 实时洞察。

**CDC 与数据同步**

Debezium → Kafka → Flink → 数据仓库 → 准实时数据可分析。

**异常检测**

流模式匹配,如"5 分钟内同 IP 登录失败 10 次"。

**ML 特征**

实时特征工程,与训练 / 推理服务对接。

## Flink SQL

最近重要发展——用 SQL 写流处理:

```sql
CREATE TABLE orders (
    user_id BIGINT,
    amount DECIMAL(10,2),
    order_time TIMESTAMP(3),
    WATERMARK FOR order_time AS order_time - INTERVAL '5' SECOND
) WITH ('connector' = 'kafka', 'topic' = 'orders', ...);

CREATE TABLE user_metrics (...) WITH ('connector' = 'jdbc', ...);

INSERT INTO user_metrics
SELECT
    user_id,
    TUMBLE_START(order_time, INTERVAL '1' HOUR) AS window_start,
    SUM(amount) AS total
FROM orders
GROUP BY user_id, TUMBLE(order_time, INTERVAL '1' HOUR);
```

降低开发门槛,数据分析师也能写流处理。Confluent ksqlDB 是 Kafka Streams SQL 对应。

## 复杂事件处理(CEP)

Flink CEP 检测事件序列模式:

```java
Pattern<Event, ?> pattern = Pattern.<Event>begin("login_fail").times(3).within(Time.minutes(5))
    .next("login_success");
```

风控、欺诈检测主战场。

## 部署模式

**Flink on Kubernetes**

- Flink Operator 模式
- 自动扩缩、故障恢复
- 与云原生栈整合

**Flink on YARN / Standalone**

- 老牌 Hadoop 集群
- 渐被 K8s 取代

**Stateful Functions**

- Flink 子项目
- 写"流应用"像写函数 / Actor
- 无状态服务调用 + 流计算融合

## 局限

**Kafka Streams**

- 不能跨 Kafka 集群
- JVM 限制
- 状态规模受单机限

**Flink**

- 复杂运维(Checkpoint、Savepoint、状态后端)
- 学习曲线陡
- Python(PyFlink)性能不及 Java
- Scala API 减弱(Flink 1.16+)

## 与 AI / LLM

实时流处理在 AI 场景:
- 实时特征(用户行为 → 召回特征)
- 模型服务监控(QPS、延迟、错误率)
- LLM 输出实时安全审核
- Agent 行为流分析

[[Kafka]] + Flink 是实时 AI 系统底层。

## 和其他概念的关系

Kafka Streams / Flink 与 [[Kafka]]、[[Apache Spark]]、[[Apache Airflow]] 共同构成数据处理栈——Airflow 调度批,Spark 大批量,Flink 低延迟流,Kafka Streams 简单流。它们与 [[Lakehouse架构]] 互补——湖仓存全量,流处理动态产出。

它们体现的"事件驱动"思想与 [[Outbox模式]]、[[事件溯源]]、[[Saga模式]] 一脉相承——业务变更 = 事件,系统反应 = 流。在 [[微服务]] 架构中,Kafka + Flink 是跨服务实时数据集成的核心。

实时处理的"延迟、吞吐、一致性、状态"四维度权衡,反映 [[CAP定理]] / [[BASE理论]] 在流场景的具象——不同业务需求选不同框架。

## 参考源

- raw/计算机/
- 相关:[[Kafka]]、[[Apache Spark]]、[[Lambda架构]]
