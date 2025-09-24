## 🔹 1. 什么是虚拟 DOM？

- **DOM（文档对象模型）**：浏览器用树状结构来表示页面，比如 `<div><p>Hello</p></div>`。
    
- **虚拟 DOM（Virtual DOM, VDOM）**：React 在内存里用 **JavaScript 对象** 来模拟 DOM 结构。
    
    - 它不是浏览器的 DOM，而是一个“轻量级的副本”。
        
    - React 会先更新 **虚拟 DOM**，再计算出最小的差异（Diff），最后高效更新真实 DOM。
        

👉 类比：

- 直接操作真实 DOM = 拿毛笔在画布上改，费时费力。
    
- 虚拟 DOM = 先在草稿纸上改好，再把差异抄到画布上，速度快得多。
    

---

## 🔹 2. 为什么需要虚拟 DOM？

操作 DOM 是 **昂贵**的，因为：

- DOM 操作会触发 **重排（Reflow）** 和 **重绘（Repaint）**。
    
- 大量频繁修改时，性能会很差。
    

React 的优化策略：

1. **用虚拟 DOM 承担所有计算**（纯 JS，速度快）。
    
2. **只把必要的差异更新到真实 DOM**（最小化开销）。
    

---

## 🔹 3. 虚拟 DOM 的工作流程

1. **创建虚拟 DOM**
    
    - JSX → 转换成 JavaScript 对象（VDOM）。
        
    
```
<h1>Hello</h1>
// 等价于：
{
  type: "h1",
  props: { children: "Hello" }
}

```
    
2. **Diff 算法比较新旧 VDOM**
    
    - React 会比较前后的虚拟 DOM 树，找到不同的节点。
        
    - 采用 **O(n)** 的高效算法（不做完全树对比，而是逐层比较 + key 优化）。
        
3. **Patch（更新真实 DOM）**
    
    - 把变化的地方应用到浏览器的真实 DOM。
        

---

## 🔹 4. 小例子

```
function App() {
  const [count, setCount] = React.useState(0);

  return (
    <div>
      <p>{count}</p>   {/* 只有这里变化 */}
      <button onClick={() => setCount(count + 1)}>+</button>
    </div>
  );
}

```

- React 每次更新时：
    
    1. 生成新的虚拟 DOM。
        
    2. 与旧的虚拟 DOM 做 Diff。
        
    3. 发现只有 `<p>{count}</p>` 变了，就只更新这个部分。
        

👉 整个 `<div>` 并不会重新渲染到真实 DOM。

---

## 🔹 5. 虚拟 DOM 的优缺点

✅ **优点**

- 提升性能（避免不必要的 DOM 更新）。
    
- 简化编程（你只管写声明式 UI）。
    
- 跨平台（不仅能映射到浏览器 DOM，还能映射到原生 UI，支持 React Native）。
    

⚠️ **缺点**

- 不是所有场景都比手写 DOM 快（例如极简页面，直接操作 DOM 可能更高效）。
    
- 多了一层虚拟计算，有一定的内存开销。
    

---

## 🔹 6. 一句话总结

**虚拟 DOM** = **在内存里模拟 DOM → Diff 算法找出变化 → 最小化更新真实 DOM**。  
它的价值在于：**高效 + 跨平台 + 声明式编程的基础设施**。