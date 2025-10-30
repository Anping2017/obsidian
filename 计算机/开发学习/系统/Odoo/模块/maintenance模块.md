# 🔧 Odoo `maintenance` 模块详解

## 一、`maintenance` 模块的作用

- 管理设备全生命周期：建档、点检、保养、维修、报废。
- 支持预防性维护（时间/计数触发）与纠正性维护（故障工单）。
- 与 `mrp`、`quality`、`stock` 集成，降低停机并提升设备可用率。

---

## 二、核心对象与字段（常用）

```python
# 设备档案
class MaintenanceEquipment(models.Model):
    _name = 'maintenance.equipment'
    name = fields.Char(required=True)
    category_id = fields.Many2one('maintenance.equipment.category', 'Category')
    serial_no = fields.Char('Serial Number')
    model = fields.Char('Model')
    partner_id = fields.Many2one('res.partner', 'Vendor')
    location = fields.Char('Location')
    technician_user_id = fields.Many2one('res.users', 'Technician')
    effective_date = fields.Date('In Service Date')
    expected_lifetime = fields.Integer('Expected Lifetime (months)')
    maintenance_team_id = fields.Many2one('maintenance.team', 'Team')
    notes = fields.Text()

# 维护请求（工单）
class MaintenanceRequest(models.Model):
    _name = 'maintenance.request'
    name = fields.Char(required=True)
    equipment_id = fields.Many2one('maintenance.equipment', required=True)
    maintenance_type = fields.Selection([
        ('corrective','Corrective'),('preventive','Preventive')
    ], default='corrective')
    request_date = fields.Datetime('Requested Date', default=fields.Datetime.now)
    schedule_date = fields.Datetime('Scheduled Date')
    close_date = fields.Datetime('Close Date')
    duration = fields.Float('Duration (hours)')
    stage_id = fields.Many2one('maintenance.stage', 'Stage')
    priority = fields.Selection([('0','Low'),('1','Normal'),('2','High'),('3','Urgent')], default='1')
    user_id = fields.Many2one('res.users', 'Assigned To')
```

---

## 三、维护策略

### 1. 预防性维护（PM）

- 触发方式：
  - 时间周期：每周/每月/每季度（基于 `schedule_date` 计划工单）
  - 计数触发：产量/运行小时（需与计数器/物联网对接或人工录入）
- 内容：点检、润滑、校准、耗材更换。

### 2. 纠正性维护（CM）

- 故障发生后创建工单，记录停机时间、原因、维修措施与更换件。
- 可与 `stock` 联动领用备件（库存出库）。

---

## 四、与其他模块集成

- `mrp`：
  - 停机登记：通过维护工单记录停机时长；可用于OEE（稼动率）分析。
  - 工单挂起/恢复：维修完成后恢复生产。
- `quality`：
  - 质量异常触发维护（如尺寸漂移→设备校准）。
- `stock`：
  - 备件管理：维护用备件入库/出库、最低库存补货。

---

## 五、KPI 与报表

- MTBF（平均故障间隔）、MTTR（平均修复时间）
- 设备可用率、停机率
- 计划维护达成率（按时完成率）
- 工单关闭时长分布、备件消耗统计

---

## 六、配置与最佳实践

1) 建立设备层级与编码规范（车间/产线/工位/设备）。
2) 制定PM计划：目标是“少量高频点检 + 关键节点校准”，降低突发停机。
3) 备件台账：常用备件设再订货点，与 `purchase` 自动补货。
4) 故障分类与根因分析：在工单模板中固定填写项，便于统计改进。
5) SLA/响应机制：对关键设备设响应时限与升级规则。

---

## 七、常见问题

- 工单堆积：设置工单优先级与计划排程，按SLA督办。
- 停机统计不准：规范“开始/完工”时间的登记，必要时引入设备信号采集。
- 备件断供：为关键件设安全库存与替代件库。

---

## 八、总结

- `maintenance` 通过设备建档、PM/CM、备件管理与KPI分析，降低故障率与停机时间。
- 与 `mrp`/`quality`/`stock` 协同，形成“质量→维护→生产”闭环，提升产线稳定性。

