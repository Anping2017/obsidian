---
title: Pinia 状态管理
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/框架/]
created: 2026-05-05
updated: 2026-05-05
summary: Pinia 是 Vue 3 官方推荐的状态管理库,Vuex 5 的继任者,完全基于 Composition API 与 TypeScript,无 mutation 概念,语法极简。
---

# Pinia 状态管理

## 定义

**Pinia**(西班牙语"松果")是 Vue 核心团队成员 Eduardo San Martin Morote 创建的 [[Vue]] 状态管理库,2021 年成为 Vue 官方推荐,取代 Vuex 成为 Vuex 5 的实质形态。Pinia 完全基于 Composition API 与 [[TypeScript类型系统]] 设计,API 简洁、类型推断完美、DevTools 支持完整。

## 核心要点

### 1. 定义 Store

#### Options 风格(类似 Vuex)

```js
import { defineStore } from 'pinia';

export const useCounter = defineStore('counter', {
  state: () => ({ count: 0 }),
  getters: { double: (state) => state.count * 2 },
  actions: { inc() { this.count++; } }
});
```

#### Setup 风格(推荐)

```js
import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

export const useCounter = defineStore('counter', () => {
  const count = ref(0);
  const double = computed(() => count.value * 2);
  function inc() { count.value++; }
  return { count, double, inc };
});
```

### 2. 在组件中使用

```vue
<script setup>
import { storeToRefs } from 'pinia';
import { useCounter } from '@/stores/counter';

const counter = useCounter();
const { count, double } = storeToRefs(counter); // 保持响应式解构
counter.inc();
</script>
```

### 3. 与 Vuex 对比

| 维度 | Vuex 4 | Pinia |
|---|---|---|
| Mutation | 必需(冗余) | 取消(action 直接改) |
| Module | 嵌套 | 扁平,多 store 互引用 |
| TS 支持 | 中 | 极佳 |
| API 体积 | 较大 | 小 |
| Composition API | 后加 | 原生 |
| DevTools | 支持 | 支持 |

### 4. 多 Store 互引用

```js
import { useUserStore } from './user';

export const useCart = defineStore('cart', () => {
  const user = useUserStore();
  function checkout() {
    if (user.isLoggedIn) { ... }
  }
});
```

无需嵌套 module,直接调用其他 store 即可。

### 5. 持久化

```js
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

export const useStore = defineStore('app', {
  state: () => ({ token: '' }),
  persist: true   // 自动 localStorage
});
```

### 6. SSR 友好

[[Nuxt]] 自动集成 Pinia,SSR hydration 透明处理。

### 7. 设计哲学

- **直观**:写起来像写普通 ref
- **类型完美**:无 unknown,无 as cast
- **轻量**:核心约 1KB
- **可测试**:store 是普通函数,易 mock

### 8. 适用

所有 Vue 3 项目的默认选择;Vue 2.7+ 也可用。

## 关系

- 属于:[[Vue]] 官方生态
- 替代:Vuex 4
- 对应:[[React]] 的 [[Zustand状态管理]] / [[Redux状态管理]]
- 基于:Composition API + 响应式
- 类型:[[TypeScript类型系统]]

## 参考源

- raw/计算机/开发学习/框架/
