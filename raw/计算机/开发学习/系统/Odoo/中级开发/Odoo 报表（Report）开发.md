# 📝 Odoo 报表（Report）开发指南

---

## 1. 报表核心概念

- Odoo 报表通常分两类：
    
    1. **QWeb 报表（HTML/PDF）**：现代方式，基于 XML 模板，支持 PDF 生成
        
    2. **RML 报表（旧版）**：已逐渐被 QWeb 取代
        
- **报表组成**：
    
    1. 数据源：模型记录集
        
    2. 报表模板：QWeb XML 文件
        
    3. 报表动作：`ir.actions.report` 定义报表与模板关联
        
- **触发方式**：
    
    - 菜单点击
        
    - 按钮点击
        
    - 服务器动作调用
        

---

## 2. 定义报表模板（QWeb）

### 2.1 XML 目录结构

```
my_module/
├── views/
│   ├── report_saleorder.xml
│   └── ...
└── report/
    └── templates.xml

```

### 2.2 QWeb 模板示例

```
<odoo>
    <template id="report_saleorder_document">
        <t t-call="web.external_layout">
            <t t-foreach="docs" t-as="o">
                <div class="page">
                    <h2>Sale Order: <t t-esc="o.name"/></h2>
                    <p>Customer: <t t-esc="o.partner_id.name"/></p>
                    <p>Total: <t t-esc="o.amount_total"/></p>
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>Product</th>
                                <th>Qty</th>
                                <th>Price</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr t-foreach="o.order_line" t-as="line">
                                <td><t t-esc="line.product_id.name"/></td>
                                <td><t t-esc="line.product_uom_qty"/></td>
                                <td><t t-esc="line.price_total"/></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </t>
        </t>
    </template>
</odoo>

```

- `t-foreach="docs"` 遍历报表数据
    
- `t-esc` 输出字段值
    
- `t-call="web.external_layout"` 使用 Odoo 默认外部布局（页眉页脚）
    

---

## 3. 定义报表动作

### 3.1 XML 配置

```
<odoo>
    <report
        id="action_report_saleorder"
        string="Sale Order"
        model="sale.order"
        report_type="qweb-pdf"
        name="my_module.report_saleorder_document"
        file="my_module.report_saleorder_document"
        print_report_name="'SaleOrder-%s' % (object.name)"
    />
</odoo>

```

|属性|说明|
|---|---|
|`id`|报表动作唯一 ID|
|`string`|报表名称（菜单显示）|
|`model`|绑定模型|
|`report_type`|`qweb-pdf` 或 `qweb-html`|
|`name`|模板引用名称|
|`file`|PDF 输出文件名|
|`print_report_name`|打印文件名模板，可动态生成|

---

## 4. Python 后端报表类（可选）

- 如果需要自定义数据或方法，可创建 `report` 类
    

```
from odoo import models, api

class SaleOrderReport(models.AbstractModel):
    _name = 'report.my_module.report_saleorder_document'
    _description = 'Sale Order Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['sale.order'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'sale.order',
            'docs': docs,
            'extra_info': 'Some extra data',
        }

```

- `_get_report_values` 返回给 QWeb 的数据字典
    
- `docs` 对应模板中 `t-foreach="docs"`
    

---

## 5. 报表触发方式

1. **菜单触发**
    
```
<menuitem id="menu_report_saleorder"
          name="Sale Order Report"
          action="action_report_saleorder"/>

```
    
2. **按钮触发**
    
```
<button name="%(action_report_saleorder)d"
        type="action"
        string="Print Sale Order"/>

```
    
3. **服务器动作触发**
    
    - 通过 `ir.actions.server` 执行报表
        
    
```
report = self.env.ref('my_module.action_report_saleorder')
return report.report_action(self)

```
    

---

## 6. 高级技巧

- **分页 & 分组**
    
    - 在 QWeb 模板中可使用 `t-foreach` 和条件判断
        
- **报表格式**
    
    - PDF / HTML / XLSX（通过第三方模块）
        
- **打印布局**
    
    - `web.external_layout` 提供页眉页脚
        
    - 自定义布局可覆盖 `web.external_layout`
        
- **动态数据**
    
    - `_get_report_values` 可返回计算字段、关联字段、额外参数
        

---

## 7. 实际应用场景

|场景|描述|
|---|---|
|销售订单打印|打印 PDF 发票、报价单|
|财务报表|打印资产负债表、利润表|
|采购报表|采购订单明细、供应商统计|
|自定义报表|项目管理、库存分析|
|批量打印|多记录批量生成 PDF|

---

## 8. 总结

- **核心流程**：
    
    1. QWeb 模板：HTML/PDF 布局
        
    2. 报表动作：绑定模型与模板
        
    3. Python 类（可选）：提供报表数据
        
    4. 前端触发：菜单 / 按钮 / 服务器动作
        
- **关键点**：
    
    - 模板 `t-foreach="docs"` 对应 Python 返回的 `docs`
        
    - `report_type='qweb-pdf'` 生成 PDF
        
    - `_get_report_values` 可自定义数据处理