---
title: FastAPI
type: concept
tags: [cs, web, backend, python, mature]
sources: [raw/计算机/开发学习/语言/Python/]
created: 2026-05-05
updated: 2026-05-05
summary: FastAPI 是 Sebastián Ramírez 2018 年创建的现代 Python Web 框架,基于类型提示自动校验请求、生成 OpenAPI 文档,异步性能比肩 Node/Go,AI 后端首选。
---

# FastAPI

## 定义

**FastAPI** 是 Sebastián Ramírez(@tiangolo)2018 年开源的 Python Web 框架,定位高性能现代 API。核心特色:**基于 Python 类型提示自动做请求校验、序列化、OpenAPI 文档生成**;基于 Starlette + Pydantic 实现 ASGI 异步 IO,性能在 Python 框架中领先,接近 Node.js / Go。AI、ML 后端的事实标准选择。

## 核心要点

### 1. 类型驱动

```python
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    tags: list[str] = []

app = FastAPI()

@app.post('/items/')
async def create_item(item: Item) -> Item:
    return item
```

类型提示同时:
- 校验请求体(自动 422 错误响应)
- 序列化响应
- 生成 OpenAPI Schema
- IDE 自动补全

### 2. 自动文档

启动后访问:
- `/docs` → Swagger UI
- `/redoc` → ReDoc UI
- `/openapi.json` → 标准 OpenAPI 规范

无需手写文档,接口定义即文档,与 [[GraphQL]] schema-first 异曲同工。

### 3. 依赖注入

```python
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.get('/users/{id}')
async def get_user(id: int, db: Session = Depends(get_db)):
    return db.query(User).get(id)
```

`Depends()` 实现简洁的 DI,支持嵌套、子依赖、缓存。

### 4. 异步原生

```python
@app.get('/x')
async def x():
    data = await fetch_external()
    return data
```

整个生命周期 ASGI 异步,搭配 Uvicorn / Hypercorn 部署。

### 5. Pydantic 数据校验

```python
class User(BaseModel):
    age: int = Field(gt=0, lt=120)
    email: EmailStr
    role: Literal['admin', 'user']
```

Pydantic v2 用 Rust 重写校验核心,速度提升数十倍。是 FastAPI 的灵魂。

### 6. 与 Django/Flask 对比

| 维度 | Django | Flask | FastAPI |
|---|---|---|---|
| 全栈 | 是(Admin、模板) | 否 | 否(API 专注) |
| 类型 | 弱 | 弱 | 强(Pydantic) |
| 异步 | 部分 | 弱 | 原生 |
| 文档 | 手写 | 手写 | 自动 OpenAPI |
| 性能 | 中 | 中 | 高 |
| 学习曲线 | 中 | 低 | 低 |
| 适用 | 内容站、SaaS | 小项目 | API、AI 后端 |

### 7. AI 后端首选

FastAPI 在 LLM 应用栈中占主导地位:
- OpenAI、Anthropic 早期 API 演示就用 FastAPI
- LangChain / LlamaIndex 文档 demo
- Hugging Face Spaces / Inference Endpoints 后端
- Fine-tuning 服务、向量数据库 API

原因:类型提示对 schema 驱动 AI 工具友好、异步流式响应([[SSE]])天然、Python 是 AI 生态主语言。

### 8. 部署

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

- Docker 友好
- 配 Gunicorn + Uvicorn workers 生产用
- Vercel Functions、Render、Fly.io、AWS Lambda(Mangum)

### 9. 局限

- 不含模板引擎(API 专用,不做 SSR)
- 无 ORM(常配 SQLAlchemy / SQLModel)
- 无 Admin(需自建)

### 10. 生态

- **SQLModel**(@tiangolo 同作者):SQLAlchemy + Pydantic 合体
- **Typer**:CLI 框架(同作者)
- **Tortoise ORM**:异步 ORM
- **strawberry-graphql**:GraphQL 集成

## 关系

- 类型:Python type hints + Pydantic
- 异步:ASGI / Starlette / asyncio
- 文档:OpenAPI 3,与 [[RESTful API]] 标准化
- 对比:[[Django框架]]、Flask、[[Express框架]]、[[Spring框架思想]]
- 应用:[[大语言模型]] 服务、向量数据库 API

## 参考源

- raw/计算机/开发学习/语言/Python/
- raw/计算机/开发学习/新技术/2025 网站开发的核心趋势.md
