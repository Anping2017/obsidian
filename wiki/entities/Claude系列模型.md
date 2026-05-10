---
title: Claude 系列模型
type: entity
tags: [ai, mature]
sources: [raw/AI人工智能/]
created: 2026-05-05
updated: 2026-05-05
summary: Claude 是 Anthropic 推出的大语言模型家族,以 Constitutional AI 为对齐核心,强调诚实、有用、无害,长上下文与代理能力领先,Sonnet/Opus/Haiku 三档定位。
---

# Claude 系列模型

## 简介

Claude 是 [[Anthropic]] 自 2023 年推出的[[大语言模型]]家族,以"可解释性优先"和[[Constitutional AI]]训练范式为标志,主打企业级安全与可靠。命名取自数学家 Claude Shannon。

## 关键代际

### Claude 1(2023 年 3 月)

首版,强调长文档处理与拒答能力。

### Claude 2(2023 年 7 月)

100k 上下文,代码与推理能力增强。

### Claude 3(2024 年 3 月)

引入三档:Haiku(轻量)、Sonnet(主力)、Opus(旗舰),首次在 MMLU 等基准超过 GPT-4。

### Claude 3.5 Sonnet(2024 年 6 月)

代码与多模态能力跨越,Artifacts 功能实现互动产物。

### Claude 3.7 Sonnet(2025 年 2 月)

引入推理模式("Extended Thinking"),可控制思考预算。

### Claude 4(2025 年 5 月,Sonnet 4 / Opus 4)

更长任务持续性、更优代理能力、200k+ 上下文。

### Claude 4.5/4.7(2025-2026)

主流 1M 上下文窗口,SWE-Bench 等代码基准领先。

## 技术特色

- **[[Constitutional AI]]**:用宪法原则替代部分人类反馈
- **长上下文**:从 100k 到 1M tokens 演进
- **MCP(Model Context Protocol)**:Anthropic 推动的开放协议
- **Computer Use**:操作浏览器与桌面的代理能力
- **可解释性研究**:发表 SAE、电路追踪等机理可解释论文

## 产品形态

- Claude.ai 网页对话
- API 平台
- Claude Code CLI 编程代理
- AWS Bedrock、Google Vertex 集成

## 与其他模型对比

- vs [[GPT系列模型]]:Claude 在写作风格、长上下文、代理任务上常领先
- vs [[Gemini系列模型]]:Claude 偏专业,Gemini 偏全能
- vs [[Llama系列模型]]:Claude 闭源安全为先,Llama 开源生态
- 内核哲学差异:[[超级对齐]]优先 vs 能力优先

## 关联概念

- [[Constitutional AI]]、[[宪法AI]]
- [[RLHF]]、[[DPO直接偏好优化]]
- [[AI Agent框架]]、[[AI编码助手]]
- [[AI红队评估]]、[[超级对齐]]、[[越狱攻击]]
- [[指令微调]]、[[预训练与微调]]
- [[思维链]]、[[反思提示]]

## 参考源

- raw/AI人工智能/04-综合提升层/
- Anthropic Constitutional AI 论文
- Claude Model Card / Responsible Scaling Policy
