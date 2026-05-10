---
title: Selenium
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Selenium 是 2004 年起发展的浏览器自动化标准工具,通过 WebDriver 协议控制真实浏览器,长期主导企业 E2E 测试市场,虽被 Playwright/Cypress 在 DX 上超越,但仍是测试自动化、爬虫、机器人流程自动化(RPA)的根基。
---

# Selenium

## 定义

**Selenium** 是 2004 年由 Jason Huggins 在 ThoughtWorks 发起的浏览器自动化框架。它是当代 Web 自动化的元老,通过 **WebDriver 协议** 控制真实浏览器(Chrome、Firefox、Safari、Edge),曾是企业测试自动化、网页爬虫、机器人流程自动化(RPA)领域的事实标准。

虽然 [[Playwright与Cypress]] 等现代工具在开发者体验上超越了它,Selenium 仍占据企业级、跨语言、长期项目的主流位置。

## 历史与版本

**Selenium 1 / Selenium RC(2004-2014)**

- Jason Huggins 早期实现
- 客户端 / 服务端(Java)架构
- JavaScript 注入控制浏览器
- 与 IE / Firefox 浏览器接口

**WebDriver(2008+)**

- Simon Stewart 重新设计的协议
- 与浏览器原生通信(更稳定)
- 后被 W3C 标准化

**Selenium 2(2011)**

- Selenium RC + WebDriver 合并

**Selenium 3(2016)**

- 默认 WebDriver

**Selenium 4(2021+)**

- W3C WebDriver Protocol
- BiDi(Bidirectional)协议(双向通信)
- DevTools Protocol 集成
- 现代化 API

## 核心架构

```
测试代码(Java/Python/JS/...)
       │
       │ WebDriver client
       │
       │ HTTP/JSON or W3C WebDriver
       │
   Browser Driver(chromedriver、geckodriver)
       │
       v
   真实浏览器
```

**Browser Driver**

每个浏览器有专门驱动:
- chromedriver
- geckodriver(Firefox)
- safaridriver(macOS 内建)
- msedgedriver

需保证 driver 与浏览器版本匹配(常见痛点)。

## 多语言绑定

Selenium 是少数真正多语言的测试工具:
- **Java**:最早,生态最强
- **Python**:简洁,爬虫流行
- **JavaScript / Node**:WebdriverIO
- **C#**
- **Ruby**
- **Kotlin**
- **PHP** (社区)

API 大同小异。

## Python 示例

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://example.com")

# 找元素
search = driver.find_element(By.NAME, "q")
search.send_keys("Hello")
search.submit()

# 等待
result = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "results"))
)

print(result.text)
driver.quit()
```

## 定位器(Locator)

- By.ID:id
- By.NAME:name 属性
- By.CLASS_NAME
- By.TAG_NAME
- By.LINK_TEXT、By.PARTIAL_LINK_TEXT
- By.CSS_SELECTOR(主流)
- By.XPATH(强但慢、易碎)

CSS 选择器是首选——快、可读、稳定。XPath 仅在 CSS 无法表达时(如基于文本)使用。

## 等待策略

**1. 显式等待(推荐)**

```python
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(...))
```

直到条件满足或超时。

**2. 隐式等待**

```python
driver.implicitly_wait(10)
```

所有 find_element 调用都最多等 10s。简单但与显式等待混用易乱。

**3. 不要 sleep**

```python
time.sleep(3)  # 反模式
```

时序敏感、慢、易碎。Always 用显式等待。

## Page Object Model(POM)

把页面抽象成对象,封装定位器与操作:

```python
class LoginPage:
    URL = "https://example.com/login"

    def __init__(self, driver):
        self.driver = driver
        self.email = (By.ID, "email")
        self.password = (By.ID, "password")
        self.submit = (By.CSS_SELECTOR, "button[type=submit]")

    def open(self):
        self.driver.get(self.URL)

    def login(self, email, password):
        self.driver.find_element(*self.email).send_keys(email)
        self.driver.find_element(*self.password).send_keys(password)
        self.driver.find_element(*self.submit).click()
```

测试代码用 LoginPage,UI 改了只改一处。POM 是 Selenium 工程化关键。

## Selenium Grid

分布式 Grid 跑测试:

```
Hub(Master)
   ├── Node 1:Chrome、Firefox
   ├── Node 2:Edge
   └── Node 3:Safari(macOS)
```

测试代码连 Hub,Hub 分发到合适 Node。

**云 Grid**

- BrowserStack、Sauce Labs、LambdaTest
- 几千种浏览器 / OS 组合
- 按使用付费

**Docker 化**

selenium/standalone-chrome、selenium/hub + node 镜像,docker-compose 一行起。

## Selenium 与 Playwright 对比

| 维度 | Selenium | [[Playwright与Cypress]] |
|---|---|---|
| 起源 | 2004 | 2020 |
| 协议 | WebDriver(W3C) | CDP(Chrome 协议) + WebDriver BiDi |
| Auto-wait | 弱 | 强 |
| 速度 | 慢 | 快 |
| API | 老旧 | 现代 |
| 调试工具 | 无内置 | Trace Viewer 极强 |
| 多语言 | 真多语言 | TS/JS/Python/.NET/Java |
| 社区 | 大 | 增长快 |
| 企业适用 | 主流 | 增多 |
| 成本 | 0(开源) | 0 |

新项目选 Playwright;遗留项目仍用 Selenium。

## 测试外的 Selenium 应用

**1. 网页爬虫**

JavaScript-heavy 网站(SPA、Cloudflare 防护)curl/requests 拿不到数据,Selenium 真浏览器渲染后取:

```python
driver.get(url)
WebDriverWait(driver, 10).until(EC.presence_of_element_located(...))
data = driver.find_element(By.ID, "data").text
```

但慢且消耗资源。Playwright 也是这个角色。

**2. RPA(机器人流程自动化)**

UiPath、Automation Anywhere 部分基于 Selenium。Web 自动化业务流程。

**3. 性能测试初步**

跑用户场景看真实页面性能(配 Lighthouse、Web Vitals)。

**4. 截图监控**

定时跑、截图、比对(视觉回归)。

## 反模式

**1. 不维护 driver 版本**

chromedriver 与 Chrome 版本不匹配,测试随机失败。
- WebDriverManager(Java)、webdriver-manager(Python)自动管理
- Selenium 4 起 SeleniumManager 内置

**2. 时序依赖**

到处 sleep(N) 而不是 WebDriverWait。脆弱。

**3. 测试间共享状态**

一个测试登录、下个测试假设已登录,失败时雪崩。

**4. 巨型测试**

50 步测试覆盖整个流程,中间一步挂全失败。拆为小测试。

**5. UI 抓取替代 API**

爬虫该用 API 时硬上 Selenium,慢 100 倍。

## 局限

- API 老旧,需写大量样板代码
- 同步阻塞设计(对比 Playwright async)
- Driver 版本管理痛
- Auto-wait 弱
- 调试视频 / Trace 需第三方
- 多浏览器同时支持但都不如 Playwright 流畅

## 部署 / CI

```yaml
# GitHub Actions
- uses: actions/setup-python@v4
- run: pip install selenium pytest
- run: |
    sudo apt-get install chromium-browser chromium-chromedriver
    pytest tests/
```

或用 Selenium Docker:
```yaml
services:
  selenium:
    image: selenium/standalone-chrome
    ports:
      - "4444:4444"
```

## 现代 Selenium(2024+)

Selenium 4 改进:
- W3C WebDriver Protocol 标准
- BiDi 双向通信(类似 CDP)
- Selenium Manager 自动管理 driver
- Relative Locators(above、below、leftOf)
- 更友好的 API

但生态惯性大,企业从 Selenium 迁 Playwright 仍缓慢。

## 和其他概念的关系

Selenium 是 [[Playwright与Cypress]]、Puppeteer、TestCafe 等现代浏览器自动化工具的精神先驱,定义了 WebDriver 协议这一行业标准。它与 [[CI_CD流水线]]、[[单元测试金字塔]] 中的 E2E 层紧密配合。

它的多语言支持让"大企业测试团队 + 开发团队不同语言"也能协作,与 [[Postman与Insomnia]] 一样代表"通用工具适配各种工程文化"的产品哲学。

它在 RPA、爬虫、监控等非测试场景的延伸,展示了"测试工具 → 通用自动化平台"的常见演进路径,与 [[Apache Airflow]] 从数据管道扩展到通用工作流类似。

## 参考源

- raw/计算机/
- 相关:[[Playwright与Cypress]]、[[CI_CD流水线]]、[[单元测试金字塔]]
