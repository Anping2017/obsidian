---
title: HumanEval 基准
type: concept
tags: [ai, programming, mature]
sources: [raw/AI人工智能/]
created: 2026-05-05
updated: 2026-05-05
summary: HumanEval 是 OpenAI 提出的代码生成评估基准,164 道 Python 函数题用单元测试自动判分,通过 pass@k 指标衡量大模型的编程能力。
---

# HumanEval 基准

## 定义

HumanEval 是 [[OpenAI]] 在 Codex 论文(2021)中发布的代码生成评估基准,包含 164 道手写 Python 函数题,每题给出函数签名、文档字符串与测试用例,要求模型生成函数体并通过单元测试。

## 评估指标:pass@k

$$\text{pass@}k = \mathbb{E}\left[1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}\right]$$

其中 $n$ 是采样数,$c$ 是通过的样本数。pass@1 表示生成一次就通过的概率。

## 重要里程碑

- Codex(2021):pass@1 = 28.8%
- GPT-3.5 Turbo:48.1%
- GPT-4:67.0%(2023 春)
- Claude 3 Opus:84.9%
- Claude 3.5 Sonnet:92.0%(2024)
- DeepSeek-V3 / GPT-4o:90%+
- 接近天花板,新基准如 SWE-Bench 取代

## 局限与衍生

HumanEval 仅考察短函数级别,实际工程中不够代表性,因此衍生:
- **MBPP**:Mostly Basic Python Problems,974 题更贴近教学
- **HumanEval+**:更严格测试用例
- **MultiPL-E**:多语言扩展
- **SWE-Bench**:GitHub 真实 issue 级别(更难)
- **LiveCodeBench**:每月更新避免污染

## 与其他基准对比

- 与 [[MMLU基准]]:专精代码 vs 综合知识
- 与 SWE-Bench:函数级 vs 仓库级
- 与 [[Chatbot Arena]]:自动评估 vs 人类偏好

## 与其他概念的关系

- 是 [[AI模型评估基准]] 的代码核心
- 评估 [[AI编码助手]] 与 [[GPT系列模型]] / [[Claude系列模型]] 的关键指标
- 训练数据污染(模型见过 LeetCode 题解)是常见质疑
- [[模型量化]] / [[模型蒸馏]] 后此项常显著下降

## 实务用途

- LLM 厂商发布技术报告必给 HumanEval 分数
- 微调实验快速回归评估
- 不能仅凭 HumanEval 选模型,需结合 SWE-Bench 与实际工程

## 参考源

- raw/AI人工智能/04-综合提升层/
- Chen et al. "Evaluating Large Language Models Trained on Code" (Codex paper, 2021)
