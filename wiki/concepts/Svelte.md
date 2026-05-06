---
title: Svelte
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/框架/]
created: 2026-05-05
updated: 2026-05-05
summary: Svelte 是 Rich Harris 2016 年创建的编译时前端框架,把组件编译为高效命令式 JS,无虚拟 DOM、无运行时,5.0 引入 Runes 响应式原语。
---

# Svelte

## 定义

**Svelte** 是 Rich Harris(纽约时报、现 Vercel)2016 年创建的前端框架。最大特色是**编译时框架(Compile-time Framework)**:Svelte 在构建期把 `.svelte` 组件编译为直接操作 DOM 的命令式 JS,**没有运行时虚拟 DOM、没有协调器**。运行包体积小、性能优。

## 核心要点

### 1. 三段单文件

```svelte
<script>
  let count = 0;
  $: doubled = count * 2;
</script>

<button on:click={() => count++}>{count} ({doubled})</button>

<style>
  button { color: red; }
</style>
```

更接近原生 HTML/JS,无 JSX、无指令前缀。

### 2. 响应式($-标签,Svelte 3-4)

```js
let count = 0;
$: doubled = count * 2;       // 响应式语句
$: if (count > 10) alert();   // 副作用
```

`$:` 是 JavaScript 标签语法被借用,编译器据此生成依赖追踪。Svelte 5 改为 Runes(`$state`/`$derived`/`$effect`)更明确。

### 3. 编译时差异

```svelte
<p>{name}</p>
<!-- 编译后 -->
const p = document.createElement('p');
const t = document.createTextNode(name);
p.appendChild(t);
// 状态变化时只更新 t.data
```

直接 DOM 操作,无 [[虚拟DOM]] diff 开销。

### 4. 与 React/Vue 对比

| 维度 | [[React]] | [[Vue]] | Svelte |
|---|---|---|---|
| 协调 | 运行时 vDOM diff | 模板编译 + vDOM | 纯编译,无 vDOM |
| 包体积 | 中 | 中 | 极小(仅业务代码) |
| 学习曲线 | 中 | 低 | 极低 |
| 性能 | 优 | 优 | 优(冷启动尤优) |
| 生态 | 极大 | 大 | 中等 |

### 5. SvelteKit

官方元框架(类比 [[Next.js]] / Nuxt):文件路由、SSR、SSG、表单 actions、API 端点、流式响应。Vercel 原生支持。

### 6. Svelte 5 Runes

```js
let count = $state(0);
let doubled = $derived(count * 2);
$effect(() => console.log(count));
```

Runes 是显式的响应式原语,解决了 `$:` 在条件/嵌套时的歧义,让大型项目更可维护。

### 7. 优势

- 包体积:Hello World ~3KB(对比 React ~40KB)
- 性能基准长期领先
- 学习成本最低
- 写代码量最少
- CSS scoped 默认

### 8. 劣势

- 生态比 [[React]] 小一两个量级
- 工程师就业市场窄
- 大型应用经验沉淀少
- TS 集成虽好但比 Vue/Angular 弱

## 关系

- 对比:[[React]]、[[Vue]]、[[SolidJS]]
- 路线:编译路线代表,与 [[虚拟DOM]] 路线对立
- 元框架:SvelteKit 类比 [[Next.js]]
- 范式:与 [[SolidJS]] 同属"无 vDOM"阵营
- 影响:推动 React/Vue 也加入编译期优化

## 参考源

- raw/计算机/开发学习/框架/
