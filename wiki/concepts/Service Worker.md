---
title: Service Worker
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/语言/HTML/04-知识拓展层/]
created: 2026-05-05
updated: 2026-05-05
summary: Service Worker 是浏览器后台运行的脚本代理,可拦截网络请求、缓存响应、推送通知、后台同步,是 PWA 与离线 Web 应用的核心引擎。
---

# Service Worker

## 定义

**Service Worker(SW)** 是浏览器在主线程之外、**与页面分离**运行的脚本。它充当**网页与网络之间的代理**,可拦截 fetch 请求并自定义响应(从缓存、网络或合成)。Service Worker 是 [[PWA]]、离线 Web、推送通知、后台同步的核心引擎,2014 年由 Google Chrome 团队推动标准化。

## 核心要点

### 1. 生命周期

```
register → install → waiting → activate → idle ↔ active(fetch/message)
                                     ↓
                                   redundant
```

```js
// 注册(在页面)
navigator.serviceWorker.register('/sw.js');

// install(在 sw.js)
self.addEventListener('install', (e) => {
  e.waitUntil(caches.open('v1').then(c => c.addAll(['/','/app.js'])));
});

// activate
self.addEventListener('activate', (e) => {
  // 清理旧缓存
});

// fetch
self.addEventListener('fetch', (e) => {
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));
});
```

### 2. 限制

- 必须 HTTPS(localhost 例外)
- 不能访问 DOM(独立线程)
- 异步 API 全部 Promise
- 作用域受脚本路径限制(`/sw.js` 默认管整站,`/foo/sw.js` 只管 /foo/*)
- 浏览器可能在闲置时回收

### 3. 缓存策略

#### Cache First(静态资源)

```js
caches.match(req).then(c => c || fetch(req));
```

#### Network First(API)

```js
fetch(req).catch(() => caches.match(req));
```

#### Stale While Revalidate(平衡)

```js
caches.match(req).then(c => {
  const network = fetch(req).then(r => {
    cache.put(req, r.clone());
    return r;
  });
  return c || network;
});
```

工具库 **Workbox**(Google 维护)封装策略,大幅降低样板代码。

### 4. Push 通知

```js
self.addEventListener('push', (e) => {
  const { title, body } = e.data.json();
  e.waitUntil(self.registration.showNotification(title, { body }));
});
```

配合 VAPID + 推送服务器(FCM、自建)。

### 5. Background Sync

```js
// 页面
const reg = await navigator.serviceWorker.ready;
await reg.sync.register('post-comments');

// sw.js
self.addEventListener('sync', (e) => {
  if (e.tag === 'post-comments') e.waitUntil(uploadPending());
});
```

网络断开时缓存意图,网络恢复后自动重试。

### 6. Periodic Background Sync

定期唤醒(如新闻应用每天更新)。需要用户主动安装并授权。

### 7. SW 与 [[PWA]] 关系

PWA = Manifest + Service Worker + HTTPS。SW 提供:

- 离线访问(关键 PWA 能力)
- 推送通知
- 后台同步
- 自定义离线页

### 8. 调试

Chrome DevTools → Application → Service Workers:

- 强制刷新(skip waiting)
- 查看缓存
- 模拟离线
- 卸载 SW

### 9. 安全考量

SW 一旦注册,会持续控制其作用域内所有页面,有效到主动注销或浏览器清理。**注入恶意 SW 是严重攻击**,因此:

- HTTPS 强制
- 同源限制
- 注册需用户行为或脚本主动调用

### 10. 替代角色

- **Web Worker**:后台计算,无网络代理能力
- **Shared Worker**:跨标签页共享,但无 fetch 拦截
- **Service Worker**:专司网络代理 + 离线 + 推送

## 关系

- 引擎:[[PWA]] 核心
- 配合:[[IndexedDB]] 存大数据
- 拦截:[[HTTP协议]] fetch
- 工具:Workbox、vite-plugin-pwa
- 对比:Web Worker / Shared Worker

## 参考源

- raw/计算机/开发学习/语言/HTML/04-知识拓展层/现代Web平台/04-9 PWA中的HTML.md
