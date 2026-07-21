---
title: ChatGPT Search
type: concept
tags: [ai, seo, stub]
sources: []
created: 2026-05-11
updated: 2026-05-11
summary: ChatGPT Search 是 OpenAI 在 2024 年推出的 LLM 原生搜索能力,把大模型对话与实时网页检索、引用来源合并,是 AI 搜索的主流产品之一。
---

# ChatGPT Search

## 定义

**ChatGPT Search** 是 OpenAI 在 ChatGPT 内置的实时联网搜索能力,先由 SearchGPT 内测,2024 年 10 月合并到 ChatGPT 主产品。用户提问时,后台会检索最新网页信息 → 综合生成答案 → 附来源链接。这与传统 Google 蓝色链接式搜索完全不同,是**对话式 AI 搜索**的代表。

## 核心要点

- **触发方式**:自动判断(问题涉及时效/事实)或用户点击"搜索"按钮
- **来源引用**:每条答案末尾列出参考网页(蓝色引用块)
- **合作出版商**:与 Reuters、AP、金融时报、Le Monde 等达成内容授权
- **对 SEO 的影响**:传统排名机制被"AI 引用度"替代 —— 网页需通过 [[Schema markup]] / [[E-E-A-T]] / 权威度获得引用
- **反爬取控制**:OAI-SearchBot User-Agent 抓取,可在 [[Robots.txt]] 中限制
- **典型场景**:天气、股价、新闻、赛事、比价、多源信息综合

## 和其他概念的关系

- 与 [[AI Overviews]](Google)、[[Perplexity]] 是"AI 搜索"三大产品
- 底层依赖 [[GPT系列模型]] 的推理能力 + 联网工具调用
- 冲击传统 [[搜索引擎优化]] 的可视性逻辑
- 属于 [[生成式AI]] 应用层,搭配 [[RAG]] 思路

## 参考源

- 综合公开报道与 OpenAI 官方文档
