---
title: Paxos
type: concept
tags: [cs, distributed, mature]
sources: [raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md]
created: 2026-05-05
updated: 2026-05-05
summary: Paxos 是 Lamport 1989 年提出的分布式共识算法基石,通过 Prepare/Accept 两阶段在异步网络中达成一致,衍生出 Multi-Paxos、Fast Paxos 等变种。
---

# Paxos

## 定义

**Paxos** 是 Leslie Lamport 在 1989 年(论文 1998 年发表)提出的分布式共识算法,以希腊岛屿命名。它解决了"在异步网络、节点可能崩溃但不会作恶(非拜占庭)的环境下,多个节点如何对一个值达成一致"的问题,被誉为"分布式系统皇冠上的明珠",是 Chubby、ZooKeeper、Spanner 等核心系统的理论基础。

## 核心要点

- **角色**
  - **Proposer(提议者)**:发起提案
  - **Acceptor(接受者)**:对提案投票
  - **Learner(学习者)**:获知最终决议
  - 实际系统中一个进程通常同时承担多角色
- **基本 Paxos 流程(单个值的共识)**
  - **阶段 1a: Prepare**
    - Proposer 选一个递增编号 n,向多数 Acceptor 发 Prepare(n)
  - **阶段 1b: Promise**
    - Acceptor 收到 Prepare(n):若 n 大于此前承诺过的所有编号,则承诺不再接受小于 n 的提案,并返回此前接受过的最大编号提案值
    - 否则拒绝
  - **阶段 2a: Accept**
    - Proposer 收到多数 Promise:从返回的提案中选最大编号的值(若无则用自己想提的值),发送 Accept(n, v)
  - **阶段 2b: Accepted**
    - Acceptor 收到 Accept(n, v):若未承诺过更大编号,则接受并广播
  - **决议**:某值被多数 Acceptor 接受即为最终决议
- **关键性质**
  - **安全性**:任何被选定的值都不会改变,所有 Learner 学到相同值
  - **活性(非保证)**:可能存在两个 Proposer 不断 Prepare 互相超越导致没有进展(活锁,需 Leader 缓解)
- **Multi-Paxos**
  - 基本 Paxos 决一个值代价大(2 轮 RPC)
  - 选出固定 Leader,后续提案跳过 Prepare,直接 Accept,2 轮 RPC 降到 1 轮
  - 是 Chubby、Spanner、ZooKeeper Zab 实际使用的形态
- **Fast Paxos / EPaxos / Flexible Paxos**
  - **Fast Paxos**:无冲突时 1 轮搞定,但仲裁集合更大
  - **EPaxos(Egalitarian Paxos)**:无 Leader 多 Proposer 并行,处理无依赖的请求最快
  - **Flexible Paxos**:Prepare 和 Accept 可用不同 quorum,只要交集非空即可
- **Paxos 的难点**
  - 论文晦涩,Lamport 自己也写过《Paxos Made Simple》
  - 实现细节(成员变更、快照、持久化)论文未给,各家工程实现差异大
  - 这正是 [[Raft共识算法]] 出现的动机
- **拜占庭容错(BFT)**
  - Paxos 假设节点崩溃但不撒谎
  - 拜占庭场景需 BFT(PBFT、HotStuff、Tendermint)
  - 区块链(Bitcoin/Ethereum 等)是另一类拜占庭共识
- **典型应用**
  - **Google Chubby**:分布式锁服务,Multi-Paxos
  - **ZooKeeper**:用 Zab 协议(Paxos 类似)
  - **Apache Cassandra**:Lightweight Transaction(LWT)用 Paxos 做 CAS
  - **Spanner**:Multi-Paxos 复制每个 Tablet
  - **Megastore / F1**:Google 早期 Paxos 系统

## 和其他概念的关系

Paxos 是分布式共识的理论起点,[[Raft共识算法]] 是其工程化简化变体,二者解决相同问题但 Raft 大幅降低实现难度,新系统多选 Raft。

共识算法实现 [[一致性模型]] 中最强的"线性一致性",是分布式 [[关系型数据库]](Spanner、CockroachDB)和元数据服务(etcd/ZK)的根基。

[[CAP定理]] 中 Paxos 是 CP 路线:分区时少数派不可达成共识。

Paxos 与 [[Quorum]] 协议密切相关:多数派(N/2+1)是 Paxos 的标准 quorum。

[[主从复制]] 的同步复制可基于 Paxos 实现强一致主从。

## 参考源

- raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md(分布式系统理论)
- raw/计算机/运维知识/容器化/Kubernetes/Kubernetes知识地图.md(etcd 共识)
