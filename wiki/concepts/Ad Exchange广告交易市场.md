---
title: Ad Exchange广告交易市场
type: concept
tags: [marketing, 数字营销, 程序化广告, mature]
sources: [raw/数字营销/03-深度应用层/05-程序化广告/]
created: 2026-05-05
updated: 2026-05-05
summary: Ad Exchange 是连接 DSP 与 SSP 的实时竞价撮合中心,以毫秒级 RTB 协议匹配广告主出价与媒体库存,2007 年 Right Media 与 DoubleClick AdX 开创范式,目前 Google AdX、OpenX、Xandr 等支撑全球数千亿曝光。
---

# Ad Exchange 广告交易市场

## 定义

**Ad Exchange(广告交易市场)** 是 [[程序化广告]] 生态中位于 [[DSP需求方平台]] 与 [[SSP供应方平台]] 之间的 **实时竞价撮合引擎**。当用户访问网页时,Ad Exchange 接收 SSP 发来的曝光请求(含上下文与用户信号),向所有连接的 DSP 广播竞价邀请,在 50-100ms 内裁决出最高出价并向获胜方发送广告位。

它把广告购买从"包年包断按位置"变成"按曝光机会单次竞拍",是 [[数字营销]] 工业化、自动化的基础设施。

## 核心要点

### 1. 历史起源

- **2007**:Right Media(被 Yahoo 收购)、DoubleClick(被 Google 收购)首批 Exchange 上线
- **2009**:Google AdX 整合 Google 自身广告库存,把 RTB 推向规模化
- **2010-2015**:DSP/SSP/DMP 生态爆炸,LumaScape 出现
- **2015 后**:Header Bidding 兴起打破 Google 优先权
- **2020 后**:隐私法规与第三方 Cookie 退役引发深度变革

### 2. 撮合机制

经典 **二价拍卖(Second-Price Auction)**:最高出价者中标但只支付第二高出价 + 0.01。这激励竞价者出真实意愿价格,符合 Vickrey 拍卖理论。Google AdX 2019 起改为 **First-Price Auction**(头部竞价时代不可避免),其他 Exchange 跟进。

### 3. 关键数据流

```
用户访问页面 (10ms)
↓ SSP 接收页面/用户信号 (5ms)
↓ Bid Request 广播给 N 个 DSP (10ms)
↓ DSPs 内部决策与出价 (50-80ms)
↓ Exchange 收齐回标,排序 (5ms)
↓ 中标 DSP 返回广告 markup
↓ 浏览器加载广告 (并行)
```

整个 RTB 必须在用户察觉不到的延迟内完成。

### 4. 关键透明度问题

广告主向 SSP 支付 1 元,实际到达媒体的可能只有 50-65 分,中间被以下层级抽水:
- DSP 服务费
- Ad Exchange 服务费(典型 10-20%)
- SSP 服务费
- 数据商费
- 验证商费

ANA 与 ISBA 的"未知差"研究使透明度成为行业重点议题。

### 5. PMP vs Open Exchange

| 类型 | 邀请制 | 价格 | 库存 |
|---|---|---|---|
| **Open Exchange** | 无 | 实时竞价 | 全开放 |
| **Private Marketplace(PMP)** | 邀请制 | 谈判 + 竞价 | 优质库存 |
| **Programmatic Guaranteed** | 一对一 | 固定 CPM | 保量 |
| **Preferred Deals** | 邀请制 | 固定价 | 不保量 |

## 与其他概念的关系

- **生态**:[[DSP需求方平台]] + [[SSP供应方平台]] + [[Ad Exchange广告交易市场]] = [[程序化广告]] 三角
- **机制**:[[RTB实时竞价]] / [[CPM]] / [[Header Bidding]]
- **数据**:[[DMP数据管理平台]] / [[CDP客户数据平台]] / [[转化API]]
- **应用**:[[展示广告]] / [[再营销]] / [[精准营销]]
- **影响因素**:[[隐私优先时代]] / [[ATT隐私框架]] / [[Privacy Sandbox]]

## 主要 Exchange

| Exchange | 母公司 | 强项 |
|---|---|---|
| Google AdX | Google | 整合 Google 库存与 DV360 |
| OpenX | 独立上市 | 独立第三方 |
| PubMatic | 独立上市 | 视频与移动 |
| Magnite | 独立上市 | CTV 龙头 |
| Xandr | Microsoft | 整合 Netflix CTV 库存 |
| Index Exchange | 私有 | 头部竞价开拓者 |
| 腾讯优量汇/穿山甲 | 中国 | 中国本土 RTB |

## 当代趋势

- **直接连接(SSP-DSP Direct)**:绕开 Exchange 减少中间层
- **Curated Marketplace**:基于内容与品牌安全策展
- **Server-Side 集成**:替代浏览器侧 Header Bidding
- **隐私沙箱**:在 Chrome 内置 RTB 部分功能
- **CTV 程序化**:全球最快增长品类

## 参考源

- raw/数字营销/03-深度应用层/05-程序化广告/
- 关联:[[程序化广告]] / [[DSP需求方平台]] / [[SSP供应方平台]] / [[展示广告]] / [[隐私优先时代]]
