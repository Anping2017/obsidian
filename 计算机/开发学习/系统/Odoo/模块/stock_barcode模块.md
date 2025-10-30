# 📱 Odoo `stock_barcode` 模块详解

## 一、`stock_barcode` 模块的作用

- 通过条形码/二维码扫描驱动仓库操作（收货、发货、转移、盘点）。
- 降低手工录入错误、提升效率；适配移动设备与工业PDA。
- 支持产品、位置、批次/序列号、拣货单、多步操作扫码。

---

## 二、支持的条码对象与编码约定

- 产品：`product.product` 的 `barcode` 字段（自定义EAN/UPC/Code128/QR）。
- 位置：`stock.location` 的 `barcode` 字段（推荐为库位贴码）。
- 批次/序列：`stock.lot` 的 `name` 可生成条码（生产行业常用）。
- 单据：拣货单/收货单的操作条码（Action Barcode）。

常见规范：
- GS1/EAN-13、Code-128、QR；在仓内推荐统一使用 Code-128 或 QR 以容纳更多信息。

---

## 三、核心模型与关键字段（只列常用）

```python
# 产品
class ProductProduct(models.Model):
    _inherit = 'product.product'
    barcode = fields.Char('Barcode')

# 位置
class StockLocation(models.Model):
    _inherit = 'stock.location'
    barcode = fields.Char('Barcode')

# 批次/序列
class StockLot(models.Model):
    _inherit = 'stock.lot'
    name = fields.Char('Lot/Serial Number', required=True)
```

---

## 四、扫码业务流程（操作页）

### 1. 收货（Receipt）

1) 扫描收货单/供应商参考（可选）
2) 扫描位置（入库地点）
3) 扫描产品条码 → 输入/扫描数量 → 确认
4) 如启用批次/序列：扫描/创建批次/序列号
5) 完成收货，系统生成库存移动与估价（配合 `stock_account`）

### 2. 发货（Delivery）

1) 扫描交货单/客户参考（可选）
2) 扫描拣货位置 → 扫描产品
3) 输入数量/批次序列 → 确认拣货
4) 完成拣货并过账发货

### 3. 内部转移（Internal Transfer）

1) 扫描源位置 → 扫描产品/批次 → 输入数量
2) 扫描目标位置 → 确认转移

### 4. 盘点（Inventory Adjustment）

1) 扫描位置 → 扫描产品（批次/序列）
2) 输入实盘数量 → 提交

---

## 五、移动端/硬件与性能

- 设备：手机/平板+摄像头、蓝牙手柄、PDA/工业扫描器。
- 模式：网页端移动视图（响应式）、PWA、PDA浏览器。
- 网络：弱网场景可使用缓存与延迟提交（需评估插件/二开）。

---

## 六、配置与最佳实践

1) 条码统一规范：统一编码格式与生成规则；避免重复条码。
2) 位置贴码：对主要库位粘贴位置条码，提升转移/盘点效率。
3) 批次/序列策略：启用需要跟踪的产品，再配套现场扫码流程。
4) 误扫容错：在界面启用撤销/清空/返回等操作，降低误操作风险。
5) 与 `stock_picking_batch` 联动：批次拣货单上逐单或按路线扫码拣货。

---

## 七、常见问题

- 扫码无响应：检查浏览器摄像头权限或PDA驱动、条码清晰度与对焦。
- 条码重复：确保产品/位置/批次条码唯一性；建立编码规范与校验。
- 数量不一致：核对度量单位与最小包装；使用“逐件扫描”模式减少偏差。

---

## 八、总结

- `stock_barcode` 通过扫码将收发存流程标准化、低差错化。
- 与 `stock`、`stock_picking_batch`、`stock_account`、`mrp` 等模块协同，形成高效的仓储作业链路。

