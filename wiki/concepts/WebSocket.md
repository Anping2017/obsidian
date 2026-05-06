---
title: WebSocket
type: concept
tags: [cs, web, network, frontend, mature]
sources: [raw/计算机/开发学习/语言/HTML/, raw/计算机/开发学习/语言/Javascript/]
created: 2026-05-05
updated: 2026-05-05
summary: WebSocket 是 RFC 6455 标准的全双工长连接协议,通过 HTTP Upgrade 升级到 ws:// 后实现毫秒级双向推送,聊天、协作、实时面板的标准通信层。
---

# WebSocket

## 定义

**WebSocket** 是 2011 年 IETF 在 RFC 6455 中标准化的应用层协议,提供**单 TCP 连接上的全双工通信**。它通过一次 HTTP `Upgrade` 握手切换协议,后续以二进制/文本帧双向自由交换,无需轮询。WebSocket 解决了 [[HTTP协议]] 请求-响应模式下"服务器无法主动推送"的根本限制。

## 核心要点

### 1. 握手过程

客户端发出标准 HTTP 请求,带 `Upgrade: websocket` 与 `Sec-WebSocket-Key`。服务器返回 101 Switching Protocols 响应后,该连接脱离 HTTP 语义,进入 WebSocket 帧协议。

### 2. 帧结构

每帧约 2-14 字节首部 + 可变载荷:

- **opcode**:文本(0x1)、二进制(0x2)、ping/pong(0x9/0xA)、close(0x8)
- **mask**:客户端到服务器必须掩码,防代理缓存中毒
- **payload length**:7/16/64 位三档变长

帧体积远小于 HTTP 首部(后者数百字节起步),适合高频小消息。

### 3. 与 HTTP 长轮询对比

| 模式 | 延迟 | 服务器开销 | 双向 |
|---|---|---|---|
| 短轮询 | 高 | 高 | 否 |
| 长轮询 | 中 | 中 | 否 |
| [[SSE]] | 低 | 低 | 单向(server→client) |
| WebSocket | 极低 | 低 | 是 |

### 4. 子协议(Subprotocol)

通过 `Sec-WebSocket-Protocol` 头协商上层协议(如 STOMP、MQTT-over-WS、GraphQL Subscription)。这层抽象让 WebSocket 成为通用传输底座。

### 5. 心跳与重连

WebSocket 不像 HTTP 有内置超时,中间代理可能在闲置 30-300 秒后断开。生产系统必须实现:ping/pong 心跳、指数退避重连、消息序列号去重。

### 6. 鉴权

握手是 HTTP,可携带 Cookie / Authorization 头;但浏览器原生 WebSocket API 不支持自定义首部,常用方案是把 token 放入子协议字段或首条消息。

## 适用场景

- 即时聊天、IM、客服(微信、Slack)
- 协作编辑(Figma、Google Docs 的实时光标)
- 实时仪表盘、股票/币价行情
- 多人在线游戏
- IoT 设备双向控制

## 关系

- 升级自:[[HTTP协议]] 通过 Upgrade 头
- 对比:[[SSE]] 是单向、自动重连、纯 HTTP 的轻量替代
- 替代:HTTP 长轮询、Comet
- 跑在:[[HTTP2协议]] 之上的扩展 RFC 8441 让 WS 也能享受多路复用
- 安全:wss:// 走 TLS,与 [[Web安全]] 同等保护

## 参考源

- raw/计算机/开发学习/语言/HTML/04-知识拓展层/技术生态集成/04-3 前后端数据交互.md
