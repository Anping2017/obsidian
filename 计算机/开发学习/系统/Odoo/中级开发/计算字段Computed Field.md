# 🧮 Odoo 计算字段（Computed Fields）教程

---

## 1. 核心概念

- **计算字段（Computed Field）**：字段值不是直接存储，而是通过方法计算得出
    
- 自动追踪依赖字段的变化，实时更新
    
- 常用于金额计算、状态汇总、百分比计算等业务场景
    
### 字段计算

在 Odoo 中，计算字段（`Computed Fields`）是根据其他字段的值动态计算出来的字段，它不直接存储在数据库中，除非你显式指定 `store=True`。

#### 关键元素

- `@api.depends(...)`：这是一个装饰器，用于声明计算字段所依赖的字段。**这是 Odoo 知道何时重新计算该字段的关键**。当依赖字段的值发生变化时，Odoo 就会自动调用计算方法。
    
- `self`：在计算方法中，`self` 是一个记录集（RecordSet）。你需要通过遍历 `for record in self` 来对每条记录进行操作，这是 Odoo ORM 的标准实践。

#### 基本语法

```
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # 定义一个计算字段
    my_computed_field = fields.Float(string='My Computed Field', compute='_compute_my_field')

    # 定义计算方法
    @api.depends('field1', 'related_field.sub_field')
    def _compute_my_field(self):
        for record in self:
            # 在这里编写计算逻辑
            # record.field1 + record.related_field.sub_field
            record.my_computed_field = ...
```



---

## 2. 基本定义

- 在模型中定义字段时，使用 `compute` 参数指定计算方法
    
- **示例属性**：
    
    - `compute`: 指定计算方法
        
    - `store`: 是否存储到数据库
        
    - `readonly`: 是否只读
        
    - `depends`: 声明依赖字段（可选，但推荐）
        

---

## 3. 计算字段基本示例

**场景**：计算销售订单的利润率

- **模型字段定义**
    
    - `cost_price`：成本价
        
    - `sale_price`：销售价
        
    - `profit_margin`：利润率（计算字段）
        
- **示例代码**
    

```
from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _name = 'sale.order.line'

    cost_price = fields.Float(string="Cost Price")
    sale_price = fields.Float(string="Sale Price")
    profit_margin = fields.Float(string="Profit Margin", compute='_compute_profit_margin', store=True)

    @api.depends('cost_price', 'sale_price')
    def _compute_profit_margin(self):
        for record in self:
            if record.cost_price:
                record.profit_margin = ((record.sale_price - record.cost_price) / record.cost_price) * 100
            else:
                record.profit_margin = 0.0

```

- `@api.depends('cost_price', 'sale_price')`
    
    - 声明依赖字段
        
    - 当依赖字段发生变化时自动重新计算
        
- `store=True`
    
    - 将计算结果存储到数据库，提高搜索和过滤效率
        
    - 默认 `store=False`，结果不存储，只在内存中计算
        

---

## 4. 进阶用法

### 4.1 多依赖字段计算

```
@api.depends('field1', 'field2', 'related_model.field3')
def _compute_total(self):
    for rec in self:
        rec.total = rec.field1 + rec.field2 + (rec.related_model.field3 or 0)

```

### 4.2 调用其他模型数据

```
@api.depends('product_id')
def _compute_stock(self):
    for rec in self:
        rec.available_qty = rec.product_id.qty_available

```

### 4.3 不存储计算字段（即时计算）

`profit_margin = fields.Float(compute='_compute_profit_margin', store=False)`

- 优点：节省数据库空间
    
- 缺点：频繁访问可能性能下降
    

### 4.4 设置只读字段

`profit_margin = fields.Float(compute='_compute_profit_margin', readonly=True)`

---

## 5. 常见问题与注意事项

|问题|解决方法|
|---|---|
|计算字段不更新|确认依赖字段是否在 `@api.depends` 中声明|
|搜索和过滤不支持|设置 `store=True` 才能在视图搜索或过滤|
|性能问题|避免在循环内大量 ORM 查询，可使用 `mapped` 或 `read_group` 优化|
|依赖关系跨模型|使用 `related_model.field` 的方式声明依赖字段|

---

## 6. 实际应用场景

1. **金额计算**：订单总价、折扣后金额、利润率
    
2. **状态汇总**：任务完成百分比、项目进度
    
3. **库存管理**：可用库存量、预计库存
    
4. **销售分析**：客户总消费额、产品销售额占比
    

---

## 7. 总结

- 计算字段是 Odoo ORM 的核心功能
    
- 核心步骤：
    
    1. 定义字段 `compute='_compute_method'`
        
    2. 用 `@api.depends()` 声明依赖字段
        
    3. 在计算方法中逐条记录赋值
        
- 可选 `store=True` 优化搜索和报表性能
    
- 可以结合 `@api.onchange` 或 `@api.constrains` 使用，实现复杂业务逻辑


    

#### 示例：多级关联字段的计算

假设你想在销售订单上添加一个字段，用于显示客户的**国家名称**。


```
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # 定义一个计算字段，用于显示客户所在的国家名称
    partner_country_name = fields.Char(string='Customer Country', compute='_compute_partner_country_name')

    # 依赖于 partner_id 和 partner_id.country_id 的变化
    @api.depends('partner_id', 'partner_id.country_id')
    def _compute_partner_country_name(self):
        for record in self:
            if record.partner_id and record.partner_id.country_id:
                record.partner_country_name = record.partner_id.country_id.name
            else:
                record.partner_country_name = False
```

- `@api.depends` 中同样使用点符号 `partner_id.country_id` 来追踪依赖。
    

#### 示例：反向关联字段的计算

假设你想在 `Product` 模型上添加一个字段，用于显示**有多少个销售订单**包含了该产品。


```
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # 计算字段，用于显示包含该产品的销售订单数量
    sale_order_count = fields.Integer(
        string='Sale Order Count',
        compute='_compute_sale_order_count'
    )

    @api.depends('sale_order_line_ids') # 这里需要依赖于反向关联字段
    def _compute_sale_order_count(self):
        # sale_order_line_ids 是一个反向关联字段，指向所有包含该产品的销售订单行
        for record in self:
            record.sale_order_count = len(record.sale_order_line_ids.mapped('order_id'))
```

- `sale_order_line_ids` 是 Odoo 自动创建的反向关联字段。它代表了所有指向当前 `product.template` 记录的 `sale.order.line` 记录。
    
- `mapped('order_id')` 用于从 `sale.order.line` 记录集中提取所有关联的 `order_id`，从而得到包含该产品的销售订单记录集。
    

### 总结

- **`Domain` 查询**：使用**点符号（`.`）**来构建多级关联查询，并结合 `&`、`|`、`!` 等逻辑运算符实现复杂的过滤。
    
- **字段计算**：使用 `@api.depends` 装饰器，同样通过**点符号（`.`）**来声明对关联字段的依赖，从而实现多级关系的字段计算。
    

这两种机制是 Odoo 灵活且强大的数据处理能力的基石，掌握它们能让你更高效地进行 Odoo 开发。