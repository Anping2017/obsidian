---
title: Reviews 目录说明
type: topic
tags: [meta, learning-system]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: 本目录存放周复盘(weekly)和月复盘(monthly)文档。
---

# Reviews

## 命名格式

- 周复盘:`YYYY-WW-weekly.md`(例 `2026-W19-weekly.md`)
- 月复盘:`YYYY-MM-monthly.md`(例 `2026-05-monthly.md`)

## 周复盘:Claude 主导,你只读

由 Claude 在每周日(或用户说"周复盘"时)自动生成,基于本周 sessions/ 文件汇总:

- 本周 session 数与 mode 分布
- **本周 vault 产物清单**(raw/wiki/output 增量)
- 涉及学科分布
- 一个亮点(最有创造性的连接/分析)
- 一个警惕(模式僵化、避难所、刷分倾向)
- 下周 2-3 个建议(关联具体 mode)

阅读时长:15 分钟。

## 月复盘:对话形式,你 + Claude 共评

每月最后一周或用户说"月复盘"时触发。对话 30-45 分钟。

流程:

1. 本月 session 概览(数量、mode 分布、累计时长)
2. **本月 vault 代谢报告**:
   - raw 新增 N 篇 / wiki 新增 N 篇 / wiki 升级 N 篇 / output 新增 N 篇
   - stub 比例变化
3. DASHBOARD 重打主观分(用户),Claude 提供客观对照
4. 三个反思问题:
   - 哪种 mode 最有价值?为什么?
   - 哪种 mode 没用上或感觉无聊?为什么?
   - 你最强烈的"想深入但还没深入"的方向?
5. **强制修订 PLAYBOOK 至少一处**(增删步骤、调整时长、新增 mode、改判定原则等)
6. 写入 [CHANGELOG.md](../CHANGELOG.md),版本号 +0.01 或 +0.1
7. 写入 [DASHBOARD.md](../DASHBOARD.md) 更新主观字段与全局健康指标的"上月变化"列

## 不要

- ❌ 不在 reviews/ 写非复盘内容
- ❌ 不跳过月复盘的强制 PLAYBOOK 修订(系统僵化的开始)
- ❌ 不在月复盘讨论里同时跑 mode(复盘是元层,与执行层分开)
