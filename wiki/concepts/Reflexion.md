---
title: Reflexion
type: concept
tags: [ai, mature]
sources: [raw/提示词工程/04-进阶优化/高级技术]
created: 2026-05-05
updated: 2026-05-05
summary: Reflexion 由 Shinn 等 2023 提出,让 LLM Agent 在失败后生成自我反思的"教训",加入下一轮 prompt,通过"行动→评估→反思→重试"循环改善任务表现,无需更新模型权重。
---

# Reflexion

## 定义

**Reflexion** 由 **Noah Shinn** 等人在 **2023 年** 论文《Reflexion: Language Agents with Verbal Reinforcement Learning》中提出,核心思想:**让 LLM Agent 在每次任务尝试后,基于结果生成自然语言形式的"反思(reflection)"或"教训(lesson)",写入下一轮的 prompt,通过"行动→评估→反思→重试"循环不断改善表现**——本质上是一种**不更新模型权重的"语言强化学习(Verbal RL)"**。它是 [[ReAct提示]] 的进化版,让 Agent 具备类似人脑的"从失败中学习"能力。

## 核心要点

### 三组件架构

| 组件 | 角色 | 例子 |
|---|---|---|
| **Actor** | 执行任务的 Agent(通常 ReAct 模式) | 解题、写代码、查信息 |
| **Evaluator** | 评估输出好坏 | 单元测试、自评、外部反馈 |
| **Self-Reflection** | 生成下次改进的反思 | "我之前忘记考虑 X" |

每轮迭代:
1. Actor 尝试任务,产生 trajectory
2. Evaluator 给出成功 / 失败 + 信号
3. 失败时,Self-Reflection 生成自然语言教训
4. 教训加入 Actor 下轮 prompt 的 episodic memory
5. 重试

### 与 ReAct 的关系

- **ReAct**:单轮内推理 + 行动
- **Reflexion**:多轮间反思 + 重试,内含 ReAct
- 简化:Reflexion = ReAct + Episodic Memory + Reflection

### 反思的两种粒度

#### Trajectory-level(整体反思)

任务失败后,反思整个尝试:
> "上次我先搜索 A 后调用 B,但 A 的结果与 B 输入不匹配。下次应先调用 B 获取格式,再针对性搜索 A。"

#### Action-level(每步反思)

每步行动后,基于即时反馈反思:
> "Action 3 调用错了 API,返回 404。需检查参数格式。"

### 经典 Prompt 设计

```
[Memory: 过往经验教训]
反思 1: 我之前在解 X 类型题时,常忽略 Y 条件。
反思 2: 调用 search 时,关键词太宽泛会得到无关结果,应加限定。
...

[Current Task]
{task}

[Instructions]
基于过往反思,这次更小心。

(Actor 执行 ReAct...)

(Evaluator 评估)

[Self-Reflection]
这次失败的原因是什么?
我下次应该怎么做?
请输出新的 reflection 加入 memory。
```

### 实证表现

Shinn 等 2023 在多个基准上:
- **HotPotQA(多跳问答)**:从 28% → 40% (+12pp)
- **AlfWorld(具身 agent)**:从 75% → 97% (+22pp)
- **HumanEval(代码生成)**:Python 接近 SOTA
- **WebShop(网购)**:任务完成率明显提升

### 主要优势

- **无需训练**:不修改模型权重,纯 prompting
- **快速适应**:几轮就能学到新任务的经验
- **可解释**:反思是自然语言,人类可读
- **可迁移**:学到的反思可在相似任务复用
- **轻量级强化学习**:替代昂贵的 RLHF

### 主要挑战

- **评估器质量**:Evaluator 不准则反思无效
- **反思过拟合**:可能学到具体题的"应试技巧"而非通用规律
- **memory 膨胀**:反思越多越长,token 成本上升
- **错误反思的累积**:错误反思可能误导后续
- **不收敛**:某些任务反思后仍失败,陷入循环

### 反思的设计技巧

- **明确具体**:不要"做得更好",要"在 X 步骤先做 Y"
- **简洁**:每条反思 1-3 句
- **可执行**:能直接转化为下次行动
- **去重**:相似反思合并
- **优先**:高频出现的错误优先

### 主要变体

**Verifier-Reflexion**:用强外部 verifier(如代码 unit test)取代 LLM 自评

**Multi-Agent Reflexion**:多 agent 互相反思对方的输出

**Long-term Reflexion**:跨任务持久 memory,逐步积累知识库

**Reflexion + RLHF**:把高质量反思作为监督信号微调模型

### 与人类学习的类比

Reflexion 模拟了人类的元认知(metacognition):
- 失败后反思:"我哪里做错了?"
- 提取教训:"下次要注意 X"
- 应用教训:再次遇到时主动避免

这与 Kolb 学习循环(经验 → 反思 → 总结 → 应用)结构高度相似。

### 落地工具

- **LangGraph**:支持反思节点的 agent 框架
- **AutoGen**:多 agent 反思
- **LlamaIndex**:Reflexion + RAG
- **手工实现**:相对简单,核心是 prompt 设计 + 控制循环

### 工程注意

- **轮次上限**:防止无限循环(常 3-5 轮)
- **早停条件**:评估器通过则停止
- **memory 管理**:截断、去重、摘要
- **失败兜底**:多轮仍失败的 fallback 策略
- **成本监控**:多轮调用累积成本快

### 与其他方法对比

| 方法 | 改进机制 | 是否需训练 | 适用 |
|---|---|---|---|
| Few-shot | 示例 | 否 | 简单任务 |
| CoT | 引出推理 | 否 | 中等推理 |
| Self-Consistency | 多采样投票 | 否 | 离散答案 |
| ReAct | 工具调用 | 否 | 现实任务 |
| **Reflexion** | 失败反思 | 否 | 多轮迭代任务 |
| RLHF | 训练 | 是 | 全局对齐 |

## 和其他概念的关系

Reflexion 是 [[ReAct提示]] 的进化形式,引入 episodic memory 与自我反思。它属于 [[AI Agent]] 的高级范式,与 [[思维树]] 的"过程探索"互补——ToT 是横向多分支,Reflexion 是纵向多轮迭代。它与 [[自一致性]] 都用"多次尝试"思想,但 SC 是并行投票,Reflexion 是序贯学习。它与 [[提示词工程方法论]] 中"迭代优化"原则一致。在 [[大语言模型应用栈]] 中,它处于 Agent 编排层。它涉及 [[模型评估]] 中评估器质量与外部反馈机制设计。

## 参考源

- raw/提示词工程/04-进阶优化/高级技术
- raw/提示词工程/03-应用实践/高级技巧
