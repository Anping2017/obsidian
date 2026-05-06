---
title: I/O模型
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: I/O 模型按"等待数据-拷贝数据"两阶段是否阻塞分为五种——阻塞、非阻塞轮询、I/O 多路复用、信号驱动、异步,决定高并发服务的架构。
---

# I/O模型

## 定义

**I/O 模型** 描述用户态进程发起 I/O 请求(读写文件、Socket)时,如何与 [[操作系统]] 内核协作完成"等待数据就绪"和"把数据从内核拷贝到用户空间"两个阶段。Stevens 在 UNP 中归纳为五种,是高性能网络服务架构的根本。

## 核心要点

- **阻塞 I/O(Blocking)**
  - `read` 一直阻塞到数据准备好并复制完成。
  - 简单直观,每连接一线程模型;C10K 之前主流。
  - 上下文切换 + 内存开销限制并发数。
- **非阻塞 I/O(Non-Blocking)**
  - `O_NONBLOCK` 标志,数据未就绪立即返回 EAGAIN。
  - 用户需轮询,CPU 浪费严重,几乎不单独使用。
- **I/O 多路复用(I/O Multiplexing)**
  - 用 `select`/`poll`/`epoll`(Linux)/`kqueue`(BSD/macOS)/`IOCP`(Windows)同时监听多个 fd。
  - 单线程可服务数万连接,事件驱动。
  - 是 nginx、Redis、Node.js、Netty 的底层。
  - **epoll 三系统调用**:`epoll_create`、`epoll_ctl`、`epoll_wait`;支持边缘触发(ET)与水平触发(LT)。
- **信号驱动 I/O(Signal-driven)**
  - 注册 SIGIO 处理函数,内核就绪时发信号;实际较少使用。
- **异步 I/O(Asynchronous)**
  - 真正"发出请求即返回",数据复制完成后由内核通知。
  - POSIX AIO 在 Linux 实现弱;`io_uring`(Linux 5.1+)是新一代——共享环形缓冲区,系统调用开销极低。
  - Windows IOCP 是工业级 AIO 代表。
- **同步 vs 异步、阻塞 vs 非阻塞**
  - 同步指调用方关心结果时机、异步指内核通知;阻塞指等待与否。
  - 多路复用本质是同步非阻塞——用户线程同步等就绪,但不为单个连接阻塞。

## 关系

- 是 [[并发与并行]] 在 I/O 层的直接体现——高并发服务大都建立在多路复用 + 事件循环。
- [[JavaScript事件循环]] 用 libuv 在 Linux 上封装 epoll、在 Windows 上用 IOCP。
- [[Go goroutine与channel]] 用 netpoller 在内部用 epoll/kqueue,把 goroutine 暴露给用户的"看似阻塞"语义实现为多路复用。
- [[Python协程]] asyncio 同样基于 selector 抽象多路复用。
- [[零拷贝]] 是在 I/O 模型之上进一步消除用户态拷贝的优化技术。
- [[Epoll与Kqueue]] 是 I/O 多路复用的具体实现细节。

## 参考源

- raw/计算机/(I/O 在 Python 异步、Node.js、运维系统中均涉及)
- raw/计算机/开发学习/语言/Python/03_理解层-深度原理与机制/3.2.3 async-await异步编程.md
