---
title: SSE 服务器推送事件
type: concept
tags: [cs, web, network, frontend, mature]
sources: [raw/计算机/开发学习/语言/HTML/, raw/计算机/开发学习/语言/Javascript/]
created: 2026-05-05
updated: 2026-05-05
summary: SSE(Server-Sent Events)是 HTML5 标准的单向服务器推流协议,基于 text/event-stream MIME 类型,通过原生 EventSource API 提供自动重连、消息 ID、事件分类。
---

# SSE 服务器推送事件

## 定义

**SSE(Server-Sent Events)** 是 HTML5 规范定义的服务器到客户端**单向推送**协议。本质是一个永不结束的 HTTP 响应,Content-Type 为 `text/event-stream`,服务器持续写入 `data: xxx\n\n` 格式的事件块。浏览器通过原生 `EventSource` API 接收。

## 核心要点

### 1. 协议格式

```
data: {"price": 100}\n
\n
data: {"price": 101}\n
id: 42\n
event: priceUpdate\n
\n
```

字段:
- `data`:消息体(可多行)
- `id`:消息 ID,用于断线重连后 `Last-Event-ID` 续传
- `event`:自定义事件名,前端可分类监听
- `retry`:重连间隔(毫秒)

### 2. EventSource API

```js
const es = new EventSource('/api/stream');
es.onmessage = (e) => console.log(e.data);
es.addEventListener('priceUpdate', (e) => {...});
es.onerror = () => {/* 自动重连 */};
```

浏览器自动处理:断线重连、消息 ID 续传、UTF-8 解码。

### 3. 与 WebSocket 对比

| 维度 | SSE | [[WebSocket]] |
|---|---|---|
| 方向 | 单向(下行) | 双向 |
| 协议 | 标准 HTTP | 升级协议 |
| 重连 | 内置 | 需手写 |
| 二进制 | 仅文本 | 文本+二进制 |
| 代理友好度 | 高(纯 HTTP) | 中(部分代理拦截) |
| 浏览器支持 | 现代主流(IE 除外) | 全主流 |

**结论**:只需服务器推送(行情、通知、AI 流式输出)时优先 SSE;需双向交互(IM、协作)时用 WebSocket。

### 4. AI 时代的复兴

LLM 流式输出(ChatGPT 打字机效果)默认用 SSE。OpenAI、Anthropic 的 chat completion 流式 API 全部基于 SSE,因为:

- 单向场景天然契合(模型生成 → 用户接收)
- 纯 HTTP 易过 CDN、防火墙
- 浏览器和 fetch 流读取均原生支持

### 5. 限制

- HTTP/1.1 下每个域名 6 连接限制(SSE 各开一条),HTTP/2 多路复用解除此限
- 仅 UTF-8 文本,不支持二进制
- 仅服务器到客户端

## 关系

- 替代:[[WebSocket]] 在单向推送场景的更轻方案
- 跑在:[[HTTP协议]]、[[HTTP2协议]] 之上
- 应用:[[大语言模型]] 流式输出的事实标准
- 对比:HTTP 长轮询(SSE 是其优雅升级版)

## 参考源

- raw/计算机/开发学习/语言/HTML/04-知识拓展层/技术生态集成/
