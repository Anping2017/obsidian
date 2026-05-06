---
title: Angular
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/框架/]
created: 2026-05-05
updated: 2026-05-05
summary: Angular 是 Google 2016 年用 TypeScript 重写的企业级前端框架,以模块系统、依赖注入、RxJS 响应式编程为核心,自带路由/表单/HTTP 全功能开箱即用。
---

# Angular

## 定义

**Angular** 是 Google 2016 年发布的开源前端框架,完全用 [[TypeScript类型系统]] 重写自原 AngularJS(1.x,已弃用)。Angular 是**自带电池**(batteries-included)的完整框架:路由、表单、HTTP、状态、依赖注入、构建工具均官方提供,与 [[React]]/[[Vue]] 的库式生态形成对比。

## 核心要点

### 1. 模块系统(NgModule)

应用按模块组织,每个模块声明组件、服务、imports 其他模块。Angular 14+ 推 Standalone Components,逐步淡化 NgModule。

### 2. 组件 + 模板 + 指令

```ts
@Component({
  selector: 'app-counter',
  template: `<button (click)="inc()">{{ count }}</button>`
})
export class CounterComponent {
  count = 0;
  inc() { this.count++; }
}
```

模板语法:`*ngFor`、`*ngIf`、`[prop]` 属性绑定、`(event)` 事件、`[(ngModel)]` 双向。

### 3. 依赖注入(DI)

Angular 内置 IoC 容器:

```ts
@Injectable({ providedIn: 'root' })
export class UserService { constructor(private http: HttpClient) {} }

// 组件构造器自动注入
constructor(private user: UserService) {}
```

DI 让单元测试简单(替换 mock),也是企业开发可维护性核心。

### 4. RxJS 与 Observable

HTTP、表单变化、路由事件都返回 Observable。需掌握 RxJS 操作符(map、switchMap、debounceTime),学习曲线陡。

### 5. AOT 编译

模板默认 Ahead-of-Time 编译,生成高效 JS,无运行时模板解析。结合 Ivy 引擎(Angular 9+)生成更小体积。

### 6. 与 React/Vue 对比

| 维度 | [[React]] | [[Vue]] | Angular |
|---|---|---|---|
| 类型 | 库 | 框架 | 完整框架 |
| 语言 | JSX(JS) | SFC(模板) | TS + 装饰器 + 模板 |
| 学习曲线 | 中 | 低 | 高 |
| 自带功能 | 极少 | 中 | 全 |
| DI | 无 | 无 | 核心 |
| 用户 | 互联网 | 中小企业 | 大企业、内部系统 |

### 7. Signals(Angular 17+)

引入 [[SolidJS]]/Vue 风格的细粒度响应式 signal:

```ts
count = signal(0);
double = computed(() => this.count() * 2);
effect(() => console.log(this.count()));
```

signal 有望逐步取代 zone.js 脏检查,简化心智模型。

### 8. SSR 与 Hydration

Angular Universal 提供 SSR;v17 引入 Non-destructive Hydration,SSR 体验显著改善。

### 9. 适用场景

- 大型企业内部系统
- 长生命周期项目(强类型 + DI + 文档完善)
- 团队偏好 OO + 强约束

不适合:小型项目(过重)、追求极简(学习成本高)。

## 关系

- 对比:[[React]]、[[Vue]]、[[Svelte]]
- 类型:[[TypeScript类型系统]] 强依赖
- 范式:[[面向对象编程]] + RxJS [[函数式编程]]
- 模式:[[设计模式]] 中 DI、装饰器密集
- 生态:Nx、NestJS(后端孪生)

## 参考源

- raw/计算机/开发学习/框架/
