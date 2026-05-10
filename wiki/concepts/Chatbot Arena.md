---
title: Chatbot Arena
type: concept
tags: [ai, mature]
sources: [raw/AI人工智能/]
created: 2026-05-05
updated: 2026-05-05
summary: Chatbot Arena 通过用户盲测投票与 Elo 评级机制对大模型排名,是衡量真实主观偏好的"金标准",与静态基准互补。
---

# Chatbot Arena

## 定义

Chatbot Arena(LMSYS Org)是加州大学伯克利分校 LMSYS 团队于 2023 年推出的[[大语言模型]]评估平台。用户在网页上输入提示,系统盲选两个模型并行回答,用户选择更好的一个或平手。基于百万级人工投票,系统使用 Elo 等级机制(借鉴国际象棋)给出实时排行榜。

## 与静态基准的差异

| 维度 | MMLU/HumanEval | Chatbot Arena |
|---|---|---|
| 测试题 | 固定 | 用户实时输入 |
| 评分 | 自动 | 人工偏好 |
| 污染 | 易污染 | 难以污染 |
| 任务覆盖 | 受限 | 真实多样 |
| 主观倾向 | 客观 | 主观偏好 |

Chatbot Arena 因此被认为更接近"真实使用价值"。

## Elo 等级

每次对决后,获胜模型的 Elo 上调,失败下调,平局轻微调整。Elo 差距 100 ≈ 64% 胜率,差距 200 ≈ 76% 胜率。

## 衍生分类

- **Hard Prompts**:筛选难题排名
- **Coding**:代码相关提示
- **Style Control**:控制回答长度等风格因素后的排名
- **多语言子排行**

## 关键发现

- 风格(回答长度、emoji、Markdown 格式)显著影响投票
- "Style Control" 后的排行可能与"原始"排行差距很大
- Claude、GPT、Gemini 多次轮替榜首
- 开源模型(Llama 3.1 405B、DeepSeek V3、Qwen)逼近闭源

## 与其他概念的关系

- 与 [[MMLU基准]]、[[HumanEval基准]] 互补构成 LLM 三大评估维度
- 与 [[MT-Bench]] 类似但更大规模
- 与 [[AI红队评估]] 形成"日常评估 vs 安全评估"两条线
- 是 [[GPT系列模型]] / [[Claude系列模型]] / [[Llama系列模型]] 营销关键

## 局限

- 用户偏好可能受训练数据污染
- 短问题占比高,长上下文/代理能力测不出
- 对"安全拒答"惩罚(用户选信息更全的)
- 中文用户少,中文排名置信度低

## 参考源

- raw/AI人工智能/04-综合提升层/
- Chiang et al. "Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference" (2024)
- chat.lmsys.org
