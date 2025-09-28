# 🧭 Odoo 向导（Wizard）开发指南

---

## 1. 核心概念

- **Wizard** 是一种临时模型（TransientModel），用于：
    
    1. 与用户交互
        
    2. 收集参数
        
    3. 执行临时业务逻辑
        
- 特点：
    
    - 临时数据存储，数据库中不永久保留
        
    - 表单简单，通常为弹窗（Modal）
        
    - 通过按钮或服务器动作触发
        

---

## 2. Wizard 模型定义

- 使用 `models.TransientModel`
    
- 常用字段：
    
    - `Many2one` / `Char` / `Selection` / `Boolean` / `Date` 等
        
- 示例：选择客户并生成报价单
    

```
from odoo import models, fields, api

class SaleOrderWizard(models.TransientModel):
    _name = 'sale.order.wizard'
    _description = 'Create Sale Order Wizard'

    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    order_date = fields.Date(string='Order Date', default=fields.Date.context_today)

    def create_order(self):
        for wizard in self:
            self.env['sale.order'].create({
                'partner_id': wizard.partner_id.id,
                'date_order': wizard.order_date,
            })
        return {'type': 'ir.actions.act_window_close'}  # 关闭向导

```

---

## 3. Wizard 视图（Form View）

```
<odoo>
    <record id="view_sale_order_wizard_form" model="ir.ui.view">
        <field name="name">sale.order.wizard.form</field>
        <field name="model">sale.order.wizard</field>
        <field name="arch" type="xml">
            <form string="Create Sale Order">
                <group>
                    <field name="partner_id"/>
                    <field name="order_date"/>
                </group>
                <footer>
                    <button string="Create Order" type="object" name="create_order" class="btn-primary"/>
                    <button string="Cancel" class="btn-secondary" special="cancel"/>
                </footer>
            </form>
        </field>
    </record>
</odoo>

```

- `type="object"`：按钮调用模型方法
    
- `special="cancel"`：关闭向导
    

---

## 4. Wizard 动作（Action）

```
<record id="action_sale_order_wizard" model="ir.actions.act_window">
    <field name="name">Create Sale Order</field>
    <field name="res_model">sale.order.wizard</field>
    <field name="view_mode">form</field>
    <field name="target">new</field> <!-- 弹窗 -->
</record>

```

- `target="new"`：以弹窗显示
    
- 通过按钮或菜单调用该 Action
    

---

## 5. 菜单或按钮触发 Wizard

### 5.1 菜单触发

```
<menuitem id="menu_sale_order_wizard"
          name="Create Sale Order"
          parent="sale.menu_sale_order"
          action="action_sale_order_wizard"/>

```

### 5.2 按钮触发

`<button string="Create Wizard" type="action" name="%(action_sale_order_wizard)d"/>`

---

## 6. Wizard 常用特性

1. **TransientModel 自动清理**
    
    - 数据在数据库中临时保存，通常会在一段时间后自动清理
        
    - `_transient_max_hours` 可设置记录最大存活时间
        
2. **多步骤向导**
    
    - 可定义多个表单视图，通过 `next` / `previous` 实现步骤切换
        
    - 常用于复杂业务流程
        
3. **默认值与上下文**
    
    - 可通过 `default_get` 设置初始值
        
    - 可通过 `context` 传递参数
        

```
@api.model
def default_get(self, fields):
    res = super().default_get(fields)
    res['order_date'] = fields.Date.today()
    return res

```

---

## 7. 实际应用场景

|场景|描述|
|---|---|
|创建销售订单|用户选择客户和日期，快速生成订单|
|批量操作|批量确认订单、审批、发送邮件|
|数据导入|向导收集参数，调用后台方法导入数据|
|财务操作|向导生成凭证、计算报表|
|设置向导|系统配置、初始化数据向导|

---

## 8. 总结

- **Wizard 核心流程**：
    
    1. 定义 `TransientModel`
        
    2. 创建向导表单视图
        
    3. 定义 Action（弹窗）
        
    4. 菜单或按钮触发
        
    5. 在方法中执行临时逻辑并关闭向导
        
- **关键点**：
    
    - 临时模型，自动清理
        
    - 弹窗表单，收集参数
        
    - 方法执行业务逻辑并返回 `act_window_close`