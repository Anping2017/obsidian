---
title: SolidJS
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/框架/]
created: 2026-05-05
updated: 2026-05-05
summary: SolidJS 是 Ryan Carniato 创建的细粒度响应式框架,JSX 语法接近 React 但底层无虚拟 DOM,通过 signal 在编译期生成精确更新代码,性能基准长期领先。
---

# SolidJS

## 定义

**SolidJS** 是 Ryan Carniato 2018 起开发、2021 年 1.0 的 JavaScript 框架。语法上看起来像 [[React]](JSX、Hooks 风格 API),但底层完全不同:**没有虚拟 DOM、没有重新渲染整个组件**,通过细粒度响应式 signal 在编译期生成针对每个绑定点的精确更新代码。性能基准(JS Framework Benchmark)长期前列。

## 核心要点

### 1. Signal 响应式原语

```jsx
import { createSignal, createEffect } from 'solid-js';

function Counter() {
  const [count, setCount] = createSignal(0);
  createEffect(() => console.log(count()));
  return <button onClick={() => setCount(count() + 1)}>{count()}</button>;
}
```

注意 `count()` 调用形式:signal 是 getter 函数,读取建立依赖。

### 2. 组件只运行一次

```jsx
function App() {
  console.log('only runs ONCE');
  const [c, setC] = createSignal(0);
  return <p>{c()}</p>;
}
```

与 React 每次状态变化重新调用整个函数完全相反。Solid 的"组件"只是一次性 setup,后续更新由 signal 直接驱动 DOM。

### 3. 编译期分析

`<p>{c()}</p>` 被编译为:

```js
const p = createElement('p');
const text = createText();
p.appendChild(text);
effect(() => text.data = c());
return p;
```

每个绑定点都是一个微 effect,signal 变化只跑相关 effect,不跑组件函数。

### 4. 与 React 对比

| 维度 | [[React]] | SolidJS |
|---|---|---|
| 组件运行 | 每次状态变化都跑 | 只跑一次 |
| 状态原语 | useState | createSignal |
| 重新渲染 | 整个组件子树 | 仅依赖此 signal 的 DOM |
| 协调 | [[虚拟DOM]] diff | 无 vDOM |
| Hooks 规则 | 顺序敏感 | 无顺序约束 |

### 5. 共享 React 心智的优势

JSX、context、suspense、lazy、refs 等 API 与 React 几乎同名,React 用户可平滑切换,但带来真实性能提升。

### 6. SolidStart

官方元框架,类似 [[Next.js]],支持 SSR、岛屿、流式渲染。

### 7. 影响

Solid 的 signal 模型反向影响:

- [[Vue]] 3 的 ref 与 Solid 几乎同构
- [[Svelte]] 5 Runes 转向 signal
- Angular 17 引入 signal
- React Forget 编译器朝精确订阅靠拢

Signal 范式正在成为新一代前端共识。

### 8. 适用场景

- 极致性能(交互密集、列表巨大)
- 喜欢 JSX 但厌倦 React 重渲染心智
- 教学:模型清晰,能看到响应式本质

### 9. 不足

- 生态比 React 小
- 库适配有限
- 国内中文资料稀缺

## 关系

- 灵感:Knockout、Vue 响应式、React JSX
- 影响:[[Vue]] 3 ref、Svelte 5 Runes、Angular Signals
- 对比:[[React]]、[[Vue]]、[[Svelte]]
- 路线:与 [[Svelte]] 同属精确更新阵营
- 元框架:SolidStart

## 参考源

- raw/计算机/开发学习/框架/
- raw/计算机/开发学习/新技术/2025 网站开发的核心趋势.md
