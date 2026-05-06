---
title: CRM客户关系管理 Customer Relationship Management
type: concept
tags: [business, marketing, sales, stub]
sources:
  - raw/营销/
  - raw/商业管理学/
created: 2026-05-05
updated: 2026-05-05
summary: CRM 是以客户为中心、贯穿获客-签单-服务-复购的全生命周期管理体系,既是商业理念也是软件类别;Salesforce、HubSpot、Zoho、Odoo CRM 是代表产品。
---

# CRM 客户关系管理

## 定义

客户关系管理(Customer Relationship Management, CRM)是**以客户为中心、整合企业各部门(营销、销售、服务、运营)对客户全生命周期进行管理**的商业理念与技术体系。它有两层含义:

1. **管理理念**:把客户视为最重要的长期资产,围绕客户价值最大化设计组织、流程、产品
2. **软件系统**:实施这一理念的信息化工具,代表如 Salesforce、HubSpot、Zoho、Odoo CRM、Microsoft Dynamics

## 核心要点

### 客户全生命周期

```
潜在客户 → 销售线索 → 商机 → 客户 → 复购客户 → 流失/挽回
   ↓        ↓        ↓      ↓       ↓
 营销引流  线索资格  销售跟踪  交付  客户成功
```

CRM 系统在每个阶段提供工具:

- **营销自动化**:邮件营销、广告归因、Landing Page、表单
- **销售管道**:商机阶段、概率、预期金额、跟进活动
- **客户服务**:工单、SLA、知识库、客户满意度
- **客户成功**:健康分、续约预测、增购机会
- **数据分析**:漏斗、留存、CLV、流失原因

### 三大类 CRM

| 类型 | 重点 | 代表 |
|---|---|---|
| 操作型 (Operational) | 自动化前台流程 | Salesforce Sales Cloud、Odoo CRM |
| 分析型 (Analytical) | 客户数据挖掘与洞察 | SAS Customer Intelligence |
| 协作型 (Collaborative) | 跨部门客户视图共享 | HubSpot CRM(免费版主推) |

现代 CRM 多为综合型,三类并重。

### 核心数据对象

- **联系人(Contact)**:个人,通常隶属于某客户
- **客户(Account)**:企业实体,可有多个联系人
- **线索(Lead)**:尚未确认价值的潜在客户
- **商机(Opportunity / Deal)**:已识别的购买意向,有阶段、金额、概率
- **活动(Activity)**:电话、邮件、会议、任务
- **工单(Ticket / Case)**:客户服务请求

### 关键指标

- 客户终生价值([[LTV]])
- 客户获取成本(CAC)
- LTV/CAC 比值,健康值 ≥ 3
- 销售周期长度
- 商机转化率
- 客户留存率与流失率
- 客户满意度(NPS、CSAT)

### 与 ERP、营销自动化的关系

| 系统 | 主要关注 |
|---|---|
| CRM | 客户、销售、服务流程 |
| ERP(如 [[Odoo模块体系|Odoo]]) | 财务、库存、生产、HR |
| 营销自动化(MA) | 引流、培育、归因 |
| CDP(客户数据平台) | 多渠道客户数据统一 |

边界日益模糊:Salesforce 收购 Pardot/Marketing Cloud,HubSpot 同时做 CRM 与 MA,[[Odoo模块体系|Odoo]] 一套同时含 CRM + ERP。

## 和其他概念的关系

CRM 是 [[营销定义与本质]] 中「以客户为中心」理念的工程化落地,与 [[消费者行为]]、[[品牌定位]]、[[STP分析]] 共同支撑营销战略。

[[销售管理]]、[[客户分层]]、[[客户复购]] 是 CRM 的核心实施场景;[[精准营销]]、[[个性化推荐]] 依赖 CRM 提供的客户画像与历史行为数据。

[[Odoo模块体系]] 中 CRM 是核心模块之一,与销售、库存、会计模块联动;典型 ERP 体系下 CRM 数据驱动整个企业的运营节奏。

[[私域流量]] 与 CRM 在中国商业语境下高度重合——本质都是把客户「装进」企业的可管理池子,通过持续触达提升复购与口碑。

## 参考源

- raw/营销/
- raw/商业管理学/
- Paul Greenberg《CRM at the Speed of Light》
- Salesforce、HubSpot、Odoo 文档
