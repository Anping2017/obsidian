# 👥 Odoo `hr` 模块详解

## 一、`hr` 模块的作用

- **人力资源管理核心模块**，所有 HR 相关模块的基础。
- 管理员工档案、组织架构、部门、职位等核心人力资源信息。
- 提供基础的人事管理功能。
- 与其他 HR 模块（薪资、考勤、招聘等）集成，构建完整的 HR 系统。

📌 形象理解：  
👉 `hr` 模块是 HR 系统的"核心数据库"，管理所有员工和组织结构信息。

---

## 二、核心功能

### 1. 员工档案管理（Employee Records）

员工档案是 HR 系统的核心数据。

#### 员工模型

```
class HrEmployee(models.Model):
    _name = 'hr.employee'
    _description = 'Employee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Employee Name', required=True)
    employee_identification_id = fields.Char('ID Number')
    work_phone = fields.Char('Work Phone')
    mobile_phone = fields.Char('Work Mobile')
    work_email = fields.Char('Work Email')
    work_location = fields.Char('Work Location')
    department_id = fields.Many2one('hr.department', 'Department')
    job_id = fields.Many2one('hr.job', 'Job Position')
    manager_id = fields.Many2one('hr.employee', 'Manager')
    coach_id = fields.Many2one('hr.employee', 'Coach')
    address_home_id = fields.Many2one('res.partner', 'Home Address')
    birthday = fields.Date('Birthday')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status')
    country_id = fields.Many2one('res.country', 'Nationality')
    active = fields.Boolean('Active', default=True)
    employee_type = fields.Selection([
        ('employee', 'Employee'),
        ('student', 'Student'),
        ('trainee', 'Trainee'),
        ('contractor', 'Contractor'),
        ('freelance', 'Freelancer')
    ], string='Employee Type')
```

#### 员工信息字段

- **基本信息**：
  - `name`：姓名
  - `employee_identification_id`：员工编号/身份证号
  - `work_email`：工作邮箱
  - `work_phone`：工作电话
  - `mobile_phone`：手机号

- **组织信息**：
  - `department_id`：所属部门
  - `job_id`：职位
  - `manager_id`：直属上级
  - `coach_id`：导师/教练

- **个人信息**：
  - `birthday`：生日
  - `gender`：性别
  - `marital`：婚姻状况
  - `country_id`：国籍

- **地址信息**：
  - `address_home_id`：家庭地址
  - `work_location`：工作地点

### 2. 组织架构和部门管理

#### 部门模型

```
class HrDepartment(models.Model):
    _name = 'hr.department'
    _description = 'HR Department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Department Name', required=True)
    complete_name = fields.Char('Complete Name', compute='_compute_complete_name')
    parent_id = fields.Many2one('hr.department', 'Parent Department')
    child_ids = fields.One2many('hr.department', 'parent_id', 'Child Departments')
    manager_id = fields.Many2one('hr.employee', 'Manager')
    member_ids = fields.One2many('hr.employee', 'department_id', 'Members')
    company_id = fields.Many2one('res.company', 'Company')
```

#### 部门层级结构

- **多层级支持**：支持无限层级的部门结构
- **部门树形视图**：可视化显示部门层级
- **部门经理**：每个部门可以指定经理
- **部门成员**：自动关联部门下的员工

#### 典型部门结构示例

```
公司
 ├── 管理层
 ├── 销售部
 │    ├── 销售一部
 │    └── 销售二部
 ├── 市场部
 ├── 技术部
 │    ├── 开发部
 │    └── 测试部
 ├── 人力资源部
 └── 财务部
```

### 3. 职位管理（Job Positions）

#### 职位模型

```
class HrJob(models.Model):
    _name = 'hr.job'
    _description = 'Job Position'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Job Position', required=True)
    expected_employees = fields.Integer('Expected New Employees')
    no_of_employee = fields.Integer('Number of Employees', compute='_compute_employee_count')
    no_of_recruitment = fields.Integer('Number of New Recruitment', default=1)
    description = fields.Html('Job Description')
    requirements = fields.Text('Requirements')
    department_id = fields.Many2one('hr.department', 'Department')
    employee_ids = fields.One2many('hr.employee', 'job_id', 'Employees')
    state = fields.Selection([
        ('recruit', 'Recruitment in Progress'),
        ('open', 'Open'),
        ('close', 'Closed')
    ], string='Status', default='recruit')
```

#### 职位功能

- **职位定义**：定义公司中的各种职位
- **职位描述**：详细的职位描述和要求
- **招聘关联**：与招聘模块集成（`hr_recruitment`）
- **员工统计**：统计每个职位的员工数量
- **职位状态**：招聘中、开放、关闭

### 4. 员工关系管理

#### 上下级关系

- **Manager（经理）**：员工的直接上级
- **Coach（导师）**：员工的指导者
- **组织结构图**：可视化显示上下级关系

#### 员工视图

- **列表视图**：员工列表，可筛选和分组
- **表单视图**：详细员工信息
- **看板视图**：按部门或职位显示员工卡片
- **组织结构图**：可视化组织架构

### 5. 员工信息跟踪

- **活动记录**：记录与员工相关的活动
- **历史记录**：跟踪员工信息变更
- **文档管理**：关联员工相关文档

---

## 三、核心模型详解

### 1. `hr.employee` - 员工

**主要字段说明**：

- `name`：员工姓名（必填）
- `employee_identification_id`：员工编号或身份证号
- `work_email`：工作邮箱
- `work_phone`：工作电话
- `mobile_phone`：手机号
- `department_id`：所属部门
- `job_id`：职位
- `manager_id`：直接上级
- `coach_id`：导师
- `address_home_id`：家庭地址（关联到 `res.partner`）
- `birthday`：生日
- `gender`：性别
- `marital`：婚姻状况
- `country_id`：国籍
- `active`：是否在职（默认为 True）

**使用示例**：

```python
# 创建员工
employee = self.env['hr.employee'].create({
    'name': '张三',
    'employee_identification_id': 'EMP001',
    'work_email': 'zhangsan@company.com',
    'work_phone': '010-12345678',
    'mobile_phone': '13800138000',
    'department_id': department.id,
    'job_id': job.id,
    'manager_id': manager.id,
    'birthday': '1990-01-01',
    'gender': 'male',
    'marital': 'married',
})

# 查找员工
employees = self.env['hr.employee'].search([
    ('department_id', '=', department.id),
    ('active', '=', True),
])
```

### 2. `hr.department` - 部门

**主要字段说明**：

- `name`：部门名称（必填）
- `complete_name`：完整路径（计算字段，如"公司/技术部/开发部"）
- `parent_id`：上级部门
- `child_ids`：下级部门
- `manager_id`：部门经理
- `member_ids`：部门成员（通过 `hr.employee.department_id` 反向关联）
- `company_id`：所属公司（多公司支持）

**使用示例**：

```python
# 创建部门
dept = self.env['hr.department'].create({
    'name': '技术部',
    'manager_id': manager.id,
    'company_id': self.env.company.id,
})

# 查找部门及其成员
dept = self.env['hr.department'].browse(dept_id)
employees = dept.member_ids
```

### 3. `hr.job` - 职位

**主要字段说明**：

- `name`：职位名称（必填）
- `description`：职位描述（HTML）
- `requirements`：任职要求
- `department_id`：所属部门
- `employee_ids`：该职位的员工（反向关联）
- `expected_employees`：预期新员工数
- `no_of_employee`：当前员工数（计算字段）
- `no_of_recruitment`：招聘人数
- `state`：状态（招聘中/开放/关闭）

---

## 四、与其他模块的集成

### 1. 与 `hr_contract` 模块

- 员工合同信息关联
- 合同状态影响员工状态

### 2. 与 `hr_payroll` 模块

- 员工薪资信息
- 薪资计算基于员工信息

### 3. 与 `hr_attendance` 模块

- 考勤记录关联员工
- 部门考勤统计

### 4. 与 `hr_recruitment` 模块

- 职位发布和招聘
- 候选人转为员工

### 5. 与 `hr_holidays` 模块

- 请假申请关联员工
- 部门假期统计

### 6. 与 `project` 模块

- 项目团队成员管理
- 员工分配到项目

### 7. 与 `account` 模块

- 员工成本核算
- 部门成本分配

### 8. 与 `mail` 模块

- 员工 Chatter 功能
- 员工活动记录

---

## 五、典型使用场景

### 场景 1：新员工入职

**需求**：录入新员工信息

**步骤**：

1. **创建员工档案**
   - 输入基本信息（姓名、邮箱、电话等）
   - 选择部门
   - 选择职位
   - 设置上级

2. **完善个人信息**
   - 输入生日、性别等
   - 添加家庭地址
   - 上传照片

3. **关联其他模块**
   - 创建员工合同（`hr_contract`）
   - 设置考勤规则（`hr_attendance`）
   - 初始化薪资信息（`hr_payroll`）

### 场景 2：组织架构调整

**需求**：调整部门结构或员工调动

**步骤**：

1. **创建或调整部门**
   - 新增部门
   - 调整部门层级
   - 指定部门经理

2. **员工调动**
   - 修改员工的部门
   - 修改员工的职位
   - 修改上级关系

3. **更新信息**
   - 系统自动更新相关统计
   - 通知相关人员

### 场景 3：员工信息查询

**需求**：查看员工或部门信息

**步骤**：

1. **查看员工列表**
   - 按部门筛选
   - 按职位筛选
   - 搜索特定员工

2. **查看员工详情**
   - 基本信息
   - 组织关系
   - 活动历史

3. **查看部门信息**
   - 部门成员列表
   - 部门层级结构
   - 部门统计

---

## 六、配置和设置

### 1. 基本配置

#### 步骤 1：创建部门

1. 进入 **员工 > 配置 > 部门**
2. 创建部门层级
3. 为每个部门指定经理

#### 步骤 2：创建职位

1. 进入 **员工 > 配置 > 职位**
2. 创建各种职位
3. 填写职位描述和要求

#### 步骤 3：创建员工

1. 进入 **员工 > 员工**
2. 创建员工档案
3. 填写员工信息
4. 分配部门和职位

### 2. 权限配置

#### 员工信息访问权限

- **普通员工**：只能查看自己的信息
- **部门经理**：可以查看部门成员信息
- **HR 管理员**：可以查看和修改所有员工信息

#### 权限规则示例

```
# 员工只能查看自己的信息
<record id="hr_employee_rule" model="ir.rule">
    <field name="name">Employee: own employee</field>
    <field name="model_id" ref="hr.model_hr_employee"/>
    <field name="domain_force">[('id', '=', user.employee_ids.ids)]</field>
</record>
```

### 3. 组织架构配置

#### 设置公司结构

1. 定义公司层级
2. 创建主要部门
3. 创建子部门
4. 指定部门经理

#### 设置职位体系

1. 定义职位类别
2. 为每个部门创建职位
3. 填写职位描述

---

## 七、高级功能

### 1. 组织结构图

- 可视化显示组织架构
- 显示层级关系
- 显示部门经理和成员

### 2. 员工统计分析

- 按部门统计员工数
- 按职位统计员工数
- 员工年龄分布
- 员工性别分布

### 3. 员工查找和搜索

- 快速搜索员工
- 多条件筛选
- 保存搜索条件

### 4. 批量操作

- 批量更新员工信息
- 批量调整部门
- 批量导入员工

---

## 八、最佳实践

### 1. 部门结构设计

- **层级清晰**：避免过深的层级
- **职责明确**：每个部门职责清晰
- **命名规范**：统一的命名规则

### 2. 员工信息管理

- **信息完整**：确保员工信息完整准确
- **及时更新**：员工信息变更及时更新
- **数据验证**：验证邮箱、电话等格式

### 3. 组织架构维护

- **定期审核**：定期检查和更新组织架构
- **及时调整**：人员变动及时调整
- **保持同步**：确保系统与实际组织架构一致

---

## 九、常见问题

### 问题 1：无法创建员工

**原因**：缺少必填字段或权限不足

**解决方案**：
1. 检查必填字段（姓名是必填的）
2. 检查用户权限
3. 确认部门已创建

### 问题 2：员工看不到自己的信息

**原因**：记录规则限制

**解决方案**：
1. 检查记录规则配置
2. 确认员工与用户账户关联
3. 调整权限设置

---

## 十、总结

- **`hr` 模块**是 Odoo HR 系统的核心基础。
- 核心功能：
  - 员工档案管理
  - 组织架构和部门管理
  - 职位管理
  - 员工关系管理
  - 与其他 HR 模块的深度集成
- 提供完整的员工和组织架构管理功能。
- 是构建 HR 管理系统的基础模块。
- 支持多层级部门结构和灵活的职位体系。

