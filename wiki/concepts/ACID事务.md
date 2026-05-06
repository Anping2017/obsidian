---
title: ACID 事务
type: concept
tags: [cs, programming, mature]
sources:
  - raw/计算机/开发学习/语言/PHP/03-应用实践层/数据库操作/04-事务处理.md
created: 2026-05-05
updated: 2026-05-05
summary: ACID 是数据库事务的四个基本特性:原子性、一致性、隔离性、持久性,保证数据在并发和故障下的正确性。
---

# ACID 事务

## 定义

**事务(Transaction)**是数据库执行的逻辑单元,把一组操作视为不可分割的整体。**ACID** 是关系型数据库为事务提供的四个保证:

- **A** Atomicity 原子性
- **C** Consistency 一致性
- **I** Isolation 隔离性
- **D** Durability 持久性

ACID 是 1983 年 Theo Härder 与 Andreas Reuter 提出的术语,自此成为关系型数据库[[关系型数据库|RDBMS]]的核心契约。

## 核心要点

### A 原子性(Atomicity)

事务内所有操作要么**全部成功提交**,要么**全部回滚**,不会出现部分成功。
经典例子:转账 A→B,扣 A 100 元和加 B 100 元必须一起成功或一起失败,否则钱会消失或凭空多出。
**实现机制**:Undo Log 撤销日志。事务执行时记录"反向操作",失败或回滚时用 Undo Log 还原。

### C 一致性(Consistency)

事务执行后,数据库从一个**有效状态**转到另一个**有效状态**,所有完整性约束(主键、外键、唯一、check)都满足。
一致性不是单独的机制,而是 A、I、D 加上业务约束共同保证的结果。
注意:这里的"一致性"和[[CAP定理]]中的"一致性"含义不同 —— 前者强调数据完整性,后者强调多副本可见性。

### I 隔离性(Isolation)

并发事务彼此感觉不到对方的存在,看到的数据像是顺序执行得到的。SQL 标准定义 4 级隔离:

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
|---|---|---|---|
| 读未提交 (Read Uncommitted) | √ | √ | √ |
| 读已提交 (Read Committed) | × | √ | √ |
| 可重复读 (Repeatable Read) | × | × | √ |
| 串行化 (Serializable) | × | × | × |

- **脏读**:读到别的事务未提交的数据
- **不可重复读**:同一事务内两次读结果不同(因别人 UPDATE)
- **幻读**:同一事务内两次范围查询行数不同(因别人 INSERT)

**实现机制**:
- **2PL** 两阶段锁:加锁阶段 + 解锁阶段
- **MVCC** [[多版本并发控制]]:每行多个版本,读不阻塞写
- 工程上 MVCC 远多见(Oracle、PostgreSQL、MySQL InnoDB)

PostgreSQL/Oracle 默认 Read Committed;MySQL InnoDB 默认 Repeatable Read 并通过间隙锁(Gap Lock)解决幻读。

### D 持久性(Durability)

事务提交后,即使系统崩溃数据也不会丢。
**实现机制**:WAL(Write-Ahead Log,预写日志):修改先写日志(顺序 IO 快),再写数据页(随机 IO 慢)。崩溃恢复时通过日志回放恢复。
工程实现:MySQL 的 redo log + binlog、PostgreSQL 的 WAL、Oracle 的 redo log。fsync 是关键步骤(从 OS 缓冲刷入磁盘),性能与可靠性的权衡点。

### 事务并发问题与解法对照

| 问题 | 现象 | 标准解法 |
|---|---|---|
| 脏读 | 读到别人未提交 | 读已提交以上 |
| 不可重复读 | 重复读结果变 | 可重复读以上 / MVCC 快照 |
| 幻读 | 行数变 | 串行化 / 间隙锁 |
| 丢失更新 | 后写覆盖先写 | 乐观锁(版本号)/ select for update |
| 写偏斜 | 多事务读相同条件、写不同行 | 串行化 / SSI |

## 和其他概念的关系

ACID 是[[关系型数据库]]的核心承诺,也是 SQL 与[[NoSQL数据库]]的核心分野之一。NoSQL 阵营提出 **BASE**(Basically Available, Soft-state, Eventually consistent)放弃强一致以换扩展性;NewSQL(Spanner、TiDB、CockroachDB)试图在分布式环境下重新提供 ACID。

[[CAP定理]]在网络分区下让 C(一致性)和 A(可用性)二选一;ACID 严格的事务相当于选了 C。

[[微服务]]架构下"每服务一数据库",跨服务事务用**Saga 模式**(补偿事务)、**2PC**(两阶段提交)、**TCC**(Try-Confirm-Cancel)等替代 ACID,本质是放弃强原子性换取可用性。

[[多版本并发控制|MVCC]] 是现代主流并发控制方法;无锁数据结构、STM(Software Transactional Memory)在程序内存事务中借用 ACID 思想。

## 参考源

- raw/计算机/开发学习/语言/PHP/03-应用实践层/数据库操作/04-事务处理.md
