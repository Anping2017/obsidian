---
title: Face ID
type: concept
tags: [ios, mature]
sources: [raw/iPhone/iPhone知识体系/03-功能特性层/生物识别/02-Face ID技术.md, raw/iPhone/iPhone知识体系/03-功能特性层/生物识别/01-Touch ID技术.md, raw/iPhone/iPhone知识体系/03-功能特性层/生物识别/03-安全认证对比.md]
created: 2026-05-05
updated: 2026-05-05
summary: Face ID 是 Apple 基于 TrueDepth 摄像头与红外点阵投影的 3D 面部识别系统,自 iPhone X 引入,错误率约 1/100 万,数据存储于 Secure Enclave 本地,从不上云。
---

# Face ID

## 定义

Face ID 是 Apple 自 2017 年 iPhone X 引入的 3D 面部生物识别技术,用于解锁、支付确认、应用授权与 AR 体验。与 2D 面部识别(可被照片骗过)和指纹识别([[Touch ID]])不同,Face ID 通过红外点阵建模整张脸的深度图,实现"活体 3D 识别"。

## 核心要点

### 硬件构成

Face ID 依赖 iPhone 顶部的 TrueDepth 模组:
- **点阵投影器**:投射约 30,000 个不可见红外点
- **红外摄像头**:捕捉这些点形成的扭曲图样
- **泛光感应元件**:在暗光下补光,使红外摄像头能工作
- **前置摄像头**:常规 RGB 成像
- **距离传感器**:判断人脸距离

### 工作流程

1. 抬起设备或注视屏幕触发
2. 点阵投影 + 红外捕捉 → 生成 3D 深度图
3. 神经网络引擎(运行于 [[A系列芯片]] 中的 Neural Engine)与本地存储的面部模型比对
4. 模型存储在 [[Secure Enclave]],绝不出芯片
5. 0.2 秒内返回成功/失败

### 安全特性

- **错误率**:1/1,000,000(指纹的 [[Touch ID]] 为 1/50,000)
- **活体检测**:照片、面具、3D 头模均无法欺骗
- **暗光可用**:依靠红外,完全黑暗也能解锁
- **持续学习**:面部细微变化(剃须、戴眼镜、长胡)由系统自动适应
- **iPhone 13 起支持戴口罩识别**

### 隐私设计

Face ID 数据**从不离开设备、从不上传到 Apple 服务器、不与开发者共享**。第三方 App 调用 Face ID 时,App 只收到"成功/失败"的二元结果,看不到任何面部数据。这是 iOS 隐私架构的样本案例。

## 关系

- 由 [[A系列芯片]] 内的 [[Secure Enclave]] 与神经网络引擎驱动
- 是 [[iOS系统架构]] 隐私设计的实例
- 替代了早期机型的 [[Touch ID]],两者不能在同一台 iPhone 共存(直至 2024 仍如此)

## 参考源

- raw/iPhone/iPhone知识体系/03-功能特性层/生物识别/02-Face ID技术.md
- raw/iPhone/iPhone知识体系/03-功能特性层/生物识别/01-Touch ID技术.md
- raw/iPhone/iPhone知识体系/03-功能特性层/生物识别/03-安全认证对比.md
