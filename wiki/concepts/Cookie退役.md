---
title: Cookie退役
type: concept
tags: [marketing, 数字营销, 隐私, 数据采集, mature]
sources: [raw/数字营销/04-高级实践层/04-合规与隐私/]
created: 2026-05-05
updated: 2026-05-05
summary: 第三方 Cookie 退役指浏览器逐步阻止跨站点 Cookie 的进程,Safari ITP(2017)Firefox(2019)Chrome(2024 完成);它瓦解了过去 20 年数字广告的跨站追踪基础,推动 Server-side Tracking、CAPI、第一方数据、上下文广告的回归。
---

# Cookie 退役

## 定义

**Cookie 退役(Cookie Deprecation)** 特指 **第三方 Cookie**(Third-Party Cookies)在主流浏览器中被逐步阻止的全过程。第三方 Cookie 是指 **由用户当前访问域之外的域设置的 Cookie**——这是过去 20 年实现 [[再营销]]、跨站追踪、广告归因的技术基础。

时间线:
- **2017**:Apple Safari ITP(Intelligent Tracking Prevention)首批限制
- **2019**:Firefox ETP 默认阻止
- **2020**:Chrome 宣布 2022 年退役计划
- **2022-2024**:Chrome 多次推迟,渐进式淘汰
- **2024**:Chrome 1% 用户先关闭
- **2025+**:仍有过渡期,Privacy Sandbox 提供替代

它是 [[隐私优先时代]] 最具影响力的技术变革,瓦解了 [[DSP需求方平台]]、[[DMP数据管理平台]]、[[Ad Exchange广告交易市场]] 等程序化广告生态的核心信号源。

## 核心要点

### 1. 第一方 vs 第三方 Cookie

| 维度 | 第一方 | 第三方 |
|---|---|---|
| **设置者** | 用户访问域 | 用户访问域之外 |
| **典型用途** | 登录、偏好、购物车 | 广告、跨站追踪、归因 |
| **是否被禁** | 否 | **是** |
| **隐私影响** | 低 | 高 |

仅 **第三方** 被退役,第一方 Cookie 仍正常工作。

### 2. Cookie 退役影响的具体能力

#### 失效或大幅缩水
- 跨站重定向追踪
- 跨站 Look-alike 扩展
- 跨站频次控制
- 跨平台归因(用户在 A 站看广告 → B 站买)
- 广告生态的 [[DMP数据管理平台]] 商业模式

#### 不影响
- 同站登录状态
- 第一方分析(GA4 自有域)
- 服务器端事件采集([[Server-side Tracking]])
- 上下文广告(基于页面内容而非用户身份)

### 3. Apple ITP 的渐进式打击(2017-至今)

| 版本 | 限制 |
|---|---|
| **ITP 1.0(2017)** | 24 小时未访问后第三方 Cookie 失效 |
| **ITP 2.0(2018)** | 第三方 Cookie 默认完全阻止 |
| **ITP 2.1(2019)** | document.cookie 设置的 Cookie 限 7 天 |
| **ITP 2.2(2019)** | 来自社交追踪的 Cookie 限 1 天 |
| **ITP 2.3-2.5(2019-2020)** | 进一步限制 link decoration、IP 跨站追踪 |
| **CNAME 伪装也限制(2020)** | 假装第一方但其实第三方的把戏被破解 |

Safari 已经基本是"无第三方 Cookie 浏览器",这与 iOS [[ATT隐私框架]] 形成的双重打击使移动端广告归因极差。

### 4. Chrome Privacy Sandbox(替代方案)

Google 提出的整套替代框架:

| API | 用途 | 状态 |
|---|---|---|
| **Topics API** | 浏览器本地分类用户兴趣 | 测试中 |
| **Protected Audience(原 FLEDGE)** | 浏览器内本地竞价,实现再营销 | 测试中 |
| **Attribution Reporting** | 隐私化转化归因 | 测试中 |
| **Trust Tokens** | 反欺诈 | |
| **First-Party Sets** | 跨域第一方共享 | |
| **Fenced Frames** | 隔离嵌入框架 | |

理论上替代部分功能,实操中精度损失大,且行业普遍认为 Google 借此巩固自己的优势。

### 5. 行业的应对策略

#### a) 服务器端追踪
[[Server-side Tracking]]、[[Google Tag Manager]] Server Container、Meta CAPI 等绕过浏览器限制。

#### b) 第一方数据建设
[[CDP客户数据平台]] 建设、登录态扩展、激励登录、邮件捕获——重新积累自有数据。

#### c) 上下文广告复兴
基于页面内容而非用户身份做定向。GroupM 估计 2025 年上下文广告市场增长 13%。

#### d) 数据洁净室(Data Clean Room)
Google Ads Data Hub、Meta Advanced Analytics、AWS Clean Rooms——跨方数据计算但不暴露原始数据。

#### e) Identity Resolution
LiveRamp ATS 等基于哈希邮箱的可持续 ID,需要用户登录或同意。

#### f) Marketing Mix Modeling 复兴
[[Marketing Mix Modeling]] 因不依赖个人数据,在 Cookie 退役后重新流行。

#### g) 内容与 SEO 价值上升
不依赖追踪的渠道(SEO、品牌、内容)价值提升。

### 6. 实施时间表(2025+)

```
2025 Q1: Chrome 1% 用户开启
2025 Q3: Chrome 50% 用户开启(待定)
2026: 完全退役(预期但仍有可能推迟)
```

Chrome 多次推迟反映出广告生态调整困难,可能再延期。

## 与其他概念的关系

- **核心相关**:[[隐私优先时代]] / [[ATT隐私框架]] / [[GDPR]] / [[CCPA]]
- **应对方案**:[[Server-side Tracking]] / [[转化API]] / [[CDP客户数据平台]] / [[Marketing Mix Modeling]]
- **生态影响**:[[DSP需求方平台]] / [[SSP供应方平台]] / [[DMP数据管理平台]] / [[Ad Exchange广告交易市场]] / [[再营销]] / [[多触点归因]]
- **跨域**:[[第一方数据]] / [[隐私沙箱]] / [[GA4配置]]

## 行业影响

### 谁是赢家
- 拥有大量第一方数据的平台(Google 自身、Meta、Amazon)
- 第一方数据基础好的品牌(订阅制、零售、电商)
- 上下文广告平台
- MMM 与因果推断咨询

### 谁是输家
- 第三方数据公司(Acxiom、LiveRamp 部分业务)
- 中小广告主(没第一方数据无法精准)
- 重度依赖跨站追踪的电商
- 部分独立 DSP/SSP

## 当代演进

- **2024 年 Chrome 推迟全面退役**:行业准备不足
- **AI Overviews 与 Cookie 退役并行**:双重打击数字营销现状
- **零方数据(Zero-Party Data)兴起**:用户主动给的偏好数据
- **登录墙(Wall of Login)**:迫使用户登录获得追踪同意
- **EU/US 法规博弈**:Cookie 同意横幅(CMP)疲劳推动新框架

## 参考源

- raw/数字营销/04-高级实践层/04-合规与隐私/
- 关联:[[隐私优先时代]] / [[ATT隐私框架]] / [[Server-side Tracking]] / [[转化API]] / [[Marketing Mix Modeling]]
