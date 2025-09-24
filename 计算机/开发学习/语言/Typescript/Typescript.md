## 1️⃣ TypeScript 基础

|分类|内容|
|---|---|
|**定义**|JavaScript 的超集，增加静态类型检查|
|**安装与环境**|npm/yarn 安装、tsconfig.json 配置|
|**编译流程**|tsc 编译、watch 模式、与 Babel 集成|
|**基本类型**|number, string, boolean, null, undefined, any, unknown, void, never|
|**类型推断**|自动推断变量和函数返回值类型|
|**变量声明**|let, const, var（类型注解）|

---

## 2️⃣ 类型系统

|分类|内容|
|---|---|
|**基本类型**|string, number, boolean, symbol, null, undefined, any, unknown, void, never|
|**数组与元组**|number[], string[], [string, number]|
|**枚举**|enum, const enum|
|**字面量类型**|字符串字面量、数字字面量、布尔字面量|
|**联合类型**|string \| number|
|**交叉类型**|type A = B & C|
|**类型别名**|type MyType = string \| number|
|**接口**|interface, 可选属性、只读属性、函数接口|
|**类型断言**|as 语法、<> 语法|
|**索引类型**|keyof, typeof, in|

---

## 3️⃣ 函数与面向对象

|分类|内容|
|---|---|
|**函数类型**|参数类型、返回值类型、可选参数、默认参数、剩余参数|
|**重载**|函数重载类型定义|
|**类**|class, 构造函数, public/private/protected, readonly|
|**继承**|extends, super|
|**接口实现**|implements|
|**抽象类**|abstract class, abstract method|
|**泛型**|泛型函数、泛型类、泛型接口、约束泛型|

---

## 4️⃣ 高级类型

|分类|内容|
|---|---|
|**条件类型**|T extends U ? X : Y|
|**映射类型**|{ [K in keyof T]: T[K] }|
|**类型保护**|typeof, instanceof, in, 自定义类型保护|
|**工具类型**|Partial, Required, Pick, Omit, Record, Exclude, Extract, NonNullable, ReturnType, Parameters|
|**类型推断**|infer 关键字|
|**联合与交叉**|类型组合与限制|

---

## 5️⃣ 模块与命名空间

|分类|内容|
|---|---|
|**ES6 模块**|import/export, 默认导出与命名导出|
|**命名空间**|namespace, 内部模块、嵌套命名空间|
|**声明文件**|.d.ts, 声明第三方库类型|
|**模块解析**|CommonJS, AMD, ESModule, UMD|

---

## 6️⃣ 类型兼容性与严格模式

|分类|内容|
|---|---|
|**结构性类型系统**|Duck typing, 类型兼容性|
|**严格模式**|strictNullChecks, noImplicitAny, strictFunctionTypes, strictBindCallApply|
|**类型收窄**|类型缩小、类型保护、类型断言|

---

## 7️⃣ TypeScript 与 JavaScript 集成

|分类|内容|
|---|---|
|**JS 互操作**|使用 JS 文件、逐步迁移项目|
|**第三方库类型**|DefinitelyTyped, @types 包|
|**React + TS**|tsx 文件、组件 Props/State 类型、泛型组件|
|**Node.js + TS**|ts-node, 类型声明、核心模块类型定义|

---

## 8️⃣ 构建与工具

|分类|内容|
|---|---|
|**编译器**|tsc, Babel 转译|
|**构建工具**|Webpack, Rollup, Vite, esbuild|
|**Lint & 格式化**|ESLint, Prettier, TSLint（已弃用）|
|**测试**|Jest, Mocha + ts-node, React Testing Library|

---

## 9️⃣ 高级实践与最佳实践

|分类|内容|
|---|---|
|**类型安全设计**|类型定义优先、减少 any|
|**泛型设计**|通用函数、通用组件、复用类型逻辑|
|**设计模式**|TS 中的单例、工厂、策略、装饰者模式|
|**大型项目组织**|模块化、类型文件管理、monorepo|