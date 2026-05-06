---
title: 转化API Conversions API
type: concept
tags: [marketing, seo, stub]
sources:
  - raw/营销/
  - raw/Google SEO/
created: 2026-05-05
updated:  2026-05-05
summary: 转化 API 是广告平台(Meta CAPI、Google Ads CAPI、TikTok Events API)的服务器端事件接口,绕过浏览器 cookie 与 ATT 限制,提升数据准确性与广告优化效果。
---

# 转化API Conversions API

## 定义

转化 API(Conversions API,CAPI)是**广告平台(Meta、Google Ads、TikTok 等)提供的服务端事件传输接口**,允许广告主**直接从自有服务器向广告平台发送转化与用户行为数据**,而不依赖浏览器端的像素(Pixel)或 cookie。

它的诞生背景:

- iOS 14.5 ATT(应用追踪透明度)阻断 IDFA
- 浏览器 Cookie 收紧(Safari ITP、Chrome Cookieless)
- 广告拦截器普及
- 隐私法规(GDPR、CCPA、LGPD)趋严

## 核心要点

### 主流平台

| 平台 | 名称 | 文档关键词 |
|---|---|---|
| Meta(Facebook、Instagram) | Conversions API (CAPI) | Pixel + CAPI 双追踪 |
| Google Ads | Enhanced Conversions for Web/Leads | 增强型转化 |
| TikTok | Events API | TikTok Events |
| Snapchat | Conversion API | - |
| LinkedIn | Conversions API | B2B 重点 |
| Pinterest | Conversions API | - |

### 客户端(Pixel)vs 服务端(CAPI)对比

| 维度 | 浏览器 Pixel | 服务端 CAPI |
|---|---|---|
| 数据源 | 浏览器 JavaScript | 自有服务器 |
| 受 ATT/ITP 影响 | 极大 | 几乎不受 |
| 数据完整度 | 30-70% | 95%+ |
| 实施难度 | 低(嵌入 JS) | 中(需开发) |
| 用户体验 | 客户端额外加载 | 无影响 |
| 隐私合规 | 受限 | 由企业完全控制 |

### 双轨实施(主流做法)

绝大多数广告主采用 Pixel + CAPI 双发送:

- Pixel 捕捉浏览器端事件
- 服务端 CAPI 同时发同一事件
- 平台用 `event_id`/`fbp`/`fbc` 等参数去重
- 平台优先信任 CAPI 数据
- 互为补充与冗余

### 关键数据点

发送到 CAPI 的事件通常包括:

- **事件类型**:Purchase、Lead、AddToCart、ViewContent
- **用户标识**:邮箱、电话(经 SHA-256 哈希)、外部 ID
- **客户端浏览器信息**:fbp(Browser ID)、fbc(Click ID)、user_agent、IP
- **事件价值**:金额、货币、内容 ID
- **时间戳**

### 实施架构

典型实施:

```
用户浏览器 ↘
              电商后台 → 服务器代码 → POST 到 Meta/Google CAPI
用户支付完成 ↗            ↓
                    保存到自有数据库
```

或通过 Server-Side GTM(Google Tag Manager Server-Side)统一管理:

```
浏览器 → GTM Web → GTM Server → 多个广告平台 CAPI
```

### 隐私合规要点

- 必须遵守 GDPR、CCPA、个保法等
- 用户数据应哈希后传输(邮箱、电话)
- 提供「用户禁止追踪」选项
- 区分必要 cookie 与营销 cookie
- 与广告平台签订数据处理协议(DPA)

## 和其他概念的关系

转化 API 是 [[隐私优先时代]] 数字广告的关键基础设施,与 [[归因模型]]、[[Marketing Mix Modeling]] 共同应对追踪能力下降。

[[精准营销]]、[[再营销]]、[[Lookalike人群]] 等高级广告功能都依赖高质量转化数据,CAPI 直接决定这些功能的有效性。

[[GA4配置]]、[[Google Search Console]] 是分析侧工具,与广告侧 CAPI 互补;[[GDPR]]、[[ATT隐私框架]] 法规驱动了 CAPI 的普及。

[[移动营销]]、[[ASO应用商店优化]]、[[Push通知]] 都涉及移动端追踪挑战,SKAdNetwork 是 iOS 上 CAPI 的应用层补充。

[[企业级SEO]] 与 [[内容营销]] 中,CAPI 让付费广告归因更准确,反向影响内容投资决策——准确归因是 ROI 评估的前提。

## 参考源

- raw/营销/
- raw/Google SEO/
- Meta Business Help: Conversions API
- Google Ads Enhanced Conversions 文档
- Simo Ahava 博客关于 Server-Side GTM
