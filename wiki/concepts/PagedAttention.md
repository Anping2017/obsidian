---
title: PagedAttention
type: concept
tags: [ai, mature]
sources: [raw/AI人工智能/]
created: 2026-05-05
updated: 2026-05-05
summary: PagedAttention 借鉴操作系统虚拟内存分页思想管理大模型 KV 缓存,大幅减少显存碎片,是 vLLM 推理引擎吞吐量 24× 提升的关键技术。
---

# PagedAttention

## 定义

PagedAttention 是加州大学伯克利分校 vLLM 项目提出的[[大语言模型]]推理优化技术,借鉴操作系统的虚拟内存(Virtual Memory)与分页(Paging)思想,将 KV 缓存切分为固定大小的"页"(Block),按需分配,大幅减少显存浪费。

## 问题背景

传统 LLM 推理框架(如 HuggingFace Transformers)将每个请求的 KV 缓存预分配为一段连续显存,以容纳最大序列长度。这造成:
- **内部碎片**:实际序列短,但预留长,浪费显存
- **外部碎片**:不同请求长度差异大,显存被切碎,新请求难以装入
- **难以共享**:相同前缀的请求无法共享 KV 缓存

实测表明传统方法显存利用率仅 20-40%。

## PagedAttention 机制

- KV 缓存按固定块(Block,常 16 个 token)切分
- 每个块独立分配,通过逻辑-物理块表映射
- 实际填充才分配,序列动态延长无需复制
- 支持[[束搜索]](Beam Search)与并行采样的 KV 共享(Copy-on-Write)

## 性能提升

vLLM 报告显示,在相同 GPU 上吞吐量比 HuggingFace Transformers 高 14-24 倍,KV 缓存内存浪费从 60-80% 降至 4% 以下。

## 与其他概念的关系

- 与[[FlashAttention]]:互补,FlashAttention 优化计算,PagedAttention 优化内存
- 与[[推测解码]]:可叠加使用,共同提升推理效率
- 与[[模型量化]]:量化减小每个块大小,PagedAttention 安排块的位置
- 是 vLLM 推理引擎的标志性技术,后被 TensorRT-LLM、SGLang 等借鉴
- 与[[Transformer架构|Transformer]] 注意力机制紧密耦合

## 实现库

- vLLM(原生支持)
- TGI (Text Generation Inference)
- SGLang
- llama.cpp 的 KV cache 分块管理

## 与系统视角

是 LLM Serving 进入"系统化"时代的标志:不再单纯追求模型层优化,而是用计算机系统(分页、调度、缓存)思想全栈优化。

## 参考源

- raw/AI人工智能/04-综合提升层/
- Kwon et al. "Efficient Memory Management for Large Language Model Serving with PagedAttention" (SOSP 2023)
- vLLM GitHub
