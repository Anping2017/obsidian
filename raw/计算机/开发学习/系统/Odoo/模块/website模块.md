# 🌐 Odoo `website` 模块详解

## 一、`website` 模块的作用

- **网站构建器核心模块**，Odoo 网站功能的基础。
- 提供拖放式网站编辑器和内容管理系统（CMS）。
- 无需编程即可创建和管理专业网站。
- 支持 SEO 优化、多语言、响应式设计等功能。
- 是 `website_sale`、`website_blog` 等网站相关模块的基础。

📌 形象理解：  
👉 `website` 模块是网站的"编辑器和控制中心"，让用户像编辑文档一样编辑网站。

---

## 二、核心功能

### 1. 拖放式网站编辑器

#### 编辑器功能

- **可视化编辑**：所见即所得（WYSIWYG）的编辑体验
- **拖放元素**：拖拽组件到页面任意位置
- **实时预览**：编辑时实时查看效果
- **元素库**：丰富的页面元素组件

#### 可编辑元素

- **文本块**：标题、段落、列表等
- **图片**：上传和插入图片
- **视频**：嵌入视频内容
- **按钮**：创建各种按钮
- **布局**：列布局、网格布局等
- **表单**：联系表单、注册表单等
- **HTML 代码**：自定义 HTML 块

#### 编辑模式

- **编辑模式**：点击"编辑"进入编辑状态
- **预览模式**：查看最终效果
- **发布/取消发布**：控制页面是否可见

### 2. 页面管理

#### 页面模型

```
class WebsitePage(models.Model):
    _name = 'website.page'
    _description = 'Website Page'
    
    name = fields.Char('Page Name', required=True)
    url = fields.Char('URL', required=True)
    view_id = fields.Many2one('ir.ui.view', 'View')
    website_id = fields.Many2one('website', 'Website')
    is_published = fields.Boolean('Is Published')
    website_meta_title = fields.Char('Website Meta Title')
    website_meta_description = fields.Text('Website Meta Description')
    website_meta_keywords = fields.Char('Website Meta Keywords')
    website_meta_og_image = fields.Binary('Website OG Image')
```

#### 页面类型

- **标准页面**：普通内容页面
- **首页**：网站首页
- **菜单页面**：导航菜单中的页面
- **系统页面**：登录、注册等系统页面

#### 页面管理功能

- **创建页面**：创建新的页面
- **编辑页面**：修改页面内容
- **删除页面**：删除不需要的页面
- **页面预览**：预览页面效果
- **发布/取消发布**：控制页面可见性

### 3. SEO 优化（Search Engine Optimization）

#### SEO 功能

- **Meta 标签**：
  - Meta Title：页面标题（影响搜索结果）
  - Meta Description：页面描述
  - Meta Keywords：关键词

- **OG（Open Graph）标签**：
  - OG Title：社交媒体分享标题
  - OG Description：社交媒体分享描述
  - OG Image：社交媒体分享图片

- **URL 优化**：
  - 友好的 URL 结构
  - 可自定义 URL
  - URL 重定向

- **站点地图**：自动生成 XML 站点地图

- **robots.txt**：搜索引擎爬虫规则

#### SEO 最佳实践

- 每个页面设置唯一的 Meta Title
- 编写有吸引力的 Meta Description
- 使用关键词优化内容
- 优化图片 Alt 文本
- 确保网站快速加载

### 4. 多语言网站

#### 多语言支持

- **语言管理**：添加和管理多种语言
- **内容翻译**：为每种语言翻译内容
- **语言切换**：网站访问者可以切换语言
- **自动检测**：根据浏览器语言自动选择

#### 翻译功能

- **翻译界面**：专门的翻译编辑界面
- **翻译状态**：显示哪些内容已翻译
- **翻译记忆**：保存常用翻译
- **专业翻译**：可集成专业翻译服务

### 5. 主题管理

#### 主题系统

- **主题选择**：从多个主题中选择
- **主题定制**：自定义主题颜色、字体等
- **响应式设计**：自动适配不同设备
- **主题预览**：切换主题前预览效果

#### 主题组件

- **颜色方案**：预设和自定义颜色
- **字体**：选择字体类型
- **布局**：选择页面布局样式
- **样式**：自定义 CSS（高级用户）

### 6. 网站配置

#### 网站基本信息

```
class Website(models.Model):
    _name = 'website'
    _description = 'Website'
    
    name = fields.Char('Website Name', required=True)
    domain = fields.Char('Website Domain')
    company_id = fields.Many2one('res.company', 'Company')
    default_lang_id = fields.Many2one('res.lang', 'Default Language')
    social_facebook = fields.Char('Facebook Account')
    social_twitter = fields.Char('Twitter Account')
    social_linkedin = fields.Char('LinkedIn Account')
    social_github = fields.Char('GitHub Account')
    social_youtube = fields.Char('Youtube Account')
    social_instagram = fields.Char('Instagram Account')
```

#### 配置选项

- **网站名称和域名**
- **公司信息**：关联的公司
- **默认语言**：网站默认语言
- **社交媒体链接**：Facebook、Twitter 等
- **联系信息**：电话、邮箱、地址
- **Logo**：网站 Logo

### 7. 菜单管理

#### 菜单系统

- **主菜单**：网站顶部导航菜单
- **页脚菜单**：网站底部菜单
- **菜单层级**：支持多级菜单
- **菜单顺序**：拖拽调整顺序

#### 菜单配置

- 创建菜单项
- 关联页面或 URL
- 设置菜单显示条件
- 多语言菜单标签

---

## 三、核心模型详解

### 1. `website.page` - 网站页面

**主要字段**：
- `name`：页面名称（必填）
- `url`：页面 URL（必填）
- `view_id`：关联的视图（Odoo 视图系统）
- `website_id`：所属网站（多网站支持）
- `is_published`：是否发布
- `website_meta_title`：SEO 标题
- `website_meta_description`：SEO 描述

**使用示例**：

```python
# 创建页面
page = self.env['website.page'].create({
    'name': 'About Us',
    'url': '/about-us',
    'website_id': website.id,
    'is_published': True,
    'website_meta_title': 'About Us - Company Name',
    'website_meta_description': 'Learn more about our company',
})

# 查找已发布的页面
pages = self.env['website.page'].search([
    ('is_published', '=', True),
    ('website_id', '=', website.id),
])
```

### 2. `website` - 网站

**主要字段**：
- `name`：网站名称（必填）
- `domain`：网站域名
- `company_id`：关联的公司
- `default_lang_id`：默认语言
- `social_*`：社交媒体链接

---

## 四、与其他模块的集成

### 1. 与 `website_sale` 模块

**在线商店**：
- 产品展示页面
- 购物车页面
- 结账页面
- 产品详情页

### 2. 与 `website_blog` 模块

**博客功能**：
- 博客文章列表页
- 博客文章详情页
- 博客分类页
- 博客标签页

### 3. 与 `website_forum` 模块

**论坛功能**：
- 论坛首页
- 帖子列表页
- 帖子详情页
- 用户个人资料页

### 4. 与 `website_event` 模块

**活动管理**：
- 活动列表页
- 活动详情页
- 活动注册页

### 5. 与 `contacts` 模块

**联系表单**：
- 联系表单自动创建潜在客户
- 表单数据存储在 `crm.lead`

---

## 五、网站工作流程

### 1. 创建网站流程

```
1. 安装 website 模块
   ↓
2. 配置网站基本信息
   - 设置网站名称
   - 选择主题
   - 配置语言
   ↓
3. 创建首页
   - 使用编辑器设计首页
   - 添加内容和元素
   ↓
4. 创建其他页面
   - 关于我们
   - 联系我们
   - 服务介绍
   ↓
5. 配置菜单
   - 创建导航菜单
   - 添加菜单项
   ↓
6. SEO 优化
   - 设置每个页面的 SEO 信息
   - 优化 URL
   ↓
7. 发布网站
   - 检查所有页面
   - 发布网站
```

### 2. 编辑页面流程

```
1. 进入编辑模式
   - 点击"编辑"按钮
   - 或访问 /page/edit
   ↓
2. 编辑内容
   - 点击元素进行编辑
   - 拖拽元素调整位置
   - 添加新元素
   ↓
3. 预览效果
   - 实时预览
   - 检查不同设备显示
   ↓
4. 保存并发布
   - 保存更改
   - 发布页面（如需要）
```

---

## 六、典型使用场景

### 场景 1：创建公司官网

**需求**：创建一个公司官方网站

**步骤**：

1. **配置网站**
   - 设置网站名称和 Logo
   - 选择主题
   - 配置公司信息

2. **创建首页**
   - 添加公司介绍
   - 添加产品/服务展示
   - 添加联系信息

3. **创建内容页面**
   - 关于我们页面
   - 产品/服务页面
   - 联系我们页面

4. **配置菜单**
   - 设置主导航菜单
   - 设置页脚菜单

5. **SEO 优化**
   - 为每个页面设置 SEO 信息
   - 优化关键词

### 场景 2：多语言网站

**需求**：创建一个支持多语言的网站

**步骤**：

1. **启用多语言**
   - 在设置中启用多语言
   - 添加需要的语言

2. **翻译内容**
   - 翻译每个页面的内容
   - 翻译菜单标签
   - 翻译 SEO 信息

3. **配置语言切换**
   - 在网站上显示语言选择器
   - 访问者可以切换语言

### 场景 3：响应式网站设计

**需求**：确保网站在不同设备上正常显示

**步骤**：

1. **选择响应式主题**
   - 使用支持响应式设计的主题

2. **测试不同设备**
   - 桌面电脑
   - 平板电脑
   - 手机

3. **调整布局**
   - 根据需要调整移动端布局
   - 优化移动端用户体验

---

## 七、配置和设置

### 1. 基本配置

#### 步骤 1：安装模块

1. **应用 > 搜索 "website"**
2. 安装 `website` 模块

#### 步骤 2：配置网站

1. **网站 > 配置 > 设置**
2. 设置网站基本信息
3. 配置公司信息
4. 设置社交媒体链接

#### 步骤 3：选择主题

1. **网站 > 主题**
2. 浏览可用主题
3. 选择并应用主题
4. 自定义主题设置

### 2. SEO 配置

#### 全局 SEO 设置

1. **网站 > 配置 > SEO**
2. 设置默认 Meta 标签
3. 配置站点地图
4. 设置 robots.txt

#### 页面 SEO

1. 编辑每个页面
2. 设置页面 Meta Title
3. 设置页面 Meta Description
4. 设置 OG 标签

### 3. 多语言配置

1. **设置 > 翻译 > 语言**
2. 添加需要的语言
3. 设置默认语言
4. 翻译网站内容

---

## 八、最佳实践

### 1. 内容管理

- **内容质量**：确保内容清晰、准确、有价值
- **定期更新**：定期更新网站内容
- **图片优化**：压缩图片以提高加载速度

### 2. SEO 优化

- **关键词研究**：研究和使用相关关键词
- **内容优化**：在内容中自然地使用关键词
- **内部链接**：建立合理的内部链接结构
- **外部链接**：获取高质量的外部链接

### 3. 用户体验

- **导航清晰**：确保导航菜单清晰易用
- **加载速度**：优化页面加载速度
- **移动友好**：确保移动端体验良好
- **可访问性**：确保网站对所有人都可访问

### 4. 安全

- **HTTPS**：使用 HTTPS 加密
- **定期更新**：保持 Odoo 和模块更新
- **权限控制**：限制编辑权限

---

## 九、常见问题

### 问题 1：页面无法编辑

**原因**：权限不足或未进入编辑模式

**解决方案**：
1. 检查用户是否有编辑权限
2. 确认已进入编辑模式
3. 检查页面是否被锁定

### 问题 2：更改未保存

**原因**：未点击保存按钮

**解决方案**：
1. 确保点击了保存按钮
2. 检查是否有验证错误
3. 刷新页面重新编辑

---

## 十、高级功能

### 1. 自定义开发

- **自定义视图**：创建自定义 QWeb 视图
- **自定义控制器**：创建自定义 URL 路由
- **JavaScript/CSS**：添加自定义脚本和样式

### 2. 多网站支持

- 创建多个网站
- 每个网站独立配置
- 共享或独立的内容

### 3. 网站分析

- 集成 Google Analytics
- 跟踪访问统计
- 分析用户行为

---

## 十一、总结

- **`website` 模块**是 Odoo 网站功能的核心基础。
- 核心功能：
  - 拖放式网站编辑器
  - 页面管理
  - SEO 优化
  - 多语言支持
  - 主题管理
  - 菜单管理
- 无需编程即可创建专业网站。
- 支持响应式设计和 SEO 优化。
- 是构建在线商店、博客、论坛等网站功能的基础。
- 适用于各种类型的网站需求。

