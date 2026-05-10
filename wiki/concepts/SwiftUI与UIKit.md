---
title: SwiftUI 与 UIKit(Apple 平台 UI 框架)
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: UIKit 是 iPhone 诞生(2008)以来 Apple 平台的命令式 UI 框架,SwiftUI 是 2019 年推出的声明式现代框架,二者长期共存——新功能用 SwiftUI,关键复杂场景仍依赖 UIKit。
---

# SwiftUI 与 UIKit(Apple 平台 UI 框架)

## 定义

**UIKit** 是 Apple 在 2008 年随 iPhone OS 2.0 推出的 iOS UI 框架,基于 Objective-C(后兼容 Swift),命令式风格——开发者显式创建视图、修改属性、响应事件。

**SwiftUI** 是 Apple 在 2019 年 WWDC 发布的现代 UI 框架,**声明式 + 数据驱动**,跨 iOS / macOS / watchOS / tvOS 统一,是 [[React]]、Flutter、[[Jetpack Compose]] 思路在 Apple 生态的对应。

二者将长期共存——新功能优先 SwiftUI,但 UIKit 仍是 Apple 平台底层与复杂场景核心。

## 设计哲学差异

**UIKit:命令式**

```swift
let label = UILabel()
label.text = "Hello"
label.font = UIFont.systemFont(ofSize: 18)
label.textColor = .blue
view.addSubview(label)
label.translatesAutoresizingMaskIntoConstraints = false
NSLayoutConstraint.activate([
    label.centerXAnchor.constraint(equalTo: view.centerXAnchor),
    label.centerYAnchor.constraint(equalTo: view.centerYAnchor),
])
```

显式创建对象、设置属性、布局约束、添加到父视图。

**SwiftUI:声明式**

```swift
struct ContentView: View {
    var body: some View {
        Text("Hello")
            .font(.title)
            .foregroundColor(.blue)
            .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}
```

只描述"UI 长什么样",框架负责创建/更新底层视图。

## SwiftUI 核心机制

**1. View Protocol**

所有 UI 都是 View 协议的实现:

```swift
protocol View {
    associatedtype Body: View
    var body: Self.Body { get }
}
```

值类型(struct),轻量,频繁重建。

**2. 数据流**

SwiftUI 数据流通过几种属性包装器:

- **@State**:View 内部状态(本地)
- **@Binding**:子 View 双向绑定父状态
- **@ObservedObject** / **@StateObject**:外部 ObservableObject(MVVM)
- **@EnvironmentObject**:全局共享(类似 React Context)
- **@Environment**:系统环境(如 colorScheme)

```swift
struct CounterView: View {
    @State private var count = 0

    var body: some View {
        VStack {
            Text("Count: \(count)")
            Button("Increment") { count += 1 }
        }
    }
}
```

@State 改变 → SwiftUI 自动重新计算 body → 视图更新。

**3. 修饰符链**

```swift
Text("Hello")
    .font(.title)
    .padding()
    .background(Color.blue)
    .cornerRadius(8)
    .shadow(radius: 4)
```

每个修饰符返回新 View,组合而非继承。

**4. 布局系统**

- VStack / HStack / ZStack(垂直/水平/层叠)
- LazyVStack / LazyHStack(懒加载)
- Grid(2.0+)
- 替代 Auto Layout 的简单组合式布局

## SwiftUI 演进时间线

| 版本 | 年份 | iOS | 关键特性 |
|---|---|---|---|
| 1.0 | 2019 | iOS 13 | 首发,功能基础 |
| 2.0 | 2020 | iOS 14 | App protocol、Lazy stacks、Grid |
| 3.0 | 2021 | iOS 15 | List 改进、AsyncImage、刷新 |
| 4.0 | 2022 | iOS 16 | NavigationStack、新表格、Charts |
| 5.0 | 2023 | iOS 17 | Observation 框架、Animations |
| 6.0 | 2024 | iOS 18 | iPad 多窗口、PreviewMacros |

每年 WWDC 都加大量新 API,但**iOS 17+ 才真正可用于复杂应用**——前几年 bug 多、性能不稳。

## 何时用 UIKit、何时用 SwiftUI

**用 SwiftUI**

- 新项目 iOS 16+ 起步
- 简单 / 中等复杂 UI
- 多平台共享代码(iOS + macOS + watchOS)
- 快速原型
- 视图层

**用 UIKit**

- iOS 14 以下兼容(SwiftUI 1.0 太弱)
- 复杂集合视图(UICollectionView 仍更强)
- 自定义渲染 / 动画(CALayer)
- 深度地图、视频播放等专业场景
- 老项目维护

**混用(主流)**

- UIHostingController:UIKit 中嵌入 SwiftUI
- UIViewRepresentable:SwiftUI 中嵌入 UIKit

实际工程中大部分新代码 SwiftUI、复杂部分 UIKit、二者打通。

## 与 React 类比

SwiftUI 与 [[React]] 思想极其相似:

| React | SwiftUI |
|---|---|
| Component | View |
| Props | 构造参数 |
| useState | @State |
| useReducer | @StateObject + ObservableObject |
| Context | EnvironmentObject |
| useEffect | onAppear / task / onChange |
| Render | body |
| 虚拟 DOM diff | View tree diff |
| JSX | DSL |

熟悉 React 的人转 SwiftUI 几天就上手。

## 与 Jetpack Compose 类比

[[Jetpack Compose]](Android)与 SwiftUI 几乎是同一思想:

- 声明式
- @Composable / View
- remember / @State
- 数据驱动 UI
- 跨平台尝试(Compose Multiplatform、SwiftUI 限 Apple)

Apple 与 Google 几乎同期推出现代 UI 框架,反映行业共识。

## 性能与陷阱

**1. body 重建**

@State 改变 → 整个 body 重建。复杂层级影响性能。
- 拆分 View(让小范围重建)
- 使用 EquatableView / Equatable 短路

**2. ForEach 性能**

```swift
ForEach(items) { item in CardView(item: item) }
```

需 items 是 Identifiable 或提供 id 闭包,否则全量重建。

**3. List vs ScrollView**

- List 自动复用 cells(类似 UITableView)
- ScrollView + LazyVStack 大列表也 OK
- ScrollView + VStack 全部加载,小列表用

**4. NavigationStack 内存**

push 多层不释放,需小心。iOS 17 改进。

## SwiftUI 局限

- **历史包袱兼容差**:很多 UIKit API 没对应
- **自定义动画复杂**:简单 .animation() 易,复杂时序难
- **视图层级调试**:不像 UIKit 有 View Debugger
- **第三方库少**:很多库仍是 UIKit
- **测试**:UI 测试支持弱(快照测试社区方案)
- **macOS 体验**:工具栏、菜单栏支持不及 AppKit

## UIKit 仍是核心的场景

**1. UICollectionView Compositional Layout**

复杂自适应网格(App Store 首页那种)SwiftUI 还做不好。

**2. CoreAnimation 自定义渲染**

CALayer + 自定义绘制超出 SwiftUI 范畴。

**3. Camera / AVFoundation 整合**

Video 预览层、滤镜需要 UIKit 桥接。

**4. PDFKit / WKWebView**

仍要 UIViewRepresentable。

**5. 极致性能要求**

UICollectionView + DiffableDataSource 性能仍最优。

## 与 React Native / Flutter 选择

**SwiftUI**

- iOS / Apple 生态最佳体验
- Swift 语言,类型安全
- 直接调 iOS 系统 API
- 不能跨 Android

**[[React Native]]**

- 跨 iOS / Android
- JavaScript / TypeScript
- 性能略差于原生
- Hot Reload 开发体验好

**[[Flutter]]**

- 跨平台(包括 Web、Desktop)
- Dart 语言
- 自己绘制(不用系统组件)
- 一套代码多平台

苹果生态独占应用 → SwiftUI;跨平台 → React Native / Flutter。

## 和其他概念的关系

SwiftUI 与 [[Jetpack Compose]]、[[React]]、[[Flutter]] 共同代表 2019-2025 声明式 UI 框架的"全行业共识"。它们都借鉴 [[React]] 的虚拟 DOM + 单向数据流思想。

它的 @State / @Binding 数据流模式与 [[Redux状态管理]]、[[Zustand状态管理]] 等状态库共享 [[设计原则SOLID]] 中的单一职责思想——状态集中、视图被动反应。

SwiftUI 与 [[Xcode开发工具]]、Swift 语言、Apple 生态深度绑定,与 [[Apple生态系统]] 中 iCloud、HealthKit、HomeKit 等服务自然整合,是 [[Apple Watch]]、CarPlay 等设备开发首选。

## 参考源

- raw/计算机/
- 相关:[[Xcode开发工具]]、[[Apple生态系统]]、[[React]]
