---
title: TCP 传输控制协议
type: concept
tags: [network, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: TCP 是面向连接、可靠、有序、字节流的传输层协议,是互联网的基石,通过三次握手、滑动窗口、拥塞控制保证可靠传输。
---

# TCP 传输控制协议

## 定义

**TCP(Transmission Control Protocol,传输控制协议)** 是 TCP/IP 协议族中**传输层**的核心协议,RFC 793(1981)定义,由 Vint Cerf 和 Bob Kahn 提出。它在不可靠的 IP 之上,为应用层提供:

- **面向连接(Connection-oriented)**:三次握手建立、四次挥手释放;
- **可靠传输(Reliable)**:确认重传机制保证不丢、不错;
- **有序交付(In-order)**:基于序列号还原正确次序;
- **字节流(Byte stream)**:无报文边界,应用自行分隔;
- **流量控制 + 拥塞控制**:适配收发双方处理能力与网络状况。

TCP 与 **UDP** 是传输层最主流的两个协议,二者形成"可靠/重 vs 轻量/快"的经典对照,见 UDP 条目对比说明。

## 核心要点

### 三次握手与四次挥手

- **建立(Three-Way Handshake)**:Client → SYN → Server → SYN+ACK → Client → ACK → 连接建立。
- **关闭(Four-Way Handshake)**:任一方 FIN → 对方 ACK → 对方 FIN → 己方 ACK → 完全关闭。

详细图示与 TIME_WAIT 状态见 [[TCP握手与挥手]]。

### 报文头(简版 20 字节)

| 字段 | 作用 |
|---|---|
| 源端口 / 目的端口 | 16 bit,定位应用进程 |
| 序列号 / 确认号 | 32 bit,字节级编号 |
| 标志位 | SYN/ACK/FIN/RST/PSH/URG |
| 窗口大小 | 接收端可接受的字节数(流控) |
| 校验和 | 端到端数据完整性 |
| 选项 | MSS、SACK、时间戳、窗口缩放 |

### 可靠性机制

- **序列号 + 确认号**:每字节有唯一编号,丢失即重传。
- **超时重传(RTO)**:动态估算 RTT,自适应。
- **快速重传**:收到 3 个重复 ACK,立即重传不等超时。
- **SACK(选择确认)**:精确告知哪些字节缺失,避免全部重传。

### 流量控制(Flow Control)

通过**滑动窗口**实现:接收端通告剩余 buffer 大小,发送端不超发,防止淹没接收端。

### 拥塞控制(Congestion Control)

为保护网络整体,有四阶段经典算法:**慢启动、拥塞避免、快速重传、快速恢复**。现代算法演进:Reno → CUBIC(Linux 默认)→ BBR(Google 2016,基于带宽-延迟模型)。

### 与上层协议的关系

[[HTTP协议]]、[[HTTPS]]、SSH、SMTP、POP3、IMAP、FTP、Telnet 等绝大多数应用层协议建立在 TCP 之上。HTTP/3 / [[QUIC]] 是首批主流"绕开 TCP"的协议,改用 UDP。

## 典型应用 / 主要工具

- **诊断**:tcpdump、Wireshark、ss、netstat、`/proc/net/tcp`。
- **性能调优**:iperf3、netperf 测试带宽与延迟。
- **内核参数**:`sysctl net.ipv4.tcp_congestion_control`、`tcp_window_scaling`、`tcp_mtu_probing`。
- **应用场景**:几乎所有 Web、文件传输、邮件、远程登录;直播 / 游戏 / DNS / VoIP 等延迟敏感场景常用 UDP。
- **加速器**:BBR、TCP Fast Open、TLS 0-RTT 减少首字节延迟。

## 局限与陷阱

- **队头阻塞(HoL Blocking)**:单字节流前面字节丢失,后续即使收到也阻塞,[[QUIC]] 借此优化。
- **握手延迟**:首次连接 1.5 RTT,跨大陆链路可达 100ms+;TFO 可缓解。
- **NAT 与防火墙**:连接状态依赖 NAT 表,长连接常被中间盒重置。
- **慢启动惩罚短连接**:小请求未充分利用带宽,HTTP/1.1 keep-alive、HTTP/2 多路复用是缓解。
- **无消息边界**:应用必须自定分包,粘包/拆包 bug 是新人常踩坑。
- **TIME_WAIT 累积**:高并发短连接服务器会累积大量 TIME_WAIT,需 SO_REUSEADDR、连接复用。

## 与其他概念的关系

- 直接对照:与 **UDP** 形成传输层双轨,UDP 提供轻量、无连接、不可靠的服务,适合 DNS、VoIP、游戏、视频。详细对照见 UDP 条目。
- 上层协议:[[HTTP协议]]、[[HTTPS]]、HTTP/2、SSH 等基于 TCP。
- 下一代替代:[[QUIC]] 基于 UDP 实现 TCP 类可靠性,作为 TCP 在 Web 场景的替代。
- 安全延伸:[[TLS]] 通常运行在 TCP 之上;[[HTTPS与TLS握手]] 详述完整握手过程。
- 关闭过程:[[TCP握手与挥手]] 描述完整连接生命周期。
- 网络全景:与 [[网络协议]]、[[网络效应]] 等条目共同构成网络主题。

## 参考源

- IETF RFC 9293(2022)更新合并的 TCP 规范
- Stevens 著《TCP/IP Illustrated》卷一
- Linux Kernel Documentation: networking/tcp.rst
