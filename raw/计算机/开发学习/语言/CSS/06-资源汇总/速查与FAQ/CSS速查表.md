# CSS速查表

## 选择器速查

### 基础选择器
```css
/* 元素选择器 */
p { }

/* 类选择器 */
.class { }

/* ID选择器 */
#id { }

/* 通配符选择器 */
* { }
```

### 组合选择器
```css
/* 后代选择器 */
div p { }

/* 子选择器 */
div > p { }

/* 相邻兄弟选择器 */
h1 + p { }

/* 通用兄弟选择器 */
h1 ~ p { }
```

### 伪类选择器
```css
/* 链接状态 */
a:link { }
a:visited { }
a:hover { }
a:active { }

/* 表单状态 */
input:focus { }
input:disabled { }
input:checked { }

/* 结构伪类 */
li:first-child { }
li:last-child { }
li:nth-child(3) { }
```

### 伪元素选择器
```css
/* 内容伪元素 */
.element::before { }
.element::after { }

/* 文本伪元素 */
p::first-line { }
p::first-letter { }
::selection { }
```

## 盒模型速查

### 盒模型属性
```css
.element {
    width: 200px;
    height: 100px;
    padding: 10px;
    border: 2px solid black;
    margin: 20px;
    box-sizing: border-box;
}
```

### 盒模型类型
```css
/* 标准盒模型 */
.content-box {
    box-sizing: content-box;
}

/* 怪异盒模型 */
.border-box {
    box-sizing: border-box;
}
```

## 定位速查

### 定位属性
```css
.element {
    position: static;    /* 默认 */
    position: relative;  /* 相对定位 */
    position: absolute;  /* 绝对定位 */
    position: fixed;     /* 固定定位 */
    position: sticky;    /* 粘性定位 */
    
    top: 10px;
    right: 20px;
    bottom: 30px;
    left: 40px;
    z-index: 1;
}
```

## 布局速查

### Flexbox布局
```css
/* 容器属性 */
.flex-container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    align-content: center;
}

/* 项目属性 */
.flex-item {
    flex: 1;
    flex-grow: 1;
    flex-shrink: 1;
    flex-basis: auto;
    align-self: center;
    order: 1;
}
```

### Grid布局
```css
/* 容器属性 */
.grid-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(2, 100px);
    gap: 20px;
    justify-items: center;
    align-items: center;
}

/* 项目属性 */
.grid-item {
    grid-column: 1 / 3;
    grid-row: 1 / 2;
    justify-self: center;
    align-self: center;
}
```

## 字体速查

### 字体属性
```css
.text {
    font-family: Arial, sans-serif;
    font-size: 16px;
    font-weight: normal;
    font-style: normal;
    line-height: 1.5;
    text-align: left;
    text-decoration: none;
    text-transform: none;
    letter-spacing: normal;
    word-spacing: normal;
}
```

### 字体大小
```css
.text-xs { font-size: 0.75rem; }    /* 12px */
.text-sm { font-size: 0.875rem; }   /* 14px */
.text-base { font-size: 1rem; }     /* 16px */
.text-lg { font-size: 1.125rem; }   /* 18px */
.text-xl { font-size: 1.25rem; }    /* 20px */
```

## 颜色速查

### 颜色表示
```css
.element {
    color: red;                    /* 关键字 */
    color: #ff0000;               /* 十六进制 */
    color: rgb(255, 0, 0);        /* RGB */
    color: rgba(255, 0, 0, 0.5);  /* RGBA */
    color: hsl(0, 100%, 50%);     /* HSL */
    color: hsla(0, 100%, 50%, 0.5); /* HSLA */
}
```

### 常用颜色
```css
/* 基础颜色 */
.red { color: #ff0000; }
.green { color: #00ff00; }
.blue { color: #0000ff; }
.black { color: #000000; }
.white { color: #ffffff; }

/* 灰色系 */
.gray-100 { color: #f5f5f5; }
.gray-200 { color: #eeeeee; }
.gray-300 { color: #e0e0e0; }
.gray-400 { color: #bdbdbd; }
.gray-500 { color: #9e9e9e; }
```

## 背景速查

### 背景属性
```css
.element {
    background-color: #f0f0f0;
    background-image: url('image.jpg');
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
    background-attachment: fixed;
}
```

### 背景简写
```css
.element {
    background: #f0f0f0 url('image.jpg') no-repeat center/cover;
}
```

## 边框速查

### 边框属性
```css
.element {
    border-width: 1px;
    border-style: solid;
    border-color: #000;
    border-radius: 4px;
}
```

### 边框简写
```css
.element {
    border: 1px solid #000;
    border-radius: 4px;
}
```

## 阴影速查

### 阴影属性
```css
.element {
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}
```

### 常用阴影
```css
.shadow-sm { box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
.shadow { box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.shadow-lg { box-shadow: 0 4px 8px rgba(0,0,0,0.15); }
.shadow-xl { box-shadow: 0 8px 16px rgba(0,0,0,0.2); }
```

## 动画速查

### 过渡属性
```css
.element {
    transition: all 0.3s ease;
    transition-property: transform;
    transition-duration: 0.3s;
    transition-timing-function: ease;
    transition-delay: 0s;
}
```

### 动画属性
```css
.element {
    animation: slideIn 0.5s ease-in-out;
    animation-name: slideIn;
    animation-duration: 0.5s;
    animation-timing-function: ease-in-out;
    animation-delay: 0s;
    animation-iteration-count: 1;
    animation-direction: normal;
    animation-fill-mode: forwards;
    animation-play-state: running;
}
```

### 关键帧动画
```css
@keyframes slideIn {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(0); }
}
```

## 响应式速查

### 媒体查询
```css
/* 移动端 */
@media (max-width: 767px) { }

/* 平板端 */
@media (min-width: 768px) and (max-width: 1023px) { }

/* 桌面端 */
@media (min-width: 1024px) { }

/* 高分辨率屏幕 */
@media (-webkit-min-device-pixel-ratio: 2) { }
```

### 响应式单位
```css
.element {
    width: 100vw;        /* 视口宽度 */
    height: 100vh;       /* 视口高度 */
    font-size: 2.5vw;    /* 视口宽度百分比 */
    margin: 5vh 0;       /* 视口高度百分比 */
}
```

## 工具类速查

### 显示工具
```css
.d-none { display: none; }
.d-block { display: block; }
.d-inline { display: inline; }
.d-inline-block { display: inline-block; }
.d-flex { display: flex; }
.d-grid { display: grid; }
```

### 文本工具
```css
.text-left { text-align: left; }
.text-center { text-align: center; }
.text-right { text-align: right; }
.text-uppercase { text-transform: uppercase; }
.text-lowercase { text-transform: lowercase; }
.text-capitalize { text-transform: capitalize; }
```

### 间距工具
```css
.m-0 { margin: 0; }
.m-1 { margin: 0.25rem; }
.m-2 { margin: 0.5rem; }
.m-3 { margin: 0.75rem; }
.m-4 { margin: 1rem; }

.p-0 { padding: 0; }
.p-1 { padding: 0.25rem; }
.p-2 { padding: 0.5rem; }
.p-3 { padding: 0.75rem; }
.p-4 { padding: 1rem; }
```

## 相关链接

- [[CSS常见问题FAQ]] - 查看常见问题
- [[CSS学习路径图]] - 了解学习路径
- [[常用属性速查]] - 快速查找属性
- [[浏览器支持表]] - 查看兼容性

---

*下一步：学习 [[CSS常见问题FAQ]] 解决常见问题*
