## 1️⃣ Node.js 基础概念

| 分类        | 内容                                |
| --------- | --------------------------------- |
| **定义**    | 基于 V8 引擎的 JavaScript 运行时，用于服务器端开发 |
| **特点**    | 单线程、事件驱动、非阻塞 I/O                  |
| **安装与环境** | Node.js 安装、npm/yarn、nvm 管理版本      |
| **运行机制**  | 事件循环（Event Loop）、异步 I/O、回调函数      |
| **REPL**  | 交互式调试环境                           |

---

## 2️⃣ Node.js 核心模块

|模块|功能|
|---|---|
|**fs**|文件系统操作（读取、写入、流）|
|**path**|路径处理|
|**http / https**|创建服务器、处理请求与响应|
|**url**|URL 解析与处理|
|**querystring**|查询字符串解析|
|**events**|事件发射与监听（EventEmitter）|
|**stream**|流式数据处理|
|**os**|操作系统信息|
|**process**|进程信息、环境变量|
|**util**|工具函数（promisify 等）|

---

## 3️⃣ 异步编程

|分类|内容|
|---|---|
|**回调函数**|基础异步模式|
|**Promise**|链式调用、错误捕获|
|**async / await**|异步函数语法糖|
|**事件循环**|macro-task / micro-task、nextTick、setImmediate|
|**流式操作**|readable, writable, transform|

---

## 4️⃣ Node.js Web 开发

|分类|内容|
|---|---|
|**HTTP 服务器**|原生 http 模块、req/res 对象|
|**Express 框架**|路由、请求中间件、响应处理、静态资源|
|**Koa / Fastify**|轻量中间件、异步/await 支持|
|**REST API**|GET/POST/PUT/DELETE、JSON 数据|
|**GraphQL**|Apollo Server、schema、resolver|
|**模板引擎**|EJS、Pug、Handlebars|
|**WebSocket**|Socket.io、实时通信|

---

## 5️⃣ 数据库

|类型|内容|
|---|---|
|**关系型数据库**|MySQL, PostgreSQL, SQLite（Sequelize ORM, TypeORM）|
|**非关系型数据库**|MongoDB (Mongoose)|
|**缓存 / 消息队列**|Redis, RabbitMQ, Kafka|
|**数据库操作**|CRUD、事务、索引、连接池|

---

## 6️⃣ Node.js 工具与生态

|工具/库|功能|
|---|---|
|**npm / yarn / pnpm**|包管理、版本管理|
|**nvm**|Node 版本管理|
|**dotenv**|环境变量管理|
|**nodemon / pm2**|热更新、进程管理|
|**ESLint / Prettier**|代码规范与格式化|
|**Webpack / Rollup / Vite**|打包、构建|
|**Babel / TypeScript**|转码、类型检查|

---

## 7️⃣ 安全与性能优化

|分类|内容|
|---|---|
|**安全**|XSS、CSRF、SQL 注入、JWT、OAuth2、CORS|
|**性能优化**|异步优化、负载均衡、缓存、压缩、集群|
|**日志与监控**|winston, bunyan, morgan, PM2 monitoring|
|**单元测试 / 集成测试**|Mocha, Chai, Jest, Supertest|

---

## 8️⃣ 高级应用

|分类|内容|
|---|---|
|**微服务架构**|REST / GraphQL API、消息队列、服务注册与发现|
|**Serverless**|AWS Lambda, Azure Functions, Vercel / Netlify|
|**实时应用**|聊天、在线协作、游戏服务器|
|**CLI 工具**|自定义命令行工具开发|
|**流媒体 / 文件处理**|视频流、文件上传、图片处理|

---

## 9️⃣ 部署与运维

|分类|内容|
|---|---|
|**Web 服务器**|Nginx、Apache 反向代理|
|**容器化**|Docker, Docker Compose|
|**云服务**|AWS, GCP, Azure, Heroku, Vercel|
|**CI/CD**|GitHub Actions, GitLab CI, Jenkins|
|**日志监控**|ELK Stack, Grafana, Prometheus|