---
title: CSS-in-JS
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/语言/CSS/, raw/计算机/开发学习/框架/React/]
created: 2026-05-05
updated: 2026-05-05
summary: CSS-in-JS 把样式写在 JS 模块中,通过组件作用域、props 驱动、Tree Shaking 解决传统 CSS 命名冲突与死代码问题,但运行时开销与 SSR 复杂度推动其向零运行时演进。
---

# CSS-in-JS

## 定义

**CSS-in-JS** 是 React 生态(2014-)兴起的样式范式,把 CSS 写在 JavaScript/[[TypeScript类型系统]] 模块内,样式与组件**强耦合**、**作用域天然隔离**。代表库:styled-components、Emotion、Linaria、vanilla-extract、Stitches。

## 核心要点

### 1. 解决的传统 CSS 痛点

| 痛点 | CSS-in-JS 方案 |
|---|---|
| 全局命名冲突 | 自动生成 hash class |
| 死代码无法删除 | 与组件 import 绑定 |
| 主题切换零散 | props/context 注入 |
| 动态样式靠 inline style | 完整 CSS 能力 |
| 类型缺失 | TS 提示 props |

### 2. 主流写法

#### 模板字符串(styled-components / Emotion)

```jsx
const Button = styled.button`
  background: ${p => p.primary ? '#4f46e5' : '#fff'};
  padding: 12px;
  &:hover { opacity: 0.8; }
`;
```

#### Object Style(Emotion css prop)

```jsx
<div css={{ color: 'red', fontSize: 16 }} />
```

#### Atomic / Static Extraction(Linaria、vanilla-extract)

编译期把 JS 中的样式提取成独立 CSS 文件,**零运行时**。

### 3. 运行时 vs 零运行时

| 类型 | 代表 | 优 | 劣 |
|---|---|---|---|
| 运行时 | styled-components, Emotion | 完全动态 | 体积+性能开销 |
| 零运行时 | Linaria, vanilla-extract, Panda | 静态 CSS, 高速 | 动态性受限 |

React 18 + RSC 让运行时方案 SSR 难度暴增,**零运行时与 Atomic CSS 成为新趋势**。

### 4. 与 CSS Modules / Tailwind 对比

| 方案 | 作用域 | 学习曲线 | 主题 | 性能 |
|---|---|---|---|---|
| 全局 CSS | 全局污染 | 低 | 难 | 优 |
| CSS Modules | 文件作用域 | 低 | 中 | 优 |
| Sass + BEM | 命名约束 | 中 | 中 | 优 |
| Tailwind(原子化) | utility class | 中 | 自带 | 极优 |
| CSS-in-JS 运行时 | 组件作用域 | 中 | 优 | 中 |
| 零运行时 CSS-in-JS | 组件作用域 | 中 | 优 | 优 |

### 5. SSR 复杂度

运行时方案需在服务端收集所有渲染样式注入 HTML,避免 FOUC。Emotion/SC 提供 SSR API,但与 React Server Components 冲突日益明显。

### 6. 当前趋势(2024-2026)

- React 团队不推荐运行时 CSS-in-JS 用于新 Server Components 应用
- Tailwind CSS + [[CSS变量]] 占据新增项目主流
- vanilla-extract、Panda CSS 等零运行时方案承接旧 styled-components 用户
- Next.js 13+ 的 RSC 推动这一迁移

## 关系

- 替代:全局 CSS、Sass + BEM
- 竞争:Tailwind 原子化、CSS Modules
- 配合:[[React]] 组件化思维
- 演进:[[CSS变量]] 让原生 CSS 也具备动态能力,挤压 CSS-in-JS 必要性
- 工具:[[Webpack]]/[[Vite]] babel-plugin 编译期处理

## 参考源

- raw/计算机/开发学习/语言/CSS/04-高级进阶层/前沿技术/
- raw/计算机/开发学习/语言/CSS/04-高级进阶层/CSS架构/
