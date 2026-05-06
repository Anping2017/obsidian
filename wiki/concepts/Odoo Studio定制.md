---
title: Odoo Studio 定制
type: concept
tags: [odoo, mature]
sources: [raw/Odoo/]
created: 2026-05-05
updated: 2026-05-05
summary: Odoo Studio 是企业版独有的可视化定制工具,允许非开发者通过拖拽创建模型字段、视图、菜单、报表、自动化规则,降低 Odoo 定制门槛,但底层仍生成可被开发者读懂的 Python 模块。
---

# Odoo Studio 定制

## 定义

Odoo Studio 是 Odoo 企业版(Enterprise Edition)中独有的低代码 / 无代码定制工具,允许业务用户通过浏览器界面直接修改 Odoo 应用——添加字段、改视图、创建报表、设计审批流程、生成新模型——无需写 Python 或 XML 代码。

它是 Odoo 区分企业版与社区版的关键差异点之一,直接对标 Salesforce 的 Setup / Process Builder、Microsoft Dynamics 的 Power Platform。

## 核心能力

**模型层定制**

- 添加字段:文本、日期、关系、计算等十多种类型
- 编辑现有字段:必填、只读、缺省值、Tooltip
- 创建新模型(自定义应用):无需代码定义新业务对象

**视图层定制**

- Form 视图:拖拽分组、Tab、字段排列
- Tree 视图:列添加、排序、统计
- Kanban 视图:卡片样式、状态色
- Pivot / Graph:数据透视、图表
- Calendar / Map / Search:其他视图

**菜单与权限**

- 顶部菜单、侧边菜单层级
- 权限组(Group)分配
- 字段级访问控制

**报表与文档**

- PDF 报表设计器(基于 QWeb)
- 拖拽方式编辑模板
- 客户邮件、合同、发票模板

**自动化规则(Automated Actions)**

- 触发条件:记录创建/更新、字段变化、定时
- 操作:发送邮件、创建活动、更新字段、调用 Python 代码
- 结合 [[Odoo工作流]] 设计审批

**Approval Studio**

- 设计多级审批流程
- 角色授权
- 条件分支

## 工作流程

**典型场景:为采购订单加"供应商评级"字段**

1. 进入采购订单,点击 Studio 按钮(右上扳手图标)
2. 在 Form 视图添加新字段"评级",选择类型 Selection(优秀/良好/一般/差)
3. 设置默认值、布局位置
4. 保存,字段立即生效
5. 在 Tree 视图加该列
6. 配置 Automated Action:订单审批时自动检查评级,差则触发审批

整个过程 5-10 分钟,无需开发者介入。

## 底层实现

Studio 在背后实际生成 Odoo 标准模块代码:

- 字段定义存于 ir.model.fields
- 视图存为 ir.ui.view 记录
- 报表存为 ir.actions.report
- 模板存为 ir.ui.view(QWeb 类型)

**导出为模块**

Studio 创建的所有定制可一键"Export"为 .zip 模块,移植到其他 Odoo 实例或交开发者审查。这是 Studio 与纯 SaaS 低代码工具的关键差别——产生的代码是开放可读、可版本化的。

**与代码定制并存**

Studio 的修改与开发者写的模块和谐共存。开发者可"接收 Studio 输出 + 手写代码补充复杂逻辑",企业内部业务人员先用 Studio 试错,确定后由开发者优化为正式模块。

## 与社区版的对比

社区版(LGPLv3 免费)无 Studio,定制需:
- 写 Python + XML 模块
- 用 Form Builder 等社区第三方模块
- 配合开发者团队

企业版(商业授权)Studio 是核心 SaaS 增值,大幅降低定制门槛。

这是中小企业选 Odoo 时,从社区版 vs 企业版的关键决策点之一。

## 与 Salesforce 对比

| 维度 | Odoo Studio | Salesforce Setup/Lightning App Builder |
|---|---|---|
| 价格 | 包含在 Enterprise 订阅 | 按用户/功能分级订阅 |
| 范围 | 全 ERP(财务/库存/HR/电商) | 主 CRM,部分 ERP 通过 AppExchange |
| 代码可移植 | 导出为 Python 模块,完全开源 | 部分元数据可导出,但锁定生态 |
| 学习曲线 | 中等 | 中等 |
| 社区资源 | 中 | 极大 |

Salesforce 在生态深度和社区上领先,Odoo Studio 在端到端 ERP 整合和价格上有优势。

## 局限

- Studio 不能直接写 Python:复杂逻辑仍需开发者
- 部分核心模块定制有禁区(财务凭证不能随意改字段)
- 升级版本时需测试 Studio 定制兼容性
- 模型修改需慎重(数据迁移风险)
- Web Studio 不覆盖 PoS、Field Service 等少数模块

## 参考源

- raw/Odoo/
- 相关:[[Odoo模块体系]]、[[Odoo工作流]]、[[Odoo视图体系]]
