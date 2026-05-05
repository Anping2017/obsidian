# Wiki Schema
# 命名规范
- 概念页：`concepts/概念名.md`（用中文和英文，多词用连字符）
- 例：`concepts/retrieval-augmented-generation.md`
- 实体页：`entities/实体名.md`（人名用中文+英文全名）
- 例：`entities/andrej-karpathy.md`
- 主题页：`topics/主题描述.md`
- 例：`topics/ai-knowledge-management-tools.md`
# Frontmatter 模板
每篇wiki文章必须包含：
```yaml
-
title: 文章标题
type: concept | entity | topic
tags: [标签1, 标签2]
sources: [raw/中的源文件路径]
created: YYYY-MM-DD
updated: YYYY-MM-DD
summary: 一句话摘要
-
```
# 标签体系
- 领域标签：#ai, #programming, #product, #business, #finance
- 状态标签：#stub（存根，需扩充）, #mature（成熟）
- 不要自创新的顶级标签，如有需要先更新本文件
# Wikilink 规则
- 首次提到某个已有wiki页面的概念时，用[[链接]]
- 同一篇文章中同一个概念只链接第一次
- 如果提到的概念没有wiki页面，创建一个stub
# 文章结构
概念页：定义 → 核心要点 → 和其他概念的关系 → 参考源
实体页：简介 → 关键贡献 → 相关概念/实体 → 参考源
主题页：概述 → 多角度分析 → 结论 → 参考源
# 全局索引
每次新增或修改wiki文章后，更新 wiki/INDEX.md
INDEX.md 按分类列出所有wiki页面及一句话摘要
