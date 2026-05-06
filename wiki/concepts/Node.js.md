---
title: Node.js
type: concept
tags: [cs, web, backend, mature]
sources: [raw/计算机/开发学习/语言/Node JS/]
created: 2026-05-05
updated: 2026-05-05
summary: Node.js 是 Ryan Dahl 2009 年基于 V8 引擎打造的 JavaScript 服务器运行时,以单线程事件循环 + libuv 非阻塞 IO 模型,使 JS 走出浏览器主导后端、CLI、桌面应用。
---

# Node.js

## 定义

**Node.js** 是 Ryan Dahl 2009 年发布的开源 JavaScript 服务器运行时,基于 Google V8 引擎和 C 库 libuv。它的核心创新:**单线程事件循环 + 非阻塞异步 IO**,让 JavaScript 离开浏览器,在服务器、命令行、桌面、IoT、嵌入式领域全面铺开。Node 让"前后端用同一种语言"成为现实,催生了庞大的 NPM 生态(2024 已 270 万+ 包)。

## 核心要点

### 1. 架构

```
┌──────────────────────────────┐
│   你的 JS 代码                │
├──────────────────────────────┤
│   Node 标准库(fs/http/...)   │
├──────────────────────────────┤
│   V8 引擎     │   libuv       │
└───────────────┴──────────────┘
                   │
            事件循环 + 线程池
```

### 2. 事件循环

详见 [[事件循环]]。Node 的事件循环 6 阶段:timers → pending callbacks → idle → poll → check → close。每阶段微任务(Promise.then)立即清空。

### 3. 非阻塞 IO

文件、网络、DNS 操作全是异步:

```js
fs.readFile('a.txt', (err, data) => { ... });
// 等价 Promise:
const data = await fsp.readFile('a.txt');
```

底层:libuv 把请求丢给线程池或 epoll/kqueue,完成后回调入事件循环。

### 4. 模块系统

详见 [[JS模块系统]]:CommonJS(require)与 ESM(import)并存。Node 22+ 同步 require ESM 缓解互操作。

### 5. 生态优势

- **NPM**:全球最大包仓库
- **跨平台**:同代码 Windows/macOS/Linux
- **JSON 一等公民**:与 [[RESTful API]] / [[GraphQL]] 天然契合
- **快速原型**:几行 Express 起 HTTP 服务

### 6. 典型用途

- **Web 后端**:[[Express]]、Koa、Fastify、NestJS、Hono
- **API 网关**:[[API网关模式]]
- **实时服务**:[[WebSocket]] / [[SSE]] / 聊天
- **构建工具**:[[Webpack]]、[[Vite]]、esbuild、Rollup
- **CLI 工具**:NPM 工具、create-* 脚手架
- **SSR/SSG**:[[Next.js]]、Nuxt
- **桌面应用**:Electron(Node + Chromium)
- **服务端渲染 + AI Agent**:LLM 调用流式代理

### 7. 性能特点

- 单线程,但高并发 IO 表现优秀
- CPU 密集型差(用 worker_threads 或外迁)
- 启动比 Java/.NET 快得多
- 比纯 Go/Rust 慢,但开发速度优势明显

### 8. 与同类对比

| 运行时 | 引擎 | 特点 |
|---|---|---|
| Node.js | V8 | 主流,生态最大 |
| **Deno**(Ryan Dahl 2.0) | V8 | TS 原生、Web 标准 API、安全沙箱 |
| **Bun** | JavaScriptCore | Zig 实现,极快,内置打包/测试 |
| **Edge Runtimes** | V8 Isolate | Cloudflare Workers、Vercel Edge |

Bun 与 Deno 对 Node 形成挑战,但 Node 仍是企业默认。

### 9. 现代特性(Node 22 LTS)

- 内建 fetch、test runner、watch 模式
- ESM 同步 require(无 top-level await 时)
- WebSocket 客户端(无需 ws 包)
- `--experimental-strip-types` 直接跑 TS
- Permission Model(类 Deno)

### 10. 部署

- PM2 / systemd 进程管理
- Docker(常用)
- Serverless:Vercel、AWS Lambda、Cloudflare Pages Functions
- VPS:Linux + Nginx 反代

## 关系

- 引擎:V8(Chrome 同款)
- 模块:[[JS模块系统]] CJS + ESM
- 异步:[[事件循环]]、[[Promise与异步]] / async-await
- 框架:[[Express]]、[[NestJS]]、Koa、Fastify、Hono
- 应用:[[Next.js]]、[[Webpack]]、[[Vite]]、[[Electron]]
- 对比:Deno、Bun、Edge Runtimes

## 参考源

- raw/计算机/开发学习/语言/Node JS/01-基础认知/
- raw/计算机/开发学习/语言/Node JS/02-核心理解/
