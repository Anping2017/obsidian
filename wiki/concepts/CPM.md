---
title: CPM 千次曝光成本
type: concept
tags: [marketing, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: CPM(Cost Per Mille)是广告每千次展示成本的计费单位,Mille 拉丁语"千",广告主以曝光量付费,品牌广告核心计价方式,与 CPC、CPA 共同构成数字广告计费体系。
---

# CPM 千次曝光成本

## 定义

**CPM(Cost Per Mille,每千次曝光成本)** 是数字广告中以"广告被展示 1000 次"为计费单位的成本指标。Mille 是拉丁语"千"。计算公式:

```
CPM = (广告总花费 / 总曝光数) × 1000
```

CPM 是品牌广告(Branding)最核心的计费方式,适用于不追求即时点击转化、而追求"被看到"的场景。与 [[CPC]](按点击付费)、[[CPA]](按行动付费)、[[CPS]](按销售付费)共同构成数字广告计费谱系。

## 核心要点

### 1. 计费机制类型

- **保量 CPM(Guaranteed CPM)**:媒体合约保证曝光量,价格固定,常用于开屏、首页 banner
- **eCPM(effective CPM)**:其他计费方式(CPC / CPA)折算回千次曝光的等效价格,用于不同计价模式横向比较
- **vCPM(viewable CPM)**:仅计入"可见曝光"(广告 50% 像素在屏幕停留 1 秒以上),IAB 标准,反作弊
- **oCPM**:智能优化 CPM(腾讯、巨量等),平台代为优化转化但保留 CPM 计费形式

### 2. 适用场景

- **品牌广告**:认知度、心智占位,不强调即时转化
- **新品发布**、新市场进入、产品大改版
- **再营销**(Retargeting)中的覆盖频次控制
- 视频广告、信息流大封面位

### 3. 行业基准范围

CPM 因平台、地域、行业差异极大:

- 显示广告(Display)全球均值约 1–5 美元
- Facebook / Instagram 信息流约 5–15 美元
- TikTok / Reels 约 4–12 美元
- LinkedIn(B2B)20–50 美元
- YouTube TrueView 约 5–25 美元
- 中国朋友圈广告 30–150 元(品类、版位差异巨大)

数字仅供参考,实际依赖竞价、定向、季节、行业。

### 4. 与转化指标关系

```
CPM × 点击率(CTR)= CPC × 1000
eCPM = CPC × CTR × 1000 = CPA × CVR × CTR × 1000
```

电商等转化导向场景常用 [[CPC]] / [[CPA]] / [[ROAS]] 取代 CPM,但平台后台仍以 CPM 作为底层度量。

## 典型应用

- **品牌曝光合约**:汽车、奢侈品在视频网站买保量 CPM
- **程序化广告(Programmatic)**:DSP 在 RTB 实时竞价中以 CPM 出价
- **AdSense / 联盟广告**:发布者收益本质是 eCPM
- **海外 SaaS**:LinkedIn CPM 高但 B2B 受众精准,被视为合理成本

## 局限与陷阱

- **曝光不等于注意**:展示 ≠ 看到 ≠ 记住,vCPM、注意力经济度量(Attention Metrics)兴起
- **作弊与无效曝光**:bot 流量、广告堆叠(stacking)、像素隐藏,IAB 反作弊标准与 [[MRC]] 验证
- **下游归因模糊**:CPM 难以直接关联转化,需 [[归因模型]] / Lift Test / [[品牌升降研究]]
- **频次失控**:同一用户被反复曝光(频控失败),浪费预算并造成反感
- **数字游戏**:低 CPM 媒体可能流量质量差,单纯比 CPM 会误导

## 与其他概念的关系

- 同族指标:[[CPC]]、[[CPA]]、[[CPS]]、[[ROAS]]、[[营销ROI|ROI]]
- 上位概念:[[数字广告]]、[[程序化广告]]
- 度量延伸:[[CTR]]、[[CVR]]、[[转化漏斗]]
- 反作弊:[[Ad Fraud]]、[[MRC]] 可见性标准
- 价值衡量:[[品牌资产]]、[[品牌升降研究]]
- 互动平台:[[信息流广告]]、[[OTT]]、[[CTV]]

## 参考源

- IAB 数字广告测量标准
- MRC(Media Rating Council)Viewability 定义
- Google Ads / Meta Business 帮助文档
