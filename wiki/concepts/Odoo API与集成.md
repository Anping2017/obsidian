---
title: Odoo API 与集成
type: concept
tags: [erp, mature]
sources: [raw/Odoo/03-应用实践层/04-集成扩展/API接口开发.md, raw/Odoo/03-应用实践层/04-集成扩展/Webhooks与消息队列.md, raw/Odoo/03-应用实践层/04-集成扩展/第三方系统集成.md]
created: 2026-05-05
updated: 2026-05-05
summary: Odoo 提供 XML-RPC、JSON-RPC、REST(自建)三种 API,结合 webhook 触发与消息队列,可与电商、物流、银行、CRM 等外部系统集成。
---

# Odoo API 与集成

## 定义

Odoo API 是把 [[Odoo ORM]] 暴露给外部系统的接口层。Odoo 没有像 Salesforce 那样统一的 REST API,而是同时支持 **XML-RPC、JSON-RPC、自定义 HTTP 控制器(REST)**,各有适用场景。集成能力决定 Odoo 在企业 IT 架构中的位置。

## 核心要点

### 三种 API 协议

| 协议 | 端点 | 适用 |
|---|---|---|
| XML-RPC | `/xmlrpc/2/common`, `/xmlrpc/2/object` | 旧式但稳定,Python `xmlrpc.client` 直接用 |
| JSON-RPC | `/jsonrpc` 或 `/web/dataset/call_kw` | Web 客户端原生用,JS 友好 |
| REST(自建) | `/api/v1/...` | 通过 `http.Controller` 自定义 |

XML-RPC 是历史最久、文档最全的方案;JSON-RPC 是现代客户端优选;真正的 RESTful 需要自建 controller,社区有 `base_rest` 等模块辅助。

### XML-RPC 调用示例

```python
import xmlrpc.client

url = 'https://mycompany.odoo.com'
db = 'mydb'
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, 'admin', 'pass', {})

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
partner_ids = models.execute_kw(db, uid, 'pass',
    'res.partner', 'search', [[['is_company','=',True]]], {'limit':10})
partners = models.execute_kw(db, uid, 'pass',
    'res.partner', 'read', [partner_ids], {'fields':['name','email']})
```

凡是 ORM 方法(search/read/create/write/unlink/方法调用)都能通过 RPC 调用,**前提是用户有对应权限**(走 [[Odoo安全模型]])。

### REST 控制器

```python
class ApiController(http.Controller):
    @http.route('/api/v1/partners', type='json', auth='user', methods=['GET'])
    def get_partners(self, **kw):
        partners = request.env['res.partner'].search([], limit=20)
        return [{'id': p.id, 'name': p.name} for p in partners]
```

`auth='user'` 要求登录态;`auth='public'` 允许匿名;`csrf=False` 用于无 cookie 的纯 API。

### Webhook(出方向)

Odoo 内置自动化规则可在记录变化时调用 HTTP webhook:
- 配置 `base.automation` → "执行 Python 代码" → `requests.post(...)`
- 或安装 OCA `webhook` 模块用配置式声明

### 消息队列

社区版无内建队列,但通过 `queue_job` 模块(OCA)可把耗时任务异步化,支持失败重试、并发控制。企业版的某些 EDI/集成模块也内建队列。

### 典型集成场景

- **电商**:Shopify、Magento、WooCommerce 双向同步订单/库存(`shopify_bridge`、`connector_woocommerce`)
- **物流**:DHL、FedEx、UPS、顺丰打单与轨迹(`delivery_*` 模块)
- **支付**:支付宝、微信、Stripe、PayPal(`payment_*` 模块)
- **银行对账**:CAMT.053、MT940、BAI2 文件导入
- **EDI**:Peppol、电子发票格式(欧盟法规驱动)
- **BI**:导出到 Metabase、Superset、Power BI

### 性能注意

RPC 每次调用都走完整 Odoo 请求栈(认证、权限、ORM、序列化),批量场景下务必用 `create([{...}, {...}, ...])` 而非循环单条插入,差距可达数十倍。

## 关系

- 调用 [[Odoo ORM]] 方法
- 受 [[Odoo安全模型]] 强制鉴权
- 配合 [[Odoo工作流]] 实现"外部系统触发内部流程"

## 参考源

- raw/Odoo/03-应用实践层/04-集成扩展/API接口开发.md
- raw/Odoo/03-应用实践层/04-集成扩展/Webhooks与消息队列.md
- raw/Odoo/03-应用实践层/04-集成扩展/第三方系统集成.md
