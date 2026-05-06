---
title: PWA 渐进式 Web 应用
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/语言/HTML/04-知识拓展层/现代Web平台/04-9 PWA中的HTML.md]
created: 2026-05-05
updated: 2026-05-05
summary: PWA 通过 Web App Manifest、Service Worker、HTTPS 三大支柱让 Web 站点获得离线、安装、推送等原生应用体验,模糊 Web 与 App 的边界。
---

# PWA 渐进式 Web 应用

## 定义

**PWA(Progressive Web App)** 是 Google 2015 年提出的概念,让 Web 站点通过一组现代浏览器 API 获得**接近原生应用**的体验:可安装到主屏、离线工作、后台推送、本地存储、全屏运行。"Progressive"指渐进增强 —— 不支持的浏览器仍能用基础 Web 功能。

## 核心要点

### 1. 三大支柱

| 支柱 | 作用 |
|---|---|
| **Web App Manifest** | 安装元信息(名称、图标、主题色) |
| **Service Worker** | 离线缓存 + 推送 + 后台同步 |
| **HTTPS** | 安全上下文,Service Worker 强制 |

### 2. Web App Manifest

```json
{
  "name": "MyApp",
  "short_name": "App",
  "start_url": "/",
  "display": "standalone",
  "icons": [{ "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }],
  "theme_color": "#4f46e5",
  "background_color": "#ffffff"
}
```

通过 `<link rel="manifest" href="/manifest.json">` 引入。浏览器据此提供"添加到主屏"体验,iOS Safari 同样支持。

### 3. Service Worker

详见 [[Service Worker]]。它是 PWA 的引擎,实现离线策略、推送通知、后台同步。

### 4. 安装体验

- **Android Chrome**:满足条件后展示"添加到主屏"横幅,安装后行为如原生 App
- **桌面 Chrome/Edge**:地址栏右侧出现安装图标,装入应用列表
- **iOS Safari**:必须用户主动选"添加到主屏",有更多限制(历史上 PWA 在 iOS 体验弱于 Android,iOS 17.4 EU 版甚至一度移除 PWA 支持)

### 5. 推送通知

```js
const sub = await registration.pushManager.subscribe({
  userVisibleOnly: true,
  applicationServerKey: vapidKey
});
// 后端发推送,Service Worker 接收 push 事件
```

不需打开 App 也能推送,与原生通知集成。iOS 16.4 起支持 Web Push(需先安装到主屏)。

### 6. 离线策略(由 Service Worker 实现)

- **Cache First**:静态资源(CSS、JS、图标)
- **Network First**:HTML、API 调用
- **Stale While Revalidate**:回旧版立即响应,后台更新
- **Cache Only / Network Only**:特殊场景

工具:Workbox(Google 官方库)、vite-plugin-pwa。

### 7. PWA 优势

- 一份代码,多端运行(浏览器 + 桌面 + 移动主屏)
- 无需通过应用商店分发(避 30% 抽成)
- 即时更新,无审核延迟
- SEO 仍受益(本身是 Web)

### 8. PWA 劣势

- iOS 限制多(后台、推送、安装入口)
- 平台原生能力部分缺失(蓝牙、NFC、原生支付有限)
- 性能不如完全原生(对游戏等高要求)

### 9. 商店化趋势

- Microsoft Store 接收 PWA 直接上架
- Google Play 通过 Trusted Web Activity 包装 PWA
- iOS 不允许商店上架 PWA

### 10. 案例

- Twitter Lite、Pinterest、Starbucks、Trivago 用 PWA 大幅降流量、提转化
- Notion、Slack、Discord、Spotify 桌面"应用"实际是 PWA / Electron

## 关系

- 核心:[[Service Worker]]、Manifest、HTTPS
- 缓存:[[IndexedDB]] 持久化大数据
- 性能:[[Core Web Vitals]] 基础
- 替代:Cordova、Hybrid App
- 对比:Electron(桌面)、React Native(移动)

## 参考源

- raw/计算机/开发学习/语言/HTML/04-知识拓展层/现代Web平台/04-9 PWA中的HTML.md
