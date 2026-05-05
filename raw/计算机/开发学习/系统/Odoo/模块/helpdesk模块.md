# 🎫 Odoo `helpdesk` 模块详解

## 一、`helpdesk` 模块的作用

- **服务台/工单管理模块**，提供完整的客户支持和服务管理功能。
- 管理客户支持工单，跟踪问题解决过程。
- 支持SLA（服务级别协议）管理和响应时间跟踪。
- 与知识库集成，提供自助服务和解决方案。
- 提供工单分类、优先级、团队分配等功能。

📌 形象理解：  
👉 `helpdesk` 模块是"客服工单系统"，管理所有客户支持请求。

---

## 二、核心功能

### 1. 工单管理

#### 工单模型

```
class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Helpdesk Ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Number', required=True)
    description = fields.Html('Description', required=True)
    partner_id = fields.Many2one('res.partner', 'Customer')
    team_id = fields.Many2one('helpdesk.team', 'Helpdesk Team', required=True)
    user_id = fields.Many2one('res.users', 'Assigned To')
    stage_id = fields.Many2one('helpdesk.stage', 'Stage')
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Urgent')
    ], string='Priority', default='1')
```

#### 工单状态

- **新建**（New）
- **进行中**（In Progress）
- **待回复**（Waiting for Customer）
- **已解决**（Resolved）
- **已关闭**（Closed）

### 2. SLA 管理

#### SLA功能

- **响应时间**：设置首次响应时间目标
- **解决时间**：设置问题解决时间目标
- **优先级规则**：不同优先级不同的SLA目标
- **警告和违约**：SLA警告和违约跟踪

### 3. 知识库集成

- **解决方案库**：保存常见问题的解决方案
- **FAQ**：常见问题解答
- **自助服务**：客户可以自助查找解决方案

---

## 三、典型使用场景

### 场景 1：处理客户支持请求

**步骤**：

1. **接收工单**
   - 客户提交问题
   - 系统自动创建工单

2. **工单处理**
   - 查看问题描述
   - 设置优先级
   - 分配处理人员

3. **问题解决**
   - 调查问题
   - 提供解决方案
   - 更新工单状态

4. **工单关闭**
   - 问题已解决
   - 关闭工单
   - 请求客户评价

---

## 四、总结

- **`helpdesk` 模块**提供完整的服务台功能。
- 核心功能：
  - 工单创建和管理
  - SLA管理和跟踪
  - 工单分类和优先级
  - 知识库集成
  - 客户满意度跟踪
- 支持客户支持和服务管理。
