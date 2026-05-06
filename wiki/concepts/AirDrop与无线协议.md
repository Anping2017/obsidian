---
title: AirDrop 与无线协议
type: concept
tags: [ios, mature]
sources: [raw/iPhone/iPhone知识体系/02-技术规格层/连接通信/02-无线连接技术.md, raw/iPhone/iPhone知识体系/02-技术规格层/连接通信/01-网络制式支持.md]
created: 2026-05-05
updated: 2026-05-05
summary: AirDrop 是 Apple 设备间利用 Bluetooth LE 发现 + Wi-Fi P2P 传输的私有协议,UWB 提供精准方向定位,共同构成 Apple 生态独享的近场体验。
---

# AirDrop 与无线协议

## 定义

AirDrop 是 Apple 设备间基于自有协议簇的近场文件传输能力。表面看是"两台 iPhone 凑近就能传图",底层却是一套 **Bluetooth LE 发现 + Wi-Fi Direct(P2P)传输 + UWB 方向感知** 的复合协议。它和 [[Apple生态系统]] 中的 Handoff、Universal Clipboard、Continuity 共享同一套发现机制。

## 核心要点

### 工作流程

1. **发现**:Bluetooth LE 广播匿名标识,识别附近 Apple 设备
2. **认证**:基于 iCloud 联系人或公开身份握手
3. **方向感知(UWB)**:iPhone 11 起内置 U1/U2 芯片,以厘米级精度判断"对方在哪"
4. **建立连接**:Wi-Fi Direct 临时建链(不经路由器)
5. **传输**:加密通道直传,不经 Apple 服务器

### 涉及的无线协议

- **Wi-Fi 6 / 6E**:6 GHz 频段,9.6 Gbps 上限,低延迟
- **Bluetooth 5.3**:LE 广播 + 经典传输,功耗优化
- **NFC**:4 cm 内,Apple Pay、交通卡、门禁
- **UWB(超宽带)**:厘米级定位,AirTag、CarKey、AirDrop 方向
- **GPS / GLONASS / Galileo**:多卫星系统融合定位

### 设计哲学

AirDrop 体现了 Apple 协议设计的两个偏执:
- **私有 + 优雅**:协议不开源,但用户不用配置任何 IP/密码
- **就近、离线优先**:不依赖云端,机场没网也能传

### 安全与隐私

- 身份分"所有人 / 仅联系人 / 关闭"三档
- iOS 16.2 起,中国大陆地区"所有人"模式自动 10 分钟超时(政策因素)
- 传输全程端到端加密
- 无 Apple ID 时只能匿名,接收方需手动确认

### 实际应用

AirDrop 是用户每天感知最强的"Apple 体验"之一:跨设备粘贴 PDF、摄影师当场传 RAW 文件、家庭成员秒传视频。这种"零配置"的便利,正是 [[Apple生态系统]] 锁定效应的来源之一。

## 关系

- 是 [[Apple生态系统]] 的核心协议组件
- 受 [[iOS系统架构]] 的 Core Services 层 API 暴露
- UWB 模块由 [[A系列芯片]] 同期推出的 U1/U2 协处理器实现

## 参考源

- raw/iPhone/iPhone知识体系/02-技术规格层/连接通信/02-无线连接技术.md
- raw/iPhone/iPhone知识体系/02-技术规格层/连接通信/01-网络制式支持.md
