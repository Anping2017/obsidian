## 1) ACL 文件结构

### 1.1 放置位置

- 路径固定：`your_module/security/ir.model.access.csv`
    
- 在 `__manifest__.py` 的 `data` 中加载（见下文）。
    

### 1.2 CSV 基本列（顺序固定）

```
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink

```

- **id**：本条 ACL 的外部 ID（唯一）。
    
- **name**：描述性名称（任意）。
    
- **model_id:id**：模型 External ID，一般是 `model_<python类名下划线>`  
    例：模型 `my.device.order` → `model_my_device_order`
    
- **group_id:id**：赋权的用户组 External ID（可空=对“所有用户”生效）。
    
- **perm_***：四项基本权限（`0`/`1`）。
    

> ⚠️ `group_id` 为空时，权限将授予**所有用户**（包括门户/公共用户不一定，因为他们通常无菜单与记录规则会限制，但要小心）


### 1.3 四个基本权限

- `perm_read`：读
    
- `perm_write`：写
    
- `perm_create`：新建
    
- `perm_unlink`：删除
    

> 只给需要的最小权限，删除权限尤其谨慎。


## 2) 为不同用户组配置 ACL（示例全集）

### 2.1 定义用户组（可选，若用系统已有组可跳过）

`security/groups.xml`


```xml
<odoo>
  <data>
    <!-- 业务员 -->
    <record id="group_my_sales_user" model="res.groups">
      <field name="name">My Sales User</field>
      <field name="category_id" ref="base.module_category_sales_management"/>
    </record>

    <!-- 经理 -->
    <record id="group_my_sales_manager" model="res.groups">
      <field name="name">My Sales Manager</field>
      <field name="implied_ids" eval="[(4, ref('your_module.group_my_sales_user'))]"/>
      <field name="category_id" ref="base.module_category_sales_management"/>
    </record>
  </data>
</odoo>

```


### 2.2 ACL 文件：`security/ir.model.access.csv`

（假设新模型是 `my.device.order`）

```
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_device_order_user,My Device Order - User,model_my_device_order,your_module.group_my_sales_user,1,1,1,0
access_my_device_order_manager,My Device Order - Manager,model_my_device_order,your_module.group_my_sales_manager,1,1,1,1
```


### 2.3 在 `__manifest__.py` 中加载

```
'data': [
    'security/groups.xml',
    'security/ir.model.access.csv',
    # 视图、菜单等...
],

```


## 常见坑与最佳实践

1. **忘记配置 ACL**
    

- 超级管理员测试一切正常，但普通用户报“权限不足”。
    
- 解决：先给最小 ACL，再逐步加严格的记录规则。
    

2. **ACL 与记录规则的职责边界**
    

- **能否做 CRUD** → ACL 决定；
    
- **能看到哪些行** → 记录规则决定。
    
- 条件化写/删（如仅草稿可删）可用记录规则的 `perm_unlink/perm_write` + `domain_force`。
    

3. **group_id 为空的风险**
    

- 等于“所有用户”都有这条 ACL。除非你明确需要，否则避免在关键业务模型上留空组。
    

4. **门户/公共用户**
    

- 一般不直接授予业务模型 ACL，门户的可见性更多靠 Portal 相关模块、专门的控制器与记录规则。
    
- 若确需门户访问，**单独建一条只读 ACL + 严格的记录规则**。
    

5. **多公司模型**
    

- ACL 不分公司；公司隔离靠记录规则域：  
    `['|', ('company_id','=',False), ('company_id','in', company_ids)]`
    

6. **测试方法**
    
```
env['my.device.order'].with_user(user).check_access_rights('write', raise_exception=True)
env['my.device.order'].with_user(user).check_access_rule('read')

```

- 对比 `with_user(user)` 与 `sudo()` 的差异，快速定位是 ACL 还是记录规则问题。
    

7. **删除权限慎给**
    

- 业务上更常见的是“归档”而不是“删除”。能否删建议只留给经理/管理员。