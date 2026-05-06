---
title: Marketing Mix Modeling (MMM)
type: concept
tags: [marketing, stub]
sources:
  - raw/营销/
  - raw/数字营销/
created: 2026-05-05
updated: 2026-05-05
summary: MMM 通过统计回归把广告/营销投入与销售结果建模,估计各渠道的边际贡献,是隐私优先时代替代精确归因的主流方法,Google Meridian、Meta Robyn 等开源工具推动其复兴。
---

# Marketing Mix Modeling (MMM)

## 定义

Marketing Mix Modeling(MMM,营销组合建模)是一种**以统计回归(通常多元线性回归或贝叶斯方法)把营销投入与销售结果建模、估计各渠道边际贡献**的分析方法。

它最早出现在 1950-60 年代消费品大企业(P&G、Coca-Cola),长期作为传统大公司年度营销预算决策的支柱。在数字精确归因兴起的 2010 年代被边缘化,但在 [[隐私优先时代]] 重新成为主流——因 cookie 与 IDFA 受限,精确多触点归因失效,MMM 这种「不依赖个体追踪」的总量建模重获价值。

## 核心要点

### 与多触点归因(MTA)对比

| 维度 | MMM | MTA(多触点归因) |
|---|---|---|
| 数据粒度 | 聚合(渠道-周-地区) | 个体(每次曝光-点击) |
| 隐私 | 完全不需要个体数据 | 需要 cookie / IDFA |
| 时间范围 | 长(数年) | 短(数日到数月) |
| 渠道覆盖 | 全渠道(线下、电视、户外、数字) | 主要数字渠道 |
| 离线效应 | 可建模 | 几乎不可 |
| 适合 | 战略预算分配 | 战术日常优化 |

实践中常**两者结合**:MMM 做战略/年度,MTA 做战术/日常。

### 基本结构

```
销量(t) = β0
        + β1 × TV(t) [+ adstock 滞后]
        + β2 × 数字广告(t)
        + β3 × 报纸(t)
        + β4 × 价格(t)
        + β5 × 季节(t)
        + β6 × 节假日(t)
        + β7 × 竞争对手(t)
        + ε
```

### 关键技术要素

1. **Adstock**(广告残留效应):广告影响不只在投放当周,会衰减
2. **Saturation**(饱和效应):花得越多边际效用越低,常用 Hill / Logistic
3. **基准(Base)与增量(Incremental)**:把销量分为「不投广告也有的」与「营销贡献」
4. **多变量控制**:经济、季节、价格、竞品
5. **贝叶斯方法**:加先验知识,处理稀疏数据,Robyn / LightweightMMM 的核心

### 主流工具

| 工具 | 厂商 | 特征 |
|---|---|---|
| Robyn | Meta(开源) | 半自动、面向中型广告主 |
| LightweightMMM | Google(开源) | 贝叶斯框架 |
| Meridian | Google | 2024 推出,综合 MMM 解决方案 |
| Marketing Evolution | 商业 | 企业级 |
| Nielsen MMM | 商业 | 传统消费品 |
| MASS Analytics | 商业 | - |

### 实施步骤

1. 收集 2-3 年周/月级数据
2. 列出所有解释变量(各渠道支出、价格、竞品、宏观)
3. 建立模型,迭代 adstock / saturation 参数
4. 验证:R²、MAPE、out-of-sample 预测
5. 计算 ROI:每渠道单位投入产出
6. 优化预算:在总预算约束下最大化总销量
7. 持续校准:加入新数据更新模型

### 局限

- 数据需求大(>2 年高质量数据)
- 多重共线性(电视与户外常同时投放)
- 不能精细到广告级别
- 假设线性 + 平稳,创新事件难处理
- 解读需要业务理解,纯算法不够
- 增量验证困难(需要 holdout 实验)

### 与 Incrementality Testing 互补

MMM 估算各渠道贡献,**增量测试**通过 A/B 实际关停某渠道验证真实效果。两者结合形成「证据三角」:MMM(全局)+ MTA(数字日常)+ Incrementality(因果验证)。

## 和其他概念的关系

MMM 是 [[隐私优先时代]] 与 [[转化API]] 互补的关键工具——在精确追踪受限时,通过聚合建模回答「钱花在哪最划算」。

[[CAC获客成本]]、[[LTV]] 是单元经济学,MMM 是渠道经济学;[[归因模型]] 是 MMM 的对比物;[[AB测试|AB测试]] 与 MMM 都是为了量化营销 ROI,但路径不同。

[[品牌定位]]、[[品牌权益]] 在 MMM 中可作为「基准销量提升」体现;[[销售漏斗]] 各阶段的营销投入在 MMM 中体现为「滞后效应」。

[[精准营销]] 在隐私优先时代逐渐让位于上下文 + MMM + 第一方数据;[[CDP客户数据平台]] 是第一方数据基础设施,与 MMM 相辅相成。

## 参考源

- raw/营销/
- raw/数字营销/
- Meta Robyn 开源项目 https://facebookexperimental.github.io/Robyn/
- Google Lightweight MMM 开源项目
- 《Marketing Analytics: Data-Driven Techniques》
