# ⚡ Odoo 服务器动作 (`ir.actions.server`)

---

## 1. 核心概念

- **服务器动作（Server Action）** 是 Odoo 后台自动执行的操作
    
- 存放在模型 `ir.actions.server` 中
    
- **作用**：
    
    1. 自动执行 Python 代码或 ORM 操作
        
    2. 响应用户操作或定时任务
        
    3. 可与自动化规则（Automated Actions）配合触发
        
- **触发方式**：
    
    - 手动触发（按钮、菜单）
        
    - 条件触发（Automated Actions）
        
    - 定时触发（Scheduled Actions / Cron Jobs）
        

---

## 2. 类型与配置

### 2.1 动作类型（`action_type`）

|类型|描述|
|---|---|
|Python Code|使用 Python 代码操作记录集|
|Create Record|创建新记录|
|Write on Record|更新当前记录|
|Trigger Object|调用模型方法|
|Execute Report|执行报表|
|Send Email|发送邮件|

### 2.2 核心字段

|字段|描述|
|---|---|
|`name`|动作名称|
|`model_id`|作用模型（当前操作对象）|
|`state`|动作类型（Python, Create, Write…）|
|`code`|Python 代码（`state='code'` 时）|
|`binding_model_id`|绑定的模型（可选）|
|`binding_type`|触发方式（手动、自动、计划任务）|

---

## 3. Python 服务器动作示例

**场景**：自动标记订单为已审核

`# 在 ir.actions.server 的 Python Code 中 for record in records:     record.state = 'approved'     record.approved_by = env.user.id`

- `records` 是触发动作的记录集
    
- 可直接使用 `env` 访问其他模型
    

---

## 4. 手动触发 vs 自动触发

### 4.1 手动触发

- 在表单或树视图中添加按钮：
    

`<button name="%(action_server_id)d" type="action" string="Approve Order"/>`

- 点击按钮 → 执行服务器动作
    

### 4.2 自动触发

- 使用 **Automated Actions**（自动化规则）
    
    - 例如：当订单状态为 `confirmed` 时自动执行动作
        
- 条件触发：
    

`# 条件：state == 'confirmed' for record in records:     record.send_notification()`

### 4.3 定时触发

- 使用 **Scheduled Actions / Cron Jobs**
    
- 定期执行 Python 服务器动作
    

`# 每天凌晨检查库存不足的产品 products = env['product.product'].search([('qty_available','<',10)]) for p in products:     p.notify_low_stock()`

---

## 5. 与 ORM 结合

服务器动作可以执行任意 ORM 方法，例如：

1. **创建记录**
    

`self.env['sale.order'].create({'name': 'Auto Order', 'amount_total': 1000})`

2. **更新记录**
    

`records.write({'state': 'done'})`

3. **调用模型方法**
    

`for rec in records:     rec.compute_total_amount()`

---

## 6. 注意事项

- Python 服务器动作执行环境：
    
    - `records` → 当前触发记录集
        
    - `env` → 当前环境
        
    - 可访问上下文 `env.context`
        
- **安全性**：
    
    - Python 代码有完全执行权限，需谨慎操作
        
    - 避免执行危险 SQL 或删除重要数据
        
- **性能**：
    
    - 批量操作时尽量使用 ORM 批量方法，避免循环内重复查询
        

---

## 7. 实际应用场景

|场景|示例|
|---|---|
|自动审批|审核订单、标记状态|
|邮件通知|订单确认后发送邮件|
|数据同步|同步库存或客户数据到其他系统|
|定时任务|每天统计销售额并生成报表|
|自动计算|更新统计字段、计算金额|

---

## 8. 总结

- **服务器动作 (`ir.actions.server`)** 是 Odoo 自动化和后台逻辑的核心工具
    
- 核心组成：
    
    1. 触发方式：手动 / 自动 / 定时
        
    2. 动作类型：Python / 创建 / 更新 / 调用方法 / 报表 / 邮件
        
    3. 关联对象：`model_id` / `records` / `env`
        
- 可结合 ORM 方法、计算字段、上下文，实现复杂业务逻辑
    

---

我可以帮你画一张 **服务器动作触发流程图**：

- 显示手动触发、自动触发、定时触发的流程
    
- 展示 `records` → Python 执行 → ORM 操作 → 前端/数据库更新