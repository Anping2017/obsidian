---
title: Odoo ORM
type: concept
tags: [erp, mature]
sources: [raw/Odoo/02-理解掌握层/01-核心概念/ORM模型机制.md, raw/Odoo/02-理解掌握层/01-核心概念/字段类型详解.md, raw/Odoo/02-理解掌握层/01-核心概念/计算字段机制.md, raw/Odoo/02-理解掌握层/01-核心概念/关系映射机制.md]
created: 2026-05-05
updated: 2026-05-05
summary: Odoo ORM 是 Python 对象到 PostgreSQL 表的映射层,通过 models.Model + fields + decorators 抽象数据访问,支持继承、计算字段、关系字段、约束、缓存。
---

# Odoo ORM

## 定义

Odoo ORM(Object-Relational Mapping)是 Odoo 的数据访问核心,把数据库表抽象为 Python 类、把记录抽象为 recordset。开发者几乎不写 SQL,通过 `search`、`browse`、`create`、`write`、`unlink` 等高级 API 即可操作数据。理解 Odoo ORM 是开发任何 [[Odoo模块体系]] 中模块的第一步。

## 核心要点

### 模型定义

```python
class SaleOrder(models.Model):
    _name = 'sale.order'
    _description = '销售订单'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_order desc'
    _rec_name = 'name'
    
    name = fields.Char('订单号', required=True)
    partner_id = fields.Many2one('res.partner', string='客户')
    order_line = fields.One2many('sale.order.line', 'order_id')
    amount_total = fields.Float(compute='_compute_total', store=True)
```

每个类对应一张表,每个 `fields.*` 对应一列(关系字段除外)。

### 字段类型

- **基础**:`Char`、`Text`、`Html`、`Integer`、`Float`、`Boolean`、`Date`、`Datetime`、`Selection`、`Binary`、`Monetary`
- **关系**:`Many2one`(N→1 外键)、`One2many`(1→N 反向)、`Many2many`(M→N 中间表)
- **计算字段**:`compute='_method'`,可加 `store=True` 持久化
- **关联字段**:`related='partner_id.country_id.name'`

### 三种继承

| 类型 | 关键字 | 作用 |
|---|---|---|
| 经典继承 | `_inherit = 'sale.order'` | 扩展现有模型,加字段/方法,**同表** |
| 委托继承 | `_inherits = {'res.partner': 'partner_id'}` | 自动暴露父模型字段,**多表** |
| 抽象继承 | `_inherit = 'mail.thread'` | mixin,只复用功能 |

### 装饰器

- `@api.depends('field1', 'field2')`:计算字段依赖
- `@api.constrains('field')`:Python 级约束
- `@api.onchange('field')`:表单字段变化时触发
- `@api.model`:类方法
- `@api.returns('self')`:返回 recordset

### 查询 API

```python
# search:返回 recordset
orders = self.env['sale.order'].search([('state','=','sale')], limit=10)

# browse:已知 ID
order = self.env['sale.order'].browse(42)

# 链式
amounts = orders.mapped('amount_total')
big = orders.filtered(lambda o: o.amount_total > 1000)
```

域(domain)语法是 Polish notation 列表:`['|', cond1, '&', cond2, cond3]`。

### 缓存与性能

ORM 内置 prefetch 机制,访问 recordset 中第一条记录的字段时,会自动预加载整个 recordset 同字段,避免 N+1 查询。理解这一点是 Odoo 性能优化的关键。

### 与 Django ORM 的差异

- Odoo 不需要 migration 文件,模型变更自动反映到 DB(开发期)
- 字段以**类属性**而非 Field 对象的方式声明
- 继承机制远比 Django 强大,但学习曲线更陡

## 关系

- 是 [[Odoo模块体系]] 中 `models/` 目录的核心
- 配合 [[Odoo视图体系]] 把数据呈现给用户
- 通过 [[Odoo安全模型]] 控制字段/记录可见性

## 参考源

- raw/Odoo/02-理解掌握层/01-核心概念/ORM模型机制.md
- raw/Odoo/02-理解掌握层/01-核心概念/字段类型详解.md
- raw/Odoo/02-理解掌握层/01-核心概念/计算字段机制.md
- raw/Odoo/02-理解掌握层/01-核心概念/关系映射机制.md
