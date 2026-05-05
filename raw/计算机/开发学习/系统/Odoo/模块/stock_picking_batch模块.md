# 📦📦 Odoo `stock_picking_batch` 模块详解

## 一、`stock_picking_batch` 模块的作用

- 将多个拣货/交货单合并为一个“批次”（Wave/Batch）统一执行。
- 支持波次拣货、按路线拣货、单人/多人分工，提高效率与准确率。
- 与条码（`stock_barcode`）联动，移动端按批次引导拣货。

---

## 二、核心模型与关键字段（常用）

```python
# 批次拣货主表
class StockPickingBatch(models.Model):
    _name = 'stock.picking.batch'
    name = fields.Char('Batch Reference', required=True, copy=False, default='New')
    user_id = fields.Many2one('res.users', 'Responsible')
    company_id = fields.Many2one('res.company', required=True)
    state = fields.Selection([
        ('draft','Draft'),('in_progress','In Progress'),('done','Done'),('cancel','Cancelled')
    ], default='draft')
    picking_ids = fields.One2many('stock.picking', 'batch_id', string='Pickings')
    operation_type_id = fields.Many2one('stock.picking.type', 'Operation Type')
    scheduled_date = fields.Datetime('Planned Date')

# 在拣货单侧有反向关联
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    batch_id = fields.Many2one('stock.picking.batch', string='Batch')
```

---

## 三、典型业务流程

### 1. 批次创建与分配

1) 选择待拣的交货单（可按客户/路线/优先级筛选）
2) 创建批次并分配至拣货员或团队
3) 固定批次的操作类型（通常为 Delivery）与计划时间

### 2. 扫码拣货执行（配合 `stock_barcode`）

1) 拣货员在移动端打开“批次拣货”
2) 按系统引导或优化路线逐位拣货：
   - 扫描库位 → 扫描产品/批次 → 输入数量
3) 完成批次后统一验证并转到打包/交付

### 3. 打包与交货

- 可在打包区进行打包、贴面单
- 统一生成交货完成记录，通知下游物流

---

## 四、分组与优化策略

- 按路线（Route）/库位群组创建批次，减少往返
- 按客户合并，降低分拣切换
- 按体积/重量控制批次规模，避免一次拣取过重/过大
- 优先级策略：先拣急单，高价值客户优先

---

## 五、关键指标（KPI）与报表

- 批次拣货完成时长（计划 vs 实际）
- 每人/每天完成批次数与行数
- 缺货率/换货率（拣货失败率）
- 库位触达次数与路线优化效果

---

## 六、配置与最佳实践

1) 操作类型与库位：确保拣货操作类型与路径配置正确
2) 批次大小：依据SKU集中度、库位分布、人员数量设定合理大小
3) 联动条码：在批次页面启用移动拣货模式，减少手工点击
4) 锁定策略：执行中的批次锁定相关拣货单，避免并发
5) 异常处理：缺货/误扫时，允许部分完成并记录异常行

---

## 七、常见问题

- 批次状态卡住：检查子拣货单是否全部完成，是否存在被分配但未执行的移动
- 路线不合理：基础数据（库位坐标/序号）不全时无法优化；完善库位元数据
- 并发冲突：执行锁与任务分配策略不清晰，建议启用锁定并规范交接

---

## 八、总结

- `stock_picking_batch` 通过批次化与移动扫码协同，大幅提升拣货效率。
- 与 `stock_barcode`、`stock`、`sale_stock` 协作，形成高效拣货-打包-交付链路。

