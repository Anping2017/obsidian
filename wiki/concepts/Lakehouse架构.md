---
title: Lakehouse 架构
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Lakehouse 把数据湖的低成本灵活与数据仓库的 ACID 性能结合,通过 Delta Lake / Iceberg / Hudi 等开放表格式实现 S3 上的事务存储,是 2020+ 数据架构主流方向。
---

# Lakehouse 架构

## 定义

**Lakehouse(湖仓一体)** 是 Databricks 在 2020 年系统化推广的数据架构概念,核心命题:**在数据湖(S3 / HDFS / GCS 上的 Parquet)之上加一层事务管理,使之兼具数据湖的灵活低成本与数据仓库的 ACID / 性能**。

它解决了过去两难:
- **数据仓库**(Snowflake、Redshift):性能好但贵、不够灵活、半结构化数据弱
- **数据湖**(S3 + Spark):便宜灵活但无 ACID、Schema 演进难、查询慢

Lakehouse 用开放表格式(Open Table Format)在湖上叠加元数据层,鱼和熊掌兼得。

## 三大开源标准

**1. Delta Lake(2019,Databricks)**

- 与 Spark 紧密耦合(Databricks 主导)
- 事务日志 _delta_log 记录每个版本变更
- ACID、Time Travel、Schema Evolution、Upsert
- 2022 年捐给 Linux Foundation 但仍 Databricks 主导

**2. Apache Iceberg(2018,Netflix)**

- 设计更通用、引擎中立
- Snapshot + Manifest 元数据结构
- 支持 Hidden Partitioning(查询不需懂分区)
- AWS、Snowflake、Trino、Dremio、Confluent 都支持
- 2024 年事实标准趋势

**3. Apache Hudi(2017,Uber)**

- 强调流式写入(Upsert)
- Copy-on-Write vs Merge-on-Read
- 更适合 CDC 场景
- 中国阿里云、字节大量使用

**对比**

| 维度 | Delta | Iceberg | Hudi |
|---|---|---|---|
| 主导 | Databricks | 中立 | Uber |
| Spark 集成 | 极强 | 强 | 强 |
| 引擎中立 | 中 | 强 | 中 |
| 元数据 | _delta_log | Manifest 树 | timeline + base+log |
| Upsert | 支持 | 支持 | 强(独有 MoR) |
| Time Travel | 是 | 是 | 是 |
| Schema 演进 | 强 | 强 | 中 |
| 流式 | 中 | 中 | 强 |
| 趋势 | 商业(Databricks) | 中立标杆 | 中(被 Iceberg 蚕食) |

## 关键能力

**1. ACID 事务**

多个写入者并发不冲突:
- 乐观并发控制(OCC)
- 提交时检测冲突
- 失败重试

**2. Time Travel**

```sql
SELECT * FROM orders TIMESTAMP AS OF '2025-01-01'
SELECT * FROM orders VERSION AS OF 42
```

历史快照查询,审计、回滚、复盘可用。

**3. Schema Evolution**

- 加列、删列、改类型(部分)、改名
- 历史数据兼容
- 解决数据湖最大痛点(schema drift)

**4. Upsert / Delete**

```sql
MERGE INTO orders USING new_orders
  ON orders.id = new_orders.id
  WHEN MATCHED THEN UPDATE SET ...
  WHEN NOT MATCHED THEN INSERT ...
```

GDPR 删除([[GDPR]] "被遗忘权")成本可控——数据湖直接 Parquet 不能 Delete,Lakehouse 可。

**5. 高性能**

- 数据跳过(Min/Max 索引)
- Z-Order 多列联合排序
- Bloom Filter
- 与列式 Parquet 结合,查询接近数仓速度

## Medallion 架构

Databricks 推广的 Lakehouse 数据组织模式:

```
原始数据 → Bronze(原始)→ Silver(清洗)→ Gold(业务聚合)
   ↑                                            ↓
  来源系统                                    BI / ML
```

- **Bronze**:原始数据,只追加,作 source of truth
- **Silver**:清洗、去重、标准化,可分析的事实表
- **Gold**:业务聚合、维度建模、最终报表

每层都是 Delta / Iceberg 表,事务保证、可回溯。

## 引擎生态

Lakehouse 不是单一引擎,而是存储 + 元数据 + 查询引擎的组合:

**查询引擎**

- [[Apache Spark]]:Databricks 大本营
- Trino / Presto:SQL 引擎,跨引擎读写
- Dremio:Lakehouse 引擎
- DuckDB:嵌入式分析
- ClickHouse:某些 Iceberg 集成
- Snowflake、BigQuery、Athena 也支持读 Iceberg

**目录(Catalog)服务**

存表元数据(Schema、分区、统计信息):
- Hive Metastore(老)
- AWS Glue Data Catalog
- Unity Catalog(Databricks)
- Polaris(Snowflake 开源,2024)
- Iceberg REST Catalog(标准)

**数据集成**

- Airbyte、Fivetran:批量入湖
- Debezium / Kafka Connect:CDC 流入湖
- dbt:转换层

## 与传统数据仓库对比

| 维度 | Snowflake / Redshift | Lakehouse(Delta/Iceberg + Spark) |
|---|---|---|
| 存储 | 专有(Snowflake)/ S3(Redshift) | S3 / GCS(开放) |
| 计算 | 专有 | Spark / Trino / 多引擎 |
| 价格 | 高 | 低(只付 S3 + 计算) |
| 性能 | 极好 | 好(差距缩小) |
| 灵活 | 中(SQL 为主) | 高(SQL + ML + 流) |
| 半结构化 | 可(Variant) | 原生 |
| Vendor Lock | 高 | 低 |
| 流处理 | 弱 | 强(Spark Streaming) |
| ML | 中 | 强(Spark MLlib + PyTorch) |
| 维护 | 简单(全托管) | 中(需 Spark / 引擎管理) |

## 商业产品

**Databricks Lakehouse Platform**

- Delta Lake + Spark + MLflow + Photon 优化引擎
- 估值 $43B(2023)
- 直接对手 Snowflake

**Snowflake + Iceberg(2024+)**

- Snowflake 原生支持外部 Iceberg 表
- Polaris Catalog 开源
- 转向"湖 + 仓融合"

**AWS Glue + S3 + Athena + Iceberg**

- 开源栈,中等成本
- 适合中等规模团队

**Microsoft Fabric**

- 整合 OneLake、Power BI
- Delta Lake 为核心

## 数据 Mesh 与 Lakehouse

**Data Mesh** 是另一种数据架构理念(Zhamak Dehghani 2019):
- 数据"产品化",域团队拥有
- 联邦治理
- 自助平台

Lakehouse 是技术层方案,Data Mesh 是组织层方案,二者可结合:每个域团队管自己的 Lakehouse 表,平台层提供基础设施。

## 实施挑战

**1. 元数据管理**

数千个表的 Schema、分区、所有者、文档需治理。Datacatalog(DataHub、Amundsen)是必要补充。

**2. 性能调优**

- 文件大小(太多小文件杀性能)
- 定期 OPTIMIZE / Z-Order
- VACUUM 清旧版本
- 分区策略

**3. 流批一体**

理论上 Lakehouse 支持流式写、批式读,但实战中:
- Spark Streaming 微批不是真流
- Flink + Iceberg 是更好流方案
- Hudi 流式 Upsert 强但生态弱

**4. 多引擎一致性**

- Spark 写、Trino 读时间差
- 不同引擎对 Iceberg 实现差异
- 需小心 Snapshot 状态

## 局限

- **运维复杂度**:对比 Snowflake 全托管,需懂 Spark / Trino
- **小数据(< 1TB)不划算**:DuckDB / 单机更快
- **学习曲线**:Catalog、Snapshot、Manifest 概念
- **流式不及专门系统**:Kafka Streams、Flink 仍有优势
- **跨引擎兼容性问题**:虽改善但仍不完美

## Lakehouse 在 AI 时代

- **LLM 训练数据**:大规模文本 / 多模态数据需 Lakehouse 规模存储 + Spark 处理
- **RAG 向量索引**:Lakehouse 表 + 向量字段(Iceberg 支持)
- **特征工程**:Spark 处理后存 Feature Store
- **MLflow + Lakehouse**:实验跟踪与数据 lineage

## 和其他概念的关系

Lakehouse 是 [[大数据]] 架构的 2020+ 演进,与 [[Lambda架构]]、传统数据仓库形成对比。它的核心引擎是 [[Apache Spark]],元数据由 Hive Metastore / AWS Glue / Unity Catalog 等管理。

它与 [[Apache Airflow]] / dbt / Fivetran 等 [[ETL与ELT]] 工具链共生——数据进入 Lakehouse 是 ELT 流程的产物。在 [[微服务]] 体系下,Outbox + CDC + Lakehouse 是事件驱动数据架构标配:服务发事件 → Kafka → Lakehouse → 分析。

它与 [[Pandas与NumPy]]、[[Apache Spark]] 在数据科学栈中分工——前者本地中小规模,后者分布式大规模。

## 参考源

- raw/计算机/
- 相关:[[Apache Spark]]、[[ETL与ELT]]、[[大数据]]
