# SMACSS

## SMACSS概述

SMACSS（Scalable and Modular Architecture for CSS）是可扩展和模块化的CSS架构方法论。

## SMACSS分类

### 1. Base（基础）
```css
/* 基础样式：HTML元素默认样式 */
html, body {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
}

h1, h2, h3, h4, h5, h6 {
    margin: 0 0 1rem;
    font-weight: 600;
    line-height: 1.2;
}

p {
    margin: 0 0 1rem;
}

a {
    color: #007bff;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

img {
    max-width: 100%;
    height: auto;
}

button {
    border: none;
    background: none;
    cursor: pointer;
}

input, textarea, select {
    font-family: inherit;
    font-size: inherit;
}
```

### 2. Layout（布局）
```css
/* 布局样式：页面结构 */
.l-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
    background: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    z-index: 1000;
}

.l-main {
    margin-top: 60px;
    min-height: calc(100vh - 60px);
    display: flex;
}

.l-sidebar {
    width: 250px;
    background: #f8f9fa;
    border-right: 1px solid #e0e0e0;
}

.l-content {
    flex: 1;
    padding: 2rem;
}

.l-footer {
    background: #333;
    color: white;
    padding: 2rem;
    text-align: center;
}

/* 响应式布局 */
@media (max-width: 768px) {
    .l-main {
        flex-direction: column;
    }
    
    .l-sidebar {
        width: 100%;
        height: auto;
    }
}
```

### 3. Module（模块）
```css
/* 模块样式：可复用组件 */
/* 按钮模块 */
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

.btn--primary {
    background-color: #007bff;
    color: white;
}

.btn--secondary {
    background-color: #6c757d;
    color: white;
}

.btn--large {
    padding: 1rem 2rem;
    font-size: 1.125rem;
}

.btn--small {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
}

/* 卡片模块 */
.card {
    background: white;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    overflow: hidden;
}

.card__header {
    padding: 1.5rem 1.5rem 0;
}

.card__title {
    margin: 0 0 0.5rem;
    font-size: 1.25rem;
    font-weight: 600;
}

.card__body {
    padding: 1.5rem;
}

.card__footer {
    padding: 0 1.5rem 1.5rem;
    border-top: 1px solid #eee;
    background: #f8f9fa;
}

/* 导航模块 */
.nav {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
}

.nav__item {
    margin-right: 1rem;
}

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

.nav__item--active .nav__link {
    background-color: #007bff;
    color: white;
}
```

### 4. State（状态）
```css
/* 状态样式：元素状态 */
.is-hidden {
    display: none !important;
}

.is-visible {
    display: block !important;
}

.is-active {
    background-color: #007bff;
    color: white;
}

.is-disabled {
    opacity: 0.6;
    cursor: not-allowed;
    pointer-events: none;
}

.is-loading {
    position: relative;
    color: transparent;
}

.is-loading::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 20px;
    height: 20px;
    margin: -10px 0 0 -10px;
    border: 2px solid #f3f3f3;
    border-top: 2px solid #007bff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* 表单状态 */
.is-valid {
    border-color: #28a745;
}

.is-invalid {
    border-color: #dc3545;
}

.is-focused {
    box-shadow: 0 0 0 3px rgba(0,123,255,0.1);
}
```

### 5. Theme（主题）
```css
/* 主题样式：视觉主题 */
/* 默认主题 */
.theme-default {
    --primary-color: #007bff;
    --secondary-color: #6c757d;
    --success-color: #28a745;
    --danger-color: #dc3545;
    --warning-color: #ffc107;
    --info-color: #17a2b8;
    --light-color: #f8f9fa;
    --dark-color: #343a40;
}

/* 深色主题 */
.theme-dark {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    --success-color: #198754;
    --danger-color: #dc3545;
    --warning-color: #fd7e14;
    --info-color: #0dcaf0;
    --light-color: #212529;
    --dark-color: #ffffff;
    background-color: #212529;
    color: #ffffff;
}

/* 彩色主题 */
.theme-colorful {
    --primary-color: #e91e63;
    --secondary-color: #9c27b0;
    --success-color: #4caf50;
    --danger-color: #f44336;
    --warning-color: #ff9800;
    --info-color: #2196f3;
    --light-color: #fce4ec;
    --dark-color: #880e4f;
}
```

## 文件组织结构

### 1. 目录结构
```
css/
├── base/
│   ├── _reset.css
│   ├── _typography.css
│   └── _base.css
├── layout/
│   ├── _header.css
│   ├── _sidebar.css
│   ├── _main.css
│   └── _footer.css
├── modules/
│   ├── _buttons.css
│   ├── _cards.css
│   ├── _navigation.css
│   └── _forms.css
├── state/
│   ├── _visibility.css
│   ├── _loading.css
│   └── _validation.css
├── theme/
│   ├── _default.css
│   ├── _dark.css
│   └── _colorful.css
└── main.css
```

### 2. 主文件导入
```css
/* main.css */
@import 'base/reset';
@import 'base/typography';
@import 'base/base';

@import 'layout/header';
@import 'layout/sidebar';
@import 'layout/main';
@import 'layout/footer';

@import 'modules/buttons';
@import 'modules/cards';
@import 'modules/navigation';
@import 'modules/forms';

@import 'state/visibility';
@import 'state/loading';
@import 'state/validation';

@import 'theme/default';
```

## 实际应用

### 1. 页面结构
```html
<!DOCTYPE html>
<html lang="zh-CN" class="theme-default">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SMACSS示例</title>
    <link rel="stylesheet" href="css/main.css">
</head>
<body>
    <header class="l-header">
        <nav class="nav">
            <div class="nav__item">
                <a href="#" class="nav__link">首页</a>
            </div>
            <div class="nav__item nav__item--active">
                <a href="#" class="nav__link">产品</a>
            </div>
            <div class="nav__item">
                <a href="#" class="nav__link">关于</a>
            </div>
        </nav>
    </header>
    
    <main class="l-main">
        <aside class="l-sidebar">
            <div class="card">
                <div class="card__header">
                    <h3 class="card__title">侧边栏</h3>
                </div>
                <div class="card__body">
                    <p>侧边栏内容...</p>
                </div>
            </div>
        </aside>
        
        <section class="l-content">
            <div class="card">
                <div class="card__header">
                    <h2 class="card__title">主要内容</h2>
                </div>
                <div class="card__body">
                    <p>主要内容区域...</p>
                    <button class="btn btn--primary">主要按钮</button>
                    <button class="btn btn--secondary">次要按钮</button>
                </div>
                <div class="card__footer">
                    <button class="btn btn--small">小按钮</button>
                </div>
            </div>
        </section>
    </main>
    
    <footer class="l-footer">
        <p>&copy; 2024 示例网站</p>
    </footer>
</body>
</html>
```

### 2. 状态管理
```javascript
// JavaScript状态管理
function toggleVisibility(element) {
    element.classList.toggle('is-hidden');
}

function setLoading(element, isLoading) {
    if (isLoading) {
        element.classList.add('is-loading');
    } else {
        element.classList.remove('is-loading');
    }
}

function setActive(element, isActive) {
    if (isActive) {
        element.classList.add('is-active');
    } else {
        element.classList.remove('is-active');
    }
}

// 表单验证
function validateForm(form) {
    const inputs = form.querySelectorAll('input');
    inputs.forEach(input => {
        if (input.checkValidity()) {
            input.classList.add('is-valid');
            input.classList.remove('is-invalid');
        } else {
            input.classList.add('is-invalid');
            input.classList.remove('is-valid');
        }
    });
}
```

### 3. 主题切换
```javascript
// 主题切换
function switchTheme(themeName) {
    document.documentElement.className = `theme-${themeName}`;
    localStorage.setItem('theme', themeName);
}

// 加载保存的主题
function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'default';
    switchTheme(savedTheme);
}

// 初始化
loadTheme();
```

## 最佳实践

### 1. 命名规范
```css
/* 布局：l-前缀 */
.l-header { }
.l-main { }
.l-sidebar { }

/* 模块：无前缀 */
.btn { }
.card { }
.nav { }

/* 状态：is-前缀 */
.is-hidden { }
.is-active { }
.is-loading { }

/* 主题：theme-前缀 */
.theme-default { }
.theme-dark { }
```

### 2. 模块化设计
```css
/* 好的：模块化 */
.btn { }
.btn--primary { }
.btn--large { }

/* 避免：非模块化 */
.primary-button { }
.large-primary-button { }
```

### 3. 状态管理
```css
/* 好的：状态类 */
.is-active { }
.is-disabled { }

/* 避免：状态样式混合 */
.btn.active { }
.btn.disabled { }
```

## 相关链接

- [[BEM方法论]] - 了解BEM命名
- [[OOCSS]] - 学习面向对象CSS
- [[工程化实践/CSS模块化]] - 了解CSS模块化
- [[最佳实践/代码规范]] - 查看编码规范

## 实践练习

### 基础练习
1. 创建SMACSS结构
2. 实现模块化组件
3. 管理状态样式

### 进阶练习
1. 构建SMACSS框架
2. 实现主题系统
3. 优化模块架构

---

*下一步：学习 [[工程化实践/CSS模块化]] 了解现代CSS工程化*
