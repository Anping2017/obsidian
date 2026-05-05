# 🧩 Odoo 核心对象：`self` 与 `env`

---

## 1. `self` 的核心概念

- **`self`** 表示当前模型对象或记录集
    
- 在 Odoo ORM 中，方法通常绑定到模型类或记录集上，`self` 即代表调用方法的记录集
    
- **特性**：
    
    - 可以是单条记录，也可以是多条记录的集合
        
    - 调用 `write()`、`unlink()`、计算字段方法时，`self` 自动包含相关记录
        
    - `self` 是 **RecordSet 对象**，支持迭代、搜索和访问字段
        

---

### 1.1 单条记录与多条记录

```
# 单条记录
order = self.env['sale.order'].browse(1)  

# 多条记录
orders = self.env['sale.order'].search([('state', '=', 'draft')])  
```


- 单条记录：
    
    `order.name  # 获取字段值`
    
- 多条记录：
    
    `for o in orders:     print(o.name)`
    

---

### 1.2 RecordSet 方法示例

- 迭代：
    
```
for record in self:     
	record.field_name = 'new_value'
```


- 搜索：
    
```
self.search([('state', '=', 'done')])
```


- CRUD：
    
```
self.create({'name': 'Test'}) 
self.write({'state': 'sent'}) 
self.unlink()
```


---

## 2. `env` 的核心概念

- **`env`** = Environment，环境对象
    
- 提供当前模型的上下文、用户、数据库和记录访问权限
    
- 可以通过 `self.env['model.name']` 访问其他模型
    

### 2.1 env 的组成

| 属性/方法                        | 说明                   |
| ---------------------------- | -------------------- |
| `env.user`                   | 当前用户对象（res.users）    |
| `env.uid`                    | 当前用户 ID              |
| `env.company`                | 当前公司对象（res.company）  |
| `env.cr`                     | 数据库游标，可执行原生 SQL（慎用）  |
| `env.context`                | 当前上下文字典              |
| `env.companies`              |                      |
| `env['model.name']`          | 获取其他模型的 RecordSet 对象 |
| `env['model.name'].search()` | 搜索记录                 |
| `env['model.name'].create()` | 创建记录                 |
| `env['model.name'].browse()` | 通过 ID 获取记录集          |
| `env.ref()`                  | 通过 XML ID 获取记录       |
| `env.is_superuser()`         |                      |
| `env.is_admin()`             |                      |
| `env.is_system()`            |                      |

---

### 2.2 env 示例

1. **访问其他模型**
    

`partner = self.env['res.partner'].search([('name', '=', 'John')])`

2. **获取当前用户**
    

`current_user = self.env.user print(current_user.name)`

3. **使用上下文**
    

`default_product = self.env.context.get('default_product_id')`

4. **执行原生 SQL（慎用）**
    

`self.env.cr.execute("SELECT id, name FROM res_partner WHERE active=True") rows = self.env.cr.fetchall()`

---

## 3. `self` 与 `env` 的关系

- `self` → 当前模型的记录集
    
- `self.env` → 当前模型的环境对象
    
- `self.env['model.name']` → 访问其他模型的记录集
    

### 示例：

```
class SaleOrder(models.Model):
    _name = 'sale.order'

    def check_customer_orders(self):
        # 访问其他模型
        partner_model = self.env['res.partner']
        customer = partner_model.search([('name', '=', 'John')])

        # 遍历当前记录集
        for order in self:
            order_count = self.search_count([('partner_id', '=', customer.id)])
            print(f"Customer {customer.name} has {order_count} orders.")

```

---

## 4. 实际开发场景

1. **访问关联模型**
    

`partner = self.env['res.partner'].browse(self.partner_id.id)`

2. **批量操作记录**
    

`self.write({'state': 'done'})`

3. **获取当前用户权限**
    

`if self.env.user.has_group('sales_team.group_sale_manager'):     # 执行管理员操作`

4. **结合上下文控制逻辑**
    

`default_price = self.env.context.get('default_price', 0.0) self.price = default_price`


# 🌐 Odoo 上下文（Context）详解

---

## 1. 核心概念

- **Context（上下文）** 是一个字典（Python dict），用于在方法调用、视图渲染或操作记录时传递额外参数
    
- 提供 **额外信息**，可影响：
    
    - 字段默认值（default_xxx）
        
    - 视图显示行为
        
    - ORM 方法逻辑
        
    - 权限、语言、时间等
        
- **获取方式**：
    
    `self.env.context`
    
- 上下文是 **可继承和可修改的**，调用方法时可以传递新的 context
    

---

## 2. context 的组成

常用 key 示例：

|key|作用|
|---|---|
|`default_field`|设置字段默认值|
|`lang`|指定语言，用于多语言显示|
|`tz`|指定时区|
|`active_id`|当前活动记录 ID（常用于动作）|
|`active_model`|当前操作模型|
|`force_company`|指定操作的公司|
|`uid`|当前用户 ID（可覆盖 env.user）|
|`search_default_xxx`|默认搜索过滤器|
|`params`|页面操作参数|
|`tracking_disable`|禁用字段跟踪（消息日志）|

---

## 3. 获取 context

`current_context = self.env.context`

- 返回一个字典对象
    
- 示例：
    

`print(self.env.context) # 输出：{'lang': 'en_US', 'tz': 'Pacific/Auckland', 'uid': 2}`

---

## 4. 使用 context 设置默认值

### 4.1 在表单视图中

`<field name="partner_id" context="{'default_country_id': 15}"/>`

- 创建新客户时，国家字段默认值为 15
    

### 4.2 在方法中

`default_price = self.env.context.get('default_price', 0.0) self.price = default_price`

---

## 5. 在 ORM 方法中使用 context

### 5.1 创建记录时

`self.env['sale.order'].with_context(default_partner_id=partner.id).create({     'amount_total': 1000 })`

- 传递 context，使新创建记录使用 `default_partner_id`
    

### 5.2 修改记录时

`self.with_context(force_company=2).write({'state': 'done'})`

- 在指定公司下执行写操作
    

### 5.3 搜索记录时

`orders = self.env['sale.order'].with_context(lang='fr_FR').search([])`

- 强制切换语言显示搜索结果
    

---

## 6. context 的传递和继承

- **默认继承**：调用方法时，原 context 会自动传递
    
- **覆盖 context**：
    

`self.with_context(new_key='value').method()`

- 可以链式调用：
    

`self.with_context(key1='v1').with_context(key2='v2').method()`

- 使用 `dict(self.env.context, key='value')` 也可生成新的 context
    

---

## 7. 实际应用场景

1. **表单默认值**
    
    - 通过 context 指定创建记录时的默认字段值
        
2. **多公司/多仓库操作**
    
    - 用 `force_company` 或 `force_warehouse` 控制操作范围
        
3. **动态语言和时区**
    
    - 用 `lang` 或 `tz` 控制显示与计算
        
4. **条件业务逻辑**
    

`if self.env.context.get('skip_validation'):     return`

- 可控制方法执行行为，例如跳过约束或验证
    

5. **报表和动作**
    
    - 动作绑定 context，用于动态生成报表或过滤记录
        

---

## 8. 注意事项

- context 是 **临时字典**，不会持久化到数据库
    
- 修改 context 不会改变原 env，需要使用 `with_context()`
    
- 多级调用 context 会被覆盖或合并，需注意 key 的唯一性
    

---

## 9. 总结

- `context` 是 Odoo 中灵活控制业务逻辑的工具
    
- 作用：
    
    1. 设置默认值
        
    2. 控制方法行为
        
    3. 控制多公司、多语言、多时区操作
        
    4. 提供临时参数给视图或动作
        
- 获取方式：`self.env.context`
    
- 传递方式：`with_context({...})`