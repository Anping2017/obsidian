`Model.search(domain)` 是 ORM 中最常用的方法之一，用于**检索数据库中的记录**，满足条件的都会被返回成 recordset。  

下面详细解释其用法、参数和底层机制：

---

## 1. 基本用法

`Model.search(_domain[, offset=0][, limit=None][, order=None]_)`


```
partners = self.env['res.partner'].search([('name', '=', '张三')])
```


**返回值**
一个 recordset，可以当做列表迭代、访问字段等。

---

## 2. 参数说明

- `_domain`：一个表达式，描述筛选条件
- 其它参数（可选）：
    - `limit`：最多返回多少条
    - `offset`：从第几条开始
    - `order`：排序方式（如 `'name desc'`）

```
partners = self.env['res.partner'].search(
    [('company_id', '=', self.env.user.company_id.id), ('name', 'ilike', '张')],
    limit=10,
    order='name asc'
)
```

---

## 3. 工作原理

- `search(domain)` 会将条件转换成 SQL 查询，检索对应的记录。

SQL:

`SELECT * FROM res_partner WHERE is_company = true LIMIT 5; SELECT * FROM res_partner WHERE id=1;`

---

## 4. 典型场景

- 检索客户、订单、产品等业务数据。
- 用于后台逻辑、前端界面、自动化脚本等。

---

## 5. 注意事项

- 没有找到记录时，返回空的 recordset（不是 None）。
- 权限与访问规则会自动生效，用户只能看到有权限的数据。
- 复杂筛选可以用逻辑运算符组合条件。

---

## 6. 代码示例

```
# 查找属于自己公司的客户
partners = self.env['res.partner'].search([('company_id', '=', self.env.user.company_id.id)])
for partner in partners:
    print(partner.name)
```

---

## 7. 更多文档

- [Odoo ORM: search() 官方文档](https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#odoo.models.Model.search)
- [Odoo domain语法参考](https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#domains)

---

### 总结

- `Model.search(domain)` 用于按条件检索记录
- 支持多种运算符和复杂逻辑
- 返回 recordset，可迭代和访问字段
- 常用于各种业务查询和自动化流程