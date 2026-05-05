# 🚀 PostCSS 教程

## 1. 什么是 PostCSS
- **定义**：PostCSS 是一个 **用 JavaScript 处理 CSS 的工具**，可以自动化优化、添加前缀、嵌套规则等  
- **特点**：
  - 通过插件处理 CSS
  - 支持自动添加浏览器前缀
  - 支持嵌套、变量、混入等功能
  - 可与 TailwindCSS、Autoprefixer 等结合使用
- **适用场景**：
  - 自动化 CSS 优化
  - 编写现代 CSS（嵌套、变量）
  - 构建可维护的前端项目

---

## 2. 安装 PostCSS

### 2.1 初始化项目（以 Vite + React 为例）
```bash
npm create vite@latest my-app
cd my-app
npm install
```

### 2.2 安装 PostCSS
```bash
npm install -D postcss autoprefixer
```

### 2.3 创建配置文件
```bash
npx tailwindcss init -p
```
生成：
- `postcss.config.js`
- `tailwind.config.js`（可选）

---

## 3. 配置 PostCSS

`postcss.config.js` 示例：
```js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
    // 其他插件可加入此处
  },
}
```

---

## 4. PostCSS 基本用法

### 4.1 使用嵌套规则
```css
/* input.css */
.button {
  background: blue;
  color: white;

  &:hover {
    background: darkblue;
  }

  .icon {
    margin-right: 0.5rem;
  }
}
```

### 4.2 输出 CSS（编译后）
```css
.button {
  background: blue;
  color: white;
}
.button:hover {
  background: darkblue;
}
.button .icon {
  margin-right: 0.5rem;
}
```

---

## 5. 常用 PostCSS 插件
- **autoprefixer**：自动添加浏览器前缀  
- **postcss-nested**：支持嵌套 CSS  
- **postcss-preset-env**：使用未来 CSS 特性  
- **cssnano**：压缩 CSS

### 安装示例
```bash
npm install -D postcss-nested postcss-preset-env cssnano
```

### 配置示例
```js
module.exports = {
  plugins: [
    require('postcss-nested'),
    require('postcss-preset-env')({ stage: 1 }),
    require('autoprefixer'),
    require('cssnano')({ preset: 'default' }),
  ],
}
```

---

## 6. PostCSS + TailwindCSS
- TailwindCSS 内部已经使用 PostCSS
- 在 `postcss.config.js` 中：
```js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```
- 与 Tailwind 配合时可以添加其他 PostCSS 插件，实现嵌套、压缩、变量等功能

---

## 7. 高级技巧
- 使用 **变量**
```css
:root {
  --main-color: #1DA1F2;
}

.button {
  background: var(--main-color);
}
```
- 使用 **自定义插件**，实现特殊功能
```js
module.exports = {
  plugins: [
    function myPlugin(css) {
      css.walkRules(rule => {
        // 插件逻辑
      });
    },
  ],
}
```

---

## 8. 构建与部署
- Vite / Webpack / Next.js 都可以内置 PostCSS  
- 开发模式自动处理 CSS  
- 生产环境可压缩、自动加前缀

---

## 9. 参考资源
- 官方文档：[https://postcss.org](https://postcss.org)  
- TailwindCSS 集成：[https://tailwindcss.com/docs/using-with-postcss](https://tailwindcss.com/docs/using-with-postcss)  
- CSS Next 特性：[https://preset-env.cssdb.org](https://preset-env.cssdb.org)
