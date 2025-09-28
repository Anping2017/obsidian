# CSS语法与结构

## CSS基本语法

### 语法结构
```css
选择器 {
    属性: 值;
    属性: 值;
}
```

### 语法组成
- **选择器**：指定要样式化的HTML元素
- **声明块**：用花括号 `{}` 包围
- **声明**：属性-值对，用分号 `;` 分隔
- **属性**：要设置的样式属性
- **值**：属性的具体值

## 选择器类型

### 1. 基础选择器
- **元素选择器**：`p`, `div`, `h1`
- **类选择器**：`.class-name`
- **ID选择器**：`#id-name`
- **通配符选择器**：`*`

### 2. 组合选择器
- **后代选择器**：`div p`
- **子选择器**：`div > p`
- **相邻兄弟选择器**：`h1 + p`
- **通用兄弟选择器**：`h1 ~ p`

### 3. 伪类选择器
- **状态伪类**：`:hover`, `:focus`, `:active`
- **结构伪类**：`:first-child`, `:last-child`, `:nth-child()`

### 4. 伪元素选择器
- **::before**：元素前插入内容
- **::after**：元素后插入内容
- **::first-line**：首行样式
- **::first-letter**：首字母样式

## 属性继承

### 可继承属性
```css
/* 文本相关属性 */
color, font-family, font-size, font-weight
line-height, text-align, text-indent

/* 列表相关属性 */
list-style, list-style-type

/* 表格相关属性 */
border-collapse, border-spacing
```

### 不可继承属性
```css
/* 盒模型属性 */
width, height, margin, padding, border

/* 定位属性 */
position, top, right, bottom, left

/* 背景属性 */
background-color, background-image
```

## 优先级规则

### 特异性计算
| 选择器类型 | 权重值 |
|------------|--------|
| 内联样式 | 1000 |
| ID选择器 | 100 |
| 类选择器 | 10 |
| 元素选择器 | 1 |

### 优先级示例
```css
/* 权重：1 */
p { color: red; }

/* 权重：10 */
.text { color: blue; }

/* 权重：100 */
#title { color: green; }

/* 权重：111 */
#title.text p { color: purple; }
```

## CSS注释

### 注释语法
```css
/* 这是单行注释 */

/*
这是多行注释
可以跨越多行
*/
```

### 注释用途
- 解释代码功能
- 标记重要信息
- 临时禁用样式
- 组织代码结构

## 常见语法错误

### 1. 缺少分号
```css
/* 错误 */
p { color: red font-size: 16px }

/* 正确 */
p { color: red; font-size: 16px; }
```

### 2. 花括号不匹配
```css
/* 错误 */
p { color: red;

/* 正确 */
p { color: red; }
```

### 3. 属性值缺少引号
```css
/* 错误 */
font-family: Arial, sans-serif;

/* 正确 */
font-family: "Arial", sans-serif;
```

## 最佳实践

### 1. 代码组织
- 按功能分组属性
- 使用缩进保持结构清晰
- 添加必要的注释

### 2. 命名规范
- 使用有意义的类名
- 避免使用ID选择器
- 遵循BEM命名法

### 3. 性能优化
- 避免过度嵌套选择器
- 使用高效的选择器
- 减少特异性冲突

## 相关链接

- [[选择器系统/基础选择器]] - 深入学习选择器
- [[CSS引入方式]] - 了解如何引入CSS
- [[浏览器渲染原理]] - 理解CSS工作原理
- [[最佳实践/代码规范]] - 查看编码规范

## 实践练习

### 基础练习
1. 创建一个简单的CSS规则
2. 使用不同的选择器类型
3. 理解优先级规则

### 进阶练习
1. 解决样式冲突
2. 优化选择器性能
3. 组织CSS代码结构

---

*下一步：学习 [[CSS引入方式]] 了解如何将CSS应用到HTML文档*
