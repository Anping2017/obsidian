---
title: Webpack
type: concept
tags: [cs, web, build, mature]
sources: [raw/计算机/开发学习/]
created: 2026-05-05
updated: 2026-05-05
summary: Webpack 是 2012 年发布的 JavaScript 模块打包器,把所有资源视为模块构建依赖图,通过 loader 与 plugin 体系成为 2015-2022 年前端工程化事实标准。
---

# Webpack

## 定义

**Webpack** 是 Tobias Koppers 2012 年开源的 JavaScript 模块打包器(Module Bundler)。核心思想:**一切皆模块**(JS、CSS、图片、字体、JSON、SVG...都可被 import),Webpack 从入口文件出发构建依赖图,经过转换、合并、优化后输出浏览器可加载的 bundle。它是 2015-2022 年前端工程化的事实标准,直至被 [[Vite]]、Turbopack 等下一代工具挑战。

## 核心要点

### 1. 五大概念

| 概念 | 作用 |
|---|---|
| **Entry** | 构建起点,可多入口 |
| **Output** | 输出位置与命名 |
| **Loader** | 转换模块(.scss → CSS、.ts → JS) |
| **Plugin** | 扩展构建过程(压缩、注入 HTML、分析) |
| **Mode** | development / production / none |

### 2. Loader 链

```js
{ test: /\.scss$/, use: ['style-loader', 'css-loader', 'sass-loader'] }
```

从右到左依次执行:Sass → CSS → 注入 style 标签。

### 3. 常用 Plugin

- **HtmlWebpackPlugin**:生成 HTML 并注入 bundle
- **MiniCssExtractPlugin**:提取 CSS 为单独文件
- **DefinePlugin**:编译期注入全局常量
- **TerserPlugin**:JS 压缩
- **BundleAnalyzerPlugin**:可视化 bundle 体积

### 4. Tree Shaking

[[JS模块系统]] ESM 静态结构允许 Webpack 在生产模式删除未使用的导出代码。前提:

- 使用 ES Modules(非 CJS)
- `package.json` 中 `sideEffects: false` 或精确列表
- 生产 mode

### 5. Code Splitting(代码分割)

```js
import('./heavy').then(m => m.run());  // 动态 import 自动切包
```

或配置 `splitChunks` 拆 vendor、common、运行时。让首屏只加载关键代码。

### 6. HMR(热模块替换)

开发模式下 webpack-dev-server 监听文件变更,通过 WebSocket 推送差异,**保留组件状态**重新执行变更模块。React/Vue 与 HMR 集成实现"修改即生效"。

### 7. 生命周期与 Tapable

Webpack 内部基于 Tapable 钩子系统,Plugin 可在 100+ 钩子上挂载。这一设计让生态极其丰富,但也导致复杂度高。

### 8. 与 Vite/Rollup/esbuild 对比

| 维度 | Webpack | [[Vite]] | [[Rollup]] | esbuild |
|---|---|---|---|---|
| 开发模式 | 全量打包 | 原生 ESM | 不主打 dev | 极快 |
| 生态 | 极广 | 大 | 中 | 小但精 |
| 配置 | 复杂 | 简单 | 中等 | 极简 |
| 适用 | 旧项目维护 | 新前端项目 | 库 | 最快需求 |
| 速度 | 慢(数十秒~分钟) | 秒级 | 中 | 毫秒级 |

### 9. 现状

Webpack 仍是 Next.js、Create React App 等老项目底层,但新项目优先 Vite/Turbopack。Webpack 5(2020)引入 Federation(模块联邦),让微前端跨应用共享模块,这是其独特生命力。

### 10. Module Federation

```js
new ModuleFederationPlugin({
  name: 'app1',
  remotes: { app2: 'app2@http://...' },
  shared: ['react']
});
```

让多个独立部署的 SPA 在运行时共享代码,微前端架构核心技术。

## 关系

- 对手:[[Vite]]、Turbopack、Parcel、Rollup
- 标准:[[JS模块系统]] 的 ESM/CJS 互操作
- 启用:[[代码分割]]、[[Tree Shaking]]、HMR
- 微前端:Module Federation
- 集成:[[TypeScript类型系统]]、Babel、PostCSS

## 参考源

- raw/计算机/开发学习/框架/React/
