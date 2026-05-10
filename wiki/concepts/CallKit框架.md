---
title: CallKit 框架
type: concept
tags: [ios, mature]
sources: [raw/iPhone/]
created: 2026-05-05
updated: 2026-05-05
summary: CallKit 是 iOS 10 引入的 VoIP 通话集成框架,让第三方通话 App(如微信、WhatsApp)能使用系统原生来电界面、与电话 App 无缝合作,并通过 Call Directory 扩展实现陌生号码识别与拦截。
---

# CallKit 框架

## 定义

CallKit 是 iOS 10 引入的**VoIP 通话集成框架**,提供两类能力:(1)让第三方 VoIP App 调用系统原生来电界面而非自绘弹窗;(2)通过 **Call Directory Extension** 让第三方 App 提供陌生号码识别(垃圾电话标记)与拦截清单。它把"通话"提升为系统级一等公民,告别 App 内部各自实现来电 UI 的混乱。

## 核心要点

**CallKit 解决的痛点**

iOS 10 之前,VoIP App 收到来电时:
- 必须自绘界面(在锁屏推送 + App 内全屏接听界面)
- 无法在锁屏直接接听 / 拒接
- 无法与系统电话 App 共享通话历史
- 用户感知与电话 App 完全不同

CallKit 把上述能力开放给第三方,实现**与原生电话同等体验**。

**两大能力分支**

1. **VoIP Calls(通话集成)**:让 App 调用系统来电 UI
2. **Call Directory(号码识别 / 拦截)**:让 App 在系统电话识别陌生号

**VoIP 通话集成的核心 API**

- `CXProvider`:声明 App 提供的通话能力(支持视频?支持多方?)
- `CXCallController`:发起 / 结束 / 静音通话
- `CXCallUpdate`:通知系统来电信息(主叫、号码、是否视频)

通话流程:
1. 收到 VoIP 推送(PushKit)
2. 创建 `CXCallUpdate` 报告来电
3. 系统弹出原生来电界面(全屏锁屏或横幅)
4. 用户接听 / 拒接 → 触发 `CXAction`,App 处理
5. 通话期间出现在通话历史

**Call Directory Extension(号码识别)**

第三方 App(如腾讯手机管家、Truecaller)可:
- 提供"已知号码标识符"(垃圾电话、推销、外卖)
- 提供"拦截号码列表"
- 系统在来电时查询所有已启用扩展,显示标识或拦截

实现:Call Directory 扩展进程在系统调度时返回数据,系统缓存。用户在 *设置 > 电话 > 来电阻止与身份识别* 启用各扩展。

**与 PushKit 的关系**

CallKit 处理 UI,**PushKit** 处理 VoIP 推送。VoIP App 必须用 PushKit 接收高优先级推送(比普通 APNs 推送有更短延迟、更可靠唤起),然后再调用 CallKit 报告来电。iOS 13 起 VoIP 推送收到必须立刻调用 CallKit,否则 App 会被杀进程。

**隐私与限制**

- Call Directory 扩展不能联网查询(数据必须预先生成)
- 扩展进程时间和内存预算极有限(几十 MB)
- iOS 12 起,中国大陆地区 CallKit 受限(运营商规定),App 必须自绘 UI
- 全球其他地区无此限制

## 与其他概念的关系

CallKit 是 [[iOS应用扩展]] 体系中的特殊扩展点,与 [[APNs推送通知]] / PushKit 深度配合。它体现了 [[Apple生态系统]] 把"系统功能逐步开放给第三方"的策略,与 [[Siri与Apple Intelligence]]、[[HealthKit生态]]、[[HomeKit智能家居]] 同属"系统能力开放"系列。

## 高频陷阱

- iOS 13+ VoIP 推送收到必须 30 秒内调用 CallKit `reportNewIncomingCall`,否则进程被杀且推送权被吊销
- Call Directory 在中国大陆区不可用 VoIP 集成功能
- 同一用户启用多个号码识别扩展时,标签可能冲突,系统按优先级合并
- VoIP 通话历史会出现在系统电话 App 中,用户隐私意识者可能反感

## 参考源

- raw/iPhone/(CallKit 章节)
- 相关:[[iOS应用扩展]]、[[APNs推送通知]]、[[Apple生态系统]]、[[iOS隐私机制]]
