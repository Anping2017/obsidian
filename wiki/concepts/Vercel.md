---
title: Vercel
type: concept
tags: [programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Vercel 是前端部署 PaaS 平台,2015 年由 Next.js 创始人 Guillermo Rauch 创立,主打 Git push 即部署、全球 CDN、Serverless 函数,是现代前端开发的"GitHub for hosting"。
---

# Vercel

## 定义

Vercel 是 Guillermo Rauch 在 2015 年创立的前端部署平台(原名 ZEIT,2020 改名)。它把现代前端开发的"开发→预览→部署"流程压缩为"git push 自动部署 + 实时预览 URL",成为 Next.js、React、Vue、Svelte 等前端框架的标准部署平台。

Vercel 本质是:**Git 仓库 + 全球 CDN + Serverless Function + 监控**的一体化 PaaS。它对开发者的吸引力源自零配置、即时预览、与 GitHub/GitLab 无缝集成的开发者体验(DX)。

## 核心特性

**1. Git 集成自动部署**

- 连接 GitHub/GitLab/Bitbucket 仓库
- 每次 push 触发构建
- main 分支 → Production
- 其他分支/PR → Preview Deployment(临时 URL)
- 在 PR 评论中自动贴出预览链接

**2. 全球 CDN(Edge Network)**

- 静态资源全球节点缓存(40+ 城市)
- 中国访问较慢(无大陆节点),需 Cloudflare 等国内加速

**3. Serverless Functions**

- /api 目录下的文件自动成为 API 端点
- 支持 Node.js、Edge Runtime、Python、Go(部分)
- 按调用计费,冷启动毫秒级

**4. Edge Functions**

- 在最近的 CDN 节点执行 JavaScript(基于 V8 isolate,非 Node.js)
- 极低延迟(< 50ms)
- 适合 A/B 测试、个性化、地理定位

**5. ISR(Incremental Static Regeneration)**

- Next.js 独有,首次访问后页面缓存,定时或按需后台重新生成
- 静态网站享动态体验

**6. 环境变量管理**

- 区分 Development / Preview / Production
- 通过 Web UI 或 CLI 配置
- 支持 Encryption 敏感值

**7. 监控与分析**

- Web Vitals(LCP/FID/CLS)实时分析
- Speed Insights、Audience Analytics
- 错误日志、函数调用统计

## 与 Next.js 的关系

Next.js 是 Vercel 主导开发的 React 框架,二者深度协同:
- Next.js 设计时考虑 Vercel 部署
- Vercel 对 Next.js 优化最深
- ISR、Edge Functions、Image Optimization 在 Vercel 上"零配置即用"

但 Next.js 也可在其他平台部署(自建 Docker、Netlify、AWS Amplify、Cloudflare Pages)。Vercel 把 Next.js 作为护城河,2021 年 Next.js 13 起的功能(Server Components、Streaming)首先在 Vercel 流畅可用。

## 与 Netlify、Cloudflare Pages 对比

| 维度 | Vercel | Netlify | Cloudflare Pages |
|---|---|---|---|
| 框架优化 | Next.js 极强 | Gatsby/Hugo | 中性 |
| Edge | 全球 | 全球 | 全球(最广 270+ 城市) |
| Serverless | Node + Edge | Functions | Workers |
| 价格 | 中 | 中 | 较低(慷慨免费层) |
| 学习曲线 | 低 | 低 | 中(Workers 概念) |

## 定价

**Hobby(免费)**

- 100 GB 带宽 / 月
- 100 deployments / 天
- 6,000 build 分钟
- 12 Serverless 函数,10s 超时
- 无商业用途

**Pro($20/用户/月)**

- 1 TB 带宽
- 6,000 build 分钟
- 并发构建
- 团队协作
- 商业可用

**Enterprise**

- 自定义,SLA、合规、全球加速

## 商业模式与争议

Vercel 估值 2024 年 32 亿美元,主要收入来自 Pro/Enterprise 订阅 + Bandwidth Overage。

**争议点**

- Pricing 不可预测:Bandwidth/Serverless 调用量大可能账单飙升
- 开源 Next.js 与商业 Vercel 边界:某些 Next.js 功能(ISR、Image Optimization)在自部署 Node 服务器上不完美
- Edge Runtime 锁定:迁出 Vercel 时部分代码需重写

## 部署流程示例

```bash
# 安装 CLI
npm i -g vercel

# 在项目目录
vercel

# 第一次会引导:
# - 关联仓库
# - 选择构建命令 (npm run build)
# - 选择输出目录 (.next 或 dist)

# 之后:
git push origin main      # 自动部署到生产
git push origin feature   # 自动部署到预览 URL
```

## 适用场景

**最适合**

- Next.js 应用
- React/Vue/Svelte 静态站
- JAMstack(Markdown blog、Doc 站)
- B2B SaaS 主页 + 简单 API
- 创业 MVP

**不太适合**

- 大量后端业务逻辑(应用 Express + AWS/GCP)
- WebSocket 长连接(Edge 不直接支持)
- 文件存储(需配合 S3 / R2)
- 中国大陆主要市场(需国内 CDN)

## 局限

- 大陆访问需要 Cloudflare 或自建 CDN 中转
- Bandwidth 超额账单不可控
- 数据库需第三方(Vercel Postgres 是托管 Neon)
- Vendor Lock-in(Edge Runtime 与 Vercel 紧耦合)
- 长任务超时(Pro 60s,Edge 30s)

## 参考源

- raw/计算机/
- 相关:[[React]]、[[现代云原生架构]]
