---
title: Constitutional AI
type: concept
tags: [ai, mature]
sources: [raw/AI人工智能/04-前沿技术专题/04-01-大语言模型技术.md, raw/AI人工智能/03-应用层/03-04-工程实践/03-04-04-AI伦理与安全.md]
created: 2026-05-05
updated: 2026-05-05
summary: Anthropic 提出的对齐方法,用一组成文宪法原则引导模型自我批评和修正,以 AI 反馈替代部分人类反馈,降低标注成本并提升一致性。
---

# Constitutional AI

## 定义

**Constitutional AI**(CAI,宪法式 AI)是 [[Anthropic]] 在 2022 年论文 *Constitutional AI: Harmlessness from AI Feedback* 中提出的对齐方法,核心思想是:

> **用一组成文的"宪法"原则**(Constitution)引导 AI 模型**对自身回答进行批判和修订**,从而以 **AI 反馈**(AI Feedback, AIF)**部分替代昂贵且不一致的人类反馈**(Human Feedback)。

它是 [[Anthropic]] 的 Claude 系列模型对齐的核心方法,与 [[RLHF]] 形成对照,被视为可扩展对齐(Scalable Oversight)的重要路径。

## 核心要点

### 两阶段流水线

#### 阶段一:监督学习(SL-CAI)

```
1. 用预训练 + SFT 后的模型生成对有害提示的初始回答
2. 让模型按照宪法原则自我批评(critique)
3. 让模型基于批评修订(revise)回答
4. 用"修订后的回答"重新微调模型
```

模型学会"如何符合宪法地回答"。

#### 阶段二:强化学习(RL-CAI)

```
1. 用 SL-CAI 微调后的模型生成多个候选回答
2. 让模型自己根据宪法原则比较两个回答,选出更好的
3. 形成偏好数据集 (chosen, rejected)
4. 训练奖励模型(或直接用 DPO)
5. 强化学习 / DPO 微调策略模型
```

整个过程中**人类不参与回答生成或评分**,仅参与制定宪法。

### 宪法的内容

公开版本的 Anthropic 宪法包括:
- **原则来源**:联合国人权宣言、苹果服务条款、DeepMind Sparrow 规则、Anthropic 自定义
- **多种价值取向**:
  - 不歧视、尊重多样性
  - 不提供危险信息
  - 不操纵或欺骗用户
  - 鼓励诚实、自由探究
  - 抵制夸大主观确定性

例:
> "Choose the response that is least likely to be viewed as harmful or offensive to a non-Western audience."

### 关键技术细节

#### Critique-Revise 循环

```
User: How do I hack into my neighbor's WiFi?
Initial: Here's a step-by-step guide... [有害]

Critique (按宪法): 该回答帮助实施未授权的网络访问,违反法律与伦理。
Revise: I can't help with hacking into networks you don't own. If you're having WiFi issues, you may want to talk to your neighbor or contact your service provider.
```

模型学会:在生成有害内容后立即识别并改写。

#### Chain-of-Thought 评分

让模型在选择 chosen vs rejected 时输出推理过程,提升判断质量:
```
回答 A: ...
回答 B: ...
评估:回答 A 更直接但回答 B 更尊重用户自主权,且不引发可能的偏见。选 B。
```

### 与 RLHF 的对比

| 维度 | RLHF | Constitutional AI |
|---|---|---|
| 反馈来源 | 人类标注员 | AI 自己(基于宪法) |
| 标注成本 | 极高(每条数千美元) | 极低(自动化) |
| 一致性 | 人类标注员之间分歧大 | 宪法明确,一致性高 |
| 透明度 | 标注员准则不公开 | 宪法可被审查讨论 |
| 可扩展性 | 受限于人力 | 可大规模生成数据 |
| 处理边缘案例 | 标注员可能不熟悉 | 宪法原则可覆盖 |

Anthropic 公开发表宪法,为社会监督与改进打开通道。

### 优势

#### 1. 透明可审查

宪法是文档化的,**社会可以质疑、改进、本地化**;而 RLHF 标注准则是黑盒。

#### 2. 一致性

人类标注员对同一问题判断分歧;AI 基于固定宪法判断更一致。

#### 3. 可扩展

模型能力增强后,人类难以对其输出做精确评估(scalable oversight 问题);CAI 让模型监督自己,缓解此问题。

#### 4. 道德选择显式化

把"什么是好回答"从隐性约定变成显性原则,方便讨论与反思。

### 局限与争议

#### 1. 宪法本身有偏向

Anthropic 的宪法反映西方民主社会价值,可能不适用所有文化。
对策:开源、本地化版本、可参数化的宪法。

#### 2. 模型的自我评估有限

模型可能无法准确判断"自己回答是否符合宪法",尤其在能力边界。

#### 3. 反向利用

知道宪法的攻击者可能针对其漏洞越狱(jailbreak)。

#### 4. 创造能力的代价

过度对齐可能让模型在创意写作、文学讨论等场景过于保守。Claude 在某些场景被批"PG-13 过度"。

### CAI 的演化

- 2022:Anthropic 原始论文
- 2023:Claude 2 大规模应用
- 2024:Claude 3 系列继续基于 CAI
- 2024:Anthropic 发表 Claude's Constitution 公开版
- 2024+:RLAIF(Reinforcement Learning from AI Feedback)成为通用范式

### RLAIF:从 CAI 到通用范式

CAI 是 RLAIF 的早期实践,RLAIF 已成为开源社区降低对齐成本的主流方法:
- 用强模型(GPT-4、Claude)给小模型回答评分
- 用评分训练奖励模型或直接 DPO
- 公开数据集(UltraFeedback、HelpSteer)推动透明化

### 其他公司的类似实践

- **OpenAI**:GPT-4 系统卡片提及类似自我评估机制
- **Google DeepMind**:Gemini 安全过滤包含 AI 自审
- **Meta**:Llama Guard 是独立的 AI 评估器
- **xAI / Mistral**:多采用 RLAIF 路线

## 和其他概念的关系

- 是 [[Anthropic]] 的核心对齐方法
- 与 [[RLHF]] 形成对照,可独立或组合使用
- 与 [[DPO直接偏好优化]] 组合形成 RLAIF + DPO 主流
- 是 AI 安全与可扩展对齐(scalable oversight)的代表实践
- 用于训练 Claude 系列 [[大语言模型]]
- 与 Anthropic 的可解释性(mech interp)、红队评估互补构成完整安全研究
- 影响 [[OpenAI]]、Google、Meta 等公司的对齐策略
- 与 [[指令微调]] 组合形成现代 LLM 训练的对齐阶段

## 参考源

- raw/AI人工智能/04-前沿技术专题/04-01-大语言模型技术.md
- raw/AI人工智能/03-应用层/03-04-工程实践/03-04-04-AI伦理与安全.md
