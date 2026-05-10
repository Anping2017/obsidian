---
title: PyTest
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: PyTest 是 Python 生态最流行的测试框架,以 fixture 依赖注入、参数化、强大的发现机制和插件生态,把 Python 单元/集成/系统测试从 unittest 的样板代码中解放,成为现代 Python 工程标准。
---

# PyTest

## 定义

**PyTest** 是 Holger Krekel 在 2004 年起开发的 Python 测试框架,2008 年独立项目化。它打破 Python 标准库 unittest 的 xUnit 风格(必须继承 TestCase 类、setUp/tearDown 命名),让测试**直接以函数形式编写,通过依赖注入获取资源**,并提供极强的参数化、Fixture、插件扩展能力。

PyTest 是当前 Python 工程的事实标准——超 90% 的开源 Python 库以 PyTest 为测试框架,Pandas、NumPy、Django、FastAPI、Sklearn 全部使用。

## 与 unittest 对比

**unittest(标准库,Java/JUnit 风)**

```python
class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
    def test_add(self):
        self.assertEqual(self.calc.add(1, 2), 3)
```

**PyTest(简洁函数风)**

```python
def test_add():
    calc = Calculator()
    assert calc.add(1, 2) == 3
```

差异:
- 无需继承 TestCase
- 用普通 assert 而非 self.assertEqual
- 失败时输出富文本对比(显示实际值/期望值/diff)
- 无样板代码

## 核心特性

**1. Fixture(夹具)**

最重要的创新——**测试依赖通过函数参数注入**:

```python
@pytest.fixture
def db():
    conn = create_connection()
    yield conn  # yield 之前是 setup,之后是 teardown
    conn.close()

def test_query(db):  # 自动注入
    assert db.query("SELECT 1") == [(1,)]
```

Fixture 支持作用域:function(默认)、class、module、session,实现资源在不同生命周期共享。

**2. 参数化(Parametrize)**

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (5, 5, 10),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert Calculator().add(a, b) == expected
```

一个测试函数变成 N 个独立测试,失败定位精确到参数组合。

**3. 自动发现**

- 默认找所有 test_*.py 或 *_test.py
- 找所有 test_* 函数 / Test* 类
- 无需手动注册

**4. 标记(Mark)**

```python
@pytest.mark.slow
def test_long_running(): ...

# 命令行:
pytest -m "slow"        # 仅运行 slow
pytest -m "not slow"    # 跳过 slow
```

**5. 插件生态**

pytest-* 包是核心扩展点:
- pytest-cov:覆盖率
- pytest-xdist:多进程并行
- pytest-asyncio:async 测试
- pytest-mock:mock 简化
- pytest-django、pytest-flask、pytest-fastapi:Web 框架集成
- pytest-benchmark:性能基准
- pytest-html:HTML 报告
- pytest-randomly:随机顺序
- pytest-sugar:更友好输出

## 高级用法

**Fixture 嵌套**

```python
@pytest.fixture
def db(): ...

@pytest.fixture
def user(db):  # 依赖另一个 fixture
    return db.create_user()

def test_action(user):
    user.do_something()
```

**conftest.py**

特殊文件,自动收集为父级目录所有测试可用的 Fixture / Plugin。是组织复杂测试套件的关键。

**Monkeypatch**

```python
def test_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "fake")
    assert os.getenv("API_KEY") == "fake"
```

**Mock 与 patch**

```python
def test_external(mocker):  # pytest-mock
    mocker.patch("module.requests.get", return_value=MockResponse())
```

## 与同类对比

| 维度 | PyTest | unittest | nose | doctest |
|---|---|---|---|---|
| 风格 | 函数 + Fixture | 类 + xUnit | nose2 已停 | 嵌入文档字符串 |
| 现状 | 主流 | 标准库,小项目 | 弃用 | 文档示例验证 |
| 发现机制 | 强 | 弱 | 中 | 不适用 |
| 插件 | 极多 | 少 | 中 | 无 |
| 学习曲线 | 中 | 低 | 中 | 低 |

## 测试运行示例

```bash
pytest                          # 跑全部
pytest tests/test_models.py     # 跑文件
pytest tests/test_models.py::test_user_creation  # 跑单个
pytest -k "user"                # 名字含 user 的测试
pytest -v                       # verbose
pytest --tb=short              # 错误堆栈精简
pytest -x                       # 首个失败即停
pytest -n 4                     # 并行 4 进程(pytest-xdist)
pytest --cov=myapp             # 覆盖率
pytest --cov=myapp --cov-report=html
```

## 测试金字塔实践

**单元测试**

- 函数级,毫秒级,用 Fixture 隔离副作用
- Mock 数据库、外部 API
- 量大、跑频繁

**集成测试**

- pytest-django 实测数据库
- pytest-fastapi TestClient 模拟 HTTP
- 中等数量,提交前跑

**系统/E2E 测试**

- Selenium、Playwright 与 PyTest 集成
- 少量、关键路径

## 与 Web 框架集成

**Django**

```python
@pytest.mark.django_db
def test_user_create(client):
    User.objects.create(name="alice")
    assert User.objects.count() == 1
```

**FastAPI**

```python
def test_endpoint():
    client = TestClient(app)
    response = client.get("/users/1")
    assert response.status_code == 200
```

**Flask**

类似 FastAPI 模式,client fixture 注入。

## CI 集成

GitHub Actions、GitLab CI、Jenkins 中标准命令:

```yaml
- run: pytest --cov=myapp --cov-report=xml
- uses: codecov/codecov-action@v3
```

PyTest 与 [[CI_CD流水线]] 集成简单——退出码标准、JUnit XML 报告兼容主流 CI。

## 局限

- Fixture 复杂时排错难(隐式注入 → 难追踪)
- 异步测试需 pytest-asyncio,API 略繁琐
- 大量 Fixture/conftest.py 可能成"魔法"
- 性能测试不是它的强项(benchmark 插件辅助)
- 流程性测试(BDD)需 pytest-bdd,但不如 Behave 直观

## 和其他概念的关系

PyTest 是 [[TDD测试驱动开发]] 在 Python 生态的核心工具。它的 Fixture 系统体现了"依赖注入"思想,与 [[设计原则SOLID]] 的依赖倒置同构——可测性 = 解耦。

PyTest 与 [[Django框架]]、[[FastAPI]]、SQLAlchemy 等主流栈深度整合,通过专属插件(pytest-django、pytest-asyncio)无缝接入。CI 实践中,它与 [[CI_CD流水线]]、[[GitFlow与TrunkBased]] 工作流共同构成 Python 工程的质量护栏。

参数化与 Mock 思想与 [[Jest与Vitest]]、JUnit 等其他语言测试框架同构,显示主流测试框架在概念层面的趋同。

## 参考源

- raw/计算机/
- 相关:[[TDD测试驱动开发]]、[[单元测试金字塔]]、[[Django框架]]
