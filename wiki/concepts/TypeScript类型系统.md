---
title: TypeScript类型系统
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/开发学习/语言/Typescript/TypeScript-知识地图/Comprehension-理解掌握层/]
created: 2026-05-05
updated: 2026-05-05
summary: TypeScript 在 JavaScript 之上叠加结构化、可推导的静态类型系统,通过类型擦除编译为 JS,核心特性是泛型、联合/交叉、条件类型与映射类型。
---

# TypeScript类型系统

## 定义

**TypeScript** 是 Microsoft 开源的 JavaScript 超集,在运行时仍是 JS,但编译期增加一套**结构化(structural)、渐进式(gradual)、可推导(inferential)** 的静态类型系统。运行时类型被擦除——TypeScript 只在编译期检查,不增加运行时开销。

## 核心要点

- **基本类型**:`number/string/boolean/bigint/symbol/null/undefined/void/never/unknown/any`;`unknown` 是类型安全的 any,`never` 是不可达类型(无穷循环、抛错)。
- **结构化类型**:类型兼容看形状而非名义——`interface Duck { quack(): void }` 任何具备 quack 的对象都兼容。
- **联合与交叉**
  - **Union** `A | B`:两类型之一,取交集成员可访问。
  - **Intersection** `A & B`:同时是两者,合并成员。
- **类型推导**:从字面量、初始化表达式、函数返回值等位置自动推断,减少显式注解负担。
- **泛型**:`function id<T>(x: T): T`,把类型作为参数传递,实现可重用的容器、函数、类型工具。
- **高级类型**
  - **Conditional Types**:`T extends U ? X : Y`,基础是 distributive over unions。
  - **Mapped Types**:`{ [K in keyof T]: ... }`,组合 `Partial/Required/Pick/Omit/Readonly` 等内置工具类型。
  - **Template Literal Types**:在类型层面拼接字符串字面量,做精确的字符串模式建模。
- **类型守护(Type Guards)**:`typeof`/`instanceof`/自定义 `x is T` 谓词函数,在分支内收窄类型。
- **`tsconfig.json` 关键**:`strict` 套件(noImplicitAny、strictNullChecks 等)、target/module 决定输出 JS 形态。

## 关系

- 是 [[静态类型与动态类型]] 中"渐进式静态类型"的代表——可与既有 JS 项目混用。
- 通过结构化类型与 [[JavaScript原型链]] 的鸭子类型哲学相容。
- [[泛型编程]] 在 TS 中借助 keyof、infer、conditional types 形成强大的类型代数。
- 与 [[Java JVM]]、[[Rust所有权]] 等名义类型系统相比,TS 更接近 OCaml/Haskell 的结构化推导风格。
- 编译输出 JS 进入 [[JavaScript事件循环]] 运行,类型仅在 IDE/CI 时存在。

## 参考源

- raw/计算机/开发学习/语言/Typescript/TypeScript-知识地图/Comprehension-理解掌握层/Type-Fundamentals/01-Type-System入门.md
- raw/计算机/开发学习/语言/Typescript/TypeScript-知识地图/Comprehension-理解掌握层/Type-Fundamentals/03-Type-Inference揭秘.md
- raw/计算机/开发学习/语言/Typescript/TypeScript-知识地图/Comprehension-理解掌握层/Advanced-Types/
