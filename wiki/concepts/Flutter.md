---
title: Flutter
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Flutter 是 Google 推出的跨平台 UI 框架,用 Dart 语言 + 自有渲染引擎(Skia/Impeller),不依赖原生组件、自己绘制每个像素,在 iOS/Android/Web/Desktop 上提供高度一致的 UI 与体验。
---

# Flutter

## 定义

**Flutter** 是 Google 在 2017 年发布(2018 GA)的开源 UI 框架。它的核心创新是**不依赖平台原生 UI 组件,而是用自有渲染引擎(早期 Skia,2023+ 自研 Impeller)直接绘制每个像素**,在不同平台上呈现高度一致的 UI 与动画。

支持平台:
- iOS / Android(主战场)
- Web(2021 GA,适合简单交互)
- macOS / Windows / Linux Desktop
- Embedded(车载、IoT)

Flutter 与 [[React Native]] 是当前跨平台移动开发主流,但思路截然不同——RN 桥接原生组件,Flutter 自己绘制。

## 核心架构

**1. Dart 语言**

Google 设计的语言:
- 类 JavaScript / TypeScript 语法
- AOT(Ahead of Time)编译为原生 ARM
- JIT 模式开发期热重载
- 单线程 + Isolate 并行

Dart 在 Flutter 之前几乎没采用,Flutter 是它的杀手应用。

**2. Skia / Impeller 渲染引擎**

- Skia:Google 2D 图形库,Chrome 也用
- Impeller(2023+):Flutter 团队自研,解决 Skia 着色器编译卡顿(Jank)
- iOS 用 Impeller,Android 渐进迁移

**3. Widget 树**

一切都是 Widget:
- 文本、按钮、布局、动画、甚至 padding 都是 Widget
- 不可变(immutable),状态通过 StatefulWidget 配 State 类持有
- 深度组合而非继承

```dart
class CounterApp extends StatefulWidget {
  @override
  State<CounterApp> createState() => _CounterState();
}

class _CounterState extends State<CounterApp> {
  int count = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $count'),
        ElevatedButton(
          onPressed: () => setState(() => count++),
          child: Text('Increment'),
        ),
      ],
    );
  }
}
```

**4. 三层 Widget 体系**

- StatelessWidget:无状态
- StatefulWidget:有状态
- InheritedWidget:跨层级数据传递(类似 React Context)

**5. 渲染管道**

```
Widget tree → Element tree → Render tree → Layer tree → GPU
```

Flutter 自己掌控全过程,不走 iOS UIView / Android View。

## 与 React Native 对比

| 维度 | Flutter | [[React Native]] |
|---|---|---|
| 语言 | Dart | JavaScript / TS |
| 渲染 | 自绘 | 原生组件桥接 |
| UI 一致性 | 跨平台 100% 一致 | 平台原生外观 |
| 性能 | 高(无桥接) | 中(桥消耗) |
| 学习曲线 | Dart 新语言 | JS / RN |
| 包体积 | 大(20+ MB) | 中 |
| 启动速度 | 略慢(引擎初始化) | 快 |
| 原生 API | Plugin / Method Channel | Native Module |
| 生态 | pub.dev,中等 | npm 巨大 |
| Hot Reload | 极佳 | 良好 |
| 适合 | 设计严谨 / 自定义 UI | 快速开发 / 已有 React 团队 |

## 与原生开发对比

| 维度 | Flutter | iOS 原生 | Android 原生 |
|---|---|---|---|
| 跨平台 | 是 | 否 | 否 |
| 性能 | 90% | 100% | 100% |
| 平台特性接入 | 需 Plugin | 原生 | 原生 |
| UI | 跨平台一致 | iOS 原汁原味 | Material |
| 团队成本 | 1 套代码 1 套人 | 2 套人 | |
| 长期维护 | 单语言 | 双语言 | |

## 何时选 Flutter

**应该选**

- 需要跨 iOS + Android,代码尽量共享
- UI 设计严谨,要在两端一致
- 团队 Dart 学习意愿
- 需要 Web + Desktop 也部署
- 创业 MVP

**不应选**

- 重度依赖平台特性(AR、ML、复杂 Camera)
- 团队已深耕 React(选 RN 更好)
- 极致性能要求
- 第三方 SDK 没 Flutter 适配

## Flutter 框架特性

**1. Hot Reload**

修改代码,1 秒内更新到运行中的 App,保留状态。开发体验顶级,是 Flutter 杀手锏。

**2. 自适应 UI**

- Material(Android 风)
- Cupertino(iOS 风)
- 同一应用可按平台切换

```dart
Theme.of(context).platform == TargetPlatform.iOS
    ? CupertinoButton(...)
    : ElevatedButton(...)
```

**3. 动画**

- AnimationController + Tween
- ImplicitlyAnimatedWidget(简单)
- Hero animations(跨页面)
- Rive、Lottie 集成

**4. 状态管理**

无官方钦定,流行方案:
- **Provider**(官方推荐入门)
- **Riverpod**(Provider 进化版)
- **Bloc**(企业级)
- **GetX**(中国流行,争议大)
- **MobX**

类似 [[React]] 状态管理百花齐放。

## 商业采用

**Google 自家**

- Google Pay
- Google Earth(Web)
- Stadia(已停)
- Classroom 部分

**第三方**

- BMW My BMW App
- eBay Motors
- Toyota IVI
- 阿里巴巴 Xianyu(闲鱼)
- 腾讯部分内部应用
- Realtor.com

Flutter 在中国和中等规模国际产品中流行,顶级互联网巨头(Meta、Microsoft)较少全面采用。

## Dart 语言要点

**特性**

- Null Safety(2.12+)
- async / await
- 模式匹配(3.0+)
- 扩展方法(extension)
- mixin

**与 Kotlin / TypeScript 对比**

- 简单清晰
- 类型推导
- 没有 Kotlin Coroutines / TS 高级类型系统
- 谷歌内部用得不多(主要 Flutter)

## 局限

**1. 包体积**

最小 Flutter App 安装包 20+ MB(引擎+框架)。Web 端 Wasm 包数 MB,首屏慢。

**2. 第三方库**

- pub.dev 主流功能有
- 长尾库少
- 复杂场景(支付、Map)Plugin 质量参差

**3. iOS 风格不完全原生**

Cupertino 接近但不等于真原生 UIKit / SwiftUI 体验。Apple 用户察觉到差异。

**4. Web 性能与 SEO**

Web 端基于 CanvasKit / HTML 渲染,SEO 弱,首屏慢,适合应用而非内容站。

**5. 桌面端稍显粗糙**

Windows / macOS Desktop 仍在改进,Toolbar、菜单等标准组件未必精致。

**6. AR / 复杂相机**

ARKit / ARCore 接入需大量 Platform Channel 代码,效率不如原生。

## Flutter 生态工具

- **Flutter SDK + Dart SDK**
- **Android Studio / VS Code Plugin**
- **DevTools**:Inspector、Performance、Network
- **fvm**:Flutter 版本管理
- **fastlane**:iOS / Android 发布
- **Codemagic / Bitrise**:CI/CD

## 与 Compose Multiplatform 竞争

[[Jetpack Compose]] Multiplatform(KMP)2024 起在 iOS 也能跑,与 Flutter 直接竞争跨平台:
- Compose KMP:Kotlin 全栈,Android 原生强
- Flutter:Dart,跨平台 UI 最一致
- React Native:JS,Web 团队迁移最顺

预计 2025-2027 跨平台生态会进一步分化。

## 工程实践

**1. 单仓多包**

melos 工具管理 monorepo:
- core:业务逻辑
- ui:共用 UI
- mobile:App 入口
- web:Web 入口

**2. 状态管理选型**

- 简单:Provider / Riverpod
- 复杂业务:Bloc
- 跨页面共享多:Riverpod

**3. 测试**

- Unit:flutter_test
- Widget:WidgetTester
- Integration:flutter_driver(已弃)/ patrol
- 黄金截图测试:golden tests

## 和其他概念的关系

Flutter 与 [[React Native]]、[[SwiftUI与UIKit|SwiftUI]]、[[Jetpack Compose]] 共同构成移动开发框架全景。它的"自绘渲染"思路与 [[Tauri]](Web 引擎渲染桌面)互补,代表跨平台 UI 的两种路径——自绘 vs 嵌入 Web。

Flutter 体现 [[设计原则SOLID]] 中的"单一职责" + 组合优于继承——一切是 Widget,通过组合而非继承构造 UI,与 [[React]] 哲学一致。

它的 Hot Reload 开发体验对 [[CI_CD流水线]] 中的"快速反馈循环"理念有所启发——本地开发也应有亚秒级反馈,这是工程效率的核心指标。

## 参考源

- raw/计算机/
- 相关:[[SwiftUI与UIKit]]、[[Jetpack Compose]]、[[React]]
