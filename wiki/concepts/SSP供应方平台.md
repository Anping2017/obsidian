---
title: SSP供应方平台
type: concept
tags: [marketing, 数字营销, 程序化广告, mature]
sources: [raw/数字营销/03-深度应用层/05-程序化广告/]
created: 2026-05-05
updated: 2026-05-05
summary: SSP(Supply-Side Platform)是程序化广告生态中代表媒体/出版商的平台,负责库存管理、向多个交易市场分发广告位曝光请求、收益最优化(Yield Optimization),与 DSP 形成"卖方-买方"对应。
---

# SSP 供应方平台

## 定义

**SSP(Supply-Side Platform,供应方平台)** 是 [[程序化广告]] 生态中代表 **媒体/出版商一方** 的平台,职责是把媒体的广告位库存(网站、App、视频流)实时打包、定价、分发到 [[Ad Exchange广告交易市场]],让全网 [[DSP需求方平台]] 能竞价采购。SSP 帮媒体在每一次曝光中获得最高单价,同时管理填充率、广告质量、数据隐私。

代表产品:Google Ad Manager(原 DFP+AdX)、Magnite、PubMatic、OpenX、Index Exchange、Xandr Monetize。

## 核心要点

### 1. SSP 五大核心能力

| 能力 | 内容 |
|---|---|
| **库存管理** | 把广告位规范化(尺寸、位置、楼层)接入交易市场 |
| **底价控制(Floor Price)** | 设置最低成交价,防止贱卖 |
| **优先级编排** | 直签合同、PMP 私有市场、Open Auction 三级 Waterfall/Header Bidding |
| **收益优化** | 用 ML 动态调整底价、刷新逻辑、广告位分配 |
| **质量控制** | 屏蔽恶意广告(Malvertising)、不合规创意、品牌不安全 |

### 2. Header Bidding(头部竞价)

2015 年兴起的关键技术,媒体在加载页面时 **同时向多个 SSP/Exchange 发起请求**,所有人的真实出价对比后选最高,打破了 Google 早期"瀑布流(Waterfall)"对自身 AdX 的偏袒。Prebid.js 是开源标准。

### 3. 私有市场(PMP)

- **PG**:程序化保量,与广告主协商固定 CPM 与曝光量
- **PD**:程序化直购,固定单价但库存不保量
- **PA**:私有竞价,邀请少数广告主在私有竞价池竞拍

PMP 给优质媒体保留高单价、可控品牌环境的机会。

### 4. 与 DSP 的对应关系

```
广告主 → DSP(买方) → Ad Exchange ← SSP(卖方) ← 媒体
```

竞价撮合发生在 Ad Exchange 内部,DSP 与 SSP 是各自一侧的代理与优化器。

### 5. 收益优化(Yield Optimization)

SSP 对每次曝光决定:
- 走开放竞价还是 PMP?
- 底价定多少?
- 用哪些受众数据增强?
- 是否触发广告刷新(refresh)?

目标是最大化 RPM(Revenue Per Mille,千次曝光收入)。

## 与其他概念的关系

- **生态对手方**:[[DSP需求方平台]] / [[Ad Exchange广告交易市场]]
- **机制**:[[RTB实时竞价]] / [[Header Bidding]] / [[CPM]]
- **跨概念**:[[展示广告]] / [[程序化广告]]
- **媒体角度**:[[内容营销]] 媒体的核心收入引擎

## 当代挑战

### 1. ads.txt / sellers.json

为打击库存假冒,IAB 推出 ads.txt(2017)与 sellers.json(2019),要求媒体公开声明授权的 SSP,DSP 只买正品库存。

### 2. Supply Path Optimization(SPO)

DSP 主动减少使用的 SSP 数量、消除重复路径,提升每元投入到达媒体的比例,SSP 不再"接得越多越赚",而要凭差异化与透明度竞争。

### 3. 隐私时代

- iOS ATT、Cookie 退役削弱可定向广告价值,SSP eCPM 普遍下降 20-40%
- Contextual targeting(基于内容上下文而非用户)回归
- Curated Marketplace(策展型市场)兴起

### 4. CTV/视频/DOOH 程序化化

新介质带来增量,但定价、衡量、SSP-DSP 集成都要重新建立。

## 参考源

- raw/数字营销/03-深度应用层/05-程序化广告/
- 关联:[[DSP需求方平台]] / [[Ad Exchange广告交易市场]] / [[程序化广告]] / [[展示广告]] / [[隐私优先时代]]
