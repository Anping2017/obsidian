---
title: Odoo 报表引擎
type: concept
tags: [erp, mature]
sources: [raw/Odoo/03-应用实践层/03-报表开发/报表开发基础.md, raw/Odoo/03-应用实践层/03-报表开发/QWeb报表定制.md, raw/Odoo/03-应用实践层/03-报表开发/外部报表集成.md]
created: 2026-05-05
updated: 2026-05-05
summary: Odoo 报表引擎基于 QWeb 模板 + wkhtmltopdf 渲染,支持 PDF、HTML、Excel 输出,通过 AbstractModel 提供数据,template + report record 定义样式。
---

# Odoo 报表引擎

## 定义

Odoo 报表引擎(Report Engine)是把 [[Odoo ORM]] 中的数据按指定模板生成 PDF/HTML/Excel 文档的子系统。它服务于发票、报价单、采购单、装箱单、工资条、财务报表等所有"打印件"场景,是企业 ERP 必不可少的输出层。

## 核心要点

### 技术栈

- **数据层**:`AbstractModel`(继承 `report.<module>.<template>`)的 `_get_report_values` 方法返回上下文
- **模板层**:[[QWeb模板引擎]],基于 XML,支持循环、条件、表达式
- **渲染层**:`wkhtmltopdf` 把 HTML 转 PDF;Excel 用 `xlsxwriter`/`xlwt`
- **配置层**:`ir.actions.report` 记录绑定模板与模型,定义输出格式

### 一个最小报表

数据模型:
```python
class SimpleReport(models.AbstractModel):
    _name = 'report.my_module.simple_report'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'docs': self.env['my.model'].browse(docids),
            'company': self.env.company,
        }
```

QWeb 模板:
```xml
<template id="simple_report_template">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="doc">
            <t t-call="web.external_layout">
                <div class="page">
                    <h2 t-field="doc.name"/>
                    <p>金额: <span t-field="doc.amount"/></p>
                </div>
            </t>
        </t>
    </t>
</template>
```

报表 action:
```xml
<record id="action_simple_report" model="ir.actions.report">
    <field name="name">简单报表</field>
    <field name="model">my.model</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">my_module.simple_report_template</field>
</record>
```

### QWeb 关键指令

- `t-foreach="list" t-as="item"`:循环
- `t-if="cond"`:条件
- `t-field="record.name"`:字段输出(自动格式化货币、日期)
- `t-esc="expr"`:Python 表达式
- `t-call="template_id"`:调用其他模板
- `t-att-class="..."`:动态属性

### 标准布局

`web.external_layout` 提供页眉/页脚框架,自动嵌入公司 Logo、地址、页码。开发者只需关注 `class="page"` 内的内容。

### 财务/会计专用

`account` 模块内置大量动态报表(资产负债表、利润表、现金流表),支持期间过滤、对比期、向下钻取。这些不走 QWeb,用专门的 `account.financial.html.report` 实现,EE 版还有 PDF/Excel 双输出。

### Excel 报表

通过继承 `report.report_xlsx.abstract` (社区模块 `report_xlsx`)实现,提供 `generate_xlsx_report(workbook, data, objects)` 钩子,直接操作 xlsxwriter API。

### 第三方集成

可推送到 Jasper、Crystal Reports 或外部 BI(Metabase、Superset),通常通过 `psql` 视图或 [[Odoo模块体系]] 的 REST API。

## 关系

- 数据来自 [[Odoo ORM]]
- 模板用 [[QWeb模板引擎]],与 [[Odoo视图体系]] 共享
- 受 [[Odoo安全模型]] 限制,无权用户无法触发对应报表

## 参考源

- raw/Odoo/03-应用实践层/03-报表开发/报表开发基础.md
- raw/Odoo/03-应用实践层/03-报表开发/QWeb报表定制.md
- raw/Odoo/03-应用实践层/03-报表开发/外部报表集成.md
