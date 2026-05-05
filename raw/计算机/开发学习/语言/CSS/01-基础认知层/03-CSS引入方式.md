# CSS引入方式

## 引入方式概述

CSS有三种主要引入方式，每种方式都有其适用场景和特点。

## 1. 内联样式（Inline Styles）

### 语法
```html
<元素 style="属性: 值; 属性: 值;">
```

### 示例
```html
<p style="color: red; font-size: 16px;">这是红色文字</p>
<div style="background-color: blue; padding: 20px;">蓝色背景</div>
```

### 特点
- **优先级最高**：权重值为1000
- **维护困难**：样式与HTML混合
- **适用场景**：临时样式、动态样式

### 优缺点对比

| 优点 | 缺点 |
|------|------|
| 优先级高 | 维护困难 |
| 加载快 | 代码冗余 |
| 适合动态样式 | 不利于SEO |

## 2. 内部样式表（Internal Stylesheet）

### 语法
```html
<head>
    <style>
        选择器 {
            属性: 值;
        }
    </style>
</head>
```

### 示例
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        h1 {
            color: blue;
            text-align: center;
        }
        .highlight {
            background-color: yellow;
        }
    </style>
</head>
<body>
    <h1>标题</h1>
    <p class="highlight">高亮文本</p>
</body>
</html>
```

### 特点
- **页面级样式**：只影响当前页面
- **中等优先级**：权重值根据选择器计算
- **适用场景**：单页面应用、页面特定样式

## 3. 外部样式表（External Stylesheet）

### 语法
```html
<head>
    <link rel="stylesheet" href="样式文件路径">
</head>
```

### 示例
```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="responsive.css">
</head>
<body>
    <!-- 页面内容 -->
</body>
</html>
```

### CSS文件结构
```css
/* styles.css */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}

.header {
    background-color: #333;
    color: white;
    padding: 20px;
}

.content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}
```

### 特点
- **可重用性**：多个页面共享
- **维护方便**：集中管理样式
- **缓存友好**：浏览器可缓存CSS文件
- **适用场景**：多页面网站、大型项目

## 引入方式对比

| 方式 | 优先级 | 维护性 | 性能 | 适用场景 |
|------|--------|--------|------|----------|
| 内联样式 | 最高 | 差 | 好 | 临时样式 |
| 内部样式 | 中等 | 一般 | 好 | 单页面 |
| 外部样式 | 低 | 好 | 一般 | 多页面 |

## 最佳实践

### 1. 选择原则
- **外部样式表**：项目主要样式
- **内部样式表**：页面特定样式
- **内联样式**：动态生成的样式

### 2. 文件组织
```
css/
├── base/
│   ├── reset.css
│   └── typography.css
├── components/
│   ├── button.css
│   └── form.css
├── layout/
│   ├── header.css
│   └── footer.css
└── main.css
```

### 3. 加载优化
```html
<!-- 关键CSS内联 -->
<style>
    /* 首屏关键样式 */
</style>

<!-- 非关键CSS异步加载 -->
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

## 现代引入方式

### 1. CSS Modules
```javascript
import styles from './Button.module.css';

function Button() {
    return <button className={styles.primary}>按钮</button>;
}
```

### 2. CSS-in-JS
```javascript
import styled from 'styled-components';

const Button = styled.button`
    background-color: blue;
    color: white;
    padding: 10px 20px;
`;
```

### 3. PostCSS
```css
/* 输入 */
:root {
    --primary-color: #007bff;
}

.button {
    background-color: var(--primary-color);
}

/* 输出（自动添加前缀） */
.button {
    background-color: var(--primary-color);
    -webkit-background-color: var(--primary-color);
}
```

## 性能优化

### 1. 关键CSS内联
```html
<style>
    /* 首屏关键样式 */
    .header { display: block; }
    .hero { height: 100vh; }
</style>
```

### 2. 非关键CSS异步加载
```html
<link rel="preload" href="non-critical.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

### 3. CSS压缩
- 移除空白字符
- 合并相同规则
- 优化选择器

## 相关链接

- [[CSS语法与结构]] - 了解CSS语法规则
- [[浏览器渲染原理]] - 理解CSS加载过程
- [[性能优化/加载优化]] - 深入学习性能优化
- [[工程化实践/CSS模块化]] - 了解现代CSS组织方式

## 实践练习

### 基础练习
1. 创建外部样式表文件
2. 在HTML中引入CSS
3. 比较不同引入方式的效果

### 进阶练习
1. 组织CSS文件结构
2. 实现关键CSS内联
3. 优化CSS加载性能

---

*下一步：学习 [[浏览器渲染原理]] 理解CSS如何影响页面渲染*
