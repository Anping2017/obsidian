---
title: HTML 语义化
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/语言/HTML/03-实践深化层/HTML5语义化/]
created: 2026-05-05
updated: 2026-05-05
summary: HTML 语义化指用合适的标签表达内容含义而非外观,通过 HTML5 引入的 article/section/nav/header 等标签提升 SEO、可访问性与代码可维护性。
---

# HTML 语义化

## 定义

**HTML 语义化** 指在标记文档时,**根据内容的含义**(meaning)选择合适的标签,而非根据外观(presentation)。语义化的反面是"div soup":整页用 `<div>` + class 堆砌。HTML5(2014)正式引入一组新语义标签,标志这一思潮的标准化。

## 核心要点

### 1. HTML5 新增语义标签

| 标签 | 用途 |
|---|---|
| `<header>` | 页面或区块顶部 |
| `<nav>` | 主导航 |
| `<main>` | 主内容区(每页一个) |
| `<article>` | 独立可发布的内容(博文、新闻) |
| `<section>` | 主题分组 |
| `<aside>` | 旁支信息(侧边栏、相关推荐) |
| `<footer>` | 页面或区块底部 |
| `<figure>`/`<figcaption>` | 图片+说明 |
| `<time>` | 机器可读时间 |
| `<mark>` | 高亮文字 |

### 2. 语义化的价值

#### SEO

搜索引擎使用语义标签理解页面结构、提取摘要、识别面包屑。`<article>`、`<time datetime>`、Schema.org JSON-LD 共同提升排名。

#### 可访问性([[ARIA可访问性]])

屏幕阅读器依赖语义标签构建朗读层级:跳过 `<nav>` 直接听 `<main>`、按 heading 跳跃。盲人用户的"地标导航"完全依赖语义。

#### 可维护性

`<nav>` 比 `<div class="nav">` 自解释,新成员接手代码效率更高。

#### 默认样式与行为

`<button>` 自带焦点、回车触发、enter 默认提交;用 `<div onclick>` 模拟需手写键盘支持、role、tabindex,易出错。

### 3. 文档大纲(Document Outline)

HTML5 设想 `<h1>-<h6>` + section 自动生成大纲,但浏览器从未实现。最佳实践仍是显式按文档主题手动维护标题层级,**不要跳级**(h1 → h3)。

### 4. 微数据与 Schema.org

更深层语义:JSON-LD / Microdata / RDFa 标记产品、文章、人物。Google 富片段(Rich Snippet)依赖此。

### 5. 反模式

- 用 `<table>` 做布局(应用 [[CSS Grid]] / [[Flexbox]])
- `<b>` `<i>` 表语义而非样式(用 `<strong>` `<em>`)
- `<br>` 替代段落(用 `<p>`)
- 全 `<div>` + class 标签

### 6. 与 ARIA 的关系

ARIA 是 HTML 语义不足时的补丁。**首要原则:能用语义标签就别加 role**。`<button>` 自带 `role=button`,加 `role=button` 反而冗余。

## 关系

- 基础:[[HTML5与现代Web平台]] 的核心特性
- 提升:SEO 排名(参见 SEO 相关 wiki)
- 增强:[[ARIA可访问性]] 与屏幕阅读器
- 协作:与 [[CSS盒模型]]、[[CSS Grid]] 解耦布局表现
- 工具:[[Lighthouse性能审计]] 检测语义化问题

## 参考源

- raw/计算机/开发学习/语言/HTML/03-实践深化层/HTML5语义化/03-1 语义化设计理念.md
- raw/计算机/开发学习/语言/HTML/03-实践深化层/HTML5语义化/03-2 页面结构语义化.md
