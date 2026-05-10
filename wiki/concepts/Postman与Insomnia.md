---
title: Postman 与 Insomnia(API 客户端)
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Postman 是 API 开发与测试领域的事实标准客户端,Insomnia 是开源轻量替代;二者从简单 HTTP 请求工具进化为 API 全生命周期管理(设计、测试、监控、文档、Mock),配套 OpenAPI 生态。
---

# Postman 与 Insomnia(API 客户端)

## 定义

**Postman** 是 Abhinav Asthana 在 2012 年从印度初创起步的 API 开发客户端,最初是 Chrome 扩展,后独立桌面 App,2024 年用户超 3000 万,成为 API 开发事实标准。

**Insomnia** 是 Gregory Schier 在 2014 年发布的开源 API 客户端,2019 年被 Kong(API 网关公司)收购,定位 Postman 的"轻量、开发者优先"替代。

二者从"简单的 HTTP 请求工具"进化为 API 全生命周期管理平台,涵盖设计、Mock、测试、监控、文档、协作。

## 核心功能

**1. HTTP 请求构造**

- Method(GET / POST / PUT / DELETE / PATCH 等)
- Headers
- Query Params
- Body(JSON / XML / Form / Multipart / Binary)
- Authorization(Basic / Bearer / OAuth / API Key)
- Pre-request Script、Tests(JS 脚本)

**2. Collection(集合)**

把相关请求组织为集合,可分文件夹、加变量、设环境。

```
My API Collection
├── Auth
│   ├── Login
│   └── Refresh Token
├── Users
│   ├── List Users
│   ├── Get User
│   └── Create User
└── Orders
    └── ...
```

**3. Environment(环境)**

变量集合,切换 dev / staging / prod:
- baseUrl: https://api.dev.example.com / https://api.example.com
- token: <env-specific>

请求中用 `{{baseUrl}}/users` 引用。

**4. Variables Hierarchy**

- Global → Collection → Environment → Local
- 后定义覆盖前

**5. Scripting(测试 / 自动化)**

```javascript
// Pre-request:请求发送前
pm.environment.set("timestamp", Date.now())

// Tests:响应到达后
pm.test("Status code is 200", () => {
  pm.response.to.have.status(200)
})
pm.test("Response has user", () => {
  const json = pm.response.json()
  pm.expect(json.user).to.exist
  pm.environment.set("userId", json.user.id)  // 存到环境
})
```

复杂测试场景:登录获 token → 后续请求带 token → 退出。

**6. Runner(批量运行)**

把整个集合按顺序跑,生成报告。CI 集成时用 newman(Postman CLI)。

**7. Mock Server**

定义示例响应,Postman 自动暴露 URL。前后端可解耦开发。

**8. API 文档**

集合自动生成网页文档,可分享 / 公开。

**9. 监控(Monitor)**

定时跑集合,失败告警,可作为 [[Sentry]] 之外的"端到端 API 监控"。

**10. 协作**

- Workspace(共享)
- Comment、Version Control(类 Git)
- 团队配额

## 与 OpenAPI 集成

OpenAPI(原 Swagger)是 API 描述标准。Postman 支持:
- 导入 OpenAPI YAML/JSON 自动生成集合
- 从集合导出 OpenAPI
- 自动同步(Postman 与 GitHub OpenAPI 仓库)

这是 API-First 工作流的核心。

## Postman vs Insomnia

| 维度 | Postman | Insomnia |
|---|---|---|
| 开源 | 否(商业) | 部分(Insomnia Core 免费) |
| 价格 | 免费层 + Pro/Enterprise | 免费 + Plus/Team |
| 团队协作 | 强 | 中 |
| 性能 | Electron,内存大 | 略轻 |
| Cloud Sync | 默认开 | 可关 |
| GraphQL | 支持 | 强 |
| gRPC | 支持 | 支持 |
| WebSocket | 支持 | 支持 |
| Plugin 生态 | 大 | 中 |
| Git 同步 | Pro+ | 免费(原生) |
| 隐私敏感 | 数据上云 | 可本地 |

**选择**

- 团队协作 / 大型企业:Postman
- 个人开发者 / 隐私敏感:Insomnia
- 完全开源需求:HTTPie / Bruno / 自建

## 替代方案兴起

**Bruno(2023+)**

- 完全开源 + 本地存储
- 无需登录
- 文件存仓库(.bru 格式),Git 友好
- 反"云锁定"运动产物

Postman 2023 年强制云同步引发开发者反弹,Bruno 趁机崛起,GitHub Star 短期破 2 万。

**Hoppscotch(原 Postwoman)**

Web 版开源,无需安装。

**Thunder Client**

[[VS Code编辑器]] 插件,在 IDE 内做 API 测试。

**HTTPie**

CLI 工具,适合脚本化:
```bash
http POST api.example.com/users name=alice age:=30
```

## 在工作流中的位置

**1. API 设计阶段**

- OpenAPI 编辑(Stoplight / Swagger Editor)
- 导入 Postman 验证
- Mock Server 让前端先动手

**2. 开发阶段**

- 调试本地 API
- 切换 dev / staging
- 共享 collection

**3. 测试阶段**

- Postman Tests + newman 跑 CI
- 集成 / E2E 验证

**4. 文档阶段**

- 自动文档分享给消费方
- 与 GitBook / Docusaurus 互补

**5. 监控阶段**

- 定时调关键端点
- 端到端可用性指标

## 与浏览器 DevTools / curl 对比

**curl**

- CLI 万能,脚本友好
- 但管理大量请求不便

**DevTools Network**

- 看请求,但难重放、难修改、难保存

**Postman / Insomnia**

- 持久化、组织、协作
- 适合 API 集成开发场景

各有定位,工程师常多工具并用。

## 高级功能

**1. OAuth 2.0 流程**

Postman 内置完整流程:
- Auth Code、Implicit、Client Credentials、PKCE
- 重定向 URI 自动捕获
- 一键获取 access token,后续请求自动带

**2. 链式请求**

测试脚本中:
```javascript
pm.environment.set("token", pm.response.json().token)
pm.sendRequest({...}, (err, res) => { /* 后续逻辑 */ })
```

**3. 数据驱动测试**

CSV / JSON 数据文件,Runner 按行跑同一请求(不同参数),适合穷举测试。

**4. SSL Certificates**

mTLS 场景,加客户端证书。

**5. Postman Flows**

可视化编排多请求(2023+),类 Zapier 但 API 专用。

## 安全实践

- Token 别进 collection(用 Environment 变量)
- 不要把 Production Token 放 Personal Workspace 团队共享
- 敏感请求 Mock,真实数据本地测
- Webhook URL 别公开
- Public collection 检查不暴露密钥

## 局限

- **数据上云风险**:Postman 默认云同步,密钥泄露事故有过
- **Electron 性能**:大 collection 卡顿
- **学习曲线**:复杂功能(Flows、Scripting)非新手即用
- **价格**:Pro 起 $14/用户/月
- **Plugins 不及 IDE**:扩展性弱

## CI/CD 集成

```yaml
# GitHub Actions
- run: |
    npm i -g newman
    newman run postman_collection.json --environment dev.json --reporters cli,html
```

newman 是 Postman 的 CLI runner,支持 collection.json 直接跑。结合 [[CI_CD流水线]] 实现"每次 PR 自动跑契约测试"。

## 和其他概念的关系

Postman / Insomnia 是 [[RESTful API]]、[[GraphQL]]、gRPC 等接口开发的核心工具,与 OpenAPI、Swagger 规范紧密互通。它们在 [[微服务]] 开发中减少跨团队协作摩擦——后端先发布 API,前端用 Postman 探索调试。

Mock Server 功能是 [[BFF]] / [[Strangler Fig模式]] 等渐进开发模式的辅助——新接口未就绪时前端用 Mock 推进。监控功能与 [[Sentry]]、[[Grafana]]、[[可观测性三支柱]] 互补。

它的"集合 + 环境 + 脚本"模型与 [[CI_CD流水线]]、[[Apache Airflow]] 中的"任务 + 配置 + 钩子"思想同构——都是把人类可读流程编码为可执行、可版本化资产。

## 参考源

- raw/计算机/
- 相关:[[RESTful API]]、[[GraphQL]]、[[CI_CD流水线]]
