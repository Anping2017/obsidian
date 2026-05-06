---
title: WebAssembly
type: concept
tags: [cs, web, performance, mature]
sources: [raw/计算机/开发学习/语言/HTML/04-知识拓展层/新兴技术趋势/04-10 Web Assembly与HTML.md]
created: 2026-05-05
updated: 2026-05-05
summary: WebAssembly(Wasm)是浏览器原生支持的可移植二进制指令格式,接近原生速度执行 C/C++/Rust/Go 代码,成为 Web 重计算与 Edge/Server-side 通用沙箱。
---

# WebAssembly

## 定义

**WebAssembly(Wasm)** 是 W3C 2017 年标准化的可移植二进制指令格式。它是**为编译器设计的目标平台**:C/C++/Rust/Go/AssemblyScript 等语言可编译为 .wasm,在浏览器内以接近原生速度执行,与 JS 互操作。设计目标:**Web 上的高性能、安全、紧凑、跨平台计算**。

## 核心要点

### 1. 解决的问题

JS 解析 + JIT 优化对**计算密集型**任务(图像处理、3D 渲染、加密、模拟、游戏)仍有瓶颈。Wasm 提供:

- **解析快**:二进制格式,流式解码
- **执行快**:静态类型 + 优化 IR,JIT 编译为机器码
- **安全**:沙箱执行,内存与浏览器隔离
- **可移植**:同一 .wasm 跑遍所有浏览器、Node、Wasmtime、Wasmer

### 2. 与 JS 互操作

```js
const { instance } = await WebAssembly.instantiateStreaming(fetch('/m.wasm'));
const result = instance.exports.add(1, 2);
```

通过 import/export 函数与共享 ArrayBuffer 交换数据。

### 3. 主流编译目标

| 语言 | 工具 |
|---|---|
| Rust | wasm-pack, wasm-bindgen |
| C/C++ | Emscripten |
| Go | TinyGo, Go 1.21+ wasi |
| AssemblyScript | TS 子集直接 → Wasm |
| .NET | Blazor WebAssembly |
| Python | Pyodide(把 CPython 编译为 Wasm) |

### 4. 杀手应用

- **Figma**:C++ 渲染引擎编译为 Wasm,实现浏览器内秒开复杂矢量
- **Google Earth**:C++ 三维渲染
- **AutoCAD Web**:百万行 C++ 直接跑 Web
- **Photoshop Web**:Adobe 通过 Emscripten 把桌面版搬到浏览器
- **FFmpeg.wasm**:浏览器内视频处理
- **Pyodide / JupyterLite**:Web 数据科学
- **SQL.js / DuckDB-Wasm**:浏览器内 SQL

### 5. WASI(WebAssembly System Interface)

浏览器外运行 Wasm 的标准:

- 文件系统、网络、随机数等系统能力
- 让 Wasm 成为**通用沙箱**,跑在服务器、Edge、CLI

Cloudflare Workers、Fastly Compute@Edge、Wasmer Cloud 让 Wasm 跑在 [[Edge计算]] 节点。

### 6. Component Model

新一代标准,定义跨语言模块组合规则。多个 Wasm 模块可像积木拼合,跨语言调用强类型。

### 7. 性能权衡

- 启动:首次解析编译 50-200ms
- 计算:接近原生(2-5x 慢于 native),远超 JS
- 内存:线性内存,无 GC(Wasm GC 提案 2023 完成,Java/Kotlin/Go 受益)
- 调用 JS DOM:仍需通过 JS 桥接,频繁 DOM 操作不划算

### 8. 何时用?

- **大量 CPU 计算**:图像、音视频、加密、机器学习推理
- **跨平台代码复用**:已有 C++ 库直接编译,无需重写
- **沙箱化插件**:VS Code Web、Figma 插件用 Wasm 隔离不可信代码

不适合:简单 UI、DOM 重操作、网络 IO 密集型(JS 已足够)。

### 9. 与 JS 关系

Wasm **不取代 JS**,而是补充。JS 仍负责 DOM、事件、UI;Wasm 处理瓶颈计算。多数项目主用 JS,关键模块换 Wasm。

## 关系

- 浏览器:[[HTTP协议]] 加载,与 JS 互操作
- Edge:[[Edge计算]] 平台首选运行时
- 安全:沙箱与 [[Web安全]] 模型
- 工具:wasm-bindgen、Emscripten
- 应用:大型客户端应用(Figma、AutoCAD)

## 参考源

- raw/计算机/开发学习/语言/HTML/04-知识拓展层/新兴技术趋势/04-10 Web Assembly与HTML.md
