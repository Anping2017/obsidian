## 一、基础知识

1. Odoo ORM简介与模型结构
2. 字段的作用和定义位置
3. 字段类型总览

---

## 二、常用字段类型详解

1. 基本类型
	- Boolean
	- Char
	- Float
	- Integer
2. 进阶类型
    - Binary
    - Html
    - Image
    - Monetary
    - Selection
    - Text
    - Date/Datetime
3. 关系字段
    - Many2one
    - One2many
    - Many2many
4. 特殊类型
    - Json

---

## 三、字段参数与属性

| 参数名                 | 作用描述             | 示例                                                            |
| ------------------- | ---------------- | ------------------------------------------------------------- |
| `string`            | 字段标签，界面显示名称      | `string='客户名称'`                                               |
| `required`          | 是否必填             | `required=True`                                               |
| `default`           | 默认值              | `default='新客户'`                                               |
| `readonly`          | 是否只读             | `readonly=True`                                               |
| `help`              | 字段帮助说明，鼠标悬停显示    | `help='这是客户的姓名'`                                              |
| `index`             | 是否加数据库索引，提高查询速度  | `index=True`                                                  |
| `copy`              | 复制记录时是否复制该字段     | `copy=False`                                                  |
| `store`             | 计算字段是否存储到数据库中    | `store=True`                                                  |
| `selection`         | 下拉选项字段，指定选项列表    | `selection=[('a','A'),('b','B')]`                             |
| `related`           | 相关字段，显示另一个模型某字段值 | `related='partner_id.name'`                                   |
| `domain`            | 关系字段的选择范围        | `domain="[('is_company', '=', True), ('active', '=', True)]"` |
| `ondelete`          | 关系字段删除时的处理方式     | `ondelete='cascade'`                                          |
| `context`           | 用于传递临时参数 ,默认值    | `context="{'search_default_group': 1}"`                       |
| `groups`            | 权限限制             |                                                               |
| `company_dependent` | 字段值是否依赖于当前公司     |                                                               |
| `group_operator`    | 对此字段进行分组时使用的聚合函数 |                                                               |
| `compute`           | 字段值自动计算，需指定方法名   | `compute='_compute_total'`                                    |

#### 计算字段 Computed Fields

- **compute** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.13)")) – 计算字段的方法名称
- **precompute**（[_bool_](https://docs.python.org/3/library/functions.html#bool "（在 Python v3.13 中）")） – 是否应在数据库中插入记录之前计算字段。
- **compute_sudo** ( [_bool_](https://docs.python.org/3/library/functions.html#bool "（在 Python v3.13 中）") ) – 是否应以超级用户身份重新计算字段以绕过访问权限（`True`对于存储字段默认`False` 为非存储字段）
    
- **recursive** ( [_bool_](https://docs.python.org/3/library/functions.html#bool "（在 Python v3.13 中）") ) – 字段是否具有递归依赖项（字段 `X`具有类似这样的依赖项`parent_id.X`）；必须明确声明字段递归，以保证重新计算正确
    
- **inverse** ( [_str_](https://docs.python.org/3/library/stdtypes.html#str "（在 Python v3.13 中）") ) – 反转字段的方法名称（可选）
    
- **search** ( [_str_](https://docs.python.org/3/library/stdtypes.html#str "（在 Python v3.13 中）") ) – 实现字段搜索的方法名称（可选）
    
- **related** ( [_str_](https://docs.python.org/3/library/stdtypes.html#str "（在 Python v3.13 中）") ) – 字段名称序列
    
- **default_export_compatible**（[_bool_](https://docs.python.org/3/library/functions.html#bool "（在 Python v3.13 中）")） – 在导入兼容的导出中，该字段是否必须默认导出


---

## 四、字段高级用法

1. 计算字段（compute/@api.depends)
2. 相关字段（related）
3. 反向字段（inverse）
4. 数据约束（@api.constrains）
5. on_change 行为

---

## 五、字段继承与扩展

1. 新增字段到已有模型（_inherit）
2. 字段扩展与重定义
3. 字段安全性和访问权限

---

## 六、字段在视图中的应用

1. 字段在form、tree、kanban等视图的配置
2. attrs属性：必填、只读、隐藏
3. 字段的高级界面行为

---

## 七、实战案例

1. 定义基本模型及字段
2. 关系字段的实际应用
3. 计算字段/相关字段综合示例
4. 字段约束与业务规则实现
5. 字段在界面中的交互

---

## 八、常见问题与调试技巧

1. 字段定义错误排查
2. 字段不显示/不生效原因
3. 关系字段常见坑
4. 字段调试与测试