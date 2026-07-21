---
title: Astro
type: concept
tags: [cs, programming, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: Astro 是面向内容驱动网站的现代前端框架,以「群岛架构」和默认零 JS 著称,在 SSG/SSR 中通过按需注水实现极致首屏性能。
---

# Astro

## 定义

**Astro** 是 2021 年由 Snowpack 团队(Fred K. Schott 等)发布的**面向内容驱动网站的前端框架**,主打"**默认零 JavaScript**"和"**群岛架构(Islands Architecture)**"两大理念。它的设计目标不是替代 [[React]] / [[Vue]] / [[Svelte]],而是给"内容网站"——博客、文档、营销页、电商展示页——提供比传统 SPA 更轻、比纯 SSG 更灵活的方案。

核心主张:**绝大多数网站不需要在浏览器里跑大量 JS**;静态 HTML + 必要处的交互组件,就足够提供现代体验。

## 核心要点

### 群岛架构(Islands Architecture)

Astro 把页面看成一片"静态海洋",其中只有少数交互组件是"小岛"——这些岛单独打包、按需加载、互不影响。

- 整页 HTML 在构建/请求时渲染,默认不带 JS
- 标注 `client:load` / `client:idle` / `client:visible` / `client:media` 的组件才注水
- 每个岛独立运行,不存在 SPA 那种全局 hydration 开销

```astro
<Layout>
  <Header />                              <!-- 纯 HTML -->
  <SearchBox client:idle />               <!-- 空闲后注水 -->
  <ProductGrid client:visible />          <!-- 滚到视口才注水 -->
  <Footer />                              <!-- 纯 HTML -->
</Layout>
```

### 多框架互操作

同一页面可混用 React、Vue、Svelte、SolidJS、Preact、Lit 组件,Astro 负责把它们各自打包成岛。这让团队迁移、组件复用变得现实。

### 渲染模式

| 模式 | 用途 |
|---|---|
| **静态(SSG)** | 默认,构建时生成 HTML,部署到 CDN |
| **SSR(按需服务端渲染)** | 适合个性化、用户内容,见 [[SSR]] |
| **混合(Hybrid)** | 大部分页面静态,少数动态,见 [[SSG]] |
| **按需预渲染** | 增量静态再生,接近 [[ISR]] |

### Content Collections

Astro 2.0 引入的**类型安全内容层**:Markdown / MDX / JSON 等内容用 Zod schema 声明,frontmatter 字段在 TS 中自动有类型。文档站、博客最直接受益。

### 性能特征

- **Lighthouse 默认满分** 是 Astro 营销口号但确有事实依据:零 JS 起步、CSS scoped、自动图片优化(`<Image>` 组件)
- 首字节小、TTI 低,**Core Web Vitals** 友好,见 [[Core Web Vitals]]
- 对 SEO 极友好:服务端完整 HTML,爬虫零成本理解,见 [[JavaScript SEO]]

## 典型应用

- **官方文档站**:Astro 自己的文档、Cloudflare Docs(基于 Astro 的 Starlight 文档框架)
- **公司营销站**:大量 SaaS 产品落地页
- **博客 / Newsletter**:个人技术博客主流选项之一
- **电商商品展示**:配合 SSR / 边缘渲染做商品页
- **代表用户**:The Guardian、Firefox、Cloudflare Docs、NordVPN、Trivago

部署平台首选 [[Vercel]]、[[Netlify]]、[[Cloudflare Pages]],也可在 [[Docker容器]] 中跑 Node adapter。

## 局限与陷阱

- **不适合应用级交互**:重交互(白板、画布、IDE 类应用)用 [[Next.js]] / [[Nuxt]] 更顺
- **多框架成本**:同页混用 React + Vue 看似酷,但 bundle 体积、心智成本都增加
- **服务端渲染较新**:SSR adapter 生态仍在追 Next.js / Nuxt
- **岛之间状态共享**:跨岛通信需自定义事件或第三方状态库,不天然便捷
- **构建时间**:大型内容站(数万页)构建可能数十分钟,需要增量构建策略

## 与其他概念的关系

- 与 [[Next.js]]、[[Nuxt]]、[[SvelteKit]] 同属现代元框架,但定位偏内容而非应用
- 是 [[Jamstack]] 思想的最新代表,与 [[SSG]] / [[SSR]] / [[ISR]] 三种渲染模式都兼容
- 群岛架构对照 [[虚拟DOM]] 整页注水,体现 [[局部最优]] 思路
- 主流部署目标:[[Vercel]]、[[Netlify]]、[[Cloudflare Pages]]
- 内容驱动定位强化了对 [[Core Web Vitals]]、[[JavaScript SEO]] 的优势
- 与 [[React]] / [[Vue]] / [[Svelte]] / [[SolidJS]] 是合作而非竞争关系

## 参考源

- Astro 官方文档 https://docs.astro.build/
- Jason Miller, *Islands Architecture* (jasonformat.com, 2019)
- Fred K. Schott 关于 Astro 设计的多次演讲
