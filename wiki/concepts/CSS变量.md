---
title: CSS 变量与自定义属性
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/语言/CSS/02-核心理解层/CSS变量与自定义属性/]
created: 2026-05-05
updated: 2026-05-05
summary: CSS 自定义属性以 --name 为前缀,通过 var() 引用,在级联中动态计算,是原生支持的设计令牌、主题切换、运行时样式控制方案。
---

# CSS 变量与自定义属性

## 定义

**CSS 自定义属性(Custom Properties)**,俗称 **CSS 变量**,是 CSS 规范定义的可复用值机制。声明形式 `--name: value`,引用形式 `var(--name, fallback)`。与 Sass/Less 等预处理器变量不同,CSS 变量**在浏览器运行时计算**,可被 JS 动态修改、参与级联与继承、响应媒体查询。

## 核心要点

### 1. 基本语法

```css
:root {
  --primary: #4f46e5;
  --spacing: 1rem;
}

.btn {
  background: var(--primary);
  padding: var(--spacing) calc(var(--spacing) * 2);
}
```

### 2. 与预处理器变量对比

| 维度 | Sass `$var` | CSS `--var` |
|---|---|---|
| 计算时机 | 编译时 | 运行时 |
| JS 可修改 | 否 | `element.style.setProperty('--x', val)` |
| 级联/继承 | 否 | 是 |
| 媒体查询切换 | 编译固定 | 动态切换 |
| 浏览器原生 | 否(需编译) | 是(IE 不支持) |

### 3. 作用域

CSS 变量遵循级联与继承:在哪个选择器声明,就在该子树有效。`:root` 即全局。

```css
.theme-dark { --bg: #000; }
.theme-light { --bg: #fff; }
body { background: var(--bg); }
/* 切换 body class 即换主题 */
```

### 4. JS 互操作

```js
document.documentElement.style.setProperty('--primary', '#0f0');
const v = getComputedStyle(el).getPropertyValue('--primary');
```

无需重排重绘整个样式表,可实现实时调色、滑块控件。

### 5. 与 calc() 联动

```css
:root {
  --base: 16px;
  --ratio: 1.25;
}
h1 { font-size: calc(var(--base) * var(--ratio) * var(--ratio) * var(--ratio)); }
```

模块化排版系统(Type Scale)。

### 6. @property(注册自定义属性)

CSS Houdini 进一步引入 @property,声明类型、初始值、是否继承,使变量参与动画:

```css
@property --angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}
```

让自定义属性可被插值动画。

### 7. 设计令牌(Design Token)

CSS 变量是 Web 端的设计令牌实现:颜色、字号、间距、圆角、阴影集中维护,Figma → Style Dictionary → CSS 变量自动同步,统一品牌系统。

### 8. 主题切换

无需重新加载样式表:

```js
document.body.dataset.theme = 'dark';
```
```css
[data-theme="dark"] { --bg: #111; --text: #eee; }
```

prefers-color-scheme 媒体查询自动跟随系统主题。

## 关系

- 替代:Sass/Less 在动态场景
- 配合:[[CSS盒模型]]、[[Flexbox]]、[[CSS Grid]] 让设计系统化
- JS:DOM API 动态修改实现交互
- 主题:暗色/品牌切换标准做法
- 高级:Houdini @property 加入动画能力
- 关联:[[CSS-in-JS]] 等方案部分被原生变量取代

## 参考源

- raw/计算机/开发学习/语言/CSS/02-核心理解层/CSS变量与自定义属性/
