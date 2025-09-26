### 在 Odoo 17 中，`Model.create(vals_list)` 是 ORM（对象关系映射）中用于**创建新记录**的核心方法之一。

在 Odoo 17 中，`Model.create(vals_list)` 是 ORM（对象关系映射）中用于**创建新记录**的核心方法之一。  
下面为你详细解释其工作原理与常见用法：

---

## 一、基本用法

- **单条记录创建**
    
    ```
    new_partner = self.env['res.partner'].create({
        'name': '张三',
        'phone': '18888888888',
    })
    ```
    
    `create` 方法会返回新建的记录对象（`recordset`）。
    
- **批量创建**
    
    ```
    partners = self.env['res.partner'].create([
        {'name': '李四'},
        {'name': '王五', 'phone': '19999999999'},
    ])
    ```
    
    批量创建时，传入一个由字典组成的列表，每个字典代表一条新记录。
    

---

## 二、参数说明

- `vals_list`：可以是一个字典（单条），也可以是字典组成的列表（多条）。
    - 字典的 key 为字段名，value 为字段值。

---

## 三、底层机制

- 会自动调用模型的 `@api.model` 装饰的 `create` 方法（可被继承重写）。
- 触发相关的 `@api.model_create_multi`（处理批量创建）、约束检查、默认值设置等。
- 自动执行字段的 `default`、`compute`、`onchange` 等逻辑。

---

## 四、常见用法场景

- 在业务流程、自动化脚本、数据导入中批量创建客户、订单、产品等。
- 在自定义模块中扩展 `create` 方法以实现附加逻辑（如自动编号、日志记录等）。

---

## 五、注意事项

1. **权限校验**：创建记录时会校验用户的访问权限。
2. **触发器**：会触发相关的自动方法（如 `_create`, `@api.model_create_multi`）。
3. **返回值类型**：
    - 单条时返回单个 `recordset`
    - 多条时返回 `recordset` 集合

---

## 六、官方参考（Odoo 17）

- [Odoo ORM API](https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html)
- [Odoo Model.create 源码](https://github.com/odoo/odoo/blob/17.0/odoo/models.py#L3850)（具体实现可以查阅源码）

---

### 总结

`Model.create(vals_list)`

- 用于创建模型新记录
- 支持批量创建
- 自动处理默认值、约束、权限
- 常用于各种业务和自定义开发场景