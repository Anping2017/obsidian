---
title: Spring 框架思想
type: concept
tags: [cs, web, backend, mature]
sources: [raw/计算机/开发学习/]
created: 2026-05-05
updated: 2026-05-05
summary: Spring 是 Java 后端事实标准框架,以依赖注入(IoC)、面向切面编程(AOP)、声明式事务、Spring Boot 自动配置奠定企业开发基础设施地位。
---

# Spring 框架思想

## 定义

**Spring Framework** 是 Rod Johnson 2003 年发布的 Java 应用框架,起源于其同年出版的《Expert One-on-One J2EE Design and Development》一书。Spring 的设计目标是**简化企业 Java 开发**:用轻量 POJO + IoC 容器替代笨重的 EJB。21 年后,Spring + Spring Boot 已是 Java 后端事实标准,从 Netflix、Uber 到中国互联网,几乎所有 Java 企业应用都基于此。

## 核心要点

### 1. IoC 与依赖注入(DI)

**控制反转(Inversion of Control)**:对象不再自己 new 依赖,而由容器创建并注入。

```java
@Service
public class UserService {
  private final UserRepository repo;
  public UserService(UserRepository repo) { this.repo = repo; }
}
```

容器扫描 `@Component`/`@Service`/`@Repository` 注解,自动装配 Bean。优势:解耦、可测试(替换为 mock)、可配置。

### 2. AOP(面向切面)

把横切关注点(日志、事务、安全)与业务代码分离:

```java
@Aspect
public class LoggingAspect {
  @Around("execution(* com.x.service..*(..))")
  public Object log(ProceedingJoinPoint pjp) throws Throwable {
    System.out.println("Before: " + pjp.getSignature());
    return pjp.proceed();
  }
}
```

底层:JDK 动态代理或 CGLIB 字节码生成。

### 3. 声明式事务

```java
@Transactional
public void transfer(...) { ... }
```

注解一行,Spring 自动开启/提交/回滚事务,支持传播行为(REQUIRED、REQUIRES_NEW...)、隔离级别。

### 4. Spring Boot

2014 年发布的"约定优于配置"层。**自动配置(Auto-configuration)**:根据 classpath 中的 jar 自动启用功能(连了 H2 就自动配 DataSource)。一个 main 启动,内置 Tomcat/Jetty:

```java
@SpringBootApplication
public class App {
  public static void main(String[] args) { SpringApplication.run(App.class); }
}
```

把传统数月配置压缩到几小时。

### 5. Spring 生态全家桶

| 模块 | 作用 |
|---|---|
| **Spring Web MVC** | 同步 [[RESTful API]] |
| **Spring WebFlux** | 响应式异步(Reactor) |
| **Spring Data** | JPA / MongoDB / Redis 等数据访问 |
| **Spring Security** | 认证授权 |
| **Spring Cloud** | 微服务套件(Eureka、Gateway、Config) |
| **Spring Batch** | 大数据批处理 |
| **Spring Integration** | 企业集成模式(EIP) |
| **Spring AI**(2024+) | LLM 集成 |

### 6. 控制器示例

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
  @Autowired private UserService service;

  @GetMapping("/{id}")
  public User get(@PathVariable Long id) { return service.find(id); }

  @PostMapping
  public User create(@RequestBody @Valid User u) { return service.save(u); }
}
```

### 7. 与其他框架对比

| 语言 | 等价物 |
|---|---|
| Python | Django、FastAPI |
| Node | NestJS([[Express框架]] + DI 装饰器,Spring 风) |
| Go | (无完全对应,Wire/Fx 提供 DI) |
| Ruby | Rails |
| .NET | ASP.NET Core |

### 8. 优势

- 强类型 + IDE 重构能力
- 线程模型成熟
- 生态完整(数据、安全、监控、消息一应俱全)
- JVM 长寿应用稳定性

### 9. 劣势

- 启动慢(几秒到几十秒)
- 内存重(几百 MB 起)
- 冷启动差(Lambda 痛点)
- 配置魔法多,新人排错难

GraalVM Native Image 与 Spring Native(2022+)缓解启动/内存问题。

## 关系

- 范式:[[面向对象编程]] + [[设计模式]] 集大成
- DI:[[Angular]] 依赖注入概念同源
- 微服务:[[微服务]] 主流实现技术
- 对比:[[Express框架]]、[[Django框架]]、[[FastAPI]]
- 配合:Spring Cloud + [[Kubernetes]] 云原生

## 参考源

- raw/计算机/开发学习/新技术/现代云原生和分布式系统完整构架.md
