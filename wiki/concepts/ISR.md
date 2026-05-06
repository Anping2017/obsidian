---
title: ISR 增量静态再生
type: concept
tags: [cs, web, frontend, performance, mature]
sources: [raw/计算机/开发学习/]
created: 2026-05-05
updated: 2026-05-05
summary: ISR 是 SSG 与 SSR 的折中:首次请求生成静态页并缓存,过期后后台异步再生,既享 CDN 速度又支持内容更新,Next.js 首创并普及。
---

# ISR 增量静态再生

## 定义

**ISR(Incremental Static Regeneration)** 是 [[Next.js]] 9.5(2020)首创的渲染模式,介于 [[SSG]] 与 [[SSR]] 之间。思路:页面**首次访问时按需生成静态 HTML 并缓存**,设定过期时间(revalidate);后续请求直接命中缓存,但若缓存过期,**后台异步重新生成**新版本,旧版本继续服务直到新版本就绪(stale-while-revalidate)。

## 核心要点

### 1. Next.js 中的写法

#### Pages Router(传统)

```js
export async function getStaticProps() {
  const data = await fetch('...').then(r => r.json());
  return {
    props: { data },
    revalidate: 60   // 60 秒后视为过期
  };
}
```

#### App Router

```jsx
export const revalidate = 60;
// 或单次 fetch
fetch(url, { next: { revalidate: 60 } });
```

### 2. 工作流

```
T0  用户访问 /post/1 → 构建 HTML(1.5s) → 缓存 + 返回
T1  10 秒后用户访问 → 缓存命中(20ms)
T2  60 秒后用户访问 → 返回旧版(快) + 后台重建
T3  重建完成 → 缓存替换
T4  下次访问 → 新版
```

### 3. 与三种渲染对比

| 模式 | 首请求 | 后续请求 | 内容新鲜度 |
|---|---|---|---|
| [[SSG]] | 极快 | 极快 | 构建期固定 |
| [[SSR]] | 慢(服务器渲染) | 慢 | 实时 |
| ISR | 中(首次构建) | 极快 | 接近实时(取决 revalidate) |
| CSR | 快(空 HTML) | 快 | 实时(浏览器请求) |

### 4. 按需失效(On-Demand Revalidation)

不必只靠时间过期。CMS 编辑文章后调用 webhook:

```js
// app/api/revalidate/route.ts
import { revalidatePath, revalidateTag } from 'next/cache';

export async function POST(req) {
  revalidatePath('/blog/[slug]', 'page');
  // 或精确:revalidateTag('post-' + id);
}
```

毫秒级让缓存失效,内容秒级上线。

### 5. Tag 机制(App Router)

```js
fetch(url, { next: { tags: ['post-' + id] } });
revalidateTag('post-1');  // 失效所有标了 post-1 的 fetch 缓存
```

精细控制比按 URL 强大得多。

### 6. ISR 适用场景

- **海量内容**:1 万 + 文章,SSG 全量构建太慢,ISR 按需生成
- **半实时**:股票快讯、电商详情(秒级 OK,不需毫秒)
- **数据滞后可接受**:博客、新闻、产品页

不适用:用户个性化首页(每人不同,缓存命中率低)。

### 7. 部署要求

- Vercel:原生
- Netlify:DPR(类似)
- 自托管 Node:可用,但需共享缓存(Redis、文件系统)
- 静态托管(Cloudflare Pages 纯静态模式):不支持 ISR

### 8. 与 stale-while-revalidate

ISR 是 HTTP `Cache-Control: stale-while-revalidate` 的应用层落地。CDN 边缘缓存层亦可实现类似行为。

## 关系

- 折中:[[SSG]] 与 [[SSR]]
- 实现:[[Next.js]] 首创,后被 SvelteKit、Nuxt 借鉴
- 部署:CDN + [[Edge计算]]
- 缓存:`Cache-Control` `stale-while-revalidate` 思想
- 度量:命中率 + 重建延迟

## 参考源

- raw/计算机/开发学习/框架/React/Next.js/Next.js.md
