---
title: NestJS
type: concept
tags: [cs, web, backend, mature]
sources: [raw/计算机/开发学习/语言/Node JS/]
created: 2026-05-05
updated: 2026-05-05
summary: NestJS 是 Kamil Mysliwiec 2017 年创建的 Node.js 企业级框架,以 TypeScript + 装饰器 + 依赖注入 + 模块化构建,被誉为 Node 版 Spring/Angular。
---

# NestJS

## 定义

**NestJS** 是 Kamil Mysliwiec 2017 年开源的 [[Node.js]] 服务端框架,目标是把企业级开发的最佳实践带入 Node 生态。它深受 [[Angular]]、[[Spring框架思想]] 启发,提供:**TypeScript 一等支持、装饰器路由、依赖注入容器、模块化、AOP 拦截器、CQRS、微服务、GraphQL、gRPC**。被誉为"Node 版 Spring"。

## 核心要点

### 1. 模块化

```ts
@Module({
  imports: [TypeOrmModule.forFeature([User])],
  controllers: [UserController],
  providers: [UserService],
  exports: [UserService]
})
export class UserModule {}
```

每个功能域一个 Module,组装到 AppModule。结构清晰,适合大型团队。

### 2. 装饰器路由

```ts
@Controller('users')
export class UserController {
  constructor(private readonly service: UserService) {}

  @Get(':id')
  findOne(@Param('id') id: string) { return this.service.findOne(+id); }

  @Post()
  @UseGuards(AuthGuard)
  create(@Body() dto: CreateUserDto) { return this.service.create(dto); }
}
```

### 3. 依赖注入

构造器注入,与 [[Spring框架思想]] / [[Angular]] 同构:

```ts
@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User) private repo: Repository<User>,
    private notifier: NotifierService
  ) {}
}
```

容器自动解析,**测试时替换为 mock 极简单**。

### 4. 七大构建块

| 概念 | 作用 |
|---|---|
| **Module** | 组织代码 |
| **Controller** | HTTP 入口 |
| **Provider/Service** | 业务逻辑 |
| **Pipe** | 校验/转换 |
| **Guard** | 鉴权 |
| **Interceptor** | AOP 切入点(日志、缓存、转换) |
| **ExceptionFilter** | 异常处理 |

### 5. 底层引擎

NestJS 不自己造 HTTP server,而是封装:

- **Express**(默认)
- **Fastify**(可切,更快)

```ts
const app = await NestFactory.create<NestFastifyApplication>(
  AppModule, new FastifyAdapter()
);
```

### 6. 全栈能力

- **REST**:控制器 + ValidationPipe + Swagger 自动文档
- **GraphQL**:`@nestjs/graphql`,Code First / Schema First
- **gRPC**:微服务模式
- **WebSocket**:`@nestjs/websockets` + Socket.IO/ws
- **TaskScheduling**:cron
- **CLI**:`nest g resource user` 一行生成 CRUD

### 7. 与同类对比

| 框架 | 哲学 | 学习曲线 |
|---|---|---|
| [[Express框架]] | 极简 | 低 |
| Koa | 异步极简 | 低 |
| Fastify | 性能 | 中 |
| Hono | Web 标准 + Edge | 低 |
| **NestJS** | 企业 + 类型 + DI | 中-高 |
| AdonisJS | Laravel 风格 | 中 |

### 8. 微服务支持

```ts
// 主进程
@Controller()
export class AppController {
  @MessagePattern('hello')
  hello(data: string) { return `Hello ${data}`; }
}
```

支持 Redis、NATS、RabbitMQ、Kafka、gRPC 等多种传输。

### 9. 适用场景

- 大型团队 + 长生命周期项目
- TypeScript 偏好强
- 来自 Java Spring / Angular 背景
- 复杂业务领域,模块拆分需求

不适用:小项目、API 网关(用 Express/Fastify/Hono 更轻)。

### 10. 著名应用

- Adidas、Mercedes-Benz、Roche 等企业
- 国内大厂内部系统迁移 Node 时常选

## 关系

- 运行时:[[Node.js]]
- 引擎:[[Express框架]] / Fastify
- 灵感:[[Angular]] + [[Spring框架思想]]
- 类型:[[TypeScript类型系统]]
- 协议:[[RESTful API]]、[[GraphQL]]、[[gRPC]]、[[WebSocket]]
- 模式:[[设计模式]] 集大成(DI、装饰器、CQRS、责任链)

## 参考源

- raw/计算机/开发学习/语言/Node JS/03-框架应用/
