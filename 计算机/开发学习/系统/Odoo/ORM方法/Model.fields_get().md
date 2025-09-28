`Model.fields_get([allfields][, attributes])` 是 ORM 的**元数据查询方法**，用于获取模型的字段定义详情，常用于开发、调试、API接口以及动态视图生成等场景。

---

## 一、方法作用

`Model.fields_get([allfields][, attributes])` 

- 获取模型所有字段的元数据（类型、标签、帮助、选项等）。
- 支持筛选字段和指定返回属性。

---

## 二、参数说明

- `allfields`（可选）：字段名列表。留空则返回所有字段。
    - 如 `['name', 'state']`
- `attributes`（可选）：需要返回的字段属性列表。留空则返回全部属性。
    - 如 `['string', 'type', 'help']`

---

## 三、返回结果

- 返回一个字典，key为字段名，value为字段属性字典。
- 典型属性有：`string`, `type`, `required`, `help`, `readonly`, `selection`, `relation`, `related`, `translate` 等。

**示例返回：**

```
{
  'name': {
    'string': '客户名称',
    'type': 'char',
    'required': True,
    'help': '客户的全称',
    'readonly': False,
    ...
  },
  'state': {
    'string': '状态',
    'type': 'selection',
    'selection': [('draft', '草稿'), ('done', '完成')],
    ...
  }
}
```

---

## 四、代码示例

**获取所有字段的所有属性：**

```
fields_info = self.env['res.partner'].fields_get()
```

**只获取特定字段：**

```
fields_info = self.env['res.partner'].fields_get(['name', 'email'])
```

**只获取部分属性：**

```
fields_info = self.env['res.partner'].fields_get(['name'], ['string', 'type'])
```

**在外部接口或自定义API中常用：**

```
# 获取所有字段的类型和标签
fields_meta = self.env['sale.order'].fields_get([], ['string', 'type'])
for fname, fmeta in fields_meta.items():
    print(fname, fmeta['string'], fmeta['type'])
```

---

## 五、常见应用场景

- 动态生成界面或API字段说明
- 文档自动化
- 第三方系统字段映射
- 调试模型结构

---

## 六、注意事项

- 只返回字段定义，不返回实际数据内容。
- 可用于所有模型（包括自定义模型）。

---

## 七、参考文档

- [Odoo 17 fields_get 官方文档](https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#odoo.models.Model.fields_get)

---

### 总结

- `fields_get()` 获取模型字段的详细定义（类型、标签、帮助等）。
- 可指定字段和属性列表。
- 便于开发、API、调试和动态界面生成。