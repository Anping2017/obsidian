---
title: Odoo 工作流
type: concept
tags: [erp, mature]
sources: [raw/Odoo/03-应用实践层/01-业务开发/工作流设计.md, raw/Odoo/03-应用实践层/01-业务开发/业务规则配置.md]
created: 2026-05-05
updated: 2026-05-05
summary: Odoo 工作流通过 Selection 状态字段 + action 方法 + tracking + activity 实现业务流程编排,从 OpenERP 时代的图形化 workflow 引擎演变为代码驱动的状态机模式。
---

# Odoo 工作流

## 定义

Odoo 工作流(Workflow)是把业务流程的状态、转换、操作、通知用代码或配置编排起来的能力。从最简单的"草稿 → 已确认 → 完成 → 取消"到复杂的多级审批 + 并行评审 + 超时升级,都靠这套机制实现。它和 [[Odoo ORM]]、[[Odoo视图体系]] 共同支撑业务模块的"动起来"。

## 核心要点

### 演进:从 workflow 引擎到状态机模式

- **OpenERP 时代(<8.0)**:有独立的 `workflow` 引擎,用图形化节点定义状态、转换、信号。
- **Odoo 8.0+**:废弃图形 workflow,改用 **简单的 Selection 字段 + Python 方法** 表达状态机。这种"代码即流程"的简化更符合现代开发实践。

### 基础状态机实现

```python
class MyDoc(models.Model):
    _name = 'my.doc'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # 启用聊天/活动
    
    state = fields.Selection([
        ('draft', '草稿'),
        ('submitted', '已提交'),
        ('approved', '已审批'),
        ('done', '完成'),
        ('rejected', '已拒绝'),
    ], default='draft', tracking=True)  # tracking 自动记录变更到 chatter
    
    def action_submit(self):
        for r in self.filtered(lambda r: r.state == 'draft'):
            r.state = 'submitted'
            r.message_post(body='已提交,等待审批')
```

### 高级模式

- **条件审批**:根据金额/优先级动态分配审批人
- **并行评审**:技术、业务、法务三方独立审批,全部通过才进入下一状态
- **循环工作流**:评审 → 修改 → 再评审,设最大次数避免死循环
- **定时工作流**:`ir.cron` 在指定时间触发 `_execute_scheduled_task`

### Activity 与 Chatter

`mail.thread` mixin 让模型自动获得"消息+活动+追踪"三件套:
- **message_post**:类似论坛贴帖
- **mail.activity**:待办任务,会出现在用户首页"我的活动"
- **tracking=True**:字段变更自动写入 chatter,审计追溯

这是 Odoo 工作流"看得见"的部分,用户感知极强。

### Studio 与无代码工作流(EE)

企业版的 Studio 模块允许通过界面拖拽配置自动化规则、审批流、通知邮件,生成的是 `base.automation` 记录,本质仍是触发器 + Python 代码。社区版需要手写。

### 与 BPMN 引擎的对比

Odoo 没有 Camunda/Activiti 那种独立 BPMN 引擎。它的哲学是 **"流程是模型的方法,而非外部图"**。代价是复杂图形流程编排不直观,优势是流程逻辑与数据模型紧密耦合,调试与扩展更直接。

## 关系

- 状态字段、action 方法都基于 [[Odoo ORM]]
- 用户通过 [[Odoo视图体系]] 中 `<button>` 触发 action
- 受 [[Odoo安全模型]] 限制(谁能点哪个按钮)

## 参考源

- raw/Odoo/03-应用实践层/01-业务开发/工作流设计.md
- raw/Odoo/03-应用实践层/01-业务开发/业务规则配置.md
