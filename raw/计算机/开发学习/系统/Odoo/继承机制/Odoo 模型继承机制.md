
> 本笔记把 Odoo 的三种模型继承机制（扩展 / 新模型基于原型 / 委托/代理）整理成清晰可检索的 Markdown，方便复制到笔记软件或 README。

---

# 目录

# Odoo 模型继承 — 清晰笔记

> 本笔记把 Odoo 的三种模型继承机制（扩展 / 新模型基于原型 / 委托/代理）整理成清晰可检索的 Markdown，方便复制到笔记软件或 README。

---

# 目录

1. [一句话概览](#一句话概览)
2. [详解（按类型）](#详解（按类型）)
   * [扩展继承（`_inherit`，无 `_name`）](#扩展继承_inherit无_name)
   * [新模型基于旧模型（`_name` + `_inherit`）](#新模型基于旧模型_name--_inherit)
   * [委托 / 代理继承（`_inherits`）](#委托--代理继承_inherits)
3. [对比表格（快速检索）](#对比表格（快速检索）)
4. [常见误区（便于检索）](#常见误区（便于检索）)
5. [选择指南（快速决策清单）](#选择指南（快速决策清单）)
6. [示例代码汇总（可复制粘贴）](#示例代码汇总（可复制粘贴）)
7. [调试与排查小贴士](#调试与排查小贴士)
8. [记忆卡片（便于快速回顾）](#记忆卡片（便于快速回顾）)
9. 额外的知识点：
	1. [[odoo继承字段属性修改规则]]
	2. [[odoo继承字段属性哪些可以改]]
	3. [[odoo如何避免多模块覆盖同一值产生冲突]]
	4. [[几种常用方法可以检查odoo字段]]
---

# 一句话概览

* **`_inherit`（无 `_name`）** → 在原模型上扩展（同表），最常用
* **`_name` + `_inherit`** → 以现有模型为原型创建新模型（新表）
* **`_inherits`** → 委托/代理继承（新表 + 被委托表，透明代理字段）

---

# 详解（按类型）

![[Pasted image 20250926231542.png]]



## 经典继承 Classical inheritance（`_name` + `_inherit`）

新模型从其基础模型中获取所有字段、方法和元信息



**关键写法**：

```python
class ServiceProduct(models.Model):
    _name = 'service.product'      # 新模型（新表）
    _inherit = 'product.product'   # 以 product.product 为原型
    service_type = fields.Selection([...])
```

**核心效果**：

* 创建一个新模型（新 DB 表），但在加载时以指定模型的字段/方法作为起点（类似“复制式”）。
* 新表与原表数据相互独立。

**优点**：

* 快速复用已有模型的定义作为新模型的骨架。

**缺点 / 注意点**：

* 可能出现字段重复或约束冲突；视图与安全规则需单独适配。
* 相比 `_inherit` 使用频率较低。

**适用场景**：

* 需要一个独立实体，但希望复用另一个模型的大量定义作为起点。

---

## 扩展/原型继承 Extension (`_inherit`，无 `_name`)

新模型将**替换**现有模型，本质上是就地扩展它


**关键写法**：

```python
class ProductExtend(models.Model):
    _inherit = 'product.product'
    is_custom_made = fields.Boolean()
```

**核心效果**：

* 不创建新的数据库表；直接在被继承模型对应表上添加字段/方法/约束。
* 最常用的非侵入式扩展方式。

**优点**：

* 简单、直接；升级（core/module 更新）冲突风险较小。

**缺点 / 注意点**：

* 如果多个模块对同一字段名或视图做修改，可能发生冲突。

**适用场景**：

* 给标准或第三方模型增加字段、增加逻辑、覆盖方法或添加约束。


---

## 委托 / 代理继承 Delegation（`_inherits`）

会将_当前模型中未找到的任何字段的查找委托给“子”模型




**关键写法**：

```python
class Patient(models.Model):
    _name = 'hospital.patient'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade', delegate=True)
    medical_record = fields.Char()
```

**核心效果**：

* 创建新模型（新表）来保存专属字段与一个指向被委托模型的 `Many2one`。
* 被委托模型保存被代理的字段。访问子模型时，对应字段会被 ORM 透明代理（例如 `patient.name` 访问 `res.partner.name`）。

**优点**：

* 将通用字段放在通用表，被特化的字段放在子表，数据结构清晰；很适合“角色化扩展”（如 contact → employee/customer/patient）。

**缺点 / 注意点**：

* 涉及两表的生命周期管理（创建/删除等）。
* 查询或约束可能跨表，需审慎设计索引与约束位置。

**适用场景**：

* 多个实体共享通用字段但各自有专属字段的场景。

---

# 对比表格（快速检索）

| 项目        |        `_inherit`（扩展） | `_name + _inherit`（新模型基于原型） |          `_inherits`（委托/代理） |
| --------- | --------------------: | --------------------------: | --------------------------: |
| 对应关键字     | `_inherit`（无 `_name`） |        `_name` + `_inherit` |                 `_inherits` |
| 是否新建 DB 表 |               否（使用父表） |                       是（新表） |                是（新表 + 被委托表） |
| 数据存储位置    |                父模型对应表 |                      新表（独立） |        新表（专属字段） + 父表（被委托字段） |
| 字段访问      |               直接在原模型上 |          新模型有独立字段（但以父定义为起点） |               访问时透明代理到被委托模型 |
| 典型用例      |          给已有模型添加字段/逻辑 |                基于现有模型创建独立实体 | 角色化扩展（如 contact → employee） |
| 常见风险      |              字段名/视图冲突 |                   字段重复、约束冲突 |                生命周期与跨表约束复杂性 |
| 使用频率      |                **最高** |                          较少 |                    较高（特定场景） |

---

# 常见误区（便于检索）

* **“Python 类继承 = Odoo 继承”**：不是。Odoo 的 ORM 在模型加载时还会根据 `_inherit/_name/_inherits` 合并字段与表结构，纯 Python 继承（不使用这些属性）不会改变数据库结构。
* **命名混淆**：社区文章中对“classic / prototype / delegation / extension”等术语使用不统一。建议以 `_inherit/_name/_inherits` 的实际行为为准来判断。
* **`delegate=True`**：通常和 `_inherits` 一起出现以便语义更明确，但 ORM 的行为由 `_inherits` 驱动。

---

# 选择指南（快速决策清单）

1. 仅需给已有模型增加字段或方法 → 使用 **`_inherit`（扩展）**。
2. 想创建独立新实体，但复用另一个模型大量定义 → 使用 **`_name` + `_inherit`**（谨慎处理重复/约束）。
3. 想让新模型“拥有”父模型字段，但数据分开存储且访问透明 → 使用 **`_inherits`（委托）**。

---

# 示例代码汇总（可复制粘贴）

### 扩展（最常用）

```python
from odoo import models, fields

class ProductExtend(models.Model):
    _inherit = 'product.product'
    is_custom_made = fields.Boolean(string='Custom Made')

    def custom_method(self):
        # 业务逻辑
        return True
```

### 新模型基于旧模型（新表）

```python
from odoo import models, fields

class ServiceProduct(models.Model):
    _name = 'service.product'
    _inherit = 'product.product'
    service_type = fields.Selection([('support','Support'),('consult','Consulting')], string='Service Type')
```

### 委托/代理继承（两表 + 代理）

```python
from odoo import models, fields

class Patient(models.Model):
    _name = 'hospital.patient'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade', delegate=True)
    medical_record = fields.Char(string='Medical Record')
```

---

# 调试与排查小贴士

* 字段不显示或重复：检查模块加载顺序、依赖关系、是否多个模块定义了相同字段名。
* 视图 `xpath` 失败：确认目标视图的结构与 `xpath` 表达式匹配，注意继承链的加载顺序。
* 查询性能（委托继承场景）：审查 SQL 生成的 JOIN，必要时增加索引或用 read\_group / SQL 优化。
* 删除/级联问题：确认 `ondelete` 的语义（`cascade` / `restrict`）是否满足业务。

---

# 记忆卡片（便于快速回顾）

* `_inherit`（无 `_name`）→ **扩展（同表）**
* `_name + _inherit` → **新表（基于原型）**
* `_inherits` → **委托/代理（两表 + 透明代理）**

---

> 如果你需要：
>
> * 我可以把此文档导出为 **Markdown 文件 (.md)** 或 **PDF**；
> * 或者把示例根据你现有的 model 文件直接改写成合适的继承方案并注释；
>   请说明你的下一步需求。

    

---

# 一句话概览

- **`_inherit`（无 `_name`）** → 在原模型上扩展（同表），最常用
    
- **`_name` + `_inherit`** → 以现有模型为原型创建新模型（新表）
    
- **`_inherits`** → 委托/代理继承（新表 + 被委托表，透明代理字段）

---

