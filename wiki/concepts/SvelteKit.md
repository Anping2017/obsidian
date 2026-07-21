---
title: SvelteKit
type: concept
tags: [cs, web, frontend, stub]
sources: []
created: 2026-05-11
updated: 2026-05-11
summary: SvelteKit 是基于 Svelte 的全栈元框架,以编译时优化、极简 API、文件系统路由为特色,是继 Next.js 之后的现代 Web 框架代表之一。
---

# SvelteKit

## 定义

**SvelteKit** 是 [[Svelte]] 的官方全栈框架,提供路由、SSR/SSG/边缘渲染、数据加载、表单处理、API endpoints 等能力。核心哲学是"**编译时做尽可能多的事**",相比 [[React]] / [[Vue]] 系框架显著减少运行时开销。1.0 于 2022 年发布,由 Rich Harris(Svelte 作者、Vercel 员工)主导。

## 核心要点

- **文件系统路由**:目录结构直接对应 URL,与 [[Next.js]] 一致但更简洁
- **数据加载**:`+page.server.ts` / `+page.ts` 显式区分服务端/通用数据
- **表单进阶**:progressive enhancement — 不写 JS 也能提交
- **多种适配器**:Node、Cloudflare、Vercel、Netlify、静态、任意 serverless
- **编译产物极小**:相同页面通常比 React 应用小 30-50%
- **上手曲线**:约定丰富但抽象少,一天可入门
- **生态**:比 Next.js 小,但社区活跃(SvelteHack 等)

## 和其他概念的关系

- 与 [[Next.js]]、[[Nuxt]]、[[Astro]]、[[Remix]] 同属现代 Web **元框架**
- 底层基于 [[Svelte]] 的编译时响应式模型
- 支持 [[SSR]]、[[SSG]]、[[ISR]]、[[Edge计算]] 多种渲染
- 部署常用 [[Vercel 与 Netlify]] 或 [[Cloudflare Workers]]

## 参考源

- 综合 SvelteKit 官方文档与社区讨论
