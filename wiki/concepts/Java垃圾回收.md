---
title: Java垃圾回收
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: JVM 垃圾回收基于"可达性分析+分代假设"自动管理堆,演进路线从 Serial 串行到 G1/ZGC 并发低延迟,是 Java 自动内存管理的核心。
---

# Java垃圾回收

## 定义

**Java 垃圾回收(GC)** 是 [[Java JVM]] 自动识别并回收堆中不再可达对象的子系统。GC 让 Java 摆脱 C/C++ 的手动 `malloc/free`,但代价是 STW(Stop-the-World)暂停与额外 CPU 开销。GC 算法演进的主线是降低延迟、增大吞吐、扩展堆规模。

## 核心要点

- **可达性分析**:从 GC Roots(线程栈引用、静态变量、JNI handle、活动锁等)出发,无法到达的对象即垃圾。引用计数法因循环引用问题不被主流 JVM 采用。
- **分代假设**:绝大多数对象朝生夕死——把堆分为新生代(Young)与老年代(Old/Tenured),不同代用不同算法。
- **算法基本款**
  - **复制(Copying)**:用于新生代,Eden + 两 Survivor,存活对象复制到 To,效率高但浪费 50% 空间。
  - **标记-清除(Mark-Sweep)**:标记可达,清除不可达,产生碎片。
  - **标记-整理(Mark-Compact)**:清除后压缩,适合老年代避免碎片。
- **GC 收集器演进**
  - **Serial / ParNew**:单/多线程,小堆。
  - **Parallel Scavenge**:吞吐优先,JDK 8 默认。
  - **CMS**:并发标记清除,STW 短但碎片化、JDK 14 移除。
  - **G1(Garbage First)**:JDK 9+ 默认,Region 化堆,可预测停顿。
  - **ZGC / Shenandoah**:并发标记+并发整理+染色指针/转发指针,STW 亚毫秒,堆可达 TB。
- **关键参数**:`-Xms/-Xmx` 堆大小、`-XX:+UseG1GC` 选择收集器、`-XX:MaxGCPauseMillis` 目标停顿。
- **调优**:监控 GC 日志、避免 Full GC、合理分代比例;关注 [[逃逸分析]] 让短命对象栈分配。

## 关系

- 是 [[Java JVM]] 中与 [[JIT编译]] 并列的两大支柱。
- 概念上对比 [[Rust所有权]] 的零成本无 GC、[[Python GIL]] 下的引用计数 + 标记清除、[[Go goroutine与channel]] 运行时的并发三色标记 GC。
- ZGC/Shenandoah 把 [[操作系统]] 虚拟内存特性(memory mapping、页保护)用作 GC 屏障,是系统编程与高级 GC 的融合。
- [[内存管理]] 在不同语言的实现:GC vs 手动 vs 所有权——Java 是 GC 派代表。
- 影响应用编程模式:对象池、堆外内存、零分配 API 是为了规避 GC 压力。

## 参考源

- raw/计算机/编程基础/编译原理/09-运行时环境/
- raw/计算机/开发学习/语言/(JVM 在 Python 内存管理对比章节中提及)
