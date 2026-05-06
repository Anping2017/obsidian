---
title: IndexedDB
type: concept
tags: [cs, web, frontend, storage, mature]
sources: [raw/计算机/开发学习/语言/HTML/04-知识拓展层/]
created: 2026-05-05
updated: 2026-05-05
summary: IndexedDB 是浏览器内置的 NoSQL 文档数据库,异步事务、索引查询、数百 MB-GB 级配额,是离线 Web 应用与大型客户端缓存的核心存储。
---

# IndexedDB

## 定义

**IndexedDB** 是 W3C 标准的浏览器内置数据库,2015 年成为正式推荐。它是**事务型 NoSQL 文档数据库**,以 key-value 为基础但支持索引、范围查询、版本迁移。与 localStorage(同步 + 5MB + 字符串)对比,IndexedDB 异步、可存数百 MB-GB 数据、支持任意 JS 对象与二进制(Blob、ArrayBuffer)。

## 核心要点

### 1. 概念层级

```
Database(数据库)
  └── Object Store(对象仓库,类似表)
        └── Record(记录,任意 JS 对象)
              ├── primary key
              └── indexes(可建二级索引)
```

### 2. 原始 API

```js
const req = indexedDB.open('app', 1);

req.onupgradeneeded = (e) => {
  const db = e.target.result;
  const store = db.createObjectStore('users', { keyPath: 'id' });
  store.createIndex('email', 'email', { unique: true });
};

req.onsuccess = (e) => {
  const db = e.target.result;
  const tx = db.transaction('users', 'readwrite');
  tx.objectStore('users').add({ id: 1, name: 'Alice', email: 'a@x.com' });
};
```

冗长是出名的难用。生产中用封装库。

### 3. 主流封装

| 库 | 风格 |
|---|---|
| **Dexie.js** | jQuery 风格链式,Promise 完整 |
| **idb**(Jake Archibald) | 轻量 Promise wrapper |
| **localForage** | LocalStorage API,后端自动选 IDB/WebSQL/LS |
| **RxDB** | NoSQL + 同步 + 加密,移动端首选 |
| **PouchDB** | CouchDB 协议,双向同步 |

```js
// Dexie 示例
import Dexie from 'dexie';
const db = new Dexie('app');
db.version(1).stores({ users: '++id, &email, name' });
await db.users.add({ name: 'Alice', email: 'a@x.com' });
const u = await db.users.where('email').equals('a@x.com').first();
```

### 4. 与其他客户端存储对比

| 存储 | 容量 | 同步/异步 | 内容 | 用途 |
|---|---|---|---|---|
| localStorage | ~5MB | 同步 | 字符串 | 简单设置 |
| sessionStorage | ~5MB | 同步 | 字符串 | 会话 |
| Cookies | ~4KB | 同步 | 字符串 | 认证 |
| IndexedDB | 数百 MB-GB | 异步 | 任意对象 + Blob | 离线大数据 |
| Cache Storage | 配额共享 | 异步 | Request/Response | [[Service Worker]] 缓存 |
| OPFS | 配额共享 | 异步 | 文件 | 文件系统(高性能) |

### 5. 配额(Quota)

浏览器按域名分配,通常占可用磁盘的 60-80%(共享于所有 Origin)。可:

```js
const { usage, quota } = await navigator.storage.estimate();
await navigator.storage.persist();  // 申请持久化,不被自动清理
```

### 6. 事务

- `readonly` / `readwrite` / `versionchange`
- 同一事务内多 Object Store 操作原子完成
- 自动提交(无需 commit),除非阻塞

### 7. 索引与查询

```js
db.users.where('age').between(18, 30).and(u => u.active).toArray();
```

支持范围、复合索引、`unique`、多值(MultiEntry)索引。

### 8. 应用场景

- **离线应用**:邮件、笔记(Notion、Trello)缓存
- **PWA 数据层**:Service Worker 取在线数据存 IDB
- **本地搜索**:Lunr.js + IDB
- **媒体缓存**:存视频片段实现伪流式
- **AI 应用**:Embeddings 本地向量库
- **客户端协作**:CRDT 状态持久化(Yjs、Automerge)

### 9. 注意

- 隐私模式下大多浏览器仅给少量配额或拒绝
- iOS Safari 7 天未访问会清空(intelligent tracking prevention)
- 跨标签页通过 `BroadcastChannel` + IDB 同步

## 关系

- 核心:[[PWA]] 离线数据层
- 配合:[[Service Worker]] Cache API
- 替代:localStorage(超大数据时)
- 工具:Dexie、idb、RxDB
- 对比:[[关系型数据库]] 服务端 vs 浏览器端

## 参考源

- raw/计算机/开发学习/语言/HTML/04-知识拓展层/现代Web平台/
