---
title: OLAP 与 OLTP
type: concept
tags: [cs, distributed, mature]
sources: [raw/计算机/数据存储/数据库/]
created: 2026-05-05
updated: 2026-05-05
summary: OLTP 面向高并发短事务的业务系统、OLAP 面向大查询低并发的分析报表,二者在工作负载、存储、模型设计上有根本差异,HTAP 试图融合二者。
---

# OLAP 与 OLTP

## 定义

- **OLTP(Online Transaction Processing,联机事务处理)**:面向日常业务操作的数据库工作负载,特征是高并发、短事务、单点 / 小范围读写、强一致。代表:订单系统、银行账务、ERP。
- **OLAP(Online Analytical Processing,联机分析处理)**:面向决策分析的工作负载,特征是低并发、长查询、扫描大量数据、聚合统计。代表:BI 报表、用户行为分析、财务数仓。

二者从硬件到软件、从设计模式到团队组织都不同,是数据系统设计的两大主轴。

## 核心要点

- **核心对比**

| 维度 | OLTP | OLAP |
|---|---|---|
| 用户 | 业务前线、机器交易 | 分析师、决策者、数据科学家 |
| 并发量 | 高(千万 QPS) | 低(数百-数千) |
| 数据量 | 单次操作 | 单次扫描 GB-TB |
| 事务时长 | 毫秒级 | 秒-分钟级 |
| 写入模式 | 频繁、随机 | 批量、顺序 |
| 一致性 | 强一致 | 最终一致可接受 |
| 模型 | 3NF/BCNF 范式 | 反范式、Star/Snowflake |
| 存储 | 行存 | [[列式存储]] |
| 索引 | B+树为主 | 列编码、块统计、位图 |
| 代表 | MySQL、PostgreSQL、Oracle | ClickHouse、Snowflake、BigQuery |

- **OLTP 数据库特点**
  - 行存,主键 / 二级索引
  - [[ACID事务]] 强保证
  - [[MVCC]] + 行锁支持高并发
  - 见 [[关系型数据库]]
- **OLAP 数据库特点**
  - 列存,块统计 + 谓词下推
  - 向量化执行,SIMD
  - 大表 JOIN、CUBE、ROLLUP、窗口函数
  - 通常无 [[ACID事务]] 或仅快照隔离
  - 见 [[数据仓库]]
- **数据流转**
  - OLTP 系统是数据源
  - 通过 [[ETL与ELT]] 抽取 → 转换 → 加载到 OLAP
  - 现代 ELT:先加载到数据湖,在 OLAP 内部转换(dbt + Snowflake)
  - 实时:CDC + Flink/Kafka Streams 流式同步,见 [[流处理]]
- **HTAP(Hybrid Transactional/Analytical Processing)**
  - 一套系统同时支持 OLTP 和 OLAP
  - 实现思路
    - 行列混存:TiDB(TiKV 行存 + TiFlash 列存)、SAP HANA(内存列存)
    - OLTP 同步到 OLAP:Aurora 自动复制到 Redshift
  - 适合中小数据量、避免维护两套系统
- **设计建议**
  - 业务初期:OLTP 单库 + 简单报表
  - 数据量大、报表慢:数据同步到 OLAP(Snowflake / ClickHouse)
  - 实时分析需求:加 Flink + Kafka 流处理
  - 巨型互联网:Lambda / Kappa 架构,见 [[Lambda架构]]
- **CAP 与 BASE 的不同选择**
  - OLTP 倾向 CP(强一致)
  - OLAP 倾向 AP + 最终一致

## 和其他概念的关系

OLAP/OLTP 是数据系统设计的根本分类。OLTP 用 [[关系型数据库]] + [[MVCC]] + [[事务隔离级别]] 保证 [[ACID事务]];OLAP 用 [[列式存储]] + 向量化引擎 + [[数据仓库]] 模型实现高速分析。

[[数据库范式]] 是 OLTP 设计准则,反范式 / Star Schema 是 OLAP 设计准则。

[[ETL与ELT]] 桥接二者。现代趋势是用 [[流处理]] + 数据湖 + 列存把 ETL 实时化。

[[查询优化器]] 在两个领域代价模型不同:OLTP 关注索引 + 行级,OLAP 关注列扫描 + JOIN 重排序。

[[微服务]] 架构下,业务库 OLTP 各自独立,通过 CDC 汇聚到中央 OLAP 做跨域分析。

## 参考源

- raw/计算机/数据存储/数据库/(子目录,概念基于通用 CS 知识整理)
- raw/计算机/运维知识/云服务/云服务器知识地图.md(数据库服务分类)
