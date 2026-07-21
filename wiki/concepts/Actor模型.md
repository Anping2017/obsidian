---
title: Actor 模型
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Actor 模型是 Carl Hewitt 1973 年提出的并发计算模型——每个 Actor 是独立计算单元,只通过异步消息通信、各自维护私有状态,Erlang/Akka/Elixir 把这一模型工业化为电信级容错系统的基础。
---

# Actor 模型

## 定义

**Actor 模型** 是 Carl Hewitt、Peter Bishop、Richard Steiger 在 1973 年的论文《A Universal Modular ACTOR Formalism for Artificial Intelligence》中提出的并发计算模型。它的核心命题:**计算的基本单位是 Actor——一个封装状态、通过异步消息与外界通信的并发实体**。

每个 Actor 收到消息时可:
1. 修改自己的私有状态
2. 创建新 Actor
3. 发送消息给其他 Actor
4. 决定下一条消息如何处理

Actor 间**只通过消息**交互,无共享内存、无锁、无方法调用——这彻底避开了传统多线程编程的死锁、竞态等噩梦。

## 三大特征

**1. 状态隔离**

每个 Actor 内部状态完全私有,外部只能通过发消息影响。无共享 = 无数据竞争 = 无锁。

**2. 异步消息**

发送 = "投信",不等回复(可选 ask 模式)。Actor 邮箱(Mailbox)缓冲消息,顺序处理。

**3. 监督树(Supervision)**

Actor 形成层级父子关系。子 Actor 出错时,父 Actor 决定:
- 重启(Restart)
- 恢复(Resume)
- 停止(Stop)
- 上报给爷爷(Escalate)

这是 Erlang "Let it crash" 哲学的工程化实现——出错就重启,不要试图修复每个边缘情况。

## Erlang / Elixir

**Erlang(1986,Joe Armstrong @ Ericsson)**

电信交换机软件起家,设计目标:99.999999999%(11 个 9)可用性。Actor 模型是它的核心,加上:
- 不可变数据
- 模式匹配
- 函数式
- BEAM 虚拟机轻量进程(几 KB 内存)
- 单机数百万并发

经典:Ericsson AXD301 ATM 交换机连续 9 年无停机。

**Elixir(2011,José Valim)**

跑在 BEAM 上的现代语言:
- Ruby 风格语法
- 完整 Erlang 互操作
- 现代工具链(mix、Hex)
- [[Phoenix LiveView]] 与 [[Phoenix LiveView]]

WhatsApp、Discord、Pinterest、Bleacher Report 等大量用 Erlang/Elixir。WhatsApp 50 名工程师支撑 9 亿用户的传奇就建立在 BEAM 之上。

## Akka(JVM)

**Akka(2009,Jonas Bonér)**

把 Actor 模型带到 JVM:
- Scala / Java API
- Cluster:跨机器 Actor 系统
- Streams:与响应式编程结合
- HTTP / gRPC 模块
- Persistence:Event Sourcing 内置

```scala
import akka.actor._

class CounterActor extends Actor {
  var count = 0
  def receive = {
    case "inc" => count += 1
    case "get" => sender() ! count
  }
}

val system = ActorSystem("MySystem")
val counter = system.actorOf(Props[CounterActor], "counter")
counter ! "inc"
counter ! "inc"
counter ? "get"  // ask 模式
```

**Akka Typed(2.6+)**

类型安全的 Actor API,编译期检查消息类型,避免老 Akka "Any 消息"问题。

**许可变更**

2022 年 Akka 改 BSL,大量用户转向 Pekko(Apache 分叉)或 Cats Effect / ZIO 等替代。

## Microsoft Orleans

.NET 的 Actor 框架,关键创新:**Virtual Actor**——开发者不显式管理 Actor 生命周期,框架按需激活/钝化。

```csharp
public interface IPlayer : IGrainWithStringKey {
  Task<int> GetScore();
  Task UpdateScore(int delta);
}
```

调用即激活,空闲即钝化,自动持久化。游戏服务器、IoT 后端常用。

## Actor vs CSP vs STM

**Actor(Erlang、Akka)**

- 异步消息
- 各 Actor 独立邮箱
- "推"模型(发送方主动)

**CSP(Communicating Sequential Processes,Go)**

- 同步通道(Channel)
- 多 goroutine 通过通道通信
- "握手"模型(发送 + 接收同步)
- 详见 [[Go goroutine与channel]]

**STM(Software Transactional Memory,Haskell、Clojure)**

- 共享状态 + 事务
- 类似数据库 ACID
- 冲突时重试

**对比**

| 维度 | Actor | CSP | STM |
|---|---|---|---|
| 通信 | 异步消息 | 同步 channel | 共享内存 |
| 状态 | 私有 | 私有(共享 channel) | 共享 + 事务 |
| 锁 | 无 | 无 | 隐式 |
| 容错 | 强(监督) | 弱 | 中 |
| 代表语言 | Erlang | Go | Haskell |

三种模型各有最适合场景,Actor 在分布式 + 容错领域最强。

## 经典 Actor 模式

**1. Pipes and Filters**

Actor A → Actor B → Actor C 链式处理,每个 Actor 是一个过滤器。

**2. Worker Pool**

Master Actor 把工作分给 N 个 Worker Actor,负载均衡。

**3. Pub/Sub**

EventBus Actor 维护订阅者列表,广播事件。

**4. Saga**

Saga Actor 协调多个步骤的本地事务和补偿(对应 [[Saga模式]])。

**5. State Machine**

Actor 用 become 切换状态:

```scala
def waiting: Receive = {
  case Order(...) => context.become(processing)
}
def processing: Receive = {
  case Done(...) => context.become(waiting)
}
```

## 优势

**1. 简化并发**

无锁、无共享 = 无数据竞争。

**2. 容错**

监督树让"局部失败不影响整体",符合分布式系统现实。

**3. 分布式天然**

Actor 不论本地还是跨机器,API 一致。

**4. 弹性**

按需创建 Actor 处理任务,自动负载分布。

**5. 可观测**

每个 Actor 独立单位,日志、追踪、监控容易定位。

## 局限

**1. 心智模型变化大**

习惯 OOP / 函数式的开发者要时间适应"思考即消息流"。

**2. 调试复杂**

异步、分布、消息顺序不定,排错难。需要分布式追踪、Mailbox 监控。

**3. 性能开销**

消息传递有序列化、调度成本。CPU 密集计算用纯函数式更快。

**4. 不适合所有问题**

数据库查询、CPU 密集计算等同步性强的工作,Actor 模型并无优势。

**5. 内存泄漏**

Actor 不正确终止 → 留在系统占内存。需 PoisonPill 或 supervisor 清理。

## 在哪些场景适合

**最适合**

- 大量长连接(Discord 用 Erlang 撑数千万)
- 有状态服务(游戏匹配、对战)
- 容错关键(电信、金融)
- 物联网设备管理
- 实时多人(协作编辑、聊天)
- 工作流编排

**不适合**

- 计算密集型(科学计算)
- 简单 CRUD(REST API + 数据库够用)
- 团队不熟 Erlang/Scala/Elixir

## Actor 在分布式中

跨机器 Actor System(Akka Cluster、Erlang OTP):

- Actor 引用透明分布式(本机 vs 远程一样调)
- Sharding:Actor 按 ID hash 分布到节点
- Singleton:全局唯一 Actor(协调器)
- Persistence:Actor 状态持久化、宕机后从事件流恢复

是 [[微服务]] 的另一种实现路径——服务即 Actor,无需显式 RPC。

## 与微服务对比

| 维度 | Actor 模型 | 微服务 |
|---|---|---|
| 粒度 | 极细(对象级) | 服务级 |
| 通信 | 消息(框架内) | RPC / REST / 消息(跨服务) |
| 部署 | 一个集群 | 各自独立 |
| 状态 | 内存 + 持久化 | 各服务独自数据库 |
| 团队边界 | 弱(单代码库) | 强(各自独立) |
| 工具 | Akka / Erlang | K8s + 网关 |

Actor 模型适合"单一团队 + 高并发 + 强一致";微服务适合"多团队 + 多语言 + 弱一致"。

## 实战工具

- **Akka(Scala/Java)**:JVM 主流
- **Pekko**:Akka Apache 分叉(开源友好)
- **Erlang/OTP**:电信级
- **Elixir/Phoenix**:Web 友好
- **Microsoft Orleans**:.NET
- **Actix(Rust)**:[[Actix与Axum]]
- **CAF**:C++ Actor Framework

## 和其他概念的关系

Actor 模型与 [[Go goroutine与channel]] CSP 并称两大并发原语,共同构成现代并发编程基础。它在 [[Phoenix LiveView]]、[[微服务]] 容错、[[分布式追踪]] 等场景大量应用。

它的"消息驱动"哲学与 [[响应式编程]]、[[消息队列]]、[[事件溯源]] 等架构思想一脉相承——通过异步消息解耦、提高弹性。

它的监督树思想与 [[Circuit Breaker]]、[[Saga模式]] 等弹性模式同源——接受失败、限制爆炸半径、有恢复策略。这是软件工程从"避免错误"到"接受错误"的成熟标志。

## 参考源

- raw/计算机/
- 相关:[[Go goroutine与channel]]、[[Phoenix LiveView]]、[[微服务]]
