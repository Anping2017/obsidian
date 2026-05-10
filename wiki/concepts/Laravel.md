---
title: Laravel
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Laravel 是 Taylor Otwell 在 2011 年创立的 PHP 全栈 Web 框架,以优雅 API、ActiveRecord ORM(Eloquent)、Artisan CLI、丰富生态(Forge/Vapor/Nova)成为 PHP 现代开发的事实标准,把 PHP "一无是处"的刻板印象彻底翻盘。
---

# Laravel

## 定义

**Laravel** 是 Taylor Otwell 在 2011 年发布的 PHP Web 应用框架。它借鉴 Ruby on Rails 的"约定优于配置"哲学,把 PHP 从 WordPress 时代的散乱脚本拉到现代 Web 框架水平——MVC 分层、ORM、迁移、队列、广播、邮件、调度等开箱即用,加上简洁优雅的 Fluent API,成为 PHP 生态再度复兴的核心引擎。

Laravel 与 Symfony 共同构成 PHP 现代框架双雄,但 Laravel 偏开发者体验,Symfony 偏组件解耦,二者底层有交叉(Laravel 大量使用 Symfony Components)。

## 核心特性

**Eloquent ORM**

ActiveRecord 模式实现:
- 模型即数据表,$user->save() 即写库
- 关系定义直观(hasMany、belongsTo、morphTo)
- 内置软删除、时间戳、作用域(Scope)
- 与 Laravel 的迁移、Seeder 紧密集成

**Artisan CLI**

PHP 写的命令行工具:
- php artisan make:model、make:controller 自动生成代码
- migrate / migrate:rollback 数据库版本管理
- queue:work 启动队列消费者
- 自定义命令 extends Command

**Blade 模板引擎**

简洁语法 @if、@foreach、@yield、@section,编译为纯 PHP,性能与可读性兼顾。组件化(Blade Components)对标 Vue 单文件组件思路。

**路由系统**

Route::get('/users/{id}', [UserController::class, 'show']) 链式声明,支持中间件、命名路由、组前缀、子域名。RESTful 资源路由 Route::resource() 一行生成 7 个端点。

**中间件(Middleware)**

类似 Express:
- 全局中间件(CORS、CSRF)
- 路由中间件(Auth、Throttle)
- 控制器构造器中间件
- 与 [[Web安全]] 默认对接

**队列与广播**

- Queue:支持 Redis、SQS、Beanstalkd、数据库等驱动,异步执行 Job
- Broadcasting:配合 Pusher、Soketi 实现实时通信([[WebSocket]])

## Laravel 生态

**官方扩展**

- **Forge**:服务器一键管理(SSH、部署、SSL)
- **Envoyer**:零停机部署
- **Vapor**:Serverless on AWS Lambda
- **Nova**:管理后台生成器(付费)
- **Cashier**:Stripe/Paddle 订阅集成
- **Sanctum**:轻量 API 认证(Token + SPA)
- **Passport**:完整 OAuth 2.0 服务端
- **Horizon**:队列监控面板
- **Telescope**:开发期调试面板

**社区生态**

- Spatie 系列:权限、备份、媒体库等高质量包
- Filament:现代 Admin Panel(开源对标 Nova)
- Livewire:全栈反应式 UI(类似 Phoenix LiveView)
- Inertia.js:Laravel + React/Vue 单页应用

## 版本演进与 LTS

- 5.x 时代(2015-2018):奠定现代格局
- 6.x(2019)起首个 LTS
- 8.x(2020):Jetstream 启动套件
- 9.x(2022):PHP 8 类型支持
- 10.x、11.x(2023-2024):简化结构
- 12.x(2025):AI 时代调整,与 Vite 5 / Vue 3 / React 19 同步

近年发布周期改为每年一个主版本 + 18 个月 LTS。

## 适用场景

**最适合**

- 中小型 SaaS 产品
- 内容管理类网站(博客、电商)
- 内部管理系统(配 Filament/Nova)
- 创业 MVP
- 含管理后台的多租户系统

**不太适合**

- 极高并发实时系统(PHP 模型限制)
- 资源敏感的 [[微服务]](Java/Go 更适合)
- 计算密集型任务(Python AI / Go 数值库更强)

## 与 Rails / Django / Spring Boot 对比

| 维度 | Laravel | Rails | Django | Spring Boot |
|---|---|---|---|---|
| 语言 | PHP | Ruby | Python | Java |
| ORM | Eloquent (AR) | ActiveRecord | Django ORM | JPA/Hibernate |
| 哲学 | 优雅 + DX | 程序员幸福 | Batteries Included | 企业稳健 |
| 异步 | 弱(队列) | 弱 | 渐进 | 强 |
| 性能 | 中 | 中 | 中 | 高 |
| 部署 | 共享主机友好 | Capistrano/Heroku | uwsgi/gunicorn | jar/war |
| 学习曲线 | 低-中 | 中 | 低 | 中-高 |

## 性能与扩展

**优化手段**

- OPcache + JIT(PHP 8+)
- Redis 缓存([[缓存]] 模式)
- 队列异步化重任务
- Octane(基于 Swoole/RoadRunner 的常驻进程)
- Vapor(Serverless)
- 数据库读写分离([[读写分离]])
- CDN 静态资源([[CDN]])

**Laravel Octane** 是性能跃迁的关键——传统 PHP 每次请求重启进程,Octane 让 Laravel 应用常驻内存,QPS 提升 10 倍以上,达到 Java/Node 同级别。

## 局限

- PHP 语言历史包袱(类型系统晚到、并发模型弱)
- Eloquent N+1 查询陷阱
- 框架"魔法"较多,排错有挑战
- 异步生态不及 Node.js / FastAPI
- 大规模微服务下不如 JVM/Go

## 和其他概念的关系

Laravel 在 PHP 生态扮演的角色等同 [[Spring Boot]] 之于 Java、[[Django框架]] 之于 Python、Rails 之于 Ruby。它的 Eloquent 与 [[关系型数据库]] 紧密耦合,队列系统对接 [[消息队列]],认证模块涉及 [[JWT]]、[[OAuth 2.0]]、[[Cookie与Session]]。

Laravel 的"全栈"特征(Blade + Livewire + Inertia)让它在 [[微服务]] 时代仍能竞争——单一团队用 Laravel 加少量前端即可交付完整产品。它的 [[设计模式]] 大量运用([[设计模式]] 中的服务容器、Facade、依赖注入),是学习企业级 PHP 的最佳样板。

## 参考源

- raw/计算机/
- 相关:[[Django框架]]、[[Spring Boot]]、[[Express]]
