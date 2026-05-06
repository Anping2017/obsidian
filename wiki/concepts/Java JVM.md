---
title: Java JVM
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: JVM 是 Java 的虚拟机,把字节码翻译为本地指令运行,核心包括类加载器、运行时数据区、执行引擎(解释器+JIT)、垃圾回收器,是"一次编写到处运行"的基础。
---

# Java JVM

## 定义

**Java 虚拟机(JVM)** 是字节码到本地代码的执行引擎规范——任何符合 JVM Spec 的实现(HotSpot、OpenJ9、GraalVM Native Image、Azul Zing)都可以运行 `.class` 字节码。它通过抽象 CPU 与 OS,达成 Java"一次编写到处运行"的承诺。

## 核心要点

- **类加载子系统**:Bootstrap → Extension → Application → 自定义,双亲委派模型;经历加载、验证、准备、解析、初始化五阶段。
- **运行时数据区**
  - **方法区(Metaspace)**:类元数据、常量池、JIT 编译后的代码缓存。
  - **堆(Heap)**:对象实例,GC 主战场;细分新生代(Eden+Survivor)、老年代。
  - **栈(JVM Stack)**:线程私有,栈帧含局部变量表、操作数栈、动态链接。
  - **本地方法栈、PC 寄存器**:JNI 调用、字节码指令指针。
- **执行引擎**
  - **解释器**:逐条字节码翻译执行,启动快但慢。
  - **JIT 编译器**(C1 客户端编译、C2 服务端编译、Graal):热点方法编译为本地代码,带分支预测、内联、逃逸分析。
  - **AOT**(GraalVM Native Image):编译期就生成本地可执行文件,启动毫秒级,代价是部分动态特性受限。
- **GC**:Serial、Parallel、CMS(已废弃)、G1、ZGC、Shenandoah —— 从分代复制到低延迟并发,典型 STW 从秒级降到毫秒以下。
- **JNI**:Java 调用本地代码通道,代价是失去 GC、JIT 优化与跨平台性。

## 关系

- 是 [[编译vs解释]] 折中——既不是纯解释也不是纯编译,而是"解释 + JIT"。
- [[JIT编译]] 是 JVM 性能的核心来源;Graal/HotSpot 的实现差异决定了 [[Java Stream API]] 等抽象的效率。
- [[Java垃圾回收]] 在 JVM 内实现,演进史本身可写一本书。
- 是 Scala、Kotlin、Clojure、Groovy 等 JVM 语言的共同运行时——多语言共享 GC 与 JIT。
- 概念上对应 [[字节码与中间表示]] 在 .NET CLR、Python CPython、JavaScript V8 中的不同实现。
- 与 [[操作系统]] 的进程/线程模型耦合——JVM 线程多数实现为 OS 原生线程。

## 参考源

- raw/计算机/编程基础/编译原理/09-运行时环境/
- raw/计算机/开发学习/语言/(Java 内容散落在 Python/JS 与编程基础下的横向比较)
