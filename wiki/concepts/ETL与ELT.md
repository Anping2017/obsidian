---
title: ETL 与 ELT
type: concept
tags: [cs, distributed, mature]
sources: [raw/计算机/数据存储/数据库/]
created: 2026-05-05
updated: 2026-05-05
summary: ETL 在装载前转换数据、ELT 装载后再转换,云数据仓库时代 ELT 占主导,搭配 dbt 的"SQL 即代码"成为现代数据栈标配。
---

# ETL 与 ELT

## 定义

- **ETL(Extract-Transform-Load)**:从源系统**抽取(Extract)** → 在中间层**转换(Transform)** → 装载到目标系统(Load)。是传统数据集成的标准范式,转换逻辑在专门 ETL 工具(Informatica、DataStage)中。
- **ELT(Extract-Load-Transform)**:抽取 → 装载到目标系统(数据湖 / 仓) → 在目标内**用 SQL 转换**。云数据仓库(Snowflake / BigQuery / Redshift)时代占主导,搭配 dbt 等"SQL 即代码"工具。

二者都是数据流入 [[数据仓库]] 的方式,差异在转换发生的位置。

## 核心要点

- **ETL 流程**
  - **Extract**:从业务库 / API / 文件抽取
  - **Transform**:在 ETL 服务器内做清洗、聚合、关联、维度匹配
  - **Load**:写入数仓
  - **特点**
    - 转换在专门服务器,数仓只存最终结果
    - 数据落地前已规范,质量高
    - 转换逻辑封装在 ETL 工具,Python/Java 函数式
- **ELT 流程**
  - **Extract**:同 ETL
  - **Load**:原始数据入数据湖 / 暂存表(staging)
  - **Transform**:在仓内用 SQL / 数仓引擎转换
  - **特点**
    - 利用云数仓强大算力做转换,无需独立服务器
    - 原始数据保留,可重新处理
    - 转换逻辑用 SQL 表达,可版本化、可测试
- **ETL vs ELT 对比**

| 维度 | ETL | ELT |
|---|---|---|
| 转换位置 | ETL 服务器 | 数据仓库内 |
| 工具 | Informatica、DataStage、Kettle | dbt + Snowflake/BigQuery |
| 算力来源 | 独立 ETL 集群 | 云仓内置 |
| 原始数据 | 通常不保留 | 全部保留(raw zone) |
| 转换语言 | Python / Java / 工具 DSL | SQL |
| 适合规模 | 中等(本地数仓) | 大(云数仓) |
| 灵活性 | 低(预定义) | 高(随时改 SQL) |
| 主流时代 | 1990-2010s | 2015 至今 |

- **现代数据栈(Modern Data Stack)**
  - **抽取/装载**:Fivetran / Airbyte / Stitch(SaaS,即抽即装,几百种连接器)
  - **数仓**:Snowflake / BigQuery / Redshift / Databricks
  - **转换**:dbt(SQL + Jinja + Git)
  - **编排**:Airflow / Prefect / Dagster
  - **BI**:Looker / Mode / Metabase / Superset
  - **观测**:Monte Carlo / Bigeye(数据可观测性)
- **dbt(data build tool)**
  - 把数据转换写成 SQL 模型(.sql 文件)+ YAML 配置
  - **SELECT 语句即模型**,自动 CREATE / VIEW
  - 自动维护依赖图、增量更新、文档、测试
  - 让数据工程师像写代码一样写 SQL,Git 管理
  - 是 ELT 时代的事实标准
- **CDC(Change Data Capture)**
  - 实时捕获业务库变更(INSERT/UPDATE/DELETE)
  - 工具:Debezium、Maxwell、Canal、AWS DMS
  - CDC + Kafka + Flink → 实时数仓,见 [[流处理]]
- **数据湖(Data Lake)与 Lakehouse**
  - **数据湖**:原始数据存对象存储(S3/OSS/GCS),Schema-on-read
  - **Lakehouse**:Delta Lake / Iceberg / Hudi 在湖上加 ACID + 索引,可直接做 ELT
- **ETL/ELT 流水线设计**
  - **分层(Bronze-Silver-Gold)**
    - **Bronze**:原始数据,完整保留
    - **Silver**:清洗后的数据,统一格式
    - **Gold**:业务可用的聚合 / 报表数据
  - **幂等设计**:任务可重跑,基于时间分区或主键去重
  - **失败处理**:死信队列、人工干预入口、重试策略
- **典型陷阱**
  - **数据漂移**:源 schema 变化 ETL 没感知,下游断
  - **小文件**:大量小文件影响数仓 IO,需合并
  - **回填(Backfill)**:历史数据补算逻辑要与增量一致
  - **依赖管理**:任务依赖图复杂,推荐 dbt / Dagster

## 和其他概念的关系

ETL/ELT 是 [[数据仓库]] 的数据入口管道,是 [[OLAP vs OLTP]] 中从 OLTP 到 OLAP 的桥梁。

[[批处理]](Spark / dbt 批量 SQL)是传统 ETL 主力,[[流处理]](Flink / CDC)是实时 ELT 的引擎。[[Lambda架构]] 与 Kappa 架构都是 ETL/ELT 的高阶组织。

数据存储常用 [[列式存储]] (Parquet / ORC),受 [[查询优化器]] 与谓词下推优化。

[[消息队列]] (Kafka)是 ETL/ELT 流水线的中央骨干,连接源与目标。

[[微服务]] 架构下,业务库分散,ETL/ELT 是跨域分析的唯一抓手。CDC + Kafka 是当代主流。

## 参考源

- raw/计算机/数据存储/数据库/(子目录)
- raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md(数据层)
