# Hello TypeScript 实践项目

## 🎯 项目目标

通过构建一个完整的用户管理程序，深入体验 TypeScript 的核心特性和最佳实践。

## 🏗️ 项目结构设计

```
hello-typescript/
├── src/
│   ├── models/          # 数据模型
│   ├── services/        # 业务逻辑
│   ├── utils/           # 工具函数
│   ├── types/           # 类型定义
│   └── index.ts         # 入口文件
├── tests/               # 测试文件
├── package.json         # 项目配置
├── tsconfig.json        # TypeScript 配置
└── README.md           # 项目说明
```

## 📋 核心类型定义

### 🎪 用户管理系统的类型架构

```typescript
// src/types/user.ts
export interface User {
    readonly id: number;
    name: string;
    email: string;
    age: number;
    role: UserRole;
    isActive: boolean;
    createdAt: Date;
}

export type UserRole = 'admin' | 'moderator' | 'user';
export type SortField = 'name' | 'email' | 'age' | 'createdAt';
export type SortDirection = 'asc' | 'desc';

export interface CreateUserRequest {
    name: string;
    email: string;
    age: number;
    role?: UserRole;
}

export interface UpdateUserRequest {
    name?: string;
    email?: string;
    age?: number;
    role?: UserRole;
    isActive?: boolean;
}
```

### 🛠️ 服务层接口设计

```typescript
// src/types/service.ts
export interface UserService {
    createUser(userData: CreateUserRequest): User;
    getUserById(id: number): User | null;
    updateUser(id: number, updates: UpdateUserRequest): User | null;
    deleteUser(id: number): boolean;
    listUsers(options?: ListUsersOptions): User[];
}

export interface ListUsersOptions {
    sortBy?: SortField;
    sortDirection?: SortDirection;
    filter?: UserFilter;
    limit?: number;
    offset?: number;
}

export interface UserFilter {
    role?: UserRole;
    isActive?: boolean;
    ageRange?: {
        min?: number;
        max?: number;
    };
}
```

## 🏭 业务逻辑实现

### 📦 用户模型类

```typescript
// src/models/User.ts
import { User, CreateUserRequest, UpdateUserRequest } from '../types/user';

export class UserModel implements User {
    readonly id: number;
    public name: string;
    public email: string;
    public age: number;
    public role: UserRole;
    public isActive: boolean;
    readonly createdAt: Date;

    constructor(data: CreateUserRequest & { id?: number }) {
        this.id = data.id ?? this.generateId();
        this.name = data.name;
        this.email = data.email;
        this.age = data.age;
        this.role = data.role ?? 'user';
        this.isActive = true;
        this.createdAt = new Date();
        
        this.validate();
    }

    private generateId(): number {
        return Math.floor(Math.random() * 1000000);
    }

    private validate(): void {
        if (this.age < 0 || this.age > 150) {
            throw new Error('Age must be between 0 and 150');
        }
        
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(this.email)) {
            throw new Error('Invalid email format');
        }
    }

    public update(updates: UpdateUserRequest): void {
        if (updates.age !== undefined) {
            if (updates.age < 0 || updates.age > 150) {
                throw new Error('Age must be between 0 and 150');
            }
            this.age = updates.age;
        }
        
        if (updates.email !== undefined) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(updates.email)) {
                throw new Error('Invalid email format');
            }
            this.email = updates.email;
        }

        if (updates.name !== undefined) this.name = updates.name;
        if (updates.role !== undefined) this.role = updates.role;
        if (updates.isActive !== undefined) this.isActive = updates.isActive;
    }
}
```

### 🔧 用户服务实现

```typescript
// src/services/UserService.ts
import { UserModel } from '../models/User';
import { 
    UserService, 
    CreateUserRequest, 
    UpdateUserRequest, 
    ListUsersOptions 
} from '../types/service';

export class InMemoryUserService implements UserService {
    private users: Map<number, UserModel> = new Map();
    private nextId: number = 1;

    createUser(userData: CreateUserRequest): User {
        const user = new UserModel({ ...userData, id: this.nextId++ });
        this.users.set(user.id, user);
        return this.createUserResponse(user);
    }

    getUserById(id: number): User | null {
        const user = this.users.get(id);
        return user ? this.createUserResponse(user) : null;
    }

    updateUser(id: number, updates: UpdateUserRequest): User | null {
        const user = this.users.get(id);
        if (!user) return null;

        user.update(updates);
        return this.createUserResponse(user);
    }

    deleteUser(id: number): boolean {
        return this.users.delete(id);
    }

    listUsers(options: ListUsersOptions = {}): User[] {
        let users = Array.from(this.users.values());

        // 应用过滤器
        if (options.filter) {
            users = this.filterUsers(users, options.filter);
        }

        // 排序
        if (options.sortBy) {
            users = this.sortUsers(users, options.sortBy, options.sortDirection);
        }

        // 分页
        const offset = options.offset ?? 0;
        const limit = options.limit ?? users.length;

        return users
            .slice(offset, offset + limit)
            .map(user => this.createUserResponse(user));
    }

    private createUserResponse(user: UserModel): User {
        return {
            id: user.id,
            name: user.name,
            email: user.email,
            age: user.age,
            role: user.role,
            isActive: user.isActive,
            createdAt: user.createdAt
        };
    }

    private filterUsers(users: UserModel[], filter: any): UserModel[] {
        return users.filter(user => {
            if (filter.role && user.role !== filter.role) return false;
            if (filter.isActive !== undefined && user.isActive !== filter.isActive) return false;
            
            if (filter.ageRange) {
                if (filter.ageRange.min !== undefined && user.age < filter.ageRange.min) return false;
                if (filter.ageRange.max !== undefined && user.age > filter.ageRange.max) return false;
            }
            
            return true;
        });
    }

    private sortUsers(users: UserModel[], field: string, direction = 'asc'): UserModel[] {
        return users.sort((a, b) => {
            let aValue: any, bValue: any;
            
            switch (field) {
                case 'name':
                case 'email':
                case 'age':
                case 'role':
                case 'isActive':
                    aValue = (a as any)[field];
                    bValue = (b as any)[field];
                    break;
                case 'createdAt':
                    aValue = a.createdAt.getTime();
                    bValue = b.createdAt.getTime();
                    break;
                default:
                    return 0;
            }

            if (aValue < bValue) return direction === 'asc' ? -1 : 1;
            if (aValue > bValue) return direction === 'asc' ? 1 : -1;
            return 0;
        });
    }
}
```

## 🛠️ 工具函数集合

### 📊 数据验证工具

```typescript
// src/utils/validators.ts
export class Validators {
    static isValidEmail(email: string): boolean {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    static isValidAge(age: number): boolean {
        return Number.isInteger(age) && age >= 0 && age <= 150;
    }

    static isValidName(name: string): boolean {
        return typeof name === 'string' && 
               name.trim().length >= 1 && 
               name.trim().length <= 50;
    }

    static validateUserData(data: any): { isValid: boolean; errors: string[] } {
        const errors: string[] = [];

        if (!this.isValidName(data.name)) {
            errors.push('Name must be between 1 and 50 characters');
        }

        if (!this.isValidEmail(data.email)) {
            errors.push('Invalid email format');
        }

        if (!this.isValidAge(data.age)) {
            errors.push('Age must be a valid integer between 0 and 150');

        return {
            isValid: errors.length === 0,
            errors
        };
    }
}
```

### 🎯 工具函数集合

```typescript
// src/utils/helpers.ts
export class Helpers {
    static generateId(): number {
        return Math.floor(Math.random() * 1000000);
    }

    static formatDate(date: Date): string {
        return date.toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    static sanitizeUserInput(input: string): string {
        return input.trim().replace(/[<>]/g, '');
    }

    static paginate<T>(array: T[], page: number, pageSize: number): {
        data: T[];
        total: number;
        page: number;
        totalPages: number;
    } {
        const total = array.length;
        const totalPages = Math.ceil(total / pageSize);
        const startIndex = (page - 1) * pageSize;
        const endIndex = startIndex + pageSize;
        const data = array.slice(startIndex, endIndex);

        return { data, total, page,的总页数: totalPages };
    }
}
```

## 🚀 主程序实现

### 📋 应用程序入口

```typescript
// src/index.ts
import { InMemoryUserService } from './services/UserService';
import { Validators } from './utils/validators';
import { Helpers } from './utils/helpers';

class UserManagementApp {
    private userService: InMemoryUserService;

    constructor() {
        this.userService = new InMemoryUserService();
        this.initializeSampleData();
    }

    private initializeSampleData(): void {
        // 创建示例用户
        const sampleUsers = [
            { name: "张三", email: "zhangsan@example.com", age: 25, role: "admin" as const },
            { name: "李四", email: "lisi@example.com", age: 30, role: "moderator" as const },
            { name: "王五", email: "wangwu@example.com", age: 28, role: "user" as const },
        ];

        sampleUsers.forEach(userData => {
            try {
                this.userService.createUser(userData);
                console.log(`✅ 创建用户: ${userData.name}`);
            } catch (error) {
                console.error(`❌ 创建用户失败: ${error.message}`);
            }
        });
    }

    public run(): void {
        console.log('\n🎉 Hello TypeScript 用户管理系统启动!');
        console.log('=====================================');

        this.displayAllProducts();
        this.demonstrateFeatures();
    }

    private displayAllProducts(): void {
        console.log('\n👥 当前用户列表:');
        const users = this.userService.listUsers({ sortBy: 'name' });
        
        if (users.length === 0) {
            console.log('   (暂无用户)');
            return;
        }

        users.forEach(user => {
            const status = user.isActive ? '✅' : '❌';
            const formattedDate = Helpers.formatDate(user.createdAt);
            console.log(`
   ${status} ${user.name} (ID: ${user.id})
     邮箱: ${user.email}
     年龄: ${user.age}岁
     角色: ${this.getRoleText(user.role)}
     创建时间: ${formattedDate}
            `);
        });
    }

    private demonstrateFeatures(): void {
        console.log('\n🔧 功能演示:');
        console.log('================');

        // 1. 创建新用户
        this.createNewUser();

        // 2. 搜索用户
        this.searchUsers();

        // 3. 更新用户
        this.updateUser();

        // 4. 删除用户
        this.deleteUser();

        // 5. 统计分析
        this.showStatistics();
    }

    private createNewUser(): void {
        console.log('\n1️⃣ 创建新用户:');
        const newUserData = {
            name: "赵六",
            email: "zhaoliu@example.com",
            age: 35,
            role: "user" as const
        };

        const validation = Validators.validateUserData(newUserData);
        if (validation.isValid) {
            try {
                const newUser = this.userService.createUser(newUserData);
                console.log(`✅ 成功创建用户: ${newUser.name} (ID: ${newUser.id})`);
            } catch (error) {
                console.log(`❌ 创建失败: ${error.message}`);
            }
        } else {
            console.log(`❌ 数据验证失败: ${validation.errors.join(', ')}`);
        }
    }

    private searchUsers(): void {
        console.log('\n2️⃣ 用户搜索:');

        // 按年龄范围搜索
        const youngUsers = this.userService.listUsers({
            filter: { ageRange: { min: 20, max: 30 } }
        });

        console.log(`👤 年龄20-30岁的用户: ${youngUsers.length}人`);
        youngUsers.forEach(user => {
            console.log(`   - ${user.name} (${user.age}岁)`);
        });

        // 按角色搜索
        const admins = this.userService.listUsers({
            filter: { role: 'admin' }
        });

        console.log(`👑 管理员用户: ${admins.length}人`);
    }

    private updateUser(): void {
        console.log('\n3️⃣ 更新用户信息:');

        const users = this.userService.listUsers();
        if (users.length > 0) {
            const targetUser = users[0];
            console.log(`更新用户: ${targetUser.name}`);

            const updates = {
                age: targetUser.age + 1,
                name: targetUser.name + ' (已更新)'
            };

            const updatedUser = this.userService.updateUser(targetUser.id, updates);
            if (updatedUser) {
                console.log(`✅ 更新成功: ${updatedUser.name}, 年龄: ${updatedUser.age}`);
            }
        }
    }

    private deleteUser(): void {
        console.log('\n4️⃣ 删除用户:');

        const users = this.userService.listUsers();
        if (users.length > 1) {
            const targetUser = users[1];
            console.log(`删除用户: ${targetUser.name}`);

            const success = this.userService.deleteUser(targetUser.id);
            if (success) {
                console.log(`✅ 删除成功: ${targetUser.name}`);
            } else {
                console.log(`❌ 删除失败: ${targetUser.name}`);
            }
        }
    }

    private showStatistics(): void {
        console.log('\n5️⃣ 用户统计:');
        
        const allUsers = this.userService.listUsers();
        const activeUsers = allUsers.filter(user => user.isActive);
        const adminCount = allUsers.filter(user => user.role === 'admin').length;
        const moderatorCount = allUsers.filter(user => user.role === 'moderator').length;
        const userCount = allUsers.filter(user => user.role === 'user').length;

        const avgAge = allUsers.reduce((sum, user) => sum + user.age, 0) / allUsers.length;

        console.log(`📊 用户统计信息:`);
        console.log(`   总用户数: ${allUsers.length}`);
        console.log(`   活跃用户: ${activeUsers.length}`);
        console.log(`   管理员: ${adminCount}人`);
        console.log(`   版主: ${moderatorCount}人`);
        console.log(`   普通用户: ${userCount}人`);
        console.log(`   平均年龄: ${avgAge.toFixed(1)}岁`);
    }

    private getRoleText(role: string): string {
        const roleMap: Record<string, string> = {
            admin: '🧑‍💼 管理员',
            moderator: '👮 版主',
            user: '👤 普通用户'
        };
        return roleMap[role] || '未知角色';
    }
}

// 启动应用程序
const app = new UserManagementApp();
app.run();

console.log('\n🎯 Hello TypeScript 实践完成!');
console.log('========================================');
console.log('✨ 这个项目展示了 TypeScript 的核心特性:');
console.log('   - 接口定义和类型安全');
console.log('   - 类的实现和封装');
console.log('   - 枚举和字面量类型');
console.log('   - 泛型和工具类型');
console.log('   - 错误处理和数据验证');
console.log('   - 模块化代码组织');
```

## 🧪 测试文件

### 🔍 单元测试示例

```typescript
// tests/UserModel.test.ts
import { UserModel } from '../src/models/User';

describe('UserModel', () => {
    test('应该正确创建用户', () => {
        const userData = {
            name: '测试用户',
            email: 'test@example.com',
            age: 25,
            role: 'user' as const
        };

        const user = new UserModel(userData);

        expect(user.name).toBe(userData.name);
        expect(user.email).toBe(userData.email);
        expect(user.age).toBe(userData.age);
        expect(user.role).toBe('user');
        expect(user.isActive).toBe(true);
        expect(user.createdAt).toBeInstanceOf(Date);
    });

    test('应该验证邮箱格式', () => {
        const invalidUserData = {
            name: '测试用户',
            email: 'invalid-email',
            age: 25
        };

        expect(() => new UserModel(invalidUserData)).toThrow();
    });

    test('应该验证年龄范围', () => {
        const invalidAgeData = {
            name: '测试用户',
            email: 'test@example.com',
            age: -5
        };

        expect(() => new UserModel(invalidAgeData)).toThrow();
    });
});
```

## 📋 项目配置

### ⚙️ package.json

```json
{
    "name": "hello-typescript",
    "version": "1.0.0",
    "description": "TypeScript 实践项目 - 用户管理系统",
    "main": "dist/index.js",
    "scripts": {
        "build": "tsc",
        "start": "node dist/index.js",
        "dev": "ts-node src/index.ts",
        "test": "jest",
        "dev:watch": "nodemon --exec ts-node src/index.ts"
    },
    "dependencies": {
        "typescript": "^5.0.0"
    },
    "devDependencies": {
        "@types/node": "^20.0.0",
        "jest": "^29.0.0",
        "@types/jest": "^29.0.0",
        "ts-jest": "^29.0.0",
        "ts-node": "^10.9.0",
        "nodemon": "^3.0.0"
    },
    "keywords": ["typescript", "node", "user-management", "learning"],
    "author": "TypeScript Learner",
    "license": "MIT"
}
```

### 🔧 tsconfig.json

```json
{
    "compilerOptions": {
        "target": "ES2022",
        "module": "CommonJS",
        "lib": ["ES2022"],
        "outDir": "./dist",
        "rootDir": "./src",
        "strict": true,
        "esModuleInterop": true,
        "skipLibCheck": true,
        "forceConsistentCasingInFileNames": true,
        "declaration": true,
        "sourceMap": true
    },
    "include": ["src/**/*"],
    "exclude": ["node_modules", "dist", "tests"]
}
```

## 🎯 运行和测试

### 🚀 项目运行

```bash
# 1. 安装依赖
npm install

# 2. 开发运行 (无需编译)
npm run dev

# 3. 编译并运行
npm run build && npm start

# 4. 运行测试
npm run test

# 5. 监听模式开发
npm run dev:watch
```

## 📚 学习总结

### ✨ 本项目展示的核心概念

| TypeScript 特性 | 应用示例 | 学习价值 |
|-----------------|----------|----------|
| **接口设计** | User, UserService 接口 | 类型契约定义 |
| **类实现** | UserModel 类 | 面向对象编程 |
| **类型注解** | 所有函数和变量 | 类型安全保障 |
| **泛型应用** | Map 数据结构 | 代码复用性 |
| **枚举类型** | UserRole 枚举 | 常量管理 |
| **类型守卫** | Validators 类 | 运行时类型检查 |
| **模块系统** | ES6 import/export | 代码组织 |

### 🎪 进阶学习建议

- [[01-Type-System入门]] - 深入理解类型系统原理
- [[01-Generics泛型精通]] - 掌握高阶泛型技巧
- [[03-Function-Types签名技巧]] - 函数类型设计

---
*💡 这是一个真实的项目示例，通过构建用户管理系统，您已经掌握了 TypeScript 的核心开发模式*
