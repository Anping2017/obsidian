# TypeScript Union & Intersection 实战

## 🎯 联合与交叉类型深度应用

### 📊 类型系统架构

```mermaid
graph TD
    A[Union & Intersection] --> B[Union Types]
    A --> C[Intersection Types]
    A --> D[Discriminated Unions]
    
    B --> B1[Basic Union]
    B --> B2[Literal Union]
    B --> B3[Union with Never]
    
    C --> C1[Interface Intersection]
    C --> C2[Mixin Pattern]
    C preference --> C3[Constrained Intersection]
    
    D --> D1[Tagged Union]
    D --> D2[State Machine]
    D --> D3[API Response]
```

## 🔗 Union Types 联合类型实战

### 💡 基础联合类型应用

```typescript
// 1. 状态管理联合类型
type LoadingState = 'loading';
type SuccessState = 'success';
type ErrorState = 'error';
type IdleState = 'idle';

type AppState = LoadingState | SuccessState | ErrorState | IdleState;

function handleState(state: AppState): string {
    switch (state) {
        case 'loading':
            return 'Data is loading...';
        case 'success':
            return 'Operation completed successfully';
        case 'error':
            return 'An error occurred';
        case 'idle':
            return 'Ready to start';
        default:
            // TypeScript 会确保所有情况都被处理
            const exhaustiveCheck: never = state;
            return exhaustiveCheck;
    }
}

// 2. 函数返回值联合
type AsyncResult<T> = 
    | { status: 'pending' }
    | { status: 'success'; data: T }
    | { status: 'error'; message: string };

function processRequest<T>(fn: () => Promise<T>): AsyncResult<T> {
    return { status: 'pending' };
}

// 3. 类型安全的事件处理器
type EventType = 
    | { type: 'click'; x: number; y: number }
    | { type: 'move'; deltaX: number; deltaY: number }
    | { type: 'resize'; width: number; height: number };

function handleEvent(event: EventType): void {
    switch (event.type) {
        case 'click':
            console.log(`Clicked at (${event.x}, ${event.y})`);
            break;
        case 'move':
            console.log(`Moved by ${event.deltaX}px horizontally`);
            break;
        case 'resize':
            console.log(`Resized to ${event.width}x${event.height}`);
            break;
    }
}
```

### 🎯 高级联合类型技巧

```typescript
// 1. 条件联合类型
type NonNullable<T> = T extends null | undefined ? never : T;

function processValue<T>(value: T): NonNullable<T> {
    if (value === null || value === undefined) {
        throw new Error('Value cannot be null or undefined');
    }
    // 在这个点之后，TypeScript 知道 value 不是 null 或 undefined
    return value;
}

// 2. 分布式条件类型
type ToArray<T> = T extends any ? T[] : never;
type StringArrayOrNumberArray = ToArray<string | number>;  // string[] | number[]

type Extract<T, U> = T extends U ? T : never;
type StringOnly = Extract<string | number | boolean, string | number>;  // string | number

// 3. 基于联合的映射类型
type MapUnion<T> = T extends any 
    ? { [K in T]: T }
    : never;

type MappedExample = MapUnion<'a' | 'b' | 'c'>;  // { a: 'a'; b: 'b'; c: 'c' }

// 4. 递归联合类型
type DeepArray<T> = T | DeepArray<T>[];

const deepStringArray: DeepArray<string> = [
    'hello',
    ['world', ['deep', ['nesting']]]
];

function flatten<T>(arr: DeepArray<T>): T[] {
    if (!Array.isArray(arr)) {
        return [arr];
    }
    return arr.flatMap(flatten);
}
```

## 🔧 Intersection Types 交叉类型实战

### 🎪 接口交叉应用

```typescript
// 1. 功能组合模式
interface Flyable {
    fly(): void;
    altitude: number;
}

interface Swimmable {
    swim(): void;
    depth: number;
}

interface Walkable {
    walk(): void;
    speed: number;
}

// 组合不同的能力
type FlyingFish = Swimmable & Flyable;
type Bird = Flyable & Walkable;
type Duck = Flyable & Swimmable & Walkable;

class Duck implements Duck {
    altitude: number = 0;
    depth: number = 0;
    speed: number = 5;

    fly(): void {
        console.log('Duck is flying');
        this.altitude = 100;
    }

    swim(): void {
        console.log('Duck is swimming');
        this.depth = 1;
    }

    walk(): void {
        console.log('Duck is walking');
    }
}

// 2. 混入模式实现
interface Timestamped {
    createdAt: Date;
    updatedAt: Date;
}

interface Auditable {
    createdBy: string;
    updatedBy: string;
}

interface Versioned {
    version: number;
}

type Entity = Timestamped & Auditable & Versioned;

class Document implements Entity {
    id: string;
    title: string;
    createdAt: Date;
    updatedAt: Date;
    createdBy: string;
    updatedBy: string;
    version: number;

    constructor(title: string, userId: string) {
        this.id = crypto.randomUUID();
        this.title = title;
        this.createdAt = new Date();
        this.updatedAt = new Date();
        this.createdBy = userId;
        this.updatedBy = userId;
        this.version = 1;
    }

    updateTitle(newTitle: string, userId: string): void {
        this.title = newTitle;
        this.updatedAt = new Date();
        this.updatedBy = userId;
        this.version++;
    }
}
```

### 🔨 泛型约束交叉

```typescript
// 1. 约束条件交叉
type NonNullable<T> = T extends null | undefined ? never : T;

function mergeObjects<T extends Record<string, any>, U extends Record<string, any>>(
    obj1: NonNullable<T>,
    obj2: NonNullable<U>
): T & U {
    return { ...obj1, ...obj2 };
}

const result = mergeObjects(
    { name: 'Alice', age: 25 },
    { city: 'Beijing', country: 'China' }
);  // { name: string; age: number; city: string; country: string }

// 2. 条件交叉类型
type ConditionalExtend<T, U> = T extends U ? T : T & U;

interface BaseConfig {
    debug: boolean;
    timeout: number;
}

interface ExtendedConfig {
    cacheSize: number;
    retries: number;
}

type SmartConfig<T extends boolean> = T extends true 
    ? BaseConfig & ExtendedConfig
    : BaseConfig;

function createConfig<T extends boolean>(useExtended: T): SmartConfig<T> {
    const baseConfig: BaseConfig = { debug: false, timeout: 5000 };
    
    if (useExtended) {
        return {
            ...baseConfig,
            cacheSize: 1000,
            retries: 3
        } as SmartConfig<T>;
    }
    
    return baseConfig as SmartConfig<T>;
}

const basicConfig = createConfig(false);     // BaseConfig
const extendedConfig = createConfig(true);    // BaseConfig & ExtendedConfig
```

## 🎭 Discriminated Unions 判别联合实战

### 🏷️ 标签联合模式

```typescript
// 1. API 响应判别联合
interface LoadingResponse {
    status: 'loading';
}

interface SuccessResponse<T> {
    status: 'success';
    data: T;
    cached?: boolean;
}

interface ErrorResponse {
    status: 'error';
    error: {
        code: string;
        message: string;
        details?: Record<string, any>;
    };
}

type ApiResponse<T> = LoadingResponse | SuccessResponse<T> | ErrorResponse;

// 响应处理器
function handleApiResponse<T>(response: ApiResponse<T>): void {
    switch (response.status) {
        case 'loading':
            console.log('Request is loading...');
            break;
            
        case 'success':
            console.log('Request successful:', response.data);
            if (response.cached) {
                console.log('Data served from cache');
            }
            break;
            
        case 'error':
            console.error(`Error ${response.error.code}:`, response.error.message);
            if (response.error.details) {
                console.error('Details:', response.error.details);
            }
            break;
    }
}

// 2. 状态机实现
type GameState = 
    | { state: 'menu' }
    | { state: 'playing'; score: number; level: number }
    | { state: 'paused'; previousState: Exclude<GameState, { state: 'menu' }> }
    | { state: 'gameOver'; finalScore: number };

class GameStateManager {
    private currentState: GameState = { state: 'menu' };

    transitionToState(newState: GameState): void {
        this.currentState = newState;
        this.handleStateTransition();
    }

    private handleStateTransition(): void {
        switch (this.currentState.state) {
            case 'menu':
                this.showMenu();
                break;
                
            case 'playing':
                this.startGamePlay();
                break;
                
            case 'paused':
                this.pauseGame();
                break;
                
            case 'gameOver':
                this.showGameOverScreen();
                break;
        }
    }

    private showMenu(): void {
        console.log('Showing main menu');
    }

    private startGamePlay(): void {
        console.log(`Starting level ${this.currentState.level}, score: ${this.currentState.score}`);
    }

    private pauseGame(): void {
        const previousState = this.currentState.previousState;
        console.log(`Game paused, was in ${previousState.state} state`);
    }

    private showGameOverScreen(): void {
        console.log(`Game Over! Final Score: ${this.currentState.finalScore}`);
    }
}
```

### 🎯 复杂判别联合

```typescript
// 1. 表单验证判别联合
interface PendingValidation {
    status: 'pending';
}

interface ValidField<T> {
    status: 'valid';
    value: T;
}

interface InvalidField<T> {
    status: 'invalid';
    value: T;
    errors: string[];
}

type FieldState<T> = PendingValidation | ValidField<T> | InvalidField<T>;

class FormField<T> {
    private state: FieldState<T> = { status: 'pending' };
    private validators: Array<(value: T) => string | null> = [];

    constructor(private initialValue: T) {}

    addValidator(validator: (value: T) => string | null): this {
        this.validators.push(validator);
        return this;
    }

    setValue(value: T): void {
        const errors: string[] = [];
        
        for (const validator of this.validators) {
            const error = validator(value);
            if (error) {
                errors.push(error);
            }
        }

        if (errors.length === 0) {
            this.state = { status: 'valid', value };
        } else {
            this.state = { status: 'invalid', value, errors };
        }
    }

    getValue(): T | undefined {
        switch (this.state.status) {
            case 'valid':
            case 'invalid':
                return this.state.value;
            case 'pending':
                return this.initialValue;
        }
    }

    isValid(): boolean {
        return this.state.status === 'valid';
    }

    getErrors(): string[] {
        switch (this.state.status) {
            case 'invalid':
                return this.state.errors;
            case 'valid':
            case 'pending':
                return [];
        }
    }
}

// 使用示例
const emailField = new FormField('')
    .addValidator(value => {
        if (!value.includes('@')) {
            return 'Invalid email format';
        }
        return null;
    })
    .addValidator(value => {
        if (value.length === 0) {
            return 'Email is required';
        }
        return null;
    });

emailField.setValue('invalid-email');
console.log(emailField.isValid());     // false
console.log(emailField.getErrors());   // ['Invalid email format']

emailField.setValue('user@example.com');
console.log(emailField.isValid());     // true
console.log(emailField.getErrors());   // []
```

## 🚀 高级实战应用

### 🔄 类型状态管理

```typescript
// 1. Redux 风格的状态管理
interface State {
    user: UserState;
    ui: UiState;
    api: ApiState;
}

type UserState = 
    | { status: 'loading' }
    | { status: 'authenticated'; user: User }
    | { status: 'anonymous' }
    | { status: 'error'; message: string };

type UiState = {
    theme: 'light' | 'dark';
    sidebarOpen: boolean;
    notifications: Notification[];
};

type ApiState = 
    | { status: 'idle' }
    | { status: 'loading' }
    | { status: 'success'; lastFetch: Date }
    | { status: 'error'; error: string };

// Action 联合类型
type UserAction = 
    | { type: 'USER_LOGIN_START' }
    | { type: 'USER_LOGIN_SUCCESS'; payload: User }
    | { type: 'USER_LOGOUT' }
    | { type: 'USER_LOGIN_ERROR'; payload: string };

type UiAction = 
    | { type: 'UI_TOGGLE_THEME' }
    | { type: 'UI_TOGGLE_SIDEBAR' }
    | { type: 'UI_ADD_NOTIFICATION'; payload: Notification };

type ApiAction = 
    | { type: 'API_REQUEST_START' }
    | { type: 'API_REQUEST_SUCCESS' }
    | { type: 'API_REQUEST_ERROR'; payload: string };

type AppAction = UserAction | UiAction | ApiAction;

// Reducer 实现
function userReducer(state: UserState, action: UserAction): UserState {
    switch (action.type) {
        case 'USER_LOGIN_START':
            return { status: 'loading' };
            
        case 'USER_LOGIN_SUCCESS':
            return { status: 'authenticated', user: action.payload };
            
        case 'USER_LOGOUT':
            return { status: 'anonymous' };
            
        case 'USER_LOGIN_ERROR':
            return { status: 'error', message: action.payload };
            
        default:
            return state;
    }
}
```

### 🎯 性能优化技巧

```typescript
// 1. 预计算联合类型
type PrecomputedUnion = 'a' | 'b' | 'c' | 'd' | 'e';

// 使用 const assertion 提升性能
const VALID_STATES = ['pending', 'success', 'error', 'idle'] as const;
type ComputedStates = typeof VALID_STATES[number];  // 'pending' | 'success' | 'error' | 'idle'

// 2. 缓存复杂联合类型检查
const unionTypeGuard = <T>(value: unknown, validTypes: readonly T[]): value is T => {
    return validTypes.includes(value as T);
};

const isValidState = (state: unknown): state is ComputedStates => {
    return unionTypeGuard(state, VALID_STATES);
};

// 3. 联合类型的映射优化
type UnionToIntersection<T> = 
    (T extends any ? (x: T) => void : never) extends ((x: infer U) => void) ? U : never;

type TestUnion = { a: number } | { b: string };
type TestIntersection = UnionToIntersection<TestUnion>;  // { a: number } & { b: string }
```

## 📚 最佳实践总结

### 🎯 设计原则

1. **明确性**: 每个联合类型都应该有明确的标签
2. **完整性**: 使用 `never` 类型确保所有情况都被处理
3. **性能**: 预计算和使用 const assertion
4. **可读性**: 使用有意义的类型名称和结构

### 🔗 相关深入学习

- [[03-Conditional-Types深度应用]] - 条件类型高级用法
- [[01-Type-Guards类型守护]] - 类型守护机制
- [[04-Mapped-Types工具类型库]] - 映射类型工具

---
*💡 联合和交叉类型是TypeScript强大类型系统的核心，掌握它们能让您的代码更加类型安全和表达力更强*
