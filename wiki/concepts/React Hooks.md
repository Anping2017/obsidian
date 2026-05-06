---
title: React Hooks
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/框架/React/]
created: 2026-05-05
updated: 2026-05-05
summary: React Hooks 是 16.8 引入的函数组件能力增强机制,通过 useState/useEffect 等钩子让函数组件持有状态、处理副作用、订阅上下文,取代 class 组件主导地位。
---

# React Hooks

## 定义

**React Hooks** 是 [[React]] 16.8(2019 年 2 月)引入的特性,允许在**函数组件中使用状态(state)、生命周期(lifecycle)、上下文(context)等原本只属于 class 组件**的能力。Hook 是以 `use` 开头的特殊函数,只能在函数组件顶层或自定义 Hook 中调用。

## 核心要点

### 1. 内置 Hooks

| Hook | 作用 |
|---|---|
| `useState` | 持有局部状态 |
| `useEffect` | 副作用:订阅、订阅清理、网络请求 |
| `useLayoutEffect` | 同步执行的 effect(浏览器绘制前) |
| `useContext` | 读取 Context |
| `useReducer` | 复杂状态用 reducer 模式 |
| `useMemo` | 缓存昂贵计算 |
| `useCallback` | 缓存函数引用,稳定 props |
| `useRef` | 持久可变值,常用于 DOM 引用 |
| `useImperativeHandle` | forwardRef 暴露命令式 API |
| `useId` | 唯一 ID(SSR 安全) |
| `useDeferredValue` | 延迟更新降级渲染 |
| `useTransition` | 标记低优先级更新 |
| `useSyncExternalStore` | 接入外部 store |

### 2. Hook 的两条核心规则

1. **只能在最顶层调用**(不在 if/for/嵌套函数里)
2. **只能在 React 函数组件或自定义 Hook 中调用**

ESLint plugin `react-hooks/rules-of-hooks` 自动校验。

### 3. 为什么有这些规则?

React 用调用顺序而非名字识别每个 Hook。每次渲染按相同顺序调用 useState/useEffect,React 才能正确关联状态与 effect。条件 if 包裹会破坏顺序,导致状态错乱。

### 4. 自定义 Hook

复用逻辑的核心机制:

```js
function useFetch(url) {
  const [data, setData] = useState();
  useEffect(() => {
    fetch(url).then(r => r.json()).then(setData);
  }, [url]);
  return data;
}
```

任何用 `use` 开头的函数即被视为 Hook,可调用其他 Hook。

### 5. 与 class 组件对比

| 维度 | class | function + Hooks |
|---|---|---|
| 学习曲线 | this 绑定、生命周期 | 直接函数 |
| 复用逻辑 | HOC、Render Props | 自定义 Hook |
| 代码量 | 多 | 少 |
| TypeScript 友好 | 中 | 高 |
| 性能 | 中 | 优(更易优化) |

class 组件并未弃用,但新代码默认 function + Hooks。

### 6. useEffect 心智模型

```js
useEffect(() => {
  const id = setInterval(...);
  return () => clearInterval(id);  // cleanup
}, [deps]);
```

- 默认每次渲染后执行
- 第二参数 deps 数组:依赖变化才执行
- 返回函数为 cleanup,在下次执行前或卸载时调用
- 严格模式下 dev 双调用以暴露副作用问题

### 7. 常见陷阱

- **依赖数组遗漏**:闭包捕获旧值
- **无限循环**:在 effect 中 setState 未加正确 deps
- **过度优化**:乱用 useMemo/useCallback,React 19 编译器自动处理
- **派生状态**:能算就算,不要 useState 存

### 8. React 19 编译器

自动添加 useMemo/useCallback,让开发者不再手写优化。Hook 心智模型回归"声明就好"。

## 关系

- 属于:[[React]] 核心范式
- 基于:JS [[闭包]] 机制
- 取代:class 生命周期 componentDidMount 等
- 对应:[[Vue]] 的 Composition API setup
- 类型:[[TypeScript类型系统]] 中泛型 useState<T>
- 调度:[[React Fiber]] 让 Hooks 与并发兼容

## 参考源

- raw/计算机/开发学习/框架/React/基础概念/组件化.md
