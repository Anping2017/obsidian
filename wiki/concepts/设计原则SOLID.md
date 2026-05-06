---
title: SOLID 设计原则
type: concept
tags: [cs, programming, mature]
sources:
  - raw/计算机/编程基础/设计模式/02-设计原则/01-SOLID原则详解.md
  - raw/计算机/编程基础/设计模式/02-设计原则/02-其他重要设计原则.md
created: 2026-05-05
updated: 2026-05-05
summary: SOLID 是 Robert Martin 提炼的五条面向对象设计原则,目标是写出易扩展、易维护、低耦合的代码,是设计模式的理论支柱。
---

# SOLID 设计原则

## 定义

**SOLID** 是面向对象设计的五条核心原则,由 Robert C. Martin(Uncle Bob)总结:
- **S** Single Responsibility Principle 单一职责
- **O** Open/Closed Principle 开闭原则
- **L** Liskov Substitution Principle 里氏替换
- **I** Interface Segregation Principle 接口隔离
- **D** Dependency Inversion Principle 依赖倒置

它们的共同目标:**让代码易于扩展、易于维护、降低修改的传播范围**。是[[设计模式]]背后的理论根基。

## 核心要点

### S - 单一职责原则

> 一个类应该只有一个引起它变化的原因。

如果一个类承担多个职责,需求变更时多个客户端都受影响。
- 反例:User 类同时管理用户数据 + 权限校验 + 日志输出
- 正例:User、AuthService、Logger 各司其职

延伸:函数也应该只做一件事(Clean Code 推崇)。

### O - 开闭原则

> 对扩展开放,对修改关闭。

新增功能应通过**添加新代码**而不是修改已有代码完成。
- 工具:抽象类 + 多态、策略模式、插件机制
- 反例:`if (type == 'Email') ... else if (type == 'SMS')` 加新通道要改这函数
- 正例:`Notifier` 接口,`EmailNotifier`、`SmsNotifier` 实现,新增 `WeChatNotifier` 不改老代码

### L - 里氏替换原则

> 子类对象必须能替换父类对象,程序行为不变。

子类重写不能"削弱"父类约定。
- 反例:Square 继承 Rectangle,但 setHeight 同时改 width 违反 Rectangle 的约定
- 正例:Bird 类有 fly(),但 Penguin 不能飞;让 Penguin 直接继承 Bird 违反 LSP → 重新设计层次

LSP 是契约式设计的形式化:前置条件不能加强、后置条件不能削弱、不变式必须保持。

### I - 接口隔离原则

> 客户端不应被迫依赖它不使用的接口方法。

胖接口应拆分为多个细接口。
- 反例:`Worker` 接口含 work() + eat(),Robot 类被迫实现 eat() 抛异常
- 正例:拆为 `Workable`、`Eatable`,Robot 只实现 Workable

### D - 依赖倒置原则

> 高层模块不应依赖底层模块,二者都应依赖抽象。
> 抽象不应依赖细节,细节应依赖抽象。

具体实现的细节(数据库、HTTP、第三方 API)在底层;业务规则在高层。两者通过抽象接口交互。
- 反例:`OrderService` 直接 `new MysqlOrderRepo()`
- 正例:`OrderService` 依赖 `OrderRepository` 接口,Mysql 实现注入

是**依赖注入(DI)**与控制反转(IoC)的理论基础,Spring、Guice 框架就是 DI 容器。

### SOLID 之外的辅助原则

- **DRY** Don't Repeat Yourself:消除重复
- **KISS** Keep It Simple, Stupid:够用就好
- **YAGNI** You Aren't Gonna Need It:不要为想象的需求过度设计
- **LoD / Demeter Law** 迪米特法则:只与直接朋友说话,降低耦合
- **Composition over Inheritance** 组合优于继承

### 工程上的取舍

- 严格遵守 SOLID 会增加抽象层数,小型项目可能"过度工程"
- 应在核心业务、长期演进的代码中用,边缘脚本可放松
- 测试驱动开发(TDD)天然推动代码遵守 SOLID(可测的代码必然低耦合)

## 和其他概念的关系

SOLID 是[[设计模式]]的灵魂:大多数 GoF 模式实现某条 SOLID 原则。如:
- 策略模式 → 开闭、依赖倒置
- 装饰器 → 开闭
- 工厂 → 依赖倒置
- 命令 → 单一职责

[[面向对象编程]]四大特性(封装/继承/多态/抽象)是 SOLID 的语言机制基础。**依赖注入框架**(Spring、NestJS)是 D 原则的工程化产物。

[[微服务]]在系统层面继承 SOLID:每个服务单一职责、通过 API 解耦(开闭/依赖倒置)。Clean Architecture(Uncle Bob 后续著作)把 SOLID 推广到整个应用架构。

## 参考源

- raw/计算机/编程基础/设计模式/02-设计原则/01-SOLID原则详解.md
- raw/计算机/编程基础/设计模式/02-设计原则/02-其他重要设计原则.md
