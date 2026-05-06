---
title: RTB实时竞价
type: concept
tags: [marketing, 数字营销, 程序化广告, mature]
sources: [raw/数字营销/03-深度应用层/05-程序化广告/]
created: 2026-05-05
updated: 2026-05-05
summary: RTB(Real-Time Bidding)是程序化广告的撮合协议,在用户加载页面的毫秒间为每一次广告曝光机会发起独立竞拍,广告主基于对该用户该时刻的价值评估出价,中标方的广告被加载,把广告采买从"批量"变为"单次单人"。
---

# RTB 实时竞价

## 定义

**RTB(Real-Time Bidding,实时竞价)** 是 [[程序化广告]] 的核心协议,由 IAB 在 OpenRTB 标准中规范化(2010 年 v1.0,2024 年 v3.0)。它的革命性在于:把 **广告位购买的最小单位从"千次曝光包"压缩到"单次曝光"**,每一次曝光都是一场独立的拍卖,在用户加载页面的 50-100 毫秒内完成。

## 核心要点

### 1. RTB 的核心循环

```
1. 用户访问网页/打开 App
2. 媒体方 SDK 触发广告请求 → SSP
3. SSP 整理上下文 + 用户信号 → 发给 Ad Exchange
4. Exchange 以 OpenRTB Bid Request 广播给所有 DSP
5. 每个 DSP 在 80ms 内:
   - 解析 Bid Request
   - 匹配受众/再营销列表/Look-alike
   - 用 ML 模型预估 CTR / CVR
   - 算法决定是否出价、出多少
   - 返回 Bid Response
6. Exchange 收齐回标,按价排序
7. 中标 DSP 返回广告创意 URL
8. 用户浏览器加载广告
```

整个流程必须在用户察觉不到的延迟(< 200ms)内完成,否则曝光失效。

### 2. 出价决策模型

广告主每次出价的核心问题:**"这次曝光对我值多少钱?"**

经典公式:
```
Bid = pCTR × pCVR × Value − Cost − Margin
```

- **pCTR**:点击率预测
- **pCVR**:点击后转化率预测
- **Value**:转化的客户终身价值
- **Cost**:数据费、媒介费等
- **Margin**:DSP 留存

这与搜索广告 [[Google Ads]] 的质量分机制底层逻辑一致,差别在 RTB 是非搜索意图的展示。

### 3. 拍卖机制演进

- **Second-Price Auction(早期主流)**:最高价中标,支付第二高 + 0.01。理论上诱导真实出价,但黑盒
- **First-Price Auction(2018+ 主流)**:最高价中标且支付自己出价。Header Bidding 时代的必然——SSP 不再能保证"二价"的可信度
- **Bid Shading**:DSP 反过来用 ML 估计自己出价能多低不被反超,降低过度支付

### 4. RTB 中的关键参数

| 参数 | 含义 |
|---|---|
| **Bid Request** | 包含曝光位置、设备、页面、用户 ID、底价等的请求 |
| **Bid Response** | DSP 返回的出价 + 广告 URL |
| **Floor Price** | SSP 设置的最低成交价 |
| **Bid Cache** | DSP 内部出价缓存,避免重复评估 |
| **Bid Throttle** | 限流,DSP 不可能对每条请求都计算 |

### 5. 数据信号

- **设备**:IDFA(iOS)/AAID(Android)/IP/UA
- **上下文**:页面 URL/类目/关键词/品牌安全标签
- **用户**:Cookie ID(浏览器)/EID(邮箱哈希)/登录 ID
- **第一方数据**:广告主自己的 CRM 匹配

[[隐私优先时代]] 后,这些信号大幅缩水,RTB 出价精度受影响。

## 与其他概念的关系

- **生态**:[[DSP需求方平台]] / [[SSP供应方平台]] / [[Ad Exchange广告交易市场]] / [[程序化广告]]
- **结算**:[[CPM]] / [[CPC]] / [[CPA]]
- **优化**:[[多触点归因]] / [[Marketing Mix Modeling]]
- **隐私**:[[ATT隐私框架]] / [[转化API]] / [[Privacy Sandbox]]
- **技术**:OpenRTB / VAST / VPAID(视频)

## 当代挑战

### 1. 隐私沙箱替代 RTB?

Google Privacy Sandbox 的 Protected Audience(原 FLEDGE)把竞价部分迁到浏览器本地完成,DSP 仅能预先选好出价模型,实时阶段无法访问个人数据。这对 RTB 现有逻辑是根本变革。

### 2. 一价竞价后的不确定

一价拍卖让出价者难以判断"出多少合适",催生 Bid Shading 工具。

### 3. CTV 与 In-App 视频

视频 RTB(VAST/VPAID)、CTV 程序化把 RTB 推向新介质。

### 4. AI 驱动的全自动出价

Performance Max、Demand Gen、AI Driven Bidding 让广告主只设目标 CPA/ROAS,DSP 内部完成所有出价决策,RTB 协议层不变但决策权全部 ML 化。

## 参考源

- raw/数字营销/03-深度应用层/05-程序化广告/
- IAB OpenRTB 规范
- 关联:[[程序化广告]] / [[DSP需求方平台]] / [[SSP供应方平台]] / [[Ad Exchange广告交易市场]] / [[展示广告]]
