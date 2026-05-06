---
title: Odoo 模块体系
type: topic
tags: [erp, mature]
sources: [raw/Odoo/01-基础认知层/01-概念与架构/Odoo架构详解.md, raw/Odoo/01-基础认知层/01-概念与架构/模块化设计理念.md, raw/Odoo/01-基础认知层/01-概念与架构/Odoo概述.md]
created: 2026-05-05
updated: 2026-05-05
summary: Odoo 通过模块(Module)实现 ERP 全功能解耦,每个模块包含 manifest、models、views、security、data 五大要素,通过 depends 关系组装为完整业务系统。
---

# Odoo 模块体系

## 概述

Odoo 是基于 Python + PostgreSQL 的开源 ERP/CRM 套件,前身是 2005 年的 TinyERP,经 OpenERP(2008)、Odoo(2014)演进至今。它最显著的设计选择是 **以"模块"作为最小功能单元**——销售、采购、库存、会计、HR、CRM、网站、电商等所有功能都是独立模块,按需安装、自由组合。这与 SAP/Oracle 那种"一体化大型套件"形成根本对比。

## 多角度分析

### 模块的物理结构

一个标准模块就是一个目录:

```
my_module/
├── __manifest__.py      # 元信息 + 依赖声明
├── __init__.py          # Python 包入口
├── models/              # 数据模型(继承 models.Model)
├── views/               # XML 定义的视图(form/tree/kanban)
├── security/            # ir.model.access.csv 权限
├── data/                # 初始数据 / 演示数据
├── static/              # 前端资源(JS/CSS/图标)
└── i18n/                # 多语言 .po 文件
```

`__manifest__.py` 是元信息中枢,声明 `depends`(依赖的其他模块)、`data`(要加载的 XML/CSV)、`installable`(是否可装)、`application`(是否作为顶级应用展示)。

### 核心业务模块簇

Odoo 官方与社区维护的核心模块按业务域聚类:

| 业务域 | 核心模块 | 关键模型 |
|---|---|---|
| 销售 | `sale`, `sale_management` | `sale.order`, `sale.order.line` |
| 采购 | `purchase` | `purchase.order` |
| 库存 | `stock` | `stock.picking`, `stock.move`, `stock.quant` |
| 制造 | `mrp` | `mrp.production`, `mrp.bom` |
| 会计 | `account` | `account.move`, `account.journal` |
| HR | `hr`, `hr_payroll`, `hr_attendance` | `hr.employee`, `hr.contract` |
| CRM | `crm` | `crm.lead`, `crm.team` |
| 项目 | `project` | `project.project`, `project.task` |
| 网站/电商 | `website`, `website_sale` | `website`, `product.template` |

模块之间通过 `depends` 形成有向无环图。例如 `sale_stock` 让销售订单触发出库,依赖 `sale` 和 `stock`。

### 模块继承机制

[[Odoo ORM]] 提供三种继承:
- **`_inherit = 'sale.order'`**(经典继承):扩展现有模型,添加字段或方法
- **`_inherits = {...}`**(委托继承):新模型自动包含父模型字段
- **新建模型**:`_name = 'my.model'`

视图也支持 XPath 继承,可以在不修改原模块的前提下,在指定位置插入/替换/删除 XML 节点。这种"非破坏性扩展"是 Odoo 二次开发的灵魂。

### Community vs Enterprise

- **社区版(CE)**:LGPLv3,完全开源,核心 ERP 功能齐全
- **企业版(EE)**:商业授权,额外提供高级会计(IFRS、巴西/法国本地化)、移动 App、专业服务支持、文档管理、营销自动化等模块

很多功能(如 OCR 发票识别、3D BoM)只在企业版,这是 Odoo SA 的主要营收来源。

### 第三方生态

OCA(Odoo Community Association)维护着数千个免费模块,涵盖财务税务本地化、行业垂直、HR 扩展等。商业市场 Odoo Apps Store 提供付费模块。模块化设计让 Odoo 成为目前最灵活的开源 ERP。

## 结论

Odoo 模块体系的真正价值不在"模块多",而在**模块化作为一种 ERP 哲学的彻底贯彻**。它让一个小公司可以只装 `sale + invoice + crm` 三个模块跑起来,后续按需加 `stock`、`mrp`、`hr_payroll`,而无需买下完整套件。理解 Odoo,就是理解"先解耦再组装"如何在企业软件领域落地。下游知识包括 [[Odoo ORM]]、[[Odoo视图体系]]、[[Odoo工作流]]、[[Odoo安全模型]]、[[Odoo报表引擎]]。

## 参考源

- raw/Odoo/01-基础认知层/01-概念与架构/Odoo架构详解.md
- raw/Odoo/01-基础认知层/01-概念与架构/模块化设计理念.md
- raw/Odoo/01-基础认知层/01-概念与架构/Odoo概述.md
