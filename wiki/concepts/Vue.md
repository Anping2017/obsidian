---
title: Vue
type: concept
tags: [cs, web, frontend, mature]
sources: [raw/计算机/开发学习/框架/]
created: 2026-05-05
updated: 2026-05-05
summary: Vue 是尤雨溪 2014 年发布的渐进式前端框架,通过响应式数据、模板语法、单文件组件提供低门槛开发体验,3.0 引入 Composition API 与 Proxy 响应式重写。
---

# Vue

## 定义

**Vue.js** 是尤雨溪(Evan You)2014 年开源的渐进式 JavaScript 框架。设计哲学是"渐进式采用":可作为页面局部增强,也可基于 Vue 生态做完整 SPA。Vue 在易用性、性能、文档质量上长期保持高水准,中国开发者用户基数尤大。

## 核心要点

### 1. 模板语法

```vue
<template>
  <button @click="count++">{{ count }}</button>
</template>
<script setup>
import { ref } from 'vue';
const count = ref(0);
</script>
```

模板更接近 HTML,条件 `v-if`、循环 `v-for`、绑定 `:href` / `@click`、双向 `v-model` 一目了然。

### 2. 响应式系统(Reactivity)

Vue 2 用 `Object.defineProperty` 劫持每个属性的 getter/setter,无法监听新增属性、数组索引修改等(需 Vue.set)。Vue 3(2020)用 ES6 [[Proxy]] 重写,完整代理对象操作,响应式更纯粹。

```js
const state = reactive({ count: 0 });
const doubled = computed(() => state.count * 2);
watch(() => state.count, (n) => console.log(n));
```

### 3. Options API vs Composition API

| 维度 | Options API(Vue 2/3) | Composition API(Vue 3) |
|---|---|---|
| 写法 | `data/methods/computed/watch` 选项 | `setup()` 内 ref/computed/watch 函数 |
| 复用 | mixin(命名冲突) | 自定义 composable 函数 |
| 类型推断 | 弱 | 强([[TypeScript类型系统]] 一等) |
| 心智 | 按"种类"分组 | 按"逻辑关注点"分组 |

`<script setup>` 是 Composition API 的语法糖,顶层声明即暴露给模板,几乎零仪式。

### 4. 单文件组件(SFC)

`.vue` 文件三段:`<template>` `<script>` `<style scoped>`。`scoped` 自动作用域隔离样式,无需 [[CSS-in-JS]]。

### 5. 与 React 对比

| 维度 | [[React]] | Vue 3 |
|---|---|---|
| UI | JSX(JS 表达式) | 模板(指令优化) |
| 状态 | 不可变 + setState | 可变响应式 |
| 编译优化 | 运行时 vDOM | 模板编译期标记静态节点 |
| 路由/状态 | 第三方 | 官方 vue-router/Pinia |
| 学习曲线 | 中(JS 重) | 低(HTML 友好) |

### 6. 编译期优化

Vue 3 编译器分析模板,标记静态节点 + PatchFlag,运行时跳过不变部分,渲染速度比 Vue 2 快 1.3-2 倍。

### 7. 生态

- **路由**:Vue Router(官方)
- **状态**:[[Pinia状态管理]](官方,取代 Vuex)
- **元框架**:Nuxt(SSR/SSG/Hybrid)、VitePress
- **UI 库**:Element Plus、Ant Design Vue、Vuetify、Naive UI
- **构建**:[[Vite]](尤雨溪同作者)
- **类型**:[[TypeScript类型系统]] 全面支持

### 8. 影响

Vue 启发了响应式数据流的简洁感,推动 [[SolidJS]]、Svelte 等"响应式优先"框架,也回流影响 React Signals 提案。

## 关系

- 对比:[[React]] 同为主流前端框架
- 兄弟:[[Svelte]]、[[SolidJS]]、[[Angular]]
- 状态:[[Pinia状态管理]](官方推荐)
- 构建:[[Vite]] 默认搭档
- 元框架:Nuxt = Vue 版 [[Next.js]]
- 类型:[[TypeScript类型系统]]
- 模板:编译期优化,与 [[虚拟DOM]] 路线区别

## 参考源

- raw/计算机/开发学习/框架/
- raw/计算机/开发学习/项目/扫码程序/(部分用 Vue)
