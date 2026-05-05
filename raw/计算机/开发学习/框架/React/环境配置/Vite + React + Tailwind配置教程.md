

## 1️⃣ 环境准备

先安装：

- **Node.js 18+**（LTS 版本，附带 npm）
    
- **VS Code**（推荐装 React、Tailwind 插件）
    

检查版本：

```
node -v
npm -v

```

---

## 2️⃣ 创建 React 项目（基于 Vite）

```
# 创建项目
npm create vite@latest my-app

# 进入项目
cd my-app

# 安装依赖
npm install

# 启动开发服务器
npm run dev

```

此时访问 `http://localhost:5173`，就能看到 React 初始页面。

---

## 3️⃣ 安装 TailwindCSS

在项目目录执行：

```
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

```

会生成：

- `tailwind.config.js`
    
- `postcss.config.js`
    

---

## 4️⃣ 配置 Tailwind

编辑 `tailwind.config.js`：

```
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",  // 让 Tailwind 扫描 src 目录
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

```

---

## 5️⃣ 引入 Tailwind 样式

在 `src/index.css` 里写入：

```
@tailwind base;
@tailwind components;
@tailwind utilities;

```

---

## 6️⃣ 修改入口文件测试

编辑 `src/App.jsx`：

```
export default function App() {
  return (
    <div className="flex h-screen items-center justify-center bg-gray-100">
      <h1 className="text-4xl font-bold text-blue-600">
        🚀 Vite + React + Tailwind 配置成功！
      </h1>
    </div>
  );
}

```

重新运行：

`npm run dev`

👉 页面居中显示蓝色大标题，说明 Tailwind 已生效。

---

## 7️⃣ 项目结构（推荐）

```
my-app/
 ├─ public/           # 静态文件
 ├─ src/
 │   ├─ assets/       # 图片、图标
 │   ├─ components/   # 组件
 │   ├─ pages/        # 页面
 │   ├─ hooks/        # 自定义 hooks
 │   ├─ App.jsx       # 根组件
 │   ├─ main.jsx      # 入口文件
 │   └─ index.css     # 全局样式
 ├─ tailwind.config.js
 ├─ package.json
 └─ vite.config.js

```

---

## 8️⃣ 进阶优化（可选）

- **代码规范**：
    
```
npm install -D eslint prettier eslint-config-prettier eslint-plugin-react-hooks
```    
- **状态管理**：Zustand / Redux Toolkit
    
- **路由**：React Router v6
    
    `npm install react-router-dom`
    

---

✅ 到这里，你就拥有一个 **Vite + React + Tailwind 的现代化开发环境**，能做企业级项目。