---
title: Odoo Manufacturing
type: concept
tags: [odoo, mature]
sources: [raw/Odoo/]
created: 2026-05-05
updated: 2026-05-05
summary: Odoo Manufacturing 包含 BoM(物料清单)、MRP(物料需求计划)、Work Order(工单)、Quality(质量)、Maintenance(维护)、PLM(产品生命周期)六大模块,覆盖中小制造企业从计划到执行的完整生产链。
---

# Odoo Manufacturing

## 定义

Odoo Manufacturing 是 Odoo 面向制造业的功能套件,把传统 ERP 中分散的生产计划、车间管理、质量控制、设备维护功能整合到 Odoo 统一界面。它的核心价值不在与 SAP / Oracle 比拼大型制造功能完备度,而在为**中小制造企业(SME)**提供"够用、易上手、与销售/采购/库存自然贯通"的生产管理。

## 模块组成

**1. Manufacturing(MRP 核心)**

- 制造订单(Manufacturing Order)
- 物料清单(BoM)管理
- 生产路线(Routing)
- 工作中心(Work Center)
- MRP Run(物料需求计算)
- 在制品(WIP)、产成品

**2. Bill of Materials(物料清单)**

- 多级 BoM(成品 → 半成品 → 原料)
- BoM 类型:Manufacture(自制)、Kit(套件)、Subcontract(委外)
- 替代物料(Alternative Component)
- 工艺路线(Routing)与 BoM 关联

**3. MRP(物料需求计划)**

- 主生产计划(Master Production Schedule)
- 净需求计算(扣库存、扣在订)
- 自动建议采购、生产
- 安全库存(Reordering Rule)

**4. Quality(质量)**

- 质量点(Quality Point):在收货、出货、生产中插入检验
- 质量警报(Quality Alert)与不合格处理
- SPC 统计过程控制
- 抽样检验

**5. Maintenance(设备维护)**

- 预防性维护计划
- 故障维修工单
- MTBF / MTTR 计算
- 设备 OEE 指标(可用性 × 性能 × 质量)

**6. PLM(产品生命周期管理,企业版)**

- 工程变更单(ECO)
- BoM 版本控制
- 工程图纸附件
- 变更审批流程

## 典型生产流程

**1. 销售触发**

客户下单 → 销售订单确认 → 系统检查库存 → 不足则触发生产订单(MO)

**2. MRP 计算**

- 看 BoM 需要哪些零件
- 检查零件库存与在订
- 不足则发起采购订单(PO)
- 计划生产时间(基于 Work Center 容量)

**3. 制造执行**

- Work Order 派发到车间
- 工人在 Tablet/Mobile 端确认开始/完成
- 实时记录工时、消耗物料、合格品/废品
- IoT Box 可对接秤、扫码枪、传感器

**4. 质量检验**

- 收货时对原料 IQC
- 生产中 IPQC 抽检
- 出货前 OQC
- 不合格记录质量警报,触发返工或报废

**5. 入库**

- 完成的产成品入库
- 自动更新销售订单可发货状态

## 工艺路线(Routing)

- 定义产品制造的多个步骤(裁切 → 焊接 → 喷漆 → 组装 → 包装)
- 每步绑定 Work Center(机器、工位)
- 时长(Cycle Time + Setup Time)
- 工人技能要求

## 看板(Kanban)与车间显示

- Work Order 列表以看板视图展示
- Tablet 适配的 Workorder 界面
- 大屏看板显示当日进度

## 委外加工(Subcontracting)

- BoM 类型设为 Subcontract
- 系统自动:发料给供应商 → 跟踪生产 → 收回成品
- 委外仓库(Subcontracting Location)管理在外物料

## 与 ERP 集成

**与销售集成**

- 卖配置型产品时自动算 BoM 成本与定价
- MTO(Make-to-Order)直接订单生产

**与采购集成**

- MRP 缺料自动建议 PO
- 多供应商比价

**与库存集成**

- 多仓位(原料仓、在制品仓、成品仓)
- 批次/序列号追溯

**与会计集成**

- 标准成本 / 实际成本
- 变动成本归集
- 在制品成本核算

## 行业适配

**离散制造**

- 机械、电子、家具、玩具
- BoM 树状结构
- 工序明确

**流程制造**

- 食品、化工、制药
- 配方(Formula)而非 BoM(部分需第三方模块)
- 批次追溯严

**装配业**

- 汽车配件、家电
- 多级 BoM
- 工艺路线长

## 与 SAP / Oracle 对比

Odoo Manufacturing 适合年产值 < $100M 的中小制造企业。SAP S/4HANA 在大型多工厂、复杂工艺、严格合规(航空、医药)场景仍是主流。Odoo 优势是上线周期短(2-6 个月 vs 1-2 年)、价格低 5-20 倍、定制灵活。

## 局限

- APS(高级排程)能力较弱,大规模优化排程需第三方
- 流程制造功能(配方、产出比、副产品)需第三方模块
- 质量管理深度不及专业 QMS(如 MasterControl)
- 多工厂调度需企业版 + 一些定制
- IoT 设备集成生态弱于工业 ERP

## 参考源

- raw/Odoo/
- 相关:[[Odoo模块体系]]、[[Odoo视图体系]]
