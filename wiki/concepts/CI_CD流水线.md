---
title: CI/CD流水线
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/运维知识/持续集成和持续交付/]
created: 2026-05-05
updated: 2026-05-05
summary: CI 持续把代码变更合并并自动验证,CD 自动交付到生产或类生产环境,流水线把代码到用户的全过程编码为可重复脚本。
---

# CI/CD流水线

## 定义

**持续集成(Continuous Integration,CI)** 指开发者频繁把变更合并到共享主干,每次合并都触发自动构建与测试,尽早发现集成问题。**持续交付(Continuous Delivery,CD)** 指经过 CI 的变更可一键部署到生产或类生产;**持续部署(Continuous Deployment)** 进一步去掉人工按钮,通过自动化全程发布。流水线(Pipeline)是上述过程的可执行编排。

## 核心要点

- **典型阶段**
  1. **触发**:Push、PR、定时、手动。
  2. **静态检查**:Lint、格式、依赖扫描、Secret 扫描。
  3. **构建**:编译、打包、生成构件(JAR、镜像、二进制)。
  4. **测试**:单元 → 集成 → 端到端 → 性能;参考 [[单元测试金字塔]]。
  5. **质量门禁**:覆盖率、漏洞、性能基线达标才放行。
  6. **打包与发布**:推送到制品库(Artifactory、Container Registry)。
  7. **部署**:开发/测试/生产环境,典型用 Helm、Argo CD、Spinnaker。
  8. **观测**:日志、指标、Trace、告警闭环。
- **关键工具生态**
  - **CI 平台**:GitHub Actions、GitLab CI、Jenkins、CircleCI、Buildkite、Drone。
  - **构建**:Maven/Gradle、Bazel、Buck、Turborepo、Nx。
  - **测试**:JUnit/PyTest/Jest 等 + Cypress/Playwright + JMeter/k6。
  - **部署**:Kubernetes + Helm + Argo CD;Terraform/Pulumi 管 IaC。
- **设计原则**
  - **快速反馈**:常用变更链路 < 10 分钟,失败立即通知作者。
  - **失败可重现**:流水线即代码(YAML),容器化执行环境。
  - **零停机部署**:蓝绿、金丝雀、滚动;配合特性开关。
  - **不可变构件**:同一构件穿越所有环境,只换配置。
  - **从开发到生产同源**:工作流统一,差异最小化。
- **进阶**
  - **GitOps**:Git 仓库即真相源,Argo CD/Flux 自动同步集群;参考 [[Kubernetes]]。
  - **Progressive Delivery**:Flagger / Argo Rollouts 自动金丝雀 + 指标回滚。
  - **DORA 四指标**:部署频率、变更前置时间、变更失败率、恢复时间——衡量 DevOps 成熟度。

## 关系

- 与 [[GitFlow与TrunkBased]]:工作流决定流水线触发点。
- 是 [[TDD测试驱动开发]]、[[BDD行为驱动开发]] 的自动化执行场。
- [[Docker容器]]、[[Kubernetes]] 是现代部署目标;镜像构建与推送是流水线核心步骤。
- [[代码评审]]、[[技术债管理]]、[[Web安全]] 都通过流水线门禁强制执行。
- 与 [[监控与告警闭环]] 合作完成"开发-发布-运维"的闭环。

## 参考源

- raw/计算机/运维知识/持续集成和持续交付/
- raw/计算机/运维知识/容器化/
