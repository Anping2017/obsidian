---
title: TestFlight
type: concept
tags: [iphone, ios, programming, mature]
sources: [raw/iPhone/iPhone知识体系/]
created: 2026-05-05
updated: 2026-05-05
summary: TestFlight 是 Apple 官方的 iOS 应用 Beta 测试分发平台,支持上传开发版应用并邀请最多 10000 名外部测试者,绕过 App Store 严格审核但仍受 90 天有效期限制。
---

# TestFlight

## 定义

TestFlight 是 Apple 官方的 iOS、iPadOS、macOS、watchOS、tvOS、visionOS 应用 Beta 测试分发平台。开发者从 [[Xcode开发工具]] Archive 上传应用后,通过 App Store Connect 配置 TestFlight,邀请测试者通过专用 TestFlight App 安装、试用、反馈。

TestFlight 在 Apple 生态中地位特殊:它是普通用户唯一合法的、不越狱的"提前用上未发布版本"的渠道。

## 历史

**TestFlight Inc.(2010-2014)**

独立公司,提供跨平台移动应用 Beta 测试服务。

**Apple 收购(2014)**

Apple 收购后停止安卓支持,整合到 App Store Connect,变成 iOS 唯一官方测试分发渠道。原先广泛使用的 Ad-Hoc(基于 UDID 列表)分发被推到边缘。

## 测试组类型

**Internal Testing(内部测试)**

- 限 100 人,必须是开发账号下的成员
- 上传 build 后立即可用,无需 Apple 审核
- 适合公司内 QA 团队、设计师、PM

**External Testing(外部测试)**

- 限 10000 人,可任意邮箱邀请
- 首次提交需 Apple Beta App Review(轻量审核,通常 24-48 小时)
- 后续 build 仅在重大变更时审核
- 适合公开 Beta、用户社区抢鲜测试

## 关键限制

**Build 90 天有效期**

每个 build 上传后 90 天后自动过期,测试者无法再启动 App。这是 Apple 防止 TestFlight 被滥用为长期分发(绕开 App Store)的核心机制。

**邀请方式**

- 公开链接(测试者点击链接进入)
- 邮箱邀请(测试者收到 Apple 邮件)
- 公开链接需 Apple 审核;邮箱邀请直接发出

**反馈机制**

- 测试者可在 TestFlight App 内截图反馈
- 反馈直接到 App Store Connect
- 崩溃日志自动收集

**数据分析**

- TestFlight 中 build 安装数、启动数、平均会话时长
- 但不如 Firebase、Mixpanel 等专业分析工具详细

## 工作流

**典型流程**

1. Xcode 中 Archive
2. 上传到 App Store Connect
3. 进入 TestFlight 标签页
4. 选择 build,配置测试组、添加测试者
5. 外部测试需提交 Beta App Review(填写测试目的、登录账号等)
6. 审核通过后测试者收到邮件 / 公开链接
7. 测试者下载 TestFlight App,接受邀请,安装

**App 内更新**

新 build 上传后,TestFlight App 提示已有测试者更新。

## 在产品策略中的角色

**Beta 用户社区建设**

- 公开 TestFlight 链接是开发者经营忠实用户的重要工具
- 用户因获得"提前体验"产生归属感
- 反馈直接进入产品迭代

**渐进发布**

某些应用在公开 App Store 前,先在 TestFlight 收集 1-2 月数据,再决定上线 App Store。

**A/B 实验**

部分团队把不同 TestFlight 组用于不同实验分支,但比起 Firebase Remote Config 等专业方案不够灵活。

## 与企业内部分发的对比

| 渠道 | 用户上限 | 审核 | 时长 | 用途 |
|---|---|---|---|---|
| App Store | ∞ | 标准 | 永久 | 公开发布 |
| TestFlight 内部 | 100 | 无 | 90 天 | 团队 |
| TestFlight 外部 | 10000 | Beta Review | 90 天 | Beta 用户 |
| Apple Enterprise(In-House) | 公司内 | 无 | 1 年(证书) | 公司内 App |
| Ad-Hoc(已淘汰) | 100 UDID | 无 | 1 年(证书) | 已不推荐 |

## 限制突破的尝试

**侧载与 AltStore**

部分用户用 AltStore 等工具在不通过 App Store / TestFlight 的情况下安装 App。技术上利用 Apple 个人开发者账号的 7 天证书,需每周重新签名。EU DMA 法规推动下,Apple 在欧盟开放第三方应用商店,部分缓解此限制。

## 参考源

- raw/iPhone/iPhone知识体系/
- 相关:[[Xcode开发工具]]、[[App Store 审核]]、[[侧载]]
