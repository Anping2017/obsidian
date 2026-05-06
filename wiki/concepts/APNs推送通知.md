---
title: APNs 推送通知
type: concept
tags: [ios, network, stub]
sources: []
created: 2026-05-05
updated: 2026-05-05
summary: Apple Push Notification service,Apple 提供的统一推送通道,App 服务端通过它把通知送达 iOS 设备,是 iOS 后台限制下保持实时性的核心机制。
---

# APNs 推送通知

## 定义

**APNs**(Apple Push Notification service)是 Apple 在 2009 年随 iOS 3 推出的**统一推送通道**,作为 [[iOS系统架构]] 后台限制策略下,App 服务端把通知实时送达设备的官方渠道。它由 Apple 在云端长期维护一个与每台设备的持久 TLS 连接,App 服务端只需把消息发给 APNs,APNs 再分发到目标设备,从而在严格限制后台进程的前提下仍保留实时性。

## 核心要点

### 工作流程

1. **App 启动**:向 APNs 注册,获得唯一的 device token
2. **App 把 token 上报后端**
3. **后端有事件时**:用证书或 Token-based 鉴权,把 payload 提交给 APNs
4. **APNs 通过持久连接** 把通知推送到设备
5. **设备 SpringBoard** 决定如何展示(横幅、声音、徽章、列表)

### 通知类型

- **Alert**:屏幕上显示文本
- **Sound**:声音提示
- **Badge**:App 图标右上角红点数字
- **Silent**(`content-available: 1`):静默推送,触发 App 短暂后台执行
- **Provisional**:临时授权,无需用户主动授权
- **Critical Alert**:即使勿扰模式也能响,医疗等场景使用

### 关键特点

- **持久连接**:设备与 APNs 之间常驻 TCP/TLS 连接,共享单一连接给所有 App
- **节能**:统一通道避免每个 App 各自轮询
- **可靠性**:APNs 不保证 100% 送达,QoS 1 默认丢弃旧消息以避免堆积
- **限速**:Apple 对发送方有严格速率与 token 复用限制

### 用户授权与隐私

- 首次推送前需用户授权(允许/拒绝)
- iOS 12 起引入 Provisional Authorization、Notification Grouping
- iOS 15 引入"通知摘要"——批量整理、定时呈现
- 与 [[iOS隐私机制]] 紧密协同:用户可随时关闭、限制单个 App 的推送

### 协议与演进

- 1.x:基于二进制 socket 协议,长连接
- HTTP/2 时代(2016+):RESTful 接口,更易调试
- Token-based 鉴权(JWT)取代部分场景的证书鉴权

## 和其他概念的关系

- 是 [[iOS系统架构]] 后台限制策略下保持实时性的关键
- 直接服务于 [[iPhone电池技术]] 的省电目标——避免 App 轮询
- 是 [[Apple生态系统]] 通讯一致性的基础设施(iMessage、FaceTime 也走类似机制)
- 协议设计反映了 [[A系列芯片]] 网络协处理器的低功耗优化

## 参考源

待补充(领域:iOS 开发、网络协议)
