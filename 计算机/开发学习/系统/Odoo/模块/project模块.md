# 📊 Odoo `project` 模块详解

## 一、`project` 模块的作用

- **项目管理核心模块**，支持项目型业务的管理。
- 管理项目的完整生命周期：从创建到完成。
- 提供任务管理、团队协作、进度跟踪等功能。
- 与销售、工时、会计等模块集成，支持项目型销售和计费。

📌 形象理解：  
👉 `project` 模块是项目管理者的"指挥中心"，协调项目团队、跟踪项目进度、管理项目资源。

---

## 二、核心功能

### 1. 项目管理

#### 项目模型

```
class ProjectProject(models.Model):
    _name = 'project.project'
    _description = 'Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Project Name', required=True)
    description = fields.Html('Description')
    partner_id = fields.Many2one('res.partner', 'Customer')
    user_id = fields.Many2one('res.users', 'Project Manager')
    company_id = fields.Many2one('res.company', 'Company')
    date_start = fields.Date('Start Date')
    date = fields.Date('End Date')
    state = fields.Selection([
        ('to_approve', 'To Approve'),
        ('approval_failed', 'Approval Failed'),
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft')
    task_ids = fields.One2many('project.task', 'project_id', 'Tasks')
    task_count = fields.Integer('Task Count', compute='_compute_task_count')
    task_count_open = fields.Integer('Open Tasks', compute='_compute_task_count')
    tag_ids = fields.Many2many('project.tags', 'Tags')
    color = fields.Integer('Color')
    active = fields.Boolean('Active', default=True)
```

#### 项目信息字段

- **基本信息**：
  - `name`：项目名称（必填）
  - `description`：项目描述（HTML）
  - `partner_id`：客户（如从销售订单创建）
  - `user_id`：项目经理
  - `company_id`：所属公司

- **时间信息**：
  - `date_start`：开始日期
  - `date`：结束日期（截止日期）
  
- **状态信息**：
  - `state`：项目状态
    - `draft`：草稿
    - `in_progress`：进行中
    - `done`：已完成
    - `cancel`：已取消

- **关联信息**：
  - `task_ids`：项目任务
  - `tag_ids`：项目标签
  - `color`：项目颜色（用于看板区分）

### 2. 任务管理（Tasks）

任务管理是项目管理的核心。

#### 任务模型

```
class ProjectTask(models.Model):
    _name = 'project.task'
    _description = 'Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Task Title', required=True, tracking=True)
    description = fields.Html('Description')
    project_id = fields.Many2one('project.project', 'Project')
    stage_id = fields.Many2one('project.task.type', 'Stage')
    user_ids = fields.Many2many('res.users', 'Task Assignees')
    user_id = fields.Many2one('res.users', 'Assigned To')
    partner_id = fields.Many2one('res.partner', 'Customer')
    company_id = fields.Many2one('res.company', 'Company')
    date_assign = fields.Datetime('Assignment Date')
    date_deadline = fields.Date('Deadline')
    date_last_stage_update = fields.Datetime('Last Stage Update')
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Very High')
    ], string='Priority', default='1')
    kanban_state = fields.Selection([
        ('normal', 'In Progress'),
        ('done', 'Ready'),
        ('blocked', 'Blocked')
    ], string='Kanban State', default='normal')
    state = fields.Selection([
        ('01_in_progress', 'In Progress'),
        ('1_done', 'Done'),
        ('1_canceled', 'Cancelled')
    ], string='Status')
    tag_ids = fields.Many2many('project.tags', 'Tags')
    subtask_ids = fields.One2many('project.task', 'parent_id', 'Sub-tasks')
    parent_id = fields.Many2one('project.task', 'Parent Task')
    child_ids = fields.One2many('project.task', 'parent_id', 'Child Tasks')
    active = fields.Boolean('Active', default=True)
    color = fields.Integer('Color')
    legend_blocked = fields.Char('Blocked', default='Blocked')
    legend_done = fields.Char('Done', default='Done')
    legend_normal = fields.Char('In Progress', default='In Progress')
```

#### 任务功能

- **任务信息**：
  - `name`：任务标题（必填）
  - `description`：任务描述
  - `project_id`：所属项目
  - `stage_id`：任务阶段

- **分配信息**：
  - `user_ids`：任务分配人（多选）
  - `user_id`：主要负责人
  - `partner_id`：客户（外部客户项目）

- **时间信息**：
  - `date_deadline`：截止日期
  - `date_assign`：分配日期
  - `date_last_stage_update`：最后阶段更新日期

- **优先级和状态**：
  - `priority`：优先级（低/正常/高/非常高）
  - `kanban_state`：看板状态（进行中/就绪/阻塞）
  - `state`：任务状态

- **子任务**：
  - `subtask_ids`：子任务
  - `parent_id`：父任务
  - 支持多层级子任务

### 3. 项目阶段（Stages）

项目阶段用于跟踪任务进展。

#### 阶段模型

```
class ProjectTaskType(models.Model):
    _name = 'project.task.type'
    _description = 'Task Stage'
    
    name = fields.Char('Stage Name', required=True)
    description = fields.Text('Description')
    sequence = fields.Integer('Sequence', default=10)
    project_ids = fields.Many2many('project.project', 'project_stage_rel', 
                                  'stage_id', 'project_id', 'Projects')
    fold = fields.Boolean('Folded in Kanban')
    mail_template_id = fields.Many2one('mail.template', 'Email Template')
```

#### 阶段功能

- **阶段定义**：为项目定义任务阶段
- **阶段顺序**：控制阶段显示顺序
- **折叠功能**：看板视图中可折叠
- **邮件模板**：阶段变更时自动发送邮件

#### 典型阶段示例

```
待办（To Do）
 ↓
进行中（In Progress）
 ↓
审查中（Review）
 ↓
已完成（Done）
```

### 4. 项目看板（Kanban）

看板视图提供直观的项目和任务管理。

#### 看板功能

- **卡片展示**：项目和任务以卡片形式展示
- **阶段列**：按阶段分组显示
- **拖拽操作**：拖拽卡片变更阶段
- **看板状态**：进行中/就绪/阻塞（用颜色标识）

#### 看板配置

- 自定义阶段列
- 设置卡片显示字段
- 配置看板颜色和样式

### 5. 项目团队协作

#### 团队成员

- **项目经理**：管理整个项目
- **任务分配人**：分配给具体的团队成员
- **客户**：项目的外部客户

#### 协作功能

- **Chatter**：任务和项目下的讨论
- **活动跟踪**：记录项目活动
- **通知**：状态变更自动通知相关人员
- **文档共享**：共享项目文档

### 6. 项目报表和分析

#### 报表类型

- **项目概览**：项目进度和状态
- **任务报表**：任务完成情况
- **工时报表**：项目工时统计（需 `hr_timesheet`）
- **成本报表**：项目成本分析（需 `sale_project`）
- **项目仪表板**：关键指标（KPI）

---

## 三、核心模型详解

### 1. `project.project` - 项目

**主要字段**：
- `name`：项目名称（必填）
- `description`：项目描述
- `partner_id`：客户
- `user_id`：项目经理
- `date_start`：开始日期
- `date`：结束日期
- `state`：项目状态
- `task_ids`：项目任务
- `task_count`：任务总数（计算）
- `task_count_open`：未完成任务数（计算）

**使用示例**：

```python
# 创建项目
project = self.env['project.project'].create({
    'name': '网站开发项目',
    'description': '为客户开发新网站',
    'partner_id': customer.id,
    'user_id': manager.id,
    'date_start': '2024-01-01',
    'date': '2024-06-30',
})

# 查找项目
projects = self.env['project.project'].search([
    ('state', '=', 'in_progress'),
])
```

### 2. `project.task` - 任务

**主要字段**：
- `name`：任务标题（必填）
- `description`：任务描述
- `project_id`：所属项目
- `stage_id`：任务阶段
- `user_ids`：分配人（多选）
- `user_id`：主要负责人
- `date_deadline`：截止日期
- `priority`：优先级
- `kanban_state`：看板状态
- `parent_id`：父任务
- `subtask_ids`：子任务

**使用示例**：

```python
# 创建任务
task = self.env['project.task'].create({
    'name': '设计首页',
    'project_id': project.id,
    'user_id': developer.id,
    'date_deadline': '2024-02-15',
    'priority': '2',  # 高优先级
})

# 分配任务
task.write({
    'user_ids': [(6, 0, [user1.id, user2.id])],
})

# 创建子任务
subtask = self.env['project.task'].create({
    'name': '设计登录页面',
    'parent_id': task.id,
    'project_id': project.id,
})
```

---

## 四、与其他模块的集成

### 1. 与 `sale` 模块（需 `sale_project`）

**销售项目**：
- 从销售订单创建项目
- 项目关联销售订单
- 项目完成时自动生成发票

**工作流程**：
```
创建销售订单（服务型）
 ↓
确认订单
 ↓
自动创建项目
 ↓
项目执行
 ↓
项目完成，生成发票
```

### 2. 与 `hr_timesheet` 模块

**工时跟踪**：
- 记录项目工时
- 工时审批
- 工时分析报表

**使用场景**：
- 团队成员记录在项目上的工时
- 项目经理审批工时
- 基于工时计算项目成本

### 3. 与 `sale_timesheet` 模块

**工时计费**：
- 工时自动转换为费用
- 生成项目发票
- 成本核算

### 4. 与 `hr` 模块

**团队管理**：
- 项目团队成员管理
- 员工分配到项目
- 项目团队统计

### 5. 与 `mail` 模块

**沟通协作**：
- 项目 Chatter 功能
- 任务讨论
- 状态变更通知

### 6. 与 `account` 模块

**项目计费**：
- 项目成本核算
- 项目收入跟踪
- 项目利润分析

---

## 五、项目工作流程

### 1. 项目启动流程

```
1. 创建项目
   - 输入项目信息
   - 选择客户（如有）
   - 指定项目经理
   ↓
2. 配置项目
   - 设置项目阶段
   - 添加项目标签
   - 配置项目团队
   ↓
3. 创建任务
   - 分解项目为任务
   - 分配任务给团队成员
   - 设置任务优先级和截止日期
   ↓
4. 启动项目
   - 项目状态设为"进行中"
   - 通知项目团队
```

### 2. 任务执行流程

```
1. 任务分配
   - 分配给团队成员
   - 设置截止日期
   - 设置优先级
   ↓
2. 任务执行
   - 团队成员更新任务进度
   - 记录遇到的问题
   - 添加任务备注
   ↓
3. 任务审查
   - 任务完成后进入审查阶段
   - 审查人员检查任务质量
   ↓
4. 任务完成
   - 任务阶段设为"已完成"
   - 更新项目进度
```

### 3. 项目完成流程

```
1. 所有任务完成
   ↓
2. 项目审查
   - 审查项目交付物
   - 客户验收
   ↓
3. 项目结算
   - 生成项目发票（如有）
   - 记录项目成本
   ↓
4. 项目归档
   - 项目状态设为"已完成"
   - 归档项目文档
   - 项目经验总结
```

---

## 六、典型使用场景

### 场景 1：软件开发项目

**需求**：管理一个软件开发项目

**步骤**：

1. **创建项目**
   - 项目名称：客户管理系统开发
   - 项目经理：技术总监
   - 开始日期和结束日期

2. **创建任务**
   - 需求分析
   - 系统设计
   - 前端开发
   - 后端开发
   - 测试
   - 部署

3. **分配任务**
   - 每个任务分配给相应的开发人员
   - 设置优先级和截止日期

4. **跟踪进度**
   - 团队成员更新任务状态
   - 项目经理查看项目进度
   - 处理阻塞的任务

### 场景 2：服务型项目

**需求**：管理一个咨询服务项目

**步骤**：

1. **从销售订单创建项目**
   - 销售订单确认后自动创建项目
   - 项目自动关联客户

2. **项目执行**
   - 创建咨询任务
   - 团队成员记录工时
   - 客户沟通和反馈

3. **项目结算**
   - 基于工时自动生成发票
   - 项目成本核算
   - 项目利润分析

### 场景 3：内部项目

**需求**：管理一个内部改进项目

**步骤**：

1. **创建内部项目**
   - 不需要客户
   - 指定内部项目经理

2. **任务管理**
   - 分解项目为任务
   - 分配给不同部门
   - 跟踪完成情况

---

## 七、配置和设置

### 1. 项目配置

#### 步骤 1：创建项目类型

1. **项目 > 配置 > 项目类型**
2. 定义不同类型的项目
3. 为每种类型配置默认设置

#### 步骤 2：配置项目阶段

1. **项目 > 配置 > 项目阶段**
2. 定义项目阶段
3. 设置阶段顺序
4. 配置阶段邮件模板（可选）

#### 步骤 3：创建项目

1. **项目 > 项目**
2. 创建新项目
3. 填写项目信息
4. 配置项目设置

### 2. 任务配置

#### 配置任务阶段

1. **项目 > 配置 > 任务阶段**
2. 定义任务阶段
3. 设置阶段顺序
4. 为每个阶段配置默认行为

#### 配置任务标签

1. **项目 > 配置 > 标签**
2. 创建常用标签
3. 标签可以用于筛选和分组

### 3. 权限配置

#### 项目访问权限

- **项目成员**：可以查看和更新自己的任务
- **项目经理**：可以管理项目所有任务
- **客户**：可以查看项目进度（通过门户）

---

## 八、最佳实践

### 1. 项目规划

- **清晰的项目目标**：明确项目要达成什么
- **合理的任务分解**：将项目分解为可管理的任务
- **明确的截止日期**：为项目和任务设置合理的截止日期

### 2. 任务管理

- **及时更新状态**：任务进度及时更新
- **明确的责任人**：每个任务都有明确的责任人
- **优先级管理**：合理设置任务优先级

### 3. 团队协作

- **有效沟通**：利用 Chatter 进行沟通
- **及时反馈**：任务状态变更及时通知相关人员
- **文档管理**：共享和保存项目文档

### 4. 进度跟踪

- **定期审查**：定期审查项目进度
- **识别风险**：及时发现和解决项目风险
- **调整计划**：根据实际情况调整项目计划

---

## 九、常见问题

### 问题 1：无法创建任务

**原因**：缺少必填字段或权限不足

**解决方案**：
1. 确保项目已创建
2. 检查用户权限
3. 确认任务名称已填写

### 问题 2：任务无法分配给用户

**原因**：用户不在项目团队中

**解决方案**：
1. 将用户添加到项目团队
2. 或直接在任务上分配（会自动添加）

---

## 十、总结

- **`project` 模块**提供完整的项目管理功能。
- 核心功能：
  - 项目和任务管理
  - 项目阶段和看板
  - 团队协作
  - 项目报表和分析
  - 与销售、工时、会计等模块的深度集成
- 支持项目全生命周期管理。
- 适用于各种类型的项目：软件开发、咨询服务、内部改进等。
- 提供灵活的任务管理和团队协作功能。

