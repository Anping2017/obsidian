---
title: DMP数据管理平台
type: concept
tags: [marketing, 数字营销, 数据, mature]
sources: [raw/数字营销/04-高级实践层/02-营销技术栈/]
created: 2026-05-05
updated: 2026-05-05
summary: DMP(Data Management Platform)是聚合、归一化、激活第三方与匿名化第一方数据的中央平台,以 Cookie/设备 ID 为锚整理人群标签,主要服务于广告投放;在 Cookie 退役与 GDPR 后逐渐让位于 CDP。
---

# DMP 数据管理平台

## 定义

**DMP(Data Management Platform,数据管理平台)** 在 2010 年代是 [[程序化广告]] 生态的"大脑"——聚合 **第一方数据**(网站访客 cookie)、**第二方数据**(合作方共享)、**第三方数据**(数据商售卖),归一化为统一受众标签后,激活到 [[DSP需求方平台]] 用于广告定向、Look-alike 扩展、频次控制。

代表产品:Adobe Audience Manager、Oracle BlueKai、Salesforce Audience Studio(原 Krux)、Lotame、Eyeota。

随着第三方 Cookie 退役与隐私监管收紧,DMP 商业模式受挫,2020 年后大量被 [[CDP客户数据平台]] 替代或整合。

## 核心要点

### 1. DMP vs CDP 关键差别

| 维度 | DMP | CDP |
|---|---|---|
| **数据主体** | 匿名 cookie/设备 ID | 已知客户(邮箱、手机) |
| **核心数据** | 第三方 + 匿名第一方 | 第一方为主 |
| **服务对象** | 广告投放团队 | 营销/CRM/产品团队 |
| **持久度** | 短(cookie 30-90 天) | 长(企业完整生命周期) |
| **主要用途** | 广告人群、Look-alike | [[精准营销]]、[[CRM客户关系管理]]、个性化体验 |
| **隐私合规** | 紧张 | 相对友好(用户同意为前提) |

### 2. DMP 三大功能

**收集 → 归一 → 激活**

1. **收集**:像素跟踪、SDK、API、数据合作
2. **归一**:跨设备拼接(Probabilistic Matching)、清洗、去重
3. **激活**:推送受众包到 DSP/SSP/邮件平台

### 3. 数据分层

- **第一方数据**:企业自有(网站访客、CRM、APP 用户)
- **第二方数据**:合作方第一方数据(媒体的访客)
- **第三方数据**:数据公司聚合(LiveRamp、Acxiom 等)

DMP 的核心商业价值曾是 **聚合第三方数据并以人群包形式售卖**。

### 4. 受众构建

- **规则受众**:30 岁以上 + 访问过定价页 + 未购买
- **Look-alike**:基于种子用户的高维相似性扩展
- **预测建模**:倾向购买、流失预警等

## 与其他概念的关系

- **同生态**:[[DSP需求方平台]] / [[SSP供应方平台]] / [[Ad Exchange广告交易市场]] / [[程序化广告]] / [[再营销]]
- **替代/演进**:[[CDP客户数据平台]] / [[转化API]] / [[Server-side Tracking]]
- **背景压力**:[[隐私优先时代]] / [[ATT隐私框架]] / [[GDPR]]
- **跨域**:[[CRM客户关系管理]] / [[第一方数据]] / [[精准营销]]

## 衰退原因

### 1. 第三方 Cookie 退役

Safari ITP(2017)、Firefox(2019)、Chrome(2024 完成)逐步切断第三方 Cookie,DMP 跨站追踪能力崩塌。

### 2. iOS ATT

App 端 IDFA 默认关闭,移动端 DMP 数据规模缩水超 70%。

### 3. GDPR/CCPA

欧盟、加州法规要求明示同意 + 数据使用透明,DMP 模型难合规。

### 4. 第一方数据回归

企业意识到自有客户数据更有价值、更合规,纷纷转 CDP。

## 当代演进

- **数据洁净室(Data Clean Room)**:Google Ads Data Hub、Meta Advanced Analytics、AWS Clean Rooms,允许跨方数据计算但不暴露原始数据
- **Curated Marketplace**:经过策展的第一方数据交换
- **Identity Resolution**:LiveRamp ATS 等基于哈希邮箱的可持续 ID

## 参考源

- raw/数字营销/04-高级实践层/02-营销技术栈/
- 关联:[[CDP客户数据平台]] / [[程序化广告]] / [[DSP需求方平台]] / [[隐私优先时代]] / [[精准营销]]
