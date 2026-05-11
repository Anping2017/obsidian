---
title: ROAS
type: concept
tags: [marketing, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: ROAS(广告支出回报率)是衡量每花一元广告费产生多少营收的核心效率指标,是数字广告投放的北极星 KPI,但需要与毛利率、归因窗口、增量性等维度协同解读才有意义。
---

# ROAS

## 定义

**ROAS(Return on Ad Spend,广告支出回报率)** 是衡量广告投放效率的核心指标:

$$\text{ROAS} = \frac{\text{广告带来的营收}}{\text{广告花费}}$$

通常以倍数(如 4x、3.5x)或百分比(400%、350%)表达。ROAS 与 [[CPA]] 形成"成本/收入"两面镜:CPA 看每获取一个客户花多少钱,ROAS 看每元广告费撬动多少营收。

ROAS 不等于 ROI(Return on Investment)。ROI 通常以利润为分子、所有相关成本为分母,而 ROAS 只看营收 vs 广告花费,**不扣除商品成本与运营成本**,因此一个 4x 的 ROAS 可能并不盈利。

## 核心要点

### 何时算盈亏平衡

设毛利率为 GM,商品成本 + 履约成本占营收的 (1-GM):

- 盈亏平衡 ROAS ≈ 1 / GM
- 例:GM = 40% → 平衡 ROAS = 2.5x;低于此值在亏钱
- 加上运营、固定成本摊销后,可持续 ROAS 通常需更高

### Target ROAS(tROAS)智能出价

Google Ads、Meta 等平台支持以 ROAS 目标直接出价:

- 广告主输入目标 ROAS(如 4x)
- 平台用 ML 模型预测每次点击的预期价值,自动调整 CPC 让长期 ROAS 接近目标
- 优势:解放手动调整;劣势:依赖回传转化质量,数据稀疏时不稳定

### 归因窗口决定 ROAS 高低

- **Click-through 1 day vs 7 day vs 28 day**:窗口越长,可归因转化越多,ROAS 看起来越高
- **View-through 归因**:把"看过广告未点击但后续购买"也算 —— 显著抬高 ROAS,但增量性存疑
- **Last-click 与 Data-driven 模型**:同一笔订单不同模型给的 ROAS 可能相差 50%

### 增量 ROAS(iROAS)

最常见的 ROAS 陷阱:**广告归因来的订单中,有多少是本就会购买的存量用户?**

- 增量 ROAS = (有广告时营收 - 没广告时营收) ÷ 广告花费
- 测量手段:Geo Holdout 实验、Ghost Ads、PSA Test、IPSOS 调研
- 经验数据:品牌词搜索广告的增量 ROAS 常不到 0.5x(用户即使不投广告也会自然搜索点击);冷启动展示广告的增量 ROAS 通常高于自报 ROAS

### 渠道层级解读

| 层级 | 典型 ROAS | 备注 |
|---|---|---|
| 品牌词搜索 | 10–30x | 名义高但增量低 |
| 非品牌词搜索 | 2–5x | 真实需求拦截 |
| 再营销 / 购物车放弃 | 5–10x | 同样面临增量问题 |
| 兴趣定向信息流 | 1.5–3x | 真正的获客层 |
| 冷启动品牌展示 | 0.5–1x | 看 LTV 而非短期 ROAS |

### LTV ROAS

短期 ROAS 只看首单营收,会低估订阅、复购模型。引入 **LTV ROAS**(用预期 12 月或 24 月 LTV 替代首单营收)更接近真实经济意义:

- 订阅类业务首月 ROAS 0.3x,但 24 月 LTV ROAS 可达 4x
- 电商美妆复购模型常用 6 月 LTV 做出价信号

## 应用 / 工具

- **平台**:Google Ads(tROAS、Maximize Conversion Value)、Meta(Value Optimization)、TikTok(VBO)、Amazon DSP
- **归因建模**:Triple Whale、Northbeam、Rockerbox、Measured
- **增量测试**:Meta Conversion Lift、Google Geo Experiments、Haus、INCRMNTAL
- **MMM(媒体组合建模)**:Robyn、LightweightMMM、Nielsen MMM 等回归型模型

## 局限与陷阱

- **不扣成本误读**:ROAS 4x 看起来很美,但若毛利率 25%,实际亏钱
- **归因偏差**:Last-click 给已经知道品牌的渠道分太多功劳
- **平台自报 ROAS 注水**:Meta/TikTok 自报往往是真实增量 ROAS 的 1.5–3 倍
- **窗口期任意性**:同一广告 1 天 vs 28 天窗口 ROAS 可差一倍
- **Privacy Sandbox / iOS ATT 影响**:[[Privacy Sandbox]] 时代点击 ROAS 测量精度普遍下降 20–40%
- **过度追求短期 ROAS**:削减品牌投入,长期获客成本上升
- **品牌词搜索"骗局"**:本就会买的用户被广告拦截,自报 ROAS 极高,增量 ROAS 极低

## 与其他概念的关系

- 与 [[CPA]] 互为镜像 —— ROAS 看收入端,CPA 看成本端
- 受 [[CPC]] 影响:`ROAS = (CVR × AOV) ÷ CPC`
- 在 [[Privacy Sandbox]] 时代精度严重受损
- 与 [[Header Bidding]] 在展示端配合 —— Header Bidding 提升 CPM,广告主侧表现为更高 CPC,需匹配的 ROAS 目标
- 与 [[品牌资产]] 形成短长期张力:强品牌摊薄获客 ROAS 的同时整体 LTV 提升
- 在 [[SEO]] 自然流量场景中存在隐含 ROAS(自然营收除以内容生产成本)
- 与 MMM、增量测试构成"效率指标三件套",单看 ROAS 必失真

## 参考源

- Google Ads Help: Target ROAS bidding
- Meta Conversion Lift Studies 白皮书
- Avinash Kaushik、Andrew Anderson 等数字分析专家关于 ROAS 局限的长期讨论
