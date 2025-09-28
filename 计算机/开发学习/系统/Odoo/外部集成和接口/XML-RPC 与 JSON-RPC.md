# 🌐 Odoo 外部接口：XML-RPC 与 JSON-RPC

---

## 1. 核心概念

- Odoo 提供 **远程过程调用（RPC）接口**，允许外部系统访问 Odoo 的 ORM 数据和方法
    
- 两种主要方式：
    
    1. **XML-RPC**：基于 XML 的 RPC 协议，兼容性好，跨语言支持广
        
    2. **JSON-RPC**：基于 JSON 的 RPC 协议，现代 Web 系统更友好，支持 HTTP POST
        
- **常见用途**：
    
    - 创建/更新/删除记录
        
    - 查询记录
        
    - 调用自定义方法
        
    - 与第三方系统（CRM、ERP、移动应用）集成
        

---

## 2. 连接 Odoo

### 2.1 连接参数

|参数|说明|
|---|---|
|`url`|Odoo 服务器 URL（如 [http://localhost:8069）](http://localhost:8069%EF%BC%89)|
|`db`|数据库名称|
|`username`|登录用户名|
|`password`|登录密码|

---

## 3. XML-RPC 使用示例

### 3.1 导入库

`import xmlrpc.client`

### 3.2 登录

```
url = 'http://localhost:8069'
db = 'odoo_db'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

```

### 3.3 调用对象方法

```
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# 搜索客户记录
partner_ids = models.execute_kw(db, uid, password,
    'res.partner', 'search',
    [[['is_company', '=', True]]])

# 读取字段
partners = models.execute_kw(db, uid, password,
    'res.partner', 'read',
    [partner_ids], {'fields': ['name', 'email']})

# 创建记录
new_partner_id = models.execute_kw(db, uid, password,
    'res.partner', 'create',
    [{'name': 'New Customer', 'email': 'customer@example.com'}])

```

---

## 4. JSON-RPC 使用示例

### 4.1 导入库

`import requests 
`import json`

### 4.2 登录

```
url = 'http://localhost:8069/jsonrpc'
db = 'odoo_db'
username = 'admin'
password = 'admin'

payload = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "service": "common",
        "method": "login",
        "args": [db, username, password]
    },
    "id": 1
}
response = requests.post(url, json=payload).json()
uid = response['result']

```

### 4.3 调用对象方法

```
payload = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "service": "object",
        "method": "execute_kw",
        "args": [
            db, uid, password,
            'res.partner', 'search_read',
            [[['is_company', '=', True]]],
            {'fields': ['name', 'email']}
        ]
    },
    "id": 2
}
response = requests.post(url, json=payload).json()
partners = response['result']

```

---

## 5. 主要区别

|特性|XML-RPC|JSON-RPC|
|---|---|---|
|数据格式|XML|JSON|
|现代 Web 支持|较旧|原生支持 JS/HTTP|
|可读性|较复杂|清晰、轻量|
|调用方式|`xmlrpc.client`|`requests`/`fetch`|
|跨语言|✅|✅|

---

## 6. 实际应用场景

1. **第三方 CRM 同步客户数据**
    
2. **移动应用查询和创建订单**
    
3. **定时脚本导入外部系统数据**
    
4. **ERP 系统集成**（财务、库存、采购）
    
5. **Web 应用通过 API 调用 Odoo 方法**
    

---

## 7. 注意事项

- 用户权限：API 调用遵循 Odoo 权限规则
    
- 性能：批量操作建议使用 `search_read` 避免循环查询
    
- 安全：建议使用 HTTPS 和 API key /密码加密
    
- JSON-RPC 更适合现代 Web 应用，XML-RPC 更适合跨语言脚本
    

---

## 8. 总结

- **XML-RPC / JSON-RPC** 是 Odoo 对外提供的远程调用接口
    
- 核心流程：
    
    1. 登录认证（获取 `uid`）
        
    2. 调用对象方法（CRUD 或自定义方法）
        
    3. 处理返回数据
        
- JSON-RPC 适合现代 Web/HTTP 调用，XML-RPC 适合传统脚本和跨语言支持
    
- 可用于第三方系统集成、移动应用开发、定时数据同步等