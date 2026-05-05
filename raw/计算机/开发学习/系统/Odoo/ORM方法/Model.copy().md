
[源代码](https://github.com/odoo/odoo/blob/17.0/odoo/models.py#L5587)

--- 

#### `Model.copy()` 是 ORM 的一个方法，用于**复制一条现有记录**，并生成一条新的记录（通常用于“复制”功能，比如复制客户、产品、订单等）。


---

## 1. 基本用法

`Model.copy(_default=None_)`

假设有一个客户记录（partner），你可以这样复制它：


```
# 假定 partner 是一个单条记录（recordset）
new_partner = partner.copy({'name': '新客户'})
```

- `copy()` 方法会返回复制后新生成的记录对象。

---

## 2. 参数说明

`default (dict)`

- `default`（可选）：一个字典，指定新记录的默认字段值。  
    比如你可以在复制时给新客户设置新的名字、编号等。
    
    ```
    new_partner = partner.copy({'name': '复制的客户', 'phone': '1234567890'})
    ```
    

---

## 3. 工作原理

- `copy()` 方法会复制原记录的所有字段，除了一些特殊字段（如唯一性字段、某些引用字段）会重新生成或清空。
- 会自动调用模型的 `_copy()` 方法（如有重载），允许开发者定制复制逻辑。
- 会触发相关的默认值设置和约束校验。

---

## 4. 常见场景

- 复制产品、客户、订单等业务记录，快速生成类似数据。
- 在自定义模块中重写 `copy()` 或 `_copy()` 方法，实现特殊的复制逻辑（比如自动加后缀、清空某些字段等）。

---

## 5. 注意事项

- 复制记录时，某些字段（如 name、code）可能需要在 `default` 参数中赋新值以防止冲突。
- 复制后的记录与原记录是独立的，唯一性字段如编号等会重新生成。
- 该方法只能在单条记录上调用（即 recordset 只能是单条）。

---

## 6. 代码示例

```
# 复制一个客户，并修改名称
partner = self.env['res.partner'].browse(1)
new_partner = partner.copy({'name': partner.name + ' (复制)'})
```

---

## 7. 官方文档参考

- [Odoo ORM: copy()](https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#copy)
- [Odoo 源码 copy 方法实现](https://github.com/odoo/odoo/blob/17.0/odoo/models.py)（通常在 models.py 文件中）

---

### 总结

- `Model.copy(default)` 用于复制记录，可指定新字段值。
- 适用于单条记录，会自动处理唯一性和默认值。
- 可以根据业务需求重写复制逻辑。