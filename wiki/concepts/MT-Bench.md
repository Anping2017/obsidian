---
title: MT-Bench 多轮对话评测基准
type: concept
tags: [ai, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: MT-Bench 是 LMSYS 团队提出的多轮对话评测基准,通过 80 道两轮问题 + GPT-4 裁判,衡量 LLM 在真实对话场景下的指令遵循和推理质量。
---

# MT-Bench 多轮对话评测基准

## 定义

**MT-Bench(Multi-Turn Benchmark)** 是 UC Berkeley LMSYS 团队 2023 年提出的开放式 [[大语言模型]] 评测基准,专门衡量模型在**多轮对话**中的指令遵循、推理与生成能力。它由 80 道精心设计的高质量问题组成,每道题包含两轮对话(第二轮基于第一轮上下文延伸提问),并用 GPT-4 等强模型作为"裁判(LLM-as-a-Judge)"自动打分。

MT-Bench 与 [[Chatbot Arena]] 同属 LMSYS 评测生态,前者是结构化离线测试,后者是大规模人类盲测,二者互补构成主流的"对话能力"评测体系。

## 核心要点

### 题目设计

80 道题覆盖 8 个能力类别,每类 10 题:写作、角色扮演、推理、数学、编程、信息抽取、STEM 知识、人文社科。每题都包含两轮:第一轮问题独立可答,第二轮问题"承接式"考察模型对历史上下文的理解与延展。

### LLM-as-a-Judge

MT-Bench 用 GPT-4(后续也用 Claude 3.5、GPT-4o)作为裁判,对待评模型输出从 1—10 打分。两种主要模式:

- **Single-answer grading**:单独给一个回答打分。
- **Pairwise comparison**:两个模型并排比较,判定胜/负/平。

裁判模型与人类标注的相关系数可达 0.8 以上,但仍存在**位置偏好(Position Bias)、冗长偏好(Verbosity Bias)、自我偏好(Self-enhancement Bias)** 等系统性误差。

### 计分规则

最终得分是 80 题平均分,通常报告 0—10 分制。Llama-2-70B-Chat 约 6.86 分,GPT-4(2023)约 8.99 分,Claude-2 约 8.06 分。分数差 0.5 一般已具有实战可感知意义。

### 在评测体系中的位置

MT-Bench 主要补足了静态选择题基准([[MMLU基准]]、[[HumanEval基准]])对**生成质量**和**对话流畅性**的评测盲区,是研发期内部"看模型行不行"的常用快速指标。

## 典型应用 / 主要工具

- **模型发布报告**:Vicuna、Llama-2、Mistral、Qwen 等开源模型发布时,几乎必报 MT-Bench 分数。
- **微调验证**:RLHF/DPO 训练后,跑 MT-Bench 验证对话能力是否退化(称为"对齐税")。
- **官方实现**:LMSYS 在 GitHub 上的 `FastChat` 仓库提供完整评测脚本与裁判 prompt。
- **拓展变体**:MT-Bench-101(中文化)、MT-Bench-Plus(更多领域)等社区改造版本。

## 局限与陷阱

- **样本量小**:80 题难以覆盖所有能力维度,长尾场景缺失。
- **裁判偏好**:GPT-4 倾向于给"长、礼貌、结构化"的回答更高分,鼓励冗长。
- **训练污染**:测试集公开,部分新模型可能在训练数据中见过题目。
- **多轮深度有限**:仅两轮,真实场景常需 5+ 轮。
- **难以扩展**:更换语言、专业领域时,需重写题库与裁判 prompt。
- **分数饱和**:前沿模型差距小时,难以分辨高低,需要 [[Chatbot Arena]] 等大样本人评补充。

## 与其他概念的关系

- 评测家族:与 [[MMLU基准]]、[[HumanEval基准]]、[[AI模型评估基准]] 共同构成 LLM 主流评测矩阵。
- 互补关系:[[Chatbot Arena]] 提供大规模人类盲测,MT-Bench 提供快速可复现离线测试。
- 评估对象:核心评测主体是 [[大语言模型]] 的对话能力。
- 工程实践:与 [[模型评估]]、[[提示词评估]]、[[AI红队评估]] 共同支撑模型发布前的质量门禁。
- 局限缓解:与 [[多智能体提示]]、[[行业Prompt模式集]] 等定制化测试共用以减少单一基准偏差。

## 参考源

- LMSYS Blog: Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (2023)
- Zheng et al. (2023). MT-Bench: A Multi-Turn Benchmark for Evaluating LLMs. NeurIPS Datasets & Benchmarks Track.
