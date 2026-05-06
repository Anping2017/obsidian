---
title: JavaScript原型链
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/开发学习/语言/Javascript/02-理解掌握层/02-原型与继承/01-原型链机制.md]
created: 2026-05-05
updated: 2026-05-05
summary: JavaScript 通过对象的隐藏 [[Prototype]] 指针串成原型链,属性查找沿链上溯至 null,是 JS 实现继承与共享的底层机制。
---

# JavaScript原型链

## 定义

**原型链(Prototype Chain)** 是 JavaScript 实现继承的底层机制:每个对象内部都有一个 `[[Prototype]]` 指针(可通过 `Object.getPrototypeOf` 访问、`__proto__` 暴露),指向另一个对象。读取属性时如果对象自身没有,引擎沿 `[[Prototype]]` 上溯查找,直到 `Object.prototype.[[Prototype]] === null`。

## 核心要点

- **三角关系**:函数 `F` 的 `prototype` 属性是构造出来的实例的 `[[Prototype]]`;实例 `instance.constructor === F`。
- **查找规则**:写属性放到对象自身,读属性沿原型链找——这种写时浅、读时深的非对称是 JS 共享方法的根本。
- **`Object.create(proto)`**:直接以指定对象作为原型创建新对象,优于 ES5 之前的构造函数 hack。
- **ES6 class**:`class` 是构造函数的语法糖,继承(`extends`)在底层仍是设置原型链 + 借用构造函数;`super` 调用沿原型链回溯。
- **性能**:链越长查找越慢,V8 通过 hidden class + inline cache 优化常见结构;频繁修改原型(monkey patch)会破坏优化。
- **`hasOwnProperty` vs `in`**:前者只检查自身属性,后者沿原型链;`for...in` 遍历可枚举的链上属性,需配合 `hasOwnProperty` 过滤。
- **典型陷阱**:数组 `Array.prototype.foo` 一改全改;原型上挂引用类型(数组、对象)会被所有实例共享。

## 关系

- 是 [[面向对象编程]] 在原型式语言中的实现,与基于类的 OOP(Java/C++)在概念层不同但效果相通。
- 与 [[JavaScript this绑定]] 联动——方法在原型上但 `this` 指向调用者,实现"不复制但行为正确"。
- 影响 [[JavaScript闭包]] 和 [[闭包]] 在面向对象封装中的角色。
- ES6 [[Proxy与Reflect]] 可在原型链查找之上拦截操作,实现元编程。
- 与 [[TypeScript类型系统]] 中的结构化类型(structural typing)理念呼应。

## 参考源

- raw/计算机/开发学习/语言/Javascript/02-理解掌握层/02-原型与继承/01-原型链机制.md
- raw/计算机/开发学习/语言/Javascript/02-理解掌握层/02-原型与继承/03-继承模式对比.md
- raw/计算机/开发学习/语言/Javascript/02-理解掌握层/02-原型与继承/04-ES6类语法.md
