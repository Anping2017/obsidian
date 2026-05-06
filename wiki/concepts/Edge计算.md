---
title: Edge 计算
type: concept
tags: [cs, web, infrastructure, mature]
sources: [raw/计算机/开发学习/语言/HTML/04-知识拓展层/新兴技术趋势/]
created: 2026-05-05
updated: 2026-05-05
summary: Edge 计算把代码运行在 CDN 全球节点上,毫秒级触达用户,Cloudflare Workers、Vercel Edge、Deno Deploy 是主流平台,V8 Isolate 启动速度比容器快百倍。
---

# Edge 计算

## 定义

**Edge 计算(Edge Computing)** 在 Web 上下文中,通常指**把应用代码部署到 CDN 全球数百个节点**,在离用户最近的边缘运行,而非集中在某地区数据中心。它结合了 CDN 的低延迟与 Serverless 的按需计算,代表平台:Cloudflare Workers、Vercel Edge Functions、Deno Deploy、AWS Lambda@Edge、Netlify Edge。

## 核心要点

### 1. 与传统部署对比

| 模式 | 延迟来源 | 启动 |
|---|---|---|
| 中心化云(AWS us-east-1) | 跨洲网络 RTT | VM/容器 |
| Serverless(AWS Lambda) | 区域内 + 冷启动 | 容器(50ms-2s 冷启动) |
| Edge Workers | 末端节点(<10ms) | V8 Isolate(<5ms) |

### 2. V8 Isolate vs 容器

Cloudflare Workers 不为每函数起容器,而在共享 V8 进程中创建轻量 Isolate:

- 内存隔离但共享 V8 引擎
- 启动 5ms 内,几乎零冷启动
- 单节点可承载数千函数
- 代价:仅 JS/Wasm 运行时,不能跑任意 Linux 二进制

### 3. 限制(以 Cloudflare 为例)

- CPU 时间:免费 10ms / 付费 30s+
- 内存:128MB
- 不能用 Node.js 全部 API(只有 Web 标准 + Cloudflare 特定 API)
- 包大小:1-10MB
- 没有持久文件系统(用 KV / R2 / D1)

### 4. 适用工作负载

- API 网关 / 路由
- 鉴权(JWT 校验)
- A/B 测试 / 个性化
- 图片转换
- 地理重定向 / 国际化
- 边缘缓存 / SSR(Vercel Edge SSR)
- LLM 流式代理(Cloudflare AI Gateway)

不适用:重 CPU/IO(视频转码)、需 Node 全 API、长事务。

### 5. 边缘数据存储

- **Cloudflare KV**:全球读快、最终一致
- **Cloudflare D1**:边缘 SQLite,区域强一致
- **Cloudflare R2**:S3 兼容对象存储,无出站费
- **Vercel KV / Postgres**:Upstash Redis、Neon Postgres
- **Deno KV**:基于 FoundationDB

### 6. 与 SSR / RSC 联动

[[Next.js]] 13+ 的 Edge Runtime:Middleware、API、SSR 都可跑在 Edge。
[[ISR]] 命中边缘缓存,首字节毫秒级。

### 7. 标准化:Web Standard Runtime

Edge 平台普遍支持 Web 标准 API(fetch、Request、Response、Streams、Crypto),而非 Node-specific。这催生 WinterCG(Web-interoperable Runtimes Community Group),标准化跨平台运行时。

### 8. 安全考量

- 多租户共享 V8 → 侧信道隔离极重要
- 密钥管理:用环境变量 + Secret 存储
- 请求体大小限制
- DDoS:由 CDN 平台兜底

### 9. 趋势

- Edge AI:Cloudflare Workers AI 在边缘跑小模型
- Edge Database:数据接近代码接近用户
- WebAssembly:让 Rust/Go/C 也能跑 Edge

## 关系

- 部署:[[Next.js]]、Astro、Remix、SvelteKit
- 运行时:V8 Isolate、[[WebAssembly]]
- 存储:边缘 KV/数据库
- 协议:[[HTTP3协议]] / QUIC 进一步降延迟
- 渲染:[[SSR]]、[[ISR]] 的天然搭档

## 参考源

- raw/计算机/开发学习/语言/HTML/04-知识拓展层/新兴技术趋势/04-13 边缘计算与HTML.md
- raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md
