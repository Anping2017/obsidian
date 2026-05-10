---
title: 学习系统迭代记录
type: topic
tags: [meta, learning-system, changelog]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: 学习辅助系统的版本与修订历史。版本号策略:月复盘改 PLAYBOOK 一项 +0.01,改 RULES 或增减 mode +0.1,架构重构 +1.0。
---

# CHANGELOG

> 版本号策略:月复盘改 PLAYBOOK 一项 → +0.01;改 RULES / 增减 mode → +0.1;架构重构 → +1.0
> 修改触发源:① 月复盘强制(每月 ≥1 处) ② 用户提"剧本不好用"即时重构

## v0.1 — 2026-05-10(初版)

- 创建 `learning/` 目录与 5 份核心文档(SYSTEM / RULES / PLAYBOOK / DASHBOARD / CHANGELOG)
- 在 vault 根 CLAUDE.md 加学习系统引导段
- 6 种 mode 全部启用:
  - **A** 学科诊断
  - **B** 跨域综合
  - **C** 主题深读
  - **D** 思维模型沙盒
  - **E** stub 升级
  - **F** 自由提问
- DASHBOARD 初始客观指标基于 PROGRESS.md(2026-05-06 快照),主观评分待用户首次月复盘填写
- 设计文档:[2026-05-10-system-design.md](_design/2026-05-10-system-design.md)
- 实施计划:[2026-05-10-implementation-plan.md](_design/2026-05-10-implementation-plan.md)

### 核心设计决策

- **工具箱模式**(非教练驱动):用户自驱性强,脚手架而非保姆
- **vault 内循环代谢**:学习产物必入 raw/wiki/output,不滞留 sessions/
- **强制月度迭代**:每次月复盘必改 PLAYBOOK 至少一处
- **主观+客观双评分**:差距本身是盲点信号
- **B 主线 + C 偶尔**:不施压时间线、保留探索弹性
