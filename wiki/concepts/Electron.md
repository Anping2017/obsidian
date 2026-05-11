---
title: Electron 跨平台桌面框架
type: concept
tags: [frontend, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: Electron 是 GitHub 2013 年发布的桌面应用框架,用 Chromium 渲染 + Node.js 后端,以 Web 技术写跨平台桌面应用,VS Code、Slack、Discord 都基于此,内存占用高是常见诟病。
---

# Electron 跨平台桌面框架

## 定义

**Electron** 是由 GitHub 在 2013 年作为 Atom 编辑器底层引擎开源、2014 年独立成框架的跨平台桌面应用开发方案。它把 [[Chromium]](负责渲染 UI)与 [[Node.js]](负责系统访问)整合到同一进程模型中,开发者用 HTML / CSS / [[JavaScript原型链|JavaScript]] / [[TypeScript类型系统|TypeScript]] 写应用,即可一次代码三端打包(Windows / macOS / Linux)。Electron 由 OpenJS Foundation 治理,是当代桌面 SaaS 客户端最主流的实现方式。

## 核心要点

### 1. 架构

Electron 采用多进程模型:

- **Main Process**(主进程):运行 Node.js,管理生命周期、原生菜单、托盘、文件 I/O
- **Renderer Process**(渲染进程):每个 BrowserWindow 一个,运行 Chromium,跑前端代码
- **Preload Script**:在渲染进程中提前注入,桥接安全暴露主进程能力
- **IPC**:`ipcMain` / `ipcRenderer` 双向通信,Electron 14+ 推荐 `contextBridge` 安全暴露
- **Utility Process**(28+):用于 CPU 密集型任务,隔离风险

### 2. 关键能力

- 跨平台原生菜单、托盘、通知、剪贴板、Shell
- 文件系统、子进程、Native Modules(可加载 C++ 编译产物)
- 自动更新(electron-updater + Squirrel)
- 应用打包(electron-builder / electron-forge)
- 原生窗口控件、屏幕录制、深度链接、协议处理

### 3. 与 Web 应用的区别

- **不受同源策略限制**:可以本地读写文件、调系统 API
- **持久化资源**:缓存、本地数据库、密钥(keytar)
- **离线优先**:无网络仍可运行
- **更高资源占用**:每个 app 自带一个 Chromium

### 4. 性能与替代方案

| 方案 | 体积 | 内存 | 平台 | 语言 |
|---|---|---|---|---|
| **Electron** | 80–200MB | 较高 | Win/Mac/Linux | JS/TS |
| **Tauri** | 10–30MB | 低 | Win/Mac/Linux | Rust + Web 前端 |
| **Wails** | 10–30MB | 低 | Win/Mac/Linux | Go + Web 前端 |
| **Flutter Desktop** | 30–50MB | 中 | Win/Mac/Linux | Dart |
| **MAUI / WPF / Cocoa** | 原生 | 低 | 单平台 | C#/Swift |

[[Tauri]] 用 OS 自带 WebView(Edge WebView2 / WKWebView)而非自带 Chromium,体积大幅缩减;但 WebView 版本碎片化、API 受限。

### 5. 代表使用者

- **VS Code**(微软)
- **Slack、Discord、Microsoft Teams**
- **Figma 桌面端、Notion、Obsidian、Trello**
- **WhatsApp Desktop、Skype**
- **GitHub Desktop**

### 6. 安全要点

- 启用 `contextIsolation: true`、`nodeIntegration: false`
- 使用 `contextBridge` 严格白名单暴露 API
- 严控加载远程内容,防 RCE
- 启用 CSP、签名应用、自动更新通道
- 关注 Chromium / Electron 安全公告,及时升级

## 局限与争议

- **资源占用**:每个 Electron 应用 100MB+ 内存起步,几个并存就吃光小内存机器
- **包体过大**:80MB+ 的安装包是常态,首次下载体验差
- **启动慢**:相对原生应用启动延迟可感知
- **同质化体验**:Electron 应用难以契合 macOS / Windows 设计语言
- **安全边界**:渲染进程拿到 Node 能力即危险,需谨慎隔离
- **替代品兴起**:[[Tauri]] / [[Wails]] / Flutter Desktop 蚕食市场

## 与其他概念的关系

- 底层栈:[[Chromium]]、[[Node.js]]、[[V8]]
- 同类框架:[[Tauri]]、[[Wails]]、[[Flutter Desktop]]、[[NW.js]]、[[CEF]]
- Web 技术:[[HTML]]、[[CSS]]、[[JavaScript原型链|JavaScript]]、[[TypeScript类型系统|TypeScript]]
- 渲染范式:[[SPA]]、[[React]]、[[Vue]]、[[Svelte]] 都可作 Electron 前端
- 打包工具:[[electron-builder]]、[[electron-forge]]
- 关联实践:[[自动更新]]、[[应用签名]]、[[CSP]]、[[沙箱]]
- 与 Web 区分:[[PWA]] 是浏览器内的桌面化方案

## 参考源

- Electron 官方文档 electronjs.org
- *Electron in Action*(Manning)
- Tauri vs Electron 对比白皮书
