# 🌐 Odoo 自定义 RESTful API 接口

---

## 1. 核心概念

- **RESTful API** 是基于 HTTP 协议的接口风格，用于与外部系统通信
    
- 在 Odoo 中可以通过 **Controller + HTTP route** 创建自定义接口
    
- 特性：
    
    1. 使用 HTTP 方法：`GET`, `POST`, `PUT`, `DELETE`
        
    2. 接收 JSON 数据，返回 JSON 数据
        
    3. 可以访问 Odoo ORM，实现 CRUD 操作
        

---

## 2. 基本结构

1. **Controller 类**：继承 `http.Controller`
    
2. **路由定义**：使用 `@http.route()` 装饰器
    
3. **方法参数**：`**kwargs` 或 `request.jsonrequest`
    
4. **返回数据**：使用 `json.dumps()` 或 `request.make_response()`
    

---

## 3. 示例：创建客户 API

### 3.1 导入依赖

`from odoo import http from odoo.http import request import json`

### 3.2 Controller 定义

```
class CustomerController(http.Controller):

    @http.route('/api/customers', type='json', auth='user', methods=['POST'], csrf=False)
    def create_customer(self, **kwargs):
        """
        POST /api/customers
        JSON body: {"name": "John Doe", "email": "john@example.com"}
        """
        name = kwargs.get('name')
        email = kwargs.get('email')

        if not name or not email:
            return {"status": "error", "message": "Missing name or email"}

        # 创建客户记录
        customer = request.env['res.partner'].sudo().create({
            'name': name,
            'email': email,
            'is_company': False
        })
        return {"status": "success", "id": customer.id, "name": customer.name}

```

---

## 4. 路由参数说明

|参数|说明|
|---|---|
|`/api/customers`|API URL 路径|
|`type='json'`|自动解析请求 JSON，返回 JSON|
|`auth='user'` / `'public'`|认证方式（user = 登录用户，public = 不需登录）|
|`methods=['POST']`|支持的 HTTP 方法|
|`csrf=False`|关闭 CSRF 校验（外部系统调用必需）|

---

## 5. 获取请求数据方式

1. **JSON body**（推荐）
    

`data = request.jsonrequest  # dict name = data.get('name')`

2. **URL 参数**
    

`@http.route('/api/customers', type='http', auth='user') def get_customer(self, **kwargs):     customer_id = kwargs.get('id')`

---

## 6. 返回数据

- **JSON 格式**
    

`return {"status": "success", "id": customer.id, "name": customer.name}`

- **自定义响应**
    

```
return request.make_response(
    json.dumps({"status": "success"}),
    headers=[('Content-Type', 'application/json')]
)

```

---

## 7. 高级用法

### 7.1 CRUD 操作示例

|HTTP 方法|ORM 操作|示例 URL|
|---|---|---|
|GET|search / read|`/api/customers?id=1`|
|POST|create|`/api/customers`|
|PUT|write|`/api/customers/1`|
|DELETE|unlink|`/api/customers/1`|

### 7.2 使用 `sudo()` 控制权限

`request.env['res.partner'].sudo().create({...})`

- 绕过当前用户权限，常用于 API 服务调用
    

### 7.3 结合 JSON-RPC / OAuth

- 可为 API 添加 Token 或 OAuth2 认证
    
- 适用于开放接口或第三方系统集成
    

---

## 8. 实际应用场景

1. 移动端 App 数据同步（创建、读取、更新客户）
    
2. 第三方系统数据导入（订单、产品、库存）
    
3. 内部系统调用 Odoo 服务（定时任务或 Webhook）
    
4. 对外提供 API 服务（B2B 或合作伙伴接口）
    

---

## 9. 注意事项

- **安全性**：
    
    - 建议使用 `auth='user'` + Token 或 OAuth2
        
    - 避免暴露敏感模型
        
- **性能**：
    
    - 批量操作建议使用 ORM 批量方法
        
    - 返回字段尽量精简
        
- **数据校验**：
    
    - 必须验证输入字段，避免数据库异常
        

---

## 10. 总结

- **创建 RESTful API 核心步骤**：
    
    1. 创建 Controller
        
    2. 定义 HTTP 路由
        
    3. 解析请求参数（JSON / URL）
        
    4. 使用 ORM 执行业务逻辑
        
    5. 返回 JSON 响应
        
- 与 XML-RPC / JSON-RPC 相比：
    
    - RESTful API 更现代，适合 Web / Mobile 调用
        
    - 支持标准 HTTP 方法，更灵活