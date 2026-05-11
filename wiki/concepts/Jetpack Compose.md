---
title: Jetpack Compose
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Jetpack Compose 是 Google 在 2021 年推出的 Android 现代声明式 UI 框架,基于 Kotlin 编译器插件实现,以 @Composable 函数和状态驱动模型取代命令式 View 体系,是 Android 平台未来五到十年主流 UI 方案。
---

# Jetpack Compose

## 定义

**Jetpack Compose** 是 Google 在 2021 年发布(Compose 1.0)的 Android 现代声明式 UI 框架。它基于 [[Kotlin]] 编译器插件,把"如何构建 UI"从命令式 View 体系改为**用普通函数声明 UI 结构,状态变化时自动重组**。

它与 [[SwiftUI与UIKit|SwiftUI]]、[[React]]、[[Flutter]] 共同代表 2019-2025 声明式 UI 全行业共识。Compose 不仅是 Android,还有 Compose Multiplatform(支持 Desktop、Web、iOS),是 Kotlin 多平台战略关键。

## 与传统 Android UI 对比

**传统 View 系统**

- XML 布局 + Java/Kotlin 代码
- ViewGroup 树、各种 LayoutManager
- findViewById / View Binding 取引用
- 显式更新视图属性
- 数据与视图耦合

**Compose**

- 全 Kotlin,无 XML
- @Composable 函数声明 UI
- 状态驱动重组
- 函数即组件

```kotlin
@Composable
fun Greeting(name: String) {
    Text(text = "Hello, $name!")
}

@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }
    Column {
        Text("Count: $count")
        Button(onClick = { count++ }) {
            Text("Increment")
        }
    }
}
```

## 核心概念

**1. @Composable**

特殊编译期注解。Compose 编译器插件转换为可重组函数,带跳过、智能重组等能力。

**2. State / remember**

- mutableStateOf:可观察状态
- remember:跨重组保留值
- rememberSaveable:跨配置变化保留(屏幕旋转)

```kotlin
val count by remember { mutableStateOf(0) }
```

**3. Recomposition**

State 变 → 依赖该 State 的 Composable 重组(只跑函数,不重创建底层节点)。Compose 编译器优化:只重组真正需要的部分。

**4. ViewModel + StateFlow**

业务状态在 ViewModel 中:
```kotlin
class CounterViewModel : ViewModel() {
    private val _count = MutableStateFlow(0)
    val count: StateFlow<Int> = _count

    fun increment() { _count.value++ }
}

@Composable
fun Counter(vm: CounterViewModel = viewModel()) {
    val count by vm.count.collectAsState()
    Column {
        Text("Count: $count")
        Button(onClick = vm::increment) { Text("Inc") }
    }
}
```

**5. 副作用(Side Effects)**

- LaunchedEffect:启动协程
- DisposableEffect:有清理的副作用
- SideEffect:每次重组都跑(轻量)
- produceState:State 来自 Flow / Future

类似 React 的 useEffect 家族。

## 布局系统

**基础容器**

- Column:垂直
- Row:水平
- Box:层叠(类似 FrameLayout)

**Modifier 链**

```kotlin
Text(
    "Hello",
    modifier = Modifier
        .padding(16.dp)
        .background(Color.Blue)
        .clickable { /* ... */ }
        .fillMaxWidth()
)
```

类似 [[SwiftUI与UIKit|SwiftUI]] 的 ViewModifier。顺序敏感(padding 在 background 前后效果不同)。

**列表**

- LazyColumn / LazyRow(对应老 RecyclerView)
- LazyVerticalGrid
- 自动复用,大列表性能 OK

**约束布局**

- ConstraintLayout(独立库)
- 复杂自适应布局

## Material 设计

- material3:Material You(Android 12+)动态色彩
- 内置主题、暗黑模式、Typography
- material:Material 2(老)

## 互操作性

**Compose 在 View 中**

```xml
<androidx.compose.ui.platform.ComposeView
    android:id="@+id/compose_view"
    .../>
```

```kotlin
findViewById<ComposeView>(R.id.compose_view).setContent {
    MyComposable()
}
```

**View 在 Compose 中**

```kotlin
AndroidView(factory = { context -> MapView(context) })
```

让 GoogleMap、ExoPlayer、WebView 等仍用 View 系统时无缝集成。

## Compose 编译器魔法

**核心创新**

Compose 不是普通 Kotlin DSL——它有专用编译器插件:

1. 给每个 @Composable 函数加 Composer 参数
2. 加 group 跟踪重组边界
3. 智能跳过(参数未变 → 不重组)
4. 状态读取自动登记依赖

这让"声明式 + 高性能"成为可能,与 React Fiber 思路同源但实现更激进。

## 与 React 类比

| React | Compose |
|---|---|
| Component | @Composable |
| useState | remember + mutableStateOf |
| useEffect | LaunchedEffect / SideEffect |
| Context | CompositionLocal |
| Memo | derivedStateOf |
| 虚拟 DOM | Composition tree |
| Reconciliation | Recomposition |
| Render | 函数调用 |

熟 React 的开发者上手 Compose 极快。

## 与 SwiftUI 对比

| 维度 | Compose | [[SwiftUI与UIKit|SwiftUI]] |
|---|---|---|
| 平台 | Android(+ KMP) | Apple |
| 语言 | Kotlin | Swift |
| 状态 | mutableStateOf | @State |
| 副作用 | LaunchedEffect | task / onAppear |
| 工具 | Android Studio | Xcode |
| 类型推导 | 极强 | 强 |
| 跨平台 | KMP 支持 | 不支持 |
| 调试 | Layout Inspector + Composition tracing | View hierarchy |

二者思想高度一致,选择基于平台。

## Compose Multiplatform

JetBrains 把 Compose 移植到:
- Desktop(Windows / macOS / Linux)
- Web(Wasm 实验性)
- iOS(2024 GA,与 SwiftUI 共存)

愿景:**一套 UI 代码跑所有平台**。挑战:
- iOS 上不如 SwiftUI 原生流畅
- Web 上 Wasm 包大
- 平台特性仍需各自实现(原生 API)

仍是新生事物,2024-2025 处于早期生产采用阶段。

## 性能与陷阱

**1. 不稳定参数导致全量重组**

参数是 List<Item> 等"不稳定"类型时,Compose 假设它每次都不同 → 重组太多:

```kotlin
@Composable
fun List(items: List<Item>) { /* List 不是 stable,会全量重组 */ }
```

解决:用 ImmutableList(kotlinx.collections.immutable)或 @Stable 注解。

**2. lambda 重建**

```kotlin
Button(onClick = { vm.increment() }) { /* lambda 每次新对象 */ }
```

Compose 1.2+ 编译器自动 remember lambda,无需手动。

**3. derivedStateOf**

只在派生值变化时触发:
```kotlin
val isEnabled by remember { derivedStateOf { input.length > 3 } }
```

避免 input 每个字符都重组依赖 isEnabled 的 UI。

**4. CompositionLocal 滥用**

类似 React Context,频繁更新会触发大量重组。

## 测试

**1. Compose Test API**

```kotlin
composeTestRule.setContent { Counter() }
composeTestRule.onNodeWithText("Count: 0").assertExists()
composeTestRule.onNodeWithText("Increment").performClick()
composeTestRule.onNodeWithText("Count: 1").assertExists()
```

**2. Preview**

```kotlin
@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    Greeting("Android")
}
```

Android Studio 实时预览,无需运行 App。

**3. 截图测试**

Paparazzi、Roborazzi:截图比对回归。

## 局限

- 学习曲线(对老 Android 开发者)
- 编译稍慢(编译器插件)
- 调试有时反直觉(重组追踪)
- 工具(Layout Inspector)成熟度提升中
- 第三方库仍部分基于 View(Map、Camera)
- iOS 移植不是真正生产级(对比 SwiftUI)

## Android 现代栈(2024+)

完整现代 Android 栈:
- **UI**:Jetpack Compose
- **状态**:ViewModel + StateFlow
- **导航**:Navigation Compose
- **DI**:Hilt(Dagger 简化)
- **网络**:Retrofit + OkHttp + kotlinx.serialization
- **数据库**:Room + Flow
- **协程**:Kotlin Coroutines
- **图片**:Coil
- **构建**:Gradle + Kotlin DSL

## 和其他概念的关系

Jetpack Compose 与 [[SwiftUI与UIKit|SwiftUI]]、[[React]]、[[Flutter]] 共同代表声明式 UI 框架全行业共识。它依赖 [[Kotlin]] 语言特性(Coroutines、Flow、Type System)实现强表达力。

它的 ViewModel + StateFlow 数据流与 [[Redux状态管理]]、[[Zustand状态管理]] 等同源,体现单向数据流的"事实上的共识"。在 [[微服务]] 时代,移动端 UI + 后端 API + [[GraphQL]] / [[RESTful API]] 构成现代应用全链路。

Compose 与 [[Vim哲学]]、[[Vite]] 等其他现代工具一样,体现"重新设计基础原语"的工程价值——不止是新 API,而是范式转移。

## 参考源

- raw/计算机/
- 相关:[[SwiftUI与UIKit]]、[[React]]、[[Kotlin]]
