# 🚀 Next.js 教程

## 1. 什么是 Next.js
- **定义**：基于 React 的全栈框架  
- **特点**：
  - 服务端渲染（SSR）
  - 静态生成（SSG）
  - 文件路由（无需 react-router）
  - API Routes（内置后端能力）
  - 图片 & 字体优化
- **适用场景**：
  - 企业官网 / 博客（SEO 友好）
  - 电商平台（SSR + 动态数据）
  - SaaS 应用（全栈能力）

---

## 2. 环境准备
- Node.js 18+（LTS 版本）
- VS Code（推荐插件：ES7+ React、Tailwind CSS IntelliSense）

安装 Next.js 项目：
```bash
npx create-next-app@latest my-app
cd my-app
npm run dev
```

访问开发服务器：
```
http://localhost:3000
```

---

## 3. 项目结构（App Router 模式）
```
my-app/
 ├─ app/
 │   ├─ page.jsx       # 首页（/）
 │   ├─ about/
 │   │   └─ page.jsx   # /about
 │   ├─ layout.jsx     # 全局布局
 │   └─ globals.css    # 全局样式
 ├─ public/            # 静态资源
 ├─ package.json
 └─ next.config.js     # 配置文件
```

示例页面：
```jsx
// app/page.jsx
export default function Home() {
  return <h1>Hello Next.js 🚀</h1>;
}
```

---

## 4. 路由系统
### 基础路由
- `app/page.jsx` → `/`
- `app/about/page.jsx` → `/about`

### 动态路由
```bash
app/blog/[id]/page.jsx
```
```jsx
export default function Blog({ params }) {
  return <h1>文章ID: {params.id}</h1>;
}
```

### 嵌套路由
```
app/dashboard/page.jsx       → /dashboard
app/dashboard/settings/page.jsx → /dashboard/settings
```

### 页面跳转
```jsx
import Link from "next/link";

export default function Nav() {
  return <Link href="/about">About</Link>;
}
```

---

## 5. 渲染模式
- **CSR**（客户端渲染） → 默认 React  
- **SSR**（服务端渲染）
- **SSG**（静态生成）
- **ISR**（增量静态生成）

示例：
```jsx
// 强制动态渲染（SSR）
export const dynamic = "force-dynamic";

// 强制静态渲染（SSG）
export const dynamic = "force-static";
```

---

## 6. 样式与优化
### 全局样式
在 `app/globals.css`：
```css
body {
  font-family: sans-serif;
  margin: 0;
}
```

### 集成 TailwindCSS
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```
配置 `tailwind.config.js`：
```js
content: [
  "./app/**/*.{js,ts,jsx,tsx}",
  "./components/**/*.{js,ts,jsx,tsx}",
]
```

### 图片优化
```jsx
import Image from "next/image";

export default function Avatar() {
  return <Image src="/avatar.png" alt="me" width={100} height={100} />;
}
```

---

## 7. 数据获取
### Server Component
```jsx
export default async function Users() {
  const res = await fetch("https://jsonplaceholder.typicode.com/users");
  const users = await res.json();
  return (
    <ul>
      {users.map(u => <li key={u.id}>{u.name}</li>)}
    </ul>
  );
}
```

### Client Component
```jsx
"use client"; // 必须声明

import { useState, useEffect } from "react";

export default function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

---

## 8. API Routes（后端接口）
创建文件：`app/api/hello/route.js`
```js
export async function GET() {
  return Response.json({ message: "Hello API" });
}
```
访问 `/api/hello` → 返回 JSON 数据。

---

## 9. 部署
构建生产环境：
```bash
npm run build
npm run start
```

推荐部署平台：
- **Vercel**（官方最佳方案）
- Netlify
- Docker + Nginx
- AWS / Cloudflare Pages

---

## 🔟 进阶功能
- **Middleware**：请求拦截（权限控制、重定向）
- **NextAuth.js**：身份认证
- **国际化 (i18n)**：多语言支持
- **Edge Runtime**：更快的边缘计算能力

---
