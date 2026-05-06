---
title: Notion 文档协作
type: concept
tags: [tools, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Notion 是 2016 年发布的多功能文档与协作平台,把文档、数据库、看板、Wiki 整合在统一的 Block 模型中,成为知识工作者和团队的"all-in-one"工具,2024 年估值 100 亿美元。
---

# Notion 文档协作

## 定义

Notion 是 Ivan Zhao 等人 2013 年创立、2016 年正式发布的文档与协作平台。它的核心创新是把传统三类工具——文档(Word/Google Docs)、笔记(Evernote)、数据库(Excel)、协作(Confluence)——抽象到一个统一的 **Block(块)模型**:每个段落、表格、列表、嵌入都是可拖拽、嵌套、转换的 Block。

它定位为"all-in-one workspace",成为初创公司 Wiki、个人知识库(PKM)、产品文档、项目管理的常见选择。2024 年估值 100 亿美元,日活用户超 4000 万。

## 核心设计:Block 模型

**所有内容皆 Block**

- 文本段落、标题、列表、引用、代码、图片、视频、嵌入、表格、数据库、链接预览,都是 Block
- 一个 Block 可拖拽到任意位置
- Block 可嵌入其他 Block(树状结构)
- "/"快捷键插入任何 Block 类型

**Block 的可转换性**

任意 Block 可一键转换为其他类型:文字段 → 标题 → 列表 → 待办 → 引用。

**Block 的引用与同步**

同一 Block 可被多处"引用"(@提及),修改一处所有处自动同步——这是知识库的核心能力。

## 数据库(Database)

Notion 的"杀手锏"功能,把表格升级为可视化数据库:

**视图**

同一份数据多种视图:
- Table(表格)
- Board(看板,Kanban)
- Calendar(日历)
- List(列表)
- Gallery(画廊)
- Timeline(甘特图)
- Chart(图表,2024 新增)

**字段类型**

- 文本、数字、单选、多选、日期、人员、文件、复选框、URL、电话、邮箱
- Relation(关联其他数据库)
- Rollup(从关联数据库聚合)
- Formula(公式,类似 Excel)
- Created/Modified time/by(自动)
- Status(带分组)

**过滤与排序**

- 多条件过滤
- 多列排序
- 分组(Group By)

**Linked Database**

把同一数据库以不同视图嵌入多处页面,改一处全部更新。

## 主要应用场景

**1. 公司 Wiki**

- 政策、流程、产品文档
- 部门主页 + 跳转到子页
- 入职手册
- 与 Confluence 竞争

**2. 项目管理**

- 任务数据库
- 甘特图视图
- 与 Asana、Trello、Jira 竞争

**3. 产品文档**

- PRD、功能文档、API 文档
- 与 GitHub Wiki、ReadMe 竞争

**4. 个人 PKM**

- 笔记、文章、灵感、阅读记录
- 与 Evernote、Obsidian、Roam Research 竞争

**5. CRM / OKR / 团队主页**

- 数据库定制 CRM
- OKR 模板
- 行业模板社区共享

## AI 集成(Notion AI)

2023 年起 Notion AI 集成 GPT-4 系:
- 写作助手(草稿、扩展、翻译、总结)
- 自动填表(Q&A 数据库自动答)
- 跨页搜索(Q&A,Notion AI Connect)
- 自定义工作流(2024)

定价:$10/月/用户,需主订阅外加。

## 与同类工具对比

| 维度 | Notion | Confluence | Coda | Airtable | Obsidian |
|---|---|---|---|---|---|
| 数据库 | 强 | 弱 | 极强 | 极强 | 弱(社区) |
| 文档 | 强 | 强 | 中 | 弱 | 极强 |
| 离线 | 弱 | 弱 | 弱 | 中 | 强 |
| 自部署 | 否 | 是 | 否 | 否 | 文件存本地 |
| API | 中 | 强 | 中 | 强 | 弱 |
| 性能 | 大库慢 | 中 | 中 | 强 | 极强 |

## 局限

- **性能问题**:大库(数千页面)加载慢,搜索不够智能
- **离线能力差**:核心依赖云端
- **数据导出弱**:导 Markdown 格式部分丢失
- **协作冲突**:并发编辑无 Google Docs 实时
- **API 受限**:数据库 schema 修改通过 API 困难
- **不适合 markdown 重度用户**:Block 模型与纯文本 Markdown 哲学不同

## 自部署替代

Notion 不开源,自部署不可。替代:
- **AppFlowy**:Rust 写的开源 Notion 替代
- **Anytype**:本地优先开源
- **Outline**:Wiki 专精
- **Coda**:商业,数据库更强

## 商业模式

**免费**:个人,部分块限制
**Plus($10/用户/月)**:小团队
**Business($15/用户/月)**:加 AI、SAML
**Enterprise**:合规、审计、安全
**Notion AI($10/月加购)**

2023 年 Notion 从工具向"操作系统"转型,推出日历、邮件(Notion Mail,2024)集成,挑战 Google Workspace、Microsoft 365。

## 文化与社区

Notion 社区文化浓厚:
- 模板社区:成千上万模板免费下载
- KOL 经济:Notion Influencer 卖模板
- 中文圈:Notion Pal、玉树芝兰、剑飞、flomo 等推动

## 参考源

- raw/计算机/
- 相关:[[Obsidian双向链接]]、[[PKM方法论]]
