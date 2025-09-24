## 一、基础认知层

### 1. Vercel 是什么

- **前端优先的云平台**，专注于 **Web 应用的部署与交付**
    
- 创始团队来自 **Next.js**，因此与 Next.js 深度绑定
    
- 核心价值：**让前端工程师无需关心后端运维，也能上线高性能应用**
    

### 2. 核心特征

- **无服务器（Serverless）**
    
- **边缘计算（Edge Functions / Edge Config）**
    
- **自动化（CI/CD 集成）**
    
- **全球 CDN 加速**
    
- **前端框架优化（尤其是 Next.js）**
    

---

## 二、核心功能层

### 1. 应用部署

- 一键连接 GitHub / GitLab / Bitbucket
    
- 自动 CI/CD：每次 push → 自动构建 + 部署
    
- Preview Deployments（预览环境）：每个 PR/分支都能有独立链接
    

### 2. 静态资源 & 动态渲染

- **静态网站托管**（SSG，适合博客、文档、营销页）
    
- **服务端渲染（SSR）**（配合 Next.js，适合电商、应用）
    
- **ISR（增量静态生成）**：兼顾静态速度与动态更新
    

### 3. 无服务器函数

- **Serverless Functions**：Node.js / Python / Go / Ruby
    
- **Edge Functions**：运行在边缘节点，延迟极低（适合认证、A/B 测试、个性化内容）
    

### 4. 数据与配置

- **Edge Config**：超低延迟的全局配置存储
    
- **KV（键值数据库，beta）**：适合缓存、用户会话
    
- **Postgres / Blob Storage（托管数据库与对象存储）**
    

---

## 三、性能与监控层

- **Analytics**：Web 性能与流量分析（类似 Google Analytics，但更原生）
    
- **Speed Insights**：Core Web Vitals 监控
    
- **Monitoring**：函数调用、延迟、错误率追踪
    

---

## 四、协作与工作流层

- **Preview Deployments**：团队可以在合并代码前预览
    
- **评论与协作**：团队成员可直接对预览版本进行反馈
    
- **环境管理**：Development / Preview / Production 三环境切换
    

---

## 五、安全与运维层

- **自动 HTTPS + SSL 证书**
    
- **自定义域名**（支持子域、子路径部署）
    
- **访问控制**（私有部署、密码保护）
    
- **合规性**（GDPR、SOC 2 等）
    

---

## 六、生态与扩展层

- **Next.js 深度集成**（Image Optimization, Middleware, App Router）
    
- **第三方集成**：Supabase、Firebase、Prisma、Stripe、Auth0
    
- **Vercel Marketplace**：插件与扩展（SEO 工具、Headless CMS、Analytics）
    

---

## 七、对比 Firebase 的定位

- **Firebase**：偏后端服务（数据库、认证、消息、函数、存储）
    
- **Vercel**：偏前端交付（部署、渲染、CDN、边缘计算）  
    👉 常见组合：**Vercel + Firebase**（前端部署 & 后端服务） 或 **Vercel + Supabase**
    

---

## 八、学习路径（推荐）

1. **入门**：托管一个静态网站（HTML/CSS/JS）
    
2. **进阶**：部署 Next.js 应用，体验 SSG / SSR / ISR
    
3. **扩展**：使用 Serverless Functions（API 路由）
    
4. **专业化**：接入 Edge Functions、数据库（Postgres/KV）、监控分析
    
