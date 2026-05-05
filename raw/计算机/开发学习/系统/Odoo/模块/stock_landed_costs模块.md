# 🚢 Odoo `stock_landed_costs` 模块详解

## 一、`stock_landed_costs` 模块的作用

- 管理采购相关的额外成本（运费、关税、保险、装卸费等），并将其合理分摊到收货产品上。
- 调整产品实际成本（FIFO/AVCO/Standard 下的处理不同），更新库存估价与会计分录。
- 与 `stock_account`、`purchase` 深度集成，保证全面成本核算。

---

## 二、核心模型与字段

```python
# 到岸成本单
class StockLandedCost(models.Model):
    _name = 'stock.landed.cost'
    picking_ids = fields.Many2many('stock.picking', string='Pickings')
    cost_lines = fields.One2many('stock.landed.cost.lines', 'cost_id', string='Cost Lines')
    valuation_adjustment_lines = fields.One2many('stock.landed.cost.valuation.adjustment.lines', 'cost_id')
    account_move_id = fields.Many2one('account.move', string='Journal Entry')
    state = fields.Selection([('draft','Draft'),('done','Posted'),('cancel','Cancelled')], default='draft')
    journal_id = fields.Many2one('account.journal', required=True)

# 成本行（费用项）
class StockLandedCostLines(models.Model):
    _name = 'stock.landed.cost.lines'
    cost_id = fields.Many2one('stock.landed.cost', required=True)
    name = fields.Char(required=True)
    product_id = fields.Many2one('product.product')         # 费用商品，可带税
    split_method = fields.Selection([
        ('quantity','By Quantity'),
        ('weight','By Weight'),
        ('volume','By Volume'),
        ('equal','Equal'),
        ('current_cost_price','By Current Cost (Value)')
    ], default='quantity', required=True)
    price_unit = fields.Float('Cost')

# 分摊结果（到每个移库行/产品）
class StockLandedCostValuationAdjustmentLines(models.Model):
    _name = 'stock.landed.cost.valuation.adjustment.lines'
    cost_id = fields.Many2one('stock.landed.cost', required=True)
    move_id = fields.Many2one('stock.move', required=True)
    quantity = fields.Float()
    former_cost = fields.Float()     # 原成本
    additional_landed_cost = fields.Float() # 分摊的新增成本
    final_cost = fields.Float()      # 调整后的成本
```

---

## 三、分摊方法与适用场景

- 按数量（quantity）：数量主导、规格一致、单价相近的产品。
- 按重量（weight）：物流费与重量强相关的场景。
- 按体积（volume）：体积型货物的运费/仓储成本分摊。
- 平均分（equal）：费用均摊，不同产品价值差异小。
- 按当前成本（current_cost_price/价值）：价值驱动，适用于关税/保险等与货值相关的费用。

---

## 四、业务流程（标准）

```
1) 采购收货（创建收货单）
   ↓
2) 创建到岸成本单（选择收货单）
   - 添加成本行：运费、关税、保险…
   - 选择分摊方法
   ↓
3) 计算（Compute）
   - 生成分摊明细（valuation_adjustment_lines）
   - 预览每个产品的分摊额
   ↓
4) 过账（Validate/Confirm）
   - 更新库存估价层（SVL）
   - 自动生成会计凭证（由 journal_id 决定）
```

---

## 五、会计影响（示例）

以“自动估价 + FIFO/AVCO”为例（具体科目取决于类别/产品配置）：

- 过账到岸成本时：
  - 借：库存资产（Inventory Asset） 增加分摊额
  - 贷：运费/关税/其他费用科目（或应付账款/预提）

如果费用来自供应商账单（Bills），也可通过发票入账，再由到岸成本进行分摊与二次转分类（取决于流程设计）。

---

## 六、与成本方法的关系

- FIFO：新生成的估价层追加到对应批次，影响后续出库成本。已出库的历史批次不回溯。
- AVCO：调整时更新移动平均成本，从过账点起影响后续出库；不会回溯已完成的出库。
- Standard：通常将差额记入“价格差异/采购价差科目”，如需反映到库存资产需配套政策。

---

## 七、配置与注意事项

1. 准备会计科目与日记账：运费、关税、保险、价差、库存资产等。
2. 在到岸成本单选择正确的 `journal_id`，确保可过账。
3. 仅对“可估价且在库的产品移动”分摊；已全部发出的移库行无法分摊（或只可对未结部分）。
4. 多币种：费用与收货币种不同，按公司本位币计算后分摊，注意汇兑差。
5. 税务：费用商品的税金按当地法规处理（可计入成本或费用）。

---

## 八、常见问题

- 分摊金额为0：检查选择的拣货/移库行是否仍有可估价数量，或分摊方法分母为0。
- 无法过账：检查日记账、科目权限、期间是否开放。
- 分摊影响与预期不符：核对分摊方法、数量/重量/体积的数据准确性。

---

## 九、总结

- `stock_landed_costs` 实现了采购附加成本的精准分摊与会计入账，提升产品成本的真实性。
- 结合 `stock_account` 的估价层、`purchase` 的收货/账单流程，形成端到端的完整成本闭环。

