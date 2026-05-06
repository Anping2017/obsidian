---
title: Rollup
type: concept
tags: [cs, web, build, mature]
sources: [raw/计算机/开发学习/]
created: 2026-05-05
updated: 2026-05-05
summary: Rollup 是 Rich Harris 2015 年创建的 ES Module 打包器,以 Tree Shaking 起家,擅长输出体积最小的库 bundle,Vite 生产模式即基于 Rollup。
---

# Rollup

## 定义

**Rollup** 是 Rich Harris(Svelte 作者)2015 年创建的 JavaScript 打包工具。设计初衷:**为 ES Modules 而生的打包器**,首次实现严格的 [[Tree Shaking]]。Rollup 不是 [[Webpack]] 的全能替代,而是聚焦"打包成可分发模块"这一场景:库、SDK、UMD 包、CDN 文件。

## 核心要点

### 1. 配置示例

```js
// rollup.config.js
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import typescript from '@rollup/plugin-typescript';

export default {
  input: 'src/index.ts',
  output: [
    { file: 'dist/index.cjs', format: 'cjs' },
    { file: 'dist/index.mjs', format: 'esm' },
    { file: 'dist/index.umd.js', format: 'umd', name: 'MyLib' }
  ],
  plugins: [resolve(), commonjs(), typescript()]
};
```

一次构建多种格式输出,SemVer 库分发标准。

### 2. 优势

#### Tree Shaking 极致

Rollup 是 Tree Shaking 概念的发明者。同样的代码,Rollup 输出经常比 Webpack 小 5-30%(尤其库)。

#### 输出干净

无 webpack runtime / chunk loader,代码近乎原样保留。便于阅读、调试。

#### ESM 优先

源代码即 ESM,无需 require 包装层。

### 3. 与 Webpack/Vite 对比

| 维度 | Webpack | Rollup | Vite |
|---|---|---|---|
| 主战场 | 应用 | 库 | 应用 + 库 |
| Tree Shaking | 良好 | 极致 | (用 Rollup) |
| HMR | 内置 | 弱 | 极强 |
| 输出格式 | 多种 | 多种 | (用 Rollup) |
| 配置复杂度 | 高 | 中 | 低 |
| 速度 | 慢 | 中 | 快 |

[[Vite]] 开发模式跳过打包,但生产模式调用 Rollup。Rollup 是 Vite 的引擎之一。

### 4. 主流插件

- `@rollup/plugin-node-resolve`:解析 node_modules
- `@rollup/plugin-commonjs`:转 CJS 为 ESM
- `@rollup/plugin-typescript`:TS 编译
- `@rollup/plugin-terser`:压缩
- `@rollup/plugin-replace`:常量替换
- `rollup-plugin-visualizer`:bundle 可视化

### 5. 使用 Rollup 的著名项目

- React(打包旧版)
- Vue 3
- D3.js
- Three.js
- React Three Fiber
- Lit
- 几乎所有主流前端库

### 6. Rolldown(2024+)

Vite 团队用 Rust 重写的 Rollup,API 兼容、速度提升数倍。预计 Vite 7 全面切换。

### 7. 何时选 Rollup?

**库作者**:发布到 NPM,需要 ESM/CJS/UMD 多格式 + 最小体积 + 干净输出。

**何时不选**:

- 应用项目(用 [[Vite]] 或 [[Webpack]],它们底层已用 Rollup)
- 开发阶段需 HMR
- 需要复杂代码分割(Webpack 更强)

## 关系

- 引擎:[[Vite]] 生产模式
- 创新:[[Tree Shaking]] 概念发明
- 对比:[[Webpack]]、esbuild、Parcel
- 演进:Rolldown(Rust 重写)
- 标准:[[JS模块系统]] ESM

## 参考源

- raw/计算机/开发学习/框架/React/Vite/
