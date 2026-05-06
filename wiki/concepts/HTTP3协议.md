---
title: HTTP/3 协议
type: concept
tags: [cs, web, network, frontend, mature]
sources: [raw/计算机/开发学习/语言/HTML/]
created: 2026-05-05
updated: 2026-05-05
summary: HTTP/3 是基于 QUIC(UDP)而非 TCP 的新一代 HTTP,通过用户态拥塞控制、0-RTT、连接迁移彻底解决 TCP 队头阻塞,成为移动与高延迟环境的最优解。
---

# HTTP/3 协议

## 定义

**HTTP/3** 是 [[HTTP协议]] 的第三代版本,2022 年在 RFC 9114 中标准化。最大的颠覆不在应用层,而是**用 QUIC 替换了 TCP+TLS** —— QUIC 是 Google 设计、运行于 UDP 之上的可靠传输协议,把加密、多路复用、拥塞控制都集成进单层。

## 核心要点

### 1. 为什么放弃 TCP?

[[HTTP2协议]] 在应用层用流解决了队头阻塞,但 TCP 仍要求**严格按序传递字节**:一个数据包丢失会阻塞所有上层流。在弱网/移动场景,这种 TCP HOL 阻塞抵消了多路复用的优势。

### 2. QUIC 的核心特性

- **基于 UDP**:绕开 TCP 的内核约束,在用户态实现可靠传输,迭代速度可比内核协议栈快数年
- **强制加密**:TLS 1.3 集成进握手,无明文 QUIC,提升 [[Web安全]] 基线
- **0-RTT 与 1-RTT 握手**:首次连接 1-RTT,二次访问 0-RTT(立即发数据),对比 TCP+TLS 的 3-RTT 大幅降低延迟
- **流级别独立丢包恢复**:某条流丢包不影响其他流,真正的多路复用
- **连接迁移**:连接由 Connection ID 标识(不依赖 IP+Port),手机 WiFi 切 4G 时连接不断,长视频/通话场景受益巨大

### 3. 部署现状

主流 CDN(Cloudflare、Fastly)、Google、Meta、字节跳动均已大规模部署。浏览器(Chrome、Firefox、Safari、Edge)默认支持。回退机制:首次仍走 HTTP/2 over TCP,通过 Alt-Svc 头宣告 HTTP/3 端点,后续访问升级。

### 4. 工程挑战

- 防火墙/NAT 对 UDP 不友好,部分企业网络需调整规则
- UDP 易被运营商限速或丢弃
- 服务端 CPU 开销高于 TCP(用户态 vs 内核 offload)

## 协议栈对比

```
HTTP/1.1  HTTP/2     HTTP/3
   |         |          |
  TCP       TCP        QUIC
            TLS         |
                       UDP
```

HTTP/3 把传输 + 加密 + 流复用三层合一为 QUIC,层数变少但单层能力变强。

## 关系

- 演进自:[[HTTP2协议]] 的多路复用
- 替换:TCP 在 HTTP 场景下的角色
- 集成:TLS 1.3 加密握手,与 [[Web安全]] 默认强绑定
- 受益:移动 [[RESTful API]]、视频流、[[微服务]] 间通信
- 对比:WebSocket 的长连接思路被 QUIC 流替代部分场景

## 参考源

- raw/计算机/开发学习/语言/HTML/04-知识拓展层/新兴技术趋势/
- 已有 wiki: [[HTTP协议]]
