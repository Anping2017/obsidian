---
title: Express
type: concept
tags: [cs, web, backend, stub]
sources:
  - raw/计算机/Web前端/
created: 2026-05-05
updated: 2026-05-05
summary: Express 是 Node.js 生态最成熟、最简单的 Web 后端框架,以中间件链式处理 HTTP 请求为核心,是 Koa、Fastify、NestJS 等众多框架的灵感来源。
---

# Express

## 定义

Express(Express.js)是 **基于 [[Node.js]] 的极简、灵活、广泛使用的 Web 应用框架**。由 TJ Holowaychuk 在 2010 年发布,至今仍是 Node.js 后端最流行的框架之一,周下载量过 3000 万。

它的核心定位:**比原生 `http` 模块易用,比大型框架轻量**。Express 不强制目录结构、不内置 ORM 或模板引擎,而是通过**中间件机制**让开发者按需组装。

(与 [[Express框架]] 同一概念)

## 核心要点

### 最小示例

```javascript
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello World');
});

app.listen(3000);
```

### 中间件机制

中间件是 Express 的灵魂——一个函数 `(req, res, next) => {}`,通过调用 `next()` 决定是否继续传递。请求依序经过中间件链,每个可读取/修改 req/res 或终结响应。

```javascript
app.use(express.json());                    // 解析 JSON body
app.use(express.static('public'));          // 静态文件服务
app.use((req, res, next) => {               // 自定义日志中间件
  console.log(req.method, req.url);
  next();
});
app.use((err, req, res, next) => {          // 错误处理中间件(4 个参数)
  res.status(500).send(err.message);
});
```

### 路由

```javascript
app.get('/users/:id', (req, res) => {
  res.json({ id: req.params.id });
});

const router = express.Router();
router.post('/', createUser);
router.delete('/:id', deleteUser);
app.use('/api/users', router);
```

### 生态

- **模板引擎**:EJS、Pug、Handlebars(也可不用)
- **ORM/ODM**:Sequelize、TypeORM、Prisma、Mongoose
- **认证**:Passport.js
- **校验**:express-validator、Joi、Zod
- **测试**:Supertest + Jest

### 与同类对比

| 框架 | 特征 |
|---|---|
| Express | 极简,中间件,事实标准 |
| Koa | TJ 同人作,基于 async/await,更现代但生态较小 |
| Fastify | 性能优先,JSON Schema 验证,Plugin 体系 |
| Hapi | 配置驱动,企业级特性丰富 |
| [[NestJS]] | 强约定,基于 TypeScript + 装饰器,内置 IoC |

### 何时不用 Express

- 需要全栈框架(SSR + API):用 [[Next.js]]、[[Nuxt]]、Remix
- 强类型与企业级架构:用 NestJS
- 极致性能与 schema 校验:用 Fastify
- Edge 部署:用 Hono、itty-router

## 和其他概念的关系

Express 是 [[Node.js]] 后端开发的事实入门标准,几乎所有 Node 教程都以它为起点。它定义了「中间件链」编程模型,深远影响了后续 [[Koa]]、[[Fastify]]、[[NestJS]] 乃至 Python 的 Flask、Go 的 chi 等。

它与 [[RESTful API|REST API]] 设计紧密结合,是 [[微服务]] 时代后端服务的常见技术栈。MEAN/MERN 全栈中 Express 是 N(后端)。

虽然 Express 本身不强制结构,但社区有成熟的最佳实践——分层架构(Controller / Service / Repository),与 [[依赖倒置]]、[[整洁代码|整洁架构]] 兼容。

[[Vercel]]、[[Cloudflare Workers]] 等 [[Serverless]] 平台都支持 Express 风格的代码,虽然边缘运行时常需更轻量替代品。

## 参考源

- raw/计算机/Web前端/
- Express 官方文档 https://expressjs.com/
- TJ Holowaychuk 早期博客
