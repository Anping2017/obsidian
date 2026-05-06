---
title: LSM树
type: concept
tags: [cs, distributed, mature]
sources: [raw/计算机/数据存储/数据库/]
created: 2026-05-05
updated: 2026-05-05
summary: Log-Structured Merge Tree 是面向写入优化的存储结构,通过内存表+多层有序文件+后台合并把随机写转为顺序写,主导现代 NoSQL/列存。
---

# LSM 树

## 定义

**LSM 树(Log-Structured Merge Tree)** 是一种为写密集场景设计的多层数据结构,核心思想是把随机写入累积到内存中,达到阈值后批量写入磁盘,通过后台合并(Compaction)维护有序性。Patrick O'Neil 等人 1996 年提出,是 LevelDB、RocksDB、Cassandra、HBase、ScyllaDB 等存储引擎的核心,也是现代列存与时序数据库的标准索引结构。

与 [[B+树]] 的"原地更新"思路相反,LSM 是"追加 + 合并"思路,牺牲读放大换取极致写入吞吐。

## 核心要点

- **三层结构**
  - **MemTable**:内存中的有序结构(通常是 [[跳表]] 或红黑树),所有写入先到这里
  - **WAL(Write-Ahead Log)**:预写日志,持久化到磁盘保证 MemTable 崩溃可恢复
  - **SSTable(Sorted String Table)**:磁盘上不可变的有序键值文件,分层组织(L0、L1、L2...)
- **写流程**
  - 1. 写 WAL(顺序追加,极快)
  - 2. 更新 MemTable(O(log n))
  - 3. MemTable 满则冻结、刷盘成新 SSTable,清空 WAL
  - **写入永远是顺序 IO**,远快于 [[B+树]] 的随机写
- **读流程**
  - 先查 MemTable → Immutable MemTable → L0 SSTable → L1 → L2...
  - **读放大**:可能查多个文件才能找到键
  - 优化:[[布隆过滤器]] 快速判断键是否在某 SSTable、稀疏索引定位文件内位置
- **合并(Compaction)**
  - **Size-tiered**:同层文件累积到 N 个就合并到下一层(Cassandra 默认),写放大低、空间放大高
  - **Leveled**:每层固定大小、每层 SSTable 之间无键范围重叠(LevelDB/RocksDB),空间放大低、写放大高
  - 合并时丢弃旧版本和墓碑(tombstone),回收空间
- **三大放大权衡**
  - **写放大**:每条数据被合并多次,实际写盘量 > 用户写入量
  - **读放大**:一次读可能扫多个 SSTable
  - **空间放大**:旧版本与已删数据未及时清理
  - 三者相互制约,Compaction 策略本质是在三者间取舍
- **删除与更新**:都是追加新记录(更新写新版本、删除写墓碑),Compaction 时才真正清理
- **典型实现**
  - **LevelDB / RocksDB**:嵌入式 KV,被 MyRocks、TiKV、CockroachDB 当作底层
  - **Cassandra / ScyllaDB**:分布式宽列存储
  - **HBase**:Hadoop 之上的宽列存储
  - **InfluxDB / ClickHouse**:时序与列存数据库借鉴 LSM 思想

## 和其他概念的关系

LSM 与 [[B+树]] 是数据库存储引擎的两大流派:B+树写需要原地更新页面、随机 IO,但读路径短;LSM 写顺序追加、读需要合并多文件。MyISAM 用 B 树、InnoDB 用 B+树、RocksDB 用 LSM,选择本质是工作负载决定的。

LSM 大量依赖 [[布隆过滤器]] 加速 SSTable 查找,内存层用 [[跳表]] 实现有序性。WAL 机制保证 [[ACID事务]] 的持久性。

LSM 是 [[NoSQL数据库]] 写性能优势的关键,Cassandra/HBase 能支撑百万级 QPS 写入正源于此。在 [[微服务]] 架构中,日志、监控指标、事件流等写多读少场景天然适合 LSM。

[[关系型数据库]] 也开始拥抱 LSM:MyRocks(MySQL + RocksDB)、TiDB(TiKV)用 LSM 存储引擎,在云原生分布式场景下取代 InnoDB。

## 参考源

- raw/计算机/数据存储/数据库/(目录存在但内容为空,概念基于通用 CS 知识整理)
- raw/计算机/运维知识/云服务/云服务器知识地图.md(分布式数据库章节)
