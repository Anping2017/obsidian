---
title: OLAP vs OLTP
type: concept
tags: [cs, database, mature]
sources:
  - raw/计算机/数据库/
created: 2026-05-05
updated: 2026-05-05
summary: OLTP 处理高并发短事务支撑业务流转,OLAP 处理低并发长查询支撑决策分析,两者在数据模型、存储格式、索引策略上有本质差异,衍生出 ETL/数据仓库/列存等中间层。
---

# OLAP vs OLTP

## 定义

**OLTP**(Online Transaction Processing,在线事务处理):面向**业务运营**的数据库工作负载,典型场景为交易系统、订单系统、库存系统。特征是高并发、短事务、读写混合、实时性要求高。

**OLAP**(Online Analytical Processing,在线分析处理):面向**决策支持**的数据库工作负载,典型场景为报表、看板、商业智能、数据挖掘。特征是低并发、长查询、读重写少、扫描海量历史数据。

(本文同 [[OLAP与OLTP]] 概念,可互换引用)

## 核心要点

### 对比维度

| 维度 | OLTP | OLAP |
|---|---|---|
| 用户 | 业务员、客户、应用 | 分析师、决策者 |
| 操作 | 增删改查,以单条/小批量为主 | 复杂聚合 + 多表 join |
| 事务量 | 高并发,QPS 千~百万 | 低并发,数十~数百 |
| 数据量 | 当前活跃数据,GB~TB | 历史全量,TB~PB |
| 响应时间 | 毫秒级 | 秒~分钟级 |
| 数据模型 | 范式化(3NF)、关系表 | 星型/雪花模式、维度+事实 |
| 存储方式 | 行存 | [[列式存储]] |
| 一致性 | 强一致([[ACID]]) | 最终一致即可 |
| 代表系统 | MySQL、PostgreSQL、Oracle | Snowflake、BigQuery、ClickHouse、Doris |

### 为什么要拆分

OLTP 与 OLAP 直接共用一个库会互相影响:

- 分析查询扫表会拖慢业务事务
- 范式化表对分析不友好(多 join)
- 历史数据膨胀拖慢业务库

因此典型企业架构:OLTP 业务库 → [[ETL与ELT]] → [[数据仓库]] → BI 工具。

### HTAP 的努力

HTAP(Hybrid Transactional/Analytical Processing)试图统一两类工作负载,如 TiDB、SAP HANA、Oracle In-Memory。常见手段:

- 行列混存:同一份数据多种格式
- 资源隔离:CPU/内存配额限制干扰
- 实时复制:OLTP 数据近实时同步给 OLAP 引擎

### OLAP 的优化技巧

- [[列式存储]]:只读所需列,大幅减少 IO
- 向量化执行:批处理代替逐行
- 物化视图:预聚合常用查询
- 数据立方体(Cube):多维聚合预计算

## 和其他概念的关系

OLTP/OLAP 是 [[数据库]] 工作负载的核心二分,直接驱动了存储引擎(行存 vs [[列式存储]])、索引策略([[B+树]] vs 跳表/位图)、事务模型([[ACID]] vs 最终一致)的分化。

OLAP 催生了 [[数据仓库]] 与 [[ETL与ELT]] 工具链;[[Lambda架构]] 与 [[Kappa架构]] 是结合实时流处理的演进。

[[查询优化器]] 在 OLAP 场景需处理更复杂的 join 顺序与 cardinality 估计。[[分布式系统]] 视角下,OLAP 通常采用 MPP(大规模并行)架构而 OLTP 采用主从复制 + 分片。

现代云原生时代,OLAP 系统与对象存储分离([[计算与存储分离]]),如 Snowflake、Iceberg。

## 参考源

- raw/计算机/数据库/
- Kimball《数据仓库工具集》
- Stonebraker《One Size Does Not Fit All》
