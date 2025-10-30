# 📅 Odoo `calendar` 模块详解

## 一、`calendar` 模块的作用

- **日历和会议管理模块**，提供完整的日程管理功能。
- 管理会议、事件和日程安排。
- 支持会议邀请、提醒和同步。
- 与业务模块集成，自动创建会议（如客户拜访、项目会议）。
- 支持日历订阅和导入导出（iCal格式）。

📌 形象理解：  
👉 `calendar` 模块是"日程管理器"，帮助管理所有会议和事件。

---

## 二、核心功能

### 1. 会议/事件管理

#### 事件模型

```
class CalendarEvent(models.Model):
    _name = 'calendar.event'
    _description = 'Calendar Event'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Meeting Subject', required=True, tracking=True)
    description = fields.Html('Description')
    start = fields.Datetime('Start', required=True, tracking=True)
    stop = fields.Datetime('Stop', required=True, tracking=True)
    allday = fields.Boolean('All Day', default=False)
    location = fields.Char('Location', tracking=True)
    partner_ids = fields.Many2many('res.partner', string='Attendees')
    user_id = fields.Many2one('res.users', 'Responsible')
    state = fields.Selection([
        ('draft', 'Unconfirmed'),
        ('open', 'Confirmed')
    ], string='Status', default='draft')
```

#### 事件类型

- **会议**：与他人会面的会议
- **电话**：电话会议
- **视频会议**：在线视频会议
- **活动**：其他类型的活动

### 2. 日历视图

#### 视图类型

- **月视图**：月度日历视图
- **周视图**：周视图
- **日视图**：日视图
- **列表视图**：事件列表

### 3. 会议邀请和参与者

#### 参与者状态

- **待响应**（Needs Action）
- **暂定**（Tentative）
- **已拒绝**（Declined）
- **已接受**（Accepted）

### 4. 会议提醒

#### 提醒方式

- **通知**：在Odoo界面显示通知
- **邮件**：发送提醒邮件

### 5. 重复事件

#### 重复规则

- **每天**、**每周**、**每月**、**每年**
- **自定义**：自定义重复规则

---

## 三、典型使用场景

### 场景 1：安排客户会议

**步骤**：

1. **创建会议**
   - 会议主题：客户拜访
   - 设置时间、地点
   - 添加参与者

2. **发送邀请**
   - 发送会议邀请
   - 参与者响应

### 场景 2：定期团队会议

**步骤**：

1. **创建重复事件**
   - 设置每周重复
   - 添加团队成员

---

## 四、总结

- **`calendar` 模块**提供完整的日历和会议管理功能。
- 核心功能：
  - 事件和会议管理
  - 多种日历视图
  - 会议邀请和参与者管理
  - 会议提醒
  - 重复事件
- 支持日程管理和会议安排。
