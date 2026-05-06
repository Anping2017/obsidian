---
title: AOT编译
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/编程基础/编译原理/]
created: 2026-05-05
updated: 2026-05-05
summary: AOT 在启动前把源码或字节码完全编译为本地机器码,启动毫秒级、内存占用低,适合 Serverless、移动端与命令行工具。
---

# AOT编译

## 定义

**AOT(Ahead-of-Time Compilation,预先编译)** 是在程序启动前把源代码或字节码完全编译为目标平台原生机器码的技术。与 [[JIT编译]] 在运行期边跑边译相对,AOT 把所有编译工作前置,运行时只装载执行,无需 warm-up。

## 核心要点

- **典型场景**
  - **Serverless / FaaS**:冷启动毫秒级至关重要。
  - **移动端**:iOS App Store 强制 AOT(Bitcode);Android ART 5.0 起 install-time AOT。
  - **CLI 工具**:Go、Rust、GraalVM Native Image 编出单一可执行文件。
  - **嵌入式 / IoT**:无 JIT 内存与权限,必须 AOT。
- **优势**
  - 启动极快:GraalVM Native Image Java 应用可达 10ms,JVM 模式可能 1s+。
  - 内存占用小:无解释器、无字节码、无 JIT 代码缓存。
  - 部署简单:静态链接产物即运行。
  - 安全审计简单:无运行时代码生成。
- **劣势**
  - **二进制膨胀**:静态链接含整个运行时与依赖。
  - **动态特性受限**:反射、动态类加载、JNI 需配置元数据(GraalVM 用 reachability metadata)。
  - **编译慢**:全程序静态分析,几秒到几分钟。
  - **优化决策一次性**:不能像 JIT 用运行时 profile;部分激进优化做不到。
  - **平台特定**:每个目标平台需单独编译。
- **代表实现**
  - **GraalVM Native Image**:Java/JVM 字节码 → 本地;支持 Quarkus、Micronaut、Spring Native。
  - **Dart AOT**:Flutter Release 模式编出原生 ARM/x64。
  - **.NET Native AOT**:.NET 7+ 第一方支持。
  - **Rust / Go / Swift**:本身就是 AOT 编译。
- **PGO(Profile-Guided Optimization)**:用一次代表性运行的 profile 反哺 AOT 编译,弥补无运行时信息的不足。

## 关系

- 与 [[JIT编译]] 是两种不同的编译时机选择,各有适用场景;现代运行时常配合或可切换。
- [[编译vs解释]] 中 AOT 是纯编译派代表。
- [[Java JVM]] 通过 GraalVM Native Image 走向 AOT,改变 Java 在 Serverless 的竞争力。
- [[Rust所有权]]、[[Go goroutine与channel]] 因语言层面无 GC 与简单类型系统,AOT 更纯粹。
- 与 [[链接与加载]] 配合——AOT 产物多为静态链接、单体可执行文件。

## 参考源

- raw/计算机/编程基础/编译原理/07-目标代码生成/
- raw/计算机/编程基础/编译原理/13-对比分析/
