---
title: Redux 状态管理
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/框架/React/]
created: 2026-05-05
updated: 2026-05-05
summary: Redux 是 Dan Abramov 2015 年受 Flux 与 Elm 启发创建的可预测状态容器,以单一 store/纯函数 reducer/不可变更新为核心三原则,Redux Toolkit 是当代标准用法。
---

# Redux 状态管理

## 定义

**Redux** 是 Dan Abramov 与 Andrew Clark 2015 年开发的 JavaScript 应用状态管理库,获得当年 React 社区压倒性采纳。设计深受 Facebook 的 **Flux 单向数据流**与 Elm 架构启发。Redux 强调**可预测性**:相同状态 + 相同 action,永远得到相同结果。

## 核心要点

### 1. 三大原则

1. **单一数据源**:整个应用状态存在一个 store 树中
2. **状态只读**:唯一改变方式是 dispatch 一个 action(描述发生了什么的对象)
3. **纯函数 reducer**:`(state, action) => newState`,不可变更新

### 2. 数据流

```
View → dispatch(action) → reducer → new state → View 订阅更新
```

```js
// action
const inc = { type: 'counter/inc' };

// reducer
function counter(state = 0, action) {
  switch (action.type) {
    case 'counter/inc': return state + 1;
    default: return state;
  }
}

// store
const store = createStore(counter);
store.dispatch(inc);
```

### 3. 中间件

`applyMiddleware(thunk, logger, saga)` 在 dispatch 与 reducer 之间插入逻辑:

- **redux-thunk**:dispatch 函数实现异步
- **redux-saga**:Generator 控制副作用
- **redux-observable**:RxJS Epic
- **logger**:开发期日志

### 4. Redux Toolkit(RTK)

官方推荐的当代用法,2019 起标准:

```js
import { createSlice, configureStore } from '@reduxjs/toolkit';

const counter = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    inc: (state) => { state.value++; }  // 内部用 Immer,可"直接修改"
  }
});

const store = configureStore({ reducer: { counter: counter.reducer } });
```

RTK 解决了 Redux 历史样板代码冗长的痛点,几乎抹平与轻量库差距。

### 5. RTK Query

数据获取与缓存层,类比 React Query:

```js
const api = createApi({
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  endpoints: (b) => ({
    getUser: b.query({ query: (id) => `users/${id}` })
  })
});
```

自动生成 hooks、缓存、失效、轮询、乐观更新。

### 6. 与轻量替代对比

| 库 | 哲学 | 学习曲线 | 适用 |
|---|---|---|---|
| Redux + RTK | 不可变 + reducer + 中间件 | 中 | 大型应用、调试要求高 |
| [[Zustand]] | 类 React 但不绑定 React | 低 | 中小型 |
| Jotai | 原子化(atom) | 低 | 细粒度订阅 |
| MobX | 响应式 OO | 中 | 类 Vue 心智 |
| Recoil | Facebook 实验,已停 | - | - |
| TanStack Query | 服务器状态 | 中 | 与 Redux 互补 |

### 7. DevTools

Redux DevTools 浏览器扩展:时间旅行调试、action 日志、状态 diff。可以"穿越"重放 action,Bug 复现的杀手锏。

### 8. 何时不需要 Redux?

- 应用状态主要是服务器数据(用 [[TanStack Query]]/SWR)
- 状态在少数组件之间共享(用 Context)
- 中小型应用(用 Zustand)

Dan Abramov 本人说:"You might not need Redux."

## 关系

- 应用:[[React]] 主流状态管理
- 范式:基于 [[函数式编程]] 纯函数 + [[闭包]]
- 对比:[[Zustand状态管理]]、Jotai、MobX
- 启发:[[Pinia状态管理]] (Vue) 借鉴了类似思路
- 工具:Redux DevTools

## 参考源

- raw/计算机/开发学习/框架/React/
