# 🏗️ Odoo `base` 模块详解

## 一、`base` 模块的作用

- Odoo 的 **核心模块**，所有其他模块都依赖它。
    
- 提供最基础的 **数据模型、字段定义、安全机制**。
    
- 定义了用户、公司、合作伙伴等核心表。
    
- 内置访问控制（权限/规则）、国际化、配置参数。
    

---

## 二、核心模型（Models）

### 1. `res.partner` —— 合作伙伴

- Odoo 中最常用的模型之一。
    
- 表示 **人/公司/供应商/客户**。
    
- 许多模块都会通过 `partner_id` 与它关联。
    

```
class Partner(models.Model):
    _name = "res.partner"
    _description = "Contact"

    name = fields.Char("Name", required=True)
    email = fields.Char("Email")
    phone = fields.Char("Phone")
    is_company = fields.Boolean("Is a Company")

```

📌 典型用法：

- 销售订单 → `partner_id`（客户）
    
- 发票 → `partner_id`（客户/供应商）
    

---

### 2. `res.users` —— 用户

- Odoo 系统用户（登录账号）。
    
- **继承自 `res.partner`** → 每个用户都是一个合作伙伴。
    

```
class Users(models.Model):
    _name = "res.users"
    _inherits = {"res.partner": "partner_id"}  # 继承 partner

    login = fields.Char("Login", required=True)
    password = fields.Char("Password")
    active = fields.Boolean("Active", default=True)

```

📌 典型用法：

- 登录认证
    
- 访问权限控制（用户组、规则）
    

---

### 3. `res.company` —— 公司

- 多公司支持的关键模型。
    
- 许多业务对象（发票、订单）会挂在某个公司下。
    

```
class Company(models.Model):
    _name = "res.company"

    name = fields.Char("Company Name")
    partner_id = fields.Many2one("res.partner", string="Partner")
    currency_id = fields.Many2one("res.currency", string="Currency")

```

📌 用于区分不同法人实体的数据隔离。

---

### 4. `ir.*` —— 技术模型

这些是 Odoo **元数据表**，用于描述和控制系统：

|模型|作用|
|---|---|
|`ir.model`|存储所有模型（Python 类）的定义|
|`ir.model.fields`|存储模型中的字段定义|
|`ir.module.module`|存储模块信息（已安装、未安装）|
|`ir.actions.*`|定义菜单、窗口动作|
|`ir.ui.menu`|系统菜单结构|
|`ir.config_parameter`|系统参数配置（键值对存储）|

📌 `ir.model` + `ir.model.fields` = **ORM 自我描述**（Odoo 的元编程能力）。

---

## 三、核心字段（Fields）

`base` 模块定义了 Odoo ORM 的 **字段类型系统**，位于 `odoo/fields.py`。

### 字段分类

- **基本字段**：`Char`, `Text`, `Boolean`, `Integer`, `Float`, `Date`, `Datetime`
    
- **关系字段**：`Many2one`, `One2many`, `Many2many`
    
- **功能字段**：`Computed`, `Related`, `Stored`
    

### 示例

```
class Example(models.Model):
    _name = "example.model"

    name = fields.Char("Name")  # 基本字段
    is_active = fields.Boolean("Active")  
    partner_id = fields.Many2one("res.partner", "Customer")  # 关系字段
    order_count = fields.Integer(
        string="Order Count",
        compute="_compute_order_count"   # 计算字段
    )

```

---

## 四、安全机制（Security）

### 1. ACL（访问控制列表）

- 定义在 **CSV 文件**里：`ir.model.access.csv`
    
- 控制某个 **组（group）** 对某个 **模型** 的 CRUD 权限。
    

例子：`res_partner` 的访问规则

`id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink access_partner_user,res_partner_user,model_res_partner,base.group_user,1,1,1,0`

🔎 解释：

- `model_res_partner` → 合作伙伴模型
    
- `group_user` → 普通用户组
    
- 权限：读/写/创建=允许，删除=禁止
    

---

### 2. 记录规则（Record Rules）

- 更细粒度的权限控制（行级别）。
    
- 定义一个 **domain** 过滤器，决定用户能看到哪些数据。
    

例子：普通用户只能看到自己公司的合作伙伴

```
<record id="res_partner_rule" model="ir.rule">
    <field name="name">Partner multi-company</field>
    <field name="model_id" ref="base.model_res_partner"/>
    <field name="domain_force">[('company_id','in',user.company_ids.ids)]</field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
</record>

```

---

### 3. 共享机制

- `res.groups` 用户组控制整体权限。
    
- 用户可以属于多个组。
    
- 权限 = 各组权限的 **并集**。
    

---

## 五、整体关系图（简化）

```
res.partner  ←──  res.users (用户继承合作伙伴)
     ↑
     │
res.company  (公司 ↔ 合作伙伴)

```

```
ir.model         → 存储模型定义
ir.model.fields  → 存储字段定义
ir.ui.menu       → 定义菜单
ir.actions.*     → 定义动作

```

---

## 六、总结

- **`base` 模块 = Odoo 的地基**，所有模块都依赖它。
    
- 提供：
    
    - **核心业务模型**：`res.partner`, `res.users`, `res.company`
        
    - **技术模型**：`ir.model`, `ir.ui.menu`, `ir.actions`
        
    - **字段系统**：Char、Integer、Many2one 等
        
    - **安全体系**：ACL + Record Rules