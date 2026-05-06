---
title: TypeScript泛型与条件类型
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/开发学习/语言/Typescript/TypeScript-知识地图/Comprehension-理解掌握层/Advanced-Types/]
created: 2026-05-05
updated: 2026-05-05
summary: 泛型让函数与类型容器接受类型参数,条件类型在类型层面引入分支与递归,共同把 TypeScript 的类型系统升级为图灵完备的类型代数。
---

# TypeScript泛型与条件类型

## 定义

**泛型(Generics)** 让函数、接口、类、类型别名接受类型参数实现复用。**条件类型(Conditional Types)** 用 `T extends U ? X : Y` 在类型层面引入 if-else,配合 `infer`、分布式 union 与递归,使 TypeScript 类型系统具备类型代数能力,被证明为图灵完备。

## 核心要点

- **泛型基础**:`<T>(x: T): T`、`Array<T>`、`Map<K, V>`;约束用 `extends`,默认值用 `=`。
- **泛型推导**:多数情况编译器从参数推断类型实参,只有歧义或抽取时才需显式 `<T>`。
- **条件类型语法**:`type IsString<T> = T extends string ? true : false`。
- **`infer` 关键字**:在条件类型内提取子类型——`type Return<T> = T extends (...args: any) => infer R ? R : never`。
- **分布式行为**:裸类型参数 `T extends U` 在 union 上自动分布——`T extends U ? X : Y` 对每个 union 成员单独求值再合并;`[T] extends [U]` 关闭分布。
- **常用工具类型**(基于条件 + 映射类型实现):`Partial<T>`、`Required<T>`、`Pick<T,K>`、`Omit<T,K>`、`Exclude<T,U>`、`Extract<T,U>`、`ReturnType<T>`、`Parameters<T>`、`Awaited<T>`。
- **递归条件类型**:在条件类型分支内引用自身,用于深拷贝类型(`DeepReadonly<T>`)、字符串解析、路径键提取。
- **性能考虑**:复杂类型可能让编译器陷入指数级求值,影响 IDE 提示;TS 4.5+ 在递归类型有改进,但仍需关注。

## 关系

- 是 [[TypeScript类型系统]] 的"高级武器",把基本类型组合升级为类型层面的元编程。
- 与 [[泛型编程]] 在 Java/C# 的对应概念相比,TS 因结构化类型 + 条件类型表达力更强。
- [[Template Literal Types]] 配合条件类型可在类型层做字符串模式匹配(路由、API schema)。
- 与运行时无关——所有泛型在编译后被擦除,不像 [[Rust所有权]] 的泛型存在 monomorphization。
- 在 [[函数式编程]] 视角下接近 Haskell 的类型族(type families)。

## 参考源

- raw/计算机/开发学习/语言/Typescript/TypeScript-知识地图/Comprehension-理解掌握层/Advanced-Types/01-Generics泛型精通.md
- raw/计算机/开发学习/语言/Typescript/TypeScript-知识地图/Comprehension-理解掌握层/Advanced-Types/03-Conditional-Types深度应用.md
- raw/计算机/开发学习/语言/Typescript/TypeScript-知识地图/Comprehension-理解掌握层/Advanced-Types/04-Mapped-Types工具类型库.md
- raw/计算机/开发学习/语言/Typescript/TypeScript-知识地图/Comprehension-理解掌握层/Advanced-Types/05-Template-Literals字符串魔法.md
