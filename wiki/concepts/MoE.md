---
title: MoE 混合专家模型
type: concept
tags: [ai, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: MoE(Mixture of Experts)是用门控网络在多个专家子网络间稀疏路由的架构,1991 年提出,Google Switch/GShard 与 Mistral Mixtral、DeepSeek-V3 后成为大模型主流路线,以稀疏激活换取参数规模与算力解耦。
---

# MoE 混合专家模型

## 定义

**MoE(Mixture of Experts,混合专家)** 是一种**稀疏神经网络**架构:把模型分解成多个并列的"专家(expert)"子网络,前置一个**门控网络(Gating / Router)** 决定每个输入 token 路由到哪几个专家激活。Robert Jacobs、Geoffrey Hinton 等人 1991 年提出原型;2017 年 Shazeer 等的 Sparsely-Gated MoE 在 NLP 中将其工程化;2021 年 Google Switch Transformer / GShard 把 MoE 推上千亿/万亿参数尺度;2023 年 Mistral Mixtral 8x7B、2024 年 DeepSeek-V2/V3 使开源 MoE 成为大模型主流。

## 核心要点

### 1. 基本结构

```
input → Router(softmax over N experts)
              ↓ top-k(通常 k=1 or 2)
       [Expert_1] [Expert_2] ... [Expert_N]
              ↓ 加权聚合
            output
```

每个专家通常是一个 [[Transformer架构|Transformer]] FFN 模块。Top-k=2 表示每个 token 同时激活 2 个专家,其它专家**不参与计算**,这就是"稀疏激活"。

### 2. 关键收益

- **算力 / 参数解耦**:模型总参数(capacity)可大,但每次前向只激活一小部分(activated parameters),推理算力近似一个小模型
- **专家分工**:不同专家在训练中倾向于处理不同类型 token / 任务
- **扩展性**:增加专家数量是低成本扩参手段
- **多任务友好**:不同任务可路由到不同专家

### 3. 工程难点

- **负载均衡(Load Balance)**:某些专家被冷落 / 某些过载,引入辅助损失(auxiliary loss)、token 丢弃 / 容量上限
- **All-to-All 通信**:专家分布在不同 GPU 时跨节点通信成本极高,需 ZeRO、专家并行、TP/PP/EP 混合策略
- **训练不稳定**:门控梯度尖锐,Expert Choice Routing、Switch、SoftMoE 等多种 router 方案应对
- **存储成本**:总参数大,显存 / 磁盘要求高
- **微调难度**:LoRA 等高效微调对 MoE 适配更复杂

### 4. 代表模型

| 模型 | 总参数 | 激活参数 | 专家数 / Top-k |
|---|---|---|---|
| Switch Transformer(2021) | 1.6T | ~7B | 2048 / 1 |
| GShard | 600B | ~50B | 2048 / 2 |
| Mixtral 8x7B(2023) | 47B | ~13B | 8 / 2 |
| Mixtral 8x22B | 141B | ~39B | 8 / 2 |
| DeepSeek-V2 | 236B | 21B | 160 + 2 共享 / 6 |
| DeepSeek-V3 | 671B | 37B | 256 / 8 |
| Qwen-MoE | 14B | 2.7B | 60 + 4 共享 / 4 |
| GPT-4(传闻) | ~1.8T | ~280B | 8 / 2(未官方证实) |

### 5. 路由策略

- **Top-k Routing**(Switch/Mixtral):token 选 expert
- **Expert Choice Routing**(Google):expert 选 token,自动均衡
- **Hash Routing**:固定哈希,减少抖动
- **Soft MoE**(Puigcerver 2023):软加权所有 expert,稳定但不再稀疏
- **Shared Expert + Routed Expert**(DeepSeek):部分专家恒激活承担通用知识

## 典型应用

- **预训练 LLM**:Switch Transformer、GLaM、Mixtral、DeepSeek-V3、Qwen-MoE
- **机器翻译**:Google GShard 多语言翻译
- **多模态**:LIMoE、MoE 用于专家分工不同模态
- **推荐系统**:阿里 SAR-Net、PLE 等任务分塔与 MoE 结合
- **MoE-LoRA**:LoRA 适配器以 MoE 形式选择,提升多任务效率

## 局限与争议

- **训练资源门槛**:小团队复现困难,需大集群 + EP 并行经验
- **推理路由开销**:小批量场景路由计算反而成为瓶颈
- **专家"塌缩"**:训练失衡导致有效专家数远低于设计
- **效果增益边际**:在小尺度下 MoE 不一定胜过 dense,需要规模配合
- **可解释性**:专家学到了什么仍是黑盒,论文常做"专家专业化"探针分析
- **部署复杂度**:服务器需常驻全部专家权重,但只激活一部分,GPU 利用率挑战

## 与其他概念的关系

- 上位概念:[[神经网络]]、[[Transformer架构|Transformer]]、[[大语言模型]]
- 训练范式:[[预训练]]、[[Scaling Law]]、[[稀疏激活]]
- 工程基础:[[GPU并行]]、[[Tensor Parallelism]]、[[ZeRO]]
- 同族架构:[[Switch Transformer]]、[[Mixtral]]、[[DeepSeek-V3]]
- 对比方案:[[稠密模型]]、[[Dense LLM]]
- 衍生方向:[[MoE-LoRA]]、[[Soft MoE]]、[[Shared Expert]]
- 历史脉络:[[Geoffrey Hinton]] 1991 原始 MoE
- 相关算法:[[蒸馏]]、[[Mixture of Depths]]

## 参考源

- Jacobs, Jordan, Nowlan, Hinton *Adaptive Mixtures of Local Experts*(1991)
- Shazeer et al. *Outrageously Large Neural Networks*(2017)
- Fedus et al. *Switch Transformer*(2021)
- Mistral *Mixtral of Experts*(2023)
- DeepSeek-V2 / V3 技术报告
