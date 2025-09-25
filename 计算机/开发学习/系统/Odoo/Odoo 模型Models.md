# 🏗️ Odoo 模型（Models）学习大纲

---

## 1. 核心概念

- 模型 = ORM 的核心单元
    
- 对应数据库表（PostgreSQL）
    
- 定义数据结构（字段）、业务逻辑（方法）、关系（关联字段）
    
- 所有标准模型继承自 `models.Model`
    
- `_name` 决定模型标识，对应数据库表名
    
- 可继承、可扩展、可复用
    

---

## 2. 模型定义结构

- **基本属性**
    
    - `_name`：模型唯一标识
        
    - `_description`：模型描述
        
    - `_inherit`：继承其他模型逻辑
        
    - `_inherits`：委托继承
        
    - `_order`：默认排序
        
    - `_rec_name`：显示名称字段
        
- **字段定义**
    
    - 基础字段（Char, Text, Integer, Float, Boolean, Date, Datetime）
        
    - 关系字段（Many2one, One2many, Many2many）
        
    - 功能字段（Computed, Related, Stored）
        
- **方法定义**
    
    - CRUD 操作（create, write, unlink, copy）
        
    - 搜索操作（search, search_count, browse）
        
    - 业务逻辑方法（计算、状态更新等）
        

---

## 3. 字段类型

1. **基础字段**
    
    - 字符串、文本、整数、浮点、布尔、日期、日期时间
        
2. **关系字段**
    
    - Many2one → 多对一
        
    - One2many → 一对多
        
    - Many2many → 多对多
        
3. **计算/关联字段**
    
    - Computed → 计算字段
        
    - Related → 关联字段
        
    - Stored → 是否存储计算结果
        

---

## 4. 模型继承方式

1. **普通继承（_inherit）**
    
    - 扩展或重写现有模型逻辑
        
2. **委托继承（_inherits）**
    
    - 保留原模型表，建立关联表，实现组合
        
3. **抽象模型（_abstract = True）**
    
    - 不生成数据库表，提供公共字段和方法供继承
        

[[Odoo 模型继承机制]]


---

## 5. ORM 常用方法

- **创建**：create(vals)
    
- **更新**：write(vals)
    
- **删除**：unlink()
    
- **搜索**：search(domain)
    
- **计数**：search_count(domain)
    
- **按 ID 获取**：browse(id)
    
- **复制**：copy(defaults)
    

---

## 6. 与其他模块的结合

- **消息系统**：继承 `mail.thread` → 可在记录上发消息
    
- **活动提醒**：继承 `mail.activity.mixin` → 待办和提醒功能
    
- **视图绑定**：模型字段决定界面显示内容
    
- **权限控制**：与 `ir.model.access` 和记录规则配合
    

---

## 7. 典型使用场景

- 客户管理（res.partner）
    
- 销售订单（sale.order）
    
- 项目任务（project.task）
    
- 产品目录（product.product）
    
- 邮件模板、活动提醒、审批流程
    

---

## 8. 注意事项

- 模型名唯一，模块间避免冲突
    
- 字段命名规范，易于维护
    
- 继承和委托继承选型需谨慎
    
- 方法尽量使用 ORM 提供接口，避免直接操作数据库
    
- 多模型组合使用，可实现业务逻辑模块化