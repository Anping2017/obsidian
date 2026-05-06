---
title: Go goroutine与channel
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Go 用轻量级用户态 goroutine + channel 实现 CSP 并发模型,go 关键字开协程几微秒,channel 提供类型化同步通信,是 Go 最具特色的设计。
---

# Go goroutine与channel

## 定义

**goroutine** 是 Go 的轻量级用户态协程,由 Go 运行时调度到一组 OS 线程上(M:N 调度);**channel** 是类型化、可缓冲或无缓冲的 FIFO 通信原语,把 CSP(Communicating Sequential Processes)思想变成语言一等公民。Go 提倡 "Don't communicate by sharing memory; share memory by communicating"。

## 核心要点

- **goroutine 特性**
  - 启动:`go f(x)`,启动开销几微秒,栈初始 2KB 可动态伸缩到 GB 级。
  - 调度:GMP 模型——G(goroutine)、M(OS 线程)、P(处理器逻辑核 / 调度上下文);Work-Stealing 平衡负载。
  - 抢占:Go 1.14 起信号驱动异步抢占,长循环不再阻塞调度。
- **channel 类型**
  - **无缓冲**:发送者阻塞直到接收者读;天然同步点。
  - **有缓冲**:`make(chan T, n)`,缓冲未满时发送非阻塞;近似生产消费队列。
  - **方向限定**:`chan<- T` 只发、`<-chan T` 只收,API 自文档。
- **关键操作**
  - `select { case <-ch: ... case ch <- x: ... default: ... }`:多路复用、非阻塞、超时。
  - `close(ch)`:关闭后接收返回零值且 `ok=false`;不能关闭只读 channel,不能向已关闭 channel 发送。
  - `range ch`:循环消费直到 channel 关闭。
- **常见模式**
  - **Pipeline**:多 stage,每个 stage 一个 goroutine + channel。
  - **Worker Pool**:固定 worker 数量从同一 channel 取任务。
  - **Fan-in / Fan-out**:多 producer 合并、单 producer 分发。
  - **Done channel**:取消传播,Go 1.7+ 推荐用 `context.Context`。
- **陷阱**:goroutine 泄漏(无人接收阻塞)、过度共享导致竞争、闭包捕获循环变量。

## 关系

- 是 [[并发与并行]] 在 Go 语言中的核心抽象,与 [[Python协程]]/asyncio、[[JavaScript事件循环]] 同属用户态并发但更接近 OS 多线程语义。
- 实现层面用 [[操作系统]] 多线程做载体,GMP 在用户态做调度,避免 OS 线程切换开销。
- 与 [[Rust所有权]] 的所有权 + 通道(`std::sync::mpsc`)思想接近,但 Go 内存模型更宽松、类型系统更简单。
- 配合 Go 接口实现的[[依赖倒置]],让并发抽象在大型服务中可组合。
- 是 Kubernetes、Docker、etcd、CockroachDB 等基础设施选 Go 的关键原因。

## 参考源

- raw/计算机/(Go 内容散落在并发对比章节)
- raw/计算机/开发学习/语言/Python/03_理解层-深度原理与机制/3.2.4 协作式并发vs抢占式并发.md
