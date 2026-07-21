---
title: QUIC 基于UDP的传输协议
type: concept
tags: [network, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: QUIC 是 Google 提出、IETF 标准化的基于 UDP 的传输层协议,集成 TLS 1.3,解决 TCP 队头阻塞与握手延迟,是 HTTP/3 的底层。
---

# QUIC 基于UDP的传输协议

## 定义

**QUIC(Quick UDP Internet Connections)** 是一种基于 UDP 的现代传输层协议,由 Google 在 2012 年提出,2021 年由 IETF 标准化为 RFC 9000。它把传输层(类似 TCP 的可靠性、拥塞控制、有序传输)与安全层([[TLS]] 1.3)整合到一个协议中,跑在 UDP 之上,成为 HTTP/3 的底层传输。

QUIC 的核心目标是:在传输层层面**消除 TCP 的固有缺陷**(队头阻塞、僵化的握手、连接迁移困难)以适应移动互联网与高 RTT 网络场景。

## 核心要点

### 为什么不直接改 TCP

TCP 由操作系统内核实现,部署节奏被中间盒(NAT、防火墙、负载均衡)严重拖累。QUIC 跑在用户态 UDP 之上,任何应用都能携带自己的 QUIC 栈,迭代速度从"年"降到"周"。

### 0-RTT / 1-RTT 握手

- **首次连接(1-RTT)**:客户端在第一个数据包就携带 TLS ClientHello,服务器在第一个响应包就返回密钥与应用数据,握手与数据合并。
- **复用连接(0-RTT)**:基于上次会话票据,客户端可在第一包就发送加密应用数据。

相比 TCP+TLS 的约 2.5-RTT(TCP 三次握手 1.5 RTT + TLS 1.3 握手 1 RTT),QUIC 显著降低首字节延迟。

### 多路复用 + 解决队头阻塞

QUIC 在单连接内支持多个**独立 stream**,每个 stream 独立排序与重传。某个 stream 丢包时,不会阻塞其他 stream(对比 [[HTTP2协议]] 在 TCP 之上仍受单条 TCP 流队头阻塞影响)。

### 连接迁移(Connection Migration)

QUIC 用 **Connection ID** 标识连接,而非 (源 IP, 源端口, 目的 IP, 目的端口) 四元组。手机从 Wi-Fi 切到 4G、IP 变化时,连接可继续,无需重连。

### 内置加密

整个 QUIC 包(包头大部分 + 全部载荷)默认 TLS 1.3 加密,中间盒难以解析或修改,既保护隐私也防御协议僵化(Ossification)。

### 拥塞控制

QUIC 在用户态实现拥塞控制(默认 NewReno / CUBIC,可换 BBR),应用可独立优化算法,而无需修改内核。

## 典型应用 / 主要工具

- **HTTP/3**:QUIC 是 [[HTTP3协议]] 的底层,Cloudflare、Google、Akamai、Fastly 均已大规模启用。
- **gRPC over QUIC**:微服务跨地域调用,降低尾延迟。
- **WebTransport**:基于 QUIC 的浏览器双向流通信 API,替代 WebSocket 的下一代选项。
- **MASQUE / VPN**:Apple Private Relay 等代理服务依赖 QUIC 实现端到端加密隧道。
- **客户端实现**:Chromium QUIC、quinn(Rust)、msquic(微软)、quic-go、aioquic。

## 局限与陷阱

- **CPU 成本**:用户态 + 加密所有数据,服务端 CPU 比 TCP+TLS 高 2—3 倍,需硬件卸载或 BBR 弥补。
- **UDP 阻塞**:部分企业网络与运营商对 UDP 限速或丢包,QUIC 性能反而劣于 TCP,需要 fallback 机制。
- **可观测性差**:中间盒无法解析 QUIC 包,传统抓包诊断工具(Wireshark 之外)缺乏成熟支持。
- **协议复杂度**:实现栈代码量数倍于 TCP,内存安全漏洞面更大。
- **生态尚在演进**:CDN、负载均衡、WAF 对 QUIC 的支持远不及 TCP 成熟。

## 与其他概念的关系

- 上层应用:[[HTTP3协议]] 直接构建在 QUIC 之上,继承全部优势。
- 底层基础:跑在 UDP 之上,集成 [[TLS]] 1.3 加密握手。
- 技术对比:与 [[TCP握手与挥手]]、[[网络协议]] 形成传输层方案对照,差异在握手次数与队头阻塞。
- 应用范围:与 [[HTTPS与TLS握手]] 紧密相关,QUIC 把 TLS 握手吸收进协议本身。
- 工程实践:CDN 与 [[微服务]] 跨地域通信普遍考虑 QUIC,带来连接迁移与低延迟优势。

## 参考源

- IETF RFC 9000: QUIC: A UDP-Based Multiplexed and Secure Transport (2021)
- IETF RFC 9001/9002: TLS for QUIC、Loss Detection and Congestion Control
- Cloudflare、Google QUIC 实践博客
