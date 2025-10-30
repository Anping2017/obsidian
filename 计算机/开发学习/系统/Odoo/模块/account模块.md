# 💰 Odoo `account` 模块详解

## 一、`account` 模块的作用

- **财务会计核心模块**，所有财务相关模块的基础。
- 提供完整的会计功能：会计科目、日记账、发票、付款等。
- 管理会计科目表、日记账分录、发票和账单、银行对账等。
- 是财务业务的基础模块，与销售、采购、库存等模块深度集成。

📌 形象理解：  
👉 `account` 模块是 Odoo 的"财务大脑"，记录和跟踪所有财务交易。

---

## 二、核心功能

### 1. 会计科目表（Chart of Accounts）

会计科目表是所有财务交易的基础分类体系。

#### 科目结构

- **多层级科目结构**：支持无限层级的科目分类
- **科目类型**：资产、负债、权益、收入、费用等
- **科目属性**：币种、科目类型、余额方向等
- **科目余额跟踪**：实时计算和跟踪科目余额

#### 科目模型

```
class AccountAccount(models.Model):
    _name = 'account.account'
    _description = 'Account'
    
    name = fields.Char('Account Name', required=True)
    code = fields.Char('Code', required=True)
    account_type = fields.Selection([
        ('asset_receivable', 'Receivable'),
        ('asset_cash', 'Bank and Cash'),
        ('asset_current', 'Current Assets'),
        ('asset_non_current', 'Non-current Assets'),
        ('asset_prepayments', 'Prepayments'),
        ('asset_fixed', 'Fixed Assets'),
        ('liability_payable', 'Payable'),
        ('liability_credit_card', 'Credit Card'),
        ('liability_current', 'Current Liabilities'),
        ('liability_non_current', 'Non-current Liabilities'),
        ('equity', 'Equity'),
        ('equity_unaffected', 'Current Year Earnings'),
        ('income', 'Income'),
        ('income_other', 'Other Income'),
        ('expense', 'Expenses'),
        ('expense_depreciation', 'Depreciation'),
        ('expense_direct_cost', 'Cost of Revenue'),
        ('off_balance', 'Off-Balance Sheet'),
    ], string='Account Type', required=True)
    company_id = fields.Many2one('res.company', 'Company')
    currency_id = fields.Many2one('res.currency', 'Currency')
    reconcile = fields.Boolean('Allow Reconciliation')
    parent_id = fields.Many2one('account.account', 'Parent Account')
    child_ids = fields.One2many('account.account', 'parent_id', 'Child Accounts')
```

#### 科目类型说明

- **资产类**（Asset）：
  - `asset_receivable`：应收账款
  - `asset_cash`：现金和银行存款
  - `asset_current`：流动资产
  - `asset_fixed`：固定资产
  
- **负债类**（Liability）：
  - `liability_payable`：应付账款
  - `liability_current`：流动负债
  - `liability_non_current`：非流动负债
  
- **权益类**（Equity）：
  - `equity`：股本
  - `equity_unaffected`：未分配利润
  
- **收入类**（Income）：
  - `income`：主营业务收入
  - `income_other`：其他收入
  
- **费用类**（Expense）：
  - `expense`：费用
  - `expense_depreciation`：折旧费用
  - `expense_direct_cost`：销售成本

### 2. 日记账分录（Journal Entries）

日记账分录是记录所有财务交易的基本方式。

#### 日记账模型

```
class AccountMove(models.Model):
    _name = 'account.move'
    _description = 'Account Entry'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Number', required=True, copy=False)
    ref = fields.Char('Reference', copy=False)
    date = fields.Date('Date', required=True)
    journal_id = fields.Many2one('account.journal', 'Journal', required=True)
    line_ids = fields.One2many('account.move.line', 'move_id', 'Journal Items')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft')
    amount_total = fields.Monetary('Total', compute='_compute_amounts')
```

#### 日记账行模型

```
class AccountMoveLine(models.Model):
    _name = 'account.move.line'
    _description = 'Journal Item'
    
    move_id = fields.Many2one('account.move', 'Journal Entry')
    account_id = fields.Many2one('account.account', 'Account', required=True)
    debit = fields.Monetary('Debit', default=0.0)
    credit = fields.Monetary('Credit', default=0.0)
    balance = fields.Monetary('Balance', compute='_compute_balance')
    partner_id = fields.Many2one('res.partner', 'Partner')
    name = fields.Char('Label', required=True)
    date = fields.Date('Date', required=True)
    reconciled = fields.Boolean('Reconciled')
    full_reconcile_id = fields.Many2one('account.full.reconcile', 'Matching Number')
```

#### 借贷平衡验证

系统自动验证每笔日记账分录的借贷平衡：

```
@api.constrains('line_ids')
def _check_balanced(self):
    for move in self:
        if move.line_ids:
            total_debit = sum(line.debit for line in move.line_ids)
            total_credit = sum(line.credit for line in move.line_ids)
            if abs(total_debit - total_credit) > move.company_id.currency_id.rounding:
                raise ValidationError(_('Journal entry is not balanced!'))
```

### 3. 日记账（Journals）

日记账是用于组织日记账分录的容器。

#### 日记账类型

- **销售日记账**：记录销售相关交易
- **采购日记账**：记录采购相关交易
- **银行日记账**：记录银行交易
- **现金日记账**：记录现金交易
- **其他日记账**：杂项日记账

#### 日记账模型

```
class AccountJournal(models.Model):
    _name = 'account.journal'
    _description = 'Journal'
    
    name = fields.Char('Journal Name', required=True)
    code = fields.Char('Short Code', required=True)
    type = fields.Selection([
        ('sale', 'Sale'),
        ('purchase', 'Purchase'),
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('general', 'Miscellaneous'),
    ], string='Type', required=True)
    currency_id = fields.Many2one('res.currency', 'Currency')
    company_id = fields.Many2one('res.company', 'Company', required=True)
    default_account_id = fields.Many2one('account.account', 'Default Account')
```

### 4. 发票管理（Invoices）

发票管理是会计模块的核心功能之一。

#### 发票类型

- **客户发票**（Customer Invoice）：向客户开具的发票
- **供应商账单**（Vendor Bill）：供应商开具的账单
- **信用备忘录**（Credit Note）：退货或退款凭证
- **退款**（Refund）：退款处理

#### 发票模型扩展

发票实际上是 `account.move` 的特殊类型：

```
# 发票是 account.move 的特殊视图
# 通过 move_type 字段区分：
# - 'out_invoice': 客户发票
# - 'in_invoice': 供应商账单
# - 'out_refund': 客户退款
# - 'in_refund': 供应商退款

class AccountMove(models.Model):
    _name = 'account.move'
    
    move_type = fields.Selection([
        ('entry', 'Journal Entry'),
        ('out_invoice', 'Customer Invoice'),
        ('out_refund', 'Customer Credit Note'),
        ('in_invoice', 'Vendor Bill'),
        ('in_refund', 'Vendor Credit Note'),
        ('out_receipt', 'Sales Receipt'),
        ('in_receipt', 'Purchase Receipt'),
    ], string='Type', required=True, default='entry')
    
    invoice_date = fields.Date('Invoice/Bill Date')
    invoice_date_due = fields.Date('Due Date')
    invoice_payment_term_id = fields.Many2one('account.payment.term', 'Payment Terms')
    invoice_partner_display_name = fields.Char('Partner Name')
    invoice_line_ids = fields.One2many('account.move.line', 'move_id', 
                                      domain=[('display_type', '!=', 'line_section')])
```

#### 发票状态

- **草稿**（Draft）：未确认的发票
- **已过账**（Posted）：已确认并过账的发票
- **已对账**（Paid）：已完全付款的发票
- **已取消**（Cancelled）：已取消的发票

### 5. 付款管理（Payments）

管理客户和供应商的付款。

#### 付款模型

```
class AccountPayment(models.Model):
    _name = 'account.payment'
    _description = 'Payment'
    
    name = fields.Char('Memo')
    payment_type = fields.Selection([
        ('outbound', 'Send Money'),
        ('inbound', 'Receive Money'),
    ], string='Payment Type', required=True)
    partner_type = fields.Selection([
        ('customer', 'Customer'),
        ('supplier', 'Vendor'),
    ], string='Partner Type', required=True)
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    amount = fields.Monetary('Amount', required=True)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True)
    payment_date = fields.Date('Payment Date', required=True)
    journal_id = fields.Many2one('account.journal', 'Payment Journal', required=True)
    invoice_ids = fields.Many2many('account.move', string='Invoices')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Validated'),
        ('sent', 'Posted'),
        ('reconciled', 'Reconciled'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')
```

### 6. 对账功能（Reconciliation）

自动或手动匹配付款和发票。

#### 对账模型

```
class AccountFullReconcile(models.Model):
    _name = 'account.full.reconcile'
    _description = 'Full Reconcile'
    
    name = fields.Char('Number', required=True, copy=False, default=lambda self: _('New'))
    reconciled_line_ids = fields.One2many('account.move.line', 'full_reconcile_id', 
                                          'Matched Journal Items')
    partial_reconcile_ids = fields.One2many('account.partial.reconcile', 'full_reconcile_id', 
                                           'Partial Reconcile')
```

### 7. 财务报表（Financial Reports）

提供标准的财务报表。

#### 报表类型

- **总账报表**（General Ledger）：所有科目的详细交易记录
- **试算平衡表**（Trial Balance）：科目余额汇总
- **科目余额表**（Account Balance）：各科目余额
- **利润表**（P&L Statement）：收入费用报表（需 `account_reports`）
- **资产负债表**（Balance Sheet）：资产负债报表（需 `account_reports`）

---

## 三、核心模型详解

### 1. `account.account` - 会计科目

存储会计科目信息。

**主要字段**：
- `name`：科目名称
- `code`：科目编码
- `account_type`：科目类型
- `reconcile`：是否允许对账
- `company_id`：所属公司
- `currency_id`：币种

**使用示例**：

```python
# 创建现金科目
cash_account = self.env['account.account'].create({
    'name': 'Cash',
    'code': '1010',
    'account_type': 'asset_cash',
    'reconcile': True,
    'company_id': self.env.company.id,
})

# 创建应收账款科目
receivable_account = self.env['account.account'].create({
    'name': 'Accounts Receivable',
    'code': '1200',
    'account_type': 'asset_receivable',
    'reconcile': True,
    'company_id': self.env.company.id,
})
```

### 2. `account.move` - 日记账分录

财务交易的主记录。

**主要字段**：
- `name`：分录编号
- `date`：交易日期
- `journal_id`：日记账
- `line_ids`：分录行
- `state`：状态（草稿/已过账/已取消）

**使用示例**：

```python
# 创建日记账分录
move = self.env['account.move'].create({
    'journal_id': journal.id,
    'date': fields.Date.today(),
    'line_ids': [
        (0, 0, {
            'account_id': cash_account.id,
            'debit': 1000.0,
            'credit': 0.0,
            'name': 'Cash received',
        }),
        (0, 0, {
            'account_id': revenue_account.id,
            'debit': 0.0,
            'credit': 1000.0,
            'name': 'Revenue',
        }),
    ],
})

# 过账
move.action_post()
```

### 3. `account.move.line` - 日记账行

日记账分录的每一行。

**主要字段**：
- `move_id`：所属分录
- `account_id`：科目
- `debit`：借方金额
- `credit`：贷方金额
- `partner_id`：合作伙伴
- `reconciled`：是否已对账

---

## 四、与其他模块的集成

### 1. 与 `sale` 模块

**自动创建客户发票**：

- 销售订单确认后，可自动创建客户发票
- 发票行自动从订单行复制
- 发票状态与订单状态同步

**工作流程**：

```
销售订单确认
 ↓
创建客户发票（account.move，move_type='out_invoice'）
 ↓
发票自动关联订单
 ↓
发票过账后，计入应收账款
 ↓
客户付款后，对账完成
```

**代码示例**：

```python
# 从销售订单创建发票
sale_order = self.env['sale.order'].browse(order_id)
invoice = sale_order._create_invoices()
invoice.action_post()
```

### 2. 与 `purchase` 模块

**自动创建供应商账单**：

- 采购订单确认后，可创建供应商账单
- 账单自动关联采购订单
- 支持三向匹配（订单、收货、发票）

**工作流程**：

```
采购订单确认并收货
 ↓
创建供应商账单（account.move，move_type='in_invoice'）
 ↓
账单自动关联采购订单
 ↓
账单过账后，计入应付账款
 ↓
付款后，对账完成
```

### 3. 与 `stock` 模块（需 `stock_account`）

**库存价值记账**：

- 库存移动自动生成会计凭证
- 收货时借记库存科目，贷记暂估科目
- 发货时贷记库存科目，借记成本科目

**工作流程**：

```
库存收货
 ↓
创建会计凭证
  借记：库存科目
  贷记：暂估应付科目
 ↓
供应商发票到达
 ↓
调整暂估应付，计入应付账款
```

### 4. 与 `hr` 模块

**员工成本核算**：

- 员工成本计入相应费用科目
- 薪资生成会计凭证

---

## 五、财务工作流程

### 1. 客户发票流程

```
1. 销售订单确认
   ↓
2. 创建客户发票
   ↓
3. 审核发票（可选）
   ↓
4. 过账发票
   ↓
5. 发送发票给客户
   ↓
6. 客户付款
   ↓
7. 登记付款
   ↓
8. 对账（匹配付款和发票）
   ↓
9. 完成收款
```

### 2. 供应商账单流程

```
1. 采购订单和收货
   ↓
2. 接收供应商发票
   ↓
3. 创建供应商账单
   ↓
4. 审核账单（三向匹配）
   ↓
5. 过账账单
   ↓
6. 付款审批
   ↓
7. 登记付款
   ↓
8. 对账（匹配付款和账单）
   ↓
9. 完成付款
```

### 3. 日记账分录流程

```
1. 创建日记账分录
   ↓
2. 添加分录行（确保借贷平衡）
   ↓
3. 审核分录
   ↓
4. 过账分录
   ↓
5. 分录不可修改（除非撤销过账）
```

---

## 六、配置和设置

### 1. 初始化会计科目表

#### 步骤 1：选择会计科目表模板

1. 进入 **会计 > 配置 > 会计科目表**
2. 选择本地化的会计科目表（如 `l10n_cn` 中国科目表）
3. 或使用通用科目表（`l10n_generic_coa`）

#### 步骤 2：配置公司信息

1. **会计 > 配置 > 设置**
2. 设置公司信息
3. 配置默认币种
4. 设置会计年度

#### 步骤 3：配置日记账

1. **会计 > 配置 > 日记账**
2. 创建必要的日记账：
   - 销售日记账
   - 采购日记账
   - 银行日记账
   - 现金日记账
   - 其他日记账

### 2. 配置科目

#### 设置对账科目

对于应收和应付科目，需要启用对账功能：

```
科目配置：
- reconcile = True
- 允许自动对账
```

#### 配置默认科目

在各日记账中设置默认科目：

- 银行日记账：默认科目为银行账户
- 现金日记账：默认科目为现金账户
- 销售日记账：默认科目为应收账款
- 采购日记账：默认科目为应付账款

### 3. 配置付款条件

**会计 > 配置 > 付款条件**

创建付款条件模板：
- 立即付款（0 天）
- 30 天付款
- 2/10, net 30（10 天内付款 2% 折扣）

### 4. 配置税收

**会计 > 配置 > 税收**

设置税率和税务规则：
- 增值税（VAT）
- 销售税
- 采购税

---

## 七、典型使用场景

### 场景 1：处理客户发票

**需求**：销售完成后，向客户开具发票并收款

**步骤**：

1. **创建发票**
   - 从销售订单创建，或手动创建
   - 输入发票信息（日期、付款条件等）
   - 添加发票行（产品、数量、价格）

2. **审核发票**
   - 检查发票信息是否正确
   - 验证税额计算

3. **过账发票**
   - 过账后，发票计入应收账款
   - 生成会计凭证

4. **发送发票**
   - 通过邮件发送发票 PDF 给客户
   - 或打印发票邮寄

5. **收款处理**
   - 客户付款后，登记付款
   - 匹配付款和发票
   - 完成对账

### 场景 2：处理供应商账单

**需求**：收到供应商发票后，进行审核和付款

**步骤**：

1. **接收发票**
   - 供应商发送发票（纸质或电子）

2. **创建供应商账单**
   - 手动输入，或从邮件附件导入
   - 关联采购订单（如有）

3. **三向匹配**
   - 订单：采购订单信息
   - 收货：实际收货数量
   - 发票：发票金额和数量
   - 确保三者一致

4. **审核账单**
   - 检查金额、税额、付款条件

5. **过账账单**
   - 过账后，计入应付账款

6. **付款审批**
   - 审批付款申请
   - 生成付款单

7. **付款处理**
   - 执行付款（银行转账、支票等）
   - 登记付款
   - 对账完成

### 场景 3：月度结账

**需求**：每月末进行财务结账

**步骤**：

1. **检查所有交易**
   - 确保所有发票都已过账
   - 确保所有付款都已登记

2. **对账检查**
   - 银行对账
   - 应收应付对账

3. **调整分录**
   - 如需要，创建调整分录
   - 折旧、预提等

4. **生成财务报表**
   - 利润表
   - 资产负债表
   - 试算平衡表

5. **审核报表**
   - 检查报表准确性
   - 分析异常项目

---

## 八、最佳实践

### 1. 科目表设计

- **遵循会计准则**：使用符合当地会计准则的科目表
- **层级清晰**：合理的科目层级，便于报表生成
- **命名规范**：科目名称和编码规范统一

### 2. 日记账管理

- **按业务类型分类**：不同类型的业务使用不同的日记账
- **定期审核**：定期审核日记账分录
- **权限控制**：限制日记账的修改权限

### 3. 发票管理

- **及时开具**：销售完成后及时开具发票
- **准确记录**：确保发票信息准确完整
- **及时收款**：跟踪应收账款，及时收款

### 4. 对账管理

- **定期对账**：定期进行银行和往来账对账
- **及时处理差异**：发现差异及时处理
- **保留对账记录**：保留对账历史记录

### 5. 报表分析

- **定期生成报表**：定期生成和审核财务报表
- **分析异常**：分析报表中的异常项目
- **趋势分析**：进行财务趋势分析

---

## 九、常见问题和解决方案

### 问题 1：日记账不平衡

**症状**：创建日记账分录时提示"借贷不平衡"

**原因**：
- 借方和贷方金额不相等
- 币种不一致

**解决方案**：
1. 检查所有行的借贷金额
2. 确保总额：总借方 = 总贷方
3. 检查币种是否一致

### 问题 2：无法对账

**症状**：无法匹配付款和发票

**原因**：
- 科目未启用对账功能
- 金额不匹配
- 币种不一致

**解决方案**：
1. 检查科目设置：`reconcile = True`
2. 检查金额是否匹配
3. 检查币种是否一致

### 问题 3：发票状态异常

**症状**：发票状态不正确，无法操作

**原因**：
- 发票已过账但需要修改
- 发票状态流转异常

**解决方案**：
1. 撤销过账（需要权限）
2. 修改发票
3. 重新过账

---

## 十、高级功能

### 1. 多货币支持

- 支持多币种交易
- 自动汇率转换
- 汇率差异处理

### 2. 多公司支持

- 多公司会计独立
- 公司间交易处理
- 合并报表（需额外模块）

### 3. 会计年度管理

- 定义会计年度
- 期间管理
- 年度结账

### 4. 财务分析

- 科目分析维度
- 自定义分析字段
- 财务报表钻取

---

## 十一、总结

- **`account` 模块**是 Odoo 财务会计系统的核心。
- 核心功能：
  - 会计科目表和科目管理
  - 日记账分录和过账
  - 发票和账单管理
  - 付款和对账
  - 财务报表生成
  - 与销售、采购、库存等模块的深度集成
- 支持完整的财务会计业务流程。
- 提供灵活的科目结构和报表功能。
- 是构建企业财务管理系统的基础模块。
- 适合各种规模和类型的企业使用。

