---
title: CSS 盒模型
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/语言/CSS/02-核心理解层/盒模型/]
created: 2026-05-05
updated: 2026-05-05
summary: CSS 盒模型把每个元素视为内容、内边距、边框、外边距四层嵌套的矩形,标准盒模型 width 不含 padding/border,IE 怪异盒模型相反,box-sizing 统一切换。
---

# CSS 盒模型

## 定义

**CSS 盒模型(Box Model)** 是 CSS 渲染的基本单元:每个 HTML 元素都被视为一个矩形盒子,由四层从内到外嵌套构成 —— **content(内容)→ padding(内边距)→ border(边框)→ margin(外边距)**。盒模型决定元素占据的空间和与周围元素的关系。

## 核心要点

### 1. 四层结构

```
+------------------ margin ------------------+
|  +-------------- border --------------+    |
|  |  +-------- padding --------+       |    |
|  |  |       content           |       |    |
|  |  +-------------------------+       |    |
|  +------------------------------------+    |
+--------------------------------------------+
```

- **content**:文本/子元素占据的核心区域
- **padding**:内容与边框间空白(背景延伸至此)
- **border**:边框线(可见、占空间)
- **margin**:外边距(透明,与相邻盒子的距离)

### 2. 标准盒模型(W3C)

`box-sizing: content-box`(默认)
```
盒子总宽 = width + padding-left + padding-right + border-left + border-right
```

设 `width: 200px; padding: 20px; border: 5px` → 实际占据 250px。修改 padding 会撑大整体,布局意外频发。

### 3. 怪异盒模型(IE 风格)

`box-sizing: border-box`
```
盒子总宽 = width(已包含 padding 与 border)
```

content 区域会自动收缩为 `width - padding - border`。所见即所得,布局可预测。

### 4. 现代最佳实践

```css
*, *::before, *::after {
  box-sizing: border-box;
}
```

业界共识:**全局 border-box**。Tailwind、Bootstrap 等框架默认应用。

### 5. margin 折叠(Collapsing)

垂直方向相邻块级盒子的 margin 会**取较大者而非相加**:

```html
<p style="margin-bottom: 30px">A</p>
<p style="margin-top: 20px">B</p>
<!-- 实际间距 30px,而非 50px -->
```

折叠条件:同方向、垂直、块级、无 padding/border 隔断、非浮动/绝对定位/Flex 容器内。Flexbox 子项不折叠,这是 [[Flexbox]] 流行的原因之一。

### 6. 内联盒模型差异

`<span>` 等内联元素的 width/height 无效,vertical padding/margin 不影响行高布局。需 `display: inline-block` 或 `display: block` 才有完整盒子。

### 7. BFC(Block Formatting Context)

特定条件触发的独立布局环境(`overflow: hidden`、`display: flow-root`):内部布局不影响外部,可解决浮动撑高、margin 穿透等历史问题。

## 关系

- 基础:所有 CSS 布局([[Flexbox]]、[[CSS Grid]])构建于盒模型之上
- 影响:`box-sizing` 设置贯穿设计系统
- 配合:`width/height/min-/max-` 与盒模型联动
- 历史:IE6 的怪异模式催生了 box-sizing 切换
- 进阶:BFC 解决 margin 折叠等顽疾

## 参考源

- raw/计算机/开发学习/语言/CSS/02-核心理解层/盒模型/标准盒模型.md
- raw/计算机/开发学习/语言/CSS/02-核心理解层/盒模型/怪异盒模型.md
- raw/计算机/开发学习/语言/CSS/02-核心理解层/盒模型/盒模型应用.md
