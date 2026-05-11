---
title: Outbox 模式
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Outbox 模式通过把"业务数据 + 待发消息"写入同一数据库事务,再由后台进程异步发布消息,解决"数据库事务与消息发送的双写一致性"难题,是微服务事件驱动架构的关键基础。
---

# Outbox 模式

## 定义

**Outbox 模式(Transactional Outbox)** 解决一个看似简单实则致命的问题:**当业务操作既要更新数据库、又要发送消息时,如何保证两者要么都成功要么都不成功?**

简单写法:
```python
db.save(order)            # 1. 写库
queue.send(OrderCreated)  # 2. 发消息
```

会出现:1 成功 2 失败 → 订单已创建但下游服务不知道;或 2 成功 1 失败 → 下游收到事件但订单不存在。这是经典的"双写一致性"问题。

Outbox 模式的方案:**把"消息"作为业务数据的一部分,写到同一个数据库事务**,后台进程读取并发到消息队列。这样数据库事务保证两者一致,事件发布异步且幂等。

## 实现细节

**1. Outbox 表**

业务数据库新增 outbox_events 表:

```sql
CREATE TABLE outbox_events (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    aggregate_id VARCHAR(64),     -- 业务实体 ID
    aggregate_type VARCHAR(64),   -- 实体类型(Order)
    event_type VARCHAR(64),       -- 事件类型(OrderCreated)
    payload JSON,                  -- 事件内容
    created_at TIMESTAMP,
    published_at TIMESTAMP NULL    -- 发布时间(NULL = 未发布)
);
```

**2. 业务事务**

```python
with db.transaction():
    order = Order(...)
    db.save(order)
    db.save(OutboxEvent(
        aggregate_id=order.id,
        event_type='OrderCreated',
        payload={...}
    ))
# 业务代码到此结束,事务提交后即"事件已落库"
```

数据库事务保证 order 和 event 同时存在或不存在。

**3. 后台发布**

独立进程 / 线程:

```python
def publish_loop():
    while True:
        events = db.query("SELECT * FROM outbox_events WHERE published_at IS NULL LIMIT 100")
        for event in events:
            try:
                kafka.send(topic=event.aggregate_type, value=event.payload)
                db.update("UPDATE outbox_events SET published_at=NOW() WHERE id=?", event.id)
            except:
                # 失败留待下次重试
                continue
        sleep(1)
```

**4. 消费者幂等**

事件可能因发布失败重试而重复,消费者必须幂等:
- 用 event id 去重
- 操作幂等(SET 而非 INCR)

## CDC 增强:Debezium

更现代的实现:**用变更数据捕获(CDC)技术从数据库 binlog 直接读 outbox 表的变更**,无需业务代码主动 polling。

**Debezium**

- 红帽开源的 CDC 平台
- 监听 MySQL/PostgreSQL/MongoDB 的 binlog/WAL
- 把变更转为事件流到 [[Apache Kafka|Kafka]]
- 与 outbox 模式天然契合

**架构**

```
应用 → 写 orders + outbox(事务)→ MySQL
                                    ↓ binlog
                                  Debezium
                                    ↓
                                  Kafka outbox topic
                                    ↓
                                  下游消费者
```

**优势**

- 无需后台 polling 进程
- 实时性高(秒级)
- 不增加业务侧代码
- 数据库操作 = 自动事件发布

## 何时用 Outbox

**该用**

- 跨服务事件驱动架构
- 需要"业务数据变更 + 通知"的强一致
- [[微服务]] + [[消息队列]]
- [[Saga模式]] 补偿事件
- [[事件溯源]]

**不需要**

- 单体应用,事件本地处理
- 不要求事件投递保证(允许丢失)
- 全部用同步 RPC 调用

## 与其他双写方案对比

**1. Best Effort(简单写两次)**

```python
db.save(order)
queue.send(event)  # 失败就丢
```

风险:不一致。仅适合非关键事件(如审计日志)。

**2. 2PC(两阶段提交)**

数据库 + 消息队列都参与 XA 事务。原理可行,但:
- 性能差(阻塞锁)
- 兼容性差(Kafka 不支持 XA)
- 长尾时间放大

实战几乎不用。

**3. Outbox**

如本文。

**4. Listen to DB**

直接 CDC 订阅业务表,无 outbox 表。问题:
- 业务表变更不一定与"业务事件"等价(部分字段更新无意义)
- 一对多事件(一次操作触发多事件)难表达
- 反序列化数据库行需要 schema 知识

Outbox 让"事件语义"显式化,业务可控。

## 反向问题:Inbox

消费侧的对称问题——**收到事件后处理与确认 ack 之间,如果业务处理失败重试,可能重复**。解决方案:

**Inbox 表**

```sql
CREATE TABLE inbox_events (
    event_id VARCHAR(64) PRIMARY KEY,
    received_at TIMESTAMP,
    processed_at TIMESTAMP NULL
);
```

```python
with db.transaction():
    if db.exists(InboxEvent.event_id == event.id):
        return  # 已处理,跳过
    db.save(InboxEvent(event_id=event.id, received_at=now()))
    process_event(event)
    update inbox_events SET processed_at=NOW() WHERE event_id=?
```

加上 At-Least-Once 投递,Inbox + Outbox 实现端到端"恰好一次"语义(Effectively Exactly Once)。

## 实战要点

**1. 表设计**

- 主键自增(顺序保证)
- 索引 published_at(快速查未发布)
- 旧已发布事件定期归档 / 清理

**2. 性能**

- 批量 publish(100 条 / 次)
- 多分区并行
- Kafka 端 Producer 配 idempotence + acks=all

**3. 顺序性**

- 同一聚合(aggregate_id)的事件按顺序发布
- Kafka 用 aggregate_id 作 partition key 保证分区内有序

**4. 监控**

- 未发布事件积压量
- 发布延迟(P99)
- 失败次数

## 与事件溯源关系

[[事件溯源]] 把"事件"作为系统的真实数据源,Outbox 与之契合:
- Event Sourcing:领域事件 = 唯一事实
- Outbox:把领域事件可靠发布到外部

二者经常一起使用:Aggregate 操作产生领域事件 → 写 outbox → CDC 发到 Kafka → 下游 [[CQRS]] 读模型订阅。

## 框架支持

- Java:Eventuate Tram、Axon Framework、Debezium Outbox Event Router
- .NET:MassTransit Outbox
- Python:无成熟框架,常自实现
- Node:typeorm + 自实现
- Spring Boot:Spring Modulith Outbox 支持

## 局限

- 增加表与基础设施
- 延迟(事件不是真实时,有秒级延迟)
- 数据库压力(写量翻倍)
- Schema 变更复杂(事件 payload 演进)
- 与历史数据不一致时(老订单无事件)需补全
- CDC 配置复杂(尤其 PG WAL)

## 和其他概念的关系

Outbox 是 [[Saga模式]]、[[事件溯源]]、[[CQRS]] 等微服务模式的关键基础设施——保证事件可靠发布。它与 [[消息队列]]([[Apache Kafka|Kafka]]、RabbitMQ)、CDC 工具(Debezium)共同构成事件驱动架构基础。

它体现的"事务边界对齐"思想是 [[ACID事务]] 在分布式时代的延伸——单库 ACID 不足以保证跨系统一致,需把"消息发送"纳入业务事务。这与 [[BASE理论]]、[[CAP定理]] 的折衷哲学一脉相承。

在 [[微服务]] / Domain-Driven Design 实践中,Outbox 让"领域事件"成为头等公民,而非业务流的副产品。

## 参考源

- raw/计算机/
- 相关:[[Saga模式]]、[[消息队列]]、[[事件溯源]]
