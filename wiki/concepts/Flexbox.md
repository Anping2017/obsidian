---
title: Flexbox 弹性布局
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/语言/CSS/03-应用实践层/现代布局/]
created: 2026-05-05
updated: 2026-05-05
summary: Flexbox 是 CSS3 一维弹性布局规范,通过容器与项目两层属性,优雅解决居中、等高、分配剩余空间等十多年的 CSS 顽疾。
---

# Flexbox 弹性布局

## 定义

**Flexbox(Flexible Box Layout)** 是 W3C 2009 起草、2017 成为正式推荐的 CSS3 一维布局模块。"一维"指一次只控制一行或一列。它通过容器(`display: flex`)与项目(子元素)两层属性,**沿主轴和交叉轴分配空间、对齐项目**。

## 核心要点

### 1. 容器属性

| 属性 | 作用 | 常用值 |
|---|---|---|
| `flex-direction` | 主轴方向 | row(默认) / column / row-reverse |
| `flex-wrap` | 是否换行 | nowrap / wrap / wrap-reverse |
| `justify-content` | 主轴对齐 | flex-start / center / space-between / space-around / space-evenly |
| `align-items` | 交叉轴对齐 | stretch(默认) / center / flex-start / baseline |
| `align-content` | 多行交叉轴对齐 | 同 justify-content + stretch |
| `gap` | 项目间距 | 长度值 |

### 2. 项目属性

| 属性 | 作用 |
|---|---|
| `flex-grow` | 剩余空间分配比例(默认 0) |
| `flex-shrink` | 不足时缩小比例(默认 1) |
| `flex-basis` | 初始尺寸(替代 width) |
| `flex` | 上三者简写,常用 `flex: 1` 表示均分 |
| `align-self` | 单独覆盖 align-items |
| `order` | 显示顺序(不影响 DOM) |

### 3. 经典痛点解决

#### 垂直水平居中(传统三十种方案的终结者)

```css
.parent {
  display: flex;
  justify-content: center;
  align-items: center;
}
```

#### 等高列

子项默认 `align-items: stretch`,自动等高。

#### 圣杯布局

```css
.holy-grail {
  display: flex;
}
.main { flex: 1; } /* 自适应 */
.sidebar { flex: 0 0 200px; } /* 固定 */
```

#### Sticky Footer

```css
body { display: flex; flex-direction: column; min-height: 100vh; }
main { flex: 1; }
```

### 4. 与浮动/Inline-block 对比

| 方案 | 居中 | 等高 | 间距 | 顺序 |
|---|---|---|---|---|
| `float` | 难 | 难 | 麻烦 | 不可 |
| `inline-block` | 文本居中可 | 不行 | 空白符 | 不可 |
| Flex | 一行 | 默认 | gap | order |

### 5. 与 Grid 区别

| 维度 | Flexbox | [[CSS Grid]] |
|---|---|---|
| 维度 | 一维 | 二维 |
| 内容驱动 | 是(项目大小决定布局) | 否(网格驱动) |
| 复杂版面 | 难 | 易 |
| 一行排列 | 优 | 可 |

**经验法则**:组件级布局(导航、卡片内部)用 Flex,页面级布局用 Grid。

### 6. 浏览器兼容

IE10/11 实现旧规范,需 `-ms-` 前缀且诸多 bug。现代项目目标 Chrome/Edge/Safari/Firefox,无兼容性顾虑。

## 关系

- 基于:[[CSS盒模型]] 但 margin 不折叠
- 互补:[[CSS Grid]] 处理二维场景
- 应用:[[响应式设计]] 中常用 flex-wrap + flex-basis
- 取代:旧的 float、inline-block、table 布局
- 配合:gap 属性同时被 Grid 复用

## 参考源

- raw/计算机/开发学习/语言/CSS/03-应用实践层/现代布局/Flexbox布局.md
