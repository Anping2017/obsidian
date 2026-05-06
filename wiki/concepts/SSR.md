---
title: SSR 服务端渲染
type: concept
tags: [cs, web, frontend, performance, mature]
sources: [raw/计算机/开发学习/语言/HTML/04-知识拓展层/技术生态集成/04-6 服务器端渲染SSR.md]
created: 2026-05-05
updated: 2026-05-05
summary: SSR 把组件树在服务器渲染为完整 HTML 后发给浏览器,解决 SPA 首屏慢、SEO 难、社交分享卡片缺失三大痛点,需配合水合(hydration)激活交互。
---

# SSR 服务端渲染

## 定义

**SSR(Server-Side Rendering)** 是指**网页 HTML 在服务器端组装完成**后再发给浏览器,而非由 JS 在浏览器内动态构建。它是相对 CSR(Client-Side Rendering)的概念。React/Vue 等单页应用(SPA)早期纯 CSR,首屏白屏严重;SSR 通过把组件树在服务器执行一次输出 HTML,实现"首字节即可见"。

## 核心要点

### 1. SSR 流程

```
浏览器请求 /
↓
Node 服务器跑 React/Vue 组件 → 生成 HTML 字符串
↓
返回:HTML(含初始数据序列化)+ JS bundle
↓
浏览器立即显示 HTML(可见内容)
↓
JS 加载完成 → 水合(hydration):绑定事件、接管交互
```

### 2. 为什么需要 SSR?

#### 性能(LCP)

CSR 首屏:HTML(空) → JS → 渲染 → 数据请求 → 渲染。SSR 直接发完整 HTML。

#### SEO

爬虫(尤其非 Google 引擎)不擅长执行 JS。SSR 输出的内容直接被索引。

#### 社交分享

Facebook/微信/Twitter 抓取 OG meta 标签,只看 HTML 不跑 JS。SSR 让 og:image / og:title 立即可见。

#### 弱设备

低端手机 JS 解析慢,SSR 减少客户端工作量。

### 3. 水合(Hydration)

```jsx
// 服务器
const html = renderToString(<App data={data} />);

// 浏览器
hydrateRoot(document.getElementById('root'), <App data={initialData} />);
```

React 用相同组件 + 服务器序列化的初始数据,**复用现有 DOM** 而非重建,只附加事件监听。失败(unhydration mismatch)时回退到 CSR。

### 4. SSR 的代价

- 服务器 CPU 成本(每请求都要跑组件)
- 复杂度上升(同构代码,window/document 不可用)
- 缓存设计困难(个性化页 vs 通用页)
- TTFB(首字节时间)增加

### 5. 解决方案演进

| 方案 | 思路 |
|---|---|
| 纯 SSR | 每请求渲染 |
| [[SSG]] | 构建期生成,完全静态 |
| [[ISR]] | SSG + 后台增量再生 |
| Streaming SSR | React 18 / Next.js,流式输出,边渲染边发 |
| RSC(React Server Components) | 部分组件永远只在服务器,客户端零 JS |
| 岛屿架构(Astro) | 默认静态,只对交互组件水合 |

### 6. 主流元框架

- **Next.js**(React)
- **Nuxt**(Vue)
- **SvelteKit**
- **SolidStart**
- **Remix**
- **Astro**(多框架,岛屿)

### 7. Hydration 瓶颈与新趋势

- **Selective Hydration**(React 18):优先水合用户交互区域
- **Resumability**(Qwik):序列化执行状态,完全跳过水合
- **岛屿架构**:大部分页静态,仅交互"岛"水合
- **RSC**:服务端组件不需要水合

## 关系

- 对比:CSR(纯客户端)、[[SSG]]、[[ISR]]
- 实现:[[Next.js]]、Nuxt、SvelteKit
- 框架:[[React]] renderToString/renderToStream、[[Vue]] @vue/server-renderer
- 配合:[[Edge计算]] 在 CDN 边缘 SSR
- 度量:[[Core Web Vitals]] 中 LCP / TTFB

## 参考源

- raw/计算机/开发学习/语言/HTML/04-知识拓展层/技术生态集成/04-6 服务器端渲染SSR.md
- raw/计算机/开发学习/新技术/2025 网站开发的核心趋势.md
