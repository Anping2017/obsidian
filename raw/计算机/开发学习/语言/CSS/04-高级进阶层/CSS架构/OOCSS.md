# OOCSS

## OOCSS概述

OOCSS（Object-Oriented CSS）是面向对象的CSS方法论，强调代码复用和模块化。

## OOCSS核心原则

### 1. 结构与皮肤分离
```css
/* 结构：布局和定位 */
.button {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.25rem;
    cursor: pointer;
    font-size: 1rem;
}

/* 皮肤：颜色和装饰 */
.button-primary {
    background-color: #007bff;
    color: white;
}

.button-secondary {
    background-color: #6c757d;
    color: white;
}

.button-success {
    background-color: #28a745;
    color: white;
}
```

### 2. 容器与内容分离
```css
/* 容器：布局容器 */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}

.container-fluid {
    width: 100%;
    padding: 0 1rem;
}

/* 内容：具体内容样式 */
.content {
    line-height: 1.6;
    color: #333;
}

.content--large {
    font-size: 1.125rem;
}

.content--small {
    font-size: 0.875rem;
}
```

## 实际应用

### 1. 按钮对象
```css
/* 基础按钮对象 */
.btn {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.25rem;
    cursor: pointer;
    font-size: 1rem;
    text-decoration: none;
    text-align: center;
    transition: all 0.3s ease;
}

/* 按钮尺寸变体 */
.btn--small {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
}

.btn--large {
    padding: 1rem 2rem;
    font-size: 1.125rem;
}

/* 按钮颜色变体 */
.btn--primary {
    background-color: #007bff;
    color: white;
}

.btn--secondary {
    background-color: #6c757d;
    color: white;
}

.btn--success {
    background-color: #28a745;
    color: white;
}

.btn--danger {
    background-color: #dc3545;
    color: white;
}

/* 按钮状态 */
.btn--disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn--block {
    display: block;
    width: 100%;
}
```

### 2. 卡片对象
```css
/* 基础卡片对象 */
.card {
    background: white;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    overflow: hidden;
}

/* 卡片变体 */
.card--elevated {
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.card--outlined {
    border: 1px solid #e0e0e0;
    box-shadow: none;
}

.card--flat {
    box-shadow: none;
    border: 1px solid #f0f0f0;
}

/* 卡片内容区域 */
.card__header {
    padding: 1.5rem 1.5rem 0;
}

.card__body {
    padding: 1.5rem;
}

.card__footer {
    padding: 0 1.5rem 1.5rem;
    border-top: 1px solid #eee;
    background: #f8f9fa;
}
```

### 3. 网格对象
```css
/* 基础网格对象 */
.grid {
    display: grid;
    gap: 1rem;
}

/* 网格变体 */
.grid--2 {
    grid-template-columns: repeat(2, 1fr);
}

.grid--3 {
    grid-template-columns: repeat(3, 1fr);
}

.grid--4 {
    grid-template-columns: repeat(4, 1fr);
}

.grid--auto {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

/* 网格间距变体 */
.grid--tight {
    gap: 0.5rem;
}

.grid--loose {
    gap: 2rem;
}
```

### 4. 文本对象
```css
/* 基础文本对象 */
.text {
    line-height: 1.6;
    color: #333;
}

/* 文本大小变体 */
.text--small {
    font-size: 0.875rem;
}

.text--large {
    font-size: 1.125rem;
}

.text--xl {
    font-size: 1.25rem;
}

/* 文本颜色变体 */
.text--primary {
    color: #007bff;
}

.text--secondary {
    color: #6c757d;
}

.text--success {
    color: #28a745;
}

.text--danger {
    color: #dc3545;
}

.text--muted {
    color: #6c757d;
}

/* 文本对齐变体 */
.text--left {
    text-align: left;
}

.text--center {
    text-align: center;
}

.text--right {
    text-align: right;
}

/* 文本权重变体 */
.text--light {
    font-weight: 300;
}

.text--normal {
    font-weight: 400;
}

.text--bold {
    font-weight: 600;
}
```

## HTML结构

### 1. 按钮组合
```html
<!-- 基础按钮 -->
<button class="btn">基础按钮</button>

<!-- 主要按钮 -->
<button class="btn btn--primary">主要按钮</button>

<!-- 大号成功按钮 -->
<button class="btn btn--success btn--large">大号成功按钮</button>

<!-- 块级危险按钮 -->
<button class="btn btn--danger btn--block">块级危险按钮</button>

<!-- 禁用按钮 -->
<button class="btn btn--primary btn--disabled" disabled>禁用按钮</button>
```

### 2. 卡片组合
```html
<!-- 基础卡片 -->
<div class="card">
    <div class="card__header">
        <h3>卡片标题</h3>
    </div>
    <div class="card__body">
        <p>卡片内容...</p>
    </div>
    <div class="card__footer">
        <button class="btn btn--primary">操作</button>
    </div>
</div>

<!-- 高架卡片 -->
<div class="card card--elevated">
    <div class="card__body">
        <h3 class="text text--xl text--bold">高架卡片</h3>
        <p class="text text--muted">这是高架卡片的内容</p>
    </div>
</div>
```

### 3. 网格组合
```html
<!-- 3列网格 -->
<div class="grid grid--3">
    <div class="card">
        <div class="card__body">
            <h3 class="text text--bold">卡片 1</h3>
            <p class="text text--muted">内容 1</p>
        </div>
    </div>
    <div class="card">
        <div class="card__body">
            <h3 class="text text--bold">卡片 2</h3>
            <p class="text text--muted">内容 2</p>
        </div>
    </div>
    <div class="card">
        <div class="card__body">
            <h3 class="text text--bold">卡片 3</h3>
            <p class="text text--muted">内容 3</p>
        </div>
    </div>
</div>

<!-- 自适应网格 -->
<div class="grid grid--auto grid--loose">
    <div class="card card--outlined">
        <div class="card__body">
            <h3 class="text text--primary text--bold">自适应卡片</h3>
            <p class="text">内容会自动适应</p>
        </div>
    </div>
</div>
```

## 最佳实践

### 1. 单一职责
```css
/* 好的：单一职责 */
.btn {
    /* 只处理按钮的基础结构 */
}

.btn--primary {
    /* 只处理主要按钮的样式 */
}

/* 避免：混合职责 */
.btn-primary {
    /* 混合了结构和样式 */
}
```

### 2. 可复用性
```css
/* 好的：可复用 */
.text {
    /* 可以在任何地方使用 */
}

.text--center {
    /* 可以应用到任何文本元素 */
}

/* 避免：特定用途 */
.header-title {
    /* 只能用于头部标题 */
}
```

### 3. 组合优于继承
```css
/* 好的：组合使用 */
<button class="btn btn--primary btn--large">按钮</button>

/* 避免：继承 */
.btn-primary-large {
    /* 创建新的类 */
}
```

### 4. 命名规范
```css
/* 好的：清晰命名 */
.btn { }
.btn--primary { }
.btn--large { }

/* 避免：模糊命名 */
.button { }
.primary { }
.big { }
```

## 工具和插件

### 1. CSS预处理器支持
```scss
// Sass中的OOCSS
.btn {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.25rem;
    cursor: pointer;
    
    &--primary {
        background-color: #007bff;
        color: white;
    }
    
    &--large {
        padding: 1rem 2rem;
        font-size: 1.125rem;
    }
}
```

### 2. 构建工具
```javascript
// PostCSS插件配置
module.exports = {
    plugins: [
        require('postcss-import'),
        require('postcss-nested'),
        require('autoprefixer')
    ]
}
```

## 相关链接

- [[BEM方法论]] - 了解BEM命名
- [[SMACSS]] - 学习可扩展CSS架构
- [[工程化实践/CSS模块化]] - 了解CSS模块化
- [[最佳实践/代码规范]] - 查看编码规范

## 实践练习

### 基础练习
1. 创建OOCSS对象
2. 实现对象组合
3. 设计可复用组件

### 进阶练习
1. 构建OOCSS框架
2. 优化对象设计
3. 实现对象工具链

---

*下一步：学习 [[SMACSS]] 了解可扩展CSS架构*
