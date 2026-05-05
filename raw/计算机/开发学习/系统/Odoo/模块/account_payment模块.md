# 💳 Odoo `account_payment` 模块详解

## 一、`account_payment` 模块的作用

- **付款管理模块**，扩展 `account` 模块的付款功能。
- 管理客户收款和供应商付款的完整流程。
- 提供银行对账功能，确保财务数据准确性。
- 支持多种付款方式：现金、银行转账、支票、信用卡等。
- 实现付款与发票的自动匹配和对账。

📌 形象理解：  
👉 `account_payment` 模块是"出纳系统"，处理所有现金和银行收付款业务。

---

## 二、核心功能

### 1. 付款登记

#### 付款类型

- **客户付款**（Inbound Payment）：
  - 接收客户的付款
  - 匹配客户发票
  - 核销应收账款

- **供应商付款**（Outbound Payment）：
  - 向供应商付款
  - 匹配供应商账单
  - 核销应付账款

#### 付款模型

```
class AccountPayment(models.Model):
    _name = 'account.payment'
    _description = 'Payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    behalf_partner_id = fields.Many2one('res.partner', string='On Behalf Of')
    payment_type = fields.Selection([
        ('outbound', 'Send Money'),
        ('inbound', 'Receive Money'),
    ], string='Payment Type', required=True)
    
    partner_type = fields.Selection([
        ('customer', 'Customer'),
        ('supplier', 'Vendor'),
    ], string='Partner Type', required=True)
    
    payment_method_line_id = fields.Many2one('account.payment.method.line', 
                                             string='Payment Method',
                                             required=True,
                                             domain="[('payment_type', '=', payment_type)]")
    
    partner_id = fields.Many2one('res.partner', string Wakti='Partner', required=True)
    amount = fields.Monetary('Amount', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    payment_date = fields.Date('Payment Date', required=True)
    
    journal_id = fields.Many2one('account.journal', string='Payment Journal', 
                                required=True,
                                domain="[('type', 'in', ('bank', 'cash'))]")
    
    bank_reference = fields.Char('Bank Reference')
    cheque_reference = fields.Char('Cheque Reference')
    effective_date = fields.Date('Effective Date')
    
    payment_method_id = fields.Many2one(related='payment_method_line_id.payment_method_id',
                                       string='Payment Method Type')
    payment_type = fields.Selection(related='payment_method_line_id.payment_type')
    
    invoice_ids = fields.Many2many('account.move', string='Invoices/Bills',
                                  domain="[('move_type', 'in', _get_valid_invoice_types())]")
    
    line_ids = fields.One2many('account.payment.line', 'payment_id', string='Payment Lines')
    
    state navigate= fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Validated'),
        ('sent', 'Posted'),
        ('reconciled', 'Reconciled'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')
    
    is_reconciled = fields.Boolean('Is Reconciled', compute='_compute_is_reconciled')
    is_matched = fields.Boolean('Is Matched', compute='_compute_is_matched')
```

#### 付款状态

- **草稿**（Draft）：新创建的付款
- **已过账**（Posted）：付款已过账
- **已发送**（Sent）：付款已发送
- **已对账**（Reconciled）：付款已完全对账
- **已取消**（Cancelled）：付款已取消

### 2. 银行对账

#### 对账功能

银行对账是确保银行账户余额与会计系统一致的重要功能。

#### 银行对账模型

```
class AccountBankStatement(models.Model):
    _name = 'account.bank.statement'
    _description = 'Bank Statement'
    
    name = fields.Char('Statement Name', required=True)
    date = fields.Date('Date', required=True)
    balance_start = fields.Monetary('Starting Balance', required=True)
    balance_end = fields.Monetary('Ending Balance', required=True)
    balance_end_real = fields.Monetary('Computed Ending Balance')
    line_ids = fields.One2many('account.bank.statement.line', 'statement_id', 
                               'Statement Lines')
    journal_id = fields.Many2one('account.journal', 'Journal', required=True)
    state = fields.Selection([
        ('open', 'New'),
        ('posted', 'Posted'),
        ('confirm', 'Validated')
    ], string='Status', default='open')
```

#### 对账流程

```
1. 导入银行对账单（或手动录入）
   ↓
2. 导入银行交易明细
   ↓
3. 自动匹配付款和收款
   ↓
4. 手动匹配未匹配的项目
   ↓
5. 核对余额
   ↓
6. 确认对账
```

#### 对账匹配规则

- **金额匹配**：相同金额自动匹配
- **参考号匹配**：通过参考号匹配
- **日期匹配**：在合理日期范围内匹配
- **手动匹配**：人工识别和匹配

### 3. 付款方式管理

#### 付款方式类型

- **现金**（Cash）：现金付款
- **银行转账**（Bank Transfer）：银行转账
- **支票**（Check）：支票付款
- **信用卡**（Credit Card）：信用卡付款
- **其他**：其他付款方式

#### 付款方式配置

1. **会计 > 配置 > 付款方式**
2. 创建付款方式：
   - **名称**：付款方式名称
   - **类型**：付款方式类型
   - **日记账**：关联的银行或现金日记账
   - **付款方法**：付款处理方式

### 4. 付款匹配发票

#### 自动匹配

- **金额匹配**：付款金额与发票金额匹配
- **自动对账**：系统自动对账
- **部分付款**：支持部分付款对账

#### 手动匹配

- **选择发票**：手动选择要匹配的发票
- **分配金额**：手动分配付款金额到发票
- **多发票匹配**：一个付款匹配多个发票

#### 匹配界面

- **付款匹配视图**：专门的匹配界面
- **发票列表**：显示待匹配的发票
- **匹配金额**：显示匹配金额
- **匹配状态**：显示匹配状态

---

## 三、核心模型详解

### 1. `account.payment` - 付款

**主要字段**：
- `payment_type`：付款类型（收款/付款）
- `partner_type`：合作伙伴类型（客户/供应商）
- `partner_id`：合作伙伴
- `amount`：付款金额
- `payment_date`：付款日期
- `journal_id`：付款日记账（银行/现金）
- `invoice_ids`：关联的发票/账单
- `state`：付款状态

**使用示例**：

```python
# 创建客户付款
payment = self.env['account.payment'].create({
    'payment_type': 'inbound',
    'partner_type': 'customer',
    'partner_id': customer.id,
    'amount': 1000.0,
    'payment_date': fields.Date.today(),
    'journal_id': bank_journal.id,
    'invoice_ids': [(6, 0, [invoice.id])],
})

# 过账付款
payment.action_post()
```

### 2. `account.bank.statement` - 银行对账单

**主要字段**：
- `name`：对账单名称
- `date`：对账日期
- `balance_start`：期初余额
- `balance_end`：期末余额
- `line_ids`：对账单明细行
- `journal_id`：银行日记账

### 3. `account.bank.statement.line` - 银行对账单行

**主要字段**：
- `statement_id`：所属对账单
- `date`：交易日期
- `payment_ref`：付款参考
- `amount`：金额
- `partner_id`：合作伙伴
- `reconciled`：是否已对账

---

## 四、付款工作流程

### 1. 客户收款流程

```
1. 客户付款
   ↓
2. 创建收款记录
   - 选择客户
   - 输入收款金额
   - 选择付款方式
   ↓
3. 匹配发票
   - 选择要匹配的发票
   - 自动或手动匹配
   ↓
4. 过账付款
   - 审核付款信息
   - 过账付款
   ↓
5. 对账完成
   - 付款与发票对账
   - 核销应收账款
```

### 2. 供应商付款流程

```
1. 收到供应商发票
   ↓
2. 审批付款
   - 审核发票
   - 审批付款申请
   ↓
3. 创建付款记录
   - 选择供应商
   - 输入付款金额
   - 选择付款方式
   ↓
4. 匹配账单
   - 关联供应商账单
   - 确认金额
   ↓
5. 执行付款
   - 银行转账/支票等
   - 确认付款执行
   ↓
6. 过账付款
   - 过账付款 }}</text>
   ↓
7. 对账完成
   - 付款与账单对账
   - 核销应付账款
```

### 3. 银行对账流程

```
1. 获取银行对账单
   - 从银行下载或导入
   - 或手动录入
   ↓
2. 创建银行对账单
   - 输入对账日期
   - 输入期初和期末余额
   - 导入银行交易明细
   ↓
3. 自动匹配
   - 系统自动匹配已知交易
   - 识别已登记的付款和收款
   ↓
4. 手动匹配
   - 手动匹配未匹配的交易
   - 识别未知交易
   ↓
5. 创建调整项
   - 银行手续费
   - 利息收入/支出
   - 其他调整
   ↓
6. 核对余额
   - 检查系统余额与银行余额
   - 处理差异
   ↓
7. 确认对账
   - 确认对账单
   - 生成对账报告
```

---

## 五、与其他模块的集成

### 1. 与 `account` 模块

- **付款记录**：付款创建会计凭证
- **对账功能**：付款与发票对账
- **科目更新**：更新银行和应收应付科目余额

### 2. 与 `sale` 模块

- **客户收款**：销售订单的收款处理
- **发票匹配**：客户付款匹配客户发票

### 3. 与 `purchase` 模块

- **供应商付款**：采购订单的付款处理
- **账单匹配**：供应商付款匹配供应商账单

### 4. 与 `account_reports` 模块

- **现金流报表**：付款数据用于现金流报表
- **应收应付报表**：对账情况反映在报表中

---

## 六、典型使用场景

### 场景 1：客户收款

**需求**：处理客户付款并匹配发票

**步骤**：

1. **创建收款**
   ```
   会计 > 付款 > 客户付款
   - 选择客户
   - 输入收款金额
   - 选择付款方式（如银行转账）
   - 输入收款日期
   ```

2. **匹配发票**
   ```
   - 选择要匹配的发票
   - 系统自动计算匹配金额
   - 确认匹配
   ```

3. **过账收款**
   ```
   - 审核收款信息
   - 点击"过账"
   - ! 系统创建会计凭证
   - 核销应收账款
   ```

### 场景 2：供应商付款

**需求**：向供应商付款

**步骤**：

1. **审批付款**
   - 审核供应商账单
   - 审批付款申请

2. **创建付款**
   ```
   会计 > 付款 > 供应商付款
   - 选择供应商
   - 输入付款金额
   - 选择付款方式
   - 关联供应商账单
   ```

3. **执行付款**
   - 执行实际付款（银行转账等）
 Min  - 确认付款执行

4. **过账付款**
   - 过账付款记录
   - 核销应付账款

### 场景 3：银行对账

**需求**：每月进行银行对账

**步骤**：

1. **获取对账单**
   - 从银行获取对账单（PDF/Excel）
   - 或登录网银下载

2. **创建对账单**
   ```
   会计 > 银行对账 > 银行对账单 > 新建
   - 选择银行账户
   - 输入对账日期
   - 输入期初余额
   - 导入银行交易明细
   ```

3. **自动匹配**
   - 系统自动匹配已知交易
   - 检查匹配结果

4. **手动匹配**
   - 手动匹配未匹配的交易
   - 创建新的付款/收款记录（如需要）

5. **核对余额**
   ```
   系统余额 = 期初余额 + 收款 - 付款 + 调整
   银行余额 = 对账单期末余额
   - 检查两者是否一致
   - 处理差异
   ```

6. **确认对账**
   - 确认对账单
   - 生成对账报告

---

## 七、配置和设置

### 1. 付款方式配置

#### 创建付款方式

1. **会计 > 配置 > 付款方式**
2. 创建付款方式：
   - **名称**：如"银行转账"、"现金"
   - **类型**：付款方式类型
   - **日记账**：关联的银行或现金日记账

#### 付款方法配置

1. **会计 > 配置 > 付款方法**
2. 配置付款方法：
   - **手动付款**：手动处理付款
   - **批量付款**：批量处理付款
   - **银行集成**：与银行系统集成（如支持）

### 2. 银行账户配置

1. **会计 > 配置 > 银行账户**
2. 创建银行账户：
   - **账户名称**：银行账户名称
   - **账户号码**：银行账号
   - **银行**：所属银行
   - **日记账**：关联的银行日记账

### 3. 对账配置

1. **会计 > 配置 > 设置**
2. 配置对账选项：
   - **自动匹配规则**：配置自动匹配规则
   - **对账提醒**：设置对账提醒
   - **对账期间**：设置对账频率

---

## 八、最佳实践

### 1. 付款管理

- **及时登记**：收到或支付款项后及时登记
- **准确匹配**：确保付款与发票准确匹配
- **定期对账**：定期进行银行对账
- **保留凭证**：保留付款凭证

### 2. 银行对账

- **定期对账**：每月定期进行银行对账
- **及时处理差异**：发现差异及时处理
- **保留对账记录**：保留对账历史记录
- **对账报告**：生成对账报告备案

### 3. 付款安全

- **权限控制**：限制付款权限
- **审批流程**：重要付款需要审批
- **双重验证**：关键付款双重验证
- **审计跟踪**：保留完整的审计跟踪

---

## 九、常见问题

### 问题 1：无法匹配付款

**原因**：
- 发票金额与付款金额不匹配
- 币种不一致
- 发票已完全付款

**解决方案**：
1. 检查金额是否匹配
2. 检查币种是否一致
3. 检查发票付款状态

### 问题 2：银行对账不平衡

**原因**：
- 有未匹配的交易
- 有未记录的付款/收款
- 系统错误

**解决方案**：
1. 检查所有未匹配的交易
2. 补录缺失的交易
3. 检查系统配置

---

## 十、总结

- **`account_payment` 模块**提供完整的付款管理功能。
- 核心功能：
  - 客户收款和供应商付款
  - 银行对账
  - 付款方式管理
  - 付款与发票匹配
  - 付款报表
- 确保财务数据的准确性和完整性。
- 简化付款流程，提高财务工作效率。

