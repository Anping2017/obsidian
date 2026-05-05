# 💰 Odoo `stock_account` 模块详解

## 一、`stock_account` 模块的作用

- **库存与会计集成模块**，将 `stock` 的库存估价与 `account` 的会计凭证打通。
- 支持永续盘存（Perpetual）与周期盘存（Periodic，较少使用）两种会计模式中的永续估价。
- 在收货、发货、内部生产等业务节点自动生成会计分录，确保库存价值在财务报表中准确反映。

---

## 二、核心概念与对象

### 1. 库存估价模式（Product Category）

- 估价方法（Costing Method）：
  - FIFO（先进先出）
  - AVCO（加权平均）
  - Standard（标准成本）
- 估价类型（Inventory Valuation）：
  - Manual（手动估价，无自动分录）
  - Automated（自动估价，自动分录）

在 `产品类别` 上配置以上选项，系统按类别继承到产品，控制成本计算与是否自动过账。

### 2. 核心技术模型（只列常用字段）

```python
# 库存估价层，记录每次估价变化（成本层）
class StockValuationLayer(models.Model):
    _name = 'stock.valuation.layer'
    product_id = fields.Many2one('product.product', required=True)
    quantity = fields.Float(required=True)
    unit_cost = fields.Float(required=True)
    value = fields.Float(required=True)           # 本次估价金额（含符号）
    remaining_qty = fields.Float()                # FIFO/AVCO余量
    stock_move_id = fields.Many2one('stock.move')
    company_id = fields.Many2one('res.company', required=True)
    description = fields.Char()

# 估价切换与自动过账依赖产品类别
class ProductCategory(models.Model):
    _inherit = 'product.category'
    property_cost_method = fields.Selection([('standard','Standard'),('fifo','FIFO'),('average','Average Price')])
    property_valuation = fields.Selection([('manual_periodic','Manual'),('real_time','Automated')])
    property_stock_valuation_account_id = fields.Many2one('account.account')   # 库存资产
    property_stock_account_input_categ_id = fields.Many2one('account.account') # 收货临时/入库
    property_stock_account_output_categ_id = fields.Many2one('account.account')# 出库/销售成本
```

---

## 三、自动会计处理（典型分录）

以下示例以“自动估价（Automated）”为前提，具体科目以类别或产品上的配置为准。

### 1. 采购收货（入库到可用库存）

- 借：库存资产（Inventory Asset）
- 贷：入库暂估/收货清算（Stock Input/GRNI）

发票过账后：
- 借：入库暂估/收货清算
- 贷：应付账款（AP）

注：使用三方匹配时，数量与价格差异通过价格差异科目或发票价差在后续体现。

### 2. 客户发货（从库存发出）

- 借：销售成本（COGS）
- 贷：库存资产（Inventory Asset）

收入确认由 `account`/`sale` 通过发票实现，成本与收入配比。

### 3. 库存调整（盘盈盘亏）

- 盘盈：借 库存资产 / 贷 库存调整差异
- 盘亏：借 库存调整差异 / 贷 库存资产

### 4. 生产领料与完工

- 原料消耗：借 在制品/生产消耗（或COGS-生产）/ 贷 库存资产
- 成品入库：借 库存资产 / 贷 在制品/生产完工

（具体科目取决于企业科目结构与 `mrp` 集成配置）

---

## 四、成本计算方法要点

### 1. FIFO
- 出库按最早的估价层逐层结转，`stock.valuation.layer` 的 `remaining_qty` 驱动层结转。
- 成本波动真实反映到不同批次的出库成本。

### 2. 加权平均（AVCO）
- 每次入库更新移动平均成本，出库按当前平均成本结转。
- 数据稳定、易理解，但跨期大额入库会影响当期出库成本。

### 3. 标准成本（Standard）
- 出库按标准单价结转；采购价与标准价差额记入“价格差异科目”，便于差异分析。

---

## 五、配置步骤（实操）

1. 科目准备（会计 > 配置 > 科目）
   - 创建/确认：库存资产、入库暂估、出库成本、价格差异等科目。
2. 产品类别（库存 > 配置 > 产品类别）
   - 估价方法：FIFO/平均/标准
   - 估价类型：Automated（自动估价）
   - 绑定科目：资产/入库/出库/差异
3. 产品主数据（库存 > 产品）
   - 如需特例，可在产品上覆盖类别的会计科目配置。
4. 多公司场景
   - 各公司独立配置类别科目与估价方法，避免交叉。

---

## 六、数据追溯与对账

- 估价层（`stock.valuation.layer`）：定位任意一次成本变化的来源（收货、发货、调整）。
- 库存卡片：按产品查看数量与金额变化明细。
- 会计分录：通过 `stock.move` 链接到对应 `account.move` 进行账实核对。

---

## 七、常见问题与排查

- 出库负库存导致成本异常：启用/规范负库存策略，避免负库存下的估价层欠账。
- 科目配置不完整导致分录失败：检查类别/产品上的资产、入库、出库科目是否齐全。
- 标准成本未更新：变更标准价需配套差异分析与期初重估。
- 跨期价格波动：平均成本与FIFO的差异理解与报告口径统一。

---

## 八、总结

- `stock_account` 提供自动估价与会计分录能力，借助估价层实现可追溯的成本核算。
- 通过产品类别的估价方法与科目绑定，驱动收发存自动入账。
- 配合 `purchase`、`sale`、`mrp`、`account` 实现端到端的数量-金额一致性与财务对账。

