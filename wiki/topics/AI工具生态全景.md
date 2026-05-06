---
title: AI 工具生态全景
type: topic
tags: [pkm, ai, mature]
sources: [raw/我的收藏/工具网址/AI工具.md, raw/我的收藏/AI视频/短视频爆款主题.md, raw/我的收藏/工具prompt/Lyra提示词专家.md, raw/我的收藏/工具prompt/JSON Prompt.md]
created: 2026-05-05
updated: 2026-05-05
summary: 2025 年 AI 工具生态可分为大语言模型、图像/视频生成、配音/音乐、剪辑/排版、自动工作流、开发助手六大象限,选择重点是匹配工作流而非追新。
---

# AI 工具生态全景

## 概述

2025 年的 AI 工具数量已超过 2 万款,任何"完整列表"都过时即失效。本主题不做穷举,而是用 **功能象限** 框架理解市场,帮助读者建立选型思维。重点不在"哪个最好",而在"哪个适合我的工作流"。

## 多角度分析

### 六大功能象限

| 象限 | 代表工具 | 适用场景 |
|---|---|---|
| 大语言模型(LLM) | ChatGPT、Claude、Gemini、Grok | 通用对话、写作、推理 |
| 图像生成 | Midjourney、即梦、Krea、Recraft、Nano Banana | 插画、品牌素材、概念稿 |
| 视频生成 | Runway、Pika、Sora、可灵、Veo3、Luma | 短视频、广告、概念片 |
| 配音/音乐 | ElevenLabs、Sora 配音、Suno、Mureka | 旁白、广告、BGM |
| 剪辑/排版 | CapCut(剪映)、Veed.io、Canva、Adobe Express | 短视频后期、平面设计 |
| 自动工作流 | Zapier、n8n、Coze、Make、Claude Skills | 跨工具串联 |

### LLM 选型逻辑

- **ChatGPT(GPT-4o/5)**:生态最广,插件/Custom GPT 多,中文一般
- **Claude(Sonnet/Opus 4.x)**:长上下文(1M token)、写作/代码质量高、安全偏保守
- **Gemini(2.x Pro)**:多模态强,Google 生态深度集成
- **Grok**:X 数据访问、风格更"野"
- **DeepSeek/Qwen**:中文强,价格低,适合本地部署

每个 LLM 都有"性格"。同一 prompt 的输出风格差异显著,选模型像选作者。

### 图像与视频的"大模型 vs 工具链"

- **底层模型**:Stable Diffusion、Flux、Midjourney、即梦、Sora
- **上层产品**:Civitai(LoRA 模型市场)、Krea(实时迭代)、Recraft(矢量风)、Liblib(电商)

新手一般直接用上层产品(订阅制),高阶玩家在 ComfyUI / Forge 等工作流工具上自由组合底层模型与 LoRA。

### 提示词工程的两个流派

- **自然语言流派**:用尽量自然的中文/英文描述,依赖 LLM 自身理解。适合快速对话。
- **结构化流派**:JSON、XML、伪代码等结构,精准控制输出。适合 API 调用、自动化。

代表 prompt 工具:**Lyra**(自然语言四步优化:Deconstruct → Diagnose → Develop → Deliver)、**JSON Prompt**(把视频/图像描述转为 JSON 结构,便于复用)。

### 自动工作流的崛起

2024-2025 最大变化是工作流工具普及:
- **Zapier**:最老牌,集成最广,定价偏贵
- **Make(原 Integromat)**:可视化流程图,功能强
- **n8n**:开源自托管,适合技术团队
- **Coze(扣子)**:字节出品,中文友好,Agent 强
- **Claude Skills / Agent SDK**:基于 LLM 的"自主调用工具"模式

这些工具的关键作用,是把"AI 输出 + 业务系统"打通,从单点效率走向流程自动化。

### 短视频专项

短视频是 AI 工具应用最热的场景:
- **生成**:Runway/Pika/Sora 直生,或 SD + AnimateDiff 工作流
- **配音**:ElevenLabs(英文最强)、微软 Azure TTS(中文晓晓/云希)
- **剪辑**:CapCut AI 自动字幕 + 节奏识别;Veed.io 自动剪辑
- **封面**:Canva AI Magic Studio、Ideogram 直生封面

爆款逻辑(YouTube Shorts 2025 算法核心):**完成率 / 重播率 / 分享率 / 语言无关性 / 高频更新**。AI 工具正帮助创作者降低"高频"成本。

### 选型反模式

- **追新**:每周换工具,什么都浅尝辄止
- **多个 LLM 同时订阅**:成本高且分散精力,选 1 个主用 1 个备用即可
- **不试就否定**:某些工具的强项要用过 2 周才显现
- **过度依赖 AI**:把判断、品味、原创性外包给模型,失去自己的视角

### 工具选择心法

1. **先描述工作流**:从输入到输出每一步是什么
2. **找瓶颈**:哪一步最慢/最痛苦
3. **针对性选工具**:不要"为了用 AI 而用 AI"
4. **测 2-4 周**:足够形成肌肉记忆判断好坏
5. **保留切换余地**:工具是手段,不要被锁定

## 结论

AI 工具生态的"信息量焦虑"是真实的,但解药不是看更多榜单,而是 **建立自己的工作流地图**。明白自己每天做什么、痛在哪、想自动化什么,工具的选择就会自然清晰。本主题与 [[PKM方法论]] 是同一精神:工具服务方法,方法服务目标。

## 参考源

- raw/我的收藏/工具网址/AI工具.md
- raw/我的收藏/AI视频/短视频爆款主题.md
- raw/我的收藏/工具prompt/Lyra提示词专家.md
- raw/我的收藏/工具prompt/JSON Prompt.md
