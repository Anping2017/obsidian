# Vault 操作手册

这是给 Claude Code 看的规则文件,定义在这个 vault 里如何工作。

## 目录结构

### 新流程目录(三层信息流:raw → wiki → output)

| 目录 | 用途 | 处理策略 |
|---|---|---|
| `raw/` | 原始输入层。文章摘录、会议记录、灵感、PDF 转 markdown 后的原始素材 | **不要随意修改内容**,只能补 frontmatter |
| `wiki/` | 知识层。一个概念一个文件,经过提炼和结构化,格式见 `SCHEMA.md` | 慎重修改,新建必须符合 SCHEMA |
| `output/` | 输出层。AI 基于 wiki 产出的文章、报告、脚本、摘要 | 可自由更新、可重新生成 |

### 已有目录(历史结构,保留不动)

vault 根目录下的主题文件夹(`AI人工智能/` `计算机/` `经济学/` `哲学/` 等)是已有的笔记,**不要主动整理或移动**。需要重组时由我手动操作或明确指令后才执行。

新写入的内容走 `raw/` `wiki/` `output/` 三层流程。

## frontmatter 规范

每条笔记必须包含五个字段(详见 `SCHEMA.md`):

```yaml
---
title: 标题
tags: [tag1, tag2]
created: YYYY-MM-DD
type: fleeting | literature | permanent
summary: 一句话摘要
---
```

新建笔记**必须**包含完整 frontmatter。补全已有笔记的 frontmatter 是允许的修改。

## 六条设计原则

1. **Markdown 是唯一格式**。PDF / Docx / 音频先转成 .md 再写入 vault,原始文件留在 vault 之外。
2. **保持用词一致**。统一术语见下方「术语表」。
3. **扁平优先**。文件夹只管生命周期,不管主题分类;路径深度不超过 3 层。
4. **每条笔记要有 summary**。一句话讲清楚这条笔记讲什么。
5. **frontmatter 五字段**:title / tags / created / type / summary。
6. **区分人的输入和 AI 的产出**。`raw/` `wiki/` 是人(或人审过)的内容,`output/` 是 AI 生成的衍生内容。

## 术语表

vault 里统一用以下写法,不要混用:

| 统一用 | 不要用 |
|---|---|
| RAG | 检索增强生成 / retrieval augmented generation |
| LLM | 大模型 / 大语言模型 / foundation model |
| Claude Code | CC / claude-code / Anthropic 的编程工具 |
| frontmatter | 元数据 / YAML 头 / 文件头信息 |
| vault | 知识库 / 仓库 |

(后续遇到新概念,请追加到这张表)

## 操作规则

- `raw/` 下的文件是我的原始素材,**未经确认不要修改正文内容**;补 frontmatter 可以。
- `wiki/` 下的文件是经过整理的知识条目,**修改前需说明改动理由**;新建必须符合 `SCHEMA.md`。
- `output/` 下的文件是 AI 衍生内容,可自由更新或覆盖。
- 新建任何笔记都必须包含完整 frontmatter(五字段全填)。
- 创建 `wiki/` 条目时,自动检查正文里出现的概念,如果 vault 里已有对应文件,加上 `[[wikilinks]]`。
- 处理 `raw/` 时如果发现可以提炼为 `wiki/` 条目,**先建议**,不要自动产出。

## AI 自动化提示

当我说「整理某篇 raw 文件为 wiki 条目」时:
1. 读取 `raw/xxx.md`
2. 按 `SCHEMA.md` 的格式输出到 `wiki/概念名.md`
3. frontmatter 的 `created` 填今天的日期
4. `summary` 写一句话,30-80 字
5. 在「来源」节写明 `raw/xxx.md` 的相对路径

当我说「基于 wiki 写一篇 output」时:
1. 检索 `wiki/` 里相关条目(标签、wikilinks、summary 都要扫)
2. 在 `output/` 下新建文件,frontmatter 的 `type: permanent`,`tags` 加 `output`
3. 在文末列出引用了哪些 wiki 条目(用 wikilinks)
