---
title: Django REST Framework
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Django REST Framework(DRF)是基于 Django 的 Web API 工具包,把序列化、视图、认证、权限、限流等 REST 通用关注点抽象为可组合的类,是 Python 生态构建 RESTful API 的事实标准。
---

# Django REST Framework

## 定义

**Django REST Framework(DRF)** 是建立在 [[Django框架]] 之上的 Web API 构建工具包,2011 年由 Tom Christie 开源。它针对 [[RESTful API]] 设计的通用问题——数据序列化、视图组合、认证授权、限流分页、版本管理——提供了一组可插拔、可继承的类,与 Django ORM 和模板模式深度对齐。

DRF 是 Python 生态构建中等规模 REST API 的事实标准,与轻量异步框架 [[FastAPI]] 形成"重型企业 vs 轻量现代"的两极。

## 核心组件

**Serializer(序列化器)**

把模型实例转换为 JSON,反之亦然。同时承担入参校验、字段约束、嵌套关系。
- ModelSerializer 自动从 Django Model 派生字段
- 支持嵌套 Serializer 表达一对多/多对多
- validate_*() 钩子自定义校验逻辑

**ViewSet 与 Generic View**

把"列表/创建/读取/更新/删除"五个标准操作合并为一个类:
- ListAPIView、RetrieveAPIView、CreateAPIView 等通用视图
- ModelViewSet 一键涵盖完整 CRUD
- 与 Router 配合自动生成 URL 路由

**Router**

DefaultRouter 将 ViewSet 自动映射到 URL,遵循 REST 风格命名(/users/、/users/{id}/),省去手写大量 url 配置。

**Authentication & Permission**

- 内建多种认证:Session、Token、JWT(配合 simplejwt)、OAuth2
- 权限类(IsAuthenticated、IsAdminUser、自定义)按视图、对象级别控制
- 与 Django 用户系统无缝衔接

**Throttle(限流)**

- AnonRateThrottle、UserRateThrottle 内置
- 简单声明 throttle_classes 即生效
- 可基于用户、IP 或自定义键限流

**Pagination(分页)**

PageNumberPagination、LimitOffsetPagination、CursorPagination 三种内建模式,后者为大数据列表稳定翻页设计。

## 与 Django 的关系

DRF 不是替代 Django MVT,而是叠加于其上:
- 复用 Django ORM([[关系型数据库]] 抽象)
- 复用 Django 中间件、Auth、Admin
- 把模板渲染层换成 JSON 响应层
- 沿袭 Django"Batteries Included"哲学

这意味着 DRF 项目自带 Admin 后台、ORM 迁移、表单验证等 Django 全套基础设施,工程化成熟度远高于纯 API 框架。

## 与 FastAPI 对比

| 维度 | DRF | FastAPI |
|---|---|---|
| 异步 | 渐进支持(3.0+) | 原生 async |
| 性能 | 中(WSGI/ASGI) | 高(Starlette + Pydantic) |
| 类型系统 | 运行时校验 | Python type hints + Pydantic |
| 文档 | drf-spectacular 等插件 | OpenAPI 内建自动生成 |
| 生态 | Django 全家桶 | 轻量,自由组合 |
| 学习曲线 | 中(要懂 Django) | 低 |
| 适合 | 含管理后台的传统 SaaS | 微服务、AI 后端 |

DRF 适合需要 ORM、Admin、复杂权限的传统业务后台;FastAPI 在 [[微服务]]、[[AI Agent]] 后端、纯 API 服务上更受欢迎。

## 典型代码模式

```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author']

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [UserRateThrottle]
```

5 行代码即获得完整 REST 端点,这是"约定优于配置"在 Python 生态的体现。

## 进阶生态

- **drf-spectacular**:OpenAPI 3.0 规范生成,与 [[Schema markup]] 体系互通
- **django-filter**:声明式过滤,?status=active 自动转换为 ORM 查询
- **drf-nested-routers**:嵌套资源 /users/{id}/articles/
- **simplejwt**:[[JWT]] 认证集成
- **drf-yasg**:旧的 Swagger 生成器,逐步被 spectacular 取代

## 局限

- WSGI 同步起源,异步生态不及原生异步框架成熟
- 复杂嵌套写法易膨胀(N+1 查询陷阱)
- 缺 Pydantic 这种现代类型系统
- 自动生成 OpenAPI 不如 FastAPI 直接
- 大型项目下 ViewSet 抽象可能过度,需回退到 APIView

## 和其他概念的关系

DRF 与 [[Django框架]]、[[关系型数据库]]、[[RESTful API]] 共同构成 Python Web 全栈方案。它的认证模块对接 [[OAuth 2.0]]、[[JWT]];限流能力是 [[API网关]] 模式的轻量替代;分页/序列化思想在 [[GraphQL]] 中被另一种方式重写。

在 [[微服务]] 架构下,DRF 适合做单个业务服务的 REST 接口层,而前端通过 [[BFF]] 或网关聚合多服务调用。

## 参考源

- raw/计算机/
- 相关:[[Django框架]]、[[FastAPI]]、[[RESTful API]]
