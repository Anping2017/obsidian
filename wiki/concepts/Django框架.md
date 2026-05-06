---
title: Django 框架
type: concept
tags: [cs, web, backend, python, mature]
sources: [raw/计算机/开发学习/语言/Python/]
created: 2026-05-05
updated: 2026-05-05
summary: Django 是 Python 全栈 Web 框架,以"自带电池"著称,提供 ORM、Admin、模板、表单、认证一站式能力,内容管理与 SaaS 后台的典型选择。
---

# Django 框架

## 定义

**Django** 是 2005 年从 Lawrence Journal-World 报社的 Python 开发实践开源出来的全栈 Web 框架。设计哲学"快速开发 + DRY(Don't Repeat Yourself)+ 自带电池(Batteries Included)":ORM、模板引擎、表单、认证、Admin 后台、缓存、信号、迁移工具一应俱全,无需第三方拼装。Django 与 [[Spring框架思想]] 处于同一位置:**完整框架,适合长生命周期企业应用**。

## 核心要点

### 1. MTV 架构

Django 的架构变体 [[MVC架构]],官方称 Model-Template-View(MTV):

- **Model**:数据库映射(ORM)
- **Template**:HTML 模板
- **View**:请求处理逻辑(对应传统 Controller)

### 2. ORM 示例

```python
class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

# 查询
Article.objects.filter(author__name='Alice', created__year=2026).order_by('-created')[:10]
```

ORM 自动生成 SQL,支持迁移(makemigrations + migrate)、关系预加载(select_related、prefetch_related)、聚合、原生 SQL fallback。

### 3. Django Admin

```python
from django.contrib import admin
admin.site.register(Article)
```

一行代码生成完整后台:列表、过滤、搜索、批量操作、表单校验。CMS、内部工具、SaaS 后台秒做出来。这是 Django 杀手级功能。

### 4. 路由与视图

```python
# urls.py
urlpatterns = [
  path('articles/<int:id>/', views.article_detail),
]

# views.py
def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'detail.html', {'article': article})
```

### 5. 表单系统

```python
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
```

自动生成 HTML、验证、错误显示,与 ORM 模型联动。

### 6. Django REST Framework(DRF)

第三方但事实标准的 [[RESTful API]] 扩展:

```python
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

提供 Serializer、ViewSet、Router、Pagination、Permission、Throttle、Auth 全套。Instagram、Disqus 等大型 API 都基于 DRF。

### 7. 与其他框架对比

| 框架 | 类型 | 哲学 |
|---|---|---|
| Django | 全栈 | 自带电池 |
| **Flask** | 微框架 | 极简、灵活 |
| **FastAPI**(参见 [[FastAPI]]) | 现代 API | 类型 + 异步 + OpenAPI |
| **Tornado** | 异步 | 长连接 |
| **Sanic** | 异步 | Flask API + 异步 |

### 8. 异步支持

Django 3.0(2019)起 ASGI 兼容,4.x 路由可定义异步视图:

```python
async def view(request):
    data = await fetch_external()
    return JsonResponse(data)
```

但 ORM 仍主要同步,正在逐步异步化。

### 9. 适用场景

- 内容管理(媒体、博客、新闻)
- 后台管理系统、SaaS 控制台
- 教育/医疗等数据密集业务
- 长生命周期项目(Django LTS 三年支持)

不适用:

- 极致性能(Go/Rust 更优)
- 实时长连接为主([[FastAPI]] / Node 更合适)

### 10. 著名应用

Instagram(早期)、Pinterest、Disqus、Mozilla、华盛顿邮报、Spotify。

## 关系

- 范式:[[MVC架构]] (MTV 变体) + Python [[面向对象编程]]
- 对比:[[FastAPI]]、Flask、[[Express框架]]、[[Spring框架思想]]
- 应用:DRF 实现 [[RESTful API]]
- 数据库:PostgreSQL 首选([[关系型数据库]])
- 运行:WSGI / ASGI

## 参考源

- raw/计算机/开发学习/语言/Python/
