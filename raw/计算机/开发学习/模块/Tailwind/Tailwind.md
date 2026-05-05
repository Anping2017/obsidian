## 1️⃣ Tailwind 基础概念

|分类|内容|
|---|---|
|**定义**|原子化 CSS 框架，通过类名快速写样式|
|**安装方式**|npm/yarn 安装、CDN 引入、与 PostCSS 集成|
|**配置文件**|tailwind.config.js，扩展主题、颜色、屏幕断点、插件|
|**JIT 模式**|Just-In-Time 编译，按需生成 CSS，减少文件体积|

---

## 2️⃣ 核心类分类

|分类|内容|
|---|---|
|**布局类**|container, box-sizing, display, float, clear, object-fit, overflow|
|**定位类**|position, top/right/bottom/left, z-index|
|**Flex & Grid**|flex, flex-col/row, flex-wrap, justify-_, items-_, grid, grid-cols, gap|
|**间距**|padding (p-_, px-_, py-_), margin (m-_, mx-_, my-_)|
|**尺寸**|width, height, min/max width/height, aspect-ratio|
|**边框**|border, border-width, border-color, border-radius, divide|
|**背景**|background-color, bg-opacity, bg-gradient, bg-blend-mode|
|**字体与文本**|font-size, font-weight, text-align, line-height, letter-spacing, text-color|
|**阴影**|box-shadow, text-shadow|

---

## 3️⃣ 响应式设计

|分类|内容|
|---|---|
|**屏幕断点**|sm, md, lg, xl, 2xl（可自定义）|
|**响应式类**|sm:p-4, md:text-lg, lg:grid-cols-3|
|**状态伪类**|hover:bg-blue-500, focus:outline-none, active:scale-95, disabled:opacity-50|
|**暗黑模式**|dark:bg-gray-800, dark:text-white|

---

## 4️⃣ 动画与过渡

|分类|内容|
|---|---|
|**过渡类**|transition, duration-_, ease-_, delay-*|
|**动画类**|animate-spin, animate-ping, animate-bounce, animate-pulse|
|**自定义动画**|在 tailwind.config.js 中扩展 keyframes 和 animation|

---

## 5️⃣ 变体与组合

|分类|内容|
|---|---|
|**组合类**|flex + justify-center + items-center|
|**状态变体**|hover:, focus:, active:, disabled:|
|**响应式变体**|sm:, md:, lg:, xl:, 2xl:|
|**暗黑模式变体**|dark:|

---

## 6️⃣ Tailwind 高级特性

|分类|内容|
|---|---|
|**插件系统**|typography, forms, aspect-ratio, line-clamp, 自定义插件|
|**CSS 变量支持**|theme.extend.colors, theme.extend.spacing|
|**自定义工具类**|@layer utilities, @apply 指令复用样式|
|**Purging**|移除未使用 CSS，优化打包体积|

---

## 7️⃣ Tailwind 与现代开发

|分类|内容|
|---|---|
|**与框架集成**|React (className), Vue, Angular, Svelte, Next.js|
|**组件化**|使用 @apply 定义可复用类、结合组件库|
|**设计系统**|配合设计 tokens、配置主题颜色和间距|
|**调试工具**|Tailwind Play, VSCode Tailwind IntelliSense 插件|

---

## 8️⃣ 性能优化

|分类|内容|
|---|---|
|**JIT 模式**|按需生成 CSS|
|**Purging**|生产环境删除未使用的类|
|**小文件体积**|配置 theme.extend 避免无用类生成|


# 🚀 Tailwind CSS 教程

## 1. 什么是 Tailwind CSS
- **定义**：Tailwind CSS 是一个 **原子化 CSS 框架**，用类名直接控制样式  
- **特点**：
  - 原子化类（例如 `text-red-500`、`bg-gray-100`）
  - 响应式设计内置（`sm:`, `md:`, `lg:`）
  - 支持暗黑模式
  - 易于定制主题
- **适用场景**：
  - 快速搭建 UI
  - 配合 React / Vue / Next.js 开发 SPA 或企业级项目

---

## 2. 安装 Tailwind CSS

### 2.1 新建项目（以 Vite + React 为例）
```bash
npm create vite@latest my-app
cd my-app
npm install
```

### 2.2 安装 Tailwind
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```
生成：
- `tailwind.config.js`
- `postcss.config.js`

---

## 3. 配置 Tailwind

编辑 `tailwind.config.js`：
```js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

---

## 4. 引入 Tailwind 样式

在 `src/index.css` 或 `globals.css` 中：
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

在入口文件 `main.jsx` 中引入：
```jsx
import "./index.css";
```

---

## 5. Tailwind 基础用法

### 5.1 布局与定位
```jsx
<div className="flex items-center justify-center h-screen bg-gray-100">
  <h1 className="text-4xl font-bold text-blue-600">Hello Tailwind!</h1>
</div>
```

### 5.2 响应式设计
```jsx
<div className="text-sm sm:text-base md:text-lg lg:text-xl">
  响应式文字
</div>
```

### 5.3 颜色与背景
```jsx
<div className="bg-red-500 text-white p-4 rounded">红色盒子</div>
```

### 5.4 间距
```jsx
<div className="m-4 p-6 space-y-4">
  <p>段落1</p>
  <p>段落2</p>
</div>
```

---

## 6. 高级功能

### 6.1 自定义主题
```js
// tailwind.config.js
theme: {
  extend: {
    colors: {
      primary: '#1DA1F2',
      secondary: '#14171A',
    },
    spacing: {
      128: '32rem',
    },
  },
},
```
使用：
```jsx
<div className="bg-primary text-white p-8">自定义颜色</div>
```

### 6.2 暗黑模式
```js
// tailwind.config.js
darkMode: 'class', // 或 'media'
```
切换：
```jsx
<div className="bg-white dark:bg-gray-800 text-black dark:text-white">
  暗黑模式支持
</div>
```

### 6.3 插件
- `@tailwindcss/forms` → 表单样式  
- `@tailwindcss/typography` → 排版样式  
- `@tailwindcss/aspect-ratio` → 宽高比  

安装示例：
```bash
npm install -D @tailwindcss/forms
```
配置：
```js
plugins: [require('@tailwindcss/forms')],
```

---

## 7. Tailwind + React 使用建议
- 使用 **组件封装类名**，减少重复
- 利用 **clsx / classnames** 动态切换类
- 配合 **Headless UI** 构建交互组件（Modal、Dropdown）

---

## 8. 构建与部署
- 开发模式：`npm run dev`
- 生产构建：`npm run build`
- Tailwind 会自动移除未使用的类（Purging）
- 部署到 Vercel / Netlify / Docker

---

## 9. 参考资源
- 官方文档：[https://tailwindcss.com](https://tailwindcss.com)  
- Headless UI：[https://headlessui.com](https://headlessui.com)  
- Tailwind Play（在线实验）：[https://play.tailwindcss.com](https://play.tailwindcss.com)
