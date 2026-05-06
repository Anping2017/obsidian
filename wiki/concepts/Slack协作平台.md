---
title: Slack 协作平台
type: concept
tags: [tools, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Slack 是 2013 年从游戏公司 Tiny Speck 副产物诞生的团队即时通讯平台,以频道(Channel)替代邮件、深度集成第三方应用、API 友好,成为科技公司协作标配,2021 年被 Salesforce 以 277 亿美元收购。
---

# Slack 协作平台

## 定义

Slack 是 2013 年由 Stewart Butterfield 等人(原 Flickr 创始人)从失败游戏 Glitch 的内部沟通工具孵化而来的团队协作平台。它把企业沟通从"分散邮件"转向"频道(Channel)聚合",把传统 IM(MSN、Skype)升级为"工作场所操作系统",彻底改变了科技公司的工作方式。

2021 年 Salesforce 以 277 亿美元收购,成为 Salesforce Customer 360 的关键沟通层。它不只是聊天工具,而是企业 Workflow、SaaS 集成、Bot 自动化的中枢。

## 核心模型:Channel

**Channel(频道)**

- 公开频道(#general、#engineering、#design):团队任何人可加
- 私密频道:邀请制
- 单聊 / 群聊
- 共享频道(Shared Channel):跨企业协作

**频道命名约定**

- #proj-xxxx:项目频道
- #team-xxx:团队主页
- #help-xxx:支持频道
- #fun-xxx:闲聊
- 命名规范让大型组织(数千人)有可导航性

## 核心功能

**1. 消息**

- Markdown 格式
- 代码块、引用
- 表情反应(Reactions)替代回复
- 编辑、撤回(短时间)
- 提及 @user / @channel / @here

**2. 线程(Thread)**

- 在某条消息下回复,不污染主频道
- "把讨论搬进线程"是 Slack 礼仪

**3. 文件分享**

- 拖拽上传
- 与 Google Drive、Dropbox、OneDrive 集成
- 文档预览

**4. 搜索**

- 全文搜索(消息、文件)
- 高级筛选:from、in、has、before、after

**5. 通知与免打扰**

- 频道级通知设定
- 关键字提醒
- Do Not Disturb 时段
- 状态(Active / Away)与自定义 Status

**6. Huddle(语音通话,2021+)**

- 频道内即开即聊语音
- 替代会议室约会的轻量沟通

**7. Canvas(2023+)**

- 在频道中持久化文档
- 协作编辑、富文本

**8. 集成与自动化**

Slack 最大优势——3000+ App 集成:
- 开发:GitHub、GitLab、Jira、Linear、PagerDuty
- 设计:Figma、Sketch、Zeplin
- 监控:Datadog、Grafana、Sentry、StatusPage
- 团队:Zoom、Google Workspace、Notion
- AI:ChatGPT、Claude、Slack AI

## 自动化:Workflow Builder

无代码工作流编辑器:
- 触发器(关键字、定时、表单提交)
- 动作(发消息、创建任务、调用 API)
- 替代部分轻量化 Zapier 用例

## API 与开发

Slack 是开发者最友好的协作平台:
- Web API:发消息、查询用户
- Events API:监听频道事件
- Webhooks
- Slash Commands(/deploy、/standup)
- Modals:Slack 内弹窗交互
- Block Kit:富文本消息构建

工程团队普遍构建内部 Slack Bot 替代命令行工具(部署、查询、值班轮换)。

## 与同类工具对比

| 维度 | Slack | Microsoft Teams | Discord | 飞书 | 企业微信 |
|---|---|---|---|---|---|
| 主要用户 | 科技公司 | 微软生态企业 | 游戏 / 社区 | 中国大企业 | 中国传统企业 |
| 频道模式 | 强 | 强 | 极强 | 强 | 中 |
| 集成生态 | 极强 | 强(微软栈) | 弱(游戏向) | 中 | 中 |
| 视频会议 | Huddle 轻量 | 主打 | 弱 | 强(自家会议) | 中 |
| 企业部署 | 云 | 云/本地 | 云 | 云 | 云 |
| 价格 | 免费/付费 | 含在 365 | 免费 | 免费/付费 | 免费/付费 |

**MS Teams 反超**

2020 年后 MS Teams 凭借捆绑 Office 365,用户数超 Slack。Slack 在科技公司仍领先,但企业市场被微软抢占。

## 商业模式

**免费**:90 天历史消息、10 集成、1:1 视频
**Pro($7.25/月/用户)**:无限历史、无限集成、群语音/视频
**Business+($12.50/月/用户)**:SAML SSO、SLA
**Enterprise Grid**:大组织、合规、HIPAA

中国大陆访问受限,主流替代是飞书/钉钉。

## 文化影响

Slack 改变了科技公司的工作节奏:
- "邮件已死":许多公司用邮件量减半
- 异步透明:#公开频道 让信息在公司内自由流动
- "频道焦虑":新人难以判断哪些频道重要
- 通知疲劳:多频道通知成为新型干扰
- "Slack 即工作"批评:把闲聊视为工作

## 局限

- 大量频道时信息过载
- 历史搜索在大企业版差(免费版只 90 天)
- 视频会议不及 Zoom / Meet
- 离线能力弱
- 价格按用户线性增长,大企业贵

## Salesforce 收购后的方向

- Slack 与 Salesforce CRM 深度集成
- Sales Hub、Service Hub Slack 化
- AI 助手(Slack AI、Einstein)
- 客户协作场景(Slack Connect)

## 参考源

- raw/计算机/
- 相关:[[Notion文档协作]]、[[现代云原生架构]]
