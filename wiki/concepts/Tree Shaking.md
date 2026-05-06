---
title: Tree Shaking
type: concept
tags: [cs, web, build, mature]
sources: [raw/计算机/开发学习/语言/Javascript/04-高级精通层/03-性能优化/]
created: 2026-05-05
updated: 2026-05-05
summary: Tree Shaking 是基于 ES Module 静态分析的死代码消除技术,构建工具在生产环境删除未被引用的导出,显著降低 bundle 体积。
---

# Tree Shaking

## 定义

**Tree Shaking**(摇树)是 JavaScript 打包工具在生产环境进行的**死代码消除(Dead Code Elimination, DCE)** 技术。术语形象:把模块依赖树摇一摇,没"挂着"的(未被引用的)代码就掉下来被丢弃。Rich Harris 在 [[Rollup]] 中首次实现,后被 [[Webpack]]、[[Vite]]、esbuild 等普及。

## 核心要点

### 1. 为什么 ESM 才能 Tree Shake?

ES Module 的 **静态结构**:

```js
import { add } from 'lodash-es';   // 编译期可知导入哪个
```

而 CommonJS 是动态的:

```js
const lib = require('lodash');     // 运行时才知道用什么
const fn = condition ? lib.a : lib.b;
```

CJS 无法静态分析,Tree Shaking 失效。

### 2. 工作流程

1. 构建工具解析所有 import/export,建立模块依赖图
2. 标记每个 export 是否被引用
3. 未引用的 export 在最终 bundle 中删除

### 3. 副作用(Side Effects)

模块顶层执行的代码(如修改全局对象、polyfill)即使没 export 被用,也不能删除。`package.json` 中:

```json
{ "sideEffects": false }
```

声明无副作用,允许激进 Tree Shaking。或精确列表:

```json
{ "sideEffects": ["*.css", "./polyfill.js"] }
```

很多 npm 包未正确声明,导致大体积。

### 4. 反模式

```js
// 错:整个 lodash 引入,Tree Shaking 难
import _ from 'lodash';
_.cloneDeep(obj);

// 对:具名导入,可摇
import { cloneDeep } from 'lodash-es';
cloneDeep(obj);
```

或使用 babel-plugin-import / unplugin-icons 自动转换。

### 5. 字符 vs 类的差异

```js
import * as utils from './utils';  // 命名空间引入,所有 export 视为用过
utils.foo();
```

工具能否摇取决于实现。Webpack 5 + ESM 通常能,旧版常摇不动。

### 6. 与 Code Splitting 区别

| 技术 | 作用 |
|---|---|
| Tree Shaking | 静态删除未用代码 |
| [[代码分割]] | 把代码拆为多个 chunk 按需加载 |

二者互补:先摇掉死代码,再拆分剩余。

### 7. Bundler 对比

| 工具 | Tree Shaking 能力 |
|---|---|
| [[Rollup]] | 起源,最强 |
| [[Webpack]] 5 | 强,需要 ESM + sideEffects |
| [[Vite]] | 生产用 Rollup,优秀 |
| esbuild | 强 |
| Parcel | 中 |

### 8. 检测工具

- `webpack-bundle-analyzer`:可视化 chunk 内容
- `source-map-explorer`:看每个文件占多少
- `rollup-plugin-visualizer`:Vite 配套
- Lighthouse:整体 JS 体积红绿灯

### 9. 实战

- 总是用 ESM 版库(`lodash-es`、`date-fns`)
- 配置 sideEffects
- 避免桶导出(`export * from`)在大型项目
- 第三方组件库选支持 Tree Shaking 的(Ant Design、Element Plus 已支持)

## 关系

- 基于:[[JS模块系统]] ESM 静态结构
- 工具:[[Webpack]]、[[Vite]]、[[Rollup]]
- 配合:[[代码分割]]
- 启用:更小 bundle → 更快 [[Core Web Vitals]] LCP
- 反例:CJS 库常导致摇不动

## 参考源

- raw/计算机/开发学习/语言/Javascript/04-高级精通层/03-性能优化/03-代码分割.md
