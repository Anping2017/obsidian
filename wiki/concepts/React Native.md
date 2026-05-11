---
title: React Native
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: React Native 是 Facebook 在 2015 年开源的跨平台移动框架,用 JavaScript + React 编写代码,通过桥接调用 iOS/Android 原生组件,在不牺牲原生体验的前提下让 Web 团队复用技能开发移动应用。
---

# React Native

## 定义

**React Native(RN)** 是 Facebook(Meta)在 2015 年开源的跨平台移动开发框架。它的核心命题:**用 [[React]] 思想 + JavaScript 编写代码,但 UI 渲染为真正的原生组件**——iOS 上是 UIView、Android 上是 View——而不像 [[Flutter]] 那样自绘。

它让数百万 React 前端工程师无缝转移动开发,把"写一份代码,跑两个平台"做成商业可行。Instagram、Facebook、Discord、Shopify、Microsoft Office 等都用 RN。

## 与 Flutter 的根本差异

| 维度 | React Native | [[Flutter]] |
|---|---|---|
| 渲染 | 桥接原生组件 | 自绘 Skia/Impeller |
| 语言 | JS / TypeScript | Dart |
| UI 一致性 | 各平台原生外观 | 跨平台一致 |
| 性能 | 中(桥接消耗) | 高 |
| Hot Reload | 良好 | 极佳 |
| 生态 | npm 巨大 | pub.dev 中等 |
| 学习曲线 | 已有 React 团队近零 | Dart 新语言 |
| 跨平台 | iOS/Android 主,Web 辅 | iOS/Android/Web/Desktop |

哲学差异:
- **RN**:尊重平台习惯,iOS 用户看到 iOS 风,Android 用户看到 Material
- **Flutter**:跨平台像素一致,品牌 UI 比平台习惯重要

## 架构演进

**老架构(2015-2022)**

```
JavaScript 线程 ←→ Bridge(异步,JSON)←→ Native 线程
```

JS 线程跑业务逻辑、React 协调,通过 Bridge 异步发送序列化命令到 Native 线程渲染。问题:
- Bridge 序列化开销
- 异步导致动画掉帧
- 大列表滚动卡顿

**新架构(Fabric + TurboModules,2022+)**

- **JSI(JavaScript Interface)**:JS 直接持有 Native 对象引用,同步调用
- **Fabric**:新渲染器,用 C++ 实现 Shadow Tree,跨平台共享
- **TurboModules**:同步、惰性加载的 Native Module
- **Codegen**:自动生成 JS ↔ Native 类型安全代码

新架构性能大幅提升,接近 Flutter。

## React Native 代码示例

```jsx
import React, { useState } from 'react'
import { View, Text, Button, StyleSheet } from 'react-native'

export default function Counter() {
  const [count, setCount] = useState(0)

  return (
    <View style={styles.container}>
      <Text style={styles.text}>Count: {count}</Text>
      <Button title="Increment" onPress={() => setCount(count + 1)} />
    </View>
  )
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  text: { fontSize: 20, marginBottom: 20 }
})
```

熟悉 React 的开发者几小时就能动手——只要换 div → View、span → Text 等。

## 核心组件

- View / Text / Image / ScrollView / FlatList / SectionList
- TouchableOpacity / Pressable
- TextInput
- Modal / Alert
- StyleSheet(用 Flexbox 布局)
- Animated / Reanimated

## 平台 API 与 Native Module

**JavaScript 层**

```javascript
import { Platform, NativeModules } from 'react-native'

if (Platform.OS === 'ios') { /* iOS */ }

NativeModules.MyCustomModule.doSomething()
```

**Native Module(自定义 iOS Swift / Android Kotlin)**

桥接到 JS,处理摄像头、蓝牙等。React Native 0.68+ 起 TurboModules 自动生成接口。

## 生态

**框架**

- **React Native CLI**:官方
- **Expo**:管理工具,免编译,适合快速开发
- **Ignite**:CLI 模板
- **React Native Reanimated 3**:动画
- **React Navigation**:导航
- **Redux / Zustand / MobX / Recoil**:状态管理
- **TanStack Query**:数据获取
- **NativeWind**:Tailwind CSS for RN

**Expo vs Bare**

- Expo:一切托管,JS 即可,但限制原生能力
- Bare:自己管 Xcode / Android Studio,完全自由

2024 年 Expo 几乎是 RN 默认入门方式。

## 商业采用

**Meta**

- Facebook、Instagram、Messenger 部分
- Marketplace、Shop 等

**其他大厂**

- Microsoft:Office 部分、Outlook 部分、Teams 部分
- Discord:全 RN
- Shopify:从原生迁 RN
- Tesla:车载 App
- Pinterest、Airbnb(2018 放弃)、Uber Eats、Walmart

**Airbnb 放弃事件**

2018 年 Airbnb 公开宣布放弃 RN,理由:维护双轨成本、Native 性能不足、招聘困难。引发巨大讨论。但同期 Discord、Shopify 大规模采用 RN,显示"是否合适"取决于团队、产品阶段、性能要求。

## 性能关键

**1. FlatList 优化**

- keyExtractor
- getItemLayout(已知行高时跳过测量)
- removeClippedSubviews

**2. Image**

- 用 react-native-fast-image 或 Expo Image(更优)
- 缓存策略
- 缩略图先行

**3. 动画**

- 用 Reanimated 而非 Animated(避免 JS 线程开销)
- worklets:在 UI 线程跑 JS 函数

**4. Bridge 优化(老架构)**

- 减少跨桥调用
- 批量通信
- 避免每帧通过 Bridge

新架构(Fabric + TurboModules)大部分自动解决。

## 调试

- Flipper(Meta 推出,2023 年宣布弃用)
- React Native Debugger(老牌,Chrome DevTools 风)
- React DevTools
- Reactotron
- 直接 Chrome / Safari Web Inspector(JS 调试)

## 局限

- 包体积比 Native App 大
- 启动慢(JS 引擎初始化)
- 部分 Native API 需自己写桥
- 与新 iOS / Android 特性同步滞后(RN 0.x 节奏)
- 升级频繁,迁移痛苦
- 性能不及 Native(尤其复杂动画、相机)
- Web RN(react-native-web)碎片化

## 与 React for Web 共享代码

**最佳实践**

- 业务逻辑:hooks、reducers、API client 全跨平台
- UI 组件:抽象 Atomic 后各自实现
- 状态管理:Redux / Zustand 通用

**框架**

- Solito:Next.js + RN 共享路由
- React Native Web:RN 组件跑 Web

实际工程难做到 100% 共享,80% 业务逻辑共享 + 20% 平台 UI 是合理目标。

## RN 趋势(2024-2025)

- **新架构(Fabric + TurboModules)成熟**:大部分主流库适配
- **Expo 全栈方案**:从开发到部署托管
- **Server Components for RN**(实验):服务端渲染部分 UI
- **AI 辅助 RN**:GitHub Copilot、Cursor 对 RN 友好
- **与 Compose Multiplatform / Flutter 三足鼎立**

## 与同行对比时的取舍

**选 RN**

- 已有 React 团队
- 跨平台 + 平台原生体验
- 需要复用 Web 业务逻辑
- 渐进式集成到老应用(嵌入)

**选 Flutter**

- UI 设计极致一致
- 性能要求高
- 不在乎学新语言

**选原生**

- 极致性能
- 重度依赖平台特性
- App Store / Play 出色评价对核心业务关键
- 团队充足

**选 Capacitor / Ionic**

- 完全 Web 团队,可接受 WebView 体验
- 极快出 PoC

## 和其他概念的关系

React Native 是 [[React]] 思想在移动端的延伸,与 [[Flutter]]、[[SwiftUI与UIKit|SwiftUI]]、[[Jetpack Compose]] 共同构成移动 UI 框架四方。它把 Web 工程师无缝带入移动开发,体现"同一抽象跨平台复用"的工程价值。

它的"桥接原生组件"思路在 [[Tauri]](桥接 Web 引擎)中也有体现——都是"重用现有引擎"思路。Reanimated 库的 Worklet 概念与 [[WebAssembly]] 一脉相承——把性能敏感代码搬到独立运行时。

RN 与 [[GraphQL]]、[[RESTful API]]、[[BFF]] 等后端架构紧密配合,形成"前端 + RN 移动端 + 后端"完整应用栈。

## 参考源

- raw/计算机/
- 相关:[[Flutter]]、[[React]]、[[SwiftUI与UIKit]]
