## 1️⃣ 基础概念

|分类|内容|
|---|---|
|**定义**|OpenCart 是一个开源 PHP + MySQL 的电子商务平台，适合中小型电商|
|**技术栈**|PHP (MVC-L) + MySQL + HTML/CSS/JS + Bootstrap/jQuery|
|**核心特点**|轻量、模块化、多店铺、多语言、多币种|
|**文件结构**|admin、catalog、system、image、config.php 等|
|**MVC-L 模式**|Model-View-Controller + Loader (Loader 用于加载模型、语言包、库)|

---

## 2️⃣ 核心模块

|模块|主要功能|
|---|---|
|**产品管理**|商品添加、编辑、分类管理、选项、属性、规格、库存|
|**订单管理**|订单列表、订单状态管理、发票生成、退货管理|
|**客户管理**|用户注册/登录、会员等级、客户组、客户积分|
|**购物车与结账**|购物车、结账流程、支付方式、配送方式|
|**支付与配送**|PayPal、Stripe、银行转账、货到付款、快递配送|
|**营销工具**|优惠券、礼品券、促销活动、积分、会员等级|
|**多语言与多币种**|支持多语言包、多币种自动汇率|

---

## 3️⃣ 开发与扩展

|分类|内容|
|---|---|
|**模板系统**|Twig 模板 + 控制器传递数据 → View 渲染|
|**模块/扩展开发**|插件 (Extension) 系统：模块、支付、配送、主题|
|**事件系统**|Event Trigger → 允许在核心逻辑前后挂钩自定义代码|
|**VQMod / OCMOD**|核心文件修改系统，避免直接修改源代码|
|**语言包**|admin 和 catalog 双端语言文件管理|
|**模型开发**|catalog/model 和 admin/model，用于数据库操作|
|**控制器开发**|catalog/controller 和 admin/controller，用于业务逻辑处理|
|**路由系统**|index.php + front/controller/admin/controller.php + route 参数|

---

## 4️⃣ 数据库结构

|表分类|主要用途|
|---|---|
|**产品表**|oc_product, oc_product_description, oc_product_to_category|
|**订单表**|oc_order, oc_order_product, oc_order_total|
|**客户表**|oc_customer, oc_customer_group|
|**购物车/会话**|oc_cart, oc_session|
|**多语言/多币种**|oc_language, oc_currency|
|**模块/扩展配置**|oc_extension, oc_setting|

---

## 5️⃣ 优化与性能

|分类|内容|
|---|---|
|**缓存**|文件缓存、内存缓存（Redis, Memcached）|
|**图片优化**|缩略图、WebP 格式|
|**SEO优化**|URL 重写、Meta 标签、Sitemap|
|**CDN 加速**|静态资源分发|
|**数据库优化**|索引优化、查询优化|

---

## 6️⃣ 部署与运维

|分类|内容|
|---|---|
|**服务器要求**|PHP >= 7.3, MySQL/MariaDB, Apache/Nginx|
|**安全措施**|权限管理、SSL、后台防护、VQMod/OCMOD 安全更新|
|**备份与恢复**|数据库备份、文件备份、增量备份|
|**版本升级**|OCMOD/VQMod 兼容性检查、主题和插件升级|