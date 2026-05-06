---
title: React Fiber
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/框架/React/]
created: 2026-05-05
updated: 2026-05-05
summary: Fiber 是 React 16 重写的协调器,把整树递归改为可中断的链表+循环,使渲染任务可切片、可优先级调度,是 Suspense、并发渲染的底层基础。
---

# React Fiber

## 定义

**React Fiber** 是 [[React]] 16(2017)推出的协调引擎,重写了 React 15 的栈式协调器(Stack Reconciler)。Fiber 的本质是把整棵 [[虚拟DOM]] 的递归更新变成**可中断的循环 + 链表数据结构**,从而让浏览器在长任务期间仍能响应用户输入。它是 Suspense、startTransition、并发渲染、Server Components 的底层基础设施。

## 核心要点

### 1. 为什么需要 Fiber?

React 15 的协调是同步递归:大组件树 diff 一旦开始,主线程被独占数十毫秒,卡住动画与输入。Fiber 把这个长任务切成约 5ms 切片,每片之间让出主线程,浏览器可以处理事件、完成绘制,再回来继续。

### 2. Fiber 节点

每个组件实例对应一个 Fiber 节点:

```js
{
  type, key, stateNode,            // 标识与实例
  return, child, sibling,          // 树形指针
  alternate,                        // 双缓冲:current vs work-in-progress
  memoizedState, memoizedProps,    // 上次状态
  pendingProps, updateQueue,       // 待处理
  effectTag, nextEffect,           // 副作用链
  lanes                             // 优先级(R18 后)
}
```

链表结构允许暂停后保留进度,递归改为循环遍历。

### 3. 双缓冲(Double Buffering)

`current` 树是当前显示的;`workInProgress` 树是正在构建的。完工后 alternate 切换,避免半完成状态被显示。

### 4. 工作循环

```
while (workInProgress && shouldYield()) {
  performUnitOfWork(workInProgress);
}
```

`shouldYield` 借助 `MessageChannel` / `requestIdleCallback` 判断是否该让出。

### 5. 优先级 / 车道(Lane Model)

React 18 引入 Lane 模型,用 31 位 bitmap 表示优先级:

- **Discrete**:点击、输入(最高)
- **Continuous**:滚动、拖动
- **Default**:网络响应
- **Transition**:`startTransition` 包裹的非急更新
- **Idle**:空闲

不同 lane 可独立调度,高优先级中断低优先级。

### 6. 并发特性

Fiber 让 React 18 解锁:

- **`startTransition`**:把非紧急更新(过滤大列表)标记为 transition,被高优先级输入打断不卡顿
- **`useDeferredValue`**:延迟值更新
- **Suspense**:暂停渲染等待数据/代码,展示 fallback
- **Selective Hydration**:SSR 后选择性激活组件
- **React Server Components**:跨边界组件,部分服务器渲染
- **Automatic Batching**:setState 自动合批,不仅在事件中

### 7. 副作用链

Fiber 在协调过程中收集 effect 链表,提交阶段(commit phase)同步执行 DOM 操作、生命周期、ref。提交不可中断,保证一致性。

### 8. 名字由来

"Fiber" 源自计算机科学里比线程更轻量的协作式调度单位,呼应其可暂停可恢复特性。

## 关系

- 属于:[[React]] 16+ 核心
- 操作:[[虚拟DOM]] 树
- 启用:[[React Hooks]] 与并发渲染配合
- 原理:链表 + 双缓冲 + 优先级调度
- 对比:[[Vue]] 3 reactivity 与 [[Svelte]] 编译路线另辟蹊径

## 参考源

- raw/计算机/开发学习/框架/React/
