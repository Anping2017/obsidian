# ✅ Odoo `quality` 模块详解

## 一、`quality` 模块的作用

- 建立从来料、在制到成品的质量控制体系（IQC、IPQC、FQC）。
- 通过“检查点（Quality Points）→ 检验（Checks）→ 不合格（NC）→ 纠正/预防措施（CAPA）”闭环管理质量。
- 与 `stock`、`mrp`、`purchase`、`maintenance` 联动，将质检嵌入业务流程。

---

## 二、核心对象与字段（常用）

```python
# 质量检查点：定义在哪个流程/产品触发检查
class QualityPoint(models.Model):
    _name = 'quality.point'
    name = fields.Char(required=True)
    team_id = fields.Many2one('quality.team', 'Quality Team')
    product_tmpl_id = fields.Many2one('product.template', 'Product')
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type')  # 收货/发货/内部/制造
    operation = fields.Selection([
        ('incoming','Receipt'), ('outgoing','Delivery'), ('internal','Internal Transfer'), ('manufacturing','Manufacturing')
    ], default='incoming')
    control_ids = fields.One2many('quality.point.test.type', 'quality_point_id', 'Controls')
    measure_frequency = fields.Float('Sampling %')

# 质量检查记录（执行时生成）
class QualityCheck(models.Model):
    _name = 'quality.check'
    point_id = fields.Many2one('quality.point')
    product_id = fields.Many2one('product.product')
    lot_id = fields.Many2one('stock.lot', 'Lot/Serial')
    picking_id = fields.Many2one('stock.picking')
    production_id = fields.Many2one('mrp.production')
    measure = fields.Float('Measured Value')
    measure_success = fields.Boolean('Passed')
    failure_message = fields.Char('Failure Reason')

# 不合格（NC）与处理
class QualityAlert(models.Model):
    _name = 'quality.alert'
    name = fields.Char(required=True)
    product_id = fields.Many2one('product.product')
    lot_id = fields.Many2one('stock.lot')
    team_id = fields.Many2one('quality.team')
    stage_id = fields.Many2one('quality.alert.stage')
    root_cause = fields.Text('Root Cause')
    corrective_action = fields.Text('Corrective Action')
    preventive_action = fields.Text('Preventive Action')
```

---

## 三、质量流程（典型）

### 1. 来料检验（IQC）

1) 在 `收货` 操作类型上配置质量检查点（可按产品/类别）。
2) 收货时自动生成 `Quality Check`：
   - 计数、量具测量、抽检表单；支持附件与照片。
3) 检验未通过：
   - 自动创建 `Quality Alert`（不合格），隔离库存（移至质检/隔离库位）。
   - 退货、退供应商或让步接收（需审批）。

### 2. 过程检验（IPQC）

- 在制造工序/工位设置检查点（需 `mrp`/`mrp_workorder`）。
- 工序开始/结束触发检验；不合格可挂起工单并触发维护/返工。

### 3. 成品检验（FQC）

- 出库前或完工入库后抽检；未通过则阻塞交付/入库，创建不合格并处置。

---

## 四、控制计划与抽样

- 控制类型：
  - 计量（测量值与上/下限）
  - 计数（缺陷数、不良率）
  - 是/否（合格/不合格）
  - 照片/文件（外观、认证）
- 抽样率：按百分比或固定频次；关键物料设100%。

---

## 五、与其他模块的集成

- `stock`：
  - 质检失败自动移至隔离库位；允许退货流程。
- `purchase`：
  - 供应商来料质检；供应商评分可纳入质量指标。
- `mrp`/`mrp_workorder`：
  - 工序质检、过程放行、返工与报废处理。
- `maintenance`：
  - 质量问题触发设备点检/维修（如尺寸漂移→设备校准）。

---

## 六、数据与报表

- 不合格率（PPM/CPK相关数据可扩展）
- 检验通过率、让步接收率
- 供应商质量绩效（来料不良率、退货率）
- 过程能力趋势（需要定制/BI）

---

## 七、配置与最佳实践

1) 从产品关键度出发设定检查点与抽样率，避免全检带来的效率损失。
2) 将隔离库位与让步接收审批固化流程，避免不合格误发货。
3) 与制造工序绑定的质检用于早发现、早处置，降低报废返工成本。
4) 保留检验数据与照片，便于追溯与8D分析。

---

## 八、常见问题

- 收货未触发质检：检查是否在相应操作类型/产品上配置了检查点。
- 不合格未隔离：确认库存规则中隔离库位与转移自动化是否到位。
- 质检卡住发货：为关键客户保留“让步接收”带审批的绿色通道。

---

## 九、总结

- `quality` 通过检查点-检验-不合格-纠正预防的闭环，将质量控制嵌入收发存与制造环节。
- 与 `stock`、`mrp`、`purchase`、`maintenance` 协同，实现质量问题的快速反馈与持续改进。

