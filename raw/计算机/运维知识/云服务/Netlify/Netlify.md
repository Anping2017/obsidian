# 🌐 Netlify 知识地图

## 1. 基础概念

- **Netlify 是什么？**
    
    - 一个 **现代 Web 应用托管与自动化平台**
        
    - 支持 **静态网站**、**Jamstack 架构**、**前端 + 无服务函数（Serverless Functions）**
        
- **核心优势**
    
    - CI/CD 自动化部署
        
    - 全球 CDN，极速访问
        
    - 简化前端开发 → 部署全链路
        

---

## 2. 核心功能模块

### 🚀 部署与托管

- **Git 集成**：直接连 GitHub / GitLab / Bitbucket，代码更新 → 自动部署
    
- **CI/CD Pipeline**：自动构建 + 预览环境 + 回滚
    
- **环境变量管理**
    

### 🌍 域名与路由

- 自定义域名绑定
    
- 免费 HTTPS / SSL 证书（Let’s Encrypt）
    
- 重定向 & 重写规则（`_redirects` 文件）
    

### ⚡ 无服务功能

- **Netlify Functions**：基于 AWS Lambda 的 Serverless 函数
    
- **Edge Functions**：运行在 CDN 边缘，低延迟逻辑（A/B 测试、个性化内容）
    

### 📦 插件与集成

- 构建插件市场（SEO、性能优化、GraphQL 等）
    
- 与 CMS 集成（Contentful、Sanity、Strapi、Netlify CMS）
    
- 第三方服务（Auth0、Supabase、Shopify 等）
    

### 🔐 身份认证

- **Netlify Identity**：内置用户认证（基于 JWT）
    
- 登录 / 注册 / 社交登录
    
- 与 Netlify Functions 联动，实现个性化 API
    

### 🗄 数据与表单

- **Netlify Forms**：无需后端即可收集表单数据
    
- **Netlify Analytics**：内置分析，无需第三方脚本
    

---

## 3. 技术生态

- **Jamstack 架构核心支撑**
    
    - JavaScript + API + Markup
        
    - 前后端彻底解耦
        
- **框架支持**
    
    - React, Vue, Next.js, Nuxt, Astro, SvelteKit 等
        
- **API 优先**：适合 Headless CMS、GraphQL API、微服务
    

---

## 4. 使用场景

1. **个人 / 团队博客 & 静态网站**
    
2. **初创产品 Landing Page**
    
3. **电商前端（结合 Shopify / Snipcart）**
    
4. **文档网站（结合 Docusaurus、Docsify）**
    
5. **带认证的轻应用（结合 Identity + Functions）**
    
6. **Jamstack 电商 / SaaS 应用**
    

---

## 5. 学习路径（建议）

1. **入门**
    
    - 注册 Netlify → 绑定 GitHub 仓库 → 部署静态页面（HTML/React）
        
2. **进阶**
    
    - 使用 Functions + Forms，构建无后端动态功能
        
    - 配置 `_redirects`，熟悉路由规则
        
    - 尝试 Identity 认证（会员系统）
        
3. **高手**
    
    - 利用 Edge Functions 实现个性化渲染
        
    - 构建插件自动优化性能
        
    - 与 Headless CMS + GraphQL API 集成
        
    - 部署多环境、多分支预览
        

---

## 6. 生态对比

- **Netlify vs Vercel**
    
    - Netlify：更适合 **静态网站 + 无服务函数 + CMS 集成**
        
    - Vercel：更强在 **Next.js / 动态 SSR 支持**
        
- **Netlify vs AWS Amplify**
    
    - Netlify：上手快，配置少，偏前端友好
        
    - Amplify：功能更全（数据库、存储、后端服务），但复杂
        

---

## 7. 学习资源

- 官方文档
    
- Jamstack.org
    
- Netlify Blog & Case Studies
    
- GitHub 上的 Netlify Starter Templates