---
title: Python协程
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/开发学习/语言/Python/03_理解层-深度原理与机制/3.2.3 async-await异步编程.md]
created: 2026-05-05
updated: 2026-05-05
summary: Python 协程通过 async/await 在单线程内协作式调度大量并发任务,基于 asyncio 事件循环和 selector,擅长 I/O 密集场景。
---

# Python协程

## 定义

**Python 协程(Coroutine)** 是 PEP 492 在 Python 3.5 引入的语言级异步原语——`async def` 定义协程函数、`await` 挂起当前协程让出控制。配合 `asyncio` 标准库的事件循环,它在单线程内实现成千上万协程的协作式并发,绕过 [[Python GIL]] 对 I/O 密集任务的限制。

## 核心要点

- **三类对象**
  - **协程函数**:`async def f(): ...`,调用返回 coroutine 对象,不立即执行。
  - **Awaitable**:实现 `__await__` 的对象;协程、Task、Future 都是 awaitable。
  - **Task**:`asyncio.create_task(coro)` 把协程提交给事件循环并行调度。
- **关键 API**
  - `asyncio.run(coro)`:启动事件循环并跑顶层协程。
  - `asyncio.gather(*aws)`:并发等待多个 awaitable,返回结果列表。
  - `asyncio.wait_for(aw, timeout)`:超时控制。
  - `asyncio.Queue/Lock/Semaphore`:协程安全的同步原语,与 threading 同名但语义不同。
  - `async with` / `async for`:配合 [[Python上下文管理器]] 与异步迭代器。
- **执行模型**
  - 事件循环跑在单线程,某协程 await I/O 时让出控制,事件循环调度下一个就绪协程。
  - 底层借助 selector(Linux 的 epoll、macOS 的 kqueue、Windows 的 IOCP)。
- **三大陷阱**
  - **阻塞同步代码**:在协程里跑同步耗时函数会卡住整个事件循环;用 `loop.run_in_executor` 派到线程池。
  - **未 await 协程**:`f()` 只生成对象不执行,需要 `await f()` 或 `create_task(f())`;新版本会警告。
  - **CPU 密集**:asyncio 不能加速 CPU 密集任务;用 multiprocessing。
- **生态库**:aiohttp、httpx、asyncpg、aiomysql、aioredis、FastAPI、Starlette、Quart。

## 关系

- 是 [[并发与并行]] 在 Python 中"协作式并发"的实现,绕过 [[Python GIL]] 限制 I/O 任务。
- 与 [[Python生成器]] 同根——asyncio 在 Python 3.5 之前用 yield-based coroutine。
- 与 [[JavaScript Promise与async-await]] 概念高度相似——都是 await + 事件循环。
- [[I_O模型]]:asyncio 底层是多路复用,看似阻塞实为非阻塞 + 事件驱动。
- [[Python上下文管理器]] 的 async 版本(`__aenter__/__aexit__`)是协程资源管理基础。
- 与 [[Go goroutine与channel]] 对比:goroutine 用户态调度但语法更像同步;协程显式 await,边界清晰。

## 参考源

- raw/计算机/开发学习/语言/Python/03_理解层-深度原理与机制/3.2.3 async-await异步编程.md
- raw/计算机/开发学习/语言/Python/03_理解层-深度原理与机制/3.2.4 协作式并发vs抢占式并发.md
