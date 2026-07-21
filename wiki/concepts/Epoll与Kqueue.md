---
title: Epoll与Kqueue
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: epoll 和 kqueue 分别是 Linux 和 BSD/macOS 提供的高效事件通知接口,用 O(1) 关注 fd 集合替代 O(n) 的 select/poll,是高并发服务的基石。
---

# Epoll与Kqueue

## 定义

**epoll** 是 Linux 2.5.44 引入的事件通知接口,**kqueue** 是 BSD/macOS 1999 年引入的等价物。两者都用内核维护"关注 fd 集合 + 就绪集合"的数据结构,把 I/O 多路复用的复杂度从 `select/poll` 的 O(n) 降到 O(1)(就绪 fd 数量),让单进程服务数十万连接成为可能。

## 核心要点

- **epoll 三步**
  - `epoll_create1(0)` 创建实例,返回 epfd。
  - `epoll_ctl(epfd, op, fd, &event)` 添加/修改/删除关注的 fd。
  - `epoll_wait(epfd, events, max, timeout)` 阻塞等待就绪事件,返回个数。
- **触发模式**
  - **水平触发(LT,Level-Triggered)**:只要可读/可写状态持续,每次 wait 都会返回 —— select/poll 默认行为,易写。
  - **边缘触发(ET,Edge-Triggered)**:仅在状态变化时触发一次,要求一次读尽缓冲区(EAGAIN 为止),性能高但易写错。
- **kqueue 特点**
  - 单一接口处理 I/O、定时器、信号、文件变更、子进程退出等多种事件。
  - `kevent` 系统调用同时做 add/modify/wait。
  - 比 epoll 更早、API 更通用,但仅 BSD/macOS。
- **select/poll 的瓶颈**
  - 每次 wait 都要复制整个 fd 集合到内核 —— O(n) 系统调用开销。
  - 内核每次都要遍历所有 fd 标记就绪 —— O(n) 内核工作。
  - epoll 用红黑树存关注集 + 就绪链表,只复制就绪事件。
- **典型使用者**
  - **nginx**、**HAProxy**、**envoy**:边缘触发 + 单线程多 worker。
  - **Redis**:单线程事件循环,基于 ae 抽象层。
  - **Node.js libuv**、**Netty**、**Tornado**、**Twisted**。
- **新一代:io_uring**
  - Linux 5.1+ 引入,共享内存环替代系统调用,真正异步;延迟更低、吞吐更高,正逐步取代 epoll 在高性能场景。

## 关系

- 是 [[I_O模型]] 中"多路复用"派的具体实现。
- 支撑 [[JavaScript事件循环]]、[[Python协程]]、[[Go goroutine与channel]] 在 Linux 上的事件驱动后端。
- 与 [[操作系统]] 内核子系统紧密耦合——网络协议栈通过 socket 文件描述符接入。
- [[零拷贝]] 与 epoll 配合,把"事件就绪 + 系统调用直传"组合成最优数据通路。
- 是 C10K → C10M 性能演进的核心技术。

## 参考源

- raw/计算机/(Linux 系统编程主题)
