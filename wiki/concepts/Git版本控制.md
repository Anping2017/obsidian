---
title: Git 版本控制
type: concept
tags: [cs, programming, mature]
sources:
  - raw/计算机/开发学习/语言/Javascript/03-应用实践层/04-工程化/04-版本控制(Git).md
created: 2026-05-05
updated: 2026-05-05
summary: Git 是分布式版本控制系统,以快照而非 diff 存储项目历史,通过提交、分支、合并支撑现代协作开发,是工程基础设施核心。
---

# Git 版本控制

## 定义

**Git** 是 Linus Torvalds 2005 年因 Linux 内核开发需要而创建的**分布式版本控制系统(Distributed Version Control System, DVCS)**。它跟踪文件随时间的变化,允许多人协作、回溯历史、并行实验、合并改动。

与早期的 SVN、CVS(集中式)不同,Git 每个工作副本(clone)都是完整仓库,**无需中心服务器即可提交、查阅历史、创建分支**。

## 核心要点

### 数据模型:快照而非差异

Git 把项目每次提交视为整个文件系统的**快照**,通过哈希(SHA-1/SHA-256)指纹引用,变化部分才存,未变部分共享指针。
这与 SVN 的"按文件存储增量"模型根本不同,使分支与历史操作极快。

### 三大对象类型(Merkle DAG)

- **Blob**:文件内容
- **Tree**:目录,引用 Blob 和子 Tree
- **Commit**:指向一个 Tree,加父 commit、作者、消息

整个 Git 仓库就是基于 SHA 的内容寻址 Merkle DAG。

### 三个区域

- **工作区(Working Directory)**:实际文件
- **暂存区(Staging / Index)**:`git add` 后等待提交
- **本地仓库(Local Repo)**:`git commit` 后入历史

加上**远程仓库(Remote)**,共四个层次。

### 核心命令

| 命令 | 作用 |
|---|---|
| git init / clone | 创建/拉取仓库 |
| git add | 暂存改动 |
| git commit | 写入本地历史 |
| git status / diff / log | 查看状态/差异/历史 |
| git branch / checkout / switch | 分支管理 |
| git merge / rebase | 合并/变基 |
| git fetch / pull / push | 远程同步 |
| git tag | 标记版本 |
| git stash | 暂存未完成改动 |
| git cherry-pick | 摘取特定提交 |
| git reset / revert | 回退/反提交 |
| git reflog | 引用日志,救命神器 |

### 分支 = 廉价指针

Git 分支只是指向某个 commit 的**指针**,创建/切换近乎零成本。这与 SVN 复制整个目录的"分支"形成对比。
分支模型是 Git 的灵魂,催生了多种工作流。

### 主流分支策略

- **Git Flow**(Vincent Driessen):master / develop / feature / release / hotfix。复杂但严谨
- **GitHub Flow**:只有 main + feature 分支,持续部署友好。简单
- **Trunk-Based Development**:所有人短分支或直 push main,频繁合并。Google/Facebook 的内部模式
- **GitLab Flow**:介于两者间

小团队推荐 GitHub Flow + 短期 feature 分支 + Pull Request 审查 + CI 自动测试。

### Merge vs Rebase

- **merge**:保留分支历史,产生合并提交。安全,适合公共分支
- **rebase**:把 feature 分支提交"重放"到 main 之后,得到线性历史。整洁,但**不要 rebase 已推送的公共分支**

经验法则:在自己的 feature 分支用 rebase 整理,推送公共分支后只用 merge。

### 冲突解决

`git merge` 或 `rebase` 时若同一文件同一行被双方修改,Git 标记冲突由人解决。
工具:VSCode 内置 diff、`git mergetool`、IntelliJ。

### 远程平台

- **GitHub**:最大的开源协作平台,Pull Request、Actions(CI)、Issues
- **GitLab**:自托管首选,内置 CI/CD
- **Bitbucket**、**Gitea**、**Gitee**

### 高级特性

- **submodule / subtree**:嵌套仓库
- **hooks**:本地自动化(pre-commit、commit-msg 等)、配合 husky 实现 lint/format
- **bisect**:二分查找定位引入 bug 的 commit
- **worktree**:多分支并行检出
- **partial clone / sparse checkout**:大仓库优化
- **LFS**:大文件存储(图片、模型)

### Git 哲学

- **不可变历史**:已发布的 commit 通常不删不改(reset --hard 慎用)
- **小而频的提交**:每个 commit 表达一个原子改动,信息量最大
- **写好 commit message**:Why > What。约定式提交(feat:/fix:/docs:)便于自动生成 changelog

## 和其他概念的关系

Git 是软件工程基础设施核心,贯穿 CI/CD、code review、issue 跟踪、自动化部署。GitHub Actions、GitLab CI、CircleCI 等基于 Git 事件触发流水线。

底层依赖[[Hash表]]、Merkle [[树]]、SHA 哈希、压缩算法。`git log --graph` 展示的是 commit DAG([[图]] DFS 拓扑)。`git blame` 是逐行历史追溯。

DevOps、GitOps(用 Git 作为基础设施真理之源,Argo CD 自动同步 K8s)、文档即代码(Docs as Code)等理念都依赖 Git。它已超越版本控制,成为软件协作的通用底座。

## 参考源

- raw/计算机/开发学习/语言/Javascript/03-应用实践层/04-工程化/04-版本控制(Git).md
