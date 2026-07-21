---
title: Express 框架
type: concept
tags: [cs, web, backend, mature]
sources: [raw/计算机/开发学习/语言/Node JS/03-框架应用/]
created: 2026-05-05
updated: 2026-05-05
summary: Express 是 TJ Holowaychuk 2010 年创建的极简 Node.js Web 框架,以中间件管道为核心设计模式,生态延续 15 年仍是 Node 后端最广泛的基础。
---

# Express 框架

## 定义

**Express.js** 是 TJ Holowaychuk 2010 年开源、目前由 OpenJS 基金会托管的 [[Node.js]] Web 框架。它的设计哲学是**最小核心 + 中间件组合**:框架本身只提供路由、请求/响应封装,其他功能(身份验证、日志、解析、压缩)通过中间件拼接。Express 是 Node 生态最广泛的 Web 框架,数百万项目的基础,npm 周下载量超 3000 万,是 MEAN / MERN 全栈技术栈中的 "E"。

## 核心要点

### 1. 极简 Hello World

```js
import express from 'express';
const app = express();
app.get('/', (req, res) => res.send('Hello'));
app.listen(3000);
```

### 2. 中间件管道

```js
app.use(express.json());                        // 解析 JSON body
app.use((req, res, next) => { console.log(req.url); next(); });
app.use('/api', authMiddleware, apiRouter);     // 路由级中间件
app.use((err, req, res, next) => { ... });      // 错误处理
```

每个请求依次经过 `(req, res, next)` 函数,调用 `next()` 传递,出错传 `next(err)`。这是 Express 唯一的核心抽象,但极强大。

### 3. 路由

```js
app.get('/users/:id', (req, res) => res.json(...));
app.post('/users', (req, res) => ...);
const router = express.Router();
router.get('/me', ...);
app.use('/api', router);
```

支持参数、通配符、链式 `.get().post()`、子路由器组合。

### 4. 模板引擎

```js
app.set('view engine', 'pug');
app.get('/', (req, res) => res.render('index', { title: 'X' }));
```

支持 Pug、EJS、Handlebars 等,但现代多用 [[SSR]] 框架取代。

### 5. 生态中间件

- **morgan**:HTTP 日志
- **helmet**:安全头
- **cors**:[[CORS跨域资源共享]]
- **cookie-parser**、**express-session**:[[Cookie与Session]]
- **passport**:认证策略
- **multer**:文件上传
- **express-rate-limit**:限流
- **compression**:gzip

### 6. 与同类对比

| 框架 | 特点 |
|---|---|
| **Express** | 老牌、生态最大、API 稳定 |
| **Koa**(同 TJ 作者) | async/await 原生、更小核心 |
| **Fastify** | 性能优、JSON Schema 校验 |
| **NestJS** | TypeScript + DI + 装饰器,类 Spring/Angular |
| **Hono** | Web 标准 API、Edge 可跑、轻量 |
| **Hapi** | 配置驱动,企业风 |

近年新项目流向 Fastify、Hono、NestJS,但 Express 兼容包仍最广。

### 7. Express 5(2024)

经过 10 年漫长 beta,2024 年 5.0 正式发布:

- 原生 async/await 错误冒泡(无需 try/catch + next(err))
- ES Module 完全支持
- Promise-based 中间件
- 移除部分历史 API

### 8. 何时用?

- 需要极广中间件生态
- 团队已熟悉
- 已有 Express 老代码
- 简单 REST API 快速搭建

何时不用?

- 高并发性能极致(Fastify、Hono 更快)
- 类型/DI 强需求(NestJS)
- 边缘部署(Hono)

### 9. 局限

- 性能:每请求中间件链遍历,~50K req/s,Fastify 可 100K+
- 类型:虽有 @types/express,但中间件链类型推断弱
- 错误处理仍需注意(5.0 改善)

## 关系

- 运行时:[[Node.js]]
- 模式:中间件链(责任链 [[设计模式]])
- 替代:Koa、Fastify、Hono、[[NestJS]]
- 配合:[[RESTful API]]、[[GraphQL]] 服务实现
- 部署:Docker / PM2 / Serverless

## 参考源

- raw/计算机/开发学习/语言/Node JS/03-框架应用/
