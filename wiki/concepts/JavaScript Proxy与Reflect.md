---
title: JavaScript Proxy与Reflect
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/开发学习/语言/Javascript/]
created: 2026-05-05
updated: 2026-05-05
summary: ES6 Proxy 拦截对象基础操作(读写、调用、属性枚举等),Reflect 提供这些操作的函数化版本,二者组合实现透明的元编程。
---

# JavaScript Proxy与Reflect

## 定义

**Proxy** 是 ES6 引入的元编程构造,接收**目标对象 + handler 处理器**,代理后所有对该 Proxy 的"基础操作"都可被 handler 拦截改写;**Reflect** 是与 Proxy 配套的内置对象,提供与 handler 同名的默认行为函数(`Reflect.get`、`Reflect.set`、`Reflect.has` 等),让你在拦截后还能调原行为。

## 核心要点

- **Proxy 用法**:`new Proxy(target, handler)`;handler 可定义 `get/set/has/deleteProperty/apply/construct/ownKeys/getPrototypeOf/...` 等 13 种 trap。
- **拦截对象操作示例**
  - `get(target, key, receiver)`:读取属性。
  - `set(target, key, value, receiver)`:写属性,需返回 boolean。
  - `has`:in 运算。
  - `apply`:函数调用。
  - `construct`:new 操作。
- **Reflect 的意义**
  - 把语言操作 API 化:`Reflect.get(obj, key)` ≡ `obj[key]`,但函数式可组合。
  - **正确转发**:在 trap 内 `return Reflect.get(...arguments)` 保留原语义,避免 receiver 错位。
  - **统一返回值**:Reflect 方法用 boolean 表示成功失败,比 Proxy 中 throw 更可控。
- **典型应用**
  - **响应式系统**:Vue 3 用 Proxy 替代 Vue 2 的 `Object.defineProperty`,支持新增属性和数组索引修改。
  - **校验与冻结**:写入时校验类型、深冻结。
  - **日志 / Profiling**:透明记录所有读写。
  - **虚拟资源**:模拟无限大小的数组、远程对象代理。
  - **命名空间隔离**:沙箱、polyfill。
- **限制与陷阱**
  - 部分操作不可拦截:`===` 比较、`typeof`、`instanceof`(后两可通过 Symbol 配合 partial)。
  - **WeakMap 私有数据**:无法被 Proxy 透明代理,因为 trap 看不到内部 slot。
  - 性能:Proxy 介入每次属性访问,大对象高频访问可能慢。

## 关系

- 与 [[JavaScript原型链]]、[[JavaScript this绑定]] 共同构成 JS 对象模型;Proxy 在原型查找之上拦截。
- 是 [[元编程]] 在 JS 的官方支持,替代 ES5 的 `__defineGetter__`/`Object.defineProperty` 黑魔法。
- Vue 3 响应式系统、MobX、Immer 等库的底层。
- 与 [[TypeScript类型系统]] 配合时需要泛型约束,确保拦截后的类型仍合理。
- 在 [[设计模式]] 视角下原生支持代理模式与装饰器模式。

## 参考源

- raw/计算机/开发学习/语言/Javascript/03-应用实践层/02-现代开发/01-ES6+新特性.md
- raw/计算机/开发学习/语言/Javascript/04-高级精通层/01-设计模式/04-JavaScript特有模式.md
