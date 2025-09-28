# 🔗 Odoo 复杂多级关系查询（Domain）

- **Domain** = 条件表达式，用于筛选记录

#### 基本语法

`('field_name', 'operator', 'value')`


**表达式格式**：
`[(字段, 操作符, 值)]`


**运算符**operator：
`=, !=, >, <, >=, <=, in, not in, like, ilike, not like, not ilike, child_of, parent_of, =like, =ilike`

- **逻辑运算**：
    
    - AND（默认连接多个条件）
        
    - OR：`['|', 条件1, 条件2]`
        
    - NOT：`['!', 条件]`
        
- **多级关系查询**：
    
    - 支持跨模型字段（Many2one/One2many/Many2many）
        
    - 使用关联字段链式访问：`field1.field2.field3`
        

---

## 2. 基本 Domain 示例

1. **简单条件**
    

`[('state', '=', 'done')]`

- 查询 `state` 为 `'done'` 的记录
    

2. **多条件 AND**
    

`[('state', '=', 'done'), ('amount_total', '>', 1000)]`

- 查询状态为 `'done'` 且总金额大于 1000 的记录
    

3. **OR 条件**
    

`['|', ('state', '=', 'draft'), ('state', '=', 'sent')]`

- 查询状态为 `'draft'` 或 `'sent'` 的记录
    

4. **NOT 条件**
    

`['!', ('active', '=', True)]`

- 查询 `active` 为 `False` 的记录
    

---

## 3. 多级关系查询

### 3.1 Many2one 关联查询

- 查询订单中客户所在城市为 `'Auckland'` 的销售订单：
    

`[('partner_id.city', '=', 'Auckland')]`

- `partner_id` → 关联 `res.partner` 模型
    
- `.city` → `res.partner` 的字段
    

### 3.2 One2many 关联查询

- 查询客户下有至少一条未付发票的客户：
    

`[('invoice_ids.state', '=', 'open')]`

- `invoice_ids` → 关联 `account.move` 模型
    
- `.state` → 发票状态字段
    

### 3.3 Many2many 关联查询

- 查询拥有特定标签的客户：
    

`[('category_id.name', '=', 'VIP')]`

- `category_id` → Many2many 标签字段
    
- `.name` → 标签名称
    

---

## 4. 关联查询的层级


#### 一级关联查询

```
domain = [('partner_id.name', '=', '客户 A')]
```

#### 多级关联查询

```
domain = [('partner_id.country_id.name', '=', '中国')]
```

#### 结合逻辑运算符

**AND** 关系

```
domain = [
    ('partner_id.country_id.name', '=', '中国'),
    ('amount_total', '>', 1000)
]
```


**OR** 关系

```
domain = [
    '|',
    ('order_line.product_id.name', 'ilike', '电脑'),
    ('state', '=', 'draft')
]
```



### 组合多级条件
示例：查询特定客户和订单状态

```
['&', 
  ('partner_id.city', '=', 'Auckland'),
  '|',
    ('state', '=', 'draft'),
    ('state', '=', 'sent')
]

```

- 逻辑解析：
    
    1. 客户城市 = `'Auckland'` AND
        
    2. (状态 = `'draft'` OR `'sent'`)
        

---

## 5. 应用场景

1. **销售**
    
    - 查询某城市客户的所有销售订单
        
    - 查询特定销售员负责且金额大于 1000 的订单
        
2. **库存**
    
    - 查询库存中属于特定分类且数量小于安全库存的产品
        
3. **项目管理**
    
    - 查询客户项目中状态为进行中且任务未完成的记录
        
4. **财务**
    
    - 查询客户未结算发票，并且总金额超过阈值
        

---

## 6. 注意事项

- 多级关系查询仅支持 **Many2one**、**One2many** 和 **Many2many**
    
- 链式字段查询仅向前追踪（从当前模型到关联模型），不能跨反向字段（One2many 反向 Many2one 链式查询需使用 `search()` 或 `filtered()`）
    
- OR/AND/NOT 逻辑组合需注意顺序，复杂逻辑可用括号可视化组合
    
- 性能优化：
    
    - 尽量减少 One2many 关联查询
        
    - 使用索引字段提高查询效率