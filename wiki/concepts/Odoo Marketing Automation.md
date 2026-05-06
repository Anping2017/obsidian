---
title: Odoo Marketing Automation
type: concept
tags: [odoo, marketing, mature]
sources: [raw/Odoo/]
created: 2026-05-05
updated: 2026-05-05
summary: Odoo Marketing Automation 提供基于触发器和分支的多步营销活动设计器,与 CRM、电商、Email、SMS、推送通道整合,实现客户旅程自动化,定位中小企业的 HubSpot 替代。
---

# Odoo Marketing Automation

## 定义

Odoo Marketing Automation 是 Odoo 提供的客户旅程自动化模块,允许营销人员通过可视化流程图设计多步骤、多渠道、基于触发器和分支的营销活动(Campaign)。它把分散的 Email、SMS、Push、社交触发整合到一个流程编辑器,实现"用户做 A 就发 B、几天后没回复就发 C"的自动化逻辑。

它的产品定位是 HubSpot Marketing Hub、ActiveCampaign 的中小企业替代,卖点是与 [[Odoo 模块体系]] 中 CRM、电商、Sales、Helpdesk 数据原生贯通。

## 核心组件

**Activities(活动节点)**

每个 Marketing Automation Campaign 由一系列活动节点组成:

- **Email Action**:发送预设的 Mass Mailing 模板
- **SMS Action**:发送 SMS(需配置 SMS 网关如 Twilio、阿里云通信)
- **Server Action**:调用 Odoo 服务端逻辑(创建 Lead、改字段、调 API)
- **Push Notification**:Web Push 推送
- **Wait**:等待时间
- **Condition**:基于字段或行为分支

**Triggers(触发器)**

活动从某个触发器开始:
- Date(具体日期触发)
- Beginning of Workflow(进入活动时立即触发)
- After Mailing Sent(上一邮件发出后)
- After Mailing Opened / Clicked / Bounced / Replied
- After SMS Sent / Delivered / Clicked
- 自定义条件(基于客户字段)

**Target Audience(目标受众)**

- 选择模型(Contact、Lead、Order、Custom)
- 过滤条件(行业 = 餐饮、城市 = 上海、最近订单 < 90 天)
- 动态/静态:动态根据条件持续加入,静态一次性

## 典型客户旅程

**新客欢迎序列**

1. Trigger:新建 Contact
2. Wait 1 hour
3. Email "Welcome"
4. Wait 3 days
5. Condition:邮件被打开?
   - YES → Email "Top Products"
   - NO → SMS "Reminder"
6. Wait 7 days
7. Email "First Discount Code"

**弃单挽回**

1. Trigger:Order in "Abandoned" 状态
2. Wait 2 hours
3. Email "You forgot something"(含购物车链接)
4. Wait 24 hours
5. Condition:订单完成?
   - YES → 退出
   - NO → Email with 10% discount

**重复购买**

1. Trigger:Order delivered + 30 days
2. Email "How was your purchase?"
3. Condition:点击好评?
   - YES → Email with referral program
   - NO → Email for support

## 多渠道整合

**Email**

- Mass Mailing 模块的全部模板可用
- A/B 测试(主题行、发件人、内容)
- DKIM、SPF、DMARC 集成提高送达率
- Bounces 自动清理

**SMS**

- Twilio、AWS SNS、阿里云通信、腾讯云通信集成
- 中国地区合规需挂模板号

**Push Notification**

- Web Push(浏览器订阅)
- 移动 App Push 需第三方集成(如 OneSignal)

**社交媒体**

- Facebook / Instagram 创建 Lead Form 直接同步到 CRM
- Marketing Automation 触发后续旅程

## 数据与报告

**统计**

- 各阶段进入人数、流失率
- 邮件 Open Rate、Click Rate
- 转化率(到下一步、到购买)

**A/B 测试**

- 在 Email Action 中创建多个变体
- 自动计算赢家、自动应用

**报表**

- Pivot 视图分群分析
- 与 Sale 模块联动,看活动 ROI

## 与 HubSpot / ActiveCampaign 对比

| 维度 | Odoo Marketing Auto | HubSpot Marketing Hub | ActiveCampaign |
|---|---|---|---|
| 价格 | Enterprise 订阅内 | $50-$3600/月 | $9-$259/月 |
| ERP 集成 | 原生 | 需 API | 需 API |
| 流程编辑 | 中等 | 极强 | 强 |
| 模板库 | 中 | 极大 | 大 |
| 中国合规 | 自部署易合规 | 全球 | 全球 |
| 学习曲线 | 中(需懂 Odoo) | 中 | 低 |

## 局限

- 视觉化流程编辑器不如 HubSpot 直观
- 邮件模板数量与设计灵活度低于专业 EMM 工具
- 中国 SMS 与微信生态需第三方对接
- 大规模发件(月百万级)需独立邮件 ESP(SendGrid、Mailgun)
- A/B 测试功能基础

## 与 Email Marketing 模块的关系

Odoo 有独立的 Mass Mailing(批量邮件)模块,Marketing Automation 是其上层封装——单次群发用 Mass Mailing,多步骤旅程用 Marketing Automation。

## 参考源

- raw/Odoo/
- 相关:[[Odoo模块体系]]、[[Odoo电商模块]]、[[CRM客户关系管理]]
