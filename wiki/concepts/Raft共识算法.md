---
title: Raft 共识算法
type: concept
tags: [cs, distributed, mature]
sources: [raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md]
created: 2026-05-05
updated: 2026-05-05
summary: Raft 是 Paxos 的工程化简化版本,通过领导者选举、日志复制、安全性三大子问题解耦,实现易理解、易实现的分布式共识。
---

# Raft 共识算法

## 定义

**Raft** 是 Diego Ongaro 和 John Ousterhout 在 2014 年发表的分布式共识算法,设计目标是"等价于 Paxos 但更易理解"。它把共识问题分解为**领导者选举(Leader Election)、日志复制(Log Replication)、安全性(Safety)** 三个相对独立的子问题,从而大幅降低工程实现难度。是 etcd、Consul、TiKV、CockroachDB、Kafka KRaft、Nomad 等系统的核心。

## 核心要点

- **角色与状态**
  - **Leader**:唯一处理客户端请求,把日志复制到 Followers
  - **Follower**:被动接收 Leader 心跳和日志
  - **Candidate**:选举过程中的临时状态
  - 状态转换:Follower → 选举超时变 Candidate → 拿到多数票变 Leader
- **任期(Term)**
  - 每次选举开启一个新 Term,单调递增
  - 每个 Term 内最多一个 Leader
  - 节点收到更高 Term 消息立即降为 Follower
  - Term 是 Raft 的"逻辑时钟"
- **领导者选举**
  - Follower 在 election timeout(随机 150-300ms)内未收到 Leader 心跳,变 Candidate
  - 自增 Term、给自己投票、向所有节点发 RequestVote
  - 收到多数票则成为 Leader
  - 平票则等下次随机超时再选(随机化避免活锁)
- **日志复制**
  - 客户端发请求 → Leader append 到本地日志
  - Leader 通过 AppendEntries RPC 复制到 Followers
  - **多数派(quorum)** 持久化后,Leader 提交(committed)
  - Leader 通知客户端成功 + 通知 Followers 更新 commitIndex
  - 状态机按 commitIndex 顺序应用日志
- **安全性约束**
  - **选举限制**:Candidate 必须包含已提交的所有日志(通过 lastLogIndex/Term 比较)
  - **日志匹配**:相同 (index, term) 的条目必然内容相同(prevLog 检查)
  - **领导者只追加**:不删除已写日志,只追加
  - **领导者完整性**:已提交的日志在所有未来 Leader 中都存在
- **关键 RPC**
  - **RequestVote**:Candidate 拉票
  - **AppendEntries**:Leader 复制日志兼心跳
  - **InstallSnapshot**:Follower 落后太多直接装快照
- **故障处理**
  - **网络分区**:少数派分区不能选出 Leader,客户端写失败;多数派正常服务
  - **Leader 挂**:Followers 选举超时,选新 Leader
  - **Follower 挂**:多数还在,Leader 继续服务
  - **脑裂**:不可能(只有多数派能选 Leader)
- **快照(Snapshot)**
  - 日志会无限增长,定期把状态机状态快照到磁盘
  - 快照前的日志可丢弃
  - 落后太多的 Follower 直接接收快照
- **Raft vs Paxos**
  - Paxos 论文晦涩,工程实现千差万别(Multi-Paxos 各家不同)
  - Raft 单 Leader 简化日志推进,易实现易理解
  - 现代新系统多选 Raft;老系统(Chubby、ZooKeeper Zab)用 Paxos 变种
- **典型应用**
  - **etcd**:Kubernetes 的元数据存储
  - **Consul**:服务发现 + KV
  - **TiKV / CockroachDB**:NewSQL 的 Region 副本组
  - **Kafka 3.x KRaft**:替代 ZooKeeper 管理元数据
  - **HashiCorp Nomad / Vault**:分布式协调

## 和其他概念的关系

Raft 是 [[Paxos]] 的工程化变体,目标都是在分布式环境下让多个节点对一个值达成一致(共识)。共识是 [[一致性模型]] 中"线性一致性"的实现基础。

Raft 多数派写入与读取的语义就是 [[Quorum]] 协议的特殊情况(W = N/2+1, R = N/2+1)。

[[CAP定理]] 中 Raft 是 CP 系统:分区时少数派不可用,多数派一致服务。

Raft 是 [[主从复制]] 的强一致版本:Leader = 主、Followers = 从,多数同步而非异步。

[[微服务]] 中的服务发现(Consul、etcd)、配置中心都建立在 Raft 之上。[[分布式锁]] 用 etcd Lease 同样依赖 Raft。

NewSQL 数据库把数据切成 Region,每 Region 一个 Raft 组,实现"分片 + 强一致复制"。

## 参考源

- raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md(分布式存储)
- raw/计算机/运维知识/容器化/Kubernetes/Kubernetes知识地图.md(etcd 角色)
