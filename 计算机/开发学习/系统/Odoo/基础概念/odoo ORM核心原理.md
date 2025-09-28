# 📚 Odoo ORM 核心概念与工作原理

## 一、ORM 的角色

ORM（对象关系映射） = **Python 类** ↔ **数据库表** 的翻译层。  
你写 Python，Odoo 自动生成 SQL 并操作 PostgreSQL。

`Python 对象   ⇄   ORM   ⇄   SQL 查询   ⇄   PostgreSQL 表`


- **ORM（对象关系映射）**：把 Python 对象映射到数据库表
    
- 提供 **面向对象操作数据库** 的方式
    
- 将业务逻辑与数据库操作解耦
    
- 核心模型：`models.Model`
    
- 数据库表对应模型，字段对应表列

---

## 二、核心组成部分

### 1. 模型（Model）

- 每个模型 = 数据库一张表。
    
- `_name` 决定表名。
    
- 继承 `models.Model`。
    

```python
from odoo import models, fields

class Partner(models.Model):
    _name = "res.partner"
    _description = "Partner"

    name = fields.Char("Name")
    email = fields.Char("Email")
    is_company = fields.Boolean("Is Company")

```

🔎 **结果：**

- 表名：`res_partner`
    
- 列：`id`, `name`, `email`, `is_company`
    

---

### 2. 字段（Fields）

- 定义数据库表的列。
    
- 支持关系型字段。


- **基础字段**
    
    - Char、Text、Integer、Float、Boolean、Date、Datetime
        
- **关系字段**
    
    - Many2one → 多对一
        
    - One2many → 一对多
        
    - Many2many → 多对多
        
- **功能字段**
    
    - Computed → 计算字段
        
    - Related → 关联字段
        
    - Stored → 是否存储计算结果


---

### 3. 环境（Environment, `env`）

- `self.env` 提供访问入口。
    
- 包含：
    
    - `self.env['model.name']` → 模型访问
        
    - `self.env.cr` → 数据库游标
        
    - `self.env.user` → 当前用户
        
    - `self.env.context` → 上下文
        

```python
partners = self.env["res.partner"].search([("is_company", "=", True)]) print(self.env.user.name)  # 当前用户
```

---

### 4. 记录集（Recordset）

- ORM 查询的结果。
    
- 可以是 **单条** 或 **多条**。
    
- **惰性加载**（不会立即执行 SQL，访问属性时才执行）。
    

```python
partners = self.env["res.partner"].search([("name", "ilike", "Alice")])
for p in partners:
    print(p.id, p.name)   # 遍历记录集

```

---

## 三、ORM 工作原理（可视化）

### 数据流动流程

```
Python 类定义
   ↓
ORM 生成/更新表结构
   ↓
Python 调用 ORM 方法 (create/search/write/unlink)
   ↓
ORM 转换为 SQL
   ↓
PostgreSQL 执行
   ↓
结果封装为 Recordset 返回

```

---

## 四、常用 ORM 方法（含 SQL 对应）

- **create(vals)**：创建记录
    
- **write(vals)**：更新记录
    
- **unlink()**：删除记录
    
- **copy(defaults)**：复制记录
    
- **search(domain)**：搜索记录
    
- **search_count(domain)**：计数
    
- **browse(id)**：按 ID 获取记录



### 1. 创建记录

```
partner = self.env['res.partner'].create({
    'name': 'Alice',
    'email': 'alice@example.com'
})
```

SQL:

`INSERT INTO res_partner (name, email) VALUES ('Alice', 'alice@example.com');`

---

### 2. 查询记录

```
# 搜索多个
partners = self.env['res.partner'].search([('is_company','=',True)], limit=5)

# 按 ID 直接访问
partner = self.env['res.partner'].browse(1)

```

SQL:

`SELECT * FROM res_partner WHERE is_company = true LIMIT 5; SELECT * FROM res_partner WHERE id=1;`

---

### 3. 更新记录

```
partner.write({'email': 'alice_new@example.com'})
```

SQL:

`UPDATE res_partner SET email='alice_new@example.com' WHERE id=1;`

---

### 4. 删除记录

```
partner.unlink()
```

SQL:

`DELETE FROM res_partner WHERE id=1;`

---

## 五、关系字段举例

### Many2one（一对多中的“多”端）

```
class SaleOrder(models.Model):
    _name = "sale.order"
    partner_id = fields.Many2one("res.partner", string="Customer")

```

SQL：

`partner_id INTEGER REFERENCES res_partner(id)`

---

### One2many（一对多中的“一”端）

```
class SaleOrder(models.Model):
    _name = "sale.order"
    order_line = fields.One2many("sale.order.line", "order_id", "Lines")

class SaleOrderLine(models.Model):
    _name = "sale.order.line"
    order_id = fields.Many2one("sale.order", "Order")

```

🔗 `order_line` 通过 `order_id` 反向映射。

---

### Many2many（多对多）

```
class Event(models.Model):
    _name = "event.event"
    attendees = fields.Many2many("res.partner", string="Attendees")

```

🔗 自动生成中间表：`event_event_res_partner_rel`

---

## 六、优势与局限

✅ 优势

- **代码即数据结构**（写 Python 就能生成表）。
    
- **安全性**（内置权限、事务）。
    
- **开发效率高**（避免写 SQL）。
    
- **自动维护关系表**。
    

⚠️ 局限

- **复杂查询** 可能需要手写 SQL：
    
    `self.env.cr.execute("SELECT COUNT(*) FROM res_partner")`
    
- **性能瓶颈**：大数据量时需优化 ORM 查询（比如用 `read_group` 而不是遍历）。
    
- **数据库依赖性**：强绑定 PostgreSQL。
    

---

## 七、学习路径建议

1. **先学模型和字段** → 理解 `_name`、字段类型。
    
2. **再练 CRUD 操作** → `create/search/write/unlink`。
    
3. **掌握关系字段** → `Many2one/One2many/Many2many`。
    
4. **进阶环境与上下文** → `env.user`, `env.context`。
    
5. **优化性能** → 学会 `search_read`, `read_group`。
    

---

👉 总结一句话：  
**Odoo ORM 是一个对象与关系表之间的桥梁，它让开发者用 Python 的方式写业务逻辑，背后帮你生成 SQL 并保证数据一致性和安全性。**