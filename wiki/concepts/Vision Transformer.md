---
title: Vision Transformer
type: concept
tags: [ai, mature]
sources: [raw/AI人工智能/03-应用层/03-01-计算机视觉/03-01-06-CV技术发展脉络.md, raw/AI人工智能/04-前沿技术专题/04-02-多模态学习.md]
created: 2026-05-05
updated: 2026-05-05
summary: Google 2020 年提出的把图像分块视为 token 序列、用纯 Transformer 处理的视觉模型,打破 CNN 在计算机视觉的主导地位。
---

# Vision Transformer

## 定义

**Vision Transformer**(ViT)是 Google 团队在 2020 年论文 *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale* 中提出的视觉模型。

它把**图像切分为固定大小的图块(patches)**,每个图块投影为向量后作为 [[Transformer]] 的输入 token——**完全摒弃 CNN 的卷积结构**,直接用 NLP 的 Transformer 架构处理图像分类。

它打破了 CNN 在计算机视觉十年的主导地位,与 [[CLIP]]、Stable Diffusion 等共同奠定多模态 AI 时代的视觉基础。

## 核心要点

### 核心思路

```
图像(224×224×3) → 切分为 14×14 = 196 个图块(每块 16×16×3)
                → 每块展平 + 线性投影 → 196 个 token
                → 加位置编码 + [CLS] token
                → 输入标准 Transformer Encoder
                → [CLS] 输出 → 分类头
```

完全套用 [[Transformer]] 架构,只在输入端做"图像 → token"的转换。

### 关键设计

#### 1. Patch Embedding

把 $H \times W \times C$ 图像切分为 $N = HW/P^2$ 个 $P \times P \times C$ 图块,每块展平后投影到 $d$ 维。

#### 2. 位置编码

由于注意力本身位置无关,需显式加入位置嵌入(可学习 1D 或 2D)。

#### 3. [CLS] Token

借自 [[BERT]] 的设计,加入一个特殊 token,其最终表示用作整图分类。

#### 4. 标准 Transformer Encoder

多层 Self-Attention + FFN + LayerNorm,完全照搬 NLP 的设计。

### 与 CNN 的根本差异

| 维度 | CNN | ViT |
|---|---|---|
| **归纳偏置** | 平移等变、局部性、层次性 | 几乎无 |
| **感受野** | 浅层小、深层大 | 第一层即全局 |
| **参数共享** | 卷积核共享 | Attention 权重不共享 |
| **数据需求** | 中等数据集即可 | 需大规模数据(ImageNet-21k+) |
| **可解释性** | 滤波器可视化 | 注意力图 |
| **计算复杂度** | 局部 | $O(N^2)$ |

CNN 的"先验知识"在数据少时是优势;数据多时反而限制学习,ViT 因无先验,大数据下可学到更优表示。

### 论文核心实验

| 数据 | CNN(ResNet) | ViT |
|---|---|---|
| ImageNet-1k(1.3M) | 优于 | 较差 |
| ImageNet-21k(14M) | 接近 | 接近 |
| JFT-300M(300M) | 较差 | **优于** |

预训练规模决定 ViT 与 CNN 的胜负,这一发现与 NLP 的 scaling laws 高度一致。

### 主要变体

#### Swin Transformer(2021,Microsoft)

引入"移位窗口"局部注意力,把 $O(N^2)$ 降为 $O(N)$,且加入层次性结构,在密集预测任务(检测、分割)上更优。

#### DeiT(Facebook)

通过蒸馏从 CNN 教师传递知识,只用 ImageNet-1k 训练即可达 ViT-Big 水准。

#### MAE(Masked Autoencoder)

何凯明等的自监督方法,把 75% 图块遮盖,用解码器重建,极大提升 ViT 预训练效率。

#### DINOv2(Meta)

自监督学习的代表,在不需标注的情况下学到通用视觉表征。

### 在多模态 AI 中的位置

```
ViT 是视觉编码器,与 LLM 解码器组合:
图像 → ViT → 视觉 token → 与 LLM 文本 token 拼接 → 多模态 LLM(GPT-4V, Gemini, Claude 3)
```

[[CLIP]] 用 ViT 做图像编码器实现"图文对齐",成为 AIGC、多模态搜索的基础。

### 计算成本与优化

ViT 长序列(高分辨率图像)$O(N^2)$ 复杂度成瓶颈:
- 高分辨率(1024×1024)→ 4096 patches
- [[FlashAttention]]、Sliding Window、Linear Attention 等降本技术普遍使用
- Token Pruning:剔除不重要 token

### 应用范围

#### 图像分类
ViT、Swin、ConvNeXt(融合 CNN 思想)

#### 目标检测
DETR、Deformable DETR(Transformer-based 检测器)

#### 语义分割
SegFormer、Mask2Former

#### 医学影像
ViT 在小数据集表现一度不佳,但通过预训练 + 蒸馏后已与 CNN 持平甚至超越

#### 视频理解
Video Swin、TimeSformer、ViViT

### 反思:CNN 的反击

2022 年 *A ConvNet for the 2020s*(ConvNeXt)证明把 ViT 的训练技巧应用到 CNN 上,CNN 仍能与 ViT 持平。

结论:**架构差异 < 训练技巧差异 + 数据规模差异**。这是深度学习"the bitter lesson"(规模为王)的又一注脚。

### 与多模态时代

ViT 之于视觉,如 [[Transformer]] 之于 NLP——它使**统一架构**(unified architecture)成为可能:
- 同一架构处理文本、图像、视频、语音
- 共享自注意力、位置编码、训练范式
- 多模态融合天然友好

GPT-4V、Gemini、Claude 3 视觉能力均依赖 ViT 类编码器。

## 和其他概念的关系

- 直接来源:[[Transformer]] 架构在视觉领域的应用
- 与 [[卷积神经网络]] 形成对照,部分场景已超越
- 与 [[CLIP]]、[[Stable Diffusion]] 共同支撑多模态 AI
- 应用 [[FlashAttention]]、[[模型量化]] 提升效率
- 在 [[预训练与微调]] 范式下表现最佳
- [[计算机视觉]] 当代主流架构之一
- 与 [[模型蒸馏]] 配合在小模型上仍可获得强能力(DeiT)

## 参考源

- raw/AI人工智能/03-应用层/03-01-计算机视觉/03-01-06-CV技术发展脉络.md
- raw/AI人工智能/04-前沿技术专题/04-02-多模态学习.md
