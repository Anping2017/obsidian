# CSS常见问题FAQ

## 基础问题

### Q1: 为什么我的CSS样式没有生效？
**A:** 可能的原因：
1. **选择器优先级不够**：使用更具体的选择器或`!important`
2. **CSS文件未正确引入**：检查`<link>`标签路径
3. **语法错误**：检查CSS语法是否正确
4. **缓存问题**：清除浏览器缓存

```css
/* 解决方案示例 */
.my-element {
    color: red !important; /* 提高优先级 */
}
```

### Q2: 如何让元素居中？
**A:** 根据情况选择不同方法：

```css
/* 水平居中 */
.center-horizontal {
    text-align: center; /* 文本居中 */
    margin: 0 auto;     /* 块级元素居中 */
}

/* 垂直居中 */
.center-vertical {
    display: flex;
    align-items: center;
    height: 100vh;
}

/* 完全居中 */
.center-both {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
```

### Q3: 如何清除浮动？
**A:** 使用以下方法：

```css
/* 方法1：伪元素清除 */
.clearfix::after {
    content: "";
    display: table;
    clear: both;
}

/* 方法2：overflow清除 */
.clearfix {
    overflow: hidden;
}

/* 方法3：现代方法 */
.clearfix {
    display: flow-root;
}
```

## 布局问题

### Q4: Flexbox和Grid有什么区别？
**A:** 
- **Flexbox**：一维布局，适合组件内部布局
- **Grid**：二维布局，适合页面整体布局

```css
/* Flexbox - 一维布局 */
.flex-container {
    display: flex;
    justify-content: space-between;
}

/* Grid - 二维布局 */
.grid-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(2, 100px);
}
```

### Q5: 如何实现响应式设计？
**A:** 使用媒体查询和弹性单位：

```css
/* 媒体查询 */
@media (max-width: 768px) {
    .container {
        width: 100%;
        padding: 1rem;
    }
}

/* 弹性单位 */
.responsive-element {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 5vw;
}
```

### Q6: 如何解决外边距重叠问题？
**A:** 使用以下方法：

```css
/* 方法1：使用padding代替margin */
.element {
    padding-top: 20px;
}

/* 方法2：使用border */
.element {
    border-top: 1px solid transparent;
}

/* 方法3：使用overflow */
.container {
    overflow: hidden;
}
```

## 样式问题

### Q7: 如何实现文字溢出省略？
**A:** 使用以下CSS：

```css
/* 单行文本溢出 */
.text-ellipsis {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* 多行文本溢出 */
.text-ellipsis-multiline {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
```

### Q8: 如何实现毛玻璃效果？
**A:** 使用backdrop-filter：

```css
.glass-effect {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}
```

### Q9: 如何实现渐变背景？
**A:** 使用linear-gradient：

```css
.gradient-bg {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 径向渐变 */
.radial-gradient {
    background: radial-gradient(circle, #ff6b6b, #4ecdc4);
}
```

## 动画问题

### Q10: 如何优化CSS动画性能？
**A:** 使用以下优化方法：

```css
/* 使用transform和opacity */
.optimized-animation {
    transform: translateX(100px);
    opacity: 0.8;
    will-change: transform, opacity;
}

/* 避免使用会触发布局的属性 */
.avoid-animation {
    /* 避免：left, top, width, height */
    /* 推荐：transform, opacity */
}
```

### Q11: 如何实现页面加载动画？
**A:** 使用关键帧动画：

```css
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.page-load {
    animation: fadeIn 0.6s ease-out;
}
```

### Q12: 如何暂停和恢复动画？
**A:** 使用animation-play-state：

```css
.pausable-animation {
    animation: spin 2s linear infinite;
    animation-play-state: running;
}

.pausable-animation.paused {
    animation-play-state: paused;
}
```

## 兼容性问题

### Q13: 如何解决IE兼容性问题？
**A:** 使用以下方法：

```css
/* 使用autoprefixer自动添加前缀 */
.flexbox {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
}

/* 使用CSS变量降级 */
:root {
    --primary-color: #007bff;
}

.element {
    color: #007bff; /* 降级方案 */
    color: var(--primary-color);
}
```

### Q14: 如何检测浏览器支持？
**A:** 使用@supports：

```css
/* 检测Grid支持 */
@supports (display: grid) {
    .grid-layout {
        display: grid;
    }
}

/* 降级方案 */
@supports not (display: grid) {
    .grid-layout {
        display: flex;
    }
}
```

## 性能问题

### Q15: 如何减少CSS文件大小？
**A:** 使用以下优化方法：

```css
/* 1. 合并相同规则 */
.element1, .element2, .element3 {
    color: red;
    font-size: 16px;
}

/* 2. 使用简写属性 */
.element {
    margin: 10px 20px; /* 而不是 margin-top: 10px; margin-bottom: 10px; */
}

/* 3. 移除未使用的CSS */
/* 使用工具如PurgeCSS */
```

### Q16: 如何实现关键CSS？
**A:** 内联关键CSS：

```html
<style>
/* 首屏关键样式 */
.header { display: block; }
.hero { height: 100vh; }
</style>

<link rel="preload" href="non-critical.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

## 调试问题

### Q17: 如何调试CSS问题？
**A:** 使用以下方法：

```css
/* 1. 使用边框调试 */
.debug * {
    outline: 1px solid red;
}

/* 2. 使用背景色调试 */
.debug-element {
    background-color: rgba(255, 0, 0, 0.1);
}

/* 3. 使用开发者工具 */
/* F12 -> Elements -> Styles */
```

### Q18: 如何解决z-index问题？
**A:** 理解层叠上下文：

```css
/* 创建新的层叠上下文 */
.layer {
    position: relative;
    z-index: 1;
}

/* 子元素在独立层叠上下文中 */
.layer .child {
    position: absolute;
    z-index: 10; /* 相对于父元素 */
}
```

## 相关链接

- [[CSS速查表]] - 快速查找语法
- [[CSS学习路径图]] - 了解学习路径
- [[常用属性速查]] - 查找属性用法
- [[浏览器支持表]] - 查看兼容性

---

*下一步：学习 [[CSS学习路径图]] 规划学习路径*
