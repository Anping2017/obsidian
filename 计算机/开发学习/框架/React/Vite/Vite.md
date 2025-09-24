# 🚀 Vite 教程（React 方向）

## 1️⃣ 什么是 Vite？

- **Vite** 是一个新一代前端构建工具，由 Vue 作者尤雨溪开发。
    
- 目标：**更快的开发体验**。
    
- 核心特点：
    
    1. **极速冷启动**：基于 ES 模块（ESM），不用打包就能启动。
        
    2. **按需编译**：只加载当前访问页面用到的文件。
        
    3. **热更新（HMR）快**：修改文件只更新局部，不会全量刷新。
        
    4. **开箱即用**：支持 TS、JSX、CSS、PostCSS。
        
    5. **灵活扩展**：基于 Rollup 插件体系。
        

---

## 2️⃣ 安装 Vite

### （推荐）npm 方式

`npm create vite@latest my-app`

👉 执行后会出现交互式选择：

```
✔ Project name: … my-app
✔ Select a framework: › React
✔ Select a variant: › JavaScript / TypeScript

```

### yarn / pnpm

```
yarn create vite my-app
pnpm create vite my-app

```

---

## 3️⃣ 运行项目

进入目录并安装依赖：

```
cd my-app
npm install
npm run dev

```

默认启动地址：

`http://localhost:5173`

---

## 4️⃣ 项目结构

```
my-app/
 ├─ index.html       # 入口 HTML
 ├─ package.json
 ├─ vite.config.js   # Vite 配置文件
 ├─ src/
 │   ├─ main.jsx     # 入口文件（挂载 React）
 │   ├─ App.jsx      # 根组件
 │   └─ assets/      # 静态资源

```

### main.jsx

```
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

```

### App.jsx

```
export default function App() {
  return <h1>Hello Vite + React 🚀</h1>;
}

```

---

## 5️⃣ Vite 常用命令

```
npm run dev     # 启动开发服务器
npm run build   # 构建生产版本
npm run preview # 本地预览生产构建结果

```

---

## 6️⃣ 配置文件（vite.config.js）

示例（React 项目）：

```
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,      // 启动端口
    open: true,      // 自动打开浏览器
  },
  build: {
    outDir: "dist",  // 输出目录
  },
});

```

---

## 7️⃣ 常见功能扩展

1. **CSS 处理**
    
    - 内置支持 PostCSS / CSS Modules。
        
    - 推荐用 TailwindCSS：
        
```
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

```
        
2. **别名设置**  
    在 `vite.config.js`：
    
```
import path from "path";

export default defineConfig({
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
});

```
    
    👉 引入时可用 `@/components/Button`
    
3. **环境变量**
    
    - 在项目根目录添加 `.env` 文件：
        
        `VITE_API_URL=https://api.example.com`
        
    - 在代码中使用：
        
        `console.log(import.meta.env.VITE_API_URL);`
        

---

## 8️⃣ Vite vs Create React App（CRA）

|对比点|Vite|CRA|
|---|---|---|
|启动速度|⚡ 极速|🐢 较慢|
|热更新|⚡ 快|一般|
|构建工具|Rollup|Webpack|
|配置灵活性|高（插件体系）|较低|
|生态|新兴但发展快|成熟但慢慢被替代|

👉 现在多数新项目都推荐 **Vite**。

---

## 9️⃣ 部署

构建生产版本：

`npm run build`

会生成 `dist/` 文件夹，把它部署到：

- **静态托管平台**：Vercel、Netlify、Surge
    
- **传统服务器**：Nginx / Apache
    
- **云平台**：AWS S3、Firebase、Cloudflare Pages
    

---

## 🔟 学习路线建议

1. 掌握基本命令（dev/build/preview）
    
2. 学会改 `vite.config.js`
    
3. 熟悉 **环境变量** 和 **别名**
    
4. 配合 **TailwindCSS / React Router / Zustand** 搭建完整项目
    

---

⚡ 总结：  
Vite 是 **轻量、极速、现代化** 的前端开发工具，React 开发里已经逐渐取代 CRA，成为主流。