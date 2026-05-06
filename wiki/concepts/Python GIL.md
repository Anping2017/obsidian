---
title: Python GIL
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/开发学习/语言/Python/03_理解层-深度原理与机制/3.2.1 GIL机制与多线程.md]
created: 2026-05-05
updated: 2026-05-05
summary: GIL 是 CPython 解释器中的全局互斥锁,任一时刻只有一个线程执行字节码,保护引用计数 GC 的同时也限制了多线程的 CPU 并行能力。
---

# Python GIL

## 定义

**GIL(Global Interpreter Lock,全局解释器锁)** 是 CPython 解释器层面的互斥锁,保证同一进程中任意时刻仅有一个原生线程在执行 Python 字节码。它是 CPython 实现细节而非语言规范——Jython、IronPython 没有 GIL。

## 核心要点

- **存在原因**:CPython 用引用计数做内存管理,多线程并发改写引用计数会损坏对象状态;GIL 提供最简单高效的全局保护。
- **释放时机**:每隔约 5ms 由 `sys.setswitchinterval` 触发释放,或在 I/O、`time.sleep`、`numpy` 等 C 扩展显式 `Py_BEGIN_ALLOW_THREADS` 时释放。
- **影响**:CPU 密集任务多线程几乎无加速,甚至因竞争更慢;I/O 密集任务可借线程切换实现并发。
- **绕过方案**
  - **多进程**(`multiprocessing`):每进程独立解释器和 GIL,真并行,代价是 IPC 开销与启动慢。
  - **C 扩展**:`numpy`/`pandas` 在 C 层面 release GIL,数值计算可真并行。
  - **协程**(`asyncio`):单线程事件循环,适合高并发 I/O。
  - **PEP 703 No-GIL**:Python 3.13 引入实验性的 free-threaded 构建,移除 GIL 用细粒度锁替代。
- **常见误区**:GIL 不保护用户态业务一致性——`x += 1` 仍需 `Lock`,因为字节码层可被切换。

## 关系

- 是 [[并发与并行]] 在 Python 中的关键约束,直接区分了"并发"与"并行"。
- 与 [[进程与线程]] 的取舍密切相关——CPU 密集首选多进程,I/O 密集多线程或协程都行。
- 推动了 [[Python协程]] (asyncio) 与 [[事件循环]] 在 Python 生态的流行。
- 影响 [[Python装饰器]] (`lru_cache` 等) 的原子性假设。
- 与 [[操作系统]] 的线程调度叠加,形成"OS 调度+GIL 调度"的双层模型。
- PEP 703 是 [[CPython内部机制]] 演进的重要节点。

## 参考源

- raw/计算机/开发学习/语言/Python/03_理解层-深度原理与机制/3.2.1 GIL机制与多线程.md
- raw/计算机/开发学习/语言/Python/03_理解层-深度原理与机制/3.2.4 协作式并发vs抢占式并发.md
