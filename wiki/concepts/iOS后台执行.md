---
title: iOS 后台执行
type: concept
tags: [iphone, ios, programming, mature]
sources: [raw/iPhone/iPhone知识体系/]
created: 2026-05-05
updated: 2026-05-05
summary: iOS 严格限制 App 后台执行以保电池和性能,只允许特定声明的后台模式持续运行,其他 App 进入后台数秒后被冻结,后台体验依赖 APNs 推送和 Background Tasks 框架。
---

# iOS 后台执行

## 定义

iOS 后台执行(Background Execution)规则是 iOS 与 Android 在系统行为上最显著的差别之一。iOS 默认假设"App 进入后台 = 不需要继续运行",在数秒内冻结进程释放资源,严格保护电池和系统性能。开发者必须主动申请后台模式,且接受 Apple 的严格审核。

这一架构让 iPhone 长期保持"开 50 个 App 也不卡顿"的体验,但也带来"为什么我退出 App 后通知没了?"的常见困惑——答案:iOS 用 [[APNs推送通知]] 替代 App 自身后台轮询。

## 核心原则

**进入后台流程**

1. 用户上滑回桌面或切到其他 App
2. App 收到 applicationDidEnterBackground 回调
3. 系统给约 5-30 秒处理收尾(取决于设备和负载)
4. 之后 App 进入 Suspend(冻结状态),内存保留但 CPU 不调度
5. 系统内存紧张时,Suspend 的 App 可被强制 Terminate(终止)

**Terminated 后的复活方式**

- 用户重新切回 App
- 收到推送通知用户点击进入
- Background Refresh、Background Fetch 等系统调度

## 允许的后台模式(Background Modes)

App 在 Info.plist 声明 UIBackgroundModes 后,Apple 审核通过即可使用:

- **audio**:音频播放(音乐 App、播客 App)
- **location**:定位更新(地图、健身、外卖、共享车)
- **voip**:VoIP 通话(微信电话、WhatsApp Call、Teams)
- **fetch**:Background Fetch,系统后台调度刷新
- **remote-notification**:静默推送唤醒
- **bluetooth-central / bluetooth-peripheral**:蓝牙
- **external-accessory**:外置配件
- **processing**:Background Processing Tasks(iOS 13+)
- **CarPlay / NewsstandContent / 其他特殊用途**

每种模式都受严格约束:
- audio 必须真在播放音频
- location 必须真用定位(否则 App Store 拒绝)
- VoIP 必须真有通话(否则 iOS 13+ 限制 PushKit)

## Background Tasks 框架(iOS 13+)

为统一后台调度,iOS 13 引入 BGTaskScheduler:

**BGAppRefreshTask**

短任务(30 秒以内),用于轻量数据刷新。系统根据用户使用习惯智能调度。

**BGProcessingTask**

长任务(数分钟),要求设备充电、连 Wi-Fi、空闲。用于数据库索引、机器学习训练等。

**调度策略**

不保证执行时间,系统根据电量、网络、用户习惯综合决定。开发者必须在 8-13 秒内完成 BGAppRefresh 否则任务被终止。

## 静默推送(Silent Push)

Apple 提供 content-available: 1 的静默推送,可短暂唤醒被冻结/终止的 App,执行 30 秒以内的工作。常用于:
- 后台同步数据
- 拉取内容预存
- 触发标准通知(如 IM 消息合并显示)

但 Apple 限制:静默推送的发送频率受系统调控,过多会被静默丢弃。

## VoIP 推送(PushKit)

iOS 13 前 VoIP App 通过 PushKit 推送可绕过后台限制即时唤醒,广泛用于微信、WhatsApp 等。iOS 13+ Apple 限制 PushKit 必须在收到推送后立即报告 CallKit 来电,否则后续推送被拒——防止滥用 PushKit 当永久后台。

中国微信因这一变化做大量适配,小米、华为基于此推出"系统级推送"作国内替代方案。

## 与 Android 的对比

| 维度 | iOS | Android |
|---|---|---|
| 默认后台 | 严格冻结 | 较宽松,可后台运行 |
| 推送通道 | APNs(强制) | FCM(国外)/各厂商通道(国内) |
| Foreground Service | 无概念 | 存在,可申请前台运行 |
| 用户控制 | 仅显示电池占用 | 详细电池管理、强制停止 |
| 续航效果 | 整体优异 | 厂商差异大 |

## 与 Apple Watch / 健康设备协同

- 健身 App 在户外跑步时持续后台 GPS,但必须真显示导航或记录路线
- Apple Watch 测量健康数据由 watchOS 调度,iPhone 端 App 无需后台运行
- HealthKit 后台样本订阅(Sample Observer)允许 App 在新数据写入时被唤醒

## 局限与争议

- 部分用户体验受影响:聊天 App 不能"瞬时收消息"完全依赖推送
- 中国 IM/外卖/直播 App 大量"假音频后台"或"假定位后台"绕过限制,被 Apple 间歇性清扫
- 跨平台 App 在 iOS 体验差异显著(Telegram、QQ 等历史问题)

## 参考源

- raw/iPhone/iPhone知识体系/
- 相关:[[iOS沙盒]]、[[APNs推送通知]]、[[iOS隐私机制]]
