---
title: TrueDepth 深感系统
type: concept
tags: [iphone, ios, mature]
sources: [raw/iPhone/iPhone知识体系/03-功能特性层/生物识别/02-Face ID技术.md]
created: 2026-05-05
updated: 2026-05-05
summary: TrueDepth 深感系统是 Apple 在 iPhone X(2017)首发的前置 3D 摄像组件,集成红外摄像头、点阵投影器、泛光感应器、原深感摄像头,共同支撑 Face ID、Animoji、人像模式等功能。
---

# TrueDepth 深感系统

## 定义

TrueDepth Camera System 是 Apple 在 iPhone X 引入的多模态前置摄像组件,核心是把 3D 几何感知能力从工业级设备带入消费电子。它由四个关键组件构成:

1. **点阵投影器(Dot Projector)**:发射约 30,000 个红外光点
2. **红外摄像头(IR Camera)**:捕捉反射的红外点阵
3. **泛光感应器(Flood Illuminator)**:发出非结构化红外光,照亮黑暗环境下的人脸
4. **前置 RGB 摄像头**:常规可见光摄像

这四件套与 A 系列芯片的 [[神经网络引擎]] 协同,生成毫米级精度的 3D 面部深度图,是 [[Face ID]]、Memoji、Animoji、[[计算摄影]] 人像模式等功能的硬件基础。

## 工作原理

**结构光原理**

点阵投影器投射出预定义图案的 30,000+ 红外点到面部,IR 摄像头捕捉变形后的图案。通过对比"已知发射模式"与"实际捕捉模式"的偏移,系统计算出每个点的距离,合成深度图(depth map)。

**与 ToF(Time of Flight)对比**

业界另一主流 3D 方案是 ToF(测光飞行时间),通过测量光脉冲往返时间计算距离。安卓阵营更多采用 ToF。结构光在近距精度高(适合面部识别),ToF 在远距和大场景表现更好。

**红外辅助**

可见光 + 红外双通道,使 TrueDepth 在完全黑暗、强光、夜间均可工作。这是 Face ID 区别于早期前置摄像头的人脸识别(光照敏感)的关键。

## 功能矩阵

**生物识别**:Face ID 通过 30,000 点匹配 Secure Enclave 中的面部模型,错误率约 1/100 万

**Animoji / Memoji**:实时捕捉面部表情(嘴、眼、眉、下巴等 50+ 肌肉运动)映射到虚拟形象,iMessage 中可发送

**人像模式自拍**:用深度图分离前景人脸与背景,实现景深效果(Bokeh)

**Portrait Lighting**:基于面部 3D 几何模拟舞台光、轮廓光等多种光照效果

**Center Stage(舞台中央)**:在 iPad 上结合超广角与 TrueDepth,自动追焦说话者(后续也用于视频通话)

**Vision Pro 联动**:Vision Pro 的眼动追踪与表情捕捉,本质是 TrueDepth 概念的延伸

## 安全设计

**反欺骗(Anti-Spoofing)**

- 拒绝照片(2D 图像无深度)
- 拒绝面具(深度匹配但纹理不符,且会检测眨眼、注视)
- 注视感知(Attention Aware):需要用户睁眼且看屏幕
- 持续学习面部变化(发型、胡须、眼镜、口罩)

**Secure Enclave**

面部模型不存云端、不出芯片,只存于 [[Secure Enclave]] 加密区域,Apple 自身也无法访问。

## 历史影响

TrueDepth 的引入意义远超人脸识别:
- 消除 Home 键,推动全面屏(刘海屏);后期演变为灵动岛(iPhone 14 Pro+)
- 把 3D 感知从工业(KinectV1)、AR/VR 设备带入主流消费市场
- 推动整个产业重新审视生物识别的隐私与精度标准

## 与替代方案的取舍

Apple 内部曾考虑屏下指纹方案,但选择 TrueDepth 路线:
- 优势:无需触摸,识别更"无感";安全性高;为 AR 铺路
- 劣势:占用屏幕空间(刘海/灵动岛);成本高;戴口罩失效(后通过 iPhone 12 Pro 起的"Face ID with Mask" 缓解)

## 参考源

- raw/iPhone/iPhone知识体系/03-功能特性层/生物识别/02-Face ID技术.md
- 相关:[[Face ID]]、[[Touch ID]]、[[Secure Enclave]]、[[计算摄影]]
