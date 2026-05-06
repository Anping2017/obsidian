---
title: Python生成器
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/开发学习/语言/Python/02_认知层-核心概念与范式/2.2.2 迭代器与生成器机制.md]
created: 2026-05-05
updated: 2026-05-05
summary: 生成器用 yield 暂停函数执行并返回值,下一次调用从断点恢复,以惰性求值实现内存常量级、可组合的迭代流水线。
---

# Python生成器

## 定义

**生成器(Generator)** 是 Python 中一类特殊的迭代器,用 `yield` 暂停函数、保留局部状态并返回值给调用方。每次 `next()` 从断点继续,直到再次 `yield` 或 `return`。生成器把"按需产生值"和"协作式让出控制"两个想法编码进函数。

## 核心要点

- **写法**
  - **生成器函数**:含 `yield` 的函数,调用返回 generator 对象。
  - **生成器表达式**:`(expr for x in iter)`,内存友好版列表推导。
- **执行模型**:`yield` 暂停后通过 `next()`/`send()`/`throw()`/`close()` 恢复;`return` 触发 `StopIteration` 并把值放入异常的 `value`。
- **`yield from`**:委托给子生成器并透传 send/throw,简化嵌套生成器组合。
- **协程双向通信**:`send(val)` 把值注入挂起的 yield 表达式,生成器最初是 PEP 342 协程的基础。
- **优势**
  - 内存常量级处理百万级数据流(读大文件、解析日志)。
  - 惰性求值与短路:管道前段不必先全量计算。
  - 可组合的迭代器链(`itertools` + 生成器)。
- **陷阱**
  - 单次消费,不能重置(可重新调用生成器函数获取新对象)。
  - 异常在 `yield` 处抛出时需要 try/finally 清理资源。

## 关系

- 是 [[迭代器协议]] 的简化实现,所有生成器都是迭代器。
- 与 [[Python协程]] (asyncio 的 async/await) 同源——asyncio 协程在 PEP 492 之前就基于生成器实现。
- 与 [[Python装饰器]]、[[Python上下文管理器]] 共同构成 Pythonic 抽象工具箱。
- 在 [[函数式编程]] 视角下提供惰性序列(类似 Haskell 的 lazy list)。
- 是 [[Python内存管理]] 中"流式处理替代 list"的关键工具。
- 与 [[事件循环]] 配合实现协作式调度(老式 yield-based coroutine)。

## 参考源

- raw/计算机/开发学习/语言/Python/02_认知层-核心概念与范式/2.2.2 迭代器与生成器机制.md
