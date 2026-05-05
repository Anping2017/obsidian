`Model.browse()` 是 ORM 的一个基础方法，用于**通过记录的主键ID获取对应的记录对象（recordset）**。它不会查询数据库，只是构造一个 recordset，如果 ID 不存在则返回空的 recordset。

---

## 1. 基本用法

`Model.browse([_ids_])`

- **单个 ID：**
    
    ```
    partner = self.env['res.partner'].browse(1)
    ```
    
    返回 ID 为 1 的客户对象（如果存在，否则为空 recordset）。
    
- **多个 ID：**
    
    ```
    partners = self.env['res.partner'].browse([1, 2, 3])
    ```
    
    返回这些 ID 对应的客户对象集合（recordset）。
    

---

## 2. 参数说明

- `ids`：可以是整数（单个ID）、列表（多个ID）、或 recordset（会自动转换）。

---

## 3. 工作原理

- `browse()` 只是创建对应ID的 recordset，不会访问数据库。
- 你访问字段时，Odoo 才会自动查询数据库。
- 如果 ID 不存在，访问字段会得到空值或异常。

---

## 4. 应用场景

- 通常在已有记录 ID 时（比如从视图、context、其它模型获取），想直接获取对象并操作。
- 适合与其它 ORM 方法连用，比如在业务流程、控制器、定制开发时。

---

## 5. 注意事项

- 不会做权限校验，访问字段时才会检查权限。
- 只适用于已知的主键 ID。
- 返回的是 recordset（可以迭代、访问字段）。

---

## 6. 代码示例

```
# 获取 ID 为 42 的客户，并打印姓名
partner = self.env['res.partner'].browse(42)
if partner.exists():
    print(partner.name)
```

---

## 7. 官方文档参考

- [Odoo ORM: browse()](https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#odoo.models.Model.browse)

---

### 总结

- `Model.browse(ids)` 根据主键ID获取记录对象（recordset），不查询数据库。
- 常用于有ID时高效获取对象，可以用于单条或多条记录。