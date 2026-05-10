---
title: AI 内容审核
type: concept
tags: [ai, mature]
sources: [raw/AI人工智能/]
created: 2026-05-05
updated: 2026-05-05
summary: AI 内容审核是用机器学习对 LLM 输出与用户输入进行分类与过滤的系统,平衡有用、无害、合规三方,是 AI 产品上线必备护栏。
---

# AI 内容审核

## 定义

AI 内容审核(Content Moderation for AI)是对[[大语言模型]]系统中用户输入与模型输出进行分类、检测、过滤的机制,目的是阻止违法、有害、违反平台政策的内容产生与传播。在 LLM 时代,审核既要防止用户输入恶意提示([[越狱攻击]]),也要兜底模型本身的训练对齐失败。

## 关键审核类别

- 暴力、自残
- 性内容(尤其涉及未成年人)
- 仇恨言论
- 非法活动指导(武器、毒品、网络攻击)
- 个人隐私(PII)与诽谤
- 误导信息(虚假医疗、金融建议)
- 合规分级(政治、宗教、地区敏感)

## 审核架构

### 前置过滤(Input Filter)

- 关键词与正则
- 分类器(轻量模型)
- 提示注入检测
- 速率限制

### 模型层对齐

- [[RLHF]] / [[DPO直接偏好优化]] / [[Constitutional AI]] 训练拒答能力
- 系统提示中嵌入安全规则

### 后置过滤(Output Filter)

- 分类器扫描生成内容
- 敏感词替换
- 二次模型审查(如 OpenAI Moderation API、Llama Guard)

### 多模态审核

图像、音频、视频内容审核(NSFW 检测、儿童保护、Deepfake)。

## 关键技术

- **分类器**:微调小模型快速过滤(如 Llama Guard 2/3)
- **指令检测**:识别越狱模板、提示注入
- **多语言**:防中转翻译绕过
- **链上审核**:对长对话维护风险状态

## 行业方案

- OpenAI Moderation API(免费)
- Anthropic Claude 内置安全
- Google Perspective API
- Llama Guard(Meta 开源)
- AWS Bedrock Guardrails
- Azure AI Content Safety

## 与其他概念的关系

- 与 [[AI红队评估]] 互补:红队找漏洞,审核堵漏洞
- 与 [[超级对齐]] 是同一目标的不同路径
- 与 [[越狱攻击]] 是矛盾对立面
- [[Constitutional AI]] 是模型层审核
- [[AI治理]] 政策推动审核标准化
- 与 [[内容审核]] 平台(社交媒体)技术互通

## 难点

- **过严**:误杀合法用例,产品不可用
- **过松**:漏过有害内容,平台担责
- **多语言**:小语种审核质量差
- **新型攻击**:角色扮演、Base64、隐喻不断翻新
- **政治标签**:何为"误导"在不同地区定义不同

## 监管前沿

- 欧盟 AI Act 高风险场景必审
- 美国 Executive Order on AI 要求红队报告
- 中国《生成式 AI 服务管理办法》强制内容审核

## 参考源

- raw/AI人工智能/04-综合提升层/AI安全与对齐/
- OpenAI Moderation 文档
- Llama Guard 论文(Meta 2023)
