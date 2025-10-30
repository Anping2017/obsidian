# 💵 Odoo `hr_payroll` 模块详解

## 一、`hr_payroll` 模块的作用

- **薪资管理模块**，扩展 `hr` 模块的薪资功能。
- 管理员工工资单的计算、生成和支付。
- 支持复杂的薪资规则和计算逻辑。
- 与会计模块集成，自动生成薪资会计凭证。
- 支持多种薪资结构、扣除项、津贴等。

📌 形象理解：  
👉 `hr_payroll` 模块是"薪资系统"，自动计算和管理员工工资。

---

## 二、核心功能

### 1 form工资单管理

#### 工资单模型

```
class HrPayslip(models.Model):
    _name = 'hr.payslip'
    _description = 'Pay Slip'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Payslip Name')
    struct_id = fields.Many2one('hr.payroll.structure', 'Structure', required=True)
    employee_id = fields.Many2one('hr.employee', 'Employee', required=True)
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Waiting'),
        ('done', 'Done'),
        ('cancel', 'Rejected')
    ], string='Status', default='draft')
    
    line_ids = fields.One2many('hr.payslip.line', 'slip_id', 'Payslip Lines')
    worked_days_line_ids = fields.One2many('hr.payslip.worked_days', 'payslip_id', 
                                           'Payslip Worked Days')
    input_line_ids = fields.One2many('hr.payslip.input', 'payslip_id', 
                                     'Other Inputs')
    
    company_id = fields.Many2one('res.company', 'Company', required=True)
    contract_id = fields.Many2one('hr.contract', 'Contract', required=True)
    credit_note = fields.Boolean('Credit Note')
    
    paid = fields.Boolean('Paid')
    journal_id = fields.Many2one('account.journal', 'Salary Journal')
    move_id = fields.Many2one('account.move', 'Accounting Entry')
```

#### 工资单状态

- **草稿**（Draft）：已创建，未计算
- **等待**（Verify）：已计算，等待验证
- **完成**（Done）：已验证，已完成
- **已拒绝**（Cancel）：已取消

#### 工资单行模型

```
class HrPayslipLine(models.Model):
    _name = 'hr.payslip.line'
    _description = 'Payslip Line'
    
    slip_id = fields.Many2one('hr.payslip', 'Payslip', required=True)
    salary_rule_id = fields.Many2one('hr.salary.rule', 'Rule', required=True)
    employee_id = fields.Many2one('hr.employee', 'Employee', required=True)
    
    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    category_id = fields.Many2one('hr.salary.rule.category', 'Category')
    
    quantity = fields.Float('Quantity', default=1.0)
    amount = fields.Float('Amount', required=True)
    total = fields.Float('Total', compute='_compute_total')
    
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)
```

### 2. 薪资结构（Salary Structure）

薪资结构定义了工资单的计算规则。

#### 薪资结构模型

```
class HrPayrollStructure(models.Model):
    _name = 'hr.payroll.structure'
    _description = 'Salary Structure'
    
    name = fields.Char('Name', required=True)
    code = fields.Char('Structure Code')
    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one('res.company', 'Company', required=True)
    
    rule_ids = fields.Many2many('hr.salary.rule', 'hr_structure_salary_rule_rel',
                                'struct_id', 'rule_id', 'Salary Rules')
    parent_id = fields.Many2one('hr.payroll.structure', 'Parent Structure')
    children_ids = fields.One2many('hr.payroll.structure', 'parent_id', 
                                   'Children Structures')
```

#### 薪资结构类型

- **基础结构**：包含基本薪资规则
- **子结构**：继承父结构，添加额外规则
- **合同结构**：员工合同关联的薪资结构

### 3. 薪资规则（Salary Rules）

薪资规则定义了工资单行的计算逻辑。

#### 薪资规则模型

```
class HrSalaryRule(models.Model):
    _name = 'hr.salary.rule'
    _description = 'Salary Rule'
    
    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    category_id = fields.Many2one('hr.salary.rule.category', 'Category', 
                                  required=True)
    active = fields.Boolean('Active', default=True)
    
    sequence = fields.Integer('Sequence', required=True, default=5)
    struct_id = fields.Many2one('hr.payroll.structure', 'Structure')
    
    condition_select = fields.Selection([
        ('none', 'Always True'),
        ('range', 'Range'),
        ('python', 'Python Expression')
    ], string='Condition Based on', default='none', required=True)
    
    condition_range = fields.Char('Range Based on', 
                                  help='This will be used to compute the % fields values; in general it is on basic, but you can also use categories code fields in lowercase as a variable names (hra, ma, lta, etc.) and the variable \'rules\' to refer to sum of all rules belonging to the selected category.')
    
    amount_select = fields.Selection([
        ('percentage', 'Percentage (%)'),
        ('fix', 'Fixed Amount'),
        ('code', 'Python Code'),
        ('python', 'Python Code')
    ], string='Amount Type', default='fix', required=True)
    
    amount_fix = fields.Float('Fixed Amount')
    amount_percentage = fields.Float('Percentage (%)')
    amount_python_compute = fields.Text('Python Code')
    
    quantity = fields.Char('Quantity', default='1.0',
                          help='It is used in computation. For e.g. If you put condition as \'result = inputs.wage > 10000\' and quantity as \'result = inputs.wage / 1000\'. Then it will compute the percentage from the code result.')
    rate = fields.Float('Rate (%)', default=100.0)
```

#### 薪资规则类型

- **收入规则**：
  - 基本工资
  - 奖金
  - 津贴（交通、餐补等）
  - 加班费

- **扣除规则**：
  - 社会保险（养老、医疗、失业等）
  - 公积金
  - 个人所得税
  - 其他扣除

- **计算规则**：
  - 基于其他规则的百分比
  - 基于固定金额
  - 基于Python代码计算

### 4. 薪资规则类别（Categories）

薪资规则类别用于组织和汇总。

#### 类别模型

```
class HrSalaryRuleCategory(models.Model):
    _name = 'hr.salary.rule.category'
    _description = 'Salary Rule Category'
    
    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    parent_id = fields.Many2one('hr.salary.rule.category', 'Parent Category')
    child_ids = fields.One2many('hr.salary.rule.category', 'parent_id', 
                                'Child Categories')
```

#### 常用类别

- **基础**（BASIC）：基本工资
- **总额**（GROSS）：税前总额
- **扣除**（DEDUCTION）：扣除总额
- **净额**（NET）：税后净额

### 5. 工作天数（Worked Days）

#### 工作天数模型

```
class HrPayslipWorkedDays(models.Model):
    _name = 'hr.payslip.worked_days'
    _description = 'Payslip Worked Days'
    
    payslip_id = fields.Many2one('hr.payslip', 'Payslip', required=True)
    name = fields.Char('Description', required=True)
    code = fields.Char('Code', required=True)
    number_of_days = fields.Float('Number of Days')
    number_of_hours = fields.Float('Number of Hours')
    contract_id = fields.Many2one('hr.contract', 'Contract')
```

#### 工作天数类型

- **出勤天数**：正常工作日
- **请假天数**：请假天数
- **加班时间**：加班小时数
- **缺勤天数**：缺勤天数

---

## 三、薪资计算流程

### 1. 工资单创建流程

```
1. 选择员工和期间
   ↓
2. 选择薪资结构（或使用合同结构）
   ↓
3. 加载合同信息
   - 基本工资
   - 薪资结构
   ↓
4. 加载工作天数
   - 从考勤模块获取（如安装了hr_attendance）
   - 或手动输入
   ↓
冰冻5. 计算工资单
   - 执行薪资规则
   - 计算各项收入
   - 计算各项扣除
   - 计算净工资
   ↓
6. 验证工资单
   - 检查计算结果
   - 审核工资单
   ↓
7. 确认工资单
   - 确认后生成会计凭证（如配置）
```

### 2. 薪资规则计算顺序

```
1. 基础工资（BASIC）
   ↓
2. 各种津贴和奖金
   ↓
3. 计算税前总额（GROSS）
   ↓
4. 社会保险和公积金
   ↓
5. 个人所得税
   ↓
6. 其他扣除
   ↓
7. 计算净工资（NET）
```

### 3. 薪资规则计算示例

#### 示例：计算基本工资

```python
# 基本工资规则
规则名称：基本工资
代码：BASIC
类别：BASIC（基础）
计算方式：固定金额
固定金额：从合同读取（contract.wage）
```

#### 示例：计算社会保险

```python
# 养老保险规则（8%）
规则名称：养老保险（个人）
代码：SI_EMP
类别：DEDUCTION（扣除）
计算方式：百分比
基础：GROSS（税前总额）
百分比：8%
```

#### 示例：计算个人所得税

```python
# 个人所得税规则
规则 comments名称：个人所得税
代码：INCOME_TAX
类别：DEDUCTION（扣除）
计算方式：Python代码
计算逻辑：
  if GROSS - DEDUCTION <= 5000:
      tax = 0
  elif GROSS - DEDUCTION <= 8000:
      tax = (GROSS - DEDUCTION - 5000) * 0.03
  # ... 其他税率档次
```

---

## 四、与其他模块的集成

### 1. 与 `hr` 模块

- **员工信息**：从员工档案获取信息
- **合同信息**：从员工合同获取薪资信息
- **部门信息**：用于部门成本分摊

### 2. 与 `hr_contract` 模块

- **合同工资**：从合同获取基本工资
- **薪资结构**：从合同获取薪资结构
- **合同期间**：确定工资单期间

### 3. 与 `hr_attendance` 模块

- **考勤数据**：获取工作天数
- **加班时间**：计算加班费
- **缺勤扣除**：缺勤扣款

### 4. 与 `account` 模块

- **会计凭证**：工资单确认后生成会计凭证
- **成本核算**：薪资计入相应成本科目
- **应付工资**：计入应付工资科目

---

## 五、典型使用场景

### 场景 1：月度工资计算

**需求**：每月计算所有员工的工资

**详细步骤**：

1. **创建工资单批次**
   ```
   薪资 > 工资单 > 创建工资单批次
   - 选择工资期间（如2024年1月）
   - 选择员工（或全部员工）
   - 选择薪资结构
   ```

2. **批量生成工资单**
   - 系统为每个员工创建工资单
   - 自动加载合同信息
   - 自动加载工作天数

3. **计算工资单**
   ```
   批量计算：
   - 选择所有工资单
   - 点击"计算工资单"
   - 系统执行薪资规则计算
   ```

4. **审核工资单**
   - 逐一检查工资单
   - 验证计算结果
   - 确认无误后验证

5. **确认工资单**
   - 批量确认工资单
   - 生成会计凭证（如配置）
   - 准备发放工资

### 场景 2：工资单调整

**需求**：调整某个员工的工资单

**步骤**：

1. **打开工资单**
   - 找到需要调整的工资单

2. **添加额外输入**
   ```
   其他输入：
   - 奖金：1000元
   - 其他调整：-200元（如扣除）
   ```

3. **重新计算**
   - 点击"计算工资单"
   - 系统重新计算包含额外输入的工资

4. **验证和确认**
   - 检查调整后的结果
   - 确认工资单

---

## 六、配置和设置

### 1. 薪资结构配置

#### 创建薪资结构

1. **薪资 > 配置 > 薪资结构**
2. 创建新结构：
   - **名称**：如"标准薪资结构"
   - **代码**：唯一代码
   - **薪资规则**：添加薪资规则

#### 配置薪资规则顺序

- **规则顺序**：规则按顺序执行
- **依赖关系**：某些规则依赖其他规则的结果
- **优先级**：使用sequence字段控制顺序

### 2. 薪资规则配置

#### 创建薪资规则

1. **薪资 > 配置 > 薪资规则**
2. 创建新规则：
   - RCA **名称和代码**：规则标识
   - **类别**：规则类别
   - **计算方式**：固定金额/百分比/Python代码
   - **条件**：应用规则的条件

#### Python代码示例

```python
# 计算加班费
if worked_days.OVERTIME_HOURS > 0:
    result = contract.wage / 174 * 1.5 * worked_days.OVERTIME_HOURS
else:
    result = 0

# 计算绩效奖金（基于绩效评分）
if inputs.PERFORMANCE_SCORE >= 90:
    result = contract.wage * 0.2  # 20%绩效奖金
elif inputs.PERFORMANCE_SCORE >= 80:
    result = contract.wage * 0.1  # 10%绩效奖金
else:
    result = 0
```

### 3. 会计集成配置

#### 配置薪资日记账

1. **薪资 > 配置 > 设置**
2. **会计**选项卡：
   - **薪资日记账**：选择薪资日记账
   - **默认科目**：配置默认科目
   - **自动记账**：是否自动生成会计凭证

#### 科目配置

- **薪资费用科目**：员工薪资计入的费用科目
- **应付工资科目**：应付工资负债科目
- **社会保险科目**：社会保险费用科目
- **个人所得税科目**：个人所得税费用科目

---

## 七、最佳实践

### 1. 薪资结构设计

- **标准化**：使用标准化的薪资结构
- **灵活性**：支持不同类型的员工
- **清晰性**：规则逻辑清晰易懂

### 2. 薪资计算

- **准确性**：确保计算准确性
- **验证**：计算后进行验证
- **审计**：保留计算历史和记录

### 3. 薪资发放

- **及时性**：按时发放工资
- **准确性**：确保金额准确
- **合规性**：符合法律法规要求

---

## 八、总结

- **`hr_payroll` 模块**提供完整的薪资管理功能。
- 核心功能：
  - 工资单计算和管理
  - 灵活的薪资结构
  - 复杂的薪资规则
  - 工作天数管理
  - 与考勤、合同、会计模块的集成
- 支持各种复杂的薪资计算需求。
- 确保薪资计算的准确性和合规性。

