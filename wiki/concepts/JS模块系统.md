---
title: JavaScript 模块系统
type: concept
tags: [cs, web, javascript, mature]
sources: [raw/计算机/开发学习/语言/Javascript/02-理解掌握层/04-模块化/]
created: 2026-05-05
updated: 2026-05-05
summary: JS 历史上有 CommonJS(Node)、AMD(浏览器异步)、UMD(通用)、ESM(标准)四种模块系统,ESM 现已成为浏览器与 Node 共同标准,Tree Shaking 的基石。
---

# JavaScript 模块系统

## 定义

**JavaScript 模块系统** 是把代码组织为独立、可复用单元并管理依赖的机制。JS 直到 ES2015 才有原生模块,在此之前演化出多种模块规范以服务不同环境(浏览器、服务器、通用)。当前主流是 **ESM(ECMAScript Modules)** + 历史遗留 **CJS(CommonJS)**。

## 核心要点

### 1. CommonJS(CJS)

Node.js 默认的模块格式:

```js
// math.js
function add(a, b) { return a + b; }
module.exports = { add };

// app.js
const { add } = require('./math');
```

特性:
- **同步**加载(适合服务端,本地文件)
- 运行时解析依赖
- 模块缓存机制(`require.cache`)
- 不支持 Tree Shaking(动态结构)

### 2. AMD(Asynchronous Module Definition)

RequireJS 推动,浏览器异步加载:

```js
define(['jquery'], function($) {
  return { init: function() { $('body'); } };
});
```

历史方案,已被打包工具淘汰。

### 3. UMD(Universal Module Definition)

兼容 CJS + AMD + 全局变量,旧库分发常用,代码冗长。

### 4. ESM(ECMAScript Modules)

ES2015 规范,JS 原生模块:

```js
// math.js
export function add(a, b) { return a + b; }
export const PI = 3.14;
export default class Calculator {}

// app.js
import { add, PI } from './math.js';
import Calc from './math.js';
import * as math from './math.js';
```

特性:
- **静态结构**:import/export 必须顶层、字面量,编译期可分析
- **异步加载**:浏览器原生 `<script type="module">`
- **严格模式**默认
- **Tree Shaking** 友好
- **循环依赖**部分支持

### 5. 动态 import

```js
const m = await import('./heavy.js');
```

ES2020 标准,返回 Promise,实现按需加载、代码分割。

### 6. CJS vs ESM 互操作

混用是 Node 与生态痛点:

| 方向 | 行为 |
|---|---|
| ESM 引 CJS | `import x from 'cjs'`,默认导出整个 module.exports |
| CJS 引 ESM | 必须 `await import()`,不能 require |
| 双包危险 | 同模块两份实例破坏单例 |

Node.js 22+ 支持同步 require ESM(无 top-level await 时),缓解互操作。

### 7. 模块解析

- **裸说明符**:`'react'` → node_modules 查找
- **相对路径**:`'./util'`
- **绝对路径**:`'/abs/path'`(需打包工具支持)
- **URL**:浏览器 ESM、Deno

`exports`、`imports` 字段(package.json)允许多入口、条件导出(node/browser/import/require)。

### 8. 现代实践

- 新项目纯 ESM(`"type": "module"`)
- 工具链支持 ESM(Vite、tsx、Bun)
- 旧 CJS 库通过编译/双包分发

## 关系

- Tree Shaking:[[Webpack]]、[[Vite]] 依赖 ESM 静态结构
- 类型:[[TypeScript类型系统]] 同样使用 import/export
- 运行时:Node.js、Deno、Bun 模块解析
- 历史:RequireJS、Browserify 已退场
- 应用:所有现代 [[React]]、[[Vue]] 项目

## 参考源

- raw/计算机/开发学习/语言/Javascript/02-理解掌握层/04-模块化/01-CommonJS规范.md
- raw/计算机/开发学习/语言/Javascript/02-理解掌握层/04-模块化/03-ES6模块系统.md
- raw/计算机/开发学习/语言/Javascript/02-理解掌握层/04-模块化/04-模块加载机制.md
