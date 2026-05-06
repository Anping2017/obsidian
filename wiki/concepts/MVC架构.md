---
title: MVC 架构
type: concept
tags: [cs, programming, mature]
sources:
  - raw/计算机/开发学习/系统/Odoo/基础概念/MVC(模型-视图-控制器)模式.md
  - raw/计算机/开发学习/语言/PHP/05-专业深化层/架构设计/01-MVC架构模式.md
created: 2026-05-05
updated: 2026-05-05
summary: MVC 把应用拆分为模型、视图、控制器三层,以分离数据、表现、交互的职责,是 Web 框架与桌面 GUI 的经典架构模式。
---

# MVC 架构

## 定义

**MVC(Model-View-Controller,模型-视图-控制器)**是 1970 年代末 Trygve Reenskaug 在 Smalltalk 中提出的图形应用架构模式,后被广泛应用于 Web 框架与桌面 GUI。它把应用拆分为三层:

- **Model 模型**:数据、业务规则、状态。不感知 UI 存在
- **View 视图**:UI 表现层,把 Model 数据呈现给用户
- **Controller 控制器**:接收用户输入,协调 Model 与 View

核心目的:**关注点分离(Separation of Concerns)** —— 数据、表现、交互各自独立演化。

## 核心要点

### 三层职责

| 层 | 职责 | 反例 |
|---|---|---|
| Model | 数据结构、业务逻辑、持久化 | View 直接操作数据库 |
| View | 渲染、绑定数据、捕获用户事件 | View 含业务逻辑 |
| Controller | 解析输入、调用 Model、选择 View | Controller 写复杂业务规则 |

### 数据流(简化)

```
用户操作 → View → Controller → Model(读/写)→ Controller → 选 View 渲染 → 用户看到
```

### 经典 MVC 与 Web MVC 的区别

经典桌面 MVC 是观察者模式:Model 主动通知 View 更新。
Web MVC(Rails、Spring MVC、Laravel、Django、Express)是请求-响应模式:每次 HTTP 请求 Controller 拉取数据传给 View 模板渲染。Web 上 Model 主动 push 给 View 不可行(无状态)。

### MVC 在主流框架中

| 框架 | Model | View | Controller |
|---|---|---|---|
| Spring MVC | JPA Entity / Service | JSP / Thymeleaf | @Controller |
| Django | Model 类(ORM) | Template | View 函数(=Controller) |
| Rails | ActiveRecord | ERB / HAML | ActionController |
| Laravel | Eloquent | Blade | Controller |
| Odoo | Model(继承) | XML 视图 | Controller(HTTP 层) |

注意 Django 把 Controller 称为 "View",Template 称为 "Template",自称 MTV;本质同 MVC。

### MVC 的演化变体

- **MVP(Model-View-Presenter)**:View 更被动,Presenter 是单元测试可测的中介。Android 早期流行
- **MVVM(Model-View-ViewModel)**:ViewModel 持有 View 状态,通过双向数据绑定与 View 同步。Vue、Angular、WPF、SwiftUI 用此
- **MVI(Model-View-Intent)**:把用户意图作为单向数据流,Redux 风格
- **Flux / Redux**:单向数据流,Action → Reducer → Store → View

### 单向 vs 双向数据流

- **双向(MVVM)**:View ↔ ViewModel 自动绑定,书写量少但难以调试
- **单向(Flux/Redux/React)**:Action → State → View,流向清晰,易于追踪

React 的 Hooks/Context 在 MVVM 与单向之间灵活权衡。

### MVC 在前端的"消亡"与重生

早期 jQuery 时代前端无明显架构,直到 Backbone.js 引入 MVC。
React 兴起后"组件化 + 单向数据流"流行,MVC 退到后端。
但前端依然在做 MVC 的事:状态(Model = Redux/Pinia 仓库)、视图(组件)、控制(reducer/action),只是术语更新。

### 何时不用 MVC

- 极简应用(几页静态)
- 数据流复杂得多视图协作(可能 Flux/Redux 更合适)
- 实时协作类(可能事件驱动 + CQRS)

## 和其他概念的关系

MVC 是[[设计模式]]在架构层面的著名案例,体现[[设计原则SOLID]]的单一职责与依赖倒置。它与[[微服务]]不冲突 —— 微服务是宏观拆分,MVC 是单体或服务内部组织。

[[RESTful API]]在概念上是"无 View 的 MVC":Controller 处理请求,Model 处理数据,View 退化为 JSON 序列化。GraphQL 也类似。

ORM(Hibernate、Eloquent、Active Record)主要服务于 MVC 中 Model 的对接持久化。模板引擎(Thymeleaf、JSP、Jinja2、ERB)服务于 View 渲染。

## 参考源

- raw/计算机/开发学习/系统/Odoo/基础概念/MVC(模型-视图-控制器)模式.md
- raw/计算机/开发学习/语言/PHP/05-专业深化层/架构设计/01-MVC架构模式.md
