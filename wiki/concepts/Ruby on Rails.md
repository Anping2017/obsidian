---
title: Ruby on Rails
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Ruby on Rails 是 DHH 在 2004 年从 Basecamp 抽离的 Ruby Web 框架,以"约定优于配置"和"程序员幸福"为哲学,催生 Twitter、GitHub、Shopify 等 SaaS 巨头,定义了现代 Web 开发框架的基本形态。
---

# Ruby on Rails

## 定义

**Ruby on Rails(简称 Rails)** 是 David Heinemeier Hansson(DHH)在 2004 年从 Basecamp(原 37signals)项目中抽离开源的 Ruby Web 框架。它把"**约定优于配置(CoC)**"和"**不重复自己(DRY)**"两条原则推向极致,催生了 Twitter、GitHub、Shopify、Airbnb 等 SaaS 巨头的早期版本。

Rails 是现代 Web 框架的"原型机"——[[Django框架]]、[[Laravel]]、[[Spring Boot]] 都受其设计深度影响。即便今天它在新项目中份额下降,它的设计哲学仍是评判 Web 框架优劣的标尺。

## 核心特性

**Active Record ORM**

由 Martin Fowler 总结的设计模式,Rails 把它落地:
- 数据表与类一一对应
- @user.save 即数据库写入
- 关系声明式 has_many、belongs_to、has_and_belongs_to_many
- 校验、回调、Scope 与领域逻辑混合(争议点之一)

**Action Pack(MVC)**

- ActionController:控制器,继承 ApplicationController
- ActionView:模板,默认 ERB(嵌入式 Ruby)
- ActionDispatch:路由,Routes.rb 定义

**Convention over Configuration**

- 命名约定:UsersController + users 表 + User 模型 + users_controller_test.rb
- 目录结构固定:app/models、app/controllers、app/views
- 一致性减少决策疲劳,新人上手快

**Migration(数据库迁移)**

- rails generate migration AddNameToUsers name:string
- 版本化数据库变更,与代码协同部署
- 几乎所有现代框架(Django、Laravel、Spring Boot)都模仿了这一设计

**Asset Pipeline / Webpacker / Importmap**

前端资源打包方案演进:
- Sprockets(经典)
- Webpacker(Rails 6 加 Webpack)
- Importmap + Hotwire(Rails 7,无打包,浏览器原生 ES Modules)

**Action Cable**

[[WebSocket]] 集成,实时通信。

**Active Job**

队列抽象层,可对接 Sidekiq、Resque、SQS 等。

## Hotwire 与 Turbo

Rails 7 起,DHH 推出 **Hotwire** 哲学——HTML over the Wire,反对前后端分离主流:
- **Turbo Drive**:将链接点击转为 AJAX,无刷新
- **Turbo Frames**:页面分块替换
- **Turbo Streams**:实时推送 HTML 片段
- **Stimulus**:轻量 JS 控制器

它让 Rails 全栈应用以极低 JS 量获得 SPA 体验,是反 React/Vue 主流的探索。Phoenix LiveView、Laravel Livewire 都是同一思路。

## 版本演进

- 1.0(2005):奠定 MVC 与 Active Record
- 3.0(2010):合并 Merb,引入 Bundler、Active Model
- 4.0(2013):Strong Parameters、Turbolinks
- 5.0(2016):Action Cable、API 模式
- 6.0(2019):多数据库、并行测试、Webpacker
- 7.0(2022):Hotwire、Importmap、Active Storage
- 8.0(2024):简化部署、Solid Queue / Cache / Cable(SQLite 也能跑生产)

## 历史地位与影响

**催生的产品**

- Basecamp、Twitter(早期)、GitHub、Shopify、Airbnb、GitLab、Stripe Dashboard、Square

**对行业的影响**

- 普及"约定优于配置"
- 普及 [[TDD测试驱动开发]] 文化
- 普及数据库迁移
- 启发 [[Django框架]]、[[Laravel]]、Phoenix 等
- 启发 RESTful 资源路由
- 启发 Bundler → npm、Composer、Cargo

## "Rails Doesn't Scale" 神话

Twitter 早期 Rails 性能问题让"Rails 不能扩展"成为流传 widely 的说法。事实是:
- Twitter 是 Rails + MySQL + Memcached 起家
- 后来扩到亿级日活时改写为 JVM(Scala)
- Shopify、GitHub 用 Rails 撑住数十亿请求

Rails 性能问题真正的核心是 Ruby 解释器(MRI)的 GIL([[Python GIL]] 类似机制),并发并行受限。但通过水平扩展、缓存、Sidekiq 队列,绝大多数 SaaS 仍能用 Rails 承担。

## 与同类框架对比

| 维度 | Rails | Django | Laravel | Spring Boot |
|---|---|---|---|---|
| 语言 | Ruby | Python | PHP | Java |
| 起源 | 2004 | 2005 | 2011 | 2014 |
| 设计哲学 | 程序员幸福 | Batteries Included | 优雅 + DX | 企业稳健 |
| 模板 | ERB / Turbo | Django Template | Blade | Thymeleaf / FreeMarker |
| 异步 | 弱(Sidekiq) | 渐进 | 弱 | 强(WebFlux) |
| 性能 | 中 | 中 | 中 | 高 |
| 流行度趋势 | 平稳但下降 | 上升(AI) | 平稳 | 平稳 |

## 局限

- Ruby 性能瓶颈(GIL、解释器速度)
- 异步并发模型受限(对比 Node.js / Go)
- "Magic"过多调试困难
- 团队招聘 Ruby 人才不易
- 大企业新项目少选

## 现状(2025)

- 仍是 Shopify、Basecamp、GitHub 等的核心栈
- DHH 通过 ONCE / 37signals 项目坚持"小团队大产能"哲学
- AI 编码助手(Copilot、Cursor)对 Rails 友好
- Hotwire + SQLite + Solid 全家桶 让"单服务器跑生产"复兴

## 和其他概念的关系

Rails 是"约定优于配置"的母体,影响了几乎所有现代 Web 框架的设计——[[Django框架]]、[[Laravel]]、[[Spring Boot]] 都明确表示借鉴。它的 [[设计模式]](MVC、ActiveRecord、Service Object 争议)是教科书素材。

Rails 与 [[关系型数据库]] 深度耦合,异步处理依赖 [[消息队列]] / Sidekiq。它的 RESTful 路由设计直接影响了 [[RESTful API]] 的工程实践。Hotwire 路线代表了对 [[微服务]] 与前后端分离的另一种回应——保持单体应用的简单性。

## 参考源

- raw/计算机/
- 相关:[[Django框架]]、[[Laravel]]、[[Spring Boot]]
