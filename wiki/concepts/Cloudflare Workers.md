---
title: Cloudflare Workers
type: concept
tags: [programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Cloudflare Workers 是基于 V8 Isolate 的边缘 Serverless 运行时,在 270+ 全球节点亚毫秒冷启动,配合 R2、KV、D1、Durable Objects 形成完整无服务器栈,代表了"在边缘做后端"的新范式。
---

# Cloudflare Workers

## 定义

Cloudflare Workers 是 Cloudflare 在 2017 年推出的边缘 Serverless 计算平台。它运行在 Cloudflare 全球 270+ 城市的 CDN 节点上,基于 V8 Isolate(同 Chrome 的 JS 引擎核心),实现亚毫秒冷启动、按请求计费,把 Serverless 概念从"AWS Lambda 区域级"推进到"全球边缘级"。

Workers 与 AWS Lambda 的根本差异在执行模型:Lambda 是"在某个区域起 Linux 容器跑 Node.js",冷启动数百毫秒到数秒;Workers 是"在用户最近节点的 V8 内启动一个 isolate",冷启动 < 1ms。这让 Workers 可以替代 CDN + 应用服务器的组合,把后端逻辑直接放到 CDN 边缘。

## 核心组件(Cloudflare Developer Platform)

**Workers(计算)**

- JavaScript / TypeScript / Rust(WASM)
- 50ms CPU 时间限制(免费),30s(付费)
- 128MB 内存
- 全球 270+ 城市
- 每日 100K 请求免费

**KV(键值存储)**

- 跨节点最终一致 KV
- 适合配置、Session、缓存
- 写延迟较高(秒级)

**Durable Objects**

- 强一致单实例对象
- 适合 WebSocket、聊天室、协同编辑、计数器
- 全球唯一实例

**D1(关系数据库)**

- 基于 SQLite 的边缘 SQL DB
- 自动复制只读到边缘
- 写仍走主区域

**R2(对象存储)**

- S3 兼容 API
- 零出站费(对比 S3 的高出站费用)
- 适合图片、视频、备份

**Queues**

- 消息队列
- 与 Workers 集成

**Vectorize**

- 向量数据库
- AI 嵌入式搜索

**Workers AI**

- LLM 推理(Llama、Mistral 等开源模型)
- 全球边缘运行

## 工作模型示例

```js
// worker.js
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url)

    // 路由
    if (url.pathname === '/api/users') {
      const user = await env.DB.prepare(
        'SELECT * FROM users WHERE id = ?'
      ).bind(url.searchParams.get('id')).first()

      return Response.json(user)
    }

    // 缓存与代理
    return await cache.match(request) || await fetch(request)
  }
}
```

部署:`wrangler deploy`(Cloudflare CLI)

## 与 AWS Lambda 对比

| 维度 | Cloudflare Workers | AWS Lambda |
|---|---|---|
| 冷启动 | < 1ms | 100ms-数秒 |
| 运行时 | V8 Isolate | Node.js / Python / 容器 |
| 节点 | 全球 270+ | 区域 30+ |
| 计费 | 请求 + CPU 时间 | 请求 + 持续时间(GB-秒) |
| 限制 | 50ms CPU 免费/30s 付费 | 15 分钟 |
| 生态 | 与 CF 服务集成 | 与 AWS 全栈集成 |

Workers 适合短小、低延迟、全球分布;Lambda 适合长任务、AWS 生态深度。

## 与 Vercel Edge Functions

二者底层都是 V8 Isolate(Vercel Edge 实际用 Cloudflare Workers 早期版),核心差异:
- Vercel:与 Next.js / 前端深度集成
- Cloudflare:更底层,可作为完整后端

## 主要使用场景

**1. 智能 CDN / 反代**

在边缘做 A/B 测试、AB 路由、URL 重写、Cookie 处理。

**2. API Gateway**

聚合多个后端 API,边缘处理认证、限流、缓存。

**3. 个性化静态站**

地理定位、Cookie 个性化:Edge SSR 或 Edge Function 注入。

**4. WebSocket / 实时**

Durable Objects 做聊天室、协同(Cloudflare 自家 Cloudflare Pages 的 Realtime Kits)。

**5. 全栈应用**

Workers + D1 + R2 + Pages 完整 Serverless 栈,无需自有服务器。

**6. 边缘 AI**

Workers AI 让小型 LLM(< 10B)在边缘推理,延迟极低。

## 与 Cloudflare Pages

Cloudflare Pages = 静态站托管 + Workers 集成,类比 Vercel。
- 静态资源走 CDN
- 动态逻辑用 Workers Functions

适合 Next.js、Astro、SvelteKit 等前端框架部署。

## 限制与注意

**API 限制**

- 不是 Node.js,某些 npm 包(用了 fs、child_process)无法跑
- 用 Web Standard API(fetch、URL、Crypto)
- WASM 可补足部分需求

**CPU 限制**

- 50ms / 30s 根据计划
- 需大计算量任务用 Lambda 或专用机

**冷启动 vs 持久化**

- Isolate 短生命周期,不能假设全局变量持久(except for caching layer)

## 定价

**免费**:100K 请求/天,10ms CPU/请求
**付费 $5/月**:10M 请求/月,30M 后 $0.30/百万,50ms CPU 起

R2 0 出站费用是 S3 的颠覆性优势(S3 出站 $0.09/GB,大流量场景成本差距巨大)。

## 商业意义

Cloudflare 用 Workers 与全球 CDN 网络同时做"基础设施 + Serverless"双轮驱动,挑战 AWS 在全球分布场景的优势。2024 年 Workers AI、Vectorize 推动其进入 AI 推理市场。

## 学习曲线

- 入门:JavaScript fetch event 即可写
- 中级:理解 isolate 模型、Durable Objects、R2 配合
- 高级:WASM、Workers AI、复杂系统设计

## 参考源

- raw/计算机/
- 相关:[[现代云原生架构]]、[[Vercel]]
