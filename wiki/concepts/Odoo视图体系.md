---
title: Odoo 视图体系
type: concept
tags: [erp, mature]
sources: [raw/Odoo/03-应用实践层/02-视图开发/视图开发基础.md, raw/Odoo/03-应用实践层/02-视图开发/视图继承机制.md, raw/Odoo/03-应用实践层/02-视图开发/自定义视图组件.md]
created: 2026-05-05
updated: 2026-05-05
summary: Odoo 视图通过 XML 声明式定义,主要类型包括 form、tree、kanban、search、graph、pivot、calendar,支持 XPath 继承机制,前端由 OWL 框架 + QWeb 模板渲染。
---

# Odoo 视图体系

## 定义

Odoo 视图(View)是把 [[Odoo ORM]] 中的数据展现给用户的 UI 层。视图采用**声明式 XML** 定义,后端解析后由前端 OWL 组件 + QWeb 模板渲染。一个模型通常配多种视图,用户切换查看方式而无需重写后端。这种"模型一份,视图多种"的设计,是 [[Odoo模块体系]] 用户体验的灵活基础。

## 核心要点

### 主要视图类型

| 类型 | 用途 | 典型场景 |
|---|---|---|
| `form` | 单条记录详细编辑 | 销售订单表单 |
| `tree` | 列表浏览 | 订单列表 |
| `kanban` | 看板卡片 | CRM 销售漏斗、Project 任务 |
| `search` | 过滤器、分组 | 列表上方搜索区 |
| `graph` | 折线/柱状/饼图 | 销售分析 |
| `pivot` | 透视表 | 多维数据汇总 |
| `calendar` | 日历 | 日程、休假 |
| `gantt` | 甘特图(EE) | 项目进度 |
| `map` | 地图(EE) | 客户分布 |
| `activity` | 活动列表 | 待办、跟进 |

### 视图定义示例

```xml
<record id="view_my_form" model="ir.ui.view">
    <field name="name">my.model.form</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <form>
            <header>
                <button name="action_confirm" string="确认" type="object" 
                        states="draft" class="oe_highlight"/>
                <field name="state" widget="statusbar"/>
            </header>
            <sheet>
                <group>
                    <field name="name"/>
                    <field name="partner_id"/>
                </group>
                <notebook>
                    <page string="明细">
                        <field name="line_ids"/>
                    </page>
                </notebook>
            </sheet>
        </form>
    </field>
</record>
```

### XPath 继承

不修改原视图,通过 XPath 在指定节点 **插入(after/before/inside) / 替换(replace) / 属性修改(attributes)**:

```xml
<record id="view_partner_form_inherit" model="ir.ui.view">
    <field name="inherit_id" ref="base.view_partner_form"/>
    <field name="arch" type="xml">
        <xpath expr="//notebook" position="inside">
            <page string="自定义">
                <field name="my_custom_field"/>
            </page>
        </xpath>
    </field>
</record>
```

这是 Odoo "非破坏性二次开发" 的关键机制,允许第三方模块扩展核心模块视图而不污染源码。

### 视图属性

- `attrs`:基于其他字段值动态控制 invisible/required/readonly(Odoo 17+ 简化为 `invisible="state == 'draft'"` 直写)
- `widget`:覆盖默认渲染,如 `widget="badge"`、`widget="statusbar"`、`widget="many2many_tags"`
- `decoration-*`:列表行根据条件着色
- `optional`:列表列可隐藏/显示

### 前端架构演进

- **2005-2014**:GTK 桌面客户端
- **2015-2021**:Web 客户端基于自研 Backbone-like 框架
- **2022+**:迁移到 **OWL**(Odoo Web Library),响应式、组件化、TypeScript 友好

## 关系

- 渲染来自 [[Odoo ORM]] 的数据
- 是 [[Odoo模块体系]] 中 `views/` 目录的产物
- 受 [[Odoo安全模型]] 字段级权限影响,无权字段会被隐藏

## 参考源

- raw/Odoo/03-应用实践层/02-视图开发/视图开发基础.md
- raw/Odoo/03-应用实践层/02-视图开发/视图继承机制.md
- raw/Odoo/03-应用实践层/02-视图开发/自定义视图组件.md
