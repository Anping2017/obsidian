---
title: JavaScript this绑定
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/开发学习/语言/Javascript/]
created: 2026-05-05
updated: 2026-05-05
summary: JS 的 this 在调用时按四种规则确定——默认、隐式、显式、new——再叠加箭头函数的词法绑定,是新人最常踩的坑。
---

# JavaScript this绑定

## 定义

**this 绑定** 是 JavaScript 中确定函数调用时 `this` 指向哪个对象的规则集合。与 Java/C++ 中 `this` 总指向当前实例不同,JS 的 `this` **由调用方式而非定义位置决定**(箭头函数除外)。

## 核心要点

- **四条优先级递增的规则**
  1. **默认绑定**:独立调用 `f()`,严格模式下为 `undefined`,非严格指向 `globalThis`。
  2. **隐式绑定**:`obj.f()`,this 指向 `obj`;隐式丢失常见于 `const g = obj.f; g()` —— 退化为默认绑定。
  3. **显式绑定**:`f.call(ctx)`、`f.apply(ctx)`、`f.bind(ctx)`,强制把 this 设为 ctx。
  4. **new 绑定**:`new F()`,创建新对象作为 this;优先级最高于显式 bind。
- **箭头函数**:不引入自己的 this,沿用定义时的词法 this;`call/apply/bind` 也无效。常用于回调中保持外层 this。
- **常见 bug**
  - DOM 事件回调:`element.onclick = obj.handler`(handler 内部 `this === element` 而非 obj);可用 bind 或箭头函数修正。
  - 类方法作回调:React class component 必须在 constructor 里 `bind`,或写为类字段箭头函数。
  - setTimeout 回调:`setTimeout(this.fn, 1000)` 失去 this——箭头函数包裹或显式 bind。
- **严格模式**:`'use strict'` 下默认绑定为 undefined 而非全局对象,提早暴露错误。
- **类与模块**:ES Module 顶层 this 为 undefined;class 方法的 this 取决于调用方式,与传统对象方法相同。

## 关系

- 与 [[JavaScript原型链]] 共同构成 JS 面向对象的两根支柱:原型决定方法在哪、this 决定方法操作谁。
- 与 [[闭包]]:闭包捕获词法变量,不解决 this 问题——this 永远是动态的(箭头函数除外)。
- 与 [[JavaScript事件循环]]:回调被宿主环境调用时 this 经常变化,需主动控制。
- [[TypeScript类型系统]] 提供 `this` 参数类型注解,在编译期发现 this 错误。
- 与 [[函数式编程]] 风格相反——FP 偏好不依赖隐式 this 的纯函数。

## 参考源

- raw/计算机/开发学习/语言/Javascript/02-理解掌握层/01-作用域与闭包/
- raw/计算机/开发学习/语言/Javascript/02-理解掌握层/02-原型与继承/04-ES6类语法.md
