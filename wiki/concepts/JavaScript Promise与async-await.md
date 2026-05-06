---
title: JavaScript Promise与async-await
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/开发学习/语言/Javascript/02-理解掌握层/03-异步编程/]
created: 2026-05-05
updated: 2026-05-05
summary: Promise 用三态对象组合异步流程,async/await 是其语法糖,把回调地狱重写为同步外形的代码,沿用事件循环微任务调度。
---

# JavaScript Promise与async-await

## 定义

**Promise** 是表示一个异步操作最终成功或失败结果的对象,状态为 pending → fulfilled/rejected,一旦 settle 不可变。**async/await**(ES2017)是基于 Promise 的语法糖——`async` 函数返回 Promise,`await` 挂起函数等待 Promise resolve 后继续。

## 核心要点

- **Promise 状态机**:`new Promise((resolve, reject) => ...)`,通过 `then/catch/finally` 注册延续;状态一旦 settle 就锁定。
- **链式调用**:`then` 返回新 Promise;返回值是普通值则包成已 resolve 的 Promise,返回 Promise 则等待;异常会变成 rejected。
- **组合工具**
  - `Promise.all`:全部成功才成功,任一失败立即失败,结果按顺序数组返回。
  - `Promise.allSettled`:等待全部 settle,返回每个结果状态。
  - `Promise.race`:首个 settle(fulfill 或 reject)即结果。
  - `Promise.any`:首个 fulfill 即结果,全部失败才失败。
- **async/await**
  - `await` 等待 Promise,值为 resolve 值;reject 转化为 throw,可被 try/catch 捕获。
  - 函数内顺序看似同步,实际每个 `await` 让出主线程进入[[JavaScript事件循环]] 微任务队列。
  - 并发:用 `await Promise.all([p1, p2])` 而非顺序 `await p1; await p2;`。
- **常见陷阱**
  - 忘记 await,Promise 直接 settle 了但代码未等待。
  - `forEach` 不能配合 await 串行(回调返回值被忽略);用 `for...of` 或 `Promise.all`。
  - 未捕获 rejection 会触发 `unhandledrejection` 事件;Node.js 默认 warning,未来版本可能 crash。
- **Promise 取消**:原生不支持,通常配合 `AbortController` 或第三方库。

## 关系

- 是 [[JavaScript事件循环]] 微任务的主要使用者——每个 `.then`/`await` 进入微任务队列。
- 替代旧式 callback 风格,化解"回调地狱"嵌套。
- 与 [[Python协程]] 的 asyncio 同构——await 语义高度相似,但 JS 早一步标准化。
- [[TypeScript类型系统]] 中 `Promise<T>` 是泛型典型例子;`await` 让 `T` 自然出现在赋值左侧。
- [[函数式编程]] 视角下 Promise 像 Future Monad,`then` 是 flatMap。

## 参考源

- raw/计算机/开发学习/语言/Javascript/02-理解掌握层/03-异步编程/03-Promise详解.md
- raw/计算机/开发学习/语言/Javascript/02-理解掌握层/03-异步编程/04-async-await语法.md
- raw/计算机/开发学习/语言/Javascript/02-理解掌握层/03-异步编程/06-错误处理策略.md
