---
title: Google Ads
type: concept
tags: [marketing, mature]
sources: [raw/Google SEO/03-应用层-实践技能/3.7-SEO整合营销/01-SEO与PPC整合.md, raw/数字营销/03-深度应用层/01-搜索引擎营销/SEO基础与策略.md]
created: 2026-05-05
updated: 2026-05-05
summary: Google Ads 是全球最大的付费广告平台,覆盖搜索、展示、视频、购物、Discovery 等库存,以质量得分加权竞价决定排名,是数字营销 SEM 的核心工具。
---

# Google Ads

## 定义

**Google Ads**(原名 Google AdWords,2018 年改名)是 Google 推出的付费广告平台,覆盖 Google 搜索、Google 展示网络(GDN,数百万合作站)、YouTube 视频、Google 购物、Discovery、Gmail、Maps、Performance Max(整合所有库存的 AI 投放)等多个产品。

Google Ads 是 Alphabet 收入的核心引擎(占总收入 70%+),也是全球数字广告市场份额最大的平台之一。掌握 Google Ads 是 [[搜索引擎营销]] 与 [[数字营销]] 从业者的核心专业能力。

## 核心要点

- **核心广告类型**:
  - **搜索广告(Search Ads)**:文字广告显示在 Google 搜索结果页顶部
  - **展示广告(Display Ads)**:GDN 上的图片、Banner、原生广告
  - **视频广告(Video Ads)**:YouTube 上的 TrueView、In-Stream、Bumper、In-Feed
  - **购物广告(Shopping / Product Listing Ads)**:产品图+价格,通过 Merchant Center 数据
  - **应用广告(App Ads / UAC)**:推广应用安装与使用
  - **本地服务广告(Local Services Ads)**:本地服务商,按线索付费
  - **Discovery 广告**:在 Discover、Gmail、YouTube 信息流中
  - **Performance Max**:AI 整合所有库存自动投放,2022 年起力推
  - **Demand Gen**:2023 年新引入,聚焦 YouTube + Discover 的需求生成
- **竞价机制(Auction)**:
  - 每次搜索/曝光机会触发一次实时竞价
  - **广告排名(Ad Rank)= 出价 × 质量得分 × 预期 CTR × 着陆页体验 × 广告扩展加权 × 上下文加权**(简化版)
  - **二价拍卖(Vickrey-style)**:实际付费 = 击败下一名所需最低价 + $0.01
  - 高质量得分 = 更低 CPC + 更高排名
- **质量得分(Quality Score)1-10**:
  - **预期点击率(Expected CTR)**:相对同位置历史
  - **广告相关性**:广告与关键词匹配度
  - **着陆页体验**:加载速度、相关性、可信度
  - 质量得分高 = 同样位置花费更少
- **关键词匹配类型**:
  - **广泛匹配(Broad)**:含同义、相关、变体——覆盖大但不精
  - **词组匹配(Phrase)**:必须包含核心短语
  - **精确匹配(Exact)**:必须完全匹配或紧密变体
  - **否定关键词(Negative)**:排除特定词,精细化定向
- **结构层级**:
  - **账户(Account)**:1 个 Google Ads 账户
  - **广告系列(Campaign)**:按目标/预算/类型组织
  - **广告组(Ad Group)**:相同主题关键词的集合
  - **广告(Ads)**:同一组下的多个文案变体
  - **关键词(Keywords)**:每广告组的关键词列表
  - **扩展(Extensions)**:附加链接、电话、地址、价格、图片
- **出价策略**:
  - **手动 CPC**:精细控制每个关键词出价
  - **增强 CPC(eCPC)**:Google 在手动基础上小幅自动调整
  - **目标 CPA**:智能投放达到目标 CPA
  - **目标 ROAS**:智能投放达到目标 ROAS
  - **最大化转化(Maximize Conversions)**:在预算内最大转化数
  - **最大化转化价值(Max Conversion Value)**:在预算内最大转化价值
  - **目标曝光份额**:品牌词常用,确保占据特定排名
- **关键 KPI**:
  - **CPC**:每次点击成本
  - **CTR**:点击率
  - **CR**:转化率
  - **CPA**:每次转化成本
  - **ROAS**:广告支出回报
  - **质量得分**
  - **曝光份额(Impression Share)**:实际曝光 / 可获得曝光
  - **转化价值(Conversion Value)**:跟踪 LTV 时使用
- **进阶技术**:
  - **受众层(Audiences)**:再营销列表、相似受众、Affinity、In-Market、Custom Intent
  - **设备/地域/时段调整**:数据驱动的出价倍数
  - **Smart Bidding**:基于机器学习的智能出价
  - **Asset 自动化**:Performance Max 让素材组合 AI 自动测试
  - **Conversion Tracking**:GA4 集成、增强转化(Enhanced Conversions)、离线转化导入
- **隐私时代的演化**:
  - 第三方 Cookie 退役下,Google 推 Privacy Sandbox(隐私沙盒)的 Topics、Protected Audiences API
  - 着重第一方数据(Customer Match)
  - 增强转化(用哈希处理的客户邮箱/电话)
  - 同意模式(Consent Mode v2)适配 GDPR
- **常见 Google Ads 错误**:
  - 不分广告组(关键词混杂质量得分低)
  - 不用否定关键词(浪费在不相关查询)
  - 着陆页与广告不匹配(质量得分低)
  - 短期数据决策(2 天就停广告组)
  - 忽视质量得分优化(只看 CPC)
  - 没有转化跟踪(无法智能优化)
  - 默认所有 Smart Bidding(适合成熟账户但不适合新账户冷启动)

## 和其他概念的关系

Google Ads 是 [[搜索引擎营销]] 中付费广告(PPC)的最主要平台,与 [[搜索引擎优化]] 形成 SEM 的两翼。

Google Ads 的关键词机制使用 [[关键词研究]] 与 [[搜索意图]] 同样的方法论;质量得分中的"着陆页体验"评估机制与 [[E-E-A-T]] 在判断逻辑上同源。

Google Ads 的转化跟踪与归因接入 [[数据驱动营销]] 体系,对 [[营销ROI]] 计算至关重要。

Performance Max 是 [[精准营销]] 在 Google 平台上的 AI 实现——人定义目标,机器决定投放。

Google Ads 的购物广告(PLA)是 [[电商SEO]] 与 [[搜索引擎营销]] 的交集——结构化产品数据(Product schema)同时服务自然与付费。

[[本地SEO]] 中的本地服务广告(LSA)与 Google Ads 协同,构成本地企业的获客组合。

## 参考源

- raw/Google SEO/03-应用层-实践技能/3.7-SEO整合营销/01-SEO与PPC整合.md
- raw/数字营销/03-深度应用层/01-搜索引擎营销/SEO基础与策略.md
- raw/SEO/01-SEO基础认知/01-1-SEO概念与原理/SEO与SEM区别.md
