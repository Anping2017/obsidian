---
title: SiriKit 与 Intents
type: concept
tags: [ios, mature]
sources: [raw/iPhone/]
created: 2026-05-05
updated: 2026-05-05
summary: SiriKit 是 iOS 10 引入、通过 Intents 框架让第三方 App 把核心功能暴露给 Siri 与快捷指令的桥梁,iOS 16 后由 App Intents 框架现代化重写,是 Apple Intelligence 时代连接 App 与 LLM 的基础设施。
---

# SiriKit 与 Intents

## 定义

**SiriKit** 是 Apple 在 iOS 10 引入的、让第三方 App **把功能暴露给 Siri** 的开放框架。其核心是 **Intents**——一组语义化的"用户意图"(发消息、订餐、叫车、转账、播放音乐等),App 实现对应 Intent 后,用户用语音说出相关请求时 Siri 可调用 App。iOS 16 推出 **App Intents** 全新框架,以 Swift-only / 声明式 API 替代旧的 SiriKit,成为 Apple Intelligence(2024+)与 LLM 集成 App 能力的基础。

## 核心要点

**Intents 的本质**

Intent = 一个**结构化的用户意图描述**:
- 域(Domain):messaging、payments、ride booking、workouts、media、car commands、visual codes
- 类型(Intent Type):SendMessage、StartCall、PayBill、PlayMedia 等
- 参数(Parameters):收件人、金额、媒体名称等

App 注册自己支持哪些 Intent,Siri / 快捷指令在用户请求时把语音 / 操作转为 Intent 对象传递给 App。

**SiriKit 三层职责**

1. **Resolution**(解析):App 检查 Intent 参数是否完整、合法,缺失则反问
2. **Confirmation**(确认):告诉 Siri 是否能执行(预算够吗?账户存在吗?)
3. **Handling**(执行):真正完成动作并返回结果

**典型 Intent 示例**

- *Hey Siri, send a WeChat message to Mom saying I'm on the way.*
- *Order an Uber to LAX.*
- *Pay my electricity bill.*
- *Start a 30-minute outdoor run with Strava.*

**App Intents(iOS 16+)的进化**

旧 SiriKit 的痛点:
- 必须用 Intents Extension(独立进程),开发体验差
- Domain 是固定列表,App 无法定义自定义域
- 需 Objective-C 写 .intentdefinition 文件

App Intents 新框架:
- **纯 Swift 声明式**:`struct OrderCoffeeIntent: AppIntent { ... }`
- **任意自定义意图**:不限于预定义 Domain
- **同时驱动 Siri、快捷指令、Spotlight、Focus 过滤、控制中心**
- iOS 17+ 集成 **Interactive Widgets**

**与 Apple Intelligence 的关系**

iOS 18 的 Apple Intelligence 让 Siri 能"跨 App 完成复杂任务",其核心机制是让 LLM 理解用户语义后调用 **App Intents** 注册的能力。开发者声明 App Intent 越丰富,App 越能被 Siri 智能编排。这是 SiriKit 的"涅槃重生"。

**与快捷指令的关系**

Intents 同时驱动**快捷指令** App:
- 用户可把若干 Intent 串联成自动化流程
- 例:点击 NFC 标签 → 关闭 Wi-Fi → 启动驾驶 Focus → 播放播客
- App 提供的 Intent 越细粒度,可组合空间越大

## 与其他概念的关系

SiriKit / App Intents 是 [[Siri与Apple Intelligence]] 的开发者侧入口,与 [[iOS应用扩展]] 同属"开放系统能力"序列。Apple Intelligence 时代的 LLM 调用 App 功能本质就是调用 App Intents,这把 [[CallKit框架]]、[[HealthKit生态]]、[[HomeKit智能家居]] 的开放范式推到极致。

## 高频陷阱

- 旧 SiriKit 不能自定义 Intent;新 App Intents 才能
- App Intents 需 Swift 项目,Objective-C 项目要桥接
- Intent 实现里不能阻塞主线程,Siri 等待时间有限
- 用户必须在系统设置允许 Siri 访问对应 App
- 中国大陆 Siri 部分 Intent 受限(支付、叫车等域)

## 参考源

- raw/iPhone/(SiriKit / App Intents 章节)
- 相关:[[Siri与Apple Intelligence]]、[[iOS应用扩展]]、[[CallKit框架]]、[[Apple生态系统]]
