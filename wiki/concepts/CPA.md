---
title: CPA
type: concept
tags: [marketing, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: CPA(每次行动成本)是按用户完成指定行动(注册/下单/安装)付费的广告计费与衡量指标,把风险从点击进一步后移到结果层,是效果广告的核心 KPI。
---

# CPA

## 定义

**CPA(Cost Per Action / Cost Per Acquisition,每次行动成本)** 是数字广告中按用户完成预定义"行动"付费的计费模式与对应指标:

- 作为计费模式:广告主只为达成行动的用户付费(注册、下单、安装、订阅等)
- 作为指标:`CPA = 广告花费 ÷ 行动次数`,衡量单次获取一个有效用户/订单的真实成本

> **注意区分**:CPA 在广告语境是"每次行动成本",与隐私法 CCPA(California Consumer Privacy Act,加州消费者隐私法案)、会计执照 CPA(Certified Public Accountant,注册会计师)是完全不同的缩写,场景几乎不会混淆但要警惕跨领域写作时被混用。

## 核心要点

### CPA 的层次定义

CPA 的"Action"含义随漏斗深浅变化,常见梯度:

| 类型 | 行动定义 | 典型场景 |
|---|---|---|
| **CPL** (Cost Per Lead) | 提交表单、留下手机号 | 教育、金融、SaaS |
| **CPI** (Cost Per Install) | 应用安装完成 | 移动游戏、工具类 App |
| **CPR** (Cost Per Registration) | 完成账号注册 | 社交、内容平台 |
| **CPO** (Cost Per Order) | 完成首单付款 | 电商、O2O |
| **CPS** (Cost Per Sale) | 销售按 GMV 分成 | 联盟营销、CPS 网盟 |

### 与 CPC 的关系

- `CPA = CPC ÷ CVR`(转化率)
- 例:CPC = ¥3,落地页 CVR = 2% → CPA = ¥150
- 当广告主以 CPA 为目标(tCPA 出价),平台仍按 CPC 扣费,但会用 ML 模型预测每次点击的转化概率来调整出价

### 谁承担风险:平台 vs 广告主

| 计费模式 | 平台风险 | 广告主风险 |
|---|---|---|
| CPM | 零 | 全部 |
| CPC | 部分(点击) | 转化层风险 |
| CPA | 大部分(点击 + 转化) | 行动质量 |
| CPS | 全部(点击 + 转化 + 履约) | 仅佣金支付 |

风险越往后推,平台收的"风险溢价"越高,但广告主预算确定性也越高。

### 智能出价时代

- Google Smart Bidding 的 **tCPA(Target CPA)**:广告主设定目标 CPA,平台用 ML 自动调整每次点击出价,使长期 CPA 接近目标
- Meta 的 **Cost Cap / Bid Cap**:逻辑类似,但 Meta 倾向最大化结果而非死守 CPA 上限
- **iOS 14.5+ 的 SKAdNetwork、Privacy Sandbox 限制**:细粒度归因受损,CPA 测量精度普遍下降,出现 [[CAPI 服务器端事件]] 等弥补方案

### CPA 公允水平参考

- 取决于:LTV、毛利率、复购率、目标 LTV/CAC 比(常用 3:1)
- 电商 CPA ≈ 首单毛利 × 系数(系数 0.5–1.5)
- SaaS CPA(CPL → CSQL → 成交)往往是月费的 10–18 倍

## 应用 / 工具

- **效果广告平台**:Google Ads(tCPA / Maximize Conversions)、Meta、TikTok Ads、Snapchat
- **联盟网盟**:Impact、CJ Affiliate、Awin、Rakuten、ClickBank
- **归因**:AppsFlyer、Adjust、Branch(移动);GA4、神策、Mixpanel(Web)
- **服务器端事件**:Meta CAPI、Google Enhanced Conversions、TikTok Events API

## 局限与陷阱

- **行动作弊**:刷量、虚假注册、僵尸账号,尤其 CPI 联盟网最严重
- **延迟归因失真**:用户两周后才转化,但平台只看 7 天窗口,CPA 显得偏高
- **平台优化短视**:tCPA 算法可能为达成目标牺牲后续 LTV,选择低质用户
- **行动定义不一致**:跨平台对"安装""注册"定义不同,数据无法直接对齐
- **隐私法规收紧**:[[Privacy Sandbox]]、ATT、GDPR 让转化数据不再 100% 可见
- **与 CCPA / 会计 CPA 不要混淆**:CCPA 是法规,会计 CPA 是职业证书

## 与其他概念的关系

- 是 [[CPC]] 的下游:CPC × (1 / CVR)= CPA
- 与 [[ROAS]] 互为镜像 —— CPA 看成本侧,ROAS 看收入侧
- 在 [[SEO]] 自然流量中存在隐含 CPA(分摊的内容生产与维护成本)
- 受 [[Privacy Sandbox]] 与 ATT 影响显著,归因精度直接影响 CPA 测量
- 联盟营销中的 CPS 是 CPA 的极端版,平台彻底承担流量成本
- 与 [[品牌资产]] 形成长短期对照:强品牌可拉低自然 CPA
- 与 [[Header Bidding]] 在供给侧无直接关系,但需求侧出价策略一致

## 参考源

- Google Ads Help: Target CPA bidding
- Meta Business Help Center: Cost Cap & Bid Cap
- IAB《Digital Advertising Glossary》
