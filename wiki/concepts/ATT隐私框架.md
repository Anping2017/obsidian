---
title: ATT 隐私框架
type: concept
tags: [ios, privacy, stub]
sources: []
created: 2026-05-05
updated: 2026-05-05
summary: App Tracking Transparency,iOS 14.5 起引入的强制 App 显式申请跨 App 追踪用户授权的机制,显著重塑了移动广告与营销生态。
---

# ATT 隐私框架

## 定义

**ATT**(App Tracking Transparency)是 Apple 在 2021 年 4 月随 iOS 14.5 引入的**强制隐私授权机制**,要求所有 App 在跨 App 或跨网站追踪用户(包括获取 IDFA)前,必须先弹窗向用户申请明确授权。该框架是 [[iOS隐私机制]] 的核心更新之一,直接重塑了全球移动广告、归因、营销技术生态,被 Meta(Facebook)等广告平台视为重大冲击。

## 核心要点

### 工作机制

- **IDFA**(Identifier for Advertisers):iOS 设备上跨 App 共享的广告标识符
- 在 ATT 之前,App 默认可读取 IDFA 用于追踪和归因
- ATT 后,任何想读取 IDFA 或跨 App/网站追踪的 App,必须先调用 `requestTrackingAuthorization` API
- 系统弹出 Apple 标准化弹窗,用户选择"允许"或"要求 App 不要追踪"
- 拒绝后,IDFA 全 0,广告归因丢失链路

### 用户体验

- 弹窗文字 Apple 严格审核,不允许诱导
- 只能问一次,被拒就不能再问(除非用户在系统设置主动开启)
- App 可在设置中提供"什么是追踪"教育
- 系统设置中可全局关闭"允许 App 请求追踪"

### 行业影响

**对开发者与广告商**:
- Meta 公开估算 2022 年因 ATT 损失约 100 亿美元收入
- 广告归因从精准重建为概率建模(Probabilistic Attribution)
- 上下文广告、SKAdNetwork(Apple 提供的隐私保护归因)兴起
- 营销 KPI 体系更看重首方数据与品牌效果

**对 Apple**:
- 强化"隐私即产品"叙事,差异化竞争对手
- 同时被批评:Apple 自家广告不受同样限制(反垄断诉讼焦点)

**对用户**:
- 有限度的隐私感知改善
- 跨 App 个性化广告减少,但 App 内广告仍然存在

### 技术细节

- 与 [[iOS隐私机制]] 中的"App 隐私清单"配套使用
- 与 SKAdNetwork(后续 SKAN 4.0)共同提供新的归因方案
- 与 [[App Store 审核]] 联动:违反 ATT 的 App 会被拒绝或下架

## 和其他概念的关系

- 是 [[iOS隐私机制]] 在 14.5 之后的核心更新
- 与 [[App Store 审核]] 一起构成隐私规则的执行机制
- 直接影响所有依赖广告归因的 App 与 SDK 生态
- 是 Apple [[Apple生态系统]] "隐私即护城河"战略的标志性政策
- 与欧盟 GDPR、加州 CCPA 的隐私潮流共同推动行业变革

## 参考源

待补充(领域:移动隐私、数字广告)
