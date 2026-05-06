---
title: 生成式AI
type: concept
tags: [ai, mature]
sources: [raw/AI人工智能/04-前沿技术专题/04-03-生成式AI技术.md]
created: 2026-05-05
updated: 2026-05-05
summary: 生成式 AI 能从训练数据中学习分布并生成全新内容(文本、图像、音频、视频、代码),代表方法包括 Transformer、GAN、Diffusion 等。
---

# 生成式AI

## 定义

**生成式 AI(Generative AI, GenAI)** 指能学习训练数据分布并生成与之相似但全新的内容(文本、图像、音频、视频、代码、3D 模型等)的 [[人工智能]] 系统。它与判别式 AI(只做分类、预测)互补,是 2022 年以来 AI 公众认知的爆炸性载体。

## 核心要点

**主要技术家族**

| 类别 | 代表方法 | 主战场 |
|---|---|---|
| 自回归 | [[Transformer]] / [[大语言模型]] | 文本、代码、对话 |
| GAN(2014) | StyleGAN、CycleGAN | 图像生成、图像翻译 |
| VAE(2013) | Vanilla VAE、VQ-VAE | 表示学习、半结构化生成 |
| 扩散模型(Diffusion) | DDPM、Stable Diffusion、DALL-E 3 | 图像、视频、音频生成 |
| 流模型(Flow) | Normalizing Flow | 概率密度估计 |

**典型产品**

- 文本/对话:ChatGPT、Claude、Gemini
- 图像:Midjourney、Stable Diffusion、DALL-E、FLUX
- 视频:Sora、Veo、Runway
- 音频与音乐:Suno、ElevenLabs、Udio
- 代码:GitHub Copilot、Cursor、Claude Code
- 3D:Meshy、Tripo

**关键能力维度**

- 可控性:文本/图像 prompt 控制风格、内容、结构
- 一致性:多帧/多角度时角色与场景保持一致(视频生成核心难点)
- 编辑性:局部修改、保留其余(inpainting、ControlNet)
- 真实性:对抗"AI 痕迹"
- 速度:从几分钟到实时,影响产品形态

**主要风险**

- 深度伪造(deepfake)与虚假信息
- 版权:训练数据是否合规
- [[幻觉]]:文本生成中事实错误
- 人类创作生态被冲击
- 滥用:钓鱼、欺诈、恶意内容生成

**与判别式 AI 的关系**

- 判别式:学 $p(y|x)$,做分类、识别
- 生成式:学 $p(x)$ 或 $p(x|c)$,做生成
- 现代大模型同时具备两者能力(LLM 可分类亦可生成)

## 和其他概念的关系

- 主流载体:文本侧由 [[大语言模型]] 主导,图像侧 Diffusion 主导
- 共同基础:[[Transformer]] 在跨模态(文本→图像、视频)中担纲条件编码
- 训练范式:依赖 [[预训练与微调]],尤其大规模无标签自监督预训练
- 对齐技术:[[RLHF]] 也在图像/视频生成中应用(美学评价对齐)
- 应用集成:与 [[AI Agent]]、[[RAG]] 共构现代 AI 应用栈

## 参考源

- raw/AI人工智能/04-前沿技术专题/04-03-生成式AI技术.md
- raw/AI人工智能/04-前沿技术专题/04-02-多模态学习.md
- raw/AI人工智能/04-前沿技术专题/04-01-大语言模型技术.md
