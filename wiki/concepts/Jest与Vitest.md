---
title: Jest 与 Vitest(JavaScript 测试框架)
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Jest 是 Facebook 推出、长期主导 JavaScript 测试领域的框架,Vitest 是基于 Vite 的现代继任者,以 ESM 原生支持、瞬时启动、与 Vite 生态紧密整合,2023 年后成为新项目主流。
---

# Jest 与 Vitest(JavaScript 测试框架)

## 定义

**Jest** 是 Facebook 在 2014 年开源的 JavaScript 单元测试框架,长期是 React 生态的默认选择。**Vitest** 是 2021 年 Anthony Fu 等人基于 [[Vite]] 推出的新一代测试框架,以"Jest 兼容 API + Vite 性能"成为 2023 年后新项目的事实标准。

二者承担同样角色:**单元测试 + 集成测试 + 快照测试 + Mock + 覆盖率报告**,但底层架构与开发体验差异巨大。

## Jest 的设计与困境

**经典设计**

- Babel 预处理(支持 ES Modules / TypeScript)
- 自实现 Module 系统(Jest Resolver)
- jsdom 环境模拟浏览器
- 内置 Mock、Spy、Snapshot
- 全局 jest 对象

**长期主导**

- React 官方默认
- Create React App 开箱即用
- 大量教程、库以 Jest 为前提

**问题积累**

- ESM 支持长期不完善(转译 + CJS 妥协)
- 启动慢(冷启 5-30 秒)
- TypeScript 配置繁琐(ts-jest 或 Babel)
- 单进程串行执行(后期改 Workers)
- 大型 Monorepo 体验差

## Vitest 的崛起

**2021-2022 引爆**

Vite 生态指数级增长后,社区急需一个不离开 Vite 配置的测试方案。

**核心创新**

- **ESM 原生**:与浏览器同样的模块系统
- **共享 Vite 配置**:vite.config.ts 即测试配置
- **HMR 热更新**:文件修改后毫秒级重跑相关测试
- **Worker 并行**:多核满载
- **Jest 兼容 API**:expect、describe、it、beforeEach 一样写

**性能对比**

| 项目规模 | Jest 启动 | Vitest 启动 |
|---|---|---|
| 100 测试 | 5s | 0.5s |
| 1000 测试 | 30s | 5s |
| 10000 测试 | 5min | 30s |

冷启动差距 10 倍,改动后 Watch 模式更明显。

## 通用 API

```javascript
import { describe, it, expect, beforeEach, vi } from 'vitest'  // 或 'jest'

describe('Calculator', () => {
  let calc
  beforeEach(() => { calc = new Calculator() })

  it('adds two numbers', () => {
    expect(calc.add(1, 2)).toBe(3)
  })

  it('mocks a dependency', () => {
    const mock = vi.fn().mockReturnValue('hello')  // jest.fn()
    expect(mock()).toBe('hello')
  })
})
```

API 90% 相同,迁移工作量极小——这是 Vitest 能快速取代 Jest 的关键。

## 关键功能对比

| 维度 | Jest | Vitest |
|---|---|---|
| 启动速度 | 慢 | 极快 |
| ESM | 部分 | 原生 |
| TS | 需 ts-jest | 原生(esbuild) |
| 配置 | jest.config | vitest.config(共享 Vite) |
| 浏览器测试 | jsdom | jsdom + 实验浏览器模式 |
| 监视模式 | 改文件全测试 | 仅相关测试 |
| 兼容性 | 极广 | 现代项目 |
| Coverage | 内置(istanbul) | v8 / istanbul 可选 |
| 快照 | 内置 | 内置 |
| Snapshot 内容 | toMatchSnapshot | toMatchSnapshot / inline |

## Mock 系统

**Jest**

```javascript
jest.mock('./api', () => ({ fetchUser: jest.fn().mockResolvedValue({}) }))
```

**Vitest**

```javascript
vi.mock('./api', () => ({ fetchUser: vi.fn().mockResolvedValue({}) }))
```

二者都支持:模块 Mock、定时器 Mock、网络 Mock(MSW 配套)、Spy。

## 适用场景

**Jest 仍适合**

- 大型存量项目(迁移成本高)
- React Native(默认配套)
- Babel 主导的工具链
- Node CommonJS 模块

**Vitest 推荐**

- Vite / Vue / SvelteKit 项目
- 全 ESM TypeScript 项目
- 新建项目
- Monorepo
- 追求极速反馈循环

## 与 Mocha / Jasmine / 其他对比

| 测试框架 | 风格 | 现状 |
|---|---|---|
| Jest | 全家桶 | 主流但被 Vitest 蚕食 |
| Vitest | 全家桶 + Vite | 新主流 |
| Mocha + Chai + Sinon | 组合式 | 老牌,Node 后端用得多 |
| Jasmine | 全家桶 | Angular 默认 |
| AVA | 极简并行 | 小众但忠诚用户 |
| Tape | 极简 | TAP 输出,衰落 |
| Bun test | 内置 | Bun 用户首选 |

## 关键工具配套

**测试库(与 Jest/Vitest 都兼容)**

- @testing-library/react、@testing-library/vue:DOM 测试
- MSW(Mock Service Worker):HTTP 拦截
- Faker:测试数据生成
- @vue/test-utils、vue-test-utils:Vue 专用
- happy-dom:轻量 jsdom 替代

**端到端补充**

- Playwright:跨浏览器([[Playwright]])
- Cypress:浏览器 E2E([[Cypress]])
- Puppeteer:Headless Chrome

## 测试组织最佳实践

**测试金字塔(参考 [[单元测试金字塔]])**

- 单元(Jest/Vitest):大量、毫秒级
- 集成(Jest/Vitest + MSW):中等
- E2E(Playwright):少量、关键路径

**目录约定**

- foo.ts + foo.test.ts(并列)
- 或 __tests__/foo.test.ts
- 测试与源码同仓 = 维护成本低

## 局限

- Jest 在 ESM/TS 时代积累技术债
- Vitest 生态相对新,某些 jest-* 插件未迁移
- 浏览器真实环境仍需 Playwright/Cypress 补充
- 性能/网络压测不是单元测试范畴
- 异步、并发、定时测试仍易出错

## 和其他概念的关系

Jest/Vitest 是 [[TDD测试驱动开发]] 与 [[BDD行为驱动开发]] 实践的核心工具。它们与 [[CI_CD流水线]] 紧密结合——每次 PR 自动跑全套测试,与 [[GitFlow与TrunkBased]] 工作流互锁。

测试覆盖率(Coverage)由 v8 / istanbul 提供,接入 SonarCloud、Codecov 等代码质量平台。Mock 思路与 [[设计模式]] 中的依赖注入、[[设计原则SOLID]](尤其依赖倒置)深度一致——可测性是好设计的副产品。

Vitest 的兴起反映了 [[Vite]] 取代 Webpack 后的工具链统一趋势,与 [[包管理器对比]] 中 pnpm 取代 npm 的故事同构。

## 参考源

- raw/计算机/
- 相关:[[TDD测试驱动开发]]、[[Vite]]、[[单元测试金字塔]]
