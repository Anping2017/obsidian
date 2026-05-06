---
title: CLIP
type: concept
tags: [ai, mature]
sources: [raw/AI人工智能/04-前沿技术专题/04-02-多模态学习.md, raw/AI人工智能/03-应用层/03-01-计算机视觉/03-01-06-CV技术发展脉络.md]
created: 2026-05-05
updated: 2026-05-05
summary: OpenAI 2021 年提出的图文对齐模型,通过对比学习把图像和文本嵌入到统一向量空间,实现零样本图像分类与文图检索,是多模态 AI 的奠基性工作。
---

# CLIP

## 定义

**CLIP**(Contrastive Language-Image Pretraining,**对比式图文预训练**)是 [[OpenAI]] 在 2021 年论文 *Learning Transferable Visual Models From Natural Language Supervision* 中提出的多模态模型。

它通过在 4 亿张"互联网图文对"上做**对比学习**,把图像和文本嵌入到**同一个向量空间**:语义相近的图文对在该空间中距离接近,无关的距离远离。这一统一空间使得**零样本图像分类**、文图检索、AIGC 文图引导等任务成为可能。

它与 [[Vision Transformer]] 共同奠定了多模态 AI 时代的基础,Stable Diffusion、DALL-E、Sora 等模型的文本理解部分都依赖 CLIP 类技术。

## 核心要点

### 核心架构

```
                              对比学习损失
                                  ↑
    图像编码器(ViT/ResNet) ←──→ 文本编码器(Transformer)
            ↓                            ↓
       图像 embedding              文本 embedding
            └──────── 余弦相似度 ────────┘
```

两个独立编码器把不同模态映射到共享 d 维空间。

### 训练数据

- **WebImageText (WIT)**:从互联网爬取的 4 亿"图像-文本"对
- 文本是 alt-text、caption、附近段落
- 噪声大但量大,用规模克服质量

### 训练目标:InfoNCE 对比损失

每个 batch 内 N 张图、N 段文本,构成 N×N 配对矩阵:
- 对角线元素 = 真匹配,目标相似度高
- 非对角线 = 不匹配,目标相似度低

```
L = -log[exp(sim(I_i, T_i)/τ) / Σ exp(sim(I_i, T_j)/τ)]
```

τ 是温度,控制分布锐度。同时计算图→文与文→图两个方向的损失,取平均。

### 零样本分类机制

CLIP 不需要重新训练即可分类任意类别:

```
1. 类别名转化为提示文本:
   "a photo of a cat" / "a photo of a dog" / ...
2. 各类提示用文本编码器获得 embedding
3. 待分类图像用图像编码器获得 embedding
4. 计算图像与各类文本的余弦相似度
5. 选最高相似度的类别为预测结果
```

实质把分类问题转化为图文匹配问题,**避开传统分类需重新训练的限制**。

### Prompt 工程对 CLIP 同样有效

不同提示模板影响分类效果:
- "cat" vs "a photo of a cat" vs "a photo of a {} cat" 性能差异显著
- 用多模板平均(prompt ensembling)进一步提升

CLIP 是 [[提示词工程]] 思想在视觉领域的早期实践。

### 性能水平

- 在 ImageNet 零样本上达到 76.2%(已训练 ResNet-50 监督水平)
- 在 30+ 数据集上的零样本性能与监督模型相当
- 对分布偏移(domain shift)鲁棒性显著优于监督模型

### 重要扩展

#### OpenCLIP / EVA-CLIP

社区开源版本,LAION-5B 数据集训练,部分场景超越 OpenAI 原版。

#### SigLIP(Google,2023)

把 InfoNCE 替换为 sigmoid 损失,更稳定且无需大 batch,成为新一代基础。

#### DFN(Data Filtering Network)

通过模型筛选数据质量,显著提升小规模 CLIP 性能。

#### Long-CLIP

支持长文本(超过 77 token 的 CLIP 默认限制)。

### 在 AIGC 中的角色

#### 文生图(DALL-E 2、Stable Diffusion)

```
文本 → CLIP 文本 embedding
     → 引导扩散模型生成图像
     → 生成图像与原文本语义对齐
```

CLIP 提供"语义空间",扩散模型在其引导下生成相符图像。

#### 文生视频(Sora、Runway)

类似机制,CLIP 提供文本理解。

#### 图像编辑(InstructPix2Pix)

CLIP 帮助理解编辑指令的语义。

### 应用领域

- **跨模态搜索**:用文字搜图、用图搜文
- **零样本分类**:无需训练即可分新类
- **图像检索**:大规模图库的语义检索
- **数据筛选**:用 CLIP 评分筛选高质量训练数据
- **图像生成引导**:扩散模型条件输入
- **图像质量评估**:CLIP-IQA 等
- **多模态 LLM 的视觉前端**

### 局限性

#### 1. 抽象推理

CLIP 学到的是"看起来相似",不是"语义关系":
- 难以理解"杯子在桌子上"vs"桌子在杯子上"
- 数数能力差(三只猫和五只猫)

#### 2. 长尾偏差

训练数据中常见的内容效果好,稀有概念效果差。

#### 3. 文化偏见

互联网数据带有文化偏见,影响下游应用。

#### 4. 文本长度受限

默认 77 token,长描述被截断。

#### 5. 词袋偏好

CLIP 对"句子结构"理解弱,更像"词袋"匹配。

### 后续路径

#### Multimodal LLMs

GPT-4V、Gemini、Claude 3 直接把视觉编码器(ViT 类)与 LLM 结合,具备 CLIP 缺失的复杂推理能力。

#### CoCa、BLIP-2、LLaVA

把图像视觉特征"翻译"为 LLM 可接受的 token,实现视觉-语言深度融合。

#### Flamingo、Llama 3.2 Vision

冻结 LLM,仅训练视觉适配器,降低成本。

## 和其他概念的关系

- 视觉编码器通常基于 [[Vision Transformer]]
- 与 [[Stable Diffusion]]、DALL-E 等 AIGC 模型共同构建多模态生态
- 思想源于对比学习,与 SimCLR、MoCo 一脉相承
- 是 [[OpenAI]] 早期重要贡献
- 与 [[Transformer]] 文本编码器架构一致
- [[Embedding]] 思想的多模态扩展
- 影响后续多模态 LLM 的视觉前端设计
- 与 [[词嵌入]] 在概念上类比

## 参考源

- raw/AI人工智能/04-前沿技术专题/04-02-多模态学习.md
- raw/AI人工智能/03-应用层/03-01-计算机视觉/03-01-06-CV技术发展脉络.md
