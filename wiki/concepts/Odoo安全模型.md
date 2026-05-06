---
title: Odoo 安全模型
type: concept
tags: [erp, mature]
sources: [raw/Odoo/04-精通创新层/01-架构设计/安全架构设计.md, raw/Odoo/01-基础认知层/01-概念与架构/Odoo架构详解.md]
created: 2026-05-05
updated: 2026-05-05
summary: Odoo 安全采用四层模型:用户(res.users)→组(res.groups)→模型访问(ir.model.access.csv)→记录规则(ir.rule)→字段访问(field groups),组合实现细粒度权限控制。
---

# Odoo 安全模型

## 定义

Odoo 安全模型(Security Model)是控制"谁在什么条件下可以读/写/创建/删除什么数据"的一整套机制。它不是单一开关,而是 **多层次组合**——任何一条记录是否可见,都是用户、组、模型权限、记录规则、字段权限五重过滤的结果。理解这套模型是部署任何严肃 [[Odoo模块体系]] 的前提。

## 核心要点

### 五层结构

```
用户 (res.users)
  ↓ 属于
权限组 (res.groups)
  ↓ 持有
[模型权限 ir.model.access | 记录规则 ir.rule | 字段权限 field.groups | 菜单可见性]
```

### 权限组(Groups)

`res.groups` 把用户归类。一个用户可以属于多个组。Odoo 内置的关键组:
- `base.group_user`:内部用户(雇员)
- `base.group_portal`:门户用户(客户)
- `base.group_public`:公共用户(网站匿名)
- `base.group_system`:管理员(超级权限)
- `base.group_no_one`:开发者模式专用(技术功能可见)

每个业务模块再定义自己的组,如 `sales_team.group_sale_manager`。

### 模型访问(ir.model.access.csv)

定义 **某个组对某个模型的 CRUD 权限**:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model.user,model_my_model,base.group_user,1,1,1,0
access_my_model_manager,my.model.manager,model_my_model,my_module.group_manager,1,1,1,1
```

四个布尔列:read、write、create、unlink(删除)。

### 记录规则(ir.rule)

模型权限是"全有或全无",记录规则做行级过滤。例如:**销售员只能看自己的订单**:

```xml
<record id="sale_order_personal" model="ir.rule">
    <field name="name">销售员仅看自己订单</field>
    <field name="model_id" ref="sale.model_sale_order"/>
    <field name="domain_force">[('user_id','=',user.id)]</field>
    <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
</record>
```

`domain_force` 是 ORM 域,`user.id` 等占位符在运行时替换。

### 字段级权限

字段定义时加 `groups`,无该组的用户看不到这个字段:

```python
salary = fields.Float('薪资', groups='hr.group_hr_manager')
```

[[Odoo视图体系]] 渲染时会自动跳过无权字段,API 也会过滤。

### 多公司隔离

`res.company` 作为多租户边界,大多数模型有 `company_id` 字段,记录规则限制每个用户只能看到自己公司的数据。集团/连锁场景的关键基础设施。

### 审计

`mail.thread` 自动追踪字段变更;关键操作可通过 `audittrail`(EE)或社区 `auditlog` 模块全量记录。

## 关系

- 拦截 [[Odoo ORM]] 的 search/read/write/unlink 调用
- 联动 [[Odoo视图体系]] 隐藏无权字段与按钮
- 配合 [[Odoo工作流]] 限定状态转换的执行者

## 参考源

- raw/Odoo/04-精通创新层/01-架构设计/安全架构设计.md
- raw/Odoo/01-基础认知层/01-概念与架构/Odoo架构详解.md
