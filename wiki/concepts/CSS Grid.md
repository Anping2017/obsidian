---
title: CSS Grid 网格布局
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/语言/CSS/03-应用实践层/现代布局/]
created: 2026-05-05
updated: 2026-05-05
summary: CSS Grid 是 2017 年浏览器全面支持的二维网格布局,通过显式行/列定义、命名区域、自动放置算法,首次让 CSS 能描述复杂版面。
---

# CSS Grid 网格布局

## 定义

**CSS Grid Layout** 是 W3C 2017 年正式推荐的二维布局规范。容器声明 `display: grid` 后,通过定义行(rows)和列(columns)形成显式网格,子项可放置到网格单元、跨越多格、形成命名区域。它是 CSS 历史上**第一次原生提供二维布局能力**,终结了长期靠 hack 实现复杂版面的时代。

## 核心要点

### 1. 基本语法

```css
.container {
  display: grid;
  grid-template-columns: 200px 1fr 1fr;     /* 三列:固定 + 两份等比 */
  grid-template-rows: auto 1fr auto;         /* 三行 */
  gap: 20px;
}
```

### 2. fr 与 minmax

- **`fr` 单位**:剩余空间份数,`1fr 2fr` 即 1:2 分配
- **`minmax(min, max)`**:最小到最大区间,避免极端尺寸塌陷
- **`auto-fill` / `auto-fit`**:自适应列数,响应式神器

```css
grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
/* 卡片自动按容器宽度调整列数 */
```

### 3. 命名区域

```css
.layout {
  display: grid;
  grid-template-columns: 200px 1fr;
  grid-template-areas:
    "header header"
    "side   main"
    "foot   foot";
}
.header { grid-area: header; }
.sidebar { grid-area: side; }
.content { grid-area: main; }
.footer { grid-area: foot; }
```

可视化布局,媒体查询切换不同 areas 实现响应式重排。

### 4. 项目放置

```css
.item {
  grid-column: 1 / 3;       /* 第 1 到 3 列 */
  grid-row: 2 / span 2;     /* 第 2 行起跨 2 行 */
}
```

### 5. 对齐(与 Flex 共享词汇)

`justify-items` / `align-items` 控制单格内对齐;`justify-content` / `align-content` 控制整个网格在容器中的对齐。

### 6. 隐式网格

未显式定义的额外行/列,由 `grid-auto-rows` / `grid-auto-columns` 控制。`grid-auto-flow: row dense` 启用密集填充算法,自动塞补空隙。

### 7. 与 Flexbox 对比

| 场景 | 推荐 |
|---|---|
| 整页布局(头/侧/主/脚) | Grid |
| 复杂报刊版面 | Grid |
| 卡片网格(自适应列数) | Grid + auto-fit |
| 导航栏、按钮组 | [[Flexbox]] |
| 单行项目对齐 | Flex |
| 不知道子项数量但要换行 | Flex wrap |
| 网格但要一维微调 | 双层嵌套 |

### 8. 子网格(Subgrid)

`grid-template-rows: subgrid` 让嵌套网格继承父网格的轨道,统一对齐多张卡片内的标题/正文/按钮。Firefox 2019、Chrome 117 (2023)、Safari 2023 全支持。

## 关系

- 互补:[[Flexbox]] 一维对齐
- 基于:[[CSS盒模型]]
- 应用:[[响应式设计]] 主要工具
- 命名:areas 让可读性远超传统布局
- 进化:Subgrid 解决嵌套对齐

## 参考源

- raw/计算机/开发学习/语言/CSS/03-应用实践层/现代布局/Grid布局.md
- raw/计算机/开发学习/语言/CSS/03-应用实践层/现代布局/布局对比与选择.md
