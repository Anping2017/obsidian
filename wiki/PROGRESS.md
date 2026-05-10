---
title: Wiki 状态跟踪器
type: topic
tags: [meta, progress, mature]
sources: []
created: 2026-05-05
updated: 2026-05-10
summary: vault 当前状态、未完成事项、下次维护计划。历史轮次详情见 CHANGELOG.md。
---

# Wiki 状态跟踪器

> **最后更新**:2026-05-10
> **历史日志**:见 [[CHANGELOG]]
> **工作流**:见 [[WORKFLOW]]

---

## 当前状态

### 规模

| 类别 | 数量 |
|---|---|
| **总 wiki** | **1545** |
| concepts | 1401 |
| topics | 50 |
| entities | 94 |
| INDEX.md | 2713 行 |
| mature | 1431(92.6%) |
| stub | 114(7.4%) |

### 学科分布

| 学科 | 词条数 | 状态 |
|---|---|---|
| 计算机科学 | 284 | ✅ 充分 |
| 营销与SEO | 245 | ✅ 充分 |
| 金融学 | 163 | ✅ 充分 |
| 思维模型 | 123 | ✅ 充分 |
| 商业管理 | 119 | ✅ 充分 |
| AI与机器学习 | 115 | ✅ 充分 |
| 工具与生活 | 106 | ✅ 充分 |
| 经济学 | 93 | ✅ 充分 |
| 英语 | 93 | ✅ 充分 |
| 哲学 | 82 | ✅ 充分 |
| 心理学 | 77 | ✅ 充分 |
| 会计学 | 45 | ⚠️ 偏少(可补强) |

### raw 覆盖率

| 维度 | 数据 |
|---|---|
| raw 总文件 | 4583 |
| 被 wiki sources 引用 | ~750(16%) |
| 已概念覆盖率(估算) | ~85%(核心概念基本全 wiki) |
| 空文件(0 字节) | 395 |
| 案例/模板/练习等已跳过 | ~3000 |

---

## 未完成事项

### P0(必做)

- [x] **设置每周定时任务**:✅ Routine `trig_01V7TvrnMC5EUtVUhhqXP3a7`,每周日 21:00 UTC(周一 09:00 NZ 时间),详见 [[schedule]]
- [ ] **首次 git commit**:1545 篇 wiki + 5 个 meta 文件(INDEX/PROGRESS/WORKFLOW/CHANGELOG/schedule)归档到 git
- [ ] **GitHub 同步**:确认本地 vault 已 push 到 `https://github.com/Anping2017/obsidian`,否则定时任务跑空

### P1(应做)

- [ ] **会计学补强**:仅 45 篇,可加 20-30 篇(国际会计/政府会计/特殊行业会计)
- [ ] **stub 升级**:114 个 stub 中,引用 ≥3 次的应升级为 mature(估计 30 个)
- [ ] **scripts/ 工具脚本**:把反查逻辑固化为 `scan_orphans.py`、`audit_quality.py`

### P2(可做)

- [ ] **output/ 层启动**:基于 wiki 写综述/学习路径(如《如何学金融》《AI 应用全景》)
- [ ] **跨域桥接补强**:还有未连的对子(outdoor↔business、ios↔ai 等小众组合)
- [ ] **生命/兴趣域扩展**:用户可能后续添加新的 raw 域(如健康、烹饪、艺术、旅行等)

### P3(等用户决定)

- [ ] **CLAUDE.md 更新**:vault 根的 CLAUDE.md 仍只描述 raw/wiki/output 三层,需同步本工作流体系
- [ ] **stub 全清理**:把 114 个 stub 全升级或合并到既有 mature

---

## 增量维护机制

### 自动触发(每周)

- **Cron**:每周一 09:00 触发增量扫描
- **配置**:见 `wiki/schedule.md`(待建)
- **流程**:见 [[WORKFLOW]] 第五节"增量更新流程"

### 手动触发

跟我说:
- "处理 raw 最新改动" → 增量扫描
- "做 wiki 反查" → 跑反查脚本
- "升级 stub" → 把高引用 stub 升级
- "重写 INDEX" → INDEX 重新生成

---

## 关键文件清单

| 文件 | 用途 | 是否要读 |
|---|---|---|
| `SCHEMA.md`(根目录) | 文件格式规范 | 每次必读 |
| `CLAUDE.md`(根目录) | vault 操作手册 | 每次必读 |
| `wiki/WORKFLOW.md` | **处理 raw 的 SOP** | **每次必读** |
| `wiki/INDEX.md` | 全局索引 | 处理前查重 |
| `wiki/PROGRESS.md`(本文件) | 状态跟踪 | 处理前看计划 |
| `wiki/CHANGELOG.md` | 历史日志 | 仅参考 |
| `wiki/schedule.md` | 定时任务清单 | 配置或暂停时看 |

---

## 工作模式速查

| 你说 | 我做 |
|---|---|
| "处理 raw 最新改动" | 跑增量流程(WORKFLOW §5) |
| "做反查" | 跑反查项目清单(WORKFLOW §4) |
| "升级 stub" | 找高引用 stub 改 mature |
| "重写 INDEX" | 派 agent 重写 |
| "新增 X 域 wiki" | 派 1-3 agent 处理新域 |
| "git commit" | 创建 commit + push |
| "查工作流" | 读 WORKFLOW.md 给你看 |

---

## 健康指标(每次维护后更新)

- [ ] frontmatter 100% 合规
- [ ] type/目录 100% 一致
- [ ] 0 空格笔误 wikilinks
- [ ] 跨域桥接 ≥12 对
- [ ] stub 占比 < 10%
- [ ] INDEX 与实际同步
- [ ] git 已归档

(对号填上的话,vault 健康)
