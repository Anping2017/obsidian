---
title: Spring Boot
type: concept
tags: [programming, mature]
sources: [raw/计算机/]
created: 2026-05-05
updated: 2026-05-05
summary: Spring Boot 是 Pivotal(VMware)2014 年发布的 Java 微服务框架,通过自动配置、起步依赖、嵌入式服务器,把 Spring 生态的复杂配置简化到"约定优于配置",成为 Java 后端事实标准。
---

# Spring Boot

## 定义

Spring Boot 是基于 [[Spring框架思想]] 的"约定优于配置(Convention over Configuration)"应用框架,2014 年由 Pivotal(后并入 VMware)团队发布。它解决了 Spring Framework 长期以来的"XML 配置噩梦"——通过自动配置(Auto-Configuration)、起步依赖(Starter Dependencies)、嵌入式服务器(Embedded Tomcat/Jetty),让 Java 开发者从"配置 100 行 XML 才跑得起来"进化到"加几个依赖就能跑"。

它是当前 Java 后端开发的事实标准,微服务、企业系统、互联网应用大量采用,并孵化了 Spring Cloud 等下游生态。

## 核心特性

**1. 起步依赖(Starter Dependencies)**

Maven/Gradle 中加一个 starter,所有相关依赖、版本、配置自动就位:

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

包含:Spring MVC、Tomcat、Jackson、validation、logging。无需手动管理几十个依赖版本兼容。

常用 Starter:
- web、data-jpa、security、actuator、test、cache、redis、kafka、mongodb、graphql 等数十种

**2. 自动配置(Auto-Configuration)**

Spring Boot 启动时根据 classpath 中的依赖自动配置 Bean:
- 看到 H2 → 自动配 DataSource
- 看到 Tomcat → 自动启嵌入式 Tomcat
- 看到 Spring Security → 自动加默认安全策略

通过 @EnableAutoConfiguration(在 @SpringBootApplication 中包含)激活。

**3. 嵌入式服务器(Embedded Server)**

无需部署 WAR 到外部 Tomcat:
- 默认 Tomcat 嵌入,App 即 java -jar 启动
- 可换 Jetty、Undertow
- 简化 DevOps,容器化部署友好

**4. 配置外部化(Externalized Configuration)**

- application.properties / application.yml 集中配置
- 支持多 Profile(dev / staging / prod)
- 环境变量、命令行、配置中心(Spring Cloud Config)

**5. Actuator(运维端点)**

内置 /actuator 路径下:
- /health 健康检查
- /info 应用信息
- /metrics、/prometheus 指标
- /env、/beans、/mappings(开发期)

是云原生部署、监控、容器调度的关键。

## 典型应用结构

```
src/main/java/com/example/app/
  ├── Application.java          // @SpringBootApplication 主类
  ├── controller/                // REST 控制器
  ├── service/                   // 业务逻辑
  ├── repository/                // 数据访问 Spring Data
  ├── entity/                    // JPA 实体
  └── config/                    // 自定义配置
src/main/resources/
  ├── application.yml
  ├── static/                    // 静态资源
  └── templates/                 // 模板(Thymeleaf)
```

## 常用注解

- **@SpringBootApplication**:类级,组合 @Configuration + @EnableAutoConfiguration + @ComponentScan
- **@RestController**:REST API 控制器
- **@RequestMapping / @GetMapping / @PostMapping**:URL 映射
- **@Service / @Repository / @Component**:Bean 注册
- **@Autowired / @Resource**:依赖注入
- **@Transactional**:声明式事务
- **@Configuration / @Bean**:Java 配置
- **@Value / @ConfigurationProperties**:配置注入
- **@ConditionalOnXxx**:条件 Bean(自定义自动配置核心)

## Spring Boot 生态

**Spring Data**:JPA、Redis、MongoDB、Cassandra、Elasticsearch 等的 Repository 抽象

**Spring Security**:认证授权,OAuth2、SAML、JWT 集成

**Spring Cloud**:微服务工具集,服务发现(Eureka、Consul)、配置中心(Config Server)、网关(Gateway)、断路器(Resilience4j)

**Spring Batch**:批处理任务

**Spring Integration**:企业集成模式(消息队列、文件、邮件)

**Spring WebFlux**:响应式异步 Web 框架,基于 Reactor

**Spring AI(2024)**:对接 OpenAI、Anthropic、Azure OpenAI、Vector DB 的 AI 应用框架

## 版本演进

- 1.x(2014):基于 Spring Framework 4
- 2.x(2018):Spring Framework 5,响应式支持(WebFlux)
- 3.x(2022):Java 17+ 强制,Jakarta EE 9 命名空间(javax → jakarta),原生映像支持(GraalVM)

每个大版本对应一个 Java 最低版本,迁移成本不可忽略。

## 与同类框架对比

| 维度 | Spring Boot | Quarkus | Micronaut | Vert.x |
|---|---|---|---|---|
| 启动速度 | 慢(2-5s) | 极快(< 0.1s,GraalVM) | 极快 | 极快 |
| 内存占用 | 较高(150-300MB) | 极低(~30MB) | 极低 | 中 |
| 生态 | 极大 | 中 | 中 | 中 |
| 学习曲线 | 中 | 低 | 低 | 中 |
| 适合 | 企业开发主流 | 云原生 / Serverless | 微服务 | 高并发 |

Spring Boot 仍是企业开发主流,Quarkus 在 Serverless 场景兴起。

## 局限

- 启动慢(传统 JVM)
- 内存占用大(对比 Go/Rust 服务)
- "魔法"多(自动配置)调试有挑战
- GraalVM Native Image 支持仍在完善
- 体量大(framework 自身依赖几百 MB)

## 参考源

- raw/计算机/
- 相关:[[Spring框架思想]]、[[Java]]、[[微服务]]
