---
title: Siri 与 Apple Intelligence
type: concept
tags: [ios, mature]
sources: [raw/iPhone/iPhone知识体系/03-功能特性层/智能功能/01-Siri语音助手.md, raw/iPhone/iPhone知识体系/03-功能特性层/智能功能/02-机器学习功能.md]
created: 2026-05-05
updated: 2026-05-05
summary: Siri 是 Apple 自 2011 年(iPhone 4s)引入的语音助手,2024 年与 Apple Intelligence 整合后获得 LLM 能力,以"端侧优先 + Private Cloud Compute"为隐私架构特色。
---

# Siri 与 Apple Intelligence

## 定义

Siri 是 Apple 在 iOS 上的语音交互系统,2011 年 iPhone 4s 首发,经历了"指令式 → 对话式 → 大模型驱动"三个阶段。2024 年 WWDC 公布的 **Apple Intelligence** 是 Siri 与生成式 AI 的整合,把 Siri 重新置于 iOS 的核心交互层。

## 核心要点

### 三阶段演进

- **早期 Siri(2011-2015)**:基于规则与意图分类,主要本地处理,功能局限于打电话、查天气、设提醒。
- **智能 Siri(2016-2020)**:云端语音识别 + 机器学习,扩展到 SiriKit、HomeKit、智能建议。这一阶段 Siri 长期被批评"不如 Alexa/Google Assistant",尤其在多轮对话与上下文记忆上。
- **现代 Siri / Apple Intelligence(2021- )**:接入大语言模型,具备文本生成、邮件总结、图像清理、跨 App 操作能力。

### Apple Intelligence 架构特点

Apple 选择了与 Google/微软完全不同的路线:**端侧优先**。
- **设备端模型**:在 iPhone 15 Pro / 16 全系本地运行(依赖 [[A系列芯片]] 的神经网络引擎)
- **Private Cloud Compute**:超出端侧能力时,数据加密上传到 Apple 自建、专门定制的服务器,处理后立即销毁,Apple 自己也无法读取。第三方安全研究者可审计该承诺。
- **第三方扩展**:可调用 ChatGPT,但每次调用前明确征得用户同意。

### 与传统语音助手对比

| 维度 | 传统 Siri | Apple Intelligence |
|---|---|---|
| 模型规模 | 小型分类器 | 端侧 ~3B + 云端 LLM |
| 上下文 | 单轮为主 | 多轮 + 跨 App |
| 隐私 | 部分上云 | 端侧优先 + PCC 加密 |
| 个性化 | 静态偏好 | 动态学习用户语境 |

### 国内特殊性

由于监管要求,Apple Intelligence 在中国大陆推出时间晚于其他市场,且需与本地大模型(如百度文心)合作满足合规。

### 与 [[iOS系统架构]] 的耦合

Siri 的"无处不在"靠的是系统级 API:Shortcuts、SiriKit、App Intents。开发者把 App 暴露给 Siri 的方式是声明式的(意图 + 参数),Siri 在调度时不需要第三方 App 在后台保活,这又回到了 [[iOS系统架构]] 的沙盒/后台限制设计。

## 关系

- 由 [[A系列芯片]] 中的神经网络引擎驱动端侧推理
- 是 [[iOS系统架构]] 的系统级服务
- 是 [[Apple生态系统]] 跨设备体验的入口(在 Watch、HomePod、Mac 上调用同一 Siri)

## 参考源

- raw/iPhone/iPhone知识体系/03-功能特性层/智能功能/01-Siri语音助手.md
- raw/iPhone/iPhone知识体系/03-功能特性层/智能功能/02-机器学习功能.md
