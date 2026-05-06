---
title: MVCC
type: concept
tags: [cs, distributed, mature]
sources: [raw/计算机/数据存储/数据库/]
created: 2026-05-05
updated: 2026-05-05
summary: 多版本并发控制通过为每行保留多版本快照,让读不阻塞写、写不阻塞读,以空间换时间显著提升数据库并发性能,是现代 OLTP 数据库的事实标准。
---

# MVCC

## 定义

**MVCC(Multi-Version Concurrency Control,多版本并发控制)** 是数据库通过保留每行的多个历史版本,实现读写并发不阻塞的并发控制技术。核心思想是"读取旧快照、写入新版本",避免传统两阶段锁中读写互斥的瓶颈。PostgreSQL、Oracle、MySQL InnoDB、SQL Server 均用 MVCC 作为核心并发模型。

## 核心要点

- **核心思想**
  - 每次更新不覆盖旧数据,而是写入新版本
  - 每条记录带版本号(事务 ID 或时间戳)
  - 读事务按一致性视图(snapshot)读特定版本,看不到比快照更新的版本
- **两类典型实现**
  - **InnoDB 风格**:版本链 + Undo Log
    - 每行有 trx_id(创建该版本的事务)和 roll_pointer(指向上一版本的 undo)
    - ReadView 记录创建时活跃事务列表,读时按 trx_id 与 ReadView 比对决定可见版本
    - 旧版本存在 undo log 中,事务结束后 purge 线程清理
  - **PostgreSQL 风格**:行内多版本
    - 每行有 xmin(创建版本的事务)和 xmax(删除版本的事务)
    - 更新 = 旧行 xmax 设为当前事务 + 插入新行 xmin = 当前事务
    - 旧版本由 VACUUM 后台清理,否则表会膨胀(臭名昭著的 PG bloat)
- **读视图(Snapshot)**
  - **READ COMMITTED**:每条 SQL 都生成新快照,看到最新已提交
  - **REPEATABLE READ**:事务开始时生成快照,整个事务用同一快照
- **优势**
  - **读不加锁**:大幅提升只读 / 读多写少场景的并发
  - **避免幻读**:RR 级别下快照固定,新插入数据不可见
  - **简化死锁**:读写不互锁
- **代价**
  - **空间放大**:旧版本占用磁盘,需后台 VACUUM/Purge
  - **长事务问题**:长事务持有的快照阻止旧版本回收,表/索引膨胀
  - **写写冲突仍需锁**:两个事务同时改同一行还是要等
- **典型陷阱**
  - **PostgreSQL VACUUM**:autovacuum 跟不上写入会导致表膨胀,需调整或手动 VACUUM FULL
  - **InnoDB Undo 膨胀**:长事务(如忘记 COMMIT 的会话)阻止 undo 清理
- **MVCC 与隔离级别**
  - 见 [[事务隔离级别]]:MVCC 是实现 RC 和 RR 的主流手段
  - **快照隔离(SI)**:MVCC 自然结果,所有读用快照,提交时检查写写冲突
  - **SSI(可串行化快照隔离)**:在 SI 上加读写依赖检测,达到 Serializable 语义

## 和其他概念的关系

MVCC 是 [[事务隔离级别]] 在现代 OLTP 数据库的主流实现。它替代/补充了传统的悲观 [[数据库锁机制]],使读不阻塞写、写不阻塞读成为可能。

MVCC 是 [[ACID事务]] 中隔离性的实现技术。在分布式数据库(Spanner、CockroachDB、TiDB)中,MVCC 与 [[Raft共识算法]]、混合逻辑时钟(HLC)结合,实现分布式快照隔离。

PostgreSQL/MySQL 的 [[关系型数据库]] 离不开 MVCC;时序数据库 InfluxDB、列存 ClickHouse 也借鉴了多版本思路。

在 [[微服务]] 中,数据库的 MVCC 是支撑高 QPS 读的关键。但长事务、未关闭的连接会侵蚀 MVCC 的优势,需要监控告警。

## 参考源

- raw/计算机/数据存储/数据库/(子目录,概念基于通用 CS 知识整理)
- raw/计算机/开发学习/系统/Wordpress/02-核心理解层/01-架构原理/数据库结构.md(InnoDB 表配置示例)
