---
title: Next.js
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/框架/React/Next.js/]
created: 2026-05-05
updated: 2026-05-05
summary: Next.js 是 Vercel 维护的 React 元框架,提供文件路由、SSR/SSG/ISR、API Routes、Image/Font 优化,App Router 与 React Server Components 重塑 React 全栈范式。
---

# Next.js

## 定义

**Next.js** 是 Vercel(原 Zeit)2016 年开源、维护至今的 [[React]] 元框架(meta-framework)。它在 React 之上提供**全栈开发能力**:文件系统路由、SSR/SSG/ISR、API Routes、Image/Font 优化、中间件、边缘运行时。Next.js 已是最广泛使用的 React 生产框架,2022 年 App Router 推出后又成为 React Server Components(RSC)的旗舰实现。

## 核心要点

### 1. 文件系统路由

Pages Router(传统):
```
pages/
  index.tsx            → /
  blog/[slug].tsx      → /blog/:slug
  api/users.ts         → /api/users
```

App Router(13+,RSC 时代):
```
app/
  page.tsx             → /
  blog/[slug]/page.tsx → /blog/:slug
  layout.tsx           → 嵌套布局
```

### 2. 渲染模式

| 模式 | 何时渲染 | 适用 |
|---|---|---|
| SSR(Server-Side Rendering) | 每次请求 | 实时数据、个性化 |
| SSG(Static Site Generation) | 构建期 | 博客、文档 |
| ISR(Incremental Static Regeneration) | 构建期 + 后台增量 | 海量页面、定期刷新 |
| CSR(Client-Side Rendering) | 浏览器 | 后台仪表盘 |
| RSC(React Server Components) | 服务器(每次或缓存) | 默认零客户端 JS |

App Router 把 SSR/SSG/ISR 合并为统一 fetch + cache 模型。

### 3. React Server Components

```tsx
// app/page.tsx — 默认 Server Component
export default async function Home() {
  const data = await fetch('https://api...', { cache: 'force-cache' });
  return <div>{(await data.json()).title}</div>;
}
```

- 默认在服务器执行,零 JS 到客户端
- 直接 await 数据源(数据库、API)
- 用 `'use client'` 切到 Client Component(交互、useState、浏览器 API)

### 4. API Routes / Route Handlers

```ts
// app/api/users/route.ts
export async function GET() {
  return Response.json({ users: [...] });
}
```

无需独立后端框架即可发布 [[RESTful API]]。

### 5. 图像与字体优化

`<Image>` 组件:自动 WebP/AVIF、按视口生成多尺寸、懒加载、占位符。

`next/font`:本地化下载 Google Font,无 FOUT,无第三方请求。

### 6. 中间件(Middleware)

```ts
// middleware.ts
export function middleware(req) {
  if (!req.cookies.get('token')) return NextResponse.redirect('/login');
}
```

跑在 Edge Runtime,毫秒级延迟。鉴权、A/B、地理重定向首选。

### 7. 部署目标

- Vercel(原生支持,零配置)
- Cloudflare Pages、AWS、Azure
- 自托管:Node 服务器或 Docker

### 8. Turbopack

Webpack 作者新作,Rust 编写,目标取代 Next.js 内置的 Webpack。开发模式速度提升数倍,2024 进入 stable。

### 9. 与其他元框架对比

| 框架 | UI 库 | 路线 |
|---|---|---|
| Next.js | [[React]] | 全栈 + RSC |
| Remix | React | Web 标准优先 |
| Nuxt | [[Vue]] | 全栈 |
| SvelteKit | [[Svelte]] | 全栈 |
| Astro | 多框架 | 内容站、岛屿架构 |

## 关系

- 基于:[[React]] + [[React Fiber]] + RSC
- 对比:Remix、Nuxt、SvelteKit
- 渲染:[[SSR]]、[[SSG]]、[[ISR]]
- 构建:Webpack → Turbopack
- 部署:[[Edge计算]] Runtime
- 类型:[[TypeScript类型系统]] 一等

## 参考源

- raw/计算机/开发学习/框架/React/Next.js/Next.js.md
- raw/计算机/开发学习/新技术/2025 网站开发的核心趋势.md
