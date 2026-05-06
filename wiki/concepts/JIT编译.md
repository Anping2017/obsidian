---
title: JIT编译
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/编程基础/编译原理/]
created: 2026-05-05
updated: 2026-05-05
summary: JIT 在程序运行时把热点代码翻译为本地机器码并缓存,结合解释器的快速启动与编译器的执行性能,是 JVM、V8、CLR 等现代运行时的核心优化。
---

# JIT编译

## 定义

**JIT(Just-In-Time Compilation,即时编译)** 是在程序运行时,根据 profile 信息把"热点"代码段翻译为本地机器码并替代解释执行的技术。它把"启动快(解释)"与"运行快(编译)"两者的优点融合,是 [[Java JVM]]、V8、CLR、PyPy、LuaJIT 的性能基础。

## 核心要点

- **分层编译**(Tiered Compilation)
  - **L0 解释器**:启动即跑,无编译开销。
  - **L1/L2 简单 JIT**(C1):快速生成中等质量本地码。
  - **L3 优化 JIT**(C2/Graal/TurboFan):激进内联、逃逸分析、向量化,质量接近 AOT。
- **优化技术**
  - **方法内联**:把热点小函数嵌入调用点,消除调用开销并暴露后续优化机会。
  - **逃逸分析**:对象未逃出方法 → 栈分配 / 标量替换,减少 GC 压力。
  - **去虚拟化**:动态多态调用根据 profile 单态化,内联具体实现。
  - **循环优化**:展开、向量化、不变量外提。
  - **猜测优化(Speculative Optimization)**:基于运行时假设(类型稳定、分支偏向)激进优化,失败则**反优化(Deoptimization)** 回退到解释。
- **代价**
  - JIT 编译本身消耗 CPU 和内存(代码缓存)。
  - 启动后短期慢——Warm-up 期;参考 [[AOT编译]] 对比。
  - 运行时有不确定性,影响延迟敏感场景。
- **典型实现**
  - **HotSpot**:C1 + C2,业界标杆;Graal 替代 C2 用 Java 写编译器。
  - **V8**:Ignition + TurboFan,引入 Maglev 中间层。
  - **PyPy**:Tracing JIT,以循环为单位编译,擅长 hot loop。
  - **.NET RyuJIT**:跨平台、Tiered、Quick JIT。

## 关系

- 是 [[编译vs解释]] 的混合模式核心。
- 与 [[AOT编译]] 对偶——前者运行时编译换性能,后者启动前编译换启动速度。
- [[Java JVM]] 性能很大程度取决于 JIT 实现质量。
- [[字节码与中间表示]] 是 JIT 的输入——SSA 形式利于优化。
- [[Java垃圾回收]] 与 JIT 互动——逃逸分析配合 GC 减少分配。
- 微基准测试的"warm-up"问题源自 JIT;长跑稳态才能反映真实性能。

## 参考源

- raw/计算机/编程基础/编译原理/06-代码优化/
- raw/计算机/编程基础/编译原理/09-运行时环境/
- raw/计算机/编程基础/编译原理/13-对比分析/
