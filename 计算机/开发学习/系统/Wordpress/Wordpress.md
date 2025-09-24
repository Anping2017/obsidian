## 1️⃣ WordPress 基础

| 分类        | 内容                                                |
| --------- | ------------------------------------------------- |
| **概念**    | CMS（内容管理系统）、博客系统、开源软件                             |
| **安装与环境** | 本地环境（XAMPP、MAMP、Laragon）、服务器部署、数据库（MySQL/MariaDB） |
| **界面操作**  | 仪表盘、文章/页面管理、分类/标签管理、媒体库、菜单、主题切换                   |

---

## 2️⃣ WordPress 核心结构

|分类|内容|
|---|---|
|**文件结构**|wp-admin、wp-includes、wp-content、index.php、wp-config.php|
|**数据库结构**|wp_posts、wp_users、wp_options、wp_postmeta、wp_terms、wp_term_relationships|
|**工作原理**|请求 → index.php → wp-load.php → wp-blog-header.php → WP 核心加载 → 插件/主题执行 → 输出 HTML|
|**模板层次**|index.php → home.php → single.php → page.php → archive.php → 404.php|
|**钩子机制**|Actions、Filters，插件和主题扩展的核心|

---

## 3️⃣ WordPress 前端

|分类|内容|
|---|---|
|**主题开发**|header.php、footer.php、sidebar.php、functions.php|
|**模板标签**|`the_title()`, `the_content()`, `get_header()`, `get_footer()`|
|**循环（The Loop）**|WP_Query、while ( have_posts() ) : the_post()|
|**自定义模板**|page templates, single templates, archive templates|
|**样式与脚本**|enqueue_style(), enqueue_script(), 自定义 CSS/JS|
|**前端框架结合**|React（Gutenberg）、Vue、SPA 前端调用 REST API|

---

## 4️⃣ WordPress 后端

|分类|内容|
|---|---|
|**插件开发**|hooks（add_action / add_filter）、短代码、widgets、options API|
|**自定义文章类型（CPT）**|register_post_type()|
|**自定义分类法**|register_taxonomy()|
|**自定义字段**|postmeta、ACF 插件、自定义字段 API|
|**用户与权限**|roles、capabilities、wp_get_current_user()|
|**REST API**|wp-json、GET/POST 请求、返回 JSON 数据|
|**数据库操作**|$wpdb、get_posts()、insert/update/delete 数据|

---

## 5️⃣ WordPress 高级功能

|分类|内容|
|---|---|
|**Gutenberg 区块编辑器**|区块注册、区块属性、JS/React 开发自定义区块|
|**缓存优化**|Object Cache、Transients API、WP Super Cache、W3 Total Cache|
|**安全**|wp_nonce、sanitize_text_field、XSS/SQL 注入防护、登录安全|
|**性能优化**|懒加载、数据库优化、图片压缩、CDN|
|**多站点**|WordPress Multisite、wp_blogs 表、站点管理|

---

## 6️⃣ WordPress 与前端交互

|分类|内容|
|---|---|
|**AJAX**|admin-ajax.php、wp_ajax_、wp_ajax_nopriv_|
|**REST API**|自定义 endpoint、认证（cookie / OAuth / JWT）|
|**PWA / SPA**|使用 Service Worker + WP REST API，实现离线访问和单页应用体验|
|**主题与前端框架结合**|Headless WordPress + React / Vue / Next.js|

---

## 7️⃣ WordPress 工具与生态

|分类|内容|
|---|---|
|**插件**|WooCommerce、Yoast SEO、ACF、Elementor、WP Rocket|
|**主题**|Twenty 系列、Divi、Astra、GeneratePress|
|**开发工具**|WP-CLI、Debug Bar、Query Monitor、Local by Flywheel|
|**版本管理**|Git + Composer + WP Packagist|
|**学习资源**|Codex、Developer Handbook、WPBeginner|

---

## 8️⃣ WordPress 部署与运维

|分类|内容|
|---|---|
|**环境**|Apache/Nginx、PHP-FPM、MySQL/MariaDB|
|**备份与迁移**|UpdraftPlus、All-in-One WP Migration|
|**安全策略**|防火墙（Wordfence）、SSL、权限管理|
|**更新**|核心更新、插件更新、主题更新|
|**性能监控**|New Relic、Query Monitor、Server Logs|