---
title: Clean Architecture
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Clean Architecture 是 Bob Martin 2012 年综合 Onion、六边形与用例驱动设计的同心圆架构,核心是依赖只能向内、业务规则与框架解耦。
---

# Clean Architecture

## 定义

**Clean Architecture** 是 Robert C. Martin 2012 年博客与 2017 年同名书提出的架构,综合了 Hexagonal、Onion、DCI、BCE 等思想,用同心圆表达层次,核心规则只有一条:**源代码依赖关系只能从外向内,内圈不知道外圈的存在**。

## 核心要点

- **同心四圈(由内向外)**
  - **Entities**:跨应用的企业级业务规则;最稳定。
  - **Use Cases**:应用级业务规则,编排实体完成具体用例。
  - **Interface Adapters**:Controller、Presenter、Gateway,把用例数据转为外部表示与存储格式。
  - **Frameworks & Drivers**:Web 框架、ORM、数据库、UI、第三方 SDK;最易变。
- **依赖规则**:任何源码引用必须指向更内圈;外圈实现内圈的接口,典型是 [[依赖倒置]] 的应用。
- **数据穿越边界**
  - 跨边界传递的数据用简单结构(DTO、原语),不要把 ORM 实体或框架对象泄露到内圈。
  - 跨边界调用方向与依赖方向可不同——用接口反转。
- **关键模式**
  - **Use Case Interactor**:用例的核心实现。
  - **Input/Output Boundary**:用例的入参与出参接口。
  - **Presenter**:把用例输出转为 ViewModel/JSON。
  - **Gateway**:外部资源访问的内层接口。
- **可测试性**:替换外圈即可测试内圈;Entity 与 Use Case 可纯函数式单元测试,无需启动框架。
- **常见落地结构**
  - **包/模块按层 vs 按特性**:推荐按特性(feature/use case)+ 内层分层,避免全局四大目录。
  - **配置类作为合成根**:在最外层把适配器装配进用例。

## 关系

- 与 [[六边形架构]]、Onion Architecture 在思想上等价,Clean 是 Bob Martin 的整合版。
- 是 [[DDD领域驱动设计]] 推荐的物理代码组织方式。
- 应用 [[设计原则SOLID]] 全套——尤其依赖倒置(D)。
- 与 [[CQRS]]、[[事件溯源]] 兼容——Use Case 层可拆 Command/Query Use Case。
- [[微服务]] 内部架构常采用 Clean,使每个服务独立可演化。
- 在 [[整洁代码]]、[[重构方法]] 框架下,架构防腐 + 局部重构是日常工作的两个尺度。

## 参考源

- raw/计算机/(架构主题分散)
- raw/计算机/编程基础/设计模式/02-设计原则/
