[官网方法](https://www.odoo.com/documentation/17.0/zh_CN/developer/reference/backend/orm.html#common-orm-methods)

[[ODOO ORM]]
[[odoo ORM核心原理]]


---

## 1. CRUD 方法（增删改查）

| 方法                   | 作用   |                             | 示例                                                            |
| -------------------- | ---- | --------------------------- | ------------------------------------------------------------- |
| `create(vals)`       | 创建记录 | [[Model.create(vals_list)]] | `partner = self.env['res.partner'].create({'name': 'Alice'})` |
| `write(vals)`        | 更新记录 | [[Model.write(vals)]]       | `partner.write({'email': 'alice@example.com'})`               |
| `unlink()`           | 删除记录 | [[Model.unlink()]]          | `partner.unlink()`                                            |
| `copy(default=None)` | 复制记录 | [[Model.copy()]]            | `new_partner = partner.copy({'name': 'Alice Copy'})`          |

> `vals` 是字典，包含字段名和值




---

## 2. 查询方法

| 方法                                             | 作用1111111111111111 |                          | 示例                                                                                           |
| ---------------------------------------------- | ------------------ | ------------------------ | -------------------------------------------------------------------------------------------- |
| `search(domain, limit=None, order=None)`       | 根据条件搜索记录集          | [[Model.search(domain)]] | `partners = self.env['res.partner'].search([('is_company','=',True)])`                       |
| `browse(ids)`                                  | 根据 ID 获取记录集        | [[Model.browse()]]       | `partner = self.env['res.partner']<br>.browse(1)`                                            |
| `read(fields=None)`                            | 读取字段值（返回字典列表）      | [[Model.read()]]         | `self.env['res.partner'].browse([1,2]).read(['name','email'])`                               |
| `search_read(domain, fields=None, limit=None)` | 一步搜索并读取字段          |                          | `self.env['res.partner'].search_read([('is_company','=',True)], ['name','email'], limit=10)` |
| `search_count(domain)`                         | 根据条件统计数量           |                          | `count = self.env['res.partner'].search_count([('is_company','=',True)])`                    |
| `mapped(field_name)`                           | 获取字段列表或关联字段值       |                          | `emails = partners.mapped('email')`                                                          |
|                                                |                    |                          |                                                                                              |

---

## 3. 记录集操作

| 方法 / 属性                           | 作用             |     | 示例                                                            |
| --------------------------------- | -------------- | --- | ------------------------------------------------------------- |
| `filtered(lambda r: ...)`         | 根据条件过滤记录集      |     | `big_partners = partners.filtered(lambda r: r.credit > 1000)` |
| `sorted(key=None, reverse=False)` | 根据字段排序记录集      |     | `partners.sorted(key=lambda r: r.name)`                       |
| `exists()`                        | 返回存在于数据库的记录    |     | `partner.exists()`                                            |
| `ids`                             | 返回记录 ID 列表     |     | `partner_ids = partners.ids`                                  |
| `ensure_one()`                    | 确保记录集只有一条，否则报错 |     | `partner.ensure_one()`                                        |

---

## 4. 关系字段的操作方法

> **操作格式**：`[(command, id, values)]`  

| 关系类型                 | 示例              |     | ORM 方法                                  |
| -------------------- | --------------- | --- | --------------------------------------- |
| One2many / Many2many | 获取子记录           |     | `record_ids = partner.child_ids`        |
| Many2one             | 获取关联记录          |     | `partner_id = record.partner_id`        |
| 赋值                   | 更新多条关联记录        |     | `partner.child_ids = [(6, 0, [1,2,3])]` |
| 添加单条关系               | 添加 ID 为 1 的关联   |     | `partner.child_ids = [(4, 1)]`          |
| 删除关系                 | 移除关联 ID 为 1 的关系 |     | `partner.child_ids = [(3, 1)]`          |
| 替换所有                 | 替换现有关联为 2,3     |     | `partner.child_ids = [(6, 0, [2,3])]`   |


> 常用 command：
> 
> - `0` 创建新记录
>     
> - `1` 更新记录
>     
> - `2` 删除记录
>     
> - `3` 移除关系
>     
> - `4` 添加关系
>     
> - `5` 移除所有关系
>     
> - `6` 替换所有关系
>     

---

## 5. 计算与调用方法

| 方法                                 | 作用     | 示例                                               |
| ---------------------------------- | ------ | ------------------------------------------------ |
| `compute`                          | 计算字段   | `total = order.amount_total`                     |
| `onchange`                         | 字段变动触发 | `@api.onchange('product_id')`                    |
| `call()` / `env['model'].method()` | 调用模型方法 | `self.env['sale.order'].confirm_order(order_id)` |

---

## 6. 事务与上下文

| 对象                    | 作用       | 示例                                             |
| --------------------- | -------- | ---------------------------------------------- |
| `sudo()`              | 绕过权限执行   | `self.env['res.partner'].sudo().create({...})` |
| `with_context(**ctx)` | 修改上下文执行  | `self.with_context(lang='en_US').name_get()`   |
| `env`                 | ORM 环境对象 | `self.env['sale.order']`                       |
| `context`             | 当前上下文    | `self.env.context.get('key')`                  |

---

## 7. 总结

- **CRUD**：`create` / `write` / `unlink` / `copy`
    
- **查询**：`search` / `search_count` / `browse` / `read` / `search_read` / `mapped`
    
- **记录集操作**：`filtered` / `sorted` / `exists` / `ensure_one` / `ids`
    
- **关系字段**：`[(0,0,vals)]` / `[(4,id)]` / `[(6,0,ids)]`
    
- **调用与计算**：`compute` / `onchange` / `method()`
    
- **权限与上下文**：`sudo()` / `with_context()` / `env` / `context`
    

> 掌握 ORM 方法是 Odoo 开发的核心技能，结合记录集、字段和关系操作，可实现绝大部分业务逻辑。