---
title: GitFlow与TrunkBased
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: GitFlow 用多分支管理发布周期、TrunkBased 用单主干持续集成,两者代表了重发布周期 vs 高频部署两种工作流哲学。
---

# GitFlow与TrunkBased

## 定义

**GitFlow** 是 Vincent Driessen 2010 年提出的 Git 分支模型,用 master、develop、feature、release、hotfix 多类分支管理软件发布周期。**Trunk-Based Development(TBD,主干开发)** 主张所有人在单一主干频繁提交,通过特性开关、CI/CD 自动验证保证主干始终可发布,与持续部署天然兼容。

## 核心要点

- **GitFlow**
  - **master**:生产代码,只接受 release/hotfix 合并,打 tag 即版本。
  - **develop**:集成分支,所有 feature 合到这。
  - **feature/X**:从 develop 拉,完成后合回 develop。
  - **release/vX**:发布稳定化分支,只允许 bug 修复;完成后双合到 master 与 develop。
  - **hotfix/X**:从 master 拉急修,合回 master + develop。
  - 适合:版本化产品、桌面客户端、嵌入式、企业季度发布、严格变更管理。
  - 缺点:分支多、合并冲突频繁;对持续部署不友好。
- **Trunk-Based Development**
  - 单 main(trunk)分支;short-lived feature branches < 1-2 天或直接在 trunk 上提交。
  - **Feature Flag**:未完成功能用开关隐藏,trunk 始终可发布。
  - 大改用 **Branch by Abstraction** 而非长生命分支。
  - 自动化测试 + Code Review 保证质量,持续合并防止漂移。
  - 适合:Web 服务、SaaS、持续部署 / 持续交付;Google、Facebook、Netflix 主流。
- **关键差异**
  - **集成频率**:TBD 每天多次,GitFlow 一周到几周。
  - **分支寿命**:TBD < 24h,GitFlow 数天到数周。
  - **合并冲突**:TBD 小而多,GitFlow 大而少。
  - **复杂度**:GitFlow 流程明晰但分支多,TBD 流程简单但工程基础设施要求高。
- **混合实践:GitHub Flow**
  - 折中——main + 短命 feature branch + PR;不强制 develop/release。
  - 适合大多数 Web 团队,介于 GitFlow 与 TBD 之间。

## 关系

- 是 [[Git版本控制]] 在团队协作层的工作流选型。
- 与 [[CI_CD流水线]] 强相关——TBD 几乎要求成熟 CI/CD。
- [[代码评审]] 是 PR/MR 流程的核心环节,影响合并速度。
- 特性开关(Feature Flag)与 [[A_B测试]]、灰度发布相关。
- 选型受 [[技术债管理]] 与团队规模影响——大团队、单仓 monorepo 更倾向 TBD。

## 参考源

- raw/计算机/(版本控制与协作主题分散)
