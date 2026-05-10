---
title: FlashAttention
type: concept
tags: [ai, mature]
sources: [raw/AI人工智能/04-前沿技术专题/04-01-大语言模型技术.md, raw/AI人工智能/02-理解层/02-03-算法与模型/02-03-04-Transformer架构.md]
created: 2026-05-05
updated: 2026-05-05
summary: 斯坦福 Tri Dao 提出的精确注意力 IO 优化算法,通过分块与重计算将 GPU 内存访问减少一个数量级,是现代大模型训练与推理的事实标准。
---

# FlashAttention

## 定义

**FlashAttention** 是斯坦福 Tri Dao 等人在 2022 年论文 *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness* 中提出的**精确注意力**(Exact Attention)算法,通过 GPU 内存层级感知的**分块计算 + 在线 softmax + 重计算**,把 [[Transformer架构|Transformer]] 注意力的内存复杂度从 $O(N^2)$ 降到 $O(N)$,推理速度提升 2-4 倍。

它已成为 PyTorch、Hugging Face、vLLM、TensorRT 等主流框架的事实标准,是当代 [[大语言模型]] 长上下文与高效训练的关键支柱。

## 核心要点

### 标准注意力的瓶颈

```
Attention(Q, K, V) = softmax(QK^T / √d) × V
```

朴素实现:
1. 计算 $S = QK^T$,显存写入 $N \times N$ 矩阵
2. softmax 归一化 $P = \text{softmax}(S)$,读写 $N \times N$
3. 计算 $O = PV$,读 $P$ 与 $V$

GPU 上的瓶颈不在 FLOPs,**而在 HBM(高带宽内存)与 SRAM(片上缓存)间的 IO**。每个矩阵都要往返 HBM,长序列时主导时间消耗。

### FlashAttention 的核心思想

#### 1. 分块(Tiling)

把 $Q, K, V$ 切分为小块,只在 SRAM 中处理:

```
for 每个 Q 的块 Q_i:
    for 每个 K, V 的块 K_j, V_j:
        加载到 SRAM
        计算 S_ij = Q_i × K_j^T
        在线更新 softmax 和输出
```

避免存储完整的 $N \times N$ 注意力矩阵到 HBM。

#### 2. 在线 Softmax(Online Softmax)

经典 softmax 需要看到完整向量后两遍扫描:

```
m = max(x_i)
sum = Σ exp(x_i - m)
softmax_i = exp(x_i - m) / sum
```

在线算法逐块更新最大值与累加器,数学等价但单次扫描:
$$
m^{(j)} = \max(m^{(j-1)}, m_j)
$$
$$
\ell^{(j)} = e^{m^{(j-1)} - m^{(j)}} \ell^{(j-1)} + e^{m_j - m^{(j)}} \ell_j
$$

#### 3. 反向传播的重计算(Recomputation)

前向不存中间矩阵 $S, P$ → 反向时重新计算
- HBM 读写减少
- FLOPs 略增,但因 IO 主导,总时间减少

### 性能数据

在 NVIDIA A100 上(序列长度 2048-16384):

| 方法 | 速度 | 显存 |
|---|---|---|
| 标准 Attention | 1× | $O(N^2)$ |
| FlashAttention v1 | 2-4× | $O(N)$ |
| FlashAttention v2(2023) | 5-10× | $O(N)$ |
| FlashAttention v3(2024) | 利用 H100 TMA + FP8,~1.5-2× v2 | $O(N)$ |

### 与近似注意力的区别

历史上为降低 $O(N^2)$ 提出了大量近似方法:

| 方法 | 精度 |
|---|---|
| Sparse Attention | 近似(选择性关注) |
| Linear Attention | 近似(线性注意) |
| Performer | 近似(随机特征) |
| Reformer | 近似(LSH 聚类) |
| **FlashAttention** | **精确(等价标准注意力)** |

FlashAttention 的关键是"既加速又不近似",这是它统治市场的根本原因。

### 长上下文的关键

随着模型上下文从 2K 扩展到 100K+(Claude 200K、Gemini 1.5M):
- 朴素注意力:显存爆炸
- FlashAttention:线性显存,可处理超长序列
- 配合 **PagedAttention** 和 **滑动窗口**,实现百万级 token 推理

### 实务集成

主流框架默认开启:
```python
# Hugging Face Transformers
model = AutoModel.from_pretrained(name, attn_implementation="flash_attention_2")

# PyTorch 2.0+
torch.nn.functional.scaled_dot_product_attention(...)  # 自动选用 FlashAttention
```

vLLM、TensorRT-LLM、DeepSpeed 等推理引擎全面集成。

### v3 的硬件协同(2024)

H100 GPU 的新特性:
- **TMA**(Tensor Memory Accelerator):异步内存访问
- **WGMMA**(Warpgroup MMA):大块矩阵乘加速
- **FP8 计算**:精度可控的进一步加速

FlashAttention v3 充分利用这些特性,展示算法-硬件协同设计的威力。

### 与其他推理优化的关系

```
现代 LLM 推理优化栈:
[模型层]:  量化(INT4/8)+ MoE
[算法层]:  FlashAttention + Speculative Decoding
[内存层]:  PagedAttention + KV-Cache 管理
[调度层]:  Continuous Batching
[硬件层]:  Tensor Cores + TMA + FP8
```

### 衍生与替代

- **xFormers**(Meta):同类 IO 优化,部分场景使用
- **FlexAttention**(PyTorch 2.5+):允许自定义注意力变体的 FlashAttention
- **Ring Attention**:多 GPU 分布式注意力,百万级上下文

## 和其他概念的关系

- 直接优化 [[Transformer架构|Transformer]] 的注意力机制
- 加速 [[大语言模型]] 训练与推理
- 与 [[模型量化]] 配合实现极致优化
- 是长 [[上下文学习]]/长上下文窗口的关键技术
- 与 GPU 体系结构(SRAM、HBM)、CUDA 编程深度耦合
- 影响 [[预训练与微调]] 的训练吞吐
- 与 [[OpenAI]]、[[Anthropic]] 等公司的推理服务成本直接相关

## 参考源

- raw/AI人工智能/04-前沿技术专题/04-01-大语言模型技术.md
- raw/AI人工智能/02-理解层/02-03-算法与模型/02-03-04-Transformer架构.md
