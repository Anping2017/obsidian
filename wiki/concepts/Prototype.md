---
title: Prototype 原型
type: concept
tags: [cs, programming, mature]
sources:
  - raw/计算机/编程语言/JavaScript/
created: 2026-05-05
updated: 2026-05-05
summary: Prototype(原型)是 JavaScript 的对象继承机制,每个对象有内部链接 [[Prototype]] 指向另一个对象,形成原型链;它也是软件工程中"原型设计模式"和产品设计中"快速原型"两个同名概念。
---

# Prototype 原型

## 定义

Prototype 在不同语境下有三层含义,本文以最常见的 JavaScript 原型机制为核心:

1. **JavaScript 原型继承**:每个对象都有一个内部链接 `[[Prototype]]`(可通过 `__proto__` 或 `Object.getPrototypeOf` 访问),指向另一个对象,形成**原型链**。属性查找沿链上溯,直到 `null`。这是 JS 实现继承与共享的底层机制。
2. **设计模式之原型模式(GoF Prototype Pattern)**:通过克隆现有对象创建新对象,避免繁琐的构造与依赖。
3. **产品/UX 原型(Prototyping)**:用低/高保真模型快速验证想法,典型工具 Figma、Sketch。

## 核心要点

### JavaScript 原型机制

```javascript
const animal = { eat() { console.log('eating'); } };
const dog = Object.create(animal);  // dog.__proto__ === animal
dog.bark = function() { console.log('woof'); };
dog.eat();   // 沿原型链找到 animal.eat,输出 eating
dog.bark();  // 自身属性
```

关键点:

- **`prototype` 属性**:函数(构造器)上的 `prototype` 是「未来实例的原型对象」
- **`__proto__` / `[[Prototype]]`**:实例上指向其原型的链接
- **原型链终点**:`Object.prototype.__proto__ === null`
- **`new` 操作符**:创建对象、设置 `__proto__`、绑定 `this`、执行构造器

ES6 的 `class` 是原型继承的语法糖,底层仍是原型链。

### 原型继承 vs 类继承

| 维度 | 原型继承(JS) | 类继承(Java/C++) |
|---|---|---|
| 心智模型 | 对象→对象 | 类→类→实例 |
| 灵活性 | 运行时可改 | 编译期固定 |
| 共享方式 | 共享同一原型对象 | 各实例独立 |
| 性能 | 原型链查找略慢 | 静态分派更快 |

JS 自 ES6 引入 `class` 后表面接近类继承,但底层语义仍是原型,可在运行时修改 `prototype` 增加方法。

### 原型设计模式

适用场景:

- 创建对象代价高(深度克隆配置)
- 对象类型在运行时确定
- 避免复杂构造层级

### 产品快速原型

- **低保真**:纸笔、白板,验证流程
- **高保真**:Figma 交互原型,验证视觉与体验
- **可点击原型**:用 InVision、Figma Smart Animate 模拟真实交互
- **代码原型**:V0、Lovable 类 AI 工具直接生成可运行 demo

## 和其他概念的关系

JavaScript 原型与 [[闭包]]、[[this 绑定]]、[[JavaScript Promise与async-await|Promise与异步]] 共同构成 [[JavaScript原型链|JavaScript]] 的核心概念。理解原型链是理解 [[Vue]]、[[React]] 等框架内部机制的前提(组件实例继承、响应式实现常用 `Object.create`)。

设计模式中的原型模式与 [[设计模式]] 体系并列,与工厂方法、抽象工厂同属创建型模式。

UX 原型是 [[产品管理]] 与 [[设计思维]] 中验证假设的工具,与 [[MVP最小可行产品]]、用户测试、A/B 测试组合使用,缩短从想法到验证的反馈周期。

## 参考源

- raw/计算机/编程语言/JavaScript/
- raw/AI人工智能/AI编程工具/
- MDN: Inheritance and the prototype chain
- GoF《Design Patterns》
