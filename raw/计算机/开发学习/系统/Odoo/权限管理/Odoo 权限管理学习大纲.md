# 📚 Odoo 权限管理学习大纲


## 一、基础概念入门

1. **用户与伙伴（User & Partner）**
    
    - 用户和 res.partner 的关系
        
    - 用户的登录账号与邮箱绑定
        
    - 内部用户 vs 门户用户 vs 公共用户
        
2. **访问控制层次**   - [[Odoo 权限的层次]]
    
    - 菜单可见性（Menu Items）
        
    - 模型访问控制（Access Control Lists，ACL）
        
    - 记录规则（Record Rules）
        
    - 字段访问控制（groups、readonly、invisible）
        

---

## 二、用户与组（Users & Groups）  - [[用户和用户组]]

1. **用户（res.users）**
    
    - 用户类型（内部、门户、公共）
        
    - 用户配置与公司（multi-company）
        
2. **用户组（res.groups）**
    
    - 用户组的继承关系
        
    - 用户组在 UI 的表现（多选项切换权限）
        
    - 隐藏/显示菜单依赖 groups
        
3. **组与权限的关系**
    
    - 模型访问权限分配
        
    - 字段 domain 与组的结合使用
        
    - record rules 与组的绑定
        

---

## 三、模型访问控制（Access Control Lists, ACL）  [[模型访问控制（ACL）]]

1. **ACL 文件结构**
    
    - ir.model.access.csv 基础结构
        
    - 读、写、创建、删除四个基本权限
        
    - 为不同用户组配置 ACL
        
2. **实战：添加 ACL**
    
    - 新建模型时如何配置 access 文件
        
    - 控制不同角色对同一模型的操作能力
        

---

## 四、记录规则（Record Rules）  - [[记录规则]]

1. **记录规则的机制**
    
    - 记录规则的定义（ir.rule）
        
    - 全局规则 vs 特定组规则
        
    - domain 表达式的使用
        
2. **常见场景**
    
    - 仅能看到自己创建的记录（user_id = uid）
        
    - 仅能访问当前公司数据（company_id = company_ids）
        
    - 部门经理可以看到部门成员数据
        
3. **调试与排错**
    
    - 使用 debug 模式查看 rule 应用情况
        
    - 优先级、冲突与安全陷阱
        

---

## 五、菜单与视图层权限

1. **菜单项权限**  - [[菜单层权限]]
    
    - MenuItem 的 groups_id 限制
        
    - 通过 ir.ui.menu 控制可见性
        
2. **视图层权限** - [[视图层权限]]
    
    - XML 视图中针对组的属性控制：groups="group_id"
        
    - 字段级别的只读、隐藏：readonly + groups
        
    - 动态 domain 与安全性
        

---

## 六、高级权限管理

1. **多公司环境**  - [[多公司环境权限管理]]
    
    - company_id 字段与公司隔离
        
    - allowed_company_ids 与切换公司
        
    - 跨公司访问控制设计
        
2. **门户用户**
    
    - portal 模块与权限机制
        
    - 仅能查看自己相关的订单、发票等
        
    - B2B/B2C 的数据隔离实践
        
3. **共享安全**
    
    - 使用 `sudo()` 的风险
        
    - env.user vs SUPERUSER_ID
        
    - 提升/降低权限的正确用法



[[安全防护]]