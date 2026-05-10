---
title: Sessions 目录说明
type: topic
tags: [meta, learning-system]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: 本目录存放每次学习会话(session)的日志文件。命名格式 YYYY-WW-<mode>-<topic>.md。
---

# Sessions

每次学习会话的日志。

## 命名格式

`YYYY-WW-<mode>-<topic>.md`

例:
- `2026-W19-A-finance.md`(2026 年第 19 周,Mode A 诊断金融学)
- `2026-W19-D-job-offer-decision.md`(Mode D 工作 offer 决策)
- `2026-W19-F-llm-emergence.md`(Mode F 自由提问 LLM 涌现)

## frontmatter 模板

完整模板见 [PLAYBOOK.md](../PLAYBOOK.md) "全局术语 — sessions 文件 frontmatter 通用模板"。

必含字段:
- `mode`(A-F)
- `date`、`duration_min`、`topic`
- `wikilinks_touched`
- `self_rating`(1-5)
- **`vault_changes`** 含 4 子字段(raw_added / wiki_added / wiki_updated / output_added)
- `follow_ups`

## 不要

- ❌ **不在本目录写知识资产**(知识应入 raw/wiki/output)
- ❌ 不删除历史 session(月复盘归档,但保留)
- ❌ 不混用 mode(一个 session 文件对应一个 mode)
