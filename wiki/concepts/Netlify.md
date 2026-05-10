---
title: Netlify
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Netlify 是 2014 年由 Mathias Biilmann 创立的 JAMstack 部署平台,以 Git 集成、CDN 静态资源、Functions 一体化定义了现代前端 PaaS 雏形,虽被 Vercel 在框架领域超越,但仍是中等规模 SSG/JAMstack 项目首选之一。
---

# Netlify

## 定义

**Netlify** 是 Mathias Biilmann 与 Christian Bach 在 2014 年创立的前端部署平台。它早于 [[Vercel]] 把"Git 推送即部署 + 全球 CDN + Serverless 函数"模式商业化,定义了**JAMstack(JavaScript + APIs + Markup)**这一术语,塑造了一代静态网站生成器(SSG)生态。

虽然在 [[Next.js]] 等"全栈 React 框架"领域被 Vercel 超越,Netlify 仍是 Gatsby、Hugo、Eleventy、Astro 等纯静态 / 内容站点的主流选择,以及中小企业站、博客、文档站的首选。

## 核心能力

**1. Git 推送即部署**

- 连 GitHub / GitLab / Bitbucket 仓库
- 每次 push 触发构建
- main 分支 → Production
- Branch / PR → Deploy Preview(自动 URL)

与 Vercel 几乎一模一样,Netlify 是这一模式的开创者。

**2. 全球 CDN**

- 静态资产边缘节点缓存
- 自动 HTTPS(Let's Encrypt)
- 智能路由

**3. Build & Deploy**

- Build Plugins:在构建过程中插入逻辑(检查、优化、通知)
- Build Cache:依赖、产物加速
- Build Image:Ubuntu 容器,可装 Node、Python 等
- Build Hooks:外部触发(如 CMS 内容更新)

**4. Functions(Serverless)**

- /netlify/functions/ 目录下的文件自动成 API
- 基于 AWS Lambda(早期)和 Netlify Edge Functions(基于 Deno)
- Node.js、Go、Rust 支持

**5. Edge Functions**

基于 Deno 在边缘节点执行,毫秒级延迟。

**6. Forms**

无后端表单接收:HTML form 加 netlify 属性即工作,Spam 过滤、邮件通知、Webhook。这是 Netlify 早期独特卖点。

**7. Identity**

用户认证 SDK,集成 GoTrue(Netlify 开源 Auth 服务)。

**8. Large Media / Asset Optimization**

图片自动优化(WebP / AVIF)、Git LFS 集成。

## 与 Vercel 对比

| 维度 | Netlify | [[Vercel]] |
|---|---|---|
| 创立 | 2014 | 2015 |
| 核心市场 | JAMstack / SSG | Next.js 全栈 |
| Functions | AWS Lambda + Deno Edge | Node + Edge Runtime |
| 特色 | Forms、Identity | Image Opt、ISR |
| 框架优化 | 中性,通用 | Next.js 极强 |
| 中国访问 | 慢 | 慢 |
| 价格 | 类似 | 类似 |

**经验法则**

- Next.js 项目 → Vercel
- Gatsby / Hugo / Astro / Eleventy → Netlify(略优)
- Vue / Nuxt → 都行
- 简单内容站、博客 → Netlify(Forms、Identity 顺手)

## JAMstack 的兴起

**JAMstack** 由 Netlify 在 2015 年推广:
- **JavaScript**:浏览器/构建期 JS
- **APIs**:Headless CMS、第三方服务
- **Markup**:预渲染静态 HTML

特点:
- 静态托管,极速
- 安全(无服务端运行)
- 易扩展(CDN)
- DX 好(Git Workflow)

JAMstack 在 2018-2022 是热门概念,后被"Next.js / Remix 全栈"和"Edge 运行"分散关注度。Netlify 仍是 JAMstack 旗手。

## Netlify CMS / Decap CMS

Netlify 开源的 Git-based CMS:
- 内容存仓库(Markdown)
- 编辑器界面 Web UI
- 与静态站生成器(Hugo、Gatsby、Eleventy)契合

2022 年品牌改为 **Decap CMS**(独立运营),Netlify 不再主导。

## 商业模式

**免费层(Starter)**

- 100 GB 带宽
- 300 build 分钟
- 125k Functions 调用
- Identity 1000 用户
- 适合个人 / 小项目

**Pro($19/用户/月)**

- 1 TB 带宽
- 25k build 分钟
- 2M Functions 调用
- 团队协作
- 商业可用

**Business / Enterprise**

- 高级安全(SSO、SAML、HIPAA)
- 优先支持
- 自定义合规

## 部署示例

```bash
# 安装 CLI
npm i -g netlify-cli

# 初始化
netlify init

# 关联仓库后,push 即部署
git push origin main

# 或本地直接部署
netlify deploy --prod
```

**netlify.toml 配置**

```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200

[[plugins]]
  package = "@netlify/plugin-lighthouse"
```

## 适用场景

**最适合**

- Static Site Generators(Hugo、Eleventy、Gatsby、Astro)
- 营销/产品官网
- 文档站(Docusaurus、Mkdocs)
- 博客
- JAMstack 中等复杂应用

**不太适合**

- 重后端业务逻辑(Functions 限 26s)
- WebSocket 长连接
- 大量数据库交互(用 Hasura、Supabase 等 BaaS 配合)
- 中国大陆主市场(需 CDN 加速)

## 与 Vercel 的工程文化差异

**Netlify**

- 老牌,建立了 JAMstack 概念
- 开发者友好,文档优秀
- 中性立场,不偏向单一框架
- Forms / Identity 等独特功能

**Vercel**

- Next.js 母公司,深度优化
- AI 时代加注 Edge Runtime、AI SDK
- 估值更高(2024 ~32 亿)
- 推动框架创新(RSC、PPR)

## 与 Cloudflare Pages 对比

| 维度 | Netlify | [[Cloudflare Workers]] / Pages |
|---|---|---|
| Edge 网络 | 中 | 最广 270+ |
| Functions | Lambda + Deno | Workers(V8 Isolate) |
| 价格 | 中 | 慷慨免费 |
| 成熟度 | 高 | 中 |
| DX | 优 | 中(技术性强) |

Cloudflare Pages 因免费层激进、网络最广,在 2023+ 蚕食 Netlify 中长尾用户。

## Netlify 演进

**2014-2018**:JAMstack 教父
**2019-2022**:Functions、Edge 跟进、Identity
**2022-2024**:Composable Web、与 Vercel 差异化
**2024+**:Strapi、CMS 整合,聚焦 Content-Heavy 场景

## 局限

- 中国大陆访问慢(无大陆节点)
- 与 Next.js 整合不如 Vercel 深
- Forms / Identity 计费分开
- 大型应用并发限制
- 不适合需要持久化连接

## 和其他概念的关系

Netlify 与 [[Vercel]]、[[Cloudflare Workers]] 共同构成现代前端 PaaS 三巨头,共享"Git 推送即部署 + 全球 CDN + Functions"商业模式。它推广的 JAMstack 概念深入影响了 [[SSG]]、[[Headless CMS]]、[[Edge Functions]] 等现代 Web 架构。

它与 [[React]]、[[Vue]]、Astro 等前端框架协同部署,是 [[CI_CD流水线]] 在前端领域的简化形态——不需要专门 Jenkins / GitLab CI,平台自动接管。

它的 Functions / Edge Functions 让 [[Serverless]] 普及到前端开发者,降低了"想加点后端逻辑"的门槛,与 [[BFF]] / [[微服务]] 形成轻量补充。

## 参考源

- raw/计算机/
- 相关:[[Vercel]]、[[Cloudflare Workers]]、[[JAMstack]]
