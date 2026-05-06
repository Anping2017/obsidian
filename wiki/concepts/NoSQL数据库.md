---
title: NoSQL 数据库
type: concept
tags: [cs, programming, mature]
sources:
  - raw/计算机/数据存储/数据库/MangoDB/
  - raw/计算机/编程基础/数据结构/06-应用实战/01-数据库王国/
created: 2026-05-05
updated: 2026-05-05
summary: NoSQL 是非关系型数据库总称,按数据模型分键值、文档、列族、图四类,以放宽 ACID 换取扩展性、灵活模式、海量并发。
---

# NoSQL 数据库

## 定义

**NoSQL**(Not Only SQL)是非关系型数据库的总称,2009 年随 Web 2.0 海量数据需求兴起。它放弃[[关系型数据库]]的某些约束(强 schema、复杂 JOIN、严格 ACID)以获得:
- **水平扩展性**(Sharding 容易)
- **灵活模式(Schema-less)**
- **海量并发吞吐**
- **特殊场景的优化模型**

NoSQL 不是单一技术,而是按数据模型划分的四大家族。

## 核心要点

### 四大类型

| 类型 | 数据模型 | 代表 | 适合 |
|---|---|---|---|
| 键值(Key-Value) | key → value(任意) | Redis、Memcached、DynamoDB、etcd | 缓存、Session、配置中心 |
| 文档(Document) | JSON / BSON | MongoDB、Couchbase、Elasticsearch | 半结构化、内容管理、产品目录 |
| 列族(Column Family) | 行 + 列簇 | Cassandra、HBase、Bigtable | 时序、日志、海量稀疏 |
| 图(Graph) | 节点 + 边 | Neo4j、JanusGraph、ArangoDB | 关系网络、推荐、风控 |

### 键值存储

最简单:value 是字节流,数据库不解析。Redis 是带丰富数据结构(string/list/hash/set/zset)的内存 KV,通常作为[[缓存]]或消息中介使用。DynamoDB 加强一致性 + 自动分片;etcd / ZooKeeper 加强一致性用作元数据存储。

### 文档存储(MongoDB)

单文档可包含嵌套对象、数组,无需 JOIN 即可表达"主-从"关系(嵌入式)。MongoDB 的 _id 是默认主键,索引可建在嵌套字段。
适合:商品目录、博客、用户档案、JSON API 后端。
不适合:需要复杂跨集合 JOIN(MongoDB 的 $lookup 性能不及 SQL JOIN)。

### 列族存储(Cassandra / HBase)

按列簇组织,行内可有任意多列,列名也是数据。设计哲学:写多读少、跨数据中心、CAP 中选 AP。
适合:日志、时序数据、传感器流、用户行为追踪。
设计要点:**先想查询模式再设计表(Query-First)**,反范式化、宽行、合理分区键。

### 图数据库(Neo4j)

节点和边都是一等公民,边有方向、类型、属性。原生图存储用指针直连(免 JOIN),适合多跳查询。
查询语言:Cypher(Neo4j)、Gremlin(Apache TinkerPop)。
应用:社交网络、推荐("跟你相似的人也买了")、知识图谱、欺诈检测、企业组织架构。

### BASE 与最终一致性

NoSQL 多数采用 **BASE** 替代 [[ACID事务|ACID]]:
- **B**asically **A**vailable 基本可用
- **S**oft state 软状态(允许中间状态)
- **E**ventually consistent 最终一致

写入后副本之间逐步同步,过渡期可能读到旧值,经一段时间所有副本收敛。Dynamo、Cassandra 是 AP 系统;HBase 是 CP。

### 何时选 NoSQL

- 数据规模超出单机 RDBMS 极限(TB 级以上)
- 写多于读,且对一致性要求不高
- 模式频繁变化或半结构化(IoT、日志)
- 特殊数据模型契合(图、地理、时序)

何时**不**选:
- 需复杂跨表 JOIN
- 需强 ACID(金融账务)
- 数据规模小(几 GB),没必要

### NewSQL:鱼和熊掌

Spanner、CockroachDB、TiDB、YugabyteDB 想兼得 SQL + ACID + 水平扩展。代价是协议复杂、延迟较高,但避免 NoSQL 的设计陷阱。

## 和其他概念的关系

NoSQL 是[[关系型数据库]]在大数据/互联网时代的补充,二者各有适用场景。Redis 通常与 RDBMS 并存:RDBMS 持久化、Redis 做[[缓存]]/排行榜/分布式锁。

[[CAP定理]]是理解 NoSQL 选型的理论框架。[[微服务]]架构推动数据库分散化,每服务可选不同存储,因此 NoSQL 在微服务生态特别活跃。

[[Hash表]]是 KV 存储的概念基础;[[B+树]]、LSM 树是物理存储引擎(MongoDB 用 B 树、Cassandra/RocksDB 用 LSM)。Elasticsearch 是带搜索的文档存储,基于 Lucene 倒排索引。

## 参考源

- raw/计算机/数据存储/数据库/MangoDB/
- raw/计算机/编程基础/数据结构/06-应用实战/01-数据库王国/
