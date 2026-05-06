---
title: JavaScript事件循环
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/开发学习/语言/Javascript/02-理解掌握层/03-异步编程/01-事件循环机制.md]
created: 2026-05-05
updated: 2026-05-05
summary: JS 事件循环以单线程调用栈+任务队列+微任务队列协作运行,是 Promise/async 异步语义、setTimeout/IO 调度的底层模型。
---

# JavaScript事件循环

## 定义

**事件循环(Event Loop)** 是 JavaScript 运行时的核心调度机制——浏览器与 Node.js 都用它把同步代码、异步回调、Promise 微任务、定时器、I/O 完成事件按顺序送入唯一的主线程执行。它把"非阻塞 I/O"和"单线程语义"统一在一个简洁模型里。

## 核心要点

- **结构**:Call Stack(同步执行)、Task Queue 宏任务(setTimeout、I/O、UI 事件)、Microtask Queue(Promise.then、queueMicrotask、MutationObserver)。
- **算法**(简化)
  1. 取一个宏任务执行,直到调用栈清空。
  2. 清空所有微任务(微任务执行中产生新微任务也要消化)。
  3. 浏览器渲染(必要时)。
  4. 回到步骤 1。
- **微任务优先**:`Promise.then` 在当前同步代码结束后、下一个宏任务前立即执行;长链微任务会饿死宏任务和渲染。
- **Node.js 差异**:多阶段队列(timers、pending、poll、check、close),`setImmediate` vs `setTimeout(0)` 顺序受当前阶段影响;Node 11 起 microtask 在每个回调后清空,行为更接近浏览器。
- **常见现象**
  - `setTimeout(0)` 不是真的 0——HTML5 规范最小延迟 4ms,且要等当前任务+微任务结束。
  - `await` 等价于 `.then`,后续代码进入微任务队列。
  - 长任务阻塞渲染——主线程超过 50ms 即可能丢帧;用 `requestIdleCallback`、Web Worker 卸载。
- **Web Worker** 在独立线程跑,有自己的事件循环,主线程通过 postMessage 通信。

## 关系

- 是 [[并发与并行]] 中"单线程并发"的典范——通过协作式任务切换达成高并发 I/O。
- 与 [[JavaScript Promise与async-await]]、[[JavaScript Generator]] 共同构成现代 JS 异步基础设施。
- [[Node.js底层架构]] 在事件循环之外加 libuv 线程池处理阻塞 I/O。
- 概念与 [[Python协程]] 的 asyncio、[[Go goroutine与channel]] 的 GMP 调度有相通之处,都是非抢占式协作并发。
- 与 [[JavaScript this绑定]] 联动——异步回调内的 this 经常需要 bind 或箭头函数修正。

## 参考源

- raw/计算机/开发学习/语言/Javascript/02-理解掌握层/03-异步编程/01-事件循环机制.md
- raw/计算机/开发学习/语言/Javascript/02-理解掌握层/03-异步编程/03-Promise详解.md
- raw/计算机/开发学习/语言/Javascript/02-理解掌握层/03-异步编程/04-async-await语法.md
