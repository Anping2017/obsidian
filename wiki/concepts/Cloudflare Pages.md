---
title: Cloudflare Pages
type: concept
tags: [cs, frontend, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: Cloudflare Pages 是 Cloudflare 推出的 Git 集成 Jamstack 平台,免费部署、自动 CDN、Workers 集成,是 Vercel/Netlify 的强力替代。
---

# Cloudflare Pages

## 定义

**Cloudflare Pages** 是 Cloudflare 在 2020 年推出的 Jamstack 静态站点 / 全栈应用部署平台,主打 **Git 集成 + 全球边缘网络 + Workers 互操作**。它和 Vercel、Netlify、GitHub Pages 同属"前端 PaaS"类,但天然继承 Cloudflare 庞大 CDN(目前 320+ 城市)与 Workers Runtime 的能力。

## 核心要点

### 工作流

1. 连接 GitHub / GitLab 仓库
2. 选择构建命令(`npm run build`、`hugo`、`astro build`...)与输出目录
3. 推送即触发自动构建,每个 Pull Request 自动生成预览部署(Preview URL)
4. 主分支构建上线后,资源被推送到 Cloudflare 边缘 PoP

### 与 Workers 的关系

Pages 早期是纯静态,2021 年起**整合 Functions**(基于 Workers Runtime,2021 年 11 月 beta、2022 年 GA):
- 在仓库根 `/functions/` 写 TS/JS 函数,自动变成 API 路由
- 支持 Pages 与 Workers 互调,可做 SSR、ISR、API、表单处理
- 与 D1(SQLite)、R2(对象存储)、KV、Durable Objects、Queues 等 Cloudflare 全家桶集成

### 定价模型

- **免费版**:无限请求、500 次/月构建、并发 1 个、无限带宽(不限流量)(其实免费层做完整生产站够用)
- **Pro+**:更多构建并发、更高构建分钟数、企业级 SLA
- 与 Vercel(免费层带宽 100GB,商业用途禁止)对比,Cloudflare Pages 商业免费极其友好

### 性能特性

- 资源自动 HTTP/3 + Brotli + Polish 图像优化
- 缓存策略可在 `_headers` / `_redirects` 文件中声明
- 默认全球 CDN,无需额外配置
- TLS 自动配 (Universal SSL)

### 限制

- 单个文件 ≤ 25 MB
- 部署总大小 ≤ 20,000 文件(免费版;付费版 100,000)
- Functions 冷启动 < 5ms(基于 Workers 的 V8 isolate)
- 函数运行时上限 CPU 30s

## 典型应用

- **个人博客 / 文档站**:Astro/Hugo/Docusaurus + Pages = 零成本
- **企业营销站**:配 D1/KV 做轻量动态(表单、邮件订阅、A/B)
- **JAMstack 商业**:配 Headless CMS + Workers + R2 → 全栈无服务器电商
- **预览环境**:每个 PR 一个独立 URL,内置邀请协作者评审

## 局限与陷阱

- **构建分钟瓶颈**:复杂 monorepo 可能耗光免费额度
- **Workers Runtime 限制**:不能跑全功能 Node.js,某些 npm 包无法运行
- **DNS 强绑定**:域名最好托管 Cloudflare,否则少了 Edge Cache 等关键优化
- **D1 仍是 SQLite**:写并发受限,大写入压力建议外置数据库
- **vs Vercel 框架感**:Next.js 等强框架在 Vercel 更原生,Pages 更框架中立

## 与其他概念的关系

- 范式归属:[[Jamstack]] 的代表性部署平台
- 互补技术:[[Astro]]、[[Headless CMS]]、[[Edge计算]]
- 直接竞品:Vercel、Netlify、GitHub Pages
- 上下游:[[CDN]]、[[Edge计算]]、Cloudflare Workers、[[HTTP3协议]]
- 与 [[微服务]]、[[服务网格|Service Mesh]] 形成"边缘函数 + 中心服务"双层架构

## 参考源

- Cloudflare Pages 官方文档:https://developers.cloudflare.com/pages/
- Cloudflare Workers Runtime:https://workers.cloudflare.com/
