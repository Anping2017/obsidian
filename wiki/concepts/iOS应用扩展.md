---
title: iOS 应用扩展
type: concept
tags: [ios, mature]
sources: [raw/iPhone/]
created: 2026-05-05
updated: 2026-05-05
summary: 应用扩展(App Extensions)是 iOS 8 引入的跨应用代码注入机制,允许第三方 App 在分享菜单、键盘、通知中心、相机、Today 小组件等系统位置以宿主权限运行,是 iOS 最深度的开放接口。
---

# iOS 应用扩展

## 定义

应用扩展(App Extensions)是 iOS 8 引入的**跨应用代码注入机制**,允许第三方 App 在系统或宿主 App 的特定"扩展点"中以受限权限运行自定义代码。它打破了 iOS 严格的沙盒隔离,让 App 之间能"借用对方的执行上下文",是除了 URL Scheme / Universal Link 外最重要的 iOS 开放接口。

## 核心要点

**扩展点的种类**

iOS 提供数十种扩展点,常见的有:
1. **Share Extension**(分享):在系统分享菜单出现自定义条目
2. **Action Extension**(操作):对当前内容执行自定义操作
3. **Today Extension / Widget**(小组件):锁屏 / 主屏 / 通知中心展示信息
4. **Custom Keyboard**(自定义键盘):取代系统键盘
5. **Photo Editing**(图片编辑):嵌入照片 App
6. **Document Provider**(文档提供者):为其他 App 提供云文件
7. **Notification Service / Content**(通知扩展):修改富通知
8. **Sticker Pack / iMessage App**(iMessage 扩展)
9. **CallKit / Call Directory**(来电拦截、识别)
10. **WatchKit**(Apple Watch App 扩展)
11. **SiriKit(Intents)**:把 App 功能暴露给 Siri / 快捷指令
12. **Network Extension**(VPN / 内容过滤)

**扩展进程模型**

- 扩展运行在**独立进程**中,与宿主 App、宿主进程隔离
- 宿主 App 不一定要在前台运行(扩展是独立进程)
- 扩展进程内存与时间预算严格(通常 16-120 MB,几秒-几十秒生命期)
- 扩展不能后台一直存活,被系统调度

**与容器 App 的关系**

每个扩展必须**绑定一个容器 App**(Containing App),不能独立分发到 App Store:
- 用户必须先安装容器 App
- 扩展通过 **App Group**(共享容器)与父 App 共享 UserDefaults / 文件
- App Group ID 形如 `group.com.example.shared`

**通讯机制**

扩展与宿主进程之间:
- **Extension Context**:宿主把当前选中内容(URL、文本、图片)传给扩展
- **请求-响应**:扩展处理后调用 `completeRequest(returningItems:)`
- **App Group 共享存储**:跨进程读写小数据 / 文件
- **NSExtensionContext.open(_:completionHandler:)**:打开容器 App

**权限与隐私**

- 扩展继承容器 App 的权限声明,但每个扩展点的可用 API 受限
- Custom Keyboard 默认无网络权限(需用户在设置允许"完全访问")
- Photo Editing 只能读传入的照片,不能扫整个相册
- iOS 14 起所有扩展都受 ATT(App Tracking Transparency)管控

**性能预算**

扩展严格受限:
- 内存:超出立即被杀(典型 30-120 MB,扩展点不同)
- 时间:Today 扩展限 5 秒响应、Share 扩展限几十秒
- 不能在扩展进程内后台运行长任务,需把任务交给容器 App

## 与其他概念的关系

应用扩展是 [[iOS沙盒]] 严格隔离下的"白名单开放"机制,在 [[iOS后台执行]] 之外提供另一种跨应用协作能力。它构成 [[Siri与Apple Intelligence]] 的能力基础(SiriKit Intents 即扩展)。WidgetKit 是其现代化继任者。

## 高频陷阱

- 扩展 = 独立进程,代码不能直接 import 容器 App 的类(需共享框架)
- App Group 必须 main App 与扩展都启用并用同一 ID
- 自定义键盘的"完全访问"模式默认关闭,需用户主动开启
- Today 小组件已被 WidgetKit 取代(iOS 14+)
- 扩展不能弹 UIAlertController 风格弹窗(只能在自身 UI 内提示)

## 参考源

- raw/iPhone/(扩展章节)
- 相关:[[iOS沙盒]]、[[iOS后台执行]]、[[Siri与Apple Intelligence]]、[[Xcode开发工具]]
