---
title: Wiki 定时任务记录
type: topic
tags: [meta, schedule, mature]
sources: []
created: 2026-05-10
updated: 2026-05-10
summary: 已设置的定时任务清单与管理方式。
---

# Wiki 定时任务

## 当前活跃任务

### 1. Wiki 周维护 - raw 增量处理

| 项 | 值 |
|---|---|
| **Routine ID** | `trig_01V7TvrnMC5EUtVUhhqXP3a7` |
| **频率** | 每周一 09:00 UTC(周一 21:00 NZ 时间,晚上 9 点) |
| **Cron** | `0 9 * * 1` |
| **仓库** | `https://github.com/Anping2017/obsidian` |
| **模型** | claude-sonnet-4-6 |
| **管理** | https://claude.ai/code/routines/trig_01V7TvrnMC5EUtVUhhqXP3a7 |
| **状态** | ✅ 启用 |

**任务内容**:按 [[WORKFLOW]] 第五节"增量更新流程"处理 raw/ 7 天内改动:
1. find 找近 7 天 raw 改动
2. 按 WORKFLOW §2.2 跳过案例/模板/练习等
3. 概念查重 → 已有 Edit sources / 新增 Write 新 wiki
4. 反查 wikilinks + frontmatter
5. 更新 INDEX.md / PROGRESS.md
6. git commit + push

**单次上限**:新建 ≤30 篇 wiki(超过表示应该手动批量,不是周维护场景)。

---

## 管理操作

### 查看定时任务
跟我说:"列出定时任务" 或访问管理页 https://claude.ai/code/routines

### 暂停/启用
通过管理页修改 enabled 字段,或跟我说:"暂停 wiki 周维护"。

### 调整频率
跟我说:"改成每两周跑一次" 等。

### 立即执行(测试)
跟我说:"立刻跑一次 wiki 周维护"。

### 删除
不能通过 API 删除。需访问 https://claude.ai/code/routines 在 UI 中删除。

---

## 注意事项

### 远程 vs 本地

⚠️ 这是**远程**任务,在 Anthropic 云端运行,**只能访问 GitHub 上的内容**。

要保证有效:
1. **本地 vault 必须定期 push 到 GitHub**(否则远程 agent 看到的是旧版)
2. 远程 agent 的 commit 会推回 GitHub,你要 git pull 拉到本地

### 仓库配置

如果 GitHub 仓库地址不对,跟我说:"改 wiki 周维护的仓库地址为 X",我用 update API 改。

### 失败排查

- agent 报错 → 看管理页的执行历史
- 没有写入 → 可能仓库里 raw/ 没有最新改动(本地未 push)
- 重复创建 → 看 INDEX 是不是同步到 GitHub 了

---

## 历史记录(每次执行后追加)

### 2026-05-11 — Prompt v2 + 时间调整

**Prompt v2 改动**:
- 增加反查 H 项:topic 人物 entity 覆盖检查
- 增加反查 B 项:Python 修空格别名笔误
- 改进异常处理:孤立 wikilinks > 20 时建议手动反查

**时间调整**:
- 原:周一 09:00 NZ(早上)
- 现:**周一 21:00 NZ(晚上 9 点)**,cron `0 9 * * 1`
- 首次自动执行:**2026-05-11 21:03 NZ**(今晚)
