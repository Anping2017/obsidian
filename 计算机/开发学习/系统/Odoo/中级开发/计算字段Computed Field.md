# 🧮 Odoo 计算字段（Computed Fields）教程

---

## 1. 核心概念

- **计算字段（Computed Field）**：字段值不是直接存储，而是通过方法计算得出
    
- 自动追踪依赖字段的变化，实时更新
    
- 常用于金额计算、状态汇总、百分比计算等业务场景
    

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