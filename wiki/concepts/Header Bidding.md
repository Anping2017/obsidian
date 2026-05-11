---
title: Header Bidding
type: concept
tags: [marketing, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: Header Bidding(头部竞价)是程序化广告中一种把多家 SSP/Exchange 并行竞价、再交给 Ad Server 决策的技术,打破了 Google AdX 的"瀑布"特权,提升了发行商收益并改变了广告技术栈。
---

# Header Bidding

## 定义

**Header Bidding(头部竞价,又称 Pre-bid、Tag-less Bidding)** 是一种程序化展示广告的供给侧竞价架构:网页加载时,在浏览器端(或服务器端)同时向多个 SSP / Ad Exchange 发起广告请求,各方实时返回出价,最高价者赢得广告位的填充权,然后再把结果传递给广告服务器(Ad Server)做最后判定。

它得名于"在 HTML `<head>` 中加载的 JavaScript 触发竞价",但 2017 年后 **Server-Side Header Bidding(S2S)** 兴起,执行位置已从浏览器迁移到服务器集群,术语保留但物理位置变了。

## 核心要点

### 历史背景:打破 Google AdX 的瀑布特权

2014 年之前,主流发行商使用 Google Ad Manager(原 DFP)+ AdX 的**瀑布(Waterfall)**模式:广告位首先以预设底价交给 AdX 出价,AdX 失败再依次询价 Rubicon、AppNexus 等次级 SSP。**AdX 永远第一个出价、且可看到底价**,事实上享有"最后挽留权(Last Look)"。其他 SSP 在不知最终成交价前无法激进出价。

2014–2016 年,Rubicon、AppNexus、PubMatic 联合发起 Header Bidding 反击:把瀑布改成**并行盲拍(parallel auction)**,所有 SSP 同时报价,公平参赛。Google 在 2017–2019 年通过 EBDA(Exchange Bidding)、Unified Pricing Rules 等做相应调整,事实上承认了 Header Bidding 的主导地位。

### 客户端(Client-Side)vs 服务器端(Server-Side)

| 维度 | Client-Side(Prebid.js)| Server-Side(S2S)|
|---|---|---|
| 执行位置 | 浏览器 | 服务器集群 |
| 延迟来源 | 用户浏览器并发请求 | 服务器单次聚合请求 |
| 数据访问 | 完整 Cookie / 头部 | 受限(需要 CHIPS、Storage Access)|
| Cookie 同步 | 可信 | 复杂 |
| 工具代表 | Prebid.js | Prebid Server、Amazon TAM、Google Open Bidding |

S2S 的主要优势:**减轻浏览器负担**、绕过浏览器对第三方 Cookie 的限制;主要劣势:**数据匹配率下降 20–40%**(浏览器侧 ID 不易同步到服务器),需要配合 **UID 2.0、RampID** 等替代 ID 体系。

### 完整请求链路

1. 用户访问页面,Prebid.js 启动
2. Prebid 向各 SSP 发起 bid request
3. SSP 内部聚合 DSP 出价,返回最终 bid
4. Prebid 选出最高价,把价格作为 keyword 传给 Ad Server(GAM)
5. GAM 比较 Header Bidding 价格、AdX 价格、直销订单优先级,决定胜出广告
6. 胜出广告渲染,Impression 上报

整个过程通常需在 200–500ms 内完成,否则用户感知卡顿、跳出率上升。

### 收益提升幅度

行业普遍认为 Header Bidding 让发行商整体广告 CPM 提升 30–70%,主要来源:

- **统一竞价池**:更多需求方同时竞价,推高最终成交价
- **消除瀑布丢单**:瀑布跳层 30% 流量,Header Bidding 几乎无丢单
- **数据公平性**:中小 SSP 也有展示自家算法实力的机会

### 主要参与者

- **Prebid.org**:开源行业联盟,Prebid.js 是事实标准
- **SSP 端**:Magnite(Rubicon + Telaria 合并)、PubMatic、Index Exchange、OpenX、Xandr
- **代表 Wrappers**:Prebid、Amazon TAM(Transparent Ad Marketplace)、Index Wrapper
- **Google 反制**:Open Bidding(原 EBDA),Google 让其他 SSP 在 AdX 内部并行竞价但保留服务器端控制

## 应用 / 工具

- **开源工具栈**:Prebid.js、Prebid Server、Prebid Mobile SDK
- **托管方案**:Magnite Demand Manager(原 nToggle)、PubMatic OpenWrap
- **混合**:Amazon TAM(无明确 SSP 偏好,跨 AWS 边缘节点的 S2S)
- **测量**:Sortable、Adomik、Burt、StackAdapt Analytics 监控竞价表现
- **优化框架**:Floor Price 优化、Timeout 设置(常见 1500ms)、Lazy Loading + HB 组合

## 局限与陷阱

- **页面性能负担**:客户端 HB 并发请求多家 SSP,首屏渲染明显变慢
- **超时丢单**:任何超时未返回 bid 的 SSP 失去机会,Timeout 设短伤收益设长伤性能
- **Cookie 同步衰减**:[[Privacy Sandbox]] 第三方 Cookie 弃用后,跨 SSP 用户匹配率断崖式下降
- **欺诈与套利**:某些 SSP 在两个 wrapper 中重复出价,产生"伪并行"
- **运营复杂度**:每加一个 SSP 都要做 adapter、测试、监控,小发行商难以维护
- **GAM 集成的"Dynamic Allocation 阴影"**:Google 仍保留对自家 AdX 的隐性优势
- **Made for Advertising(MFA)风险**:Header Bidding 抬高 CPM 但低质量站点更易出现劣质需求

## 与其他概念的关系

- 是 [[程序化广告]] 供给侧架构的关键演进
- 与 [[CPC]] / [[CPM]] 计费在广告主侧无直接关系,但通过推高竞价影响广告主成本
- 与 [[Privacy Sandbox]] 强相关 —— 第三方 Cookie 弃用直接挑战 HB 的用户匹配
- 影响 [[ROAS]] —— 广告主侧 CPM 上行需匹配更高 ROAS 目标
- 与 [[Real-Time Bidding]] 同为程序化两大基石,RTB 是底层协议,HB 是供给侧组织方式
- 在 [[GAM/Ad Manager]] 中通过 keyword targeting + Price Priority Line Items 嵌入
- 是 [[Made for Advertising]] 站点泛滥的间接推手 —— 高 CPM 激励垃圾站点诞生

## 参考源

- Prebid.org 文档与博客
- AdExchanger 长期报道 Header Bidding 演化(2014–至今)
- DigiDay《Programmatic Advertising 101》系列
