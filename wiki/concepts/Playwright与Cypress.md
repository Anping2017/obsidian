---
title: Playwright 与 Cypress(端到端测试)
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Playwright 是微软推出的多浏览器现代 E2E 测试工具,Cypress 是开发者体验导向的浏览器内运行框架;前者覆盖广、并行强,后者直观易学,二者代表当前端到端测试两条主流路径。
---

# Playwright 与 Cypress(端到端测试)

## 定义

**端到端(End-to-End,E2E)测试** 在真实浏览器中模拟用户操作,验证完整功能链路——从前端 UI、API、后端、数据库的整体行为。

- **Playwright**(2020,Microsoft):一组 Puppeteer 团队转投微软后推出的多浏览器、多语言 E2E 框架
- **Cypress**(2015):基于浏览器的 JavaScript 测试运行器,以"开发者友好"著称

二者取代了 Selenium 在新项目中的位置——后者仍主导企业测试自动化,但工程体验落后。

## Playwright 的设计

**多浏览器支持**

- Chromium、Firefox、WebKit(Safari 内核)
- 同一份测试跨三浏览器跑
- 比 Cypress 多了 Firefox 与 Safari

**多语言绑定**

- TypeScript / JavaScript(主)
- Python、.NET、Java
- 可与 PyTest、JUnit、xUnit 等集成

**关键特性**

- **Auto-waiting**:自动等待元素可点击 / 可见,减少 sleep
- **Network 拦截**:Mock API 响应
- **Trace Viewer**:回放每一步,带 DOM、网络、控制台
- **Codegen**:浏览器中点击,自动生成测试代码
- **并行 + 分片**:CI 上多核满载
- **多 Tab、多窗口、多设备(模拟移动)**

## Cypress 的设计

**浏览器内运行**

- 测试代码与被测页面同进程运行
- DevTools 即测试调试工具
- 时间旅行(Time Travel):每个命令的快照可点回放

**直观语法**

```javascript
describe('Login', () => {
  it('logs in with valid creds', () => {
    cy.visit('/login')
    cy.get('input[name=email]').type('alice@example.com')
    cy.get('input[name=password]').type('secret123')
    cy.contains('Sign in').click()
    cy.url().should('include', '/dashboard')
  })
})
```

链式 cy.* API,自动重试,流畅可读。

**限制**

- 只支持 Chromium / WebKit / Firefox(2022 后扩展,但仍弱于 Playwright)
- 不能跨域(单源安全限制),需 cy.origin() 解决
- 不能多 Tab(2023 后实验性支持)
- 单线程并行(收费 Dashboard 解决跨机器分片)

## Playwright vs Cypress 对比

| 维度 | Playwright | Cypress |
|---|---|---|
| 浏览器 | Chromium/Firefox/WebKit | Chromium/Firefox/WebKit |
| 并行 | 原生强 | 单机弱,需 Cloud |
| 速度 | 快 | 中 |
| 多 Tab | 是 | 实验性 |
| 跨域 | 原生 | cy.origin() 解决 |
| API 拦截 | 强 | 强 |
| Trace | 视频 + Trace Viewer | Time Travel 内嵌 |
| DX | 良好 | 优秀 |
| 学习曲线 | 中 | 低 |
| 开源协议 | Apache 2 | MIT(测试免费,Cloud 付费) |
| 主导 | 微软 | Cypress.io |
| 价格 | 完全免费 | 测试免费,云协作付费 |

整体趋势:**Playwright 在新项目中份额超越 Cypress**(2023 后),特别是企业用户因多浏览器、并行能力转投。Cypress 在小团队、快速开发场景仍受欢迎。

## 通用测试模式

**Page Object Model(POM)**

把页面抽象成对象,封装定位器与操作:

```typescript
class LoginPage {
  constructor(private page) {}
  async login(email, password) {
    await this.page.fill('[name=email]', email)
    await this.page.fill('[name=password]', password)
    await this.page.click('button[type=submit]')
  }
}
```

测试代码用 LoginPage,UI 改了只改一处。

**Fixtures / Hooks**

- beforeEach 重置数据库
- 测试间互相独立
- 使用 API 直接登录而非 UI(节省时间)

**Visual Testing**

- screenshot 比对
- 配合 Percy、Chromatic 做视觉回归

**Accessibility 检查**

- @axe-core/playwright、cypress-axe
- 自动化 WCAG 检查

## 与 Selenium 对比

Selenium 是元老级 E2E 工具(2004 起),仍是企业测试自动化主流,但工程体验落后:

| 维度 | Playwright | Selenium |
|---|---|---|
| 等待 | 自动 | 显式 wait |
| 速度 | 快 | 慢(WebDriver 协议) |
| 安装 | 一行 | 需配 Driver |
| 多语言 | 4 种 | 极多 |
| 现代 API | 优 | 老旧 |
| 企业生态 | 中 | 大 |

新项目首选 Playwright;遗留项目 Selenium 还在跑。

## CI / CD 集成

**GitHub Actions 示例**

```yaml
- uses: actions/setup-node@v3
- run: npm ci
- run: npx playwright install --with-deps
- run: npx playwright test
- uses: actions/upload-artifact@v3
  if: failure()
  with:
    name: playwright-report
    path: playwright-report/
```

E2E 失败时上传 trace.zip,用 Trace Viewer 复盘。

## 测试金字塔位置

参照 [[单元测试金字塔]]:
- 顶层(数量最少):E2E(Playwright/Cypress)
- 中层:集成测试([[Jest与Vitest]]、[[PyTest]] + MSW)
- 底层:单元测试

E2E 价值:验证关键路径(注册、支付、关键转化漏斗);代价:运行慢、易碎、调试难。**保留 10-20 个核心 E2E 测试**优于 200 个脆弱测试。

## 常见挑战

**1. Flaky Test(碎片测试)**

时序敏感测试偶发失败:
- 修复:auto-wait、消除 sleep、独立测试数据
- 容忍:retry 1-2 次,但要监控 flaky 率

**2. 测试数据**

- 选项 A:独立测试库,每次清空
- 选项 B:每个测试创建唯一数据(随机后缀)
- 选项 C:固定 Seed 数据,测试只读

**3. 第三方依赖**

- Stripe / 支付:用 Sandbox 模式
- 邮件验证:用临时邮箱 API(MailHog)
- 短信:Mock 网关
- 时间:Time freezer / mock Date

## 局限

- 维护成本是单元测试的 10-100 倍
- 跑全套 E2E 几十分钟
- Mock 与真实平衡难
- 第三方变化导致测试碎裂
- 团队需有专门 QA 投入

## 和其他概念的关系

Playwright/Cypress 是 [[CI_CD流水线]] 中"上线前最后一道关卡"。它们与 [[TDD测试驱动开发]]、[[BDD行为驱动开发]] 互补——TDD 自下而上写单元,E2E 自上而下验证用户旅程。

E2E 测试常对接 [[AB测试]] 平台、[[GA4配置]] 等分析工具校验埋点是否触发。可访问性测试([[ARIA可访问性]])可作为 E2E 测试套件的一部分自动化。

在 [[微服务]] 体系下,E2E 跑得最慢但价值最高——单元测试无法覆盖跨服务调用真实表现。Contract Testing(Pact 等)是 E2E 之外的中间方案。

## 参考源

- raw/计算机/
- 相关:[[Jest与Vitest]]、[[PyTest]]、[[单元测试金字塔]]
