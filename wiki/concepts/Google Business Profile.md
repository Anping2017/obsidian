---
title: Google Business Profile
type: concept
tags: [seo, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: Google Business Profile(GBP,原 Google My Business)是 Google 为本地商家提供的免费档案系统,直接驱动 Google Maps、本地包(Local Pack)、知识面板的展示,是本地 SEO 的核心入口。
---

# Google Business Profile

## 定义

**Google Business Profile(GBP)** 是 Google 为线下商家提供的免费档案管理系统,2021 年 11 月由 **Google My Business(GMB)** 更名而来。它是商家在 Google 搜索、Google Maps、Google 助手等表面呈现的"信息源",对本地店面、连锁品牌、服务半径型业务(SAB)而言,GBP 几乎等同于一张数字"门面"。

> 名称沿革:Google Local Business Center(2004)→ Google Places(2010)→ Google+ Local(2012)→ Google My Business(2014)→ Google Business Profile(2021)。从业者口语中 GMB 与 GBP 经常混用。

## 核心要点

### 档案承载的字段

| 字段 | 用途 |
|---|---|
| Business name | 商家名称(不可堆砌关键词,否则会被处罚) |
| Category | 主类别 + 最多 9 个次类别,直接影响"哪些查询能触发你" |
| Address / Service Area | 地址或服务范围(SAB 商家可隐藏地址) |
| Hours | 营业时间 + 特殊时段(节日、临时关闭) |
| Phone / Website | 联系方式 |
| Attributes | "提供 WiFi""轮椅可达""女性持有"等结构化属性 |
| Photos / Videos | 照片是点击率最大单一变量之一 |
| Products / Services | 商品/服务清单,带价格 |
| Posts | 类似社交媒体的短动态,提升活跃度信号 |
| Q&A | 用户问答,商家可主动回答 |
| Reviews | 评价(数量、平均分、新鲜度) |

### 本地 SEO 的"3 Local Pack"

当用户搜索带本地意图的查询(如"附近的咖啡店""北京 海淀 牙科"),Google 在结果顶部呈现 **Local Pack** —— 通常是 3 个商家 + 地图。进入 Local Pack 的核心因子(Google 官方说法):

- **Relevance(相关性)**:GBP 资料与查询匹配度
- **Distance(距离)**:用户/搜索词与商家位置距离
- **Prominence(知名度)**:评价数量与分数、外链、网站权威度、品牌提及

### 评价生态

- 评价数量与平均星级是本地排名最强相关变量之一
- Google 严禁"赎买评价""刷评论""离职员工差评清理"等行为,违规会触发评论隐藏或档案暂停
- 商家回复(尤其负面评价的专业回复)同样被算作活跃信号

### GBP Posts、Q&A、Messages

- **Posts**:What's New、Offers、Events、COVID-19 更新等,展示 7 天后从顶部移除但 URL 永存
- **Q&A**:用户提问任何人可回答 —— 竞争对手、不满客户都可能率先回答,需要监控
- **Messages**:可启用聊天功能,响应时间被列为公开指标

### Insights / Performance 报告

GBP 提供 6 个月内的曝光、搜索词、行动(电话、路线、网站)、照片浏览等数据。2022 年改版后术语统一为 Performance,与 [[Google Search Console]] 风格趋同。

### 多门店:GBP API 与批量管理

- 10+ 门店可申请 **Bulk Verification**,通过 Spreadsheet 批量管理
- 100+ 门店通常上 Yext、Uberall、Rio SEO 等本地数据分发平台,统一推送到 Google、Apple Maps、Bing Places、Facebook、Yelp 等多源

## 应用 / 工具

- **官方入口**:[business.google.com](https://business.google.com/)、Google Maps 商家端
- **数据聚合**:GBP API、Google Search Console(关联同域名后可见 Local 查询)
- **多平台同步**:Yext、Uberall、Moz Local、BrightLocal、Whitespark
- **评价管理**:Birdeye、Podium、ReviewTrackers

## 局限与陷阱

- **名称堆砌**:在 Business Name 加关键词(如"老王面馆 海淀最佳手工面")会被检测并降权
- **类别选择错误**:主类别选错直接掉出 Local Pack
- **地理隐藏的 SAB 商家**:必须把"Service Area"设置正确,否则距离因子失效
- **照片真实性**:与实际不符的照片会被用户标记
- **休假/搬迁未更新**:用户白跑一趟,负面评价随之而来
- **评论审核黑箱**:Google 会过滤可疑评论但不告诉商家原因
- **暂停(Suspension)**:任何疑似违规(同一地址多档案、虚假地址)都可能导致档案暂停,恢复申诉周期长
- **AI Overview 时代的不确定性**:当 SGE / AI Overview 接管"附近推荐",Local Pack 的可见度变量正被重写

## 与其他概念的关系

- 是 [[本地SEO]] 的核心入口与第一抓手
- 与 [[SEO]] 总论中"链接/内容/技术/UX"四维并列的第五维:**实体一致性(NAP 一致)**
- 与 [[Google Search Console]] 平行 —— 一个管商家档案、一个管网站
- 在 [[Generative Engine Optimization]] 时代,GBP 数据是 AI 答案的本地事实来源之一
- 评论体系与 [[品牌资产]] 中"感知质量"维度强关联
- 与 [[CPC]] 中的 Local Search Ads 配合 —— GBP 健康度同时影响付费表现

## 参考源

- Google Business Profile Help Center
- Sterling Sky、Local SEO Guide、Whitespark 等本地 SEO 行业研究
- Joy Hawkins 等本地 SEO 专家长期博客
