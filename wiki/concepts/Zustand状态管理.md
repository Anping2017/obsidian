---
title: Zustand 状态管理
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/框架/React/]
created: 2026-05-05
updated: 2026-05-05
summary: Zustand 是 React Three Fiber 作者 Poimandres 团队推出的极简状态库,基于 hook + 闭包,无 Provider/无 reducer,API 表面积极小,成为 Redux 替代主力。
---

# Zustand 状态管理

## 定义

**Zustand**(德语"状态")是 Poimandres 团队(react-three-fiber、react-spring 同作者)2019 年开源的 React 状态管理库。核心理念是**极简**:无 Provider 包裹、无 reducer 仪式、无 immutable 强约束。一个 hook 即得到 store,既能读也能写。当前 Zustand 已是 NPM 周下载量超越 Redux 的主流方案之一。

## 核心要点

### 1. 基本用法

```js
import { create } from 'zustand';

const useStore = create((set) => ({
  count: 0,
  inc: () => set((s) => ({ count: s.count + 1 })),
  reset: () => set({ count: 0 })
}));

function Counter() {
  const { count, inc } = useStore();
  return <button onClick={inc}>{count}</button>;
}
```

8 行写完 Redux 需 50 行的功能。

### 2. 选择器订阅

```js
const count = useStore((s) => s.count); // 仅 count 变才重渲染
```

避免无关状态变化触发重渲。`shallow` 比较器用于多字段:

```js
const { a, b } = useStore((s) => ({ a: s.a, b: s.b }), shallow);
```

### 3. 在组件外访问

```js
useStore.getState().count;
useStore.setState({ count: 0 });
useStore.subscribe((s) => console.log(s.count));
```

非常适合在事件、定时器、非 React 代码中读写。

### 4. 中间件

```js
import { persist, devtools, immer } from 'zustand/middleware';

const useStore = create(
  persist(
    devtools(
      immer((set) => ({ ... }))
    ),
    { name: 'app-storage' }
  )
);
```

- **persist**:localStorage / IndexedDB 持久化
- **devtools**:接入 Redux DevTools(时间旅行)
- **immer**:可像可变代码一样写更新

### 5. 与 Redux 对比

| 维度 | [[Redux状态管理]] + RTK | Zustand |
|---|---|---|
| 学习曲线 | 中 | 极低 |
| 样板代码 | 中(RTK 已大幅减少) | 极少 |
| Provider | 需要 | 不需要 |
| 体积 | ~13KB | ~1KB |
| DevTools | 一等公民 | 中间件支持 |
| 大型项目结构 | 强约束 | 自由 |
| 服务器状态 | RTK Query | TanStack Query 配合 |

### 6. 与 Context 对比

Context 性能差(任意更新触发整树):Zustand 用外部 store + 选择器,不靠 Context。

### 7. Slices 模式

```js
const createBearSlice = (set) => ({
  bears: 0,
  addBear: () => set((s) => ({ bears: s.bears + 1 }))
});
const createFishSlice = (set) => ({ ... });
const useStore = create((...a) => ({
  ...createBearSlice(...a),
  ...createFishSlice(...a)
}));
```

模块化拆分,适合中大型应用。

### 8. 适用与不适用

**适用**:中小型项目、原型快速搭建、UI 状态、3D 应用(react-three-fiber)。

**不适用**:超大型团队需要严格规范、复杂副作用编排(用 saga/observable 时)。

## 关系

- 替代:[[Redux状态管理]] 在中小项目
- 应用:[[React]] 生态
- 配合:TanStack Query 处理服务器状态
- 兄弟:Jotai(原子化)、Valtio(代理)
- 范式:基于 [[闭包]] + hook

## 参考源

- raw/计算机/开发学习/框架/React/
- raw/计算机/开发学习/新技术/2025 网站开发的核心趋势.md
