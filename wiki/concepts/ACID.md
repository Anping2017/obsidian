---
title: ACID
type: concept
tags: [cs, database, stub]
sources:
  - raw/计算机/数据库/
created: 2026-05-05
updated: 2026-05-05
summary: ACID 是数据库事务的四大保证——原子性、一致性、隔离性、持久性,由 Jim Gray 1970s 提出,是关系型数据库的基石,也是 BASE/最终一致的对照物。
---

# ACID

## 定义

ACID 是**数据库事务必须满足的四个基本属性**的首字母缩写,由 Jim Gray 等人在 1970s 提出,后被 Andreas Reuter & Theo Härder 1983 年正式定义。它是 [[关系型数据库]] 区别于简单文件系统的核心承诺。

| 字母 | 全称 | 含义 |
|---|---|---|
| A | Atomicity 原子性 | 事务要么全部成功,要么全部不发生 |
| C | Consistency 一致性 | 事务前后数据库状态都满足约束 |
| I | Isolation 隔离性 | 并发事务间互不干扰 |
| D | Durability 持久性 | 一旦提交,永久保存,即使崩溃 |

## 核心要点

### 各属性细解

**原子性(Atomicity)**:
- 事务是不可分割的工作单元
- 任一操作失败,整个事务回滚
- 实现机制:undo log 记录修改前镜像

**一致性(Consistency)**:
- 数据库从一个一致状态变为另一个一致状态
- 约束包括:主键唯一、外键、CHECK 约束、触发器、应用层不变量
- 这是 A、I、D 联合保证的「目标」,而非独立机制

**隔离性(Isolation)**:
- 并发事务的中间状态对彼此不可见
- 由隔离级别控制:Read Uncommitted < Read Committed < Repeatable Read < Serializable
- 实现机制:[[数据库锁机制]] 或 [[MVCC]]

**持久性(Durability)**:
- 提交后数据写入非易失存储
- 实现机制:WAL(Write-Ahead Logging)、fsync、复制
- 极端故障(磁盘坏、机房毁)需要异地备份

### 隔离级别与异常

| 级别 | 脏读 | 不可重复读 | 幻读 |
|---|---|---|---|
| Read Uncommitted | ✓ | ✓ | ✓ |
| Read Committed | × | ✓ | ✓ |
| Repeatable Read | × | × | ✓(InnoDB 通过间隙锁阻止) |
| Serializable | × | × | × |

更严格的级别牺牲并发性。

### 实现代价

- WAL:每事务至少一次磁盘写
- 锁/MVCC:内存与 CPU 开销
- 跨节点 ACID:即 [[分布式事务]],如 2PC,代价巨大

### ACID vs BASE

[[BASE理论]](Basically Available, Soft state, Eventual consistency)是 NoSQL 的口号,与 ACID 形成对照:

| 维度 | ACID | BASE |
|---|---|---|
| 一致性 | 强 | 最终 |
| 可用性 | 一般(锁可阻塞) | 高 |
| 性能/扩展 | 单机优化 | 水平扩展 |
| 适用 | 金融、订单 | 海量并发、社交 |

实践中很多系统是混合的——核心数据 ACID,统计/缓存 BASE。

## 和其他概念的关系

ACID 是 [[关系型数据库]] 的灵魂,也是 [[OLAP与OLTP]] 中 OLTP 的底层契约。理解 ACID 是写出正确多用户系统的前提。

实现层面,[[数据库锁机制]] 与 [[MVCC]] 是 Isolation 的两条路线;WAL([[Redo Log]]、[[Undo Log]])是 Atomicity 与 Durability 的基础。

[[分布式系统]] 中,跨节点 ACID 通过 [[分布式事务]](2PC、Saga、TCC)实现,但代价巨大,引出 [[CAP定理]] 与 [[BASE理论]] 的权衡讨论。

[[微服务]] 时代「数据库 per service」让跨服务事务难以维持 ACID,从而催生了事件溯源、CQRS、最终一致等新范式。

## 参考源

- raw/计算机/数据库/
- Jim Gray《The Transaction Concept: Virtues and Limitations》
- 《Designing Data-Intensive Applications》第 7 章
- Härder & Reuter 1983《Principles of Transaction-Oriented Database Recovery》
