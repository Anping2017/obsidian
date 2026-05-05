# BEM方法论

## BEM概述

BEM（Block Element Modifier）是CSS命名方法论，提供了一种清晰、可维护的CSS架构。

## BEM核心概念

### 1. Block（块）
```css
/* 独立的组件 */
.button { }
.menu { }
.card { }
.header { }
```

### 2. Element（元素）
```css
/* 块的组成部分 */
.button__text { }
.menu__item { }
.card__title { }
.header__logo { }
```

### 3. Modifier（修饰符）
```css
/* 块或元素的状态或变体 */
.button--primary { }
.button--large { }
.menu__item--active { }
.card--featured { }
```

## BEM命名规范

### 1. 命名规则
```css
/* 块 */
.block { }

/* 元素 */
.block__element { }

/* 修饰符 */
.block--modifier { }
.block__element--modifier { }
```

### 2. 命名示例
```css
/* 按钮组件 */
.button { }
.button__text { }
.button--primary { }
.button--large { }
.button--primary--large { }

/* 菜单组件 */
.menu { }
.menu__item { }
.menu__link { }
.menu__item--active { }
.menu--vertical { }

/* 卡片组件 */
.card { }
.card__header { }
.card__title { }
.card__content { }
.card__footer { }
.card--featured { }
.card__title--large { }
```

## 实际应用

### 1. 按钮组件
```css
/* 基础按钮 */
.button {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.25rem;
    cursor: pointer;
    font-size: 1rem;
    text-decoration: none;
    transition: all 0.3s ease;
}

/* 按钮文本 */
.button__text {
    font-weight: 500;
}

/* 按钮图标 */
.button__icon {
    margin-right: 0.5rem;
}

/* 主要按钮 */
.button--primary {
    background-color: #007bff;
    color: white;
}

.button--primary:hover {
    background-color: #0056b3;
}

/* 次要按钮 */
.button--secondary {
    background-color: #6c757d;
    color: white;
}

.button--secondary:hover {
    background-color: #545b62;
}

/* 大按钮 */
.button--large {
    padding: 1rem 2rem;
    font-size: 1.125rem;
}

/* 小按钮 */
.button--small {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
}

/* 禁用状态 */
.button--disabled {
    opacity: 0.6;
    cursor: not-allowed;
}
```

### 2. 卡片组件
```css
/* 基础卡片 */
.card {
    background: white;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    overflow: hidden;
}

/* 卡片头部 */
.card__header {
    padding: 1.5rem 1.5rem 0;
}

/* 卡片标题 */
.card__title {
    margin: 0 0 0.5rem;
    font-size: 1.25rem;
    font-weight: 600;
    color: #333;
}

/* 卡片副标题 */
.card__subtitle {
    margin: 0 0 1rem;
    font-size: 0.875rem;
    color: #666;
}

/* 卡片内容 */
.card__content {
    padding: 1.5rem;
}

/* 卡片底部 */
.card__footer {
    padding: 0 1.5rem 1.5rem;
    border-top: 1px solid #eee;
    background: #f8f9fa;
}

/* 特色卡片 */
.card--featured {
    border: 2px solid #007bff;
    box-shadow: 0 4px 8px rgba(0,123,255,0.2);
}

/* 大标题卡片 */
.card__title--large {
    font-size: 1.5rem;
}

/* 无边框卡片 */
.card--no-border {
    border: none;
    box-shadow: none;
}
```

### 3. 导航组件
```css
/* 基础导航 */
.nav {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
}

/* 导航项 */
.nav__item {
    margin-right: 1rem;
}

/* 导航链接 */
.nav__link {
    display: block;
    padding: 0.5rem 1rem;
    color: #333;
    text-decoration: none;
    border-radius: 0.25rem;
    transition: background-color 0.3s ease;
}

.nav__link:hover {
    background-color: #f8f9fa;
}

/* 活动导航项 */
.nav__item--active .nav__link {
    background-color: #007bff;
    color: white;
}

/* 垂直导航 */
.nav--vertical {
    flex-direction: column;
}

.nav--vertical .nav__item {
    margin-right: 0;
    margin-bottom: 0.5rem;
}

/* 面包屑导航 */
.breadcrumb {
    display: flex;
    align-items: center;
    font-size: 0.875rem;
}

.breadcrumb__item {
    display: flex;
    align-items: center;
}

.breadcrumb__link {
    color: #007bff;
    text-decoration: none;
}

.breadcrumb__link:hover {
    text-decoration: underline;
}

.breadcrumb__separator {
    margin: 0 0.5rem;
    color: #666;
}

.breadcrumb__item--current {
    color: #666;
}
```

## HTML结构

### 1. 按钮HTML
```html
<!-- 基础按钮 -->
<button class="button">
    <span class="button__text">点击我</span>
</button>

<!-- 带图标的按钮 -->
<button class="button button--primary">
    <i class="button__icon">📧</i>
    <span class="button__text">发送邮件</span>
</button>

<!-- 大按钮 -->
<button class="button button--primary button--large">
    <span class="button__text">大按钮</span>
</button>

<!-- 禁用按钮 -->
<button class="button button--disabled" disabled>
    <span class="button__text">禁用按钮</span>
</button>
```

### 2. 卡片HTML
```html
<!-- 基础卡片 -->
<div class="card">
    <div class="card__header">
        <h3 class="card__title">卡片标题</h3>
        <p class="card__subtitle">卡片副标题</p>
    </div>
    <div class="card__content">
        <p>卡片内容...</p>
    </div>
    <div class="card__footer">
        <button class="button button--primary">操作</button>
    </div>
</div>

<!-- 特色卡片 -->
<div class="card card--featured">
    <div class="card__header">
        <h3 class="card__title card__title--large">特色卡片</h3>
    </div>
    <div class="card__content">
        <p>这是特色卡片的内容...</p>
    </div>
</div>
```

### 3. 导航HTML
```html
<!-- 水平导航 -->
<nav class="nav">
    <div class="nav__item">
        <a href="#" class="nav__link">首页</a>
    </div>
    <div class="nav__item">
        <a href="#" class="nav__link">关于</a>
    </div>
    <div class="nav__item nav__item--active">
        <a href="#" class="nav__link">产品</a>
    </div>
    <div class="nav__item">
        <a href="#" class="nav__link">联系</a>
    </div>
</nav>

<!-- 面包屑导航 -->
<nav class="breadcrumb">
    <div class="breadcrumb__item">
        <a href="#" class="breadcrumb__link">首页</a>
    </div>
    <span class="breadcrumb__separator">/</span>
    <div class="breadcrumb__item">
        <a href="#" class="breadcrumb__link">产品</a>
    </div>
    <span class="breadcrumb__separator">/</span>
    <div class="breadcrumb__item breadcrumb__item--current">
        详情
    </div>
</nav>
```

## 最佳实践

### 1. 命名规范
```css
/* 好的命名 */
.button { }
.button__text { }
.button--primary { }

/* 避免的命名 */
.btn { }
.buttonText { }
.button-primary { }
```

### 2. 结构清晰
```css
/* 按BEM结构组织 */
/* Block */
.card { }

/* Elements */
.card__header { }
.card__title { }
.card__content { }
.card__footer { }

/* Modifiers */
.card--featured { }
.card__title--large { }
```

### 3. 避免过度嵌套
```css
/* 避免：过度嵌套 */
.card__header__title__text { }

/* 推荐：扁平结构 */
.card__title { }
.card__title--large { }
```

### 4. 语义化命名
```css
/* 好的语义化命名 */
.button { }
.menu { }
.card { }
.header { }

/* 避免：非语义化命名 */
.red { }
.big { }
.left { }
```

## 工具和插件

### 1. CSS预处理器支持
```scss
// Sass中的BEM
.card {
    &__header {
        padding: 1rem;
    }
    
    &__title {
        font-size: 1.25rem;
        
        &--large {
            font-size: 1.5rem;
        }
    }
    
    &--featured {
        border: 2px solid #007bff;
    }
}
```

### 2. PostCSS插件
```javascript
// postcss-bem插件配置
module.exports = {
    plugins: [
        require('postcss-bem')({
            style: 'bem'
        })
    ]
}
```

## 相关链接

- [[OOCSS]] - 了解面向对象CSS
- [[SMACSS]] - 学习可扩展CSS架构
- [[工程化实践/CSS模块化]] - 了解CSS模块化
- [[最佳实践/代码规范]] - 查看编码规范

## 实践练习

### 基础练习
1. 使用BEM命名组件
2. 创建BEM结构
3. 实现BEM修饰符

### 进阶练习
1. 构建BEM组件库
2. 优化BEM架构
3. 实现BEM工具链

---

*下一步：学习 [[OOCSS]] 了解面向对象CSS*
