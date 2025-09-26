

# 🎯 Odoo 17 装饰器完全教程


![Odoo](https://img.shields.io/badge/Odoo-17.0-714B7B?style=for-the-badge&logo=odoo&logoColor=white)

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)

![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

  
## 掌握Odoo装饰器，提升开发效率 🚀
  
---

## 🎯 什么是装饰器

> **装饰器（Decorator）** 是Python中的一个重要概念，它允许我们在不修改原函数代码的情况下，为函数添加额外的功能。


在Odoo中，装饰器被广泛用于增强模型方法的功能，是Odoo开发的核心技术之一。


### 🔍 核心概念

```python
# 基础装饰器示例
@api.model
def my_method(self):
    """这是一个被装饰的方法"""
    pass
```

  

---

  

## ⚡ Odoo中装饰器的作用

在Odoo开发中，装饰器主要用于以下场景：

| 功能            | 描述        | 装饰器                        |
| ------------- | --------- | -------------------------- |
| 🎮 **控制调用方式** | 定义方法的调用模式 | `@api.model`, `@api.multi` |
| 🔗 **依赖关系管理** | 字段间的自动计算  | `@api.depends`             |
| 🖥️ **界面交互**  | 用户操作响应    | `@api.onchange`            |
| ✅ **数据验证**    | 约束和验证     | `@api.constrains`          |
| ⚡ **性能优化**    | 缓存和批量处理   | `@api.model_create_multi`  |

---

## 🔧 常用装饰器详解

### @api.model

> **用途**：用于不涉及特定记录的方法，通常用于类级别的操作。

#### ✨ 特点

- 🎯 方法不会接收记录集作为self

- 🔧 通常用于创建、搜索、工具方法等

- ⚡ 性能优化，避免不必要的记录集传递

#### 📝 示例

```python

from odoo import models, api, fields

  

class ProductTemplate(models.Model):
    _name = 'product.template'

    @api.model

    def get_default_category(self):
        """获取默认商品类别"""
        return self.env['product.category'].search([('name', '=', '默认类别')], limit=1)

    @api.model
    def create_product_batch(self, products_data):
        """批量创建商品"""
        created_products = []
        for product_data in products_data:
            product = self.create(product_data)
            created_products.append(product)
        return created_products

```

---
### @api.depends


> **用途**：声明计算字段的依赖关系，当依赖字段变化时自动重新计算。

#### ✨ 特点

- 🔄 用于computed字段

- 🔗 可以依赖多个字段

- 🌐 支持关联字段的依赖

- ⚡ 自动缓存和更新

#### 📝 示例

```python

class SaleOrder(models.Model):

    _name = 'sale.order'

    order_line = fields.One2many('sale.order.line', 'order_id', string='订单行')

    amount_untaxed = fields.Float('未税金额', compute='_compute_amount')

    amount_tax = fields.Float('税额', compute='_compute_amount')

    amount_total = fields.Float('总金额', compute='_compute_amount')

    @api.depends('order_line.price_subtotal', 'order_line.price_tax')

    def _compute_amount(self):
        """计算订单金额"""
        for order in self:
            order.amount_untaxed = sum(line.price_subtotal for line in order.order_line)
            order.amount_tax = sum(line.price_tax for line in order.order_line)
            order.amount_total = order.amount_untaxed + order.amount_tax

```

---
### @api.onchange

> **用途**：在用户界面中，当指定字段值改变时触发方法执行。

#### ✨ 特点

- 🖥️ 只在用户界面中生效

- 🔄 可以修改其他字段的值

- ⚠️ 可以显示警告信息

- 🎯 实时响应用户操作

#### 📝 示例

```python

class SaleOrderLine(models.Model):

    _name = 'sale.order.line'

    product_id = fields.Many2one('product.product', '商品')

    product_uom_qty = fields.Float('数量', default=1.0)

    price_unit = fields.Float('单价')

    discount = fields.Float('折扣')

    price_subtotal = fields.Float('小计', compute='_compute_amount')

    @api.onchange('product_id')

    def _onchange_product_id(self):

        """当商品改变时，自动填充相关信息"""

        if self.product_id:

            self.price_unit = self.product_id.list_price

            self.name = self.product_id.name

            # 返回警告信息

            if not self.product_id.active:

                return {

                    'warning': {

                        'title': '警告',

                        'message': '所选商品已停用，请选择其他商品。'

                    }

                }

    @api.onchange('product_uom_qty', 'price_unit', 'discount')

    def _onchange_discount(self):

        """当数量、单价或折扣改变时，给出建议"""

        if self.product_uom_qty >= 100:

            return {

                'warning': {

                    'title': '批量采购建议',

                    'message': f'您购买了{self.product_uom_qty}件商品，建议联系销售获取更好的价格。'

                }

            }

```

---
### @api.constrains

> **用途**：定义约束条件，在记录创建或更新时进行数据验证。

#### ✨ 特点

- 💾 在保存记录时执行

- ❌ 验证失败会抛出异常

- 🔗 可以同时约束多个字段

- 🛡️ 保证数据完整性


#### 📝 示例

```python

from odoo.exceptions import ValidationError

  

class Employee(models.Model):

    _name = 'hr.employee'

    name = fields.Char('姓名', required=True)

    age = fields.Integer('年龄')

    salary = fields.Float('薪资')

    email = fields.Char('邮箱')

    @api.constrains('age')

    def _check_age(self):

        """检查年龄有效性"""

        for employee in self:

            if employee.age < 18 or employee.age > 65:

                raise ValidationError('员工年龄必须在18-65岁之间。')

    @api.constrains('salary')

    def _check_salary(self):

        """检查薪资有效性"""

        for employee in self:

            if employee.salary <= 0:

                raise ValidationError('员工薪资必须大于0。')

    @api.constrains('email')

    def _check_email_unique(self):

        """检查邮箱唯一性"""

        for employee in self:

            if employee.email:

                existing = self.search([

                    ('email', '=', employee.email),

                    ('id', '!=', employee.id)

                ])

                if existing:

                    raise ValidationError(f'邮箱 {employee.email} 已被其他员工使用。')

```

---
### @api.model_create_multi

> **用途**：用于批量创建记录的优化方法。

#### ✨ 特点

- ⚡ 性能优化，批量处理

- 🔄 支持预处理和后处理逻辑

- 📦 减少数据库查询次数

#### 📝 示例

```python

class ProductProduct(models.Model):

    _name = 'product.product'

    @api.model_create_multi

    def create(self, vals_list):

        """批量创建商品时的自定义逻辑"""

        # 在创建前预处理数据

        for vals in vals_list:

            if 'default_code' not in vals:

                vals['default_code'] = self._generate_default_code()

        # 调用父类方法创建记录

        products = super().create(vals_list)

        # 创建后的处理逻辑

        for product in products:

            product._update_related_data()

        return products

    def _generate_default_code(self):

        """生成默认编码"""

        sequence = self.env['ir.sequence'].next_by_code('product.code')

        return f'PROD{sequence}'

```

---
### @api.returns

> **用途**：指定方法的返回类型，用于API一致性。

#### ✨ 特点

- 🎯 定义方法返回类型

- 🔄 保持API一致性

- 📝 提高代码可读性

#### 📝 示例

```python

class ResPartner(models.Model):

    _name = 'res.partner'

    @api.returns('self', lambda value: value.id)

    def copy(self, default=None):

        """复制客户记录"""

        default = dict(default or {})

        default.update({

            'name': f"{self.name} (副本)",

            'email': False,  # 邮箱不复制

        })

        return super().copy(default)

```

---

## 💼 实际应用示例


### 🛒 完整的销售订单示例
  
> 这个示例展示了如何在实际业务场景中综合使用多种装饰器

```python

from odoo import models, fields, api

from odoo.exceptions import ValidationError

from datetime import datetime, timedelta

  

class SaleOrder(models.Model):

    _name = 'sale.order'

    _description = '销售订单'

    # 基础字段

    name = fields.Char('订单号', required=True, copy=False, default='新订单')

    partner_id = fields.Many2one('res.partner', '客户', required=True)

    date_order = fields.Datetime('订单日期', default=fields.Datetime.now)

    validity_date = fields.Date('有效期', compute='_compute_validity_date', store=True)

    # 订单行

    order_line = fields.One2many('sale.order.line', 'order_id', '订单行')

    # 金额字段

    amount_untaxed = fields.Float('未税金额', compute='_compute_amounts', store=True)

    amount_tax = fields.Float('税额', compute='_compute_amounts', store=True)

    amount_total = fields.Float('总金额', compute='_compute_amounts', store=True)

    # 状态字段

    state = fields.Selection([

        ('draft', '草稿'),

        ('sent', '已发送'),

        ('sale', '销售订单'),

        ('done', '已完成'),

        ('cancel', '已取消'),

    ], default='draft', string='状态')

    @api.model

    def create(self, vals):

        """创建订单时自动生成订单号"""

        if vals.get('name', '新订单') == '新订单':

            vals['name'] = self.env['ir.sequence'].next_by_code('sale.order') or '新订单'

        return super().create(vals)

    @api.depends('date_order')

    def _compute_validity_date(self):

        """计算订单有效期（默认30天）"""

        for order in self:

            if order.date_order:

                order.validity_date = order.date_order.date() + timedelta(days=30)

            else:

                order.validity_date = False

    @api.depends('order_line.price_subtotal', 'order_line.price_tax')

    def _compute_amounts(self):

        """计算订单总金额"""

        for order in self:

            order.amount_untaxed = sum(order.order_line.mapped('price_subtotal'))

            order.amount_tax = sum(order.order_line.mapped('price_tax'))

            order.amount_total = order.amount_untaxed + order.amount_tax

    @api.onchange('partner_id')

    def _onchange_partner_id(self):

        """客户改变时的处理"""

        if self.partner_id:

            # 检查客户信用状态

            if self.partner_id.credit_limit > 0 and self.partner_id.credit > self.partner_id.credit_limit:

                return {

                    'warning': {

                        'title': '信用警告',

                        'message': f'客户 {self.partner_id.name} 已超出信用额度，当前欠款：{self.partner_id.credit}'

                    }

                }

    @api.constrains('order_line')

    def _check_order_line(self):

        """检查订单行不能为空"""

        for order in self:

            if order.state in ('sale', 'done') and not order.order_line:

                raise ValidationError('销售订单必须包含至少一个订单行。')

    @api.constrains('amount_total')

    def _check_amount_total(self):

        """检查订单总金额"""

        for order in self:

            if order.amount_total < 0:

                raise ValidationError('订单总金额不能为负数。')

    def action_confirm(self):

        """确认订单"""

        for order in self:

            if not order.order_line:

                raise ValidationError('不能确认空订单。')

            order.state = 'sale'

        return True

```

---

## ⭐ 最佳实践

### 🚀 1. 性能优化建议

```python

# ✅ 好的实践：批量处理

@api.depends('line_ids.amount')

def _compute_total(self):

    for record in self:

        record.total = sum(record.line_ids.mapped('amount'))

  

# ❌ 避免：在循环中进行数据库查询

@api.depends('partner_id')

def _compute_partner_info(self):

    for record in self:

        # 避免在循环中查询数据库

        partners = self.env['res.partner'].search([('id', '=', record.partner_id.id)])

```

### 🔗 2. 依赖关系管理

```python

# ✅ 正确的依赖声明

@api.depends('order_line.product_id', 'order_line.price_unit', 'order_line.product_uom_qty')

def _compute_amount_total(self):

    for order in self:

        order.amount_total = sum(line.price_subtotal for line in order.order_line)

  

# ✅ 支持嵌套依赖

@api.depends('partner_id.country_id.code')

def _compute_tax_region(self):

    for record in self:

        record.tax_region = record.partner_id.country_id.code or 'DEFAULT'

```

### 🛡️ 3. 错误处理

```python

@api.constrains('email')

def _check_email_format(self):

    """检查邮箱格式"""

    import re

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    for record in self:

        if record.email and not re.match(email_pattern, record.email):

            raise ValidationError(f'邮箱格式不正确：{record.email}')

```

---

## ❓ 常见问题

### ❓ Q1: @api.depends 和 @api.onchange 的区别？


**A**:

- `@api.depends`: 用于计算字段，在后端自动计算，数据会存储到数据库

- `@api.onchange`: 用于用户界面交互，只在前端表单中生效，不存储到数据库


### ❓ Q2: 如何避免循环依赖？
**A**:

```python

# ❌ 错误：循环依赖

@api.depends('field_b')

def _compute_field_a(self):

    self.field_a = self.field_b * 2

  

@api.depends('field_a')  # 这会造成循环依赖

def _compute_field_b(self):

    self.field_b = self.field_a / 2

  

# ✅ 正确：使用基础字段作为依赖

@api.depends('base_value')

def _compute_field_a(self):

    self.field_a = self.base_value * 2

  

@api.depends('base_value')

def _compute_field_b(self):

    self.field_b = self.base_value / 2

```


### ❓ Q3: 装饰器的执行顺序？

**A**: 装饰器按照从下到上的顺序执行：

```python

@api.multi        # 第二个执行

@api.depends('field1')  # 第一个执行

def _compute_field(self):

    pass

```


### ❓ Q4: 如何调试装饰器相关的问题？

**A**:

1. **使用日志记录**：

```python

import logging

_logger = logging.getLogger(__name__)

  

@api.depends('field1')

def _compute_field(self):

    _logger.info(f'Computing field for records: {self.ids}')

    # 计算逻辑

```

  

2. **检查字段依赖**：在Odoo调试模式下查看字段的依赖关系

3. **使用Odoo shell进行测试**：

```bash

# 启动Odoo shell

python3 odoo-bin shell -d your_database

  

# 测试装饰器方法

>>> order = env['sale.order'].browse(1)

>>> order._compute_amounts()

```

---
## 📝 总结

Odoo 17的装饰器是开发高质量模块的关键工具。通过合理使用这些装饰器，您可以：


### 🎯 核心优势

  

| 优势              | 描述           | 实现方式                              |
| --------------- | ------------ | --------------------------------- |
| 🔧 **提高可维护性**   | 清晰的依赖关系和约束条件 | `@api.depends`, `@api.constrains` |
| 🎨 **增强用户体验**   | 实时的字段计算和界面交互 | `@api.onchange`, `@api.depends`   |
| 🛡️ **保证数据完整性** | 有效的数据验证和约束   | `@api.constrains`                 |
| ⚡ **优化性能**      | 合理的计算和缓存策略   | `@api.model_create_multi`         |

  

### 📋 使用要点

记住，好的装饰器使用需要：

- ✅ **明确的依赖关系声明**

- ✅ **适当的错误处理**

- ✅ **性能考虑**

- ✅ **充分的测试**

  

### 🚀 下一步学习

- 📖 深入学习Odoo ORM机制

- 🔍 探索更多高级装饰器

- 💼 在实际项目中应用这些概念

- 🧪 编写单元测试验证装饰器行为

---

**希望这个教程能帮助您更好地掌握Odoo 17中装饰器的使用！** 🎉

![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)

  

