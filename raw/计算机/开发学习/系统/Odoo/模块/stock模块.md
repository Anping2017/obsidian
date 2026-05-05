# 📦 Odoo `stock` 模块详解

## 一、`stock` 模块的作用

- **库存管理核心模块**。
- 管理多仓库、库存移动、库存调整等功能。
- 提供完整的仓库管理解决方案。
- 是库存业务的基础模块。

📌 形象理解：  
👉 仓库团队使用 `stock` 模块管理仓库库存和货物移动。

---

## 二、核心功能

### 1. 多仓库管理

- 创建和管理多个仓库
- 仓库位置（Locations）管理
- 仓库层级结构
- 多仓库库存查询

### 2. 库存移动（Stock Moves）

- 管理货物的所有移动
- 入库、出库、内部转移
- 移动状态跟踪
- 移动历史记录

### 3. 库存调整

- 库存盘点
- 库存调整
- 差异处理
- 调整历史记录

### 4. 库存估值

- 计算库存价值
- 成本计算方法（FIFO、平均成本等）
- 库存价值报表

### 5. 库存报表

- 库存报表和分析
- 库存周转分析
- 库存预警
- 库存趋势分析

---

## 三、核心模型

### 1. `stock.warehouse` - 仓库

仓库主模型：

```
class StockWarehouse(models.Model):
    _name = 'stock.warehouse'
    
    name = fields.Char('Warehouse Name', required=True)
    code = fields.Char('Short Name', required=True)
    partner_id = fields.Many2one('res.partner', 'Address')
    view_location_id = fields.Many2one('stock.location', 'View Location')
    lot_stock_id = fields.Many2one('stock.location', 'Location Stock')
```

### 2. `stock.location` - 位置

仓库位置模型：

```
class StockLocation(models.Model):
    _name = 'stock.location'
    
    name = fields.Char('Location Name', required=True)
    location_id = fields.Many2one('stock.location', 'Parent Location')
    complete_name = fields.Char('Full Location Name', compute='_compute_complete_name')
    usage = fields.Selection([
        ('supplier', 'Vendor Location'),
        ('view', 'View'),
        ('internal', 'Internal Location'),
        ('customer', 'Customer Location'),
        ('inventory', 'Inventory'),
        ('production', 'Production'),
        ('transit', 'Transit Location')
    ], string='Location Type')
```

位置类型：
- **供应商位置**：从供应商接收货物的位置
- **视图**：虚拟位置，用于组织
- **内部位置**：仓库内部存储位置
- **客户位置**：向客户发货的位置
- **盘点位置**：库存盘点位置
- **生产位置**：生产相关位置
- **中转位置**：运输中转位置

### 3. `stock.move` - 库存移动

库存移动模型：

```
class StockMove(models.Model):
    _name = 'stock.move'
    
    name = fields.Char('Description', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    product_uom_qty = fields.Float('Demand', required=True)
    quantity_done = fields.Float('Done', default=0.0)
    location_id = fields.Many2one('stock.location', 'From', required=True)
    location_dest_id = fields.Many2one('stock.location', 'To', required=True)
    state = fields.Selection([
        ('draft', 'New'),
        ('waiting', 'Waiting Another Move'),
        ('confirmed', 'Waiting Availability'),
        ('assigned', 'Available'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status')
```

移动状态：
- **草稿**（Draft）：新创建的移动
- **等待**（Waiting）：等待其他移动
- **已确认**（Confirmed）：等待可用库存
- **已分配**（Assigned）：库存已预留
- **已完成**（Done）：移动已完成
- **已取消**（Cancelled）：移动已取消

### 4. `stock.picking` - 交货单/收货单

交货单/收货单模型：

```
class StockPicking(models.Model):
    _name = 'stock.picking'
    
    name = fields.Char('Reference', required=True)
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type')
    partner_id = fields.Many2one('res.partner', 'Partner')
    move_ids = fields.One2many('stock.move', 'picking_id', 'Operations')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('ready', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status')
```

---

## 四、库存操作类型

### 1. 收货（Incoming）

- 从供应商接收货物
- 创建收货单
- 处理入库操作

### 2. 发货（Outgoing）

- 向客户发送货物
- 创建交货单
- 处理出库操作

### 3. 内部转移（Internal Transfer）

- 仓库间转移
- 位置间转移
- 内部移动管理

### 4. 库存调整（Inventory Adjustment）

- 库存盘点
- 差异调整
- 库存修正

---

## 五、库存计算

### 1. 在手库存（On Hand）

- 仓库中实际可用的库存
- 实时计算
- 按位置显示

### 2. 预留库存（Reserved）

- 已为订单预留的库存
- 预留后不可用于其他订单
- 订单完成后释放

### 3. 可用库存（Available）

- 在手库存 - 预留库存
- 可用于新订单的库存
- 实时更新

### 4. 在途库存（In Transit）

- 正在运输中的库存
- 从供应商到仓库
- 从仓库到客户

---

## 六、与其他模块的集成

### 1. 与 `sale` 模块（需 `sale_stock`）

- 销售订单创建交货单
- 自动预留库存
- 发货跟踪

### 2. 与 `purchase` 模块（需 `purchase_stock`）

- 采购订单创建收货单
- 收货处理
- 库存入库

### 3. 与 `mrp` 模块

- 生产订单消耗原材料
- 生产完成入库
- 生产库存移动

### 4. 与 `account` 模块（需 `stock_account`）

- 库存价值记账
- 成本核算
- 库存会计科目

---

## 七、库存报表和分析

### 1. 库存报表

- 当前库存报表
- 按仓库的库存
- 按产品的库存
- 库存价值报表

### 2. 库存周转分析

- 库存周转率
- 周转天数
- 滞销产品分析

### 3. 库存预警

- 低库存预警
- 高库存预警
- 过期产品预警

---

## 八、典型使用场景

1. **多仓库管理**：管理多个仓库和位置
2. **库存跟踪**：跟踪所有库存移动
3. **库存调整**：进行库存盘点和调整
4. **库存分析**：分析库存状况和趋势
5. **库存优化**：优化库存水平，减少库存成本

---

## 九、配置和设置详解

### 1. 仓库配置

#### 创建仓库

1. **库存 > 配置 > 仓库 > 仓库**
2. 创建新仓库：
   - **名称**：仓库名称（如"主仓库"、"配送中心"）
   - **简称**：仓库代码（用于单据编号）
   - **地址**：仓库地址（关联 `res.partner`）

3. **位置结构**：
   系统自动创建以下位置：
   - **视图位置**：仓库的根位置（虚拟位置）
   - **库存位置**：实际存储货物的位置
   - **供应商位置**：接收供应商货物
   - **客户位置**：向客户发货

#### 仓库位置结构示例

```
主仓库（View Location）
 ├── 供应商位置（Vendor Location）
 ├── 库存位置（Stock Location）
 │    ├── A区
 │    ├── B区
 │    └── C区
 └── 客户位置（Customer Location）
```

#### 多仓库配置

- **创建多个仓库**：支持多个物理仓库
- **仓库间转移**：处理仓库间的货物转移
- **多仓库库存查询**：查看所有仓库的库存

### 2. 位置配置

#### 创建位置层级

1. **库存 > 配置 > 位置**
2. 创建位置层级：
   - **主仓库**（View）
     - **A区**（Internal）
       - **货架1**（Internal）
       - **货架2**（Internal）
     - **B区**（Internal）

#### 位置类型详解

- **视图位置**（View）：
  - 用于组织，不存储实际货物
  - 可以是仓库的根位置或区域

- **内部位置**（Internal）：
  - 仓库内实际存储位置
  - 可以是货架、区域、房间等

- **供应商位置**（Vendor Location）：
  - 虚拟位置，代表供应商
  - 收货时从供应商位置移出

- **客户位置**（Customer Location）：
  - 虚拟位置，代表客户
  - 发货时移到客户位置

- **盘点位置**（Inventory）：
  - 用于库存盘点
  - 盘点差异调整位置

- **生产位置**（Production）：
  - 生产相关位置
  - 原材料消耗和成品入库

- **中转位置**（Transit）：
  - 运输中转位置
  - 仓库间转移时使用

### 3. 操作类型配置

#### 操作类型模型

```
class StockPickingType(models.Model):
    _name = 'stock.picking.type'
    _description = 'Picking Type'
    
    name = fields.Char('Operation Type', required=True)
    code = fields.Selection([
        ('incoming', 'Receipt'),
        ('outgoing', 'Delivery'),
        ('internal', 'Internal Transfer'),
        ('mrp_operation', 'Manufacturing')
    ], string='Type of Operation', required=True)
    default_location_src_id = fields.Many2one('stock.location', 'Default Source Location')
    default_location_dest_id = fields.Many2one('stock.location', 'Default Destination Location')
    sequence_id = fields.Many2one('ir.sequence', 'Sequence')
    company_id = fields.Many2one('res.company', 'Company')
```

#### 配置收货类型

1. **库存 > 配置 > 操作类型**
2. 编辑"收货"操作类型：
   - **默认源位置**：供应商位置
   - **默认目标位置**：库存位置
   - **序列号**：收货单编号规则

#### 配置发货类型

1. 编辑"发货"操作类型：
   - **默认源位置**：库存位置
   - **默认目标位置**：客户位置
   - **序列号**：交货单编号规则

#### 配置内部转移类型

1. 编辑"内部转移"操作类型：
   - **默认源位置**：源仓库位置
   - **默认目标位置**：目标仓库位置

### 4. 库存规则配置

#### 补货规则（Reordering Rules）

1. **库存 > 配置 > 补货规则**
2. 创建补货规则：
   - **产品**：要补充的产品
   - **仓库**：应用规则的仓库
   - **最小数量**：触发补货的最低库存
   - **最大数量**：补货目标数量
   - **补货方法**：
     - 采购（Purchase）
     - 制造（Manufacture）
     - 从其他位置转移（Transfer）

#### 补货规则模型

```
class StockWarehouseOrderPoint(models.Model):
    _name = 'stock.warehouse.orderpoint'
    _description = 'Reordering Rule'
    
    name = fields.Char('Name', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', required=True)
    location_id = fields.Many2one('stock.location', 'Location')
    product_min_qty = fields.Float('Minimum Quantity', required=True)
    product_max_qty = fields.Float('Maximum Quantity', required=True)
    qty_multiple = fields.Float('Qty Multiple', default=1.0)
    group_id = fields.Many2one('procurement.group', 'Procurement Group')
```

#### 自动采购规则

- **触发条件**：库存低于最小数量
- **自动创建采购请求**：系统自动创建采购请求
- **批量补货**：合并多个产品的补货需求

---

## 十、典型使用场景详解

### 场景 1：标准收货流程

**需求**：从供应商接收货物并入库

**详细步骤**：

1. **采购订单确认**
   - 采购订单确认后自动创建收货单（需 `purchase_stock`）
   - 或手动创建收货单

2. **收货单处理**
   ```
   库存 > 操作 > 收货
   - 选择收货单
   - 检查产品和数量
   - 确认收货
   ```

3. **货物验收**
   - 检查货物是否符合订单
   - 检查数量是否正确
   - 检查质量（可选）

4. **确认收货**
   - 输入实际收货数量（如与订单不同）
   - 选择存储位置
   - 确认收货

5. **库存入库**
   - 系统自动更新库存
   - 库存从供应商位置移到库存位置
   - 更新在手库存数量

### 场景 2：销售发货流程

**需求**：向客户发货

**详细步骤**：

1. **销售订单确认**
   - 销售订单确认后自动创建交货单（需 `sale_stock`）
   - 系统自动预留库存

2. **交货单处理**
   ```
   库存 > 操作 > 发货
   - 选择交货单
   - 从库存位置拣货
   - 确认发货数量
   ```

3. **拣货和打包**
   - 从指定位置取货
   - 检查产品是否正确
   - 打包准备发货

4. **确认发货**
   - 输入实际发货数量
   - 选择发货位置
   - 确认发货

5. **库存出库**
   - 系统自动更新库存
   - 库存从库存位置移到客户位置
   - 释放预留库存（如有剩余）

### 场景 3：库存盘点

**需求**：定期进行库存盘点

**详细步骤**：

1. **创建盘点**
   ```
   库存 > 操作 > 库存调整
   - 选择产品和位置
   - 输入盘点日期
   - 创建盘点单
   ```

2. **执行盘点**
   - 实际清点库存
   - 记录实际数量
   - 在系统中输入实际数量

3. **差异分析**
   - 系统计算差异
   - 分析差异原因
   - 记录差异说明

4. **确认调整**
   - 审核差异
   - 确认库存调整
   - 系统更新库存数量

5. **差异处理**
   - 差异原因分析
   - 采取措施防止再次发生
   - 更新库存记录

### 场景 4：仓库间转移

**需求**：在多个仓库间转移货物

**详细步骤**：

1. **创建转移**
   ```
   库存 > 操作 > 内部转移
   - 选择源仓库和目标仓库
   - 选择产品和数量
   - 创建转移单
   ```

2. **转移处理**
   - 从源仓库拣货
   - 确认转移数量
   - 安排运输

3. **确认转移**
   - 货物到达目标仓库
   - 确认接收
   - 更新两仓库的库存

---

## 十一、库存计算详解

### 1. 在手库存（On Hand）计算

**计算公式**：

```
在手库存 = 初始库存 + 总收货 - 总发货 + 调整
```

**查询方式**：

```python
# 查询产品在手库存
product = self.env['product.product'].browse(product_id)
on_hand_qty = product.qty_available

# 查询指定位置的库存
location = self.env['stock.location'].browse(location_id)
products = location.quant_ids.mapped('product_id')
```

### 2. 预留库存（Reserved）计算

**预留机制**：

- 销售订单确认时自动预留
- 生产订单创建时预留原材料
- 预留后不可用于其他订单

**查询方式**：

```python
# 查询预留数量
product = self.env['product.product'].browse(product_id)
reserved_qty = product.virtual_available - product.qty_available
```

### 3. 可用库存（Available）计算

**计算公式**：

```
可用库存 = 在手库存 - 预留库存
```

**用途**：

- 检查是否可以满足新订单
- 库存预警
- 补货决策

### 4. 预测库存（Forecasted）计算

**计算逻辑**：

```
预测库存 = 在手库存 
         + 预计收货（采购订单、生产订单）
         - 预留库存
         - 预计发货（销售订单、生产消耗）
```

**应用场景**：

- MRP 计划
- 补货决策
- 库存预警

---

## 十二、库存移动详解

### 1. 库存移动类型

#### 收货移动（Incoming）

```
源位置：供应商位置
目标位置：库存位置
触发：采购订单、手动收货
```

#### 发货移动（Outgoing）

```
源位置：库存位置
目标位置：客户位置
触发：销售订单、手动发货
```

#### 内部转移移动（Internal）

```
源位置：源仓库位置
目标位置：目标仓库位置
触发：内部转移单、位置调整
```

#### 盘点移动（Inventory）

```
源位置：库存位置
目标位置：盘点位置（差异调整）
触发：库存盘点
```

### 2. 移动状态流转

```
草稿（Draft）
 ↓
已确认（Confirmed）- 系统确认移动可行
 ↓
已分配（Assigned）- 库存已预留
 ↓
已完成（Done）- 实际移动完成
```

### 3. 移动执行

#### 自动执行

- 某些移动可以自动执行
- 如收货时自动确认并完成

#### 手动执行

- 需要人工确认的移动
- 如需要验证的收货和发货

---

## 十三、批次和序列号详解

### 1. 批次管理（Lots）

#### 批次配置

- **产品级别**：在产品上启用批次跟踪
- **批次命名**：自动或手动命名批次
- **批次属性**：生产日期、过期日期等

#### 批次模型

```
class StockLot(models.Model):
    _name = 'stock.lot'
    _description = 'Lot/Serial'
    
    name = fields.Char('Lot/Serial Number', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    expiration_date = fields.Datetime('Expiration Date')
    use_date = fields.Datetime('Best before Date')
    product_uom_id = fields.Many2one('uom.uom', 'Unit of Measure')
    company_id = fields.Many2one('res.company', 'Company')
```

#### 批次使用场景

- **食品行业**：跟踪生产日期和过期日期
- **化工行业**：批次质量控制
- **制药行业**：批次追溯要求

### 2. 序列号管理（Serial Numbers）

#### 序列号配置

- **产品级别**：在产品上启用序列号跟踪
- **唯一序列号**：每个产品单元有唯一序列号
- **序列号追溯**：完整的序列号历史记录

#### 序列号使用场景

- **电子产品**：每台设备有唯一序列号
- **汽车**：每辆车有唯一VIN码
- **高价值产品**：需要精确跟踪的产品

### 3. 追溯功能

#### 向上追溯（Upstream Traceability）

- 查看产品的来源
- 哪些批次/序列号用于生产
- 采购来源信息

#### 向下追溯（Downstream Traceability）

- 查看产品的去向
- 销售给哪些客户
- 用于哪些生产订单

---

## 十四、高级功能详解

### 1. 多仓库管理

#### 仓库网络

- **多个物理仓库**：地理位置不同的仓库
- **仓库层级**：总仓、分仓、配送中心
- **仓库类型**：生产仓库、配送仓库、零售仓库

#### 仓库间转移策略

- **手动转移**：手动创建转移单
- **自动补货**：基于库存规则自动转移
- **集中管理**：从中心仓库向分仓补货

### 2. 库存估值方法

#### FIFO（先进先出）

- **原理**：最早购入的货物优先发出
- **适用**：价格波动较大的产品
- **成本计算**：使用最早批次的价格

#### 平均成本（Average Cost）

- **原理**：使用加权平均成本
- **适用**：简化成本计算
- **更新**：每次收货后更新平均成本

#### 标准成本（Standard Cost）

- **原理**：使用预设的标准成本
- **适用**：标准化生产
- **差异分析**：实际成本与标准成本对比

### 3. 库存补充策略

#### 基于再订购点（Reorder Point）

- **设定再订购点**：最小库存数量
- **自动触发**：库存低于再订购点时触发补货
- **补货数量**：补充到最大库存数量

#### 基于预测（Forecast Based）

- **需求预测**：基于历史数据预测需求
- **计划补货**：提前计划补货
- **平滑需求**：避免库存波动

#### 基于MRP

- **物料需求计划**：基于生产计划计算需求
- **自动生成采购建议**：自动创建采购订单
- **精准计划**：满足生产需求

---

## 十五、库存报表和分析详解

### 1. 库存报表类型

#### 当前库存报表

- **所有产品库存**：查看所有产品的当前库存
- **按仓库筛选**：查看特定仓库的库存
- **按位置筛选**：查看特定位置的库存
- **按产品类别筛选**：按产品类别查看库存

#### 库存价值报表

- **当前库存价值**：按成本计算的库存总值
- **按产品类别**：各类别产品的库存价值
- **按仓库**：各仓库的库存价值
- **按成本方法**：不同成本方法的价值对比

#### 库存变动报表

- **历史变动记录**：所有库存变动历史
- **变动原因**：收货、发货、调整等
- **变动趋势**：库存变化趋势分析

### 2. 库存周转分析

#### 周转率计算

```
库存周转率 = 销售成本 / 平均库存
```

#### 周转天数计算

```
周转天数 = 365 / 库存周转率
```

#### 周转分析应用

- **识别滞销产品**：低周转率的产品
- **优化库存水平**：减少高周转率产品的库存
- **季节性分析**：分析季节性库存需求

### 3. 库存预警

#### 低库存预警

- **设定最小库存**：为产品设置最小库存阈值
- **自动预警**：库存低于阈值时预警
- **补货建议**：自动建议补货

#### 高库存预警

- **设定最大库存**：为产品设置最大库存阈值
- **超量预警**：库存超过阈值时预警
- **原因分析**：分析高库存原因

#### 过期预警

- **批次管理**：跟踪批次过期日期
- **过期预警**：即将过期时预警
- **处理建议**：优先销售建议

---

## 十六、最佳实践

### 1. 仓库布局设计

- **合理分区**：按产品类型或流程分区
- **位置标识**：清晰的位置标识系统
- **路径优化**：优化拣货路径，提高效率

### 2. 库存控制

- **ABC分析**：识别重要产品（A类）
- **定期盘点**：定期进行库存盘点
- **及时调整**：发现差异及时调整

### 3. 库存优化

- **减少库存成本**：在满足需求的前提下减少库存
- **提高周转率**：提高库存周转效率
- **减少滞销**：及时处理滞销产品

### 4. 数据准确性

- **实时更新**：及时更新库存数据
- **定期核对**：定期核对系统与实际库存
- **差异处理**：及时处理库存差异

---

## 十七、常见问题

### 问题 1：库存数量不准确

**原因**：
- 移动未确认
- 盘点未完成
- 系统错误

**解决方案**：
1. 检查未完成的移动
2. 完成盘点
3. 核对账目
4. 必要时进行库存调整

### 问题 2：无法发货

**原因**：
- 库存不足
- 库存未预留
- 位置配置错误

**解决方案**：
1. 检查可用库存
2. 确认库存预留
3. 检查位置配置

### 问题 3：批次/序列号错误

**原因**：
- 批次信息录入错误
- 批次与产品不匹配

**解决方案**：
1. 验证批次信息
2. 确保批次正确关联产品
3. 必要时创建调整移动

---

## 十八、总结

- **`stock` 模块**是 Odoo 库存管理的核心。
- 核心功能：
  - 多仓库和位置管理
  - 库存移动跟踪
  - 库存调整和盘点
  - 批次和序列号管理
  - 库存估值
  - 库存报表和分析
  - 与销售、采购、制造等模块的深度集成
- 提供完整的仓库管理解决方案。
- 支持复杂的仓库和库存业务流程。
- 是构建库存管理系统的基础模块。
- 适用于各种规模和类型的仓库管理需求。

