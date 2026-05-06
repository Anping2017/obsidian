---
title: GA4配置
type: concept
tags: [seo, marketing, mature]
sources: [raw/数字营销/05-实战案例库/02-工具使用/Google Analytics使用指南.md, raw/SEO/03-SEO工具应用/03-3-数据监控体系/流量分析体系.md]
created: 2026-05-05
updated: 2026-05-05
summary: Google Analytics 4 基于事件 + 用户的下一代分析框架,2023 强制替代 UA。
---

# GA4配置

## 定义

GA4(Google Analytics 4)是 Google 在 2020 年推出、2023 年 7 月强制全面替代 Universal Analytics(UA)的新一代网站与 App 统一分析平台。它彻底改变了数据模型:从 UA 的"会话(Session)+ 命中(Hit)"模型,转为"事件(Event)+ 用户(User)+ 参数(Parameter)"模型,统一 Web 与 App 数据,内置机器学习预测,移除 IP 存储以适应隐私时代。学习曲线陡峭,但配置正确后远比 UA 强大。

## 核心要点

**事件驱动的数据模型**:

- **每一个用户行为都是一个 Event**:页面浏览、点击、滚动、视频播放、表单提交。
- **Event + 多个 Parameters**:`page_view` 事件附带 `page_location`、`page_title`、`page_referrer` 等参数。
- **没有"指标 + 维度"的固定二元拆分**,任何参数都可作为维度。

**事件四类**:

1. **自动收集事件(Automatic)**:`session_start`、`first_visit`、`page_view` 等内置。
2. **增强测量事件(Enhanced Measurement)**:开关后自动追踪 scroll、outbound click、site search、video engagement、file download。
3. **推荐事件(Recommended)**:Google 给出标准命名,如 `purchase`、`sign_up`、`add_to_cart` —— 命名遵守可解锁标准报告。
4. **自定义事件(Custom)**:业务特有事件,如 `consultation_booked`。

**关键转化(Conversions / Key Events)**:

- 在 GA4 中标记某些事件为转化(Key Event)。
- 同一事件可在不同账户中标记 / 不标记为转化。
- 转化事件可发送到 Google Ads,用于广告优化。

**核心配置步骤**:

1. **创建账户 + 媒体资源(Property)**:Web 与 App 同属一个 Property。
2. **设置数据流(Data Stream)**:Web 数据流(网址)、iOS 数据流、Android 数据流。
3. **安装代码 / SDK**:Web 通过 Google Tag(原 GTAG)或 GTM(Google Tag Manager);App 通过 Firebase SDK。
4. **配置增强测量(Enhanced Measurement)**:勾选自动追踪选项。
5. **定义自定义事件**:用 GTM 触发器或代码 dataLayer 推送。
6. **创建自定义维度与指标(Custom Dimensions / Metrics)**:把 event 参数注册为维度才能在报告中查询。
7. **关联 Google Ads**:同步转化事件,用于 Smart Bidding。
8. **关联 Search Console**:看 SEO 流量来源关键词。
9. **关联 BigQuery**(免费版有限制)**:导出原始事件数据,做高级分析。
10. **配置受众(Audience)**:基于行为定义动态人群,可同步到 Google Ads。

**重要变化(UA → GA4)**:

| 维度 | UA | GA4 |
|---|---|---|
| 数据模型 | Session + Hit | Event + User |
| 默认指标 | Bounce Rate(跳出率) | Engagement Rate(参与率)|
| 用户识别 | 主要靠 Cookie | User-ID + Device ID + Modeling |
| 报告 | 预定义为主 | 自定义为主 |
| 留存 | 14 个月免费 | 14 个月免费(收费 Property 26 个月) |
| 隐私 | IP 存储 | 默认匿名化、Consent Mode |

**Engagement Rate 替代 Bounce Rate**:

- Engagement Rate = 参与会话 / 总会话。
- 参与会话 = 持续 ≥ 10 秒,或 ≥ 1 次转化,或 ≥ 2 次页面浏览。

**机器学习能力**:

- **预测受众**:7 天内可能购买、7 天内可能流失的用户群,自动同步到 Google Ads。
- **数据驱动归因(DDA)**:GA4 默认归因模型,见 [[归因模型]]。
- **异常检测**:报告中突增或骤降的指标自动标记。

**典型分析场景**:

- **探索分析(Explorations)**:Free-form 表格 / Funnel(漏斗)/ Path(路径)/ Cohort(同期群)/ Segment Overlap。
- **生命周期报告(Lifecycle)**:Acquisition、Engagement、Monetization、Retention 四象限。
- **DebugView**:实时查看自己设备上发出的事件,验证埋点。

**反模式**:

- 直接复用 UA 思维 → 在 GA4 找不到 Bounce Rate 等指标,报告设计错误。
- 不注册自定义维度 → 自定义参数永远不能进报告。
- 转化事件命名不规范 → 跨产品对比困难。
- 不关联 BigQuery → 长期数据分析受限。
- 隐私同意未配置(Consent Mode v2) → 欧盟流量大量丢失。

## 和其他概念的关系

GA4 是 [[数字营销]] 与 [[SEO]] 数据分析的事实标准基础设施,与 [[Google Search Console]](GSC)、Google Tag Manager(GTM)、Google Ads 构成 Google 数据栈四件套。它是 [[归因模型]]、[[转化漏斗]]、[[同期群分析]]、[[漏斗优化]] 的数据底座。

GA4 的事件模型与 [[CDP客户数据平台]] 高度同构,某种程度可作为轻量 CDP 使用。它是 [[北极星指标]] 监测、[[转化率优化]] 实验度量的工具上游。在 [[隐私优先时代]],GA4 的 Consent Mode v2、Server-side Tagging、Modeled Conversions 是必修。

它与 [[再营销]]、[[Lookalike人群]] 受众同步,是 Google Ads 智能投放的训练数据源。GA4 的 Explorations 工具支撑了 [[数据驱动营销]] 的日常自助分析。

## 参考源

- raw/数字营销/05-实战案例库/02-工具使用/Google Analytics使用指南.md
- raw/SEO/03-SEO工具应用/03-3-数据监控体系/流量分析体系.md
- raw/数字营销/03-深度应用层/08-数据分析优化/数据分析工具.md
