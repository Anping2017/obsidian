---
title: Quorum
type: concept
tags: [cs, distributed, mature]
sources: [raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md]
created: 2026-05-05
updated: 2026-05-05
summary: Quorum 是分布式系统中通过多数派投票达成一致的机制,核心规则 R+W>N 保证读写有交集,是可调一致性与共识算法的基础。
---

# Quorum

## 定义

**Quorum(法定多数 / 仲裁集合)** 是分布式系统中读写需达成的最小节点数集合。核心规则 **R + W > N**(读 quorum + 写 quorum > 副本总数)保证任意读 quorum 与任意写 quorum 有交集,从而读到最新写入,实现强一致。是 Cassandra、DynamoDB、Riak 等可调一致性系统、以及 [[Raft共识算法]]/[[Paxos]] 共识协议的数学基础。

## 核心要点

- **基本公式**
  - **N**:副本总数
  - **W**:写入需多少个副本确认才返回成功
  - **R**:读取需读多少个副本并比较版本才认为是有效结果
  - **R + W > N** ⇒ 任意读集合与任意写集合相交,读必能见到最新写
  - **R + W ≤ N** ⇒ 可能读到旧值,最终一致
- **典型配置**(N=3 时)
  - **W=3, R=1**:写慢、读快、强一致;但任一副本挂就不能写
  - **W=1, R=3**:写快、读慢、强一致;任一副本挂就不能读
  - **W=2, R=2(QUORUM)**:平衡,大多数系统默认
  - **W=1, R=1**:最终一致,可用性最高
- **可调一致性(Tunable Consistency)**
  - Cassandra / DynamoDB 让客户端按请求选 ONE / QUORUM / ALL
  - 高重要性写(订单)用 QUORUM 或 ALL
  - 低重要性写(日志)用 ONE
  - 读热点用 ONE 加速,关键查询用 QUORUM
- **Quorum 与 Paxos/Raft**
  - Paxos 的多数派 = ⌈N/2⌉ + 1,正是 Quorum 的特殊情况
  - [[Raft共识算法]] 的 Leader 选举与日志提交都需要多数派
  - 共识算法是"严格 Quorum"的工程化实现
- **Sloppy Quorum + Hinted Handoff**
  - 严格 Quorum 在节点不可达时整体不可写
  - Sloppy Quorum:把写暂存到健康节点(hinted handoff),事后再转交给目标节点
  - 提高可用性,代价是短暂窗口可能读到旧值
  - Cassandra、DynamoDB 默认采用
- **Read Repair / Anti-entropy**
  - QUORUM 读发现副本版本不一致时,后台异步修复,见 [[BASE理论]]
- **节点权重 / 加权 Quorum**
  - 不同副本权重不同(地理、配置)
  - W/R 改为权重之和满足条件
- **几何 Quorum**
  - 网格 Quorum:行 ∪ 列保证交集,quorum size O(√N)
  - Tree Quorum、Crumbling Walls 等学术变种
- **Witness 节点**
  - 仅参与投票不存数据,降低存储成本
  - MongoDB Arbiter、Spanner Witness、SQL Server AlwaysOn 都用此模式
- **设计权衡**
  - **N 越大**:容错越强,但写延迟随 W 增加
  - **W 越大**:数据安全,可用性下降
  - **R 越大**:一致性强,读延迟增加
  - 需结合 SLA、故障概率、业务一致性需求选

## 和其他概念的关系

Quorum 是 [[Raft共识算法]] / [[Paxos]] 多数派要求的数学抽象,是这些共识算法的核心机制。

在 [[CAP定理]] 中,Quorum 让我们能在 C 和 A 间动态调节(W=ALL → CP,W=ONE → AP)。

[[一致性模型]] 中,R+W>N 直接对应"读到最新写"的强一致语义。

[[NoSQL数据库]] Cassandra、DynamoDB、Riak 都把 Quorum 暴露为客户端参数,这是"可调一致性"的来源。

[[主从复制]] 的同步策略可以理解为 Quorum 的特殊情况(同步复制 ≈ W=N、异步复制 ≈ W=1)。

[[分布式锁]] 的 Redlock 算法也基于 Quorum:跨多 Redis 实例获取多数锁才算成功。

## 参考源

- raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md(分布式数据)
- raw/计算机/运维知识/云服务/云服务器知识地图.md(分布式数据库)
