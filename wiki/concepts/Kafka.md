---
title: Kafka
type: concept
tags: [cs, distributed-systems, stub]
sources:
  - raw/计算机/分布式系统/
created: 2026-05-05
updated: 2026-05-05
summary: Apache Kafka 是分布式发布/订阅消息系统与流处理平台,以日志为核心抽象,提供高吞吐、持久化、可重放的消息流,是事件驱动架构与实时数据管道的事实标准。
---

# Kafka

## 定义

Apache Kafka 是 LinkedIn 2010 年开源、现 Apache 顶级项目的**分布式发布/订阅消息系统与流处理平台**。其核心创新是把**消息抽象为「分布式、可持久化、可重放的提交日志(Commit Log)」**,而非传统消息队列的「投递即消失」语义。

Kafka 同时承担了:

- 消息中间件(类似 RabbitMQ、ActiveMQ)
- 数据管道(类似 Flume、Logstash)
- 流处理底层(配合 Kafka Streams、Flink、Spark Streaming)
- 事件溯源(Event Sourcing)的事实标准

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
| Controller | 集群元数据管理者(KRaft 替代 ZooKeeper) |

### 架构特征

- **分区水平扩展**:Topic 可分为成百上千个 partition,分布到多个 broker
- **顺序写磁盘**:利用磁盘顺序写比内存随机访问还快的特性
- **零拷贝(sendfile)**:数据从磁盘到网卡不经过用户态
- **副本与高可用**:Leader 接收读写,ISR 副本同步;Leader 故障由 Controller 选举
- **消费者位移由消费者管理**:Kafka 不删消息直到保留期到,消费者按需重放

### 与传统 MQ 的区别

| 维度 | 传统 MQ(RabbitMQ) | Kafka |
|---|---|---|
| 消息模型 | 队列 / 主题 | 分布式提交日志 |
| 投递语义 | 投递即删 | 保留期内可重放 |
| 顺序保证 | 队列内有序,多消费者无序 | Partition 内有序 |
| 吞吐 | 高 | 极高(10w-100w+ msg/s) |
| 延迟 | 低(ms) | 中(ms~10ms) |
| 用途 | 命令、任务调度 | 事件流、数据管道、日志聚合 |

### 典型用例

- 日志聚合(应用日志 → Kafka → ELK/Splunk)
- 事件总线(微服务解耦)
- 流处理(Kafka Streams、Flink、Spark Streaming)
- 变更数据捕获(CDC,Debezium → Kafka → 下游)
- 用户行为追踪
- IoT 数据接入

### KRaft 与去 ZooKeeper

Kafka 历史依赖 ZooKeeper 管理元数据,2022 KRaft 模式 GA,用 Raft 协议自管理元数据,简化部署。

## 和其他概念的关系

Kafka 是 [[消息队列]] 与 [[流处理]] 的事实标准之一,与 [[Pulsar]]、[[NATS]]、[[Redis Streams]] 形成对照。

它是 [[事件驱动架构]]、[[CQRS]]、[[事件溯源]]、[[微服务]] 解耦的关键基础设施。[[Lambda架构]] 与 [[Kappa架构]] 都以 Kafka 为核心。

[[ETL与ELT]] 现代化为「实时数据管道」,Kafka + Connect + Schema Registry 是常见组合;[[数据湖]] 与 [[数据仓库]] 越来越多通过 Kafka 实时摄入。

[[分布式系统]] 视角下,Kafka 集成了分区、复制、共识(Raft via KRaft)、Quorum 等众多分布式技术,是学习分布式系统的优秀样本。

[[DDD领域驱动设计|DDD 领域驱动设计]] 中,领域事件天然适合 Kafka 承载,使得跨服务的最终一致性与审计变得可行。

## 参考源

- raw/计算机/分布式系统/
- Kafka 官方文档 https://kafka.apache.org/
- 《Kafka: The Definitive Guide》(Confluent)
- Jay Kreps《The Log: What every software engineer should know》
