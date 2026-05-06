---
title: Web Components
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/语言/HTML/04-知识拓展层/新兴技术趋势/04-12 Web Components体系.md]
created: 2026-05-05
updated: 2026-05-05
summary: Web Components 是浏览器原生的组件标准,由 Custom Elements、Shadow DOM、HTML Templates 三件套组成,框架无关、可跨技术栈复用,是设计系统的基础设施。
---

# Web Components

## 定义

**Web Components** 是 W3C 一组**浏览器原生**组件标准,目标:让开发者**不依赖任何框架**就能创建可复用、封装、可组合的自定义 HTML 元素。三大核心规范:

1. **Custom Elements**:定义新标签 `<my-button>`
2. **Shadow DOM**:封装内部 DOM 与样式,防外部污染
3. **HTML Templates**:`<template>` `<slot>` 标签,惰性 DOM

## 核心要点

### 1. Custom Elements

```js
class MyButton extends HTMLElement {
  constructor() { super(); }
  connectedCallback() { this.innerHTML = '<button>Click</button>'; }
  disconnectedCallback() {}
  attributeChangedCallback(name, old, val) {}
  static get observedAttributes() { return ['label']; }
}

customElements.define('my-button', MyButton);
```

```html
<my-button label="Save"></my-button>
```

生命周期回调对应 [[React]]/[[Vue]] 的 mount/unmount。

### 2. Shadow DOM

```js
this.attachShadow({ mode: 'open' }).innerHTML = `
  <style>button { color: red; }</style>
  <button><slot></slot></button>
`;
```

Shadow DOM 内的 CSS 不影响外部,外部 CSS 也不污染内部。`<slot>` 接收外部子节点。这是组件封装的关键:**真正的样式隔离**(对比 Vue scoped、CSS Modules 是约定 hash,Shadow DOM 是浏览器级)。

### 3. HTML Templates

```html
<template id="card">
  <div class="card"><slot></slot></div>
</template>
<script>
  const tpl = document.getElementById('card');
  document.body.appendChild(tpl.content.cloneNode(true));
</script>
```

`<template>` 内容不渲染,可重复克隆插入,适合列表、复杂组件。

### 4. 与 React/Vue 框架组件对比

| 维度 | 框架组件 | Web Components |
|---|---|---|
| 运行时依赖 | 需框架 | 浏览器原生 |
| 跨技术栈 | 难 | 任何项目都能用 |
| 样式隔离 | scoped/Modules | Shadow DOM 真隔离 |
| 状态管理 | 框架方案 | 自管理或库 |
| 学习曲线 | 框架专用 | DOM API 直接 |
| 生态 | 巨大 | 中(Lit、Stencil) |

### 5. Lit 与 Stencil

直接写 Web Components 太底层(模板字符串、手动 attribute 绑定)。两个工具广泛使用:

- **Lit**(Google):基于 Tagged Template,2KB,响应式 + 模板,语法接近 React
- **Stencil**(Ionic):TypeScript 装饰器,编译为 Web Components,可生成 React/Vue 包装器

```js
import { LitElement, html } from 'lit';

class MyCounter extends LitElement {
  static properties = { count: { type: Number } };
  constructor() { super(); this.count = 0; }
  render() {
    return html`<button @click=${() => this.count++}>${this.count}</button>`;
  }
}
customElements.define('my-counter', MyCounter);
```

### 6. 实际应用

- **设计系统**:Salesforce Lightning、Adobe Spectrum、IBM Carbon、SAP UI5、GitHub Primer
- **跨技术栈复用**:同一个 `<chart-widget>` 在 React、Vue、纯 HTML 都可用
- **Microsoft Edge / GitHub**:大量内部 UI 用 Web Components

### 7. 框架集成

React 19 改进 Web Components 支持(原本对 prop/event 处理不佳)。Vue/Angular/Svelte 早已天然支持 `<my-element>` 标签。

### 8. 局限

- SSR 复杂(declarative shadow DOM 标准化中)
- 表单关联(form-associated custom elements)需额外 API
- Shadow DOM 内 CSS 全局变量可穿透,需用 CSS Custom Properties 桥接

## 关系

- 标准:浏览器原生,W3C 标准化
- 工具:Lit、Stencil
- 对比:[[React]]、[[Vue]]、[[Angular]] 框架组件
- 配合:[[CSS变量]] 跨 Shadow 边界传值
- 应用:设计系统、微前端

## 参考源

- raw/计算机/开发学习/语言/HTML/04-知识拓展层/新兴技术趋势/04-12 Web Components体系.md
