---
title: SharePlay 同播共享
type: concept
tags: [ios, mature]
sources: [raw/iPhone/]
created: 2026-05-05
updated: 2026-05-05
summary: SharePlay 是 iOS 15 引入的 FaceTime 同播共享框架,让多人通话时同步观看视频、听音乐、看屏幕、玩游戏,是 Apple 在疫情后对"远程共在"场景的系统级响应。
---

# SharePlay 同播共享

## 定义

SharePlay 是 Apple 在 iOS 15 / iPadOS 15 / tvOS 15 / macOS Monterey 推出的**FaceTime 内同播共享**功能,让通话中的多人**同步观看视频、聆听音乐、查看屏幕、协作玩游戏**。所有参与者的播放进度自动对齐,任意一方暂停 / 快进所有人同步,语音通话与播放并行不打扰。

## 核心要点

**支持的内容形态**

1. **视频流**:Disney+、Hulu、HBO Max、Paramount+、ESPN+、Apple TV+ 等
2. **音乐**:Apple Music(同步播放列表 / 队列)
3. **屏幕共享**:把整个 iPhone / iPad 屏幕投到通话中
4. **游戏 / App**:第三方 App 通过 GroupActivities 框架接入(如健身、画画)
5. **教育互动**:演示文稿、白板

**用户体验**

1. 在 FaceTime 通话中切到某 App(如 Apple TV+)
2. 选择内容播放,App 检测到 FaceTime 活跃 → 弹"为大家播放?"
3. 所有参与者收到通知,可选择跟随
4. 进度条全员同步,任一方暂停 / 倒带 / 切集均同步
5. 实时语音 / 视频通话叠加在内容旁

**技术机制**

- 基于 **GroupActivities** 框架
- App 声明一个 `GroupActivity` 对象(类型 + 元数据)
- FaceTime 把 GroupActivity 序列化并通过 iCloud 中继分发到所有参与者
- 各端 App 收到 GroupActivity 后启动同步会话(通常通过 Combine 发布订阅协调进度)

**版权与授权**

- 内容版权方需各自实现 SharePlay 接入
- 用户必须各自有内容订阅(SharePlay 不绕开版权:看 Disney+ 大家都得有 Disney+ 账户)
- 例外:某些 App 提供"主持人共享"模式,只需主持人有订阅

**跨平台支持**

- iOS / iPadOS / tvOS:原生
- macOS:原生(Monterey+)
- visionOS:Apple Vision Pro 的核心远程协作场景
- Android:不支持

**iOS 16 增强**

- 锁屏小组件显示当前 SharePlay
- 第三方 App 可通过控件让用户随时启动 SharePlay
- 支持 messages 而非仅 FaceTime 启动 SharePlay

## 与其他概念的关系

SharePlay 是 [[Apple生态系统]] 在"远程协作"场景的代表,与 [[CallKit框架]] 通话能力、[[iOS应用扩展]] 共同构成 iOS 系统级互动栈。它高度依赖 [[iCloud云服务]] 中继。Vision Pro 平台让其延伸到 [[家人共享]] 与商务协作。

## 高频陷阱

- 内容订阅各自需要(误以为可"白嫖"主持人订阅)
- 同步漂移:网络抖动时进度短暂不一致,App 需重新对齐逻辑
- 不是所有 App 都支持,需开发者集成 GroupActivities
- 中国大陆 FaceTime 的 SharePlay 部分内容服务受地区限制

## 参考源

- raw/iPhone/(SharePlay 章节)
- 相关:[[Apple生态系统]]、[[iOS应用扩展]]、[[CallKit框架]]、[[家人共享]]
