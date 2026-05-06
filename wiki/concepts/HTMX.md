---
title: HTMX
type: concept
tags: [cs, web, frontend, stub]
sources:
  - raw/计算机/Web前端/
created: 2026-05-05
updated: 2026-05-05
summary: HTMX 是一个轻量 JavaScript 库,通过 HTML 属性扩展实现 AJAX、WebSocket、SSE 等动态交互,主张回归 HATEOAS 与服务端渲染,是对 SPA 复杂度的反思。
---

# HTMX

## 定义

HTMX(读作"H-T-M-X")是一个 **约 14KB 的 JavaScript 库**,通过给 HTML 元素添加形如 `hx-get`、`hx-post`、`hx-swap` 的属性,使得开发者**只用 HTML 就能写出动态、交互式 Web 应用**,无需编写大量前端 JavaScript。

它代表了 Web 开发的一种「反潮流」思潮:

- 回归 [[HATEOAS]](Hypermedia As The Engine Of Application State)
- 拥抱 [[服务端渲染SSR]],由后端生成完整 HTML 片段
- 让前后端分工回到 HTTP/HTML 时代,前端只负责展示

## 核心要点

### 核心属性

| 属性 | 作用 |
|---|---|
| `hx-get` / `hx-post` / `hx-put` / `hx-delete` | 触发对应 HTTP 请求 |
| `hx-trigger` | 何时触发(click、change、every Ns) |
| `hx-target` | 把响应放到哪个 DOM 元素 |
| `hx-swap` | 如何插入(innerHTML、outerHTML、beforeend) |
| `hx-vals` | 附加请求参数 |
| `hx-confirm` | 触发前弹确认框 |
| `hx-boost` | 自动把 a/form 升级为 AJAX |

### 工作流程

1. 用户点击 `<button hx-post="/like" hx-target="#count">点赞</button>`
2. HTMX 拦截事件,发起 AJAX POST `/like`
3. 服务器返回 HTML 片段(不是 JSON)
4. HTMX 把片段插入 `#count` 元素

### 适用场景

- 服务端渲染框架补强:Django、Rails、Laravel、Phoenix
- 中小型动态应用,无需复杂客户端状态
- 后台管理系统、企业内部工具
- 替代部分 jQuery + AJAX 用法

不适用:

- 离线优先应用
- 大量客户端状态的应用(协作编辑、实时游戏)
- 要 SEO 又复杂交互的场景(其实正好可以,但需要后端支持)

## 和其他概念的关系

HTMX 是对 SPA 复杂度的反思,与 [[React]]、[[Vue]] 等 [[前端框架]] 形成另一极。它哲学上接近 [[服务端组件]](React Server Components)、[[Phoenix LiveView]],都是「前后端组件统一,服务器为主」的探索。

HTMX 与 [[Alpine.js]]、[[Stimulus]] 同属轻量增强派,可组合使用。它依赖 [[HTTP协议|HTTP]] 协议本身的语义(动词、状态码、缓存),是 [[RESTful API|REST API]] 设计哲学的极致回归。

[[全栈框架]] 中,HTMX 与 Tailwind CSS、SQLite/Postgres、Go/Python 后端组合,可以用 1/10 的代码量交付与 SPA 体验近似的应用。

## 参考源

- raw/计算机/Web前端/
- htmx.org 官方文档
- Carson Gross《Hypermedia Systems》
