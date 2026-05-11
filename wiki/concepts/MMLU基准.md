---
title: MMLU 基准
type: concept
tags: [ai, mature]
sources: [raw/AI人工智能/]
created: 2026-05-05
updated: 2026-05-05
summary: MMLU 是覆盖 57 个学科的多任务语言理解基准,以 5-shot 方式测试模型在数学、历史、法律、医学等领域的综合知识,是大模型代际比较的事实标准。
---

# MMLU 基准

## 定义

MMLU(Massive Multitask Language Understanding)是 Hendrycks 等人于 2020 年提出的[[大语言模型]]综合评估基准,涵盖 STEM、人文、社会科学、其他四大类共 57 个学科,约 1.6 万道多选题,问题难度从初等到专业级。

## 评估方式

- **少样本(Few-shot)**:通常 5-shot
- **零样本(Zero-shot)**:模型直接答题
- **CoT 模式(MMLU-Pro)**:允许[[思维链]]推理

测量指标为准确率(Accuracy)。

## 关键里程碑

- GPT-3:43.9%(刚高于随机)
- GPT-4:86.4%(2023,首破 80%)
- Claude 3 Opus:86.8%(2024)
- GPT-4o:88.7%
- Llama 3.1 405B:88.6%
- Claude 3.5 Sonnet:88.3%
- 人类专家估计上限:89.8%

## 子集与衍生

- **MMLU-Pro**:更高难度,引入 10 选 1 与推理需求
- **MMLU-Redux**:修正原题质量问题
- **C-Eval / CMMLU**:中文版本
- **MMMLU**:多语言扩展

## 与其他基准对比

- 与 [[HellaSwag]]:常识推理
- 与 [[ARC]]:推理与多跳
- 与 [[GSM8K]] / MATH:数学专精
- 与 [[HumanEval基准|HumanEval]]:代码专精
- 与 [[MT-Bench]]:开放对话评分

## 局限

- 多选题可被运气、消除法穿越
- 接近天花板,区分度下降
- 训练数据污染(Test Contamination)风险高
- 不测多轮对话与代理能力

## 与其他概念的关系

- 属于 [[AI模型评估基准]] 的核心成员
- 训练时常被指控"为 MMLU 优化"造成 [[Goodhart定律]] 失效
- 与 [[GPT系列模型]]、[[Claude系列模型]]、[[Llama系列模型]] 比较时必引用
- 与 [[HumanEval基准|HumanEval]]、[[Chatbot Arena]] 形成评估三件套

## 参考源

- raw/AI人工智能/04-综合提升层/
- Hendrycks et al. "Measuring Massive Multitask Language Understanding" (2020)
- HuggingFace Open LLM Leaderboard
