# TypeScript 模板字面量字符串魔法

## 🎯 模板字面量类型概览

### 📊 字符串类型系统

```mermaid
graph TD
    A[Template Literals] --> B[Basic Syntax]
    A --> C[Pattern Matching]
    A --> D[Inference Techniques]
    A --> E[Advanced Patterns]
    
    B --> B1[${variable}]
    B --> B2[Literal Concatenation]
    B --> B3[Union Types]
    
    C --> C1[Split Patterns]
    C --> C2[Prefix/Suffix]
    C --> C3[Complex Patterns]
    
    D --> D1[Type Inference]
    D --> D2[Conditional Types]
    D --> D3[Recursive Types]
    
    E --> E1[DSL Construction]
    E --> E2[Path Manipulation]
    E --> E3[Code Generation]
```

## 🔧 基础模板字面量

### 💡 语法与基本应用

```typescript
// 1. 基础模板字面量
type Greeting = `Hello, ${string}`;
type Goodbye = `Goodbye, ${string}`;

type NamedGreeting<T extends string> = `Hello, ${T}`;
type UserGreeting = NamedGreeting<'Alice'>;  // 'Hello, Alice'

// 2. 联合类型模板
type EventType = 'click' | 'hover' | 'scroll';
type EventHandler = `on_${EventType}`;
// 'on_click' | 'on_hover' | 'on_scroll'

// 3. 嵌套模板
type CSSProperty = 'color' | 'background-color' | 'font-size';
type CSSClassPrefix = 'btn-';
type CSSClassName<P extends CSSProperty> = `${CSSClassPrefix}${P}`;

type ButtonColors = CSSClassName<'color'>;  // 'btn-color'
```

### 🎪 条件字符串类型

```typescript
// 4. 条件字符串构建
type HTTPMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
type ApiEndpoint<M extends HTTPMethod, P extends string> = 
    `${M} /api${P}`;

type UserEndpoint = ApiEndpoint<'GET', '/users'>;  // 'GET /api/users'
type CreateEndpoint = ApiEndpoint<'POST', '/users'>; // 'POST /api/users'

// 5. 字符串验证
type ValidEmail<T extends string> = T extends `${string}@${string}.${string}` 
    ? T 
    : never;

type ValidUrl<T extends string> = T extends `http${'s' | ''}://${string}`
    ? T
    : never;

// 使用示例
type EmailAddress = ValidEmail<'user@example.com'>;  // 'user@example.com'
type WebAddress = ValidUrl<'https://example.com'>;   // 'https://example.com'
// type InvalidEmail = ValidEmail<'invalid-email'>;   // never
```

## 🔍 模式匹配与推断

### 🎯 字符串分拆技术

```typescript
// 1. 基础分拆模式
type SplitByDot<S extends string> = S extends `${infer First}.${infer Rest}`
    ? [First, ...SplitByDot<Rest>]
    : [S];

type PathSegments = SplitByDot<'api.users.123'>;  // ['api', 'users', '123']

// 2. 分隔符通用化
type Split<S extends string, D extends string> = 
    S extends `${infer First}${D}${infer Rest}`
        ? [First, ...Split<Rest, D>]
        : [S];

type CommaSplit = Split<'a,b,c,d', ','>;          // ['a', 'b', 'c', 'd']
type SlashSplit = Split<'path/to/file', '/'>;     // ['path', 'to', 'file']
type SpaceSplit = Split<'hello world', ' '>;      // ['hello', 'world']

// 3. 去除前后缀
type RemovePrefix<T, U extends string> = T extends `${U}${infer R}` ? R : T;
type RemoveSuffix<T, U extends string> = T extends `${infer R}${U}` ? R : T;

type CleanRoute = RemovePrefix<'/api/users', '/api'>;  // '/users'
type CleanFilename = RemoveSuffix<'file.ts', '.ts'>;   // 'file'

// 4. 提取路径组件
type ExtractPath<Path extends string> = Path extends `/${infer Route}`
    ? Route
    : Path;

type RouteRoot = ExtractPath<'/api/users'>;      // 'api/users'
type SubRoute = ExtractPath<'api/users'>;       // 'api/users'
```

### 🔄 递归字符串处理

```typescript
// 1. 深度路径解析
type ParsePathSegment<P extends string> = P extends `/${infer Head}/${infer Tail}`
    ? [Head, ...ParsePathSegment<`/${Tail}`>]
    : P extends `/${infer Head}`
    ? [Head]
    : P extends `${infer Only}`
    ? [Only]
    : [];

type DeepPath = ParsePathSegment<'/api/users/123/profile'>;  // ['api', 'users', '123', 'profile']

// 2. 驼峰转换
type ToCamelCase<S extends string> = S extends `${infer First}_${infer Rest}`
    ? `${Lowercase<First>}${Capitalize<ToCamelCase<Rest>>}`
    : Lowercase<S>;

type SnakeToCamel = ToCamelCase<'user_first_name'>;  // 'userFirstName'

// 3. 首字母转换
type ToSnakeCase<S extends string> = S extends `${infer First}${infer Rest}`
    ? Rest extends Uncapitalize<Rest>
        ? `${Lowercase<First>}${ToSnakeCase<Rest>}`
        : `${Lowercase<First>}_${ToSnakeCase<Uncapitalize<Rest>>}`
    : S;

type CamelToSnake = ToSnakeCase<'firstName'>;  // 'first_name'

// 4. 大小写转换工具
type ToLowerCase<S extends string> = S extends `${infer F}${infer R}`
    ? F extends 'A' ? `a${ToLowerCase<R>}`
    : F extends 'B' ? `b${ToLowerCase<R>}`
    : F extends 'C' ? `c${ToLowerCase<R>}`
    // ... 更多字母映射
    : `${F}${ToLowerCase<R>}`
    : S;
```

## 🚀 高级字符串操作

### 🎭 API 路由类型构建

```typescript
// 1. RESTful API 路由
interface RouteDefinition {
    path: string;
    method: HTTPMethod;
    handler: string;
}

type ApiRoutes = {
    '/users': {
        GET: 'getUsers';
        POST: 'createUser';
    };
    '/users/:id': {
        GET: 'getUser';
        PUT: 'updateUser';
        DELETE: 'deleteUser';
    };
};

// 生成 API 路径类型
type ApiPath = keyof ApiRoutes;

// 生成处理器类型
type GetHandler<P extends ApiPath, M extends keyof ApiRoutes[P]> = 
    ApiRoutes[P][M];

type GetUserRoute = GetHandler<'/users', 'GET'>;      // 'getUsers'
type CreateUserRoute = GetHandler<'/users', 'POST'>; // 'createUser'

// 2. 动态路由参数提取
type ExtractParams<T extends string> = T extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractParams<`/${Rest}`>
    : T extends `${string}:${infer Param}`
        ? Param
        : never;

type RouteParams = ExtractParams<'/users/:id/posts/:postId'>;  // 'id' | 'postId'

// 3. 路径参数替换
type ReplaceParams<T extends string, P extends Record<string, string>> = 
    T extends `${infer Start}:${infer Param}/${infer Rest}`
        ? Param extends keyof P
            ? `${Start}${P[Param]}/${ReplaceParams<`/${Rest}`, P>}`
            : `${Start}:${Param}/${ReplaceParams<`/${Rest}`, P>}`
        : T extends `${infer Start}:${infer Param}`
            ? Param extends keyof P
                ? `${Start}${P[Param]}`
                : `${Start}:${Param}`
            : T;

type ReplacedPath = ReplaceParams<'/users/:id', { id: '123' }>;  // '/users/123'
```

### 🔧 CSS 类名构建器

```typescript
// 1. CSS 类名静态检查
type CSSClass = 
    | 'btn'
    | 'btn-primary'
    | 'btn-secondary'
    | 'btn-sm'
    | 'btn-lg'
    | 'card'
    | 'card-header'
    | 'card-body'
    | 'form'
    | 'form-group'
    | 'form-control';

type ValidCSSClass<T extends string> = T extends CSSClass ? T : never;

// 2. CSS 类名组合
type CombineClasses<C1 extends string, C2 extends string> = `${C1} ${C2}`;

type ButtonClass = CombineClasses<'btn', 'btn-primary'>;  // 'btn btn-primary'

// 3. 主题系统类型
type Theme = 'light' | 'dark' | 'auto';
type ThemePrefix = 'theme-';

type ThemedClass<Base extends string, ThemeType extends Theme> = 
    `${Base} ${ThemePrefix}${ThemeType}`;

type ThemedButton = ThemedClass<'btn', 'dark'>;  // 'btn theme-dark'

// 4. 响应式类名
type Breakpoint = 'xs' | 'sm' | 'md' | 'lg' | 'xl';
type ResponsiveClass<T extends string, B extends Breakpoint> = 
    `${T}-${B}`;

type ResponsiveButton = ResponsiveClass<'btn', 'md'>;  // 'btn-md'
```

## 📚 字符串类型工具库

### 🛠️ 通用字符串工具

```typescript
// 1. 字符串长度
type StringLength<S extends string> = S extends `${infer First}${infer Rest}`
    ? Rest extends ''
        ? 1
        : StringLength<Rest> extends number
            ? 1 + StringLength<Rest>
            : never
    : 0;

type LengthExample = StringLength<'hello'>;  // 5

// 2. 字符串反转
type StringReverse<S extends string> = S extends `${infer First}${infer Rest}`
    ? `${StringReverse<Rest>}${First}`
    : '';

type ReverseExample = StringReverse<'hello'>;  // 'olleh'

// 3. 字符串替换
type ReplaceOnce<S extends string, From extends string, To extends string> = 
    S extends `${infer Before}${From}${infer After}`
        ? `${Before}${To}${After}`
        : S;

type ReplaceAll<S extends string, From extends string, To extends string> = 
    S extends `${infer Before}${From}${infer After}`
        ? `${ReplaceAll<Before, From, To>}${To}${ReplaceAll<After, From, To>}`
        : S;

type Replaced = ReplaceAll<'hello world', ' ', '_'>;  // 'hello_world'

// 4. 开始和结束检查
type StartsWith<S extends string, Prefix extends string> = 
    S extends `${Prefix}${string}` ? true : false;

type EndsWith<S extends string, Suffix extends string> = 
    S extends `${string}${Suffix}` ? true : false;

type HasPrefix = StartsWith<'hello world', 'hello'>;  // true
type HasSuffix = EndsWith<'hello world', 'world'>;    // true
```

### 🎯 高级字符串模式

```typescript
// 1. 语义化版本号解析
type SemVer = `${number}.${number}.${number}`;

type ParseVersion<V extends SemVer> = V extends `${infer Major}.${infer Minor}.${infer Patch}`
    ? { major: Major; minor: Minor; patch: Patch }
    : never;

type VersionInfo = ParseVersion<'1.2.3'>;  // { major: '1'; minor: '2'; patch: '3' }

// 2. 文件路径操作
type Basename<P extends string> = P extends `${infer Start}/${infer End}`
    ? End extends ''
        ? Start
        : Basename<End>
    : P;

type Dirname<P extends string> = P extends `${infer Start}/${infer End}`
    ? End extends ''
        ? Start
        : Start extends ''
            ? ''
            : `${Start}/${Dirname<End>}`
    : '';

type FileExtension<P extends string> = P extends `${string}.${infer Ext}`
    ? Ext
    : never;

type FileBasenameEx = Basename<'/path/to/file.ts'>;   // 'file.ts'
type FileDirnameEx = Dirname<'/path/to/file.ts'>;    // '/path/to'
type FileExtEx = FileExtension<'file.ts'>;           // 'ts'

// 3. 模板字面量 DSL
type SQLSelect<T extends string> = `SELECT * FROM ${T}`;
type SQLWhere<T extends string> = `WHERE ${T}`;
type SQLQuery<T extends string> = `${SQLSelect<T>}` | `${SQLSelect<T>} ${SQLWhere<string>}`;

type UserQuery = SQLQuery<'users'>;  // 'SELECT * FROM users' | 'SELECT * FROM users WHERE ...'
```

## 🎪 性能优化与最佳实践

### ⚡ 性能考虑

```typescript
// 1. 避免过度深层递归
type ShallowSplit<S extends string, D extends string, Depth extends number = 3> = 
    Depth extends 0 
        ? [S]
        : S extends `${infer First}${D}${infer Rest}`
            ? [First, ...ShallowSplit<Rest, D, Prev<Depth>>]
            : [S];

type Prev<T extends number> = [...Array<T>, never] extends [infer A, ...infer _]
    ? A extends number ? A : never
    : never;

// 2. 缓存复杂字符串操作
type CachedStringOp<T extends string> = T extends infer U
    ? U extends string
        ? `${U}_processed`
        : U
    : never;

// 3. 批量字符串操作
type BatchStringTransform<T extends string[], Op extends string> = {
    [K in keyof T]: `${T[K]}_${Op}`;
};

type TransformedStrings = BatchStringTransform<['hello', 'world'], 'processed'>;
// ['hello_processed', 'world_processed']
```

### 🎯 设计模式

```typescript
// 1. 字符串工厂模式
type StringFactory<T extends Record<string, any>> = {
    [K in keyof T]: T[K] extends string ? `API_${T[K]}` : T[K];
};

// 2. 字符串验证器
type StringValidator<T extends string> = T extends `${string}@${string}.${string}`
    ? T
    : 'Invalid email format';

// 3. 字符串转换链
type ConversionChain<T extends string> = 
    ToCamelCase<T> extends infer U
        ? U extends string
            ? Capitalize<U>
            : U
        : T;
```

### 🔗 相关深入学习

- [[04-Mapped-Types工具类型库]] - 映射类型工具
- [[03-Conditional-Types深度应用]] - 条件类型机制
- [[02-Type-Inference揭秘]] - 类型推断原理

---
*💡 模板字面量类型是TypeScript字符串编程的核心，掌握这些技巧能构建出强类型约束的字符串操作系统*
