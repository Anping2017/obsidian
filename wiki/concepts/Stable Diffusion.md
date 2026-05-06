---
title: Stable Diffusion
type: concept
tags: [ai, mature]
sources: [raw/AI人工智能/04-前沿技术专题/04-03-生成式AI技术.md, raw/AI人工智能/04-前沿技术专题/04-02-多模态学习.md]
created: 2026-05-05
updated: 2026-05-05
summary: Stability AI 与慕尼黑大学等 2022 年发布的开源潜在扩散模型,把扩散过程移到压缩后的潜在空间,大幅降低算力门槛并引爆 AIGC 开源生态。
---

# Stable Diffusion

## 定义

**Stable Diffusion**(SD)是 Stability AI、慕尼黑大学(LMU)CompVis 实验室和 Runway 在 2022 年 8 月联合发布的**开源潜在扩散模型**(Latent Diffusion Model, LDM),技术核心来自论文 *High-Resolution Image Synthesis with Latent Diffusion Models*(2021)。

它把传统扩散模型的去噪过程从"像素空间"移到"潜在空间"(latent space),让生成 512×512 高质量图像的算力需求从数据中心级降到**消费级 GPU**(8GB 显存),并以**完全开源**的姿态引爆了 AIGC 开源生态——ControlNet、LoRA、各类风格模型、视频/音频扩散等都在其基础上发展。

## 核心要点

### 三大组件架构

```
              Text("a cat in space")
                    ↓
              Text Encoder(CLIP / OpenCLIP)
                    ↓
              Cross-Attention 条件
                    ↓
[噪声 latent] → U-Net 去噪 → ... → [清晰 latent]
                                      ↓
                                  VAE 解码器
                                      ↓
                                   图像输出
```

| 组件 | 作用 |
|---|---|
| **VAE** | 把 512×512 像素压缩到 64×64 潜空间,降维 8× |
| **U-Net** | 在潜空间执行去噪,核心扩散模型 |
| **Text Encoder** | 把文本编码为条件向量(SD 1.x 用 CLIP, SD 2.x/XL 用 OpenCLIP) |

### 扩散过程的简洁公式

#### 前向(加噪)

逐步把清晰图像 $x_0$ 加噪到纯噪声 $x_T$:
$$
x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1-\bar{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0,I)
$$

#### 反向(去噪)

学习一个网络 $\epsilon_\theta(x_t, t, c)$ 预测噪声:
$$
L = \mathbb{E}_{x_0,\epsilon,t,c}\left[||\epsilon - \epsilon_\theta(x_t, t, c)||^2\right]
$$

其中 $c$ 是文本条件。

#### 采样

从随机噪声开始,迭代去噪 30-50 步,得到生成图像。常用算法:
- DDIM
- DPM-Solver
- LCM(蒸馏后,4 步出图)

### 主要版本演化

| 版本 | 时间 | 关键改进 |
|---|---|---|
| **SD 1.4 / 1.5** | 2022 | 首次开源,512×512 |
| **SD 2.0 / 2.1** | 2022-2023 | OpenCLIP,768×768 |
| **SDXL 1.0** | 2023 | 1024×1024,双 text encoder,高质量 |
| **SDXL Turbo** | 2024 | 1 步出图(蒸馏) |
| **SD 3 Medium** | 2024 | DiT 架构(把 U-Net 替换为 Transformer) |
| **Flux.1** | 2024 | Black Forest Labs(SD 团队分离),代际超越 |

### 核心创新:Latent Diffusion

经典扩散模型在像素空间扩散,512×512×3 的张量去噪极其昂贵。LDM 思想:

```
1. 用 VAE 把图像压缩到 64×64×4 潜空间(8× 压缩)
2. 在潜空间做扩散(计算量降低 64 倍)
3. 最后 VAE 解码回像素空间
```

这一变化让扩散模型从"研究论文"变为"消费级应用"。

### 条件机制(Cross-Attention)

文本通过 [[CLIP]] 文本编码器变成 token 序列,通过 cross-attention 注入 U-Net:

```
图像 latent: query
文本 token: key, value
```

这让生成图像与文本高度对齐。

### 开源生态(2022-2025)

#### ControlNet(张吕敏,2023)

冻结 SD 主模型,加可训练副本接收"控制信号"(边缘、骨架、深度图、Canny 等),实现**结构可控生成**。一夜爆红,成为 AIGC 工业化落地的关键。

#### LoRA(2023 应用)

仅训练一对低秩矩阵适配器(几 MB),让用户用自己的数据"训出风格"——动漫、特定人物、特定场景。Civitai、HuggingFace 上有十万级 LoRA。

#### Textual Inversion / DreamBooth

少量图像即可让模型学会新概念(自己的脸、特定物体)。

#### Image-to-Image / Inpainting

不再是"从噪声生成",而是"以现有图像为起点修改"。

### 商业应用

- **Midjourney**(闭源,但思想类似)
- **Adobe Firefly**:训练数据合规
- **Runway**:视频生成
- **Leonardo / Playground AI**:用户友好的 SD 服务
- **本地部署**:Stable Diffusion WebUI、ComfyUI 是开发者社区主流工具

### 法律与道德议题

#### 版权争议

- 训练数据包含未授权艺术家作品 → 起诉(Getty Images vs Stability AI)
- 生成图像版权归属(美国版权局拒绝纯 AI 作品版权)

#### 深度伪造与有害内容

- 名人深度伪造、未经同意的私密图像
- 各国推动 AI 生成内容标识规则

#### 数据集偏见

- LAION-5B 包含偏见、暴力、儿童不良内容
- LAION-5B 一度因 CSAM 内容被下架重组

### Flux 与新一代

2024 年 Black Forest Labs(原 SD 团队)发布 Flux,在 12B 参数下达到 SD3 与 Midjourney 水平,继续推动开源前沿。

### 视频与多模态扩散

扩散思想已扩展到:
- **视频生成**:Sora、Runway Gen-3、Pika、Kling
- **音频生成**:AudioLDM、MusicLM
- **3D 生成**:DreamFusion、Wonder3D

### 与生成式 AI 主流路线对比

| 方法 | 代表 | 特点 |
|---|---|---|
| 扩散模型 | SD、DALL-E、Imagen | 高质量,慢 |
| 自回归 | Parti、xAI | 较慢但灵活 |
| GAN | StyleGAN | 快但模式坍塌 |
| 流匹配 | Flux、SD3 | 新兴,效率高 |

扩散模型 2022-2024 主导,流匹配 2024+ 后来居上。

## 和其他概念的关系

- 文本理解模块依赖 [[CLIP]] 系列
- 视觉处理与 [[Vision Transformer]] 思想相通
- 与 GAN([[卷积神经网络]] 的对抗学习版本)在生成式 AI 中并立
- 训练时利用 [[反向传播]] + Adam 优化器
- 推理优化用 [[模型量化]] 等技术
- 与 [[OpenAI]] 的 DALL-E、Google 的 Imagen 形成商业 vs 开源对照
- 是 AIGC 开源生态的事实基础

## 参考源

- raw/AI人工智能/04-前沿技术专题/04-03-生成式AI技术.md
- raw/AI人工智能/04-前沿技术专题/04-02-多模态学习.md
