---
title: Tauri(轻量跨平台桌面框架)
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Tauri 是基于 Rust 后端 + 系统原生 WebView 前端的桌面应用框架,以 5MB 起步包体积、低内存、Rust 安全性挑战 Electron 在跨平台桌面领域的统治地位。
---

# Tauri(轻量跨平台桌面框架)

## 定义

**Tauri** 是 2019 年起由 Daniel Thompson-Yvetot 等人发起、2022 年 1.0 GA 的桌面应用框架。它的核心创新:**用 Rust 写后端,前端用任意 Web 框架(React/Vue/Svelte),界面渲染交给系统原生 WebView**(不像 Electron 自带 Chromium)。

结果:
- 包体积:Tauri 5-15 MB,Electron 100-200 MB
- 内存:Tauri 50-150 MB,Electron 200-500 MB
- 安全:Rust 后端 + 严格 IPC 权限模型

Tauri 是 Electron 的重要挑战者,2024 年成为 GitHub 增长最快的 Rust 项目之一。

## 与 Electron 对比

| 维度 | Tauri | Electron |
|---|---|---|
| 后端 | Rust | Node.js |
| 前端渲染 | 系统 WebView(WebKit/WebView2/WebKitGTK) | 自带 Chromium |
| 包体积 | 5-15 MB | 100-200 MB |
| 内存 | 50-150 MB | 200-500 MB |
| 启动速度 | 快 | 慢 |
| 跨平台 UI 一致 | 不(各系统 WebView 引擎差异) | 一致(都是 Chromium) |
| 安全 | 严格(Rust + 权限模型) | 中(Node 全权限) |
| 生态 | 新兴 | 成熟(VS Code、Slack、Discord) |
| 学习曲线 | Rust + Web | 全 Web |

## 架构

```
+-----------------------------+
|       前端(WebView)        |
|  React / Vue / Svelte / ... |
+--------------+--------------+
               | IPC(invoke / event)
+--------------v--------------+
|         Rust Core            |
|   命令处理、文件系统、API     |
+-----------------------------+
```

**前端**

- 任何 Web 框架(SPA)
- 通过 @tauri-apps/api 调 Rust 命令
- 也可调系统 API(文件、shell、HTTP 等)的封装

**Rust 后端**

```rust
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running");
}
```

**前端调用**

```typescript
import { invoke } from '@tauri-apps/api/tauri'

const result = await invoke<string>('greet', { name: 'Alice' })
```

类型安全(2.0+ 起 TS / Rust 双向类型生成)。

## 系统 WebView 取舍

**优势**

- 包小(不带浏览器)
- 系统更新带 WebView 升级
- 内存占用低

**问题**

- 各系统 WebView 不一样:
  - macOS:WebKit
  - Windows:WebView2(Chromium-based,需安装)
  - Linux:WebKitGTK
- CSS / JS 兼容性差异(如 Linux 上 Chrome 独有 API 不可用)
- Animation、Codec 表现不同

新项目需在三平台测试,避免使用 Chrome-only API。

## 核心特性

**1. 多窗口**

```rust
WindowBuilder::new(&app, "secondary", WindowUrl::App("about.html".into()))
    .title("About")
    .inner_size(400.0, 300.0)
    .build()?;
```

**2. 系统托盘**

```rust
SystemTray::new()
    .with_menu(SystemTrayMenu::new()...)
```

**3. 全局快捷键**

```rust
app.global_shortcut_manager()
    .register("CmdOrCtrl+Shift+H", || { /* show window */ })?;
```

**4. 通知 / 文件对话框 / 剪贴板 / 文件系统**

API 封装齐全,跨平台一致。

**5. 自动更新**

内置签名验证更新机制。

**6. 命令行参数 / Deep Linking**

注册 myapp:// URL scheme。

## 安全模型

Tauri 安全比 Electron 严格,Capability 系统:

```json
{
  "permissions": [
    "core:default",
    "fs:allow-read-text-file",
    "shell:allow-open"
  ]
}
```

前端只能调用显式授权的 API。Rust 后端默认无 shell:execute 权限,避免恶意代码任意命令执行。

## Tauri 2.0(2024)

重大升级:
- **支持移动端**:iOS / Android(基于 Tauri Mobile)
- **新 IPC**:更高性能、字节级传输
- **Capability 系统**:更精细权限
- **多 Webview per Window**
- **Plugin 系统重构**

让 Tauri 不再仅是桌面框架,向"全平台 Web Native"演进,与 Capacitor 形成竞争。

## 商业采用

**已知 Tauri 应用**

- Spacedrive(跨平台文件管理器)
- Tabby(终端模拟器)
- Pot(翻译工具)
- 1Password(部分 UI)
- 多个开源工具

仍在早期生态,但增速快。

## 适用场景

**最适合**

- 资源敏感桌面应用(笔记、词典、小工具)
- 启动速度重要(每天用)
- 已有 Web 团队 + Rust 团队
- 安全要求高(密码管理器、金融工具)

**不太适合**

- 重度依赖 Chrome 独有 API
- 大型企业应用(Electron 生态成熟)
- 团队无 Rust 能力

## 学习曲线

**前端**

- 熟悉 React/Vue/Svelte:很快
- TypeScript 推荐
- 配 Vite 极快

**Rust**

- 不需要写大量 Rust 也能起步
- 复杂功能需深入(Async、Trait、生命周期)
- Rust 学习曲线本身陡

**完整学习**

- 1-2 周完成简单项目
- 3-6 月达到生产水平
- 要熟练 Rust 半年到一年

## 工具链

```bash
# 创建项目
npm create tauri-app

# 开发(自动启动 Rust + 前端)
npm run tauri dev

# 构建
npm run tauri build  # 生成 .app / .exe / .dmg / .deb
```

## 局限

- WebView 兼容性差异
- Linux 上 WebKitGTK 表现不一
- 调试复杂(Rust + JS 双语言)
- 第三方 plugins 仍少
- 文档不及 Electron 全面
- 部署到 App Store / Microsoft Store 流程不熟

## 与 Capacitor 对比

**Capacitor**(Ionic 出品)与 Tauri 类似但走另一路线:
- 后端用平台原生(Swift / Kotlin)
- 跨平台移动 + 桌面
- 无 Rust

二者都属"WebView Native 应用"路线,Tauri 强调性能和 Rust 安全,Capacitor 强调原生平台 API 完整。

## 与浏览器扩展架构对比

Tauri 应用结构与浏览器扩展(content script + background)有相似:
- 前端 = content script(WebView 中)
- Rust 后端 = background(权限控制)
- IPC = message passing

## 和其他概念的关系

Tauri 是 [[微服务]] 架构思想在桌面应用的体现——前端 / 后端分离,通过 IPC 协议通信。它与 [[Electron]]、[[Flutter]] Desktop、[[SwiftUI]] for macOS 共同构成桌面应用开发选项。

它使用的 [[Rust所有权]] 系统让"桌面应用 + 系统调用"安全大幅提升,与 [[Web安全]] / [[OWASP Top 10]] 关注的桌面端安全问题(如恶意更新、命令注入)契合。

Tauri 体现的"用现成基础设施(系统 WebView)而非自建"哲学,与 [[Linkerd]] 用现成 Tokio 而非自研运行时同源——避免重新发明轮子,聚焦差异化价值。

## 参考源

- raw/计算机/
- 相关:[[Rust所有权]]、[[Electron]]、[[Flutter]]
