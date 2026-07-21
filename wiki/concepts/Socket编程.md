---
title: Socket编程
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Socket 是网络通信的端点抽象,通过 BSD Socket API(socket/bind/listen/accept/connect/send/recv)实现 TCP/UDP/Unix 域跨语言可移植网络编程。
---

# Socket编程

## 定义

**Socket** 是网络通信的端点抽象——由 IP 地址 + 端口号(网络套接字)或路径(Unix 域套接字)唯一标识,应用通过 Socket API 发送和接收数据。BSD Socket(1983)成为事实标准,被 POSIX 收编,所有现代 OS 与语言都提供。

## 核心要点

- **基本 API**(C 风格,语义跨语言一致)
  - `socket(AF_INET, SOCK_STREAM, 0)`:创建套接字描述符。
  - `bind(sockfd, addr, len)`:绑定本地地址。
  - `listen(sockfd, backlog)`:转为被动套接字。
  - `accept(sockfd, ...)`:阻塞等待连接,返回新连接 fd。
  - `connect(sockfd, addr, len)`:主动建立连接。
  - `send/recv` 或 `read/write`:数据传输。
  - `close(sockfd)`:关闭。
- **协议族与类型**
  - **AF_INET / AF_INET6**:IPv4 / IPv6。
  - **AF_UNIX**:Unix 域,本机进程通信,绕过协议栈。
  - **SOCK_STREAM**:面向连接(TCP)。
  - **SOCK_DGRAM**:无连接(UDP)。
  - **SOCK_RAW**:原始套接字(ping、抓包)。
- **TCP 关键状态机**
  - 三次握手建立、四次挥手关闭。
  - TIME_WAIT、CLOSE_WAIT 是常见排查点。
  - **Nagle 算法 / TCP_NODELAY**:小包合并 vs 低延迟取舍。
  - **Keep-Alive**、**SO_REUSEADDR/SO_REUSEPORT**:常见 socket 选项。
- **服务端模型演进**
  - **每连接一进程/线程**:简单但 C10K 瓶颈。
  - **预派 fork(prefork)/线程池**:Apache 经典。
  - **事件驱动单线程**:基于 [[Epoll与Kqueue]],nginx/Redis。
  - **多 Reactor**:主 Reactor 接连接、子 Reactor 处理 I/O,Netty/Tornado。
  - **多线程 + 协程**:Go 的标准库直接屏蔽这些细节。
- **常见陷阱**
  - **粘包**:TCP 是字节流,需应用层定边界(长度前缀或定界符)。
  - **半连接队列 / 全连接队列**:`tcp_max_syn_backlog`、`somaxconn` 配置不当导致连接被丢。
  - **TIME_WAIT 堆积**:大量短连接耗尽端口,SO_REUSEADDR/连接复用缓解。

## 关系

- 是 [[I_O模型]] 与 [[Epoll与Kqueue]] 操作的具体对象。
- 通过 Socket API 实现 [[HTTP协议]]、gRPC、MQTT 等高层协议。
- [[操作系统]] 内核网络协议栈是 Socket 的实现基础;TCP/UDP/IP 在内核态。
- [[内核态与用户态]] 切换在每个 send/recv 都发生,因此 [[零拷贝]]、io_uring 优化收益明显。
- [[Go goroutine与channel]]、[[Python协程]]、[[JavaScript事件循环]] 都在 Socket 之上构建高并发抽象。

## 参考源

- raw/计算机/(网络主题分散)
