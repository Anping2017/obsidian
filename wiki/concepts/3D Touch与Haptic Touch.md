---
title: 3D Touch 与 Haptic Touch
type: concept
tags: [ios, mature]
sources: [raw/iPhone/]
created: 2026-05-05
updated: 2026-05-05
summary: 3D Touch 通过电容压力传感把"按多重"映射为新交互维度,Haptic Touch 用长按 + Taptic Engine 触感反馈达到相似效果但成本更低,Apple 在 2018 年起逐步用后者替代前者。
---

# 3D Touch 与 Haptic Touch

## 定义

**3D Touch** 是 Apple 在 2015 年 iPhone 6s 引入的压力触控技术,通过屏幕下电容应变传感器测量按压力度(轻、稍重、重),把"力的强度"作为新的输入维度。

**Haptic Touch** 是 Apple 自 2018 年(XR / SE 2)起逐步推广、并在 11 系列后全面替代 3D Touch 的方案,本质是**长按 + 振动反馈**——靠时间长短而非压力大小触发菜单,用 Taptic Engine 提供触感模拟"按下感"。

## 核心要点

**3D Touch 工作原理**

- 屏幕下方铺设电容应变片阵列
- 测量手指按压时屏幕的微小形变(亚毫米级)
- 形变量映射为 0-100 压力数值
- 配合 Taptic Engine(线性马达)给手指反馈"按下了"的振动

**3D Touch 三档交互**

1. **Peek**(轻按):预览内容,不真正打开
2. **Pop**(再用力):打开/进入完整界面
3. **快捷菜单**(用力按图标):弹出 App 自定义菜单(查看、删除、共享等)

**为什么被替代**

- **硬件成本**:压力传感器层让屏幕模组复杂、增厚、成本上升
- **使用率低**:大量用户从未发现 3D Touch 的存在或不会区分轻/重按
- **跨设备一致性**:iPad、SE 没有 3D Touch,iOS 设计需考虑兼容
- **Taptic Engine 已强**:振动反馈足够"伪造"按下感,长按 + 触感实现 90% 同等体验

**Haptic Touch 的差异**

- **触发方式**:长按(默认 0.5 秒)而非按压
- **没有压力级别**:只有"是否触发"二态
- **依赖 Taptic Engine**:第二代以后的线性马达精度足够
- **统一 iPad 与 iPhone**:全设备体验一致

**应用层 API 变化**

3D Touch 的 `UITouch.force` API 在 iOS 13+ 仍保留,但 Apple 推广开发者改用通用的 `UIContextMenuInteraction`,后者既支持 3D Touch 也支持 Haptic Touch。新代码应避免依赖压力值。

**Taptic Engine 的角色**

无论 3D Touch 还是 Haptic Touch,Apple 都靠 **Taptic Engine** 线性马达提供精细的触觉反馈——能模拟"咔哒"、"震动"、"敲击"、"心跳"等丰富节奏。这是 Apple 触觉差异化的硬件基础。

## 与其他概念的关系

3D Touch 是 [[Face ID]] 之外的另一项 iPhone 6s 时代标志性硬件创新,与 [[Touch ID]] 同处压力-生物识别探索期。其退场反映了 [[iPhone历代演进]] 中"非必要技术裁剪"的产品决策模式。Haptic Touch 现已是 iPhone / iPad 通用长按交互。

## 高频陷阱

- "Haptic Touch 不是 3D Touch 的简化"——是不同的触发机制(时间 vs 压力)
- iPad 从未支持 3D Touch,只有 Haptic Touch
- 老 App 的 Peek and Pop 在新机器上仍可工作(Haptic Touch 模拟)
- 锁屏快捷开关、3D Touch 拖动光标(在键盘上长按空格)在 Haptic Touch 时代仍保留功能但触发方式改长按

## 参考源

- raw/iPhone/(3D Touch / Haptic Touch 章节)
- 相关:[[iPhone历代演进]]、[[Face ID]]、[[Touch ID]]
