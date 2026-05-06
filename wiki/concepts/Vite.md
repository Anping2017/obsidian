---
title: Vite
type: concept
tags: [cs, web, build, mature]
sources: [raw/计算机/开发学习/框架/React/Vite/]
created: 2026-05-05
updated: 2026-05-05
summary: Vite 是尤雨溪 2020 年发布的下一代前端构建工具,开发模式利用原生 ESM 实现毫秒级冷启动,生产模式用 Rollup 打包,已成新项目首选。
---

# Vite

## 定义

**Vite**(法语"快"的意思,发音 /vit/)是尤雨溪(Vue 作者)2020 年发布的下一代前端构建工具。核心创新:**开发模式跳过打包**,利用浏览器原生 ESM(`<script type="module">`)按需编译每个文件;**生产模式**用 [[Rollup]] 打成传统 bundle。冷启动从 [[Webpack]] 的几十秒降到秒级,HMR 几乎瞬时。

## 核心要点

### 1. 开发模式原理

```html
<script type="module" src="/src/main.ts"></script>
```

浏览器收到 main.ts → 请求 → Vite 用 esbuild 即时编译 TS/JSX → 返回 ESM。子模块 `import './App.vue'` 触发新请求,**只编译被实际访问的文件**。无需打包整个项目。

### 2. 依赖预构建

第三方依赖(react、vue、lodash)通常是 CJS 或散碎模块,首次启动时 Vite 用 esbuild 预打包到 `node_modules/.vite`,转 ESM 并合并。后续秒级启动。

### 3. 生产模式

调用 [[Rollup]] 进行传统打包(代码分割、Tree Shaking、压缩)。原因:

- 浏览器若直接加载几百个独立 ESM 模块会请求过多
- Rollup 输出体积、Tree Shaking 在库场景仍最优

未来可能切到 Rolldown(Vite 团队用 Rust 重写的 Rollup)。

### 4. 与 Webpack 对比

| 维度 | [[Webpack]] | Vite |
|---|---|---|
| 冷启动 | 数十秒 | 1-3 秒 |
| HMR | 秒级 | 毫秒级 |
| 配置 | 复杂(loader/plugin) | 极简 |
| 生态 | 极广 | 大且增长快 |
| 编译器 | JS(慢) | esbuild + SWC(Rust/Go) |
| Bundle | Webpack 自身 | Rollup |
| 旧浏览器 | 直接支持 | 需 @vitejs/plugin-legacy |

### 5. 配置(vite.config.ts)

```ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: { port: 3000 },
  build: { outDir: 'dist' }
});
```

约定优于配置:public 目录、assets 处理、CSS 模块化、TS 等开箱即用。

### 6. 插件系统

Vite 兼容 Rollup 插件 API,生态可复用。同时 Vite 自有 hooks(configureServer、transformIndexHtml...)。常用:

- @vitejs/plugin-react / vue / svelte
- vite-plugin-pwa
- vite-plugin-mock
- unplugin-auto-import

### 7. SSR 与元框架

Vite 提供 SSR 原语;之上有:

- **Nuxt 3** ([[Vue]])
- **SvelteKit** ([[Svelte]])
- **SolidStart** ([[SolidJS]])
- **Astro**(多框架并存)
- **Remix** v2(从 Webpack 迁来)

[[Next.js]] 仍用 Webpack/Turbopack。

### 8. Vite 6(2024)与 Environment API

支持多环境构建(浏览器、SSR、Worker、Edge)统一配置,为更多元框架奠基。

## 关系

- 替代:[[Webpack]] 在新项目
- 用作:[[Rollup]] 包装(生产)+ esbuild 包装(开发)
- 兼容:Rollup 插件
- 应用:[[Vue]]、[[React]]、[[Svelte]]、[[SolidJS]]
- 衍生:Nuxt、SvelteKit、Astro、Remix
- 原理:[[JS模块系统]] 浏览器原生 ESM

## 参考源

- raw/计算机/开发学习/框架/React/Vite/Vite.md
