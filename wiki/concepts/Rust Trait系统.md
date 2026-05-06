---
title: Rust Trait系统
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Trait 是 Rust 的接口抽象——定义共享行为、支持泛型约束与默认实现,通过静态分发(单态化)零成本或动态分发(trait object)实现多态。
---

# Rust Trait系统

## 定义

**Trait** 是 Rust 描述类型行为的方式——类似 Java 接口、Haskell 类型类(typeclass)、Swift protocol。Trait 定义方法签名(可附默认实现),类型通过 `impl Trait for Type` 显式实现,后续函数可对"任何实现 X trait 的类型"操作,实现面向接口编程与零成本抽象。

## 核心要点

- **定义与实现**:`trait Greet { fn hi(&self); }` + `impl Greet for User { fn hi(&self) { ... } }`。
- **默认方法**:trait 内可写默认实现,实现者可覆盖;支持 trait 演进而不破坏实现者。
- **泛型约束**:`fn print<T: Display>(x: T)` 只接受实现 Display 的类型;复杂约束用 `where` 子句更可读。
- **静态分发(单态化)**:泛型在编译期为每个实参生成专用版本(monomorphization),零运行时成本但二进制膨胀。
- **动态分发(Trait Object)**:`Box<dyn Trait>`/`&dyn Trait`,通过 vtable 调用,运行时多态,代价是间接调用且 trait 必须是对象安全的。
- **关键标记 trait**
  - `Send`:类型可安全在线程间转移所有权。
  - `Sync`:类型 `&T` 可安全在线程间共享。
  - `Sized`:编译期已知大小;泛型默认 `T: Sized`,关闭用 `?Sized`。
  - `Copy/Clone/Drop`:控制所有权与复制行为。
- **孤儿规则**:实现 Trait 时 trait 或类型至少之一来自当前 crate,避免冲突;`newtype` 模式绕过限制。
- **关联类型 vs 泛型参数**:`type Output;` 一个类型实现一次 trait;`<T>` 同类型可对不同 T 多次实现;Iterator 用关联类型避免 turbofish。

## 关系

- 与 [[Rust所有权]]、[[Rust生命周期]] 共同构成 Rust 类型系统三大支柱。
- 在 [[面向对象编程]] 视角下提供组合替代继承——Rust 没有传统继承,trait + struct 是首选模式。
- [[泛型编程]] 比较:Rust trait bound 类似 C++20 concepts,比 Java/C# 的接口更强。
- 与 [[函数式编程]] 的 typeclass 思想接近——可对外部类型实现外部 trait(满足孤儿规则)。
- 是 Rust 实现 Iterator、Future(async/.await)、Error 处理(? 运算符)等现代抽象的核心机制。

## 参考源

- raw/计算机/(Rust 散落于面向对象与泛型对比)
- raw/计算机/编程基础/设计模式/02-设计原则/
