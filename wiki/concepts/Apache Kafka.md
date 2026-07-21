---
title: Apache Kafka
type: concept
tags: [cs, distributed, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: Apache Kafka 是分布式发布订阅消息系统与流处理平台,以分区化、可持久化、可重放的提交日志为核心抽象,成为事件流处理与实时数据管道的事实标准。
---

# Apache Kafka

## 定义

**Apache Kafka** 是 LinkedIn 2010 年开发、2011 年开源、现为 Apache 顶级项目的**分布式发布/订阅消息系统与流处理平台**。其根本创新是把消息抽象为**"分布式、可持久化、可重放的提交日志(Commit Log)"**——而非传统消息队列那种"投递即消失"的语义。

Kafka 一身兼任四种角色:

- **消息中间件**(对照 RabbitMQ、ActiveMQ)
- **数据管道**(对照 Flume、Logstash)
- **流处理底层**(配合 Kafka Streams、[[Apache Flink]]、Spark Streaming)
- **事件溯源**(Event Sourcing)与变更数据捕获(CDC)的事实标准

## 核心要点

### 关键概念

| 概念 | 含义 |
|---|---|
| Topic | 消息类别,按主题分门别类 |
| Partition | Topic 内的物理分片,水平扩展单元 |
| Offset | Partition 内每条消息的有序编号 |
| Producer | 写入消息的客户端 |
| Consumer | 读取消息的客户端 |
| Consumer Group | 消费者组,组内 partition 互斥分配 |
| Broker | Kafka 集群的一台节点 |
| Replica | Partition 的副本,Leader + Follower |
| ISR | In-Sync Replicas,与 Leader 同步的副本集 |
| Controller | 集群元数据管理者(KRaft 已替代 ZooKeeper) |

### 高性能架构特征

- **分区水平扩展**:Topic 可分为数百上千个 partition,分布到多 broker
- **顺序写磁盘**:利用顺序写比内存随机访问还快的硬件特性
- **零拷贝(sendfile)**:数据从磁盘直接到网卡,绕过用户态
- **批量与压缩**:Producer 批量打包,broker 端再压缩
- **副本与高可用**:Leader 接收读写,ISR 同步;Leader 故障由 Controller 选举

单集群百万级 QPS、PB 级数据保留都是常规水平。

### 与传统 MQ 的区别

| 维度 | 传统 MQ(RabbitMQ) | Kafka |
|---|---|---|
| 消息模型 | 队列 / 主题 | 分布式提交日志 |
| 投递语义 | 投递即删 | 保留期内可重放 |
| 顺序保证 | 队列内有序 | Partition 内有序 |
| 吞吐 | 高 | 极高(10w-100w+ msg/s) |
| 延迟 | 低(亚 ms) | 中(ms 到 10ms) |
| 用途 | 命令、任务调度 | 事件流、数据管道、日志聚合 |

### KRaft 与去 ZooKeeper

Kafka 历史依赖 ZooKeeper 管理元数据,运维复杂。2022 年 KRaft 模式 GA,用 Raft 协议自管理元数据,部署从两套集群降为一套,见 [[Raft共识算法]]。

### 生态组件

- **Kafka Connect**:声明式接入数据库 / S3 / Elasticsearch 等数百种 source/sink
- **Schema Registry**:消息 schema 版本化(Avro / Protobuf / JSON Schema)
- **Kafka Streams**:JVM 内嵌的轻量流处理库
- **MirrorMaker 2**:跨数据中心复制
- **ksqlDB**:用 SQL 写流处理

## 典型应用 / 主要厂商

- **日志聚合**:应用日志 → Kafka → [[ELK Stack]]
- **事件总线**:微服务解耦,见 [[微服务]]
- **流处理底座**:Kafka + Flink / Spark Streaming
- **CDC**:Debezium → Kafka → 数据湖 / 数仓
- **用户行为追踪**:页面事件 → Kafka → 分析栈
- **IoT 数据接入**:百万设备遥测
- **托管服务**:Confluent Cloud(原厂)、AWS MSK、Aiven、Redpanda(C++ 兼容实现)

## 局限与陷阱

- **存储成本**:长保留期 + 多副本 → PB 级存储,云上账单陡峭
- **运维复杂**:分区规划、ISR 调优、再均衡风暴、消费者位移管理
- **重复消费**:默认 at-least-once,exactly-once 需事务 + 幂等 producer
- **大消息不友好**:几 MB 以上的消息会拖垮 broker,需要对象存储 + 引用
- **消息顺序粒度限于 partition**:跨 partition 全局有序需要单 partition 拓扑
- **小集群成本高**:即便很小的负载,也需 3+ broker 做高可用
- **替代选项**:Pulsar(分层存储)、Redpanda(无 JVM)、NATS JetStream

## 与其他概念的关系

- 与流处理引擎的配合见 [[Kafka Streams与Flink]]

- 是 [[消息队列]] 与 [[流处理]] 的事实标准
- [[Kappa架构]] 与 [[Lambda架构]] 都以 Kafka 为核心事件日志
- 与 [[Apache Flink]]、Kafka Streams、[[Apache Spark]] Streaming 配合做流处理
- 是 [[事件驱动架构]]、[[事件溯源]]、CQRS、[[Outbox模式]]、[[Saga模式]] 的关键基础设施
- 数据通过 [[ETL与ELT]] 流入 [[数据湖]] / [[数据仓库]] / [[Lakehouse架构]]
- KRaft 模式底层依赖 [[Raft共识算法]]
- 在 [[微服务]] 跨服务集成中扮演中枢
- 与 [[分布式系统]] 中的分区、复制、共识、Quorum 概念深度耦合

## 参考源

- Kafka 官方文档 https://kafka.apache.org/
- Jay Kreps, *The Log: What every software engineer should know about real-time data's unifying abstraction*
- *Kafka: The Definitive Guide* (Confluent / O'Reilly)
