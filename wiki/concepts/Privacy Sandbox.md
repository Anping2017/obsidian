---
title: Privacy Sandbox
type: concept
tags: [marketing, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: Privacy Sandbox 是 Google 主导的浏览器级隐私保护与广告技术替代方案集合,目标是在弃用第三方 Cookie 的同时保留广告生态可运转,核心 API 包括 Topics、Protected Audience、Attribution Reporting 等。
---

# Privacy Sandbox

## 定义

**Privacy Sandbox** 是 Google 自 2019 年提出、由 Chrome 团队牵头推进的一组**浏览器级隐私保护技术与广告 API**,目的在于:

1. 弃用浏览器第三方 Cookie 与跨站跟踪能力
2. 同时提供受控的、聚合的、面向广告生态的替代 API
3. 让 Web 仍能维持以广告为主的免费内容商业模型

它不是单一技术,而是一组 API 与机制,覆盖兴趣定向、再营销、归因测量、防指纹、跨站访问控制等场景。设计哲学是"通过浏览器在客户端处理敏感数据,只把聚合/去标识化结果暴露给广告生态"。

## 核心要点

### 时间线

- 2019.08:Google 首次提出 Privacy Sandbox 概念
- 2020.01:宣布两年内弃用 Chrome 第三方 Cookie
- 2021–2024:多次推迟弃用计划(从 2022 → 2023 → 2024 → 2025)
- 2024.07:Google 宣布**不再单方面弃用**,改为"用户选择"机制
- 2025+:用户选择 + Privacy Sandbox API 共存,行业仍在适配

### 核心 API 一览

| API | 用途 | 替代什么 |
|---|---|---|
| **Topics API** | 浏览器本地推断用户 3–5 个兴趣主题,向广告主披露 | 跨站行为定向 |
| **Protected Audience(原 FLEDGE)** | 浏览器内运行再营销与自定义受众竞价 | 第三方 Cookie 再营销 |
| **Attribution Reporting** | 事件级延迟 + 噪声归因报告;聚合归因 | 第三方 Cookie 转化跟踪 |
| **Shared Storage** | 跨站存储但仅在受控环境读取 | 跨站状态共享 |
| **CHIPS(Cookies Having Independent Partitioned State)** | 按 Top-level Site 分区第三方 Cookie | 兼容存量第三方 Cookie 用例 |
| **First-Party Sets / Related Website Sets** | 同一组织多域名归为同一方 | 跨域单点登录、子品牌识别 |
| **Fenced Frames** | 加固 iframe,不允许跨边界数据流 | 不安全嵌入 |
| **User-Agent Client Hints** | 替代旧 UA 字符串,按需披露 | 浏览器指纹 |
| **Private State Tokens(原 Trust Tokens)** | 跨站反作弊、防机器人 | reCAPTCHA + Cookie |

### Topics API 详解

- 浏览器每周本地分析用户访问站点,从约 500 个主题分类中选出 5 个
- 用户访问广告站点时,浏览器随机披露 3 个主题(每个调用方一周一变)
- 5% 概率返回随机主题以增加噪声
- 主题与具体页面无关、不可被反推为用户身份

### Protected Audience 详解(原 FLEDGE)

- 替代再营销:用户在 A 站点被加入"兴趣组",信息存浏览器本地
- 用户访问 B 站点,浏览器内运行受控的 JavaScript Worklet 做出价决策
- 出价过程在"密室"里发生,各 DSP 看不到对方
- 中标结果通过 Fenced Frame 渲染,无法读取宿主页面数据

### Attribution Reporting 详解

两种归因:

- **Event-level reports**:转化事件含噪声,且延迟数小时到数天发送
- **Summary reports**:跨用户聚合到 Aggregation Service 后输出

替代了过去 1:1 精确的转化回传,广告主精度损失显著。

### Server-Side 与 Privacy Sandbox 的关系

- 服务器端事件(Meta CAPI、Google Enhanced Conversions、TikTok Events API)绕过浏览器侧 Cookie 限制,但 ATT、Privacy Sandbox 与 GDPR 同样限制服务器端可使用的标识符
- 趋势:**[[Server-Side Tracking]]** + **[[Data Clean Room]]** + Privacy Sandbox 三者结合

### 监管与反垄断博弈

- 欧盟 CMA 对 Privacy Sandbox 立案审查,担心 Google 滥用浏览器位置巩固广告优势
- Google 承诺"不在 Privacy Sandbox 之外使用替代标识符",并接受 CMA 监督
- IAB Tech Lab、Ad Tech 行业普遍认为 Privacy Sandbox 还不能完全替代第三方 Cookie

## 应用 / 工具

- **官方文档**:[privacysandbox.com](https://privacysandbox.com/)、Chrome Developer 文档
- **生态适配**:Prebid 6.x+(集成 Topics、Protected Audience)、Google Ad Manager、Magnite Demand Manager
- **测试工具**:Chrome DevTools Privacy Sandbox 面板、Origin Trial 注册
- **替代标识符**:UID 2.0(The Trade Desk)、RampID(LiveRamp)、ID5、Hadron ID
- **数据匹配**:AWS Clean Rooms、Habu、InfoSum、LiveRamp Clean Room

## 局限与陷阱

- **测量精度下降**:实测 [[ROAS]]、[[CPA]] 测量误差可达 20–40%
- **再营销效果衰减**:Protected Audience 不如旧 Cookie 再营销精准
- **小发行商劣势**:API 复杂、需要资金/技术接入,头部平台获益更大
- **Google 利益冲突**:既是浏览器拥有方,也是最大广告平台
- **跨浏览器不一致**:Safari、Firefox 早已自己的隐私方案,Privacy Sandbox 仅 Chrome
- **2024 政策反转**:不再强制弃用 Cookie,行业战略规划需重新评估
- **品牌主"假装合规"**:仍偷偷使用指纹与 Server-Side Cookie 绕过限制,有合规风险
- **服务器端不是万能解**:浏览器外标识符同样受 GDPR/CCPA 约束

## 与其他概念的关系

- 强烈影响 [[CPC]]、[[CPA]]、[[ROAS]] 的测量与出价机制
- 直接挑战 [[Header Bidding]] 的用户匹配链路,推动 S2S Header Bidding 与替代 ID
- 与 [[Generative Engine Optimization]] 间接关联 —— 精准定向衰减后,品牌曝光与权威建设更重要
- 影响 [[SEO]] —— Google 在隐私语境下进一步弱化第三方 Cookie 依赖的归因
- 与 [[CBBE模型]] / [[品牌资产]] 形成正向关系 —— 强品牌减少对精准追踪依赖
- 与 [[Data Clean Room]]、[[Server-Side Tracking]] 同为 Cookie 后时代解决方案
- 在 [[CCPA]] / [[GDPR]] 等法律框架下被推动加速

## 参考源

- Google Privacy Sandbox 官方文档与博客
- W3C Web Advertising Business Group 提案与讨论记录
- Chris Kane (Jounce Media)、Eric Seufert (Mobile Dev Memo) 等行业分析
- UK CMA(Competition and Markets Authority)Privacy Sandbox 季度报告
