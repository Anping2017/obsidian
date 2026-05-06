---
title: React
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/框架/React/]
created: 2026-05-05
updated: 2026-05-05
summary: React 是 Facebook 2013 年开源的声明式 UI 库,以组件化、单向数据流、虚拟 DOM 为核心,通过 Hooks 范式与 Fiber 调度奠定现代前端基础设施地位。
---

# React

## 定义

**React** 是 Facebook(现 Meta)2013 年开源的 JavaScript UI 库,Jordan Walke 创建。其设计哲学是"声明式 UI(Declarative)+ 组件化(Component)+ 一次学习随处编写(Learn Once, Write Anywhere)"。React 不是完整框架,而是 UI 层,搭配路由(React Router)、状态管理([[Redux状态管理]])、构建工具([[Webpack]] / [[Vite]])构成完整应用栈。

## 核心要点

### 1. 声明式 UI

```jsx
function App() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

开发者声明"在状态 X 下界面应该长什么样",React 负责差异更新,无需手动 DOM 操作。

### 2. 组件化

UI 拆为可复用、独立、可组合的组件,从原子级(Button)到页面级。组件通过 props 传入、回调传出,自上而下单向数据流。

### 3. 虚拟 DOM([[虚拟DOM]])

JSX 编译为 createElement 调用,生成内存中的 JS 对象树。状态变化时 React 重建 vDOM,与上次比较(diff),只把差异提交到真实 DOM。降低昂贵的 DOM 操作开销。

### 4. JSX

JSX 是 JS 表达式的扩展,允许在 JS 中写类 HTML 语法。Babel 编译为 `React.createElement(...)` 或 React 17+ 的 `_jsx(...)`。

### 5. Hooks(2018-)

```js
useState, useEffect, useContext, useReducer, useMemo, useCallback, useRef, useLayoutEffect, useImperativeHandle...
```

[[React Hooks]] 让函数组件具备状态、副作用、上下文等能力,取代 class 组件的复杂生命周期。是 React 范式从面向对象转向函数式的关键。

### 6. Fiber 架构

[[React Fiber]] 是 React 16 重写的协调器,将渲染任务切片为可中断、可优先级调度的工作单元,实现并发渲染、Suspense、startTransition 等特性。

### 7. 单向数据流

数据从父组件流向子组件;子组件通过事件回调通知父组件。这种约束让数据流可预测、易调试,虽然繁琐但远优于双向绑定的"魔法"。

### 8. 生态

- **路由**:React Router、TanStack Router
- **状态**:[[Redux状态管理]]、Zustand、Jotai、TanStack Query、SWR
- **样式**:Tailwind、[[CSS-in-JS]]、CSS Modules
- **元框架**:[[Next.js]](SSR/SSG/RSC)、Remix、Astro
- **类型**:[[TypeScript类型系统]] 一等公民
- **测试**:Vitest、Testing Library、Playwright

### 9. React Server Components(RSC)

React 18 引入的服务端组件:在服务器渲染、零客户端 JS、可直接 await fetch。配合 Next.js App Router 重塑全栈开发。

### 10. 影响力

React 启发了 [[Vue]]、Preact、SolidJS,推动组件化、虚拟 DOM 成为前端共识。Web 之外延伸到 React Native(移动)、React VR、Ink(CLI)、TV 平台。

## 关系

- 核心:[[虚拟DOM]] + [[React Hooks]] + [[React Fiber]]
- 元框架:[[Next.js]]、Remix、Astro
- 状态:[[Redux状态管理]]、Zustand
- 兄弟:[[Vue]]、[[Svelte]]、[[SolidJS]]
- 生态:[[Webpack]]、[[Vite]] 构建
- 类型:[[TypeScript类型系统]]
- 输入:JSX → Babel → JS

## 参考源

- raw/计算机/开发学习/框架/React/React.md
- raw/计算机/开发学习/框架/React/基础概念/
