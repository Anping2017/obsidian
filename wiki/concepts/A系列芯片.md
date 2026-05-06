---
title: A 系列芯片
type: concept
tags: [ios, mature]
sources: [raw/iPhone/iPhone知识体系/02-技术规格层/核心硬件/01-芯片规格对比.md, raw/iPhone/iPhone知识体系/01-基础认知层/技术发展脉络/01-芯片发展历程.md]
created: 2026-05-05
updated: 2026-05-05
summary: A 系列(A10-A18 Pro)是 Apple 自研基于 ARM 指令集的 SoC,集成 CPU、GPU、神经网络引擎、ISP、Secure Enclave,采用大小核异构与渐进式制程演进(16nm→3nm)。
---

# A 系列芯片

## 定义

A 系列(Apple Ax/Ax Pro)是 Apple 为 iPhone 自研的片上系统(SoC),基于 ARM 指令集,由台积电(TSMC)代工。与高通骁龙、联发科天玑不同,A 系列只服务于 Apple 自家产品,因此可与 [[iOS系统架构]] 做极致协同优化。

## 核心要点

### 架构组件

每代 A 系列芯片包含的固定模块:
- **CPU**:大小核异构。性能核心(2 个,处理重负载)+ 能效核心(4 个,处理后台任务),功耗动态调度。
- **GPU**:Apple 自研(从 A11 开始,此前由 Imagination 授权)。
- **[[神经网络引擎]]**(Neural Engine):专用 AI 加速器,从 A11 引入,A18 Pro 已达 35 TOPS。
- **ISP**(图像信号处理器):支撑 [[计算摄影]] 的硬件流水线。
- **[[Secure Enclave]]**:独立安全协处理器,存储 Face ID 数据、Apple Pay 密钥。
- **统一内存控制器**:CPU/GPU 共享 DRAM,降低数据搬运成本。

### 制程演进

从 A10(16 nm)到 A18 Pro(3 nm 第二代),每一次制程跃迁带来约 15-25% 的性能提升与同等幅度的能效改善。3 nm 是当前商用节点的极限,后续将进入 2 nm 时代。

### 关键代际节点

- **A11 Bionic(2017)**:首次集成神经网络引擎,使 [[Face ID]] 成为可能。
- **A12 Bionic(2018)**:首颗 7 nm 移动 SoC。
- **A14 Bionic(2020)**:首次进入 5 nm。
- **A17 Pro(2023)**:首次 3 nm,引入硬件光线追踪。
- **A18 Pro(2024)**:为 Apple Intelligence(端侧 LLM)设计。

### 软硬协同

A 系列的真正威力不在跑分,而在**只服务于 iOS、只服务于 iPhone 这一确定性目标**。例如 A17 Pro 的硬件光追是为 [[Metal]] 图形 API 准备的,神经网络引擎被 Core ML 直接调用,Secure Enclave 与 Face ID/Touch ID 一一对应。这种"芯片级独占优化"是 Android 阵营难以复制的。

## 关系

- 是 [[iOS系统架构]] 的物理基础
- 集成的 [[神经网络引擎]] 驱动 [[计算摄影]] 与端侧 AI
- 集成的 [[Secure Enclave]] 是 [[Face ID]]、Apple Pay、Touch ID 的信任根
- 与 [[iPhone电池技术]] 共同决定续航上限

## 参考源

- raw/iPhone/iPhone知识体系/02-技术规格层/核心硬件/01-芯片规格对比.md
- raw/iPhone/iPhone知识体系/01-基础认知层/技术发展脉络/01-芯片发展历程.md
