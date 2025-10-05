# TypeScript 条件类型深度应用

## 🎯 条件类型核心机制

### 📊 条件类型架构

```mermaid
graph TD
    A[Conditional Types] --> B[Basic Syntax]
    A --> C[Distributive Types]
    A --> D[Inference Types]
    A --> E[Utility Types]
    
    B --> B[B1][T extends U ? X : Y]
    B --> B2[Ternary Operator]
    
    C --> C1[Union Distribution]
    C --> C2[Array Elements]
    
    D --> D1[infer Keyword]
    D --> D2[Type Inference]
    
    E --> E1[Extract/Omit]
    E --> E2[NonNullable]
```

## 🔍 基础条件类型

### 💡 语法与基本应用

```typescript
// 1. 基础条件类型语法
type IsString<T> = T extends string ? true : false;

type Test1 = IsString<string>;      // true
type Test2 = IsString<number>;      // false
type Test3 = IsString<string | number>; // boolean (true | false)

// 2. 类型选择器
type NonNullable<T> = T extends null | undefined ? never : T;

type CleanString = NonNullable<string | null>;        // string
type CleanNumber = NonNullable<number | undefined>;  // number
type CleanMixed = NonNullable<string | null | number | undefined>; // string | number

// 3. 嵌套条件类型
type DeepCheck<T> = T extends string 
    ? T extends 'hello'
        ? 'greeting'
        : T extends 'goodbye'
            ? 'farewell'
            : 'unknown string'
    : T extends number
        ? 'numeric'
        : 'other';

type GreetingResult = DeepCheck<'hello'>;       // 'greeting'
type FarewellResult = DeepCheck<'goodbye'>;     // 'farewell'
type NumericResult = DeepCheck<42>;             // 'numeric'
type OtherResult = DeepCheck<{}>;               // 'other'
```

### 🎪 复杂条件表达式

```typescript
// 1. 多条件嵌套
type TypeCategory<T> = T extends string
    ? 'text'
    : T extends number
        ? 'numeric'
        : T extends boolean
            ? 'boolean'
            : T extends Function
                ? 'function'
                : 'object';

type StringCategory = TypeCategory<string>;     // 'text'
type NumberCategory = TypeCategory<number>;      // 'numeric'
type BooleanCategory = TypeCategory<boolean>;    // 'boolean'
type FunctionCategory = TypeCategory<() => void>; // 'function'
type ObjectCategory = TypeCategory<{}>;          // 'object'

// 2. 使用工具类型结合条件
type ConditionalArray<T> = T extends string | number 
    ? T[]
    : T extends object
        ? Partial<T>[]
        : never[];

type StringArray = ConditionalArray<string>;        // string[]
type ObjectArray = ConditionalArray<{ a: string }>; // Partial<{ a: string }>[]
type NeverArray = ConditionalArray<symbol>;         // never[]

// 3. 条件类型递归
type DeepReadonly<T> = T extends object
    ? T extends Function
        ? T
        : { readonly [P in keyof T]: DeepReadonly<T[P]> }
    : T;

interface DeepObject {
    level1: {
        level2: {
            value: string;
            array: number[];
        };
    };
}

type DeepReadonlyTest = DeepReadonly<DeepObject>;
// 全部属性都变为 readonly
```

## 🚀 Infer 关键字深度应用

### 🔧 类型提取技巧

```typescript
// 1. 函数返回类型提取
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

type StringReturn = ReturnType<() => string>;        // string
type NumberReturn = ReturnType<(x: number) => number>; // number
type ComplexReturn = ReturnType<(a: string, b: number) => boolean>; // boolean

// 2. 函数参数类型提取
type Parameters<T> = T extends (...args: infer P) => any ? P : never;

type NoParams = Parameters<() => void>;               // []
type StringParam = Parameters<(x: string) => void>;   // [string]
type MultiParams = Parameters<(a: string, b: number) => void>; // [string, number]

// 3. 构造函数参数类型
type ConstructorParameters<T> = T extends new (...args: infer P) => any ? P : never;

class ExampleClass {
    constructor(public name: string, public age: number) {}
}

type ExampleParams = ConstructorParameters<typeof ExampleClass>; // [string, number]

// 4. 实例类型提取
type InstanceType<T> = T extends new (...args: any[]) => infer R ? R : never;

type ExampleInstance = InstanceType<typeof ExampleClass>; // ExampleClass
```

### 🎯 高级 infer 模式

```typescript
// 1. 数组元素类型提取
type ArrayElement<T> = T extends (infer U)[] ? U : never;

type StringArrayElement = ArrayElement<string[]>;     // string
type NumberArrayElement = ArrayElement<number[]>;     // number
type MixedArrayElement = ArrayElement<(string | number)[]>; // string | number

// 2. Promise 类型提取
type Awaited<T> = T extends Promise<infer U> ? U : T;

type StringPromise = Awaited<Promise<string>>;        // string
type NestedPromise = Awaited<Promise<Promise<number>>>; // number
type NonPromise = Awaited<string>;                    // string

// 3. 递归类型提取
type DeepArrayElement<T> = T extends (infer U)[]
    ? U extends (infer V)[]
        ? DeepArrayElement<V>
        : U
    : T;

type DeepString = DeepArrayElement<string[][][]>;     // string
type DeepNumber = DeepArrayElement<number[[]]>;       // number

// 4. 可选类型提取
type OptionalKeys<T> = {
    [K in keyof T]-?: {} extends Pick<T, K> ? K : never;
}[keyof T];

type RequiredKeys<T> = keyof T extends OptionalKeys<T> ? never : {
    [K in keyof T]-?: {} extends Pick<T, K> ? never : K;
}[keyof T];

interface ExampleInterface {
    required: string;
    optional?: number;
    alsoOptional?: boolean;
}

type OptionalFields = OptionalKeys<ExampleInterface>; // "optional" | "alsoOptional"
type RequiredFields = RequiredKeys<ExampleInterface>; // "required"
```

## 🔀 分布式条件类型

### 🎪 Union 类型分发

```typescript
// 1. 分布式条件类型基础
type ToArray<T> = T extends any ? T[] : never;

type StringOrNumberArray = ToArray<string | number>; // string[] | number[]
// 相当于：
// ToArray<string> | ToArray<number> = string[] | number[]

// 2. 非分布式条件类型
type ToNonDistributiveArray<T> = [T] extends [any] ? T[] : never;

type StringOrNumberNonDistributive = ToNonDistributiveArray<string | number>;
// (string | number)[]

// 3. 条件类型的实际应用
type Extract<T, U> = T extends U ? T : never;

type StringOrNumber = Extract<string | number | boolean, string | number>;
// string | number

type OmitNever<T> = {
    [K in keyof T]: T[K] extends never ? never : T[K];
};

interface MixedInterface {
    stringProp: string;
    neverProp: never;
    numberProp: number;
}

type CleanInterface = OmitNever<MixedInterface>;
// { stringProp: string; numberProp: number; }
```

### 🔧 实用工具类型实现

```typescript
// 1. Flatten 扁平化
type Flatten<T> = T extends (infer U)[]
    ? U extends (infer V)[]
        ? Flatten<V>
        : U
    : T;

type FlattenedResult = Flatten<string[][][]>; // string

// 2. Deep Flatten 递归扁平化
type DeepFlatten<T> = T extends unknown[]
    ? {
        [K in keyof T]: T[K] extends unknown[]
            ? DeepFlatten<T[K]>
            : T[K]
    }[number]
    : T;

type DeepFlattened = DeepFlatten<[1, [2, [3, [4]]]]>; // number

// 3. Tuple to Union 元组转联合
type TupleToUnion<T> = T extends readonly (infer U)[] ? U : never;

type StringTuple = TupleToUnion<['a', 'b', 'c']>; // 'a' | 'b' | 'c'
type NumberTuple = TupleToUnion<[1, 2, 3]>;       // 1 | 2 | 3

// 4. 反转元组
type Reverse<T extends readonly unknown[]> = T extends readonly [infer Head, ...infer Tail]
    ? [...Reverse<Tail>, Head]
    : [];

type Reversed = Reverse<[1, 2, 3, 4]>; // [4, 3, 2, 1]
```

## 🎭 高级实战应用

### 🏗️ 类型谓词与条件类型

```typescript
// 1. 智能类型守护
type IsArray<T> = T extends unknown[] ? true : false;

function safeArrayAccess<T>(value: T): IsArray<T> extends true ? T : never {
    return Array.isArray(value) ? value : undefined as any;
}

const stringArray = safeArrayAccess(['a', 'b', 'c']);     // string[]
const notArray = safeArrayAccess('hello');               // never

// 2. 条件泛型约束
type ConditionalConstraint<T> = T extends string
    ? { value: T; isString: true }
    : T extends number
        ? { value: T; isNumber: true }
        : { value: T; isOther: true };

function processConditional<T>(input: T): ConditionalConstraint<T> {
    if (typeof input === 'string') {
        return { value: input, isString: true } as ConditionalConstraint<T>;
    } else if (typeof input === 'number') {
        return { value: input, isNumber: true } as ConditionalConstraint<T>;
    }
    return { value: input, isOther: true } as ConditionalConstraint<T>;
}

const stringResult = processConditional('hello');    // { value: string; isString: true }
const numberResult = processConditional(42);         // { value: number; isNumber: true }
const otherResult = processConditional({});         // { value: {}; isOther: true }
```

### 🎯 复杂类型推导

```typescript
// 1. 路径类型推导
type Paths<T> = T extends object ? {
    [K in keyof T]: K extends string
        ? `${K}` | `${K}.${Paths<T[K]>}`
        : never;
}[keyof T] : '';

interface ComplexObject {
    user: {
        name: string;
        profile: {
            email: string;
            settings: {
                theme: 'light' | 'dark';
            };
        };
    };
    config: {
        api: string;
    };
}

type ObjectPaths = Paths<ComplexObject>;
// "user" | "config" | "user.name" | "user.profile" | "config.api" | "user.profile.email" | "user.profile.settings" | "user.profile.settings.theme"

// 2. 值类型推导
type PathValue<T, P extends string> = 
    P extends keyof T ? T[P] :
    P extends `${infer K}.${infer Rest}` ?
        K extends keyof T ? PathValue<T[K], Rest> : never :
    never;

type UserName = PathValue<ComplexObject, 'user.name'>;              // string
type UserEmail = PathValue<ComplexObject, 'user.profile.email'>;    // string
type Theme = PathValue<ComplexObject, 'user.profile.settings.theme'>; // 'light' | 'dark'
```

## 📚 性能优化与最佳实践

### ⚡ 性能考虑

```typescript
// 1. 避免深度递归
type LimitedDepth<T, Depth extends number = 3> = 
    Depth extends 0 ? T :
    T extends object ? {
        [K in keyof T]: LimitedDepth<T[K], Prev<Depth>>
    } : T;

type Prev<T extends number> = [...Array<T>, never] extends [infer A, ...infer _]
    ? A extends number ? A : never
    : never;

// 2. 缓存复杂类型
type Memoized<T> = T extends infer U 
    ? U extends object
        ? { readonly [K in keyof U]: Memoized<U[K]> }
        : U
    : never;

// 3. 简化条件表达式
type SimpleCondition<T> = T extends string ? 'string' : T extends number ? 'number' : 'other';

// 避免过度嵌套
type AvoidNesting<T> = Cond1<T> extends true
    ? Cond2<T> extends true
        ? Cond3<T> extends true
            ? 'deep'
            : 'level2'
        : 'level1'
    : 'none';
```

### 🎯 设计模式

```typescript
// 1. 类型工厂模式
type TypeFactory<T extends string> = T extends 'user'
    ? { id: string; name: string }
    : T extends 'product'
        ? { id: string; title: string; price: number }
        : T extends 'order'
            ? { id: string; userId: string; items: string[] }
            : never;

type UserType = TypeFactory<'user'>;      // { id: string; name: string }
type ProductType = TypeFactory<'product'>; // { id: string; title: string; price: number }

// 2. 代理模式
type Proxied<T> = {
    [K in keyof T]: T[K] extends Function ? T[K] & { _orig: T[K] } : T[K]
};

// 3. 装饰器模式
type Decorated<T, D extends Record<string, any>> = T & {
    [K in keyof D]: D[K]
};
```

### 🔗 相关深入学习

- [[02-Union-and-Intersection实战]] -  union & intersection 类型
- [[04-Mapped-Types工具类型库]] - 映射类型工具集
- [[05-Template-Literals字符串魔法]] - 模板字面量类型

---
*💡 条件类型是TypeScript的类型编程核心，掌握条件类型能让您构建更加智能和强大的类型系统*
