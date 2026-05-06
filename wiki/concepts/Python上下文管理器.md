---
title: Python上下文管理器
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/开发学习/语言/Python/]
created: 2026-05-05
updated: 2026-05-05
summary: 上下文管理器通过 __enter__/__exit__ 协议把"获取资源-使用-释放"封装到 with 语句,确保异常路径下资源也被正确清理。
---

# Python上下文管理器

## 定义

**上下文管理器(Context Manager)** 是实现 `__enter__` 与 `__exit__` 协议的对象,配合 `with` 语句把资源生命周期与代码块绑定:进入块时初始化,离开块(无论正常还是异常)时清理。它是 RAII 思想在 Python 的对应。

## 核心要点

- **协议**:`__enter__()` 在进入 with 块时调用,返回值绑定到 `as`;`__exit__(exc_type, exc, tb)` 在离开时调用,返回 True 可吞掉异常。
- **`contextlib.contextmanager`**:用[[Python生成器]] 写上下文管理器——`yield` 之前是 enter,之后是 exit;try/finally 处理异常清理。
- **异步版本**:`async with` 对应 `__aenter__/__aexit__`,在 [[Python协程]] 中管理异步资源(连接池、信号量)。
- **嵌套与组合**:`with A() as a, B() as b:` 自上而下进入、自下而上退出;`ExitStack` 支持动态嵌套未知数量上下文。
- **常见用途**
  - 文件、Socket、数据库连接的获取与释放。
  - 锁(`threading.Lock`) 的 acquire/release。
  - 临时改变全局状态(decimal 精度、warnings 配置)。
  - 性能计时器、日志缩进、事务回滚。
- **优势**:异常安全比手动 try/finally 更难写错;`with` 块边界即资源边界,意图清晰。

## 关系

- 与 [[Python生成器]]:`@contextmanager` 复用生成器机制实现轻量上下文管理器。
- 与 [[Python装饰器]] 都属于 Python 的代码组织语法糖。
- 在 [[操作系统]] 资源(文件描述符、Socket、信号量)管理中频繁使用,避免泄漏。
- 类似思想见 C# `using`、Java `try-with-resources`、Rust [[Rust所有权]] 的 RAII。
- 是 [[整洁代码]] 中"资源即对象、生命期可控"的实践。

## 参考源

- raw/计算机/开发学习/语言/Python/04_应用层-标准库与第三方库/
- raw/计算机/开发学习/语言/Python/03_理解层-深度原理与机制/3.3.1 异常处理最佳实践.md
