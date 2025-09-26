`Model.read()` 是 ORM 的底层方法之一，用于**批量读取记录的指定字段值**，它直接从数据库检索并返回**原始数据字典列表**，而不是 recordset。

---

## 1. 基本用法

`Model.read([_fields_])`

假设你已经有客户的 recordset：

```
partners = self.env['res.partner'].search([('is_company', '=', True)])
data = partners.read(['name', 'phone', 'email'])
print(data)
```

**输出示例：**

```
[
    {'id': 1, 'name': '客户A', 'phone': '123456789', 'email': 'a@example.com'},
    {'id': 2, 'name': '客户B', 'phone': '987654321', 'email': 'b@example.com'},
]
```

**返回值：**
将字段名称映射到其值的字典列表，每个记录一个字典

---

## 2. 参数说明

- `fields(list)`：要返回的字段名称的列表，默认全部。
- `load(str)`：加载模式，可选，控制是否加载一些特殊字段（很少用，建议默认值， `None`以避免加载`display_name`m2o 字段）。

---

## 3. 工作原理

- `read()` 是从数据库直接读取原始字段值，返回的是**字典列表**，每个字典代表一条记录。
- 不会触发 `compute` 字段、onchange等，只获取数据库已存储的值。
- 适合需要一次性获取大量数据、用于外部系统导出、接口等场景。

---

## 4. 应用场景

- 数据导出（比如同步到第三方、生成报表等）。
- 需要原始数据（而不是 recordset 对象）时。
- 性能敏感场景（只读字段，不需要业务逻辑）。

---

## 5. 注意事项

- 如果字段是关系字段（如 many2one），只返回关联记录的ID（不是对象）。
- 不触发业务逻辑（如自动计算、onchange）。
- 返回的数据是原始字典列表，不能用 recordset 的 API。

---

## 6. 代码示例

```
# 获取所有客户的名字和电话
partners = self.env['res.partner'].search([])
data = partners.read(['name', 'phone'])
for item in data:
    print(item['name'], item['phone'])
```

---

## 7. 官方文档参考

- [Odoo ORM: read()](https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#odoo.models.Model.read)

---

### 总结

- `Model.read(fields)` 用于批量读取记录的原始字段值，返回字典列表。
- 适合需要原始数据、接口或数据导出场景。
- 不触发任何业务逻辑，仅返回数据库存储的内容