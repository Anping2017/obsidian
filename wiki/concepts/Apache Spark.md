---
title: Apache Spark
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Apache Spark 是基于内存计算的分布式数据处理引擎,通过 RDD/DataFrame 抽象、DAG 执行引擎和 Catalyst 优化器,把 MapReduce 的"批处理慢"问题翻盘,统一批/流/SQL/ML/图四大场景,是大数据时代核心计算框架。
---

# Apache Spark

## 定义

**Apache Spark** 是 UC Berkeley AMPLab 在 2009 年起开发、2014 年成为 Apache 顶级项目的开源分布式数据处理引擎。它由 Matei Zaharia 主导,核心创新是用**内存中的 RDD(Resilient Distributed Dataset)**取代 Hadoop MapReduce 的磁盘中间结果,把迭代计算性能提升 10-100 倍。

Spark 是当前 [[大数据]] 生态的事实标准——批处理、流处理、SQL 查询、机器学习、图计算五大场景都用 Spark,在 [[Lambda架构]] / Kappa 架构、Lakehouse 等数据架构中是核心引擎。

## 核心抽象演进

**1. RDD(2009-2014)**

- 弹性分布式数据集
- 不可变、分区、可重算
- API:map / filter / reduce / join 等
- 缺点:无 schema,优化空间小

**2. DataFrame(2015+)**

- 类似 SQL 表 + Pandas DataFrame 的分布式版
- 有 schema,Catalyst 优化器可介入
- Tungsten 内存编码极致优化
- 与 PySpark / Spark SQL 紧密集成

**3. Dataset(Scala / Java)**

- DataFrame + 强类型
- 编译期类型检查
- Python 不支持(Python 无 JVM 类型)

现在新代码用 DataFrame / SQL,RDD 仅在底层或迁移用。

## 架构

**Driver / Executor / Cluster Manager**

```
Driver(主程序)
  ├── 分析 DAG
  ├── 调度 Task
  └── 收集结果

Cluster Manager(YARN / K8s / Mesos / Standalone)
  └── 分配 Executor

Executor(工作节点)
  ├── 执行 Task
  ├── 缓存数据
  └── 上报状态
```

**关键执行流程**

1. 用户写 DataFrame / SQL 代码
2. Catalyst 解析逻辑计划 → 物理计划
3. DAG Scheduler 切分 Stage(Shuffle 边界)
4. Task Scheduler 分发 Task 到 Executor
5. Executor 拉取数据、计算、Shuffle
6. 结果回 Driver

## 五大模块

**Spark Core**

RDD、Task 调度、内存管理、I/O。

**Spark SQL**

- 关系查询(SQL / DataFrame API)
- Catalyst 优化器(规则 + 代价)
- Hive 兼容(读 metastore、调 UDF)

**Spark Streaming(微批)/ Structured Streaming**

- 微批模式:每秒/每分一批
- Structured Streaming(2017+):统一 SQL/DataFrame API,事件时间、水印
- 与 Kafka、Kinesis、Pulsar 集成

**MLlib**

- 经典机器学习算法(分类、回归、聚类、推荐)
- Pipeline API(类 Sklearn)
- 在深度学习时代被 PyTorch / TensorFlow 蚕食

**GraphX**

- 图算法(PageRank、连通分量、最短路径)
- 不及 Neo4j、TigerGraph 专业,边缘场景

## 与 Hadoop / MapReduce 对比

| 维度 | Hadoop MapReduce | Spark |
|---|---|---|
| 中间结果 | 磁盘 | 内存 |
| 性能 | 慢 | 快 10-100x |
| API | Map + Reduce(原始) | DAG / SQL / DataFrame |
| 流处理 | 不擅长(Storm/Flink 替代) | 内建 |
| 机器学习 | Mahout(已停) | MLlib / 与 PyTorch 共生 |
| 现状 | 衰落 | 主流 |

Hadoop 系仍占数据湖底层(HDFS / Hive),但计算层几乎都是 Spark。

## 与 Flink 对比

**Flink** 是与 Spark 并列的分布式计算引擎,设计哲学不同:

| 维度 | Spark | [[Apache Flink]] |
|---|---|---|
| 起源 | 批处理 + 流 | 流处理 + 批 |
| 流处理模型 | 微批(秒级) | 真正流(毫秒) |
| 状态管理 | 弱(Streaming) | 强(KeyedState) |
| 事件时间 | 支持 | 第一公民 |
| 批处理 | 强 | 中 |
| 生态 | 大(全场景) | 中(流为主) |
| 主流领域 | 数据仓库、ETL、ML | 实时 ETL、CEP、风控 |

简单说:Spark 适合"批 + 接近实时",Flink 适合"严格实时低延迟"。

## 部署模式

**1. Standalone**

Spark 自己当集群管理器,简单但不主流。

**2. YARN**

Hadoop 集群常用,与 HDFS 共生。

**3. Kubernetes(2018+)**

[[Kubernetes]] 上跑 Spark,支持 Spark Operator,云原生主流方向。

**4. Databricks**

Spark 商业公司,提供托管 Spark + Delta Lake + Notebook。占据 Spark 商业市场主导。

**5. AWS EMR / GCP Dataproc / Azure HDInsight**

云厂商托管 Spark / Hadoop。

## PySpark

Python API,90% 的 Spark 用户走 Python:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("demo").getOrCreate()
df = spark.read.parquet("s3://bucket/data/")
result = (df.filter(df.country == "CN")
            .groupBy("city")
            .agg({"revenue": "sum"})
            .orderBy("sum(revenue)", ascending=False))
result.show()
```

底层 JVM 执行,Python ↔ JVM 用 Py4J 通信。性能略低于 Scala API,但生态(Pandas、NumPy)整合压倒性。

## Delta Lake / Iceberg / Hudi

Spark 之上的事务存储层(Lakehouse):
- **Delta Lake**(Databricks):ACID、Time Travel、Schema Evolution
- **Apache Iceberg**(Netflix → Apache):类似,设计更通用
- **Apache Hudi**(Uber):支持 upsert、流式写入

把数据湖(S3 上的 Parquet)升级到"湖仓一体":既有数据湖灵活,又有数据仓库 ACID。

## 性能调优要点

**1. 分区(Partitioning)**

- 输入分区数影响并行度
- repartition vs coalesce
- 数据倾斜(Data Skew)需 salt 散列

**2. Shuffle**

- 最贵操作(磁盘 + 网络)
- 减少 Shuffle:用 broadcast join、局部聚合
- spark.sql.shuffle.partitions 默认 200,需调

**3. Broadcast Join**

- 小表(< 100MB)广播到所有 Executor
- 避免大表 Shuffle Join

**4. 缓存(cache / persist)**

- 多次访问同 DataFrame 时缓存
- 选择存储级别(MEMORY_ONLY、MEMORY_AND_DISK)

**5. 列式存储**

- Parquet > CSV / JSON
- 列式压缩 + 谓词下推 + 投影下推

## 局限

- 内存消耗大
- 启动慢(JVM + Driver 几分钟)
- 调试困难(分布式堆栈)
- 真实流处理不及 Flink
- 小数据(< 1GB)用 Pandas 更快
- Python 用户性能损耗(JVM ↔ Python 切换)

## 适用场景

**最适合**

- 数据仓库 ETL
- 机器学习特征工程
- 批量报表
- 数据湖查询
- 中等规模流处理(秒级)

**不适合**

- 单机数据(< 10GB)
- 严格毫秒延迟流
- 高并发交互查询(用 ClickHouse / Druid)
- 简单转换(用 SQL 数据库)

## 和其他概念的关系

Spark 是 [[大数据]] 生态计算层核心,与 HDFS / S3([[关系型数据库]] 之外的存储)、Hive Metastore、[[Kafka]] 流、[[ETL与ELT]] 工具链共同构成数据平台。

在 [[Lambda架构]] 中 Spark 担任批处理层(speed layer 用 Storm / Flink);在 Lakehouse 架构中 Spark 是统一计算引擎,Delta / Iceberg 是统一存储。

机器学习侧,Spark MLlib 与 [[Embedding]]、[[BERT]] 等模型推理共生——大规模特征工程用 Spark,模型训练用 PyTorch / TensorFlow,推理服务用专门 Serving 系统。

## 参考源

- raw/计算机/
- 相关:[[Kafka]]、[[Lambda架构]]、[[ETL与ELT]]
