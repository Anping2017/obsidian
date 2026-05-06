---
title: 虚拟 DOM
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/框架/React/基础概念/虚拟 DOM.md]
created: 2026-05-05
updated: 2026-05-05
summary: 虚拟 DOM 是真实 DOM 的 JS 对象副本,通过 diff 算法找出最小变更集再批量提交,以小成本计算换取大成本 DOM 操作的减少。
---

# 虚拟 DOM

## 定义

**虚拟 DOM(Virtual DOM, vDOM)** 是用 JavaScript 对象描述 UI 树结构的轻量副本。它由 [[React]] 在 2013 年首次大规模商用,核心思想:**所有 UI 变化先在 vDOM 上发生,通过 diff 算法计算与上一棵 vDOM 的差异,只把必要的最小变更应用到真实 DOM**。

## 核心要点

### 1. 为何需要 vDOM?

真实 DOM 操作昂贵,每次修改可能触发:

- **重排(Reflow)**:浏览器重新计算几何布局
- **重绘(Repaint)**:重新绘制像素

频繁直接操作会掉帧。vDOM 把昂贵的写操作集中、批量、最小化。

### 2. JSX → vDOM 节点

```jsx
<h1 className="title">Hello</h1>
```

被 Babel 编译为:

```js
{
  type: 'h1',
  props: { className: 'title', children: 'Hello' }
}
```

整棵 UI 是这种对象的递归树。

### 3. Diff 算法

理论最优树 diff 是 O(n³),React 通过两条假设把它降到 O(n):

1. **同层级比较**:不跨层级移动节点
2. **key 优化**:列表中用 key 标识节点身份,顺序变化时复用节点而非重建

```jsx
{items.map(item => <Row key={item.id} data={item} />)}
```

key 错(用 index 作 key 且列表会重排)是性能与状态错乱的常见 bug 源。

### 4. Reconciliation(协调)

React 把 diff 结果转为 effects(insert / update / delete),再批量提交到真实 DOM。React 16+ 的 [[React Fiber]] 把这一过程切片,可中断、可优先级。

### 5. 与其他方案对比

| 方案 | 代表 | 思路 |
|---|---|---|
| 虚拟 DOM | [[React]]、Preact | 整树 diff |
| 编译时分析 | [[Svelte]]、[[SolidJS]] | 编译期生成精确更新代码,无 diff |
| 数据劫持 | [[Vue]] 2 | Proxy/defineProperty 触发组件级 diff |
| 直接 DOM | jQuery、AngularJS 早期 | 手动操纵 |

### 6. vDOM 真的快吗?

很多场景**不一定**比手工 DOM 快(diff 本身有成本)。它的真正价值在于:

- 声明式 UI 编程模型
- 跨平台(React Native 用 vDOM 映射到原生 UI)
- 与状态管理无缝结合

性能极致追求时,Svelte/Solid 的编译方案更快。

### 7. 跨平台

vDOM 抽象层让 React 能渲染到:

- 浏览器 DOM(react-dom)
- 移动原生(React Native → iOS UIView / Android View)
- VR(react-360)
- 终端(react-ink)
- Canvas(react-three-fiber)

## 关系

- 核心:[[React]] 范式基础
- 实现:[[React Fiber]] 当前协调器
- 对比:[[Svelte]]、[[SolidJS]] 编译路线
- 对比:[[Vue]] Proxy 路线
- 应用:跨平台渲染目标的统一 IR

## 参考源

- raw/计算机/开发学习/框架/React/基础概念/虚拟 DOM.md
