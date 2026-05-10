---
title: AOP 面向切面编程
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: 面向切面编程通过"切点 + 通知"把横切关注点(日志、事务、安全、缓存)从业务代码抽离,以装饰、代理或字节码织入实现优雅注入,是 Spring/Django 中间件等框架的核心机制。
---

# AOP 面向切面编程

## 定义

**AOP(Aspect-Oriented Programming,面向切面编程)** 是 Gregor Kiczales 等人在 1997 年提出、AspectJ 项目(2001)推广的编程范式。它解决的核心问题:**如何在不修改业务代码的前提下,优雅注入"横切关注点(Cross-Cutting Concerns)"**——日志、事务、安全检查、缓存、性能监控等。

OOP 用类组织代码,但日志/事务等需求穿越多个类。AOP 提供"切面(Aspect)"作为新的代码组织单位——把"在哪里切入(Pointcut)"和"切入做什么(Advice)"组合定义。

## 核心概念

**Aspect(切面)**

横切关注点的模块化单位,如 LoggingAspect、TransactionAspect。

**Join Point(连接点)**

程序执行过程中可被切入的点:
- 方法调用前 / 后 / 抛异常时
- 字段访问
- 对象创建
- 异常处理
- (限制因实现不同)

**Pointcut(切点)**

匹配 Join Point 的表达式:
```java
@Pointcut("execution(* com.example.service.*.*(..))")
public void serviceLayer() {}
```

含义:com.example.service 包下所有类的所有方法。

**Advice(通知)**

在切点执行的逻辑,五种时机:
- @Before:方法执行前
- @After:之后(无论成功失败)
- @AfterReturning:成功返回后
- @AfterThrowing:抛异常后
- @Around:环绕(可控制是否继续)

**Weaving(织入)**

把 Aspect 注入到目标代码的过程:
- **编译时织入(CTW)**:AspectJ 编译器
- **加载时织入(LTW)**:类加载时修改字节码
- **运行时织入(动态代理)**:Spring AOP 默认

## 经典示例:声明式事务

**没有 AOP**

```java
public Order placeOrder(Order order) {
    Connection conn = ds.getConnection();
    conn.setAutoCommit(false);
    try {
        orderDao.insert(conn, order);
        inventoryDao.deduct(conn, order);
        conn.commit();
        return order;
    } catch (Exception e) {
        conn.rollback();
        throw e;
    } finally {
        conn.close();
    }
}
```

每个业务方法都重复事务管理代码。

**有 AOP**

```java
@Service
public class OrderService {
    @Transactional
    public Order placeOrder(Order order) {
        orderDao.insert(order);
        inventoryDao.deduct(order);
        return order;
    }
}
```

`@Transactional` 由 Spring AOP 自动织入事务管理。业务代码只关心业务。

## Spring AOP 实现

**基于代理(Proxy)**

```java
@Service
public class OrderService {
    @Transactional
    public Order placeOrder(Order order) { ... }
}

// Spring 启动时:
// 1. 扫描 @Service Bean
// 2. 检测含 @Transactional 等切面注解
// 3. 生成 OrderService 的代理子类(CGLIB)或代理实现(JDK)
// 4. 客户端拿到的是代理,不是原始 OrderService
```

**调用链**

```
client → OrderService 代理.placeOrder(order)
            → TransactionInterceptor.before()
              → 真实 OrderService.placeOrder()
            → TransactionInterceptor.after()
```

**限制**

- 只能切 Spring Bean 公开方法
- 内部调用(this.method())不走代理 → AOP 失效
- 不能切 final 方法 / 类(CGLIB 限制)

## AspectJ 完整 AOP

AspectJ 是更强大的 AOP:
- 编译时织入(更高性能)
- 切点更广(字段、构造、初始化)
- 不依赖框架

```aspectj
public aspect LoggingAspect {
    pointcut serviceCall():
        execution(* com.example.service..*(..));

    before(): serviceCall() {
        System.out.println("Entering: " + thisJoinPoint);
    }
}
```

需 AspectJ 编译器 ajc 处理,工程更复杂但能力更强。Spring 也支持加载时 AspectJ。

## 主流 AOP 应用场景

**1. 日志**

```java
@Around("execution(* com.example..*(..))")
public Object log(ProceedingJoinPoint jp) throws Throwable {
    long start = System.currentTimeMillis();
    Object result = jp.proceed();
    long duration = System.currentTimeMillis() - start;
    log.info("{} took {}ms", jp.getSignature(), duration);
    return result;
}
```

**2. 事务**

@Transactional + Spring TransactionManager。

**3. 安全**

```java
@PreAuthorize("hasRole('ADMIN')")
public void deleteUser(Long id) { ... }
```

Spring Security 用 AOP 实现声明式权限。

**4. 缓存**

```java
@Cacheable("users")
public User getUser(Long id) { ... }

@CacheEvict("users")
public void updateUser(User u) { ... }
```

**5. 重试**

```java
@Retryable(value = TransientException.class, maxAttempts = 3)
public Result call() { ... }
```

Spring Retry / Resilience4j。

**6. 性能监控**

@Timed 收集 Micrometer 指标。

**7. 输入验证**

@Valid + Bean Validation(JSR-303)。

**8. 多租户**

切方法,从 ThreadLocal 取 tenantId,加到 SQL where。

## 其他语言中的 AOP

**Python**

- 装饰器(decorator)是 AOP 简化形式:
```python
@log_time
@retry(attempts=3)
@cached(ttl=60)
def get_user(id): ...
```
- Django Middleware:HTTP 切面
- Flask before/after_request

**JavaScript / TypeScript**

- 装饰器(stage 3)
- Express / NestJS 中间件
- React HOC、useEffect、Higher-order Hooks

**C#/.NET**

- PostSharp(商业 AOP)
- DispatchProxy(.NET Core)
- MediatR Behaviors

**Ruby**

- Module include / prepend
- Rails Concerns

**Go**

- 函数包装(无 AOP 框架,显式更主流)
- HTTP middleware 模式

## 与中间件 / 拦截器对比

中间件(Express、Django、Spring MVC)是 HTTP 请求层 AOP:
- 请求进入 → 中间件链 → 控制器 → 中间件链 → 响应
- 每个中间件 = 切面

AOP 是更通用的概念,中间件是其在 Web 框架的特化。

## 优势

- **关注点分离**:业务代码纯净
- **可复用**:同一切面用于多模块
- **可配置**:通过注解 / XML 启用
- **DRY**:不重复
- **演进友好**:加新切面不改业务代码

## 局限与陷阱

**1. 隐式行为**

业务代码看不出"为什么慢"——可能 5 个切面在背后跑。新人看不懂。

**2. 调试困难**

堆栈深、跳转复杂。
- 看似简单方法实际执行了 N 个切面
- 出错时定位难

**3. 性能开销**

- 代理对象创建
- 反射调用
- 切面链遍历

通常忽略(微秒级),热点方法需 profile。

**4. 内部调用陷阱**

```java
@Service
public class OrderService {
    @Transactional
    public void m1() { /* tx */ }
    public void m2() { this.m1(); /* tx 不生效!*/ }
}
```

this.m1() 不走代理。需通过自注入 self 调用、或重构。

**5. 切点表达式难写**

`execution(* com.example.service..*.*(..))` 学习成本高,出错时静默不生效。

**6. 测试复杂**

测试时是否启用 AOP?Spring Test 配置不同。

## AOP 反模式

**1. 切面过于"聪明"**

切面修改业务结果(改返回值、改参数),完全偏离原意。AOP 应是"附加",不应改变核心行为。

**2. 切面间依赖**

切面 A 依赖切面 B 先跑,顺序问题。@Order 控制但脆弱。

**3. 万物皆切面**

把业务逻辑也写到切面,失去清晰边界。AOP 限于横切关注点。

**4. 不可见的死循环**

@Cacheable 的方法又调用同一对象其他 @Cacheable,递归触发。

## 与 DDD / 干净架构

[[Clean Architecture]]、[[DDD领域驱动设计]] 反对过度 AOP——领域模型应清晰,AOP 让"领域规则"模糊。但基础设施关注点(事务、日志)用 AOP 仍合适。

平衡:**领域逻辑显式,基础设施 AOP**。

## 和其他概念的关系

AOP 与 [[依赖注入与控制反转]] 是 Spring / NestJS 等框架的两大支柱——DI 解决"谁创建依赖",AOP 解决"如何切入横切逻辑"。二者结合让"业务代码 = 业务逻辑"成为可能。

它的"横切关注点"思想与 [[设计模式]] 中代理、装饰器、责任链直接对应,AOP 是这些模式的工业化。在 [[微服务]] / [[服务网格]] 时代,部分横切关注点(mTLS、重试、追踪)进一步下沉到 Sidecar,代码层 AOP 与平台层切面互补。

它与 [[响应式编程]] 操作符链思想同源——把"做什么"与"如何修饰"分开,以提高代码组织清晰度。

## 参考源

- raw/计算机/
- 相关:[[Spring Boot]]、[[依赖注入与控制反转]]、[[设计模式]]
