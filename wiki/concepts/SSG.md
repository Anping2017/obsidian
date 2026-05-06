---
title: SSG 静态站点生成
type: concept
tags: [cs, web, frontend, performance, mature]
sources: [raw/计算机/开发学习/语言/HTML/04-知识拓展层/技术生态集成/04-5 静态站点生成器.md]
created: 2026-05-05
updated: 2026-05-05
summary: SSG 在构建期把所有页面预渲染为静态 HTML,部署到 CDN 后无需服务器即可全球毫秒级响应,内容站、文档站、博客的最佳方案。
---

# SSG 静态站点生成

## 定义

**SSG(Static Site Generation)** 是在**构建期**(build time)把所有页面预渲染为静态 HTML 文件,部署到 CDN 后用户访问直接命中边缘节点的方案。每次内容更新需重新构建。SSG 是性能、成本、安全三方面的局部最优:无服务器即无攻击面,CDN 全球分发即毫秒响应,纯文件即低成本。

## 核心要点

### 1. 工作流程

```
内容(Markdown / CMS / 数据库)
    ↓
构建期:框架遍历所有路由 → 调用数据源 → 渲染 HTML
    ↓
输出:dist/index.html, dist/blog/post-1.html ...
    ↓
部署 CDN:Vercel / Netlify / Cloudflare Pages
    ↓
用户访问:CDN 直接返回 HTML
```

### 2. 与 SSR 对比

| 维度 | [[SSR]] | SSG |
|---|---|---|
| 渲染时机 | 每次请求 | 构建期 |
| 服务器 | 必需 | 不需要 |
| TTFB | 中(服务器 CPU) | 极低(CDN) |
| 内容时效 | 实时 | 构建后过期 |
| 成本 | 中-高 | 极低 |
| 适用 | 个性化、动态 | 博客、文档、营销页 |

### 3. 主流 SSG 工具

#### React 生态

- **Next.js**(`generateStaticParams`)
- **Gatsby**(GraphQL 数据层,曾经流行,2023 衰退)
- **Astro**(多框架并存,内容首选)

#### Vue 生态

- **VitePress**(尤雨溪,文档官选)
- **Nuxt**(generate 模式)
- **VuePress**(已被 VitePress 取代)

#### 其他

- **Jekyll**(Ruby,GitHub Pages 默认)
- **Hugo**(Go,极快,博客首选)
- **11ty / Eleventy**(Node,灵活)
- **Docusaurus**(Meta 文档系统)
- **Hexo**(Node,中文社区流行)

### 4. 构建时间问题

页面数过多时,构建时间线性增长。1 万篇博客可能要 30 分钟。解决:

- **增量构建(ISR)**:[[ISR]] 折中
- **DPR(Distributed Persistent Rendering)**:Netlify 提案,部分按需
- **并行构建**:多核加速
- **缓存**:增量缓存数据/HTML

### 5. 数据来源

- Markdown / MDX 文件
- Headless CMS:Contentful、Sanity、Strapi、Notion
- Git-based CMS:Decap CMS(原 Netlify CMS)
- 数据库:在构建期一次查询

### 6. 客户端能力

SSG 不等于无 JS。页面可包含 React/Vue/Svelte 组件,在浏览器水合后获得交互性(JAMstack 思想):

- 表单 → Serverless Function 处理
- 评论 → 第三方(Disqus、Giscus)
- 搜索 → Algolia / Pagefind 静态索引

### 7. 何时不选 SSG?

- 海量页面(数百万 URL)
- 内容秒级更新
- 强个性化(每用户不同)
- 重交互(复杂仪表盘)

→ 选 [[SSR]]、[[ISR]] 或 CSR。

## 关系

- 对比:[[SSR]]、[[ISR]]、CSR
- 框架:[[Next.js]]、Astro、VitePress、Nuxt
- 部署:CDN、[[Edge计算]]
- 哲学:JAMstack(JavaScript + APIs + Markup)
- 性能:[[Core Web Vitals]] LCP 极优

## 参考源

- raw/计算机/开发学习/语言/HTML/04-知识拓展层/技术生态集成/04-5 静态站点生成器.md
