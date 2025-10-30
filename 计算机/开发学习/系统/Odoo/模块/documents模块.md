# 📁 Odoo `documents` 模块详解

## 一、`documents` 模块的作用

- **文档管理系统**，企业级文档存储和管理解决方案。
- 集中管理企业所有文档：合同、发票、报告、图片等。
- 支持文档分类、标签、搜索和版本控制。
- 提供文档共享、协作和审批工作流。
- 与业务模块集成，自动关联文档到相关业务记录。

📌 形象理解：  
👉 `documents` 模块是"企业文件柜"，统一管理和存储所有企业文档。

---

## 二、核心功能

### 1. 文档存储和管理

#### 文档模型

```
class DocumentDocument(models.Model):
    _name = 'documents.document'
    _description = 'Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Name', required=True)
    folder_id = fields.Many2one('documents.folder', 'Folder', required=True)
    type = fields.Selection([('empty', 'Request'), ('binary', 'File'), ('url', 'URL')],
                           string='Type', required=True, default='empty')
    res_model = fields.Char('Resource Model', index=True)
    res_id = fields.Many2oneReference('Resource ID', model_field='res_model', index=True)
    active = fields.Boolean('Active', default=True)
    attachment_id = fields.Many2one('ir.attachment', 'Attachment')
    file_size = fields.Integer('File Size', related='attachment_id.file_size')
    thumbnail = fields.Binary('Thumbnail', related='attachment_id.thumbnail')
    mimetype = fields.Char('MIME Type', related='attachment_id.mimetype')
    checksum = fields.Char('Checksum', related='attachment_id.checksum')
    index_content = fields.Text('Indexed Content', related='attachment_id.index_content')
    tag_ids = fields.Many2many('documents.tag', 'document_tag_rel', 'document_id', 'tag_id',
                               string='Tags')
    owner_id = fields.Many2one('res.users', 'Owner', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', 'Customer/Vendor')
    company_id = fields.Many2one('res.company', 'Company')
    access_token = fields.Char('Access Token')
    preview = fields.Html('Preview', compute='_compute_preview')
```

#### 文档类型

- **文件（File）**：上传的文件文档（PDF、Word、Excel、图片等）
- **URL**：外部链接文档
- **空文档（Request）**：开展文档请求，等待上传

#### 支持的文件格式

- **办公文档**：PDF、Word、Excel、PowerPoint
- **图片**：JPG、PNG、GIF
- **文本**：TXT、Markdown
- **其他**：ZIP、CSV等

### 2. 文件夹和分类

#### 文件夹模型

```
class DocumentFolder(models.Model):
    _name = 'documents.folder'
    _description = 'Document Folder'
    
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    parent_folder_id = fields.Many2one('documents.folder', 'Parent Folder')
    children_folder_ids = fields.One2many('documents.folder', 'parent_folder_id', 'Sub Folders')
    document_ids = fields.One2many('documents.document', 'folder_id', 'Documents')
    user_specific = fields.Boolean('User Specific', default=False)
    company_id = fields.Many2one('res.company', 'Company')
    read_group_ids = fields.Many2many('res.groups', 'folder_read_group_rel', 'folder_id', 'group_id',
                                     string='Read Groups')
    write_group_ids = fields.Many2many('res.groups', 'folder_write_group_rel', 'folder_id', 'group_id',
                                      string='Write Groups')
```

#### 文件夹功能

- **层级结构**：支持文件夹嵌套
- **权限控制**：设置文件夹的读写权限
- **用户特定**：支持用户专属文件夹
- **自动分类**：基于规则自动分类文档

#### 典型文件夹结构

```
文档根目录
 ├── 财务文档
 │    ├── 发票
 │    ├── 合同
 │    └── 报告
 ├── HR文档
 │    ├── 员工档案
 │    ├── 合同
 │    └── 培训材料
 ├── 销售文档
 │    ├── 报价单
 │    ├── 订单
 │    └── 客户资料
 └── 项目文档
      ├── 项目计划
      ├── 会议记录
      └── 交付物
```

### 3. 标签管理

#### 标签模型

```
class DocumentTag(models.Model):
    _name = 'documents.tag'
    _description = 'Document Tag'
    
    name = fields.Char('Name', required=True, translate=True)
    color = fields.Integer('Color')
    folder_id = fields.Many2one('documents.folder', 'Folder')
```

#### 标签功能

- **分类标记**：使用标签标记文档特征
- **颜色标识**：使用颜色区分不同类型的标签
- **快速筛选**：通过标签快速筛选文档
- **多标签支持**：一个文档可以有多个标签

### 4. 文档搜索

#### 搜索功能

- **全文搜索**：基于文档内容搜索
- **按名称搜索**：搜索文档名称
- **按标签搜索**：基于标签筛选
- **按文件夹搜索**：在指定文件夹内搜索
- **高级搜索**：多条件组合搜索

### 5. 文档共享和协作

#### 共享方式

- **内部共享**：在公司内部共享文档
- **外部共享**：通过链接共享给外部人员
- **权限控制**：设置查看、编辑、删除权限
- **访问令牌**：使用访问令牌控制访问

#### 协作功能

- **评论**：在文档上添加评论
- **版本控制**：跟踪文档版本变更
- **审批流程**：文档审批工作流
- **通知**：文档变更通知

---

## 三、与其他模块的集成

### 1. 与 `account` 模块

- **发票附件**：自动关联发票文档
- **凭证附件**：会计凭证的附件管理

### 2. 与 `sale` 模块

- **报价单附件**：报价单相关文档
- **订单附件**：销售订单文档
- **客户文档**：客户相关文档

### 3. 与 `purchase` 模块

- **采购订单附件**：采购相关文档
- **供应商文档**：供应商文档管理

### 4. 与 `hr` 模块

- **员工档案**：员工档案文档
- **合同管理**：员工合同文档
- **培训材料**：培训相关文档

### 5. 与 `project` 模块

- **项目文档**：项目相关文档
- **交付物管理**：项目交付物文档

---

## 四、典型使用场景

### 场景 1：存储和管理合同

**需求**：管理公司所有合同文档

**步骤**：

1. **创建文件夹**
   ```
   文档 > 文件夹 > 新建
   - 名称：合同文档
   - 描述：存储所有合同
   ```

2. **上传合同**
   ```
   文档 > 上传文档
   - 选择文件夹：合同文档
   - 上传文件：合同PDF
   - 添加标签：如"客户合同"、"供应商合同"
   ```

3. **关联业务记录**
   - 关联到销售订单（如客户合同）
   - 关联到采购订单（如供应商合同）

### 场景 2：文档审批流程

**需求**：审批重要文档

**步骤**：

1. **上传文档**
   - 上传需要审批的文档

2. **发起审批**
   - 选择审批人
   - 设置审批流程

3. **审批处理**
   - 审批人审核文档
   - 添加审批意见
   - 批准或拒绝

4. **审批完成**
   - 文档状态更新
   - 通知相关人员

### 场景 3：文档共享

**需求**：与客户共享文档

**步骤**：

1. **选择文档**
   - 选择要共享的文档

2. **创建共享链接**
   - 生成共享链接
   - 设置访问权限
   - 设置有效期

3. **发送链接**
   - 通过邮件发送链接
   - 客户点击链接访问文档

---

## 五、配置和设置

### 1. 文件夹配置

1. **文档 > 配置 > 文件夹**
2. 创建文件夹：
   - **名称**：文件夹名称
   - **父文件夹**：上级文件夹（如需要）
   - **权限**：设置读写权限

### 2. 标签配置

1. **文档 > 配置 > 标签**
2. 创建标签：
   - **名称**：标签名称
   - **颜色**：选择标签颜色
   - **文件夹**：关联文件夹（如需要）

### 3. 工作流配置

1. **文档 > 配置 > 工作流**
2. 配置工作流：
   - **文档类型**：应用工作流的文档类型
   - **审批流程**：定义审批步骤
   - **自动操作**：自动执行的操作

---

## 六、最佳实践

### 1. 文档组织

- **清晰结构**：建立清晰的文件夹结构
- **命名规范**：使用一致的文档命名规范
- **标签使用**：合理使用标签分类
- **定期整理**：定期整理和归档文档

### 2. 权限管理

- **最小权限原则**：授予最小必要权限
- **定期审查**：定期审查文档权限
- **访问审计**：跟踪文档访问记录

### 3. 安全保护

- **备份策略**：定期备份重要文档
- **版本控制**：保留文档版本历史
- **访问控制**：严格控制文档访问

---

## 七、高级功能

### 1. OCR（光学字符识别）

- **自动提取**：从图片中自动提取文字
- **全文搜索**：支持图片文档的全文搜索
- **批量处理**：批量OCR处理

### 2. 文档预览

- **在线预览**：在浏览器中预览文档
- **多格式支持**：支持多种格式预览
- **快速查看**：快速查看文档内容

### 3. 批量操作

- **批量上传**：批量上传文档
- **批量分类**：批量移动或分类文档
- **批量下载**：批量下载文档

---

## 八、总结

- **`documents` 模块**提供企业级文档管理功能。
- 核心功能：
  - 文档存储和管理
  - 文件夹和分类组织
  - 标签和搜索
  - 文档共享和协作
  - 版本控制和审批流程
  - 与业务模块的集成
- 支持多种文档类型和格式。
- 提供灵活的权限控制和安全性。
- 是企业文档管理的完整解决方案。

