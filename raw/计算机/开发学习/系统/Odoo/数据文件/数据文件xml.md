# 📄 Odoo 数据文件（`data.xml`）详解

---

## 一、作用

`data.xml` 用于在 **模块安装或更新时** 初始化或加载数据，包括：

1. **业务数据**（如产品类别、合作伙伴、状态）
    
2. **系统配置**（如公司、货币、邮件模板）
    
3. **界面定义**（菜单、视图、动作）
    
4. **权限控制**（访问规则、记录规则）
    

📌 数据文件通过 **`ir.model.data`** 记录，每条数据有一个唯一 **XML ID**。

---

## 二、XML 文件结构

### 1. 基本模板

```
<odoo>
    <record id="xml_id_name" model="model.name">
        <field name="field1">value1</field>
        <field name="field2">value2</field>
    </record>
</odoo>

```

- `<odoo>`：根标签
    
- `<record>`：创建一条记录
    
    - `id`：XML ID（模块内唯一）
        
    - `model`：模型名
        
- `<field>`：模型字段赋值
    

---

### 2. 示例：创建产品类别

```
<odoo>
    <record id="product_category_electronics" model="product.category">
        <field name="name">Electronics</field>
        <field name="sequence">10</field>
    </record>
</odoo>

```

- 安装模块时，会在数据库 `product_category` 表中创建一条记录
    
- XML ID = `module_name.product_category_electronics`
    

---

### 3. 示例：创建菜单

```
<odoo>
    <menuitem id="menu_sales_root" name="Sales"/>
    <menuitem id="menu_sales_orders" name="Orders" parent="menu_sales_root" action="action_sales_order"/>
</odoo>

```

- `menuitem` 定义菜单
    
- `parent` 指定上级菜单
    
- `action` 绑定动作（`ir.actions.act_window`）
    

---

### 4. 示例：创建动作（Action）

```
<odoo>
    <record id="action_sales_order" model="ir.actions.act_window">
        <field name="name">Sales Orders</field>
        <field name="res_model">sale.order</field>
        <field name="view_mode">tree,form</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Create your first sales order
            </p>
        </field>
    </record>
</odoo>

```

- `ir.actions.act_window` → 定义窗口动作
    
- 前端点击菜单会执行这个动作，显示 `sale.order` 的列表和表单视图
    

---

### 5. 示例：创建邮件模板

```
<odoo>
    <record id="email_template_sale_confirmation" model="mail.template">
        <field name="name">Sale Confirmation</field>
        <field name="model_id" ref="sale.model_sale_order"/>
        <field name="subject">Your order ${object.name} is confirmed</field>
        <field name="email_from">${object.user_id.email|safe}</field>
        <field name="body_html">
            <![CDATA[
                <p>Dear ${object.partner_id.name},</p>
                <p>Your order has been confirmed.</p>
            ]]>
        </field>
    </record>
</odoo>

```

- `mail.template` → 邮件模板
    
- 支持 **占位符** `${object.field}` 自动渲染数据
    
- `<![CDATA[]]>` 用于写 HTML
    

---

## 三、引用关系（`ref`）

- `<field name="field_name" ref="xml_id"/>` → 关联已有 XML ID
    
- 支持跨模块引用
    
- 例：将动作绑定到菜单：
    

`<menuitem id="menu_sales_orders" name="Orders" parent="menu_sales_root" action="action_sales_order"/>`

- `action="action_sales_order"` 指向 `ir.actions.act_window` 的 XML ID
    

---

## 四、加载顺序与依赖

1. **`__manifest__.py`** 中定义 `data` 文件加载顺序：
    

```
'data': [
    'data/data.xml',
    'views/sale_order_views.xml',
    'security/ir.model.access.csv',
],

```

2. **顺序重要**：
    
    - 先加载 **基础数据**（例如分类、状态）
        
    - 再加载 **视图和动作**
        
    - 最后加载 **权限 CSV**
        
3. **依赖模块**：
    
    - 如果引用了其他模块的 XML ID，需要在 `depends` 中声明
        

---

## 五、`data.xml` 使用场景

1. **初始化业务数据**
    
    - 产品分类、销售状态、客户等级
        
2. **界面定义**
    
    - 菜单、动作、视图
        
3. **邮件与通知模板**
    
    - 自动发邮件、提醒客户
        
4. **权限控制**
    
    - ACL、记录规则
        
5. **演示数据**
    
    - demo 数据用于模块测试或演示
        

---

## 六、可视化关系图

```
data.xml
 ├─ record(id, model) → 创建记录
 │     ├─ field(name, value) → 字段赋值
 │     └─ ref="xml_id" → 关联已有记录
 ├─ menuitem → 菜单
 ├─ ir.actions.act_window → 动作
 ├─ mail.template → 邮件模板
 └─ security/ir.model.access.csv → 权限

```

---

## 七、总结

- `data.xml` 是 **模块初始化数据核心文件**
    
- 核心特点：
    
    - **记录定义**：`<record>`
        
    - **字段赋值**：`<field>`
        
    - **引用 XML ID**：`ref`
        
    - **顺序加载**：依赖关系 + 模块依赖
        
- 与 **模型（Models）**、**视图（Views）**、**权限（Security）** 配合，实现模块完整功能