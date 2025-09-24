## 1️⃣ CSS 基础

| 分类        | 内容                                                                            |         |
| --------- | ----------------------------------------------------------------------------- | ------- |
| **选择器**   | 元素选择器、类选择器、ID选择器、组合选择器、伪类、伪元素                                                 | [[选择器]] |
| **基本语法**  | 属性:值;、注释、层叠规则                                                                 |         |
| **颜色**    | 关键字、HEX、RGB、RGBA、HSL、透明度                                                      |         |
| **字体与文本** | font-family, font-size, font-weight, line-height, text-align, text-decoration |         |
| **盒模型**   | content, padding, border, margin, box-sizing                                  |         |
| **背景与边框** | background-color, background-image, border-radius, border-style, box-shadow   |         |
| **单位**    | px, em, rem, %, vh, vw, ch, fr                                                |         |

---

## 2️⃣ 布局与定位

|分类|内容|
|---|---|
|**定位**|static, relative, absolute, fixed, sticky, z-index|
|**浮动与清除**|float, clear|
|**Flexbox**|display: flex, flex-direction, justify-content, align-items, flex-wrap, flex-grow/shrink/basis|
|**Grid**|display: grid, grid-template-rows/columns, gap, grid-area, grid-template-areas|
|**多列布局**|column-count, column-gap, column-rule|
|**响应式设计**|@media 查询、min/max-width、移动优先布局|
|**现代单位**|CSS Variables (Custom Properties), calc(), clamp()|

---

## 3️⃣ CSS 选择器与优先级

|分类|内容|
|---|---|
|**选择器优先级**|Inline > ID > Class/Attr/Pseudo-class > Element|
|**组合选择器**|后代选择器、子选择器、相邻兄弟、通用兄弟|
|**伪类**|:hover, :focus, :active, :nth-child, :first-child, :last-child|
|**伪元素**|::before, ::after, ::first-letter, ::first-line|

---

## 4️⃣ 动画与过渡

|分类|内容|
|---|---|
|**过渡**|transition-property, transition-duration, transition-timing-function, transition-delay|
|**关键帧动画**|@keyframes, animation-name, animation-duration, animation-timing-function, animation-delay, animation-iteration-count|
|**CSS 动画属性**|transform, opacity, scale, rotate, translate|
|**硬件加速优化**|transform & opacity 优化动画性能|

---

## 5️⃣ 高级特性

|分类|内容|
|---|---|
|**变量与函数**|CSS 自定义属性、var()、calc()、clamp()|
|**高级选择器**|:not(), :has(), :is(), :where()|
|**滤镜与混合模式**|filter (blur, brightness, grayscale), mix-blend-mode, background-blend-mode|
|**剪裁与遮罩**|clip-path, mask|
|**文本特效**|text-shadow, text-stroke, word-wrap, text-overflow|
|**响应式图片**|object-fit, srcset, sizes|

---

## 6️⃣ CSS 现代实践

|分类|内容|
|---|---|
|**CSS 预处理器**|Sass, LESS, Stylus|
|**CSS 后处理器**|PostCSS, autoprefixer|
|**模块化 CSS**|CSS Modules, BEM, SMACSS, OOCSS|
|**CSS-in-JS**|styled-components, Emotion|
|**框架与工具**|Tailwind CSS, Bootstrap, Bulma, Materialize|

---

## 7️⃣ CSS 性能优化

| 分类          | 内容                                         |
| ----------- | ------------------------------------------ |
| **选择器优化**   | 避免低效选择器、减少通配符和后代选择器                        |
| **减少重排与重绘** | transform, opacity 替代 top/left、避免频繁 DOM 修改 |
| **文件优化**    | minify、合并、gzip                             |
| **关键 CSS**  | 关键渲染路径优化、按需加载                              |