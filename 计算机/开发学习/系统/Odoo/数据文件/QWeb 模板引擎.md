### QWeb 模板引擎：报表、邮件模板与自定义前端模板

**QWeb** 是 Odoo 中强大的 XML 模板引擎，它借鉴了 Twig 和 Jinja2 的理念，并与 Odoo 的 ORM（对象关系映射）紧密集成。它主要用于渲染视图，无论是后台的动态看板、前端网页、还是用于打印的报表和发送的邮件，QWeb 都是其背后的核心技术。

---

### 1. 报表（Reports）

QWeb 是 Odoo 报表系统的基石。它允许你创建动态的、可打印的 PDF 报表，如发票、销售订单或采购订单。

#### 工作原理

- **XML 定义**: 报表是使用 XML 文件定义的。在这个文件中，你使用 QWeb 指令（如 `t-esc`、`t-if`、`t-foreach`）来遍历数据、显示字段、处理条件逻辑。
    
- **数据源**: QWeb 报表通过一个**模型**和**记录集**来获取数据。在报表 XML 中，`doc` 变量通常代表当前报表所针对的记录，`docs` 则代表整个记录集。
    
- **报表动作 (`ir.actions.report`)**: 在 Odoo 后台，一个报表动作 (`ir.actions.report`) 会将一个 Python 模型方法（用于获取数据）与一个 QWeb 模板（用于渲染布局）关联起来。
    

#### 示例：发票报表

XML

```
<template id="report_invoice_document">
    <t t-call="web.external_layout">
        <t t-set="o" t-value="docs"/>
        <div class="page">
            <h2><span t-field="o.name"/></h2>
            <div class="row mt32 mb32">
                <div class="col-6">
                    <strong>客户:</strong>
                    <span t-field="o.partner_id.name"/>
                </div>
            </div>
            <table class="table table-sm mt16">
                <thead>
                    <tr>
                        <th>产品</th>
                        <th class="text-right">数量</th>
                        <th class="text-right">单价</th>
                    </tr>
                </thead>
                <tbody>
                    <t t-foreach="o.invoice_line_ids" t-as="line">
                        <tr>
                            <td><span t-field="line.product_id.name"/></td>
                            <td class="text-right"><span t-field="line.quantity"/></td>
                            <td class="text-right"><span t-field="line.price_unit"/></td>
                        </tr>
                    </t>
                </tbody>
            </table>
        </div>
    </t>
</template>
```

**关键指令**:

- `t-call="web.external_layout"`: 继承 Odoo 默认的外部布局，它包含了页眉和页脚。
    
- `t-set="o" t-value="docs"`: 将 `docs` 记录集赋给一个名为 `o` 的变量，便于简化代码。
    
- `t-foreach="o.invoice_line_ids" t-as="line"`: 遍历发票行（`invoice_line_ids`）并将其赋值给 `line` 变量。
    

---

### 2. 邮件模板（Email Templates）

邮件模板也完全由 QWeb 驱动。它允许你创建动态的、富文本或纯文本的邮件内容，并能够嵌入来自 Odoo 记录的数据。

#### 工作原理

- **`mail.template` 模型**: Odoo 的邮件模板存储在 `mail.template` 模型中。
    
- **`body_html` 字段**: 邮件内容的核心是 `body_html` 字段，它包含了 QWeb 模板代码。
    
- **动态数据**: 在邮件模板中，`object` 变量通常代表发送邮件所针对的记录（例如，一个 `sale.order`）。
    

#### 示例：销售订单确认邮件

XML

```
<template id="email_template_sale_order_confirm">
    <t t-set="object" t-value="object"/>
    <div style="font-family: 'Lucica Grande', Verdana, Arial, sans-serif; font-size: 12px; color: #444;">
        <p>尊敬的 <t t-esc="object.partner_id.name"/>,</p>
        <p>您的销售订单 <t t-esc="object.name"/> 已确认。</p>
        <p>订单详情:</p>
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="border-bottom: 1px solid #ddd;">
                    <th>产品</th>
                    <th>数量</th>
                    <th>价格</th>
                </tr>
            </thead>
            <tbody>
                <t t-foreach="object.order_line" t-as="line">
                    <tr>
                        <td><t t-esc="line.product_id.name"/></td>
                        <td><t t-esc="line.product_uom_qty"/></td>
                        <td><t t-esc="line.price_total"/></td>
                    </tr>
                </t>
            </tbody>
        </table>
        <p>非常感谢您的支持！</p>
    </div>
</template>
```

**关键指令**:

- `t-set="object" t-value="object"`: 再次简化变量名。
    
- `t-esc="object.partner_id.name"`: `t-esc` 指令用于将变量值安全地插入到 HTML 中（它会自动转义特殊字符）。
    

---

### 3. 自定义前端模板（Website Templates）

QWeb 是 Odoo 网站模块（`website`）的核心。所有网站页面、博客、电子商务商店和自定义前端视图都由 QWeb 模板构建。

#### 工作原理

- **`website` 模块**: `website` 模块提供了 QWeb 模板渲染的上下文，包括 URL 路由和页面布局。
    
- **页面定义**: 你可以在 XML 文件中定义一个 QWeb 模板，并将其关联到网站的一个 URL。
    
- **动态数据**: Odoo 的控制器 (`http.Controller`) 会处理 HTTP 请求，并向 QWeb 模板传递数据。
    

#### 示例：自定义前端页面

XML

```
<template id="my_custom_page" name="My Custom Page">
    <t t-call="website.layout">
        <div id="wrap">
            <div class="container">
                <h1>欢迎来到我的定制页面</h1>
                <p>这是由 Odoo QWeb 模板渲染的页面。</p>
                <div class="row">
                    <t t-foreach="products" t-as="product">
                        <div class="col-md-4">
                            <h4><t t-esc="product.name"/></h4>
                            <p><t t-esc="product.description_sale"/></p>
                        </div>
                    </t>
                </div>
            </div>
        </div>
    </t>
</template>
```

Python

```
# controllers/main.py
from odoo import http

class MyController(http.Controller):
    @http.route('/my_page', type='http', auth='public', website=True)
    def my_page(self):
        products = http.request.env['product.template'].search([])
        return http.request.render('my_module.my_custom_page', {
            'products': products,
        })
```

**关键点**:

- `@http.route`: 装饰器定义了页面的 URL。
    
- `http.request.render(...)`: 这个方法是 Odoo 渲染 QWeb 模板的入口。它接受模板的 XML ID 和一个包含数据的字典作为参数。这个字典中的键（`products`）在模板中可以直接作为变量使用。
    

### 总结：QWeb 指令集

|指令|描述|
|---|---|
|`t-esc="var"`|输出变量 `var` 的值，并进行 HTML 转义。|
|`t-raw="var"`|输出变量 `var` 的值，不进行转义。|
|`t-if="condition"`|如果条件为 `True`，则渲染内容。|
|`t-elif="condition"`|在 `t-if` 之后使用，如果条件为 `True` 则渲染。|
|`t-else`|在 `t-if` 和 `t-elif` 之后使用，其他情况都渲染。|
|`t-foreach="collection" t-as="item"`|遍历集合 `collection`，并将每个元素赋值给 `item`。|
|`t-field="record.field_name"`|渲染字段的值，并考虑字段的类型（例如，`Many2one` 字段会渲染其名称）。|
|`t-att-attribute_name="value"`|动态设置 HTML 属性的值，例如 `t-att-class="'active' if active else ''"`。|
|`t-call="template_id"`|嵌入另一个 QWeb 模板。|