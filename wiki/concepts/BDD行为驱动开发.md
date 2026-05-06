---
title: BDD行为驱动开发
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: BDD 通过 Given-When-Then 自然语言描述行为,把业务、测试、代码绑定到统一术语,既是协作语言也是验收测试框架。
---

# BDD行为驱动开发

## 定义

**行为驱动开发(Behavior-Driven Development,BDD)** 是 Dan North 2003 年提出、对 [[TDD测试驱动开发]] 的演进。核心想法是用业务可读的自然语言描述系统行为,作为开发、测试、产品、用户共同的契约,既驱动测试自动化也驱动需求沟通。

## 核心要点

- **核心句式 Given-When-Then(Gherkin 语法)**
  - **Given**:前置上下文(已注册用户、购物车有商品)。
  - **When**:触发事件(点击下单)。
  - **Then**:期望结果(订单生成、扣款、邮件发送)。
- **三个抽象层**
  - **Feature**:面向用户的业务能力。
  - **Scenario**:具体业务事例。
  - **Step Definition**:技术层把 Gherkin 句子绑定到代码。
- **典型工具**
  - **Cucumber**(JVM/Ruby 等多语言)。
  - **SpecFlow**(.NET)、**Behave/Pytest-BDD**(Python)、**Jasmine/Mocha**(JS,描述式)。
- **三圆模型**:Discovery(发现)、Formulation(描述)、Automation(自动化)——BDD 不是"自动化语法糖",更强调"对话与共识"。
- **Outside-In TDD**:从一个 BDD 场景出发,内层用 TDD 写单元测试驱动实现——先验收后单元。
- **常见反模式**
  - 把 Gherkin 当 UI 操作脚本(点击此处、填写此项)而非业务行为描述。
  - 步骤定义紧耦合实现,导致脚本脆弱。
  - "BDD without conversation":只剩工具,缺了三方协作。

## 关系

- 是 [[TDD测试驱动开发]] 在团队协作层面的延伸——TDD 驱动开发、BDD 驱动需求理解。
- 与 [[DDD领域驱动设计]] 的"通用语言(Ubiquitous Language)" 同根——都强调业务术语统一。
- [[单元测试金字塔]] 中,BDD 多用于验收/集成层;单元层仍以 TDD 为主。
- 与 [[CI_CD流水线]] 配合自动跑 Cucumber 报告,作为发布门禁。
- 不是银弹——团队若不真做"三方对话",BDD 会退化为冗长的脚本框架。

## 参考源

- raw/计算机/(测试与软件工程主题分散)
