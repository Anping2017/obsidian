# README — Sprint 0 / Step 1

目标：**1）初始化前端+BFF 仓库 2）打通 Odoo JSON‑RPC 连通性 3）提供健康检查与可视化验证页**。

> 要求：Node.js **v20 LTS**；包管理器任选 **npm/pnpm/yarn**（下方以 npm 为例）。

---

## 目录结构
```
rt-headless/
├─ app/
│  ├─ api/
│  │  ├─ health/route.ts
│  │  └─ odoo/
│  │     └─ ping/route.ts
│  └─ page.tsx
├─ lib/
│  └─ odoo.ts
├─ .env.example
├─ next.config.ts
├─ package.json
├─ tsconfig.json
└─ README.md
```

---

## 快速开始
```bash
# 1) 初始化仓库
mkdir rt-headless && cd rt-headless && git init

# 2) 写入本项目中的文件（将本页文件保存到对应路径）

# 3) 安装依赖
npm i next@14 react react-dom
npm i -D typescript @types/node @types/react @types/react-dom eslint eslint-config-next

# 4) 复制环境变量模板并填写
cp .env.example .env.local
# 编辑 .env.local，填入你的 Odoo 开发环境参数

# 5) 启动本地开发
npm run dev
# 访问 http://localhost:3000 看到 Odoo 连通性状态
```

---

## .env.example
```ini
# Odoo 基本配置
ODOO_BASE_URL=https://odoo.example.co.nz
ODOO_DB=your_odoo_db
ODOO_USER=api_user@example.co.nz
ODOO_PASSWORD=your_password

# 可选：请求超时（毫秒）
ODOO_TIMEOUT_MS=10000
```

---

## package.json
```json
{
  "name": "rt-headless",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "next": "14.2.5",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/node": "^20.12.12",
    "@types/react": "^18.2.66",
    "@types/react-dom": "^18.2.22",
    "eslint": "^8.57.0",
    "eslint-config-next": "14.2.5",
    "typescript": "^5.4.5"
  }
}
```

---

## tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "allowJs": false,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "types": ["node"]
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
```

---

## next.config.ts
```ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactStrictMode: true,
}

export default nextConfig
```

---

## lib/odoo.ts — 轻量 Odoo JSON‑RPC 客户端（服务端专用）
```ts
// lib/odoo.ts
// Minimal Odoo JSON-RPC client for Next.js Route Handlers (Node runtime)

export type JsonRpc<T = unknown> = {
  jsonrpc: '2.0'
  id?: number | string | null
  method: 'call'
  params: T
}

function required(name: string, v?: string) {
  if (!v) throw new Error(`Missing env: ${name}`)
  return v
}

const ODOO_BASE_URL = required('ODOO_BASE_URL', process.env.ODOO_BASE_URL)
const ODOO_DB = required('ODOO_DB', process.env.ODOO_DB)
const ODOO_USER = required('ODOO_USER', process.env.ODOO_USER)
const ODOO_PASSWORD = required('ODOO_PASSWORD', process.env.ODOO_PASSWORD)
const ODOO_TIMEOUT_MS = Number(process.env.ODOO_TIMEOUT_MS ?? 10000)

export type OdooSession = { uid: number; session_id?: string; cookies?: string }

async function postJson(path: string, payload: any, cookie?: string) {
  const ctrl = new AbortController()
  const to = setTimeout(() => ctrl.abort(), ODOO_TIMEOUT_MS)
  try {
    const res = await fetch(new URL(path, ODOO_BASE_URL).toString(), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(cookie ? { Cookie: cookie } : {}),
      },
      body: JSON.stringify(payload),
      signal: ctrl.signal,
      // IMPORTANT: Next.js route handlers run on server — no need for credentials: 'include'
    })
    const setCookie = res.headers.get('set-cookie') || undefined
    const data = await res.json().catch(() => ({}))
    if (!res.ok || data.error) {
      throw new Error(
        `Odoo RPC error: HTTP ${res.status} ${(data && JSON.stringify(data.error)) || ''}`
      )
    }
    return { data, setCookie }
  } finally {
    clearTimeout(to)
  }
}

export async function authenticate(): Promise<OdooSession> {
  const payload: JsonRpc<{ db: string; login: string; password: string; context: Record<string, any> }> = {
    jsonrpc: '2.0',
    method: 'call',
    params: { db: ODOO_DB, login: ODOO_USER, password: ODOO_PASSWORD, context: {} },
  }
  const { data, setCookie } = await postJson('/web/session/authenticate', payload)
  const result = data?.result
  if (!result?.uid) throw new Error('Odoo auth failed: missing uid')

  // Try to extract session_id from JSON first, then fallback to Set-Cookie
  let session_id: string | undefined = result.session_id
  if (!session_id && setCookie) {
    const m = /session_id=([^;]+)/.exec(setCookie)
    if (m) session_id = m[1]
  }
  const cookies = session_id ? `session_id=${session_id}` : setCookie
  return { uid: result.uid, session_id, cookies }
}

export type CallKwArgs = {
  model: string
  method: string
  args?: any[]
  kwargs?: Record<string, any>
}

export async function callKw<T = unknown>(session: OdooSession, { model, method, args = [], kwargs = {} }: CallKwArgs): Promise<T> {
  const payload: JsonRpc<{ model: string; method: string; args: any[]; kwargs: Record<string, any> }> = {
    jsonrpc: '2.0',
    method: 'call',
    params: { model, method, args, kwargs },
  }
  const { data } = await postJson('/web/dataset/call_kw', payload, session.cookies)
  return data.result as T
}

// 一步到位的“认证+调用”
export async function withSession<T>(fn: (s: OdooSession) => Promise<T>) {
  const s = await authenticate()
  return fn(s)
}
```

---

## app/api/health/route.ts — 健康检查
```ts
import { NextResponse } from 'next/server'
export const runtime = 'nodejs'

export async function GET() {
  return NextResponse.json({ ok: true, ts: new Date().toISOString() })
}
```

---

## app/api/odoo/ping/route.ts — 连通性验证（认证 + 一个最小调用）
```ts
import { NextResponse } from 'next/server'
import { authenticate, callKw } from '@/lib/odoo'

export const runtime = 'nodejs'

export async function GET() {
  try {
    const session = await authenticate()
    // 用一个很轻的调用测试权限：统计 res.partner 数量（仅作连通性验证）
    const count = await callKw<number>(session, {
      model: 'res.partner',
      method: 'search_count',
      args: [[]],
      kwargs: {},
    })

    return NextResponse.json({ ok: true, uid: session.uid, partners: count })
  } catch (e: any) {
    return NextResponse.json({ ok: false, error: String(e?.message || e) }, { status: 500 })
  }
}
```

---

## app/page.tsx — 首页：显示 Odoo 连通性
```tsx
async function getPing() {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL ?? ''}/api/odoo/ping`, { cache: 'no-store' })
    if (!res.ok) throw new Error('Ping failed')
    return res.json()
  } catch (e) {
    return { ok: false, error: String(e) }
  }
}

export default async function Home() {
  const data = await getPing()
  const ok = data?.ok
  return (
    <main style={{ fontFamily: 'ui-sans-serif, system-ui', padding: 24 }}>
      <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: 12 }}>RT Headless — Odoo 连接状态</h1>
      <div style={{ padding: 16, border: '1px solid #e5e7eb', borderRadius: 12 }}>
        {ok ? (
          <>
            <p>✅ 已连接 Odoo</p>
            <p>UID: {data.uid}</p>
            <p>res.partner 数量: {data.partners}</p>
          </>
        ) : (
          <>
            <p>❌ 连接失败</p>
            <pre style={{ whiteSpace: 'pre-wrap' }}>{data?.error}</pre>
          </>
        )}
      </div>
      <p style={{ marginTop: 16, color: '#6b7280' }}>提示：若失败，请检查 .env.local 的 Odoo 参数与用户权限。</p>
    </main>
  )
}
```

---

## README.md（补充说明）

# RT Headless — Step 1

本阶段交付：
1. Next.js (App Router) + TypeScript 项目骨架
2. Odoo JSON-RPC 轻量客户端（服务端）
3. /api/health 与 /api/odoo/ping 两个路由
4. 首页可视化 Odoo 连通性

## 环境要求
- Node.js 20 LTS
- Odoo 开发/测试环境账户（有 basic read 权限）

## 常见问题
- **401/403**：检查 Odoo 用户/密码/数据库是否正确，或用户是否允许外部 API 访问。
- **超时**：调整 ODOO_TIMEOUT_MS；检查 VPN/专线/安全组。
- **CORS**：所有 RPC 在服务器端执行，无浏览器跨域问题；仅需保证 BFF → Odoo 网络可达。

## 下一步（Step 2 预告）
- 接入 Tailwind + shadcn/ui（组件库与主题 token）
- 设计 /api/products 列表（SSR/ISR）与 /api/pricing/compute 接口骨架
- 加入 Redis 短期缓存与日志追踪（Sentry）```



我已经把「**Step 1 — 项目初始化与 Odoo 连通性（可直接运行）**」代码骨架放到右侧（含目录结构、.env 模板、Next.js 路由、`lib/odoo.ts` 客户端、首页连通性页）。

照着这三步跑起来就行：

1. 在你的电脑上
    

- 安装 Node.js 20 LTS
    
- 在 Odoo 创建一个**测试用户**（有最小读权限），准备好 `ODOO_BASE_URL / ODOO_DB / ODOO_USER / ODOO_PASSWORD`
    
- 进入右侧文档写的命令：`npm i` → `cp .env.example .env.local` → 填好 Odoo 参数 → `npm run dev`
    

2. 打开 `http://localhost:3000`
    

- 看到 ✅ 即表示**已打通 Odoo**（会显示 uid 和 `res.partner` 数量）
    
- 失败就看页面上的错误提示按 README 的“常见问题”排查
    

3. 成功后，下一步我直接给你：
    

- Tailwind + shadcn/ui 接入（统一设计风格）
    
- `/api/products` 与 `/api/pricing/compute` 的接口骨架
    
- Redis 缓存与 Sentry 日志接入






# README — Step 2（在 Step 1 基础上继续）

本步交付：
1) 接入 **TailwindCSS + shadcn/ui** 基础样式与组件；
2) 新增 **产品列表 API：/api/products**（支持搜索/分页）；
3) 新增 **价格计算 API：/api/pricing/compute**（骨架，后续接 Odoo 价表）；
4) 内置 **轻量缓存**（Redis 优先，fallback 为内存 TTL）；
5) 提供 **/products** 页面与通用 Layout。

> 复制以下文件到 Step 1 的仓库相应路径，并按下文更新依赖与环境变量。

---

## 1) 依赖安装
```bash
npm i -D tailwindcss postcss autoprefixer
npm i class-variance-authority tailwind-merge lucide-react
# 如需 Redis：
npm i ioredis
```

---

## 2) 新增/更新文件

### package.json（追加依赖，不改变 scripts）
```json
{
  "devDependencies": {
    "autoprefixer": "^10.4.20",
    "postcss": "^8.4.47",
    "tailwindcss": "^3.4.10"
  },
  "dependencies": {
    "class-variance-authority": "^0.7.0",
    "lucide-react": "^0.452.0",
    "tailwind-merge": "^2.5.2",
    "ioredis": "^5.4.1"
  }
}
```

### tailwind.config.ts
```ts
import type { Config } from 'tailwindcss'

export default {
  darkMode: ['class'],
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      container: { center: true, padding: '1rem' },
      borderRadius: {
        xl: '0.75rem',
        '2xl': '1rem'
      }
    }
  },
  plugins: []
} satisfies Config
```

### postcss.config.js
```js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### app/globals.css
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root { --bg: #ffffff; --fg: #0f172a; }
body { background: var(--bg); color: var(--fg); }
```

### app/layout.tsx（新增全局布局）
```tsx
import './globals.css'
import Link from 'next/link'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen antialiased">
        <header className="sticky top-0 z-20 border-b bg-white/80 backdrop-blur">
          <div className="container flex h-14 items-center justify-between">
            <Link href="/" className="font-semibold">RT Headless</Link>
            <nav className="flex items-center gap-4 text-sm text-slate-600">
              <Link href="/products">Products</Link>
              <a href="/api/health" className="hidden sm:inline">Health</a>
            </nav>
          </div>
        </header>
        <main className="container py-6">{children}</main>
      </body>
    </html>
  )
}
```

### components/ui/button.tsx（shadcn 风格极简 Button）
```tsx
import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { twMerge } from 'tailwind-merge'

const buttonVariants = cva(
  'inline-flex items-center justify-center whitespace-nowrap rounded-2xl text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-400 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-slate-900 text-white hover:bg-slate-700',
        outline: 'border border-slate-200 hover:bg-slate-50',
        ghost: 'hover:bg-slate-50'
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 px-3',
        lg: 'h-11 px-5'
      }
    },
    defaultVariants: { variant: 'default', size: 'default' }
  }
)

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> {}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(({ className, variant, size, ...props }, ref) => (
  <button ref={ref} className={twMerge(buttonVariants({ variant, size }), className)} {...props} />
))
Button.displayName = 'Button'
```

### components/ui/card.tsx（shadcn 风格极简 Card）
```tsx
import * as React from 'react'
import { twMerge } from 'tailwind-merge'

export function Card({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={twMerge('rounded-2xl border bg-white shadow-sm', className)} {...props} />
}

export function CardHeader({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={twMerge('flex flex-col gap-1 border-b p-4', className)} {...props} />
}

export function CardTitle({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) {
  return <h3 className={twMerge('text-base font-semibold', className)} {...props} />
}

export function CardContent({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={twMerge('p-4', className)} {...props} />
}
```

### components/product-card.tsx
```tsx
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'

export type Product = {
  id: number
  sku: string
  name: string
  list_price: number
  qty_available?: number
}

export function ProductCard({ p }: { p: Product }) {
  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>{p.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-sm text-slate-600">SKU: {p.sku}</div>
        <div className="mt-2 text-lg font-semibold">${p.list_price.toFixed(2)}</div>
        {typeof p.qty_available === 'number' && (
          <div className="mt-1 text-xs text-slate-500">Stock: {p.qty_available}</div>
        )}
        <div className="mt-4">
          <Button>Add to Cart</Button>
        </div>
      </CardContent>
    </Card>
  )
}
```

### lib/cache.ts（Redis 优先，内存 TTL 兜底）
```ts
// lib/cache.ts
import type { Redis } from 'ioredis'
let redis: Redis | null = null

try {
  if (process.env.REDIS_URL) {
    const IORedis = require('ioredis') as typeof import('ioredis')
    redis = new IORedis(process.env.REDIS_URL as string)
  }
} catch {}

type Entry<T> = { v: T; exp: number }
const mem = new Map<string, Entry<any>>()

export async function cacheGet<T>(key: string): Promise<T | null> {
  if (redis) {
    const v = await redis.get(key)
    return v ? (JSON.parse(v) as T) : null
  }
  const e = mem.get(key)
  if (!e) return null
  if (Date.now() > e.exp) { mem.delete(key); return null }
  return e.v as T
}

export async function cacheSet<T>(key: string, val: T, ttlSec: number) {
  if (redis) {
    await redis.set(key, JSON.stringify(val), 'EX', ttlSec)
    return
  }
  mem.set(key, { v: val, exp: Date.now() + ttlSec * 1000 })
}
```

### lib/odoo-products.ts（产品查询与价钱映射占位）
```ts
import { withSession, callKw } from '@/lib/odoo'

export type RawProduct = {
  id: number
  name: string
  default_code?: string
  list_price: number
  qty_available?: number
}

export async function searchProducts({ q, limit = 12, offset = 0 }: { q?: string; limit?: number; offset?: number }) {
  return withSession(async (s) => {
    const domain: any[] = [[['sale_ok', '=', true]]].flat()
    if (q && q.trim()) {
      domain.push('|')
      domain.push(['name', 'ilike', q])
      domain.push(['default_code', 'ilike', q])
    }

    const fields = ['name', 'default_code', 'list_price', 'qty_available']

    const [total, items] = await Promise.all([
      callKw<number>(s, { model: 'product.product', method: 'search_count', args: [domain] }),
      callKw<RawProduct[]>(s, {
        model: 'product.product',
        method: 'search_read',
        args: [domain, fields],
        kwargs: { limit, offset, order: 'write_date desc' },
      }),
    ])

    const mapped = items.map((r) => ({
      id: r.id,
      sku: r.default_code || String(r.id),
      name: r.name,
      list_price: Number(r.list_price || 0),
      qty_available: typeof r.qty_available === 'number' ? r.qty_available : undefined,
    }))

    return { total, items: mapped }
  })
}

export async function computePriceForSkus({ skus }: { skus: string[] }) {
  // 占位：目前返回 list_price，后续接 Odoo 价表/客户等级
  return withSession(async (s) => {
    const domain: any[] = [['default_code', 'in', skus]]
    const fields = ['name', 'default_code', 'list_price']
    const items = await callKw<RawProduct[]>(s, { model: 'product.product', method: 'search_read', args: [domain, fields] })
    return items.map((r) => ({ sku: r.default_code || String(r.id), price: Number(r.list_price || 0) }))
  })
}
```

### app/api/products/route.ts（搜索/分页，带缓存）
```ts
import { NextResponse } from 'next/server'
import { cacheGet, cacheSet } from '@/lib/cache'
import { searchProducts } from '@/lib/odoo-products'

export const runtime = 'nodejs'

export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url)
    const q = searchParams.get('q') || undefined
    const page = Number(searchParams.get('page') || '1')
    const pageSize = Math.min(48, Math.max(1, Number(searchParams.get('pageSize') || '12')))
    const offset = (page - 1) * pageSize

    const key = `products:q=${q || ''}:p=${page}:s=${pageSize}`
    const cached = await cacheGet<any>(key)
    if (cached) return NextResponse.json({ ok: true, cached: true, ...cached })

    const data = await searchProducts({ q, limit: pageSize, offset })
    await cacheSet(key, data, 30) // 30s 短缓存

    return NextResponse.json({ ok: true, ...data })
  } catch (e: any) {
    return NextResponse.json({ ok: false, error: String(e?.message || e) }, { status: 500 })
  }
}
```

### app/api/pricing/compute/route.ts（骨架）
```ts
import { NextResponse } from 'next/server'
import { computePriceForSkus } from '@/lib/odoo-products'

export const runtime = 'nodejs'

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(() => ({}))
    const skus: string[] = Array.isArray(body?.skus) ? body.skus.slice(0, 200) : []
    if (!skus.length) return NextResponse.json({ ok: false, error: 'skus required' }, { status: 400 })

    const prices = await computePriceForSkus({ skus })
    return NextResponse.json({ ok: true, prices })
  } catch (e: any) {
    return NextResponse.json({ ok: false, error: String(e?.message || e) }, { status: 500 })
  }
}
```

### app/products/page.tsx（SSR 列表页：支持 ?q= 搜索）
```tsx
import Link from 'next/link'
import { ProductCard, type Product } from '@/components/product-card'

async function loadProducts(q?: string): Promise<{ total: number; items: Product[] }> {
  const url = new URL(`${process.env.NEXT_PUBLIC_BASE_URL ?? ''}/api/products`)
  if (q) url.searchParams.set('q', q)
  const res = await fetch(url, { cache: 'no-store' })
  if (!res.ok) throw new Error('Failed to load products')
  const data = await res.json()
  return { total: data.total ?? 0, items: data.items ?? [] }
}

export default async function ProductsPage({ searchParams }: { searchParams?: { q?: string } }) {
  const q = searchParams?.q
  const { total, items } = await loadProducts(q)

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Products {q ? `— “${q}”` : ''}</h1>
        <Link href="/?from=products" className="text-sm text-slate-600 hover:underline">Back to Home</Link>
      </div>

      <form action="/products" className="flex gap-2">
        <input name="q" defaultValue={q} placeholder="Search…" className="h-10 flex-1 rounded-2xl border px-3" />
        <button className="h-10 rounded-2xl border px-4 hover:bg-slate-50" type="submit">Search</button>
      </form>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {items.map((p) => (<ProductCard key={p.id} p={p} />))}
      </div>

      <div className="text-sm text-slate-500">Total: {total}</div>
    </div>
  )
}
```

---

## 3) 环境变量（新增可选）
```ini
# 可选 Redis（Upstash/ioredis 连接串）
REDIS_URL=redis://:password@host:6379/0

# 建议保留，SSR 拉取 API 的绝对地址（本地开发可不填）
NEXT_PUBLIC_BASE_URL=http://localhost:3000
```

---

## 4) 运行 & 验收
```bash
npm run dev
# 访问 /products，试试 ?q=iphone 或输入 SKU 片段
# 调用价格 API：
curl -X POST http://localhost:3000/api/pricing/compute -H 'Content-Type: application/json' -d '{"skus":["A2898","SM-A146P"]}'
```

---

## 5) 下一步（Step 3 预告）
- 接入 **AddressFinder**（地址自动完成）与 **NZ Post 运价接口**（BFF 封装）；
- 新增 **购物车/校验/锁定** API 与结算页骨架；
- 接入 **Windcave 3DS2** 沙箱支付流；
- 增加日志追踪（Sentry）与 API 结构化日志。



**Step 2 — UI（Tailwind+shadcn）与产品/价格接口（含缓存）**」放到右侧代码文档里，内容包括：

- Tailwind + 基础 shadcn 组件（Button、Card）与全局 Layout；
    
- `/api/products`（搜索/分页 + Redis/内存TTL缓存）；
    
- `/api/pricing/compute`（价格计算骨架，后续接 Odoo 价表）；
    
- `/products` 列表页（支持 ?q= 搜索）；
    
- 依赖安装与运行说明。
    

按文档步骤装依赖、启动后，先试试：

- 打开 `http://localhost:3000/products?q=iphone` 看能否列出产品；
    
- `POST /api/pricing/compute` 传入一些 SKU，返回的 `price` 目前等于 `list_price`（下步接入价表引擎）。




# README — Step 3

本步在 Step 1/2 基础上新增：
1) **购物车与结算骨架**：服务器侧购物车存储（Redis/内存兜底）、增删商品、校验与总价；
2) **地址自动完成**：BFF 代理 AddressFinder Autocomplete/Metadata；
3) **运价查询（NZ Post UAT）**：OAuth2 client_credentials 获取 token → 调用 ShippingOptions Domestic；
4) **Checkout 页面**：地址输入（自动完成）→ 试算运费 → 展示服务与总价。

> 将以下文件追加/更新到仓库，对照 `.env` 新增变量，`npm run dev` 即可。

---

## 1) 环境变量新增（.env.example）
```ini
# AddressFinder（NZ）
ADDRESSFINDER_KEY=your_key
ADDRESSFINDER_SECRET=your_secret
ADDRESSFINDER_DOMAIN=example.co.nz

# NZ Post（UAT 默认）
NZPOST_CLIENT_ID=your_client_id
NZPOST_CLIENT_SECRET=your_client_secret
NZPOST_ENV=uat  # uat 或 prod
NZPOST_ACCOUNT_NUMBER=12345678  # 可选：有合约价时建议传
```

---

## 2) 新增库：地址与运价

### lib/addressfinder.ts
```ts
// lib/addressfinder.ts
const AF_BASE = 'https://api.addressfinder.io'
const KEY = process.env.ADDRESSFINDER_KEY!
const SECRET = process.env.ADDRESSFINDER_SECRET!
const DOMAIN = process.env.ADDRESSFINDER_DOMAIN

function required(name: string, v?: string) {
  if (!v) throw new Error(`Missing env: ${name}`)
  return v
}

export async function afAutocomplete(q: string, opts?: { max?: number }) {
  required('ADDRESSFINDER_KEY', KEY)
  required('ADDRESSFINDER_SECRET', SECRET)
  const url = new URL('/api/nz/address/autocomplete', AF_BASE)
  url.searchParams.set('key', KEY)
  url.searchParams.set('secret', SECRET)
  url.searchParams.set('q', q)
  url.searchParams.set('format', 'json')
  if (opts?.max) url.searchParams.set('max', String(opts.max))
  if (DOMAIN) url.searchParams.set('domain', DOMAIN)

  const r = await fetch(url, { method: 'GET', headers: { Accept: 'application/json' }, cache: 'no-store' })
  if (!r.ok) throw new Error(`AF autocomplete ${r.status}`)
  return r.json()
}

export async function afMetadata({ pxid, dpid }: { pxid?: string; dpid?: string }) {
  required('ADDRESSFINDER_KEY', KEY)
  required('ADDRESSFINDER_SECRET', SECRET)
  const url = new URL('/api/nz/address/metadata', AF_BASE)
  url.searchParams.set('key', KEY)
  url.searchParams.set('secret', SECRET)
  url.searchParams.set('format', 'json')
  if (pxid) url.searchParams.set('pxid', pxid)
  if (dpid) url.searchParams.set('dpid', dpid)
  if (DOMAIN) url.searchParams.set('domain', DOMAIN)
  const r = await fetch(url, { method: 'GET', headers: { Accept: 'application/json' }, cache: 'no-store' })
  if (!r.ok) throw new Error(`AF metadata ${r.status}`)
  return r.json()
}
```

### lib/nzpost.ts
```ts
// lib/nzpost.ts — OAuth2 + ShippingOptions Domestic(UAT/Prod)
import { cacheGet, cacheSet } from '@/lib/cache'

const ENV = (process.env.NZPOST_ENV || 'uat').toLowerCase()
const TOKEN_URL = 'https://oauth.nzpost.co.nz/as/token.oauth2'
const BASE = ENV === 'prod' ? 'https://api.nzpost.co.nz' : 'https://api.uat.nzpost.co.nz'
const SHIPPING_OPTIONS_DOMESTIC = `${BASE}/shippingoptions/2.0/domestic`

async function getToken() {
  const ckey = `nzpost:token:${ENV}`
  const cached = await cacheGet<{ access_token: string; exp: number }>(ckey)
  if (cached && Date.now() < cached.exp) return cached.access_token

  const cid = process.env.NZPOST_CLIENT_ID
  const secret = process.env.NZPOST_CLIENT_SECRET
  if (!cid || !secret) throw new Error('Missing NZ Post client credentials')

  const body = new URLSearchParams()
  body.set('grant_type', 'client_credentials')
  body.set('client_id', cid)
  body.set('client_secret', secret)

  const res = await fetch(TOKEN_URL, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body })
  if (!res.ok) throw new Error(`NZ Post token ${res.status}`)
  const json = (await res.json()) as { access_token: string; token_type: string; expires_in: number }
  const exp = Date.now() + Math.max(60_000, (json.expires_in || 86400) * 1000 - 120_000)
  await cacheSet(ckey, { access_token: json.access_token, exp }, Math.floor((exp - Date.now()) / 1000))
  return json.access_token
}

export type DomesticRateInput = {
  weightKg: number
  lengthCm: number
  widthCm: number
  heightCm?: number
  diameterCm?: number
  pickup?: { suburb?: string; city?: string; postcode?: string; address_id?: string; dpid?: string; site_code?: string }
  delivery?: { suburb?: string; city?: string; postcode?: string; address_id?: string; dpid?: string; site_code?: string }
  account_number?: string
}

export async function getDomesticOptions(input: DomesticRateInput) {
  const token = await getToken()
  const params = new URLSearchParams()
  params.set('weight', String(input.weightKg))
  params.set('length', String(input.lengthCm))
  params.set('width', String(input.widthCm))
  if (input.heightCm) params.set('height', String(input.heightCm))
  if (input.diameterCm) params.set('diameter', String(input.diameterCm))

  const pick = input.pickup || {}
  const drop = input.delivery || {}
  if (pick.address_id) params.set('pickup_address_id', pick.address_id)
  else if (pick.dpid) params.set('pickup_dpid', pick.dpid)
  else {
    if (pick.suburb) params.set('pickup_suburb', pick.suburb)
    if (pick.city) params.set('pickup_city', pick.city)
    if (pick.postcode) params.set('pickup_postcode', pick.postcode)
  }
  if (drop.address_id) params.set('delivery_address_id', drop.address_id)
  else if (drop.dpid) params.set('delivery_dpid', drop.dpid)
  else {
    if (drop.suburb) params.set('delivery_suburb', drop.suburb)
    if (drop.city) params.set('delivery_city', drop.city)
    if (drop.postcode) params.set('delivery_postcode', drop.postcode)
  }

  const acct = input.account_number || process.env.NZPOST_ACCOUNT_NUMBER
  if (acct) params.set('account_number', acct)

  const url = `${SHIPPING_OPTIONS_DOMESTIC}?${params.toString()}`
  const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } })
  const data = await res.json()
  if (!res.ok) throw new Error(`NZ Post domestic ${res.status}: ${JSON.stringify(data)}`)
  return data as {
    success: boolean
    services: Array<{ carrier: string; description: string; service_code: string; price_including_gst: number; price_excluding_gst: number; service_standard?: string; tracking_included: boolean; signature_included: boolean; addons?: any[] }>
    rated_weight: number
    errors?: Array<{ code: string; message: string; details?: string }>
    message_id: string
  }
}
```

---

## 3) 新增库：购物车

### lib/cart.ts
```ts
// lib/cart.ts — 服务器侧购物车（Redis 优先，内存兜底）
import { cacheGet, cacheSet } from '@/lib/cache'
import { cookies } from 'next/headers'
import { randomUUID } from 'crypto'
import { computePriceForSkus } from '@/lib/odoo-products'

export type CartLine = { sku: string; name: string; qty: number }
export type Cart = { id: string; lines: CartLine[]; updatedAt: number }

const CART_COOKIE = 'cart_id'
const CART_TTL_SEC = 60 * 60 * 24 * 7 // 7d

function getCartKey(id: string) { return `cart:${id}` }

export async function getOrCreateCart(): Promise<Cart> {
  const jar = cookies()
  let id = jar.get(CART_COOKIE)?.value
  if (!id) {
    id = randomUUID()
    // 设置 httpOnly cookie（Route Handler 环境）
    jar.set(CART_COOKIE, id, { httpOnly: true, secure: true, sameSite: 'lax', path: '/', maxAge: CART_TTL_SEC })
  }
  const key = getCartKey(id)
  const existing = await cacheGet<Cart>(key)
  if (existing) return existing
  const blank: Cart = { id, lines: [], updatedAt: Date.now() }
  await cacheSet(key, blank, CART_TTL_SEC)
  return blank
}

export async function saveCart(cart: Cart) {
  cart.updatedAt = Date.now()
  await cacheSet(getCartKey(cart.id), cart, CART_TTL_SEC)
}

export async function addLine(sku: string, qty: number, name?: string) {
  const cart = await getOrCreateCart()
  const i = cart.lines.findIndex(l => l.sku === sku)
  if (i >= 0) cart.lines[i].qty += qty
  else cart.lines.push({ sku, qty, name: name || sku })
  await saveCart(cart)
  return cart
}

export async function removeLine(sku: string) {
  const cart = await getOrCreateCart()
  cart.lines = cart.lines.filter(l => l.sku !== sku)
  await saveCart(cart)
  return cart
}

export type CartTotals = { subtotal: number; items: Array<{ sku: string; name: string; qty: number; unit: number; total: number }> }

export async function computeTotals(cart: Cart): Promise<CartTotals> {
  if (!cart.lines.length) return { subtotal: 0, items: [] }
  const skus = cart.lines.map(l => l.sku)
  const prices = await computePriceForSkus({ skus }) // 目前使用 list_price，后续接价表
  const priceMap = new Map(prices.map(p => [p.sku, p.price]))
  const items = cart.lines.map(l => {
    const unit = Number(priceMap.get(l.sku) || 0)
    return { sku: l.sku, name: l.name, qty: l.qty, unit, total: unit * l.qty }
  })
  const subtotal = items.reduce((a, b) => a + b.total, 0)
  return { subtotal, items }
}
```

---

## 4) BFF 路由：Address、Shipping、Cart

### app/api/address/autocomplete/route.ts
```ts
import { NextResponse } from 'next/server'
import { afAutocomplete } from '@/lib/addressfinder'
export const runtime = 'nodejs'

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url)
  const q = searchParams.get('q') || ''
  if (!q.trim()) return NextResponse.json({ ok: true, completions: [] })
  try {
    const data = await afAutocomplete(q, { max: 8 })
    return NextResponse.json({ ok: true, ...data })
  } catch (e: any) {
    return NextResponse.json({ ok: false, error: String(e?.message || e) }, { status: 500 })
  }
}
```

### app/api/address/metadata/route.ts
```ts
import { NextResponse } from 'next/server'
import { afMetadata } from '@/lib/addressfinder'
export const runtime = 'nodejs'

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url)
  const pxid = searchParams.get('pxid') || undefined
  const dpid = searchParams.get('dpid') || undefined
  if (!pxid && !dpid) return NextResponse.json({ ok: false, error: 'pxid or dpid required' }, { status: 400 })
  try {
    const data = await afMetadata({ pxid, dpid })
    return NextResponse.json({ ok: true, ...data })
  } catch (e: any) {
    return NextResponse.json({ ok: false, error: String(e?.message || e) }, { status: 500 })
  }
}
```

### app/api/shipping/rate/route.ts
```ts
import { NextResponse } from 'next/server'
import { getDomesticOptions } from '@/lib/nzpost'

export const runtime = 'nodejs'

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(() => ({}))
    const input = {
      weightKg: Number(body.weightKg || 1),
      lengthCm: Number(body.lengthCm || 10),
      widthCm: Number(body.widthCm || 10),
      heightCm: body.heightCm ? Number(body.heightCm) : undefined,
      diameterCm: body.diameterCm ? Number(body.diameterCm) : undefined,
      pickup: body.pickup,
      delivery: body.delivery,
      account_number: body.account_number,
    }
    const data = await getDomesticOptions(input)
    return NextResponse.json({ ok: true, ...data })
  } catch (e: any) {
    return NextResponse.json({ ok: false, error: String(e?.message || e) }, { status: 500 })
  }
}
```

### app/api/cart/add/route.ts
```ts
import { NextResponse } from 'next/server'
import { addLine } from '@/lib/cart'
import { withSession, callKw } from '@/lib/odoo'

export const runtime = 'nodejs'

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(() => ({}))
    const sku = String(body.sku || '')
    const qty = Math.max(1, Number(body.qty || 1))
    if (!sku) return NextResponse.json({ ok: false, error: 'sku required' }, { status: 400 })

    // 从 Odoo 取名称做回显（可加库存校验）
    const name = await withSession(async (s) => {
      const rs = await callKw<any[]>(s, { model: 'product.product', method: 'search_read', args: [[['default_code', '=', sku]], ['name']], kwargs: { limit: 1 } })
      return rs?.[0]?.name || sku
    })

    const cart = await addLine(sku, qty, name)
    return NextResponse.json({ ok: true, cart })
  } catch (e: any) {
    return NextResponse.json({ ok: false, error: String(e?.message || e) }, { status: 500 })
  }
}
```

### app/api/cart/remove/route.ts
```ts
import { NextResponse } from 'next/server'
import { removeLine } from '@/lib/cart'

export const runtime = 'nodejs'

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(() => ({}))
    const sku = String(body.sku || '')
    if (!sku) return NextResponse.json({ ok: false, error: 'sku required' }, { status: 400 })
    const cart = await removeLine(sku)
    return NextResponse.json({ ok: true, cart })
  } catch (e: any) {
    return NextResponse.json({ ok: false, error: String(e?.message || e) }, { status: 500 })
  }
}
```

### app/api/cart/validate/route.ts
```ts
import { NextResponse } from 'next/server'
import { getOrCreateCart, computeTotals } from '@/lib/cart'
import { afMetadata } from '@/lib/addressfinder'
import { getDomesticOptions } from '@/lib/nzpost'

export const runtime = 'nodejs'

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(() => ({}))
    const cart = await getOrCreateCart()
    const totals = await computeTotals(cart)

    // 地址：优先 pxid→metadata 抽 dpid（NZ Post 推荐传 dpid 或 address_id）
    let delivery: any = body.delivery || {}
    if (delivery.pxid && !delivery.dpid) {
      const m = await afMetadata({ pxid: delivery.pxid })
      const meta = m?.completions?.[0]
      if (meta?.dpid) delivery = { ...delivery, dpid: String(meta.dpid), suburb: meta.post_suburb || meta.suburb, city: meta.mailtown || meta.city, postcode: meta.postcode }
    }

    // 简化：按购物车重量体积估算；真实项目请用具体商品维度累计
    const weightKg = Number(body.weightKg || 1)
    const lengthCm = Number(body.lengthCm || 10)
    const widthCm = Number(body.widthCm || 10)
    const heightCm = Number(body.heightCm || 10)

    let shipping: any = { success: true, services: [] }
    try {
      shipping = await getDomesticOptions({ weightKg, lengthCm, widthCm, heightCm, pickup: body.pickup, delivery })
    } catch (e) {
      shipping = { success: false, error: String(e) }
    }

    return NextResponse.json({ ok: true, cart, totals, shipping })
  } catch (e: any) {
    return NextResponse.json({ ok: false, error: String(e?.message || e) }, { status: 500 })
  }
}
```

---

## 5) Checkout 页面（含地址自动完成 & 运费试算）

### app/checkout/page.tsx
```tsx
'use client'
import { useEffect, useMemo, useState } from 'react'

function useDebounce<T>(v: T, ms: number) {
  const [d, setD] = useState(v)
  useEffect(() => { const t = setTimeout(() => setD(v), ms); return () => clearTimeout(t) }, [v, ms])
  return d
}

export default function CheckoutPage() {
  const [q, setQ] = useState('')
  const [list, setList] = useState<any[]>([])
  const [sel, setSel] = useState<{ pxid?: string; dpid?: string; label?: string } | null>(null)
  const dq = useDebounce(q, 200)

  useEffect(() => {
    if (!dq) { setList([]); return }
    fetch(`/api/address/autocomplete?q=${encodeURIComponent(dq)}`).then(r => r.json()).then(j => {
      setList(j?.completions || [])
    }).catch(() => setList([]))
  }, [dq])

  const [quote, setQuote] = useState<any | null>(null)
  const canQuote = useMemo(() => !!sel, [sel])

  async function handleQuote() {
    if (!sel) return
    // 取 metadata 获取 dpid
    const meta = await fetch(`/api/address/metadata?${sel.pxid ? `pxid=${sel.pxid}` : `dpid=${sel.dpid}`}`).then(r => r.json())
    const m = meta?.completions?.[0]
    const delivery = m ? { dpid: String(m.dpid), suburb: m.post_suburb || m.suburb, city: m.mailtown || m.city, postcode: m.postcode } : undefined

    const r = await fetch('/api/cart/validate', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ delivery, weightKg: 1, lengthCm: 10, widthCm: 10, heightCm: 10 })
    })
    const j = await r.json()
    setQuote(j)
  }

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-semibold">Checkout（试算）</h1>
      <div className="space-y-2">
        <label className="block text-sm font-medium">收货地址（自动完成）</label>
        <input value={q} onChange={e => { setQ(e.target.value); setSel(null) }} placeholder="例如：1 Queen Street, Auckland" className="h-10 w-full rounded-2xl border px-3" />
        {list.length > 0 && (
          <ul className="rounded-2xl border bg-white shadow-sm">
            {list.map((x: any) => (
              <li key={x.pxid} className="cursor-pointer px-3 py-2 hover:bg-slate-50" onClick={() => { setSel({ pxid: x.pxid, label: x.a }); setQ(x.a); setList([]) }}>{x.a}</li>
            ))}
          </ul>
        )}
      </div>

      <button className="h-10 rounded-2xl border px-4 hover:bg-slate-50 disabled:opacity-50" disabled={!canQuote} onClick={handleQuote}>试算运费</button>

      {quote && (
        <div className="space-y-3">
          <h2 className="text-lg font-semibold">运价选项</h2>
          {!quote.shipping?.success && <div className="text-red-600 text-sm">无法获取运价：{quote.shipping?.error}</div>}
          <ul className="space-y-2">
            {quote.shipping?.services?.map((s: any) => (
              <li key={s.service_code} className="rounded-2xl border p-3">
                <div className="font-medium">{s.description} <span className="text-slate-500">({s.carrier})</span></div>
                <div className="text-sm text-slate-600">{s.service_standard || '—'}</div>
                <div className="mt-1 font-semibold">${Number(s.price_including_gst).toFixed(2)} (GST incl.)</div>
              </li>
            ))}
          </ul>
          <div className="mt-4 text-sm text-slate-600">小计（不含运费）：${(quote.totals?.subtotal || 0).toFixed(2)}</div>
        </div>
      )}
    </div>
  )
}
```

---

## 6) 快速验证
```bash
# 1) 填好 AddressFinder/NZ Post 的 UAT 凭据
# 2) 重启开发服务器
npm run dev
# 3) 访问 /checkout，输入地址关键字，选择建议 → 点击“试算运费”
# 4) 用以下接口操纵购物车并再次试算：
#   添加：
curl -X POST http://localhost:3000/api/cart/add -H 'Content-Type: application/json' -d '{"sku":"A2898","qty":1}'
#   校验：
curl -X POST http://localhost:3000/api/cart/validate -H 'Content-Type: application/json' -d '{"delivery":{"dpid":"2727895"},"weightKg":1,"lengthCm":10,"widthCm":10,"heightCm":10}'
```

---

## 7) 说明与后续
- 当前价格计算仍以 `list_price` 为占位；下一步接 **Odoo 价表/客户等级**（`res.partner` -> pricelist）并引入**幂等下单**与**支付会话**；
- 运价参数暂以统一尺寸/重量估算，后续按 SKU 维度聚合体积重（Odoo product.dimensions / 自定义字段）；
- AddressFinder/Metadata→获取 `dpid`，优先向 NZ Post 传 `dpid` 或 `address_id`；
- 生产建议：所有外部 API 超时、熔断与重试（指数退避）+ 结构化日志。




**Step 3 已经就位**，我把完整代码与说明放到右侧文档里了（购物车/结算骨架 + AddressFinder 自动完成 + NZ Post 运价 UAT）。

你现在可以按文档跑通 `/checkout` 的**地址选择 → 运价试算**和**服务器侧购物车**。本步关键点用到的官方接口如下（以便你查验）：

- AddressFinder：
    
    - NZ 地址自动完成与参数（`key`、`secret`、`q` 等）。 [addressfinder.com](https://addressfinder.com/au/docs/api/nz/nz-address-autocomplete-api/)
        
    - NZ 地址元数据（根据 `pxid` 或 `dpid` 取 `dpid/postcode/city/suburb` 等）。 [addressfinder.com](https://addressfinder.com/au/docs/api/nz/nz-address-metadata-api/)
        
- NZ Post ShippingOptions（Domestic）：
    
    - UAT端点：`https://api.uat.nzpost.co.nz/shippingoptions/2.0/domestic`，必填维度/重量与地址字段；返回 `price_including_gst` 等。 [anypoint.mulesoft.com](https://anypoint.mulesoft.com/exchange/portals/nz-post-group/b8271f09-2ad8-4e1c-b6b1-322c5727d148/shippingoptions-api/minor/1.0/pages/Domestic/)
        
    - OAuth2 获取访问令牌（client_credentials 到 `https://oauth.nzpost.co.nz/as/token.oauth2`）。 [anypoint.mulesoft.com](https://anypoint.mulesoft.com/exchange/portals/nz-post-group/b8271f09-2ad8-4e1c-b6b1-322c5727d148/shippingoptions-api/minor/1.0/pages/Authentication/)




# README — Step 4（在 Step 1/2/3 基础上继续）

本步交付：
1) **价表/客户等级**：按门店（company/warehouse/pricelist）与客户（partner）计算价格；
2) **库存校验与锁定**：检查指定仓库可售量并生成短期锁定 token（Redis）；
3) **创建 Odoo sale.order 草稿**：按门店/客户与购物车生成订单；
4) **支付会话骨架**（Windcave 3DS2/HPP 占位）：创建支付会话（占位实现）与回调入口，后续替换为真实网关调用。

> 说明：定价与库存完全走 Odoo；BFF 仅做聚合与缓存。支付留出接口，可在收到商户参数后接入正式网关。

---

## 1) 环境变量新增（.env.example）
```ini
# —— 门店映射（JSON）——
# 约定：key 为前端的 store_key；value 为 Odoo 的 company/pricelist/warehouse id
STORE_MAP={
  "default": { "company_id": 1, "pricelist_id": 1, "warehouse_id": 1 },
  "albany": { "company_id": 2, "pricelist_id": 5, "warehouse_id": 3 }
}

# —— Windcave（占位）——
# 真实参数请向 Windcave 申请并按其 3DS2/HPP 文档配置
WINDCAVE_MERCHANT_ID=your_merchant_id
WINDCAVE_API_KEY=your_api_key
WINDCAVE_API_SECRET=your_api_secret
WINDCAVE_RETURN_URL=https://example.co.nz/payment/return
WINDCAVE_CALLBACK_URL=https://example.co.nz/api/payments/callback
```

---

## 2) 新增/更新库代码

### lib/store.ts — 门店上下文
```ts
// lib/store.ts
export type StoreCtx = { key: string; company_id: number; pricelist_id: number; warehouse_id: number }

let STORE_MAP: Record<string, StoreCtx> = {}
try {
  const raw = process.env.STORE_MAP
  if (raw) {
    const o = JSON.parse(raw)
    STORE_MAP = Object.fromEntries(
      Object.entries(o).map(([k, v]: any) => [k, { key: k, company_id: Number(v.company_id), pricelist_id: Number(v.pricelist_id), warehouse_id: Number(v.warehouse_id) }])
    )
  }
} catch (e) {
  // eslint-disable-next-line no-console
  console.warn('Invalid STORE_MAP json:', e)
}

export function getStoreCtx(store_key?: string): StoreCtx {
  const k = store_key && STORE_MAP[store_key] ? store_key : Object.keys(STORE_MAP)[0] || 'default'
  const ctx = STORE_MAP[k]
  if (!ctx) throw new Error('STORE_MAP not configured')
  return ctx
}
```

### lib/odoo-ex.ts — Odoo 调用（含上下文）
```ts
// lib/odoo-ex.ts
import { authenticate } from '@/lib/odoo'

type Ctx = { allowed_company_ids?: number[]; force_company?: number; pricelist?: number; warehouse_id?: number; lang?: string }

async function postJson(path: string, payload: any, cookie?: string) {
  const res = await fetch(new URL(path, process.env.ODOO_BASE_URL!).toString(), {
    method: 'POST', headers: { 'Content-Type': 'application/json', ...(cookie ? { Cookie: cookie } : {}) }, body: JSON.stringify(payload)
  })
  const data = await res.json().catch(() => ({}))
  if (!res.ok || data.error) throw new Error(`Odoo RPC error: HTTP ${res.status} ${(data && JSON.stringify(data.error)) || ''}`)
  return data
}

export async function callKwCtx<T = unknown>(model: string, method: string, args: any[] = [], kwargs: Record<string, any> = {}, ctx: Ctx = {}): Promise<T> {
  const s = await authenticate()
  const payload = {
    jsonrpc: '2.0', method: 'call',
    params: { model, method, args, kwargs: { context: { ...(kwargs?.context || {}), ...ctx } } }
  }
  const data = await postJson('/web/dataset/call_kw', payload, s.cookies)
  return data.result as T
}

export async function execModelMethod<T = unknown>(model: string, method: string, args: any[] = [], ctx: Ctx = {}) {
  return callKwCtx<T>(model, method, args, {}, ctx)
}
```

### lib/pricing.ts — 价表计算（门店+客户）
```ts
// lib/pricing.ts
import { callKwCtx } from '@/lib/odoo-ex'
import { getStoreCtx } from '@/lib/store'

export type PriceInput = { skus: string[]; qty?: number; partner_id?: number; store_key?: string }

export async function computePrices(input: PriceInput) {
  const { skus, qty = 1, partner_id, store_key } = input
  if (!skus?.length) return []
  const store = getStoreCtx(store_key)

  // 1) 拿到产品 ID 映射
  const prods = await callKwCtx<any[]>(
    'product.product', 'search_read',
    [[['default_code', 'in', skus]], ['id', 'default_code']],
    {}, { force_company: store.company_id, allowed_company_ids: [store.company_id], pricelist: store.pricelist_id }
  )
  const idBySku = new Map<string, number>()
  prods.forEach((p: any) => idBySku.set(p.default_code, p.id))

  // 2) 逐个计算（不同 Odoo 版本定价 API 存在差异，做多策略回退）
  const out: Array<{ sku: string; price: number }> = []
  for (const sku of skus) {
    const pid = idBySku.get(sku)
    if (!pid) { out.push({ sku, price: 0 }); continue }
    let price = 0
    // 优先：product.pricelist 的 get_product_price(product_id, qty, partner_id?)
    try {
      price = await callKwCtx<number>('product.pricelist', 'get_product_price', [[store.pricelist_id], pid, qty, partner_id || false], {}, { force_company: store.company_id, pricelist: store.pricelist_id })
    } catch {}
    // 回退：product.pricelist 的 price_get（旧版本）
    if (!price) {
      try {
        const rs = await callKwCtx<Record<string, number>>('product.pricelist', 'price_get', [[store.pricelist_id], [pid], qty, partner_id || false], {}, { force_company: store.company_id, pricelist: store.pricelist_id })
        const k = String(store.pricelist_id)
        price = rs?.[k] || 0
      } catch {}
    }
    // 再回退：拿 list_price
    if (!price) {
      try {
        const r = await callKwCtx<any[]>('product.product', 'read', [[pid], ['list_price']], {}, { force_company: store.company_id })
        price = Number(r?.[0]?.list_price || 0)
      } catch {}
    }
    out.push({ sku, price: Number(price || 0) })
  }
  return out
}
```

### lib/stock.ts — 指定仓库可售量（stock.quant 聚合）
```ts
// lib/stock.ts
import { callKwCtx } from '@/lib/odoo-ex'
import { getStoreCtx } from '@/lib/store'

export async function getAvailableQtyBySkus(skus: string[], store_key?: string) {
  const store = getStoreCtx(store_key)
  // 1) 取产品 id
  const products = await callKwCtx<any[]>('product.product', 'search_read', [[['default_code', 'in', skus]], ['id', 'default_code']], {}, { force_company: store.company_id })
  const pidBySku = new Map<string, number>()
  products.forEach((p) => pidBySku.set(p.default_code, p.id))

  if (!products.length) return {}

  // 2) 找仓库的主库位（lot_stock_id）
  const wh = await callKwCtx<any[]>('stock.warehouse', 'read', [[store.warehouse_id], ['lot_stock_id']], {}, { force_company: store.company_id })
  const lot = wh?.[0]?.lot_stock_id?.[0]
  if (!lot) return {}

  // 3) 查 quant：location child_of 仓库主库位
  const domain = [['product_id', 'in', products.map(p => p.id)], ['location_id', 'child_of', lot]]
  const quants = await callKwCtx<any[]>('stock.quant', 'search_read', [domain, ['product_id', 'quantity', 'reserved_quantity']], { limit: 5000 }, { force_company: store.company_id })
  const map: Record<string, number> = {}
  for (const q of quants) {
    const pid = Array.isArray(q.product_id) ? q.product_id[0] : q.product_id
    const sku = [...pidBySku.entries()].find(([, id]) => id === pid)?.[0]
    if (!sku) continue
    const free = Number(q.quantity || 0) - Number(q.reserved_quantity || 0)
    map[sku] = (map[sku] || 0) + free
  }
  return map
}
```

### lib/lock.ts — 库存锁定（Redis）
```ts
// lib/lock.ts
import { cacheGet, cacheSet } from '@/lib/cache'

export type LockItem = { sku: string; qty: number }
export type LockInfo = { token: string; items: LockItem[]; store_key?: string }

const TTL = 60 * 15 // 15 分钟

export async function createLock(token: string, info: LockInfo) {
  await cacheSet(`lock:${token}`, info, TTL)
}

export async function getLock(token: string): Promise<LockInfo | null> {
  return cacheGet<LockInfo>(`lock:${token}`)
}
```

---

## 3) API 路由

### /api/pricing/compute（升级：支持 store_key/partner_id）
```ts
// app/api/pricing/compute/route.ts
import { NextResponse } from 'next/server'
import { computePrices } from '@/lib/pricing'

export const runtime = 'nodejs'

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(() => ({}))
    const skus: string[] = Array.isArray(body?.skus) ? body.skus.slice(0, 200) : []
    const qty = Number(body?.qty || 1)
    const partner_id = body?.partner_id ? Number(body.partner_id) : undefined
    const store_key = body?.store_key as string | undefined
    if (!skus.length) return NextResponse.json({ ok: false, error: 'skus required' }, { status: 400 })

    const prices = await computePrices({ skus, qty, partner_id, store_key })
    return NextResponse.json({ ok: true, prices })
  } catch (e: any) {
    return NextResponse.json({ ok: false, error: String(e?.message || e) }, { status: 500 })
  }
}
```

### /api/cart/lock（校验仓库可售量 + 生成锁定 token）
```ts
// app/api/cart/lock/route.ts
import { NextResponse } from 'next/server'
import { randomUUID } from 'crypto'
import { getAvailableQtyBySkus } from '@/lib/stock'
import { createLock } from '@/lib/lock'

export const runtime = 'nodejs'

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(() => ({}))
    const items: Array<{ sku: string; qty: number }> = Array.isArray(body?.items) ? body.items : []
    const store_key: string | undefined = body?.store_key
    if (!items.length) return NextResponse.json({ ok: false, error: 'items required' }, { status: 400 })

    const skus = items.map(i => i.sku)
    const avail = await getAvailableQtyBySkus(skus, store_key)

    const insufficient = items.filter(i => (avail[i.sku] || 0) < i.qty)
    if (insufficient.length) {
      return NextResponse.json({ ok: false, error: 'insufficient_stock', details: insufficient })
    }

    const token = randomUUID()
    await createLock(token, { token, items, store_key })
    return NextResponse.json({ ok: true, token })
  } catch (e: any) {
    return NextResponse.json({ ok: false, error: String(e?.message || e) }, { status: 500 })
  }
}
```

### /api/orders/create（根据购物车 + 锁定 token 创建草稿订单）
```ts
// app/api/orders/create/route.ts
import { NextResponse } from 'next/server'
import { getLock } from '@/lib/lock'
import { callKwCtx } from '@/lib/odoo-ex'
import { getStoreCtx } from '@/lib/store'

export const runtime = 'nodejs'

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(() => ({}))
    const token = String(body?.lock_token || '')
    const partner_id = Number(body?.partner_id || 0)
    const store_key = String(body?.store_key || 'default')
    if (!token || !partner_id) return NextResponse.json({ ok: false, error: 'lock_token and partner_id required' }, { status: 400 })

    const lock = await getLock(token)
    if (!lock) return NextResponse.json({ ok: false, error: 'lock_expired' }, { status: 400 })
    const store = getStoreCtx(store_key)

    // 1) 找到产品 id
    const prods = await callKwCtx<any[]>('product.product', 'search_read', [[['default_code', 'in', lock.items.map(i => i.sku)]], ['id', 'default_code']], {}, { force_company: store.company_id })
    const idBySku = new Map<string, number>()
    prods.forEach((p) => idBySku.set(p.default_code, p.id))

    // 2) 构造 order_line（(0,0,{vals}) 列表）
    const lines = lock.items.map(i => {
      const pid = idBySku.get(i.sku)
      if (!pid) throw new Error(`product not found: ${i.sku}`)
      return [0, 0, { product_id: pid, product_uom_qty: i.qty }]
    })

    // 3) 创建 sale.order（草稿）
    const order_vals = {
      partner_id,
      company_id: store.company_id,
      pricelist_id: store.pricelist_id,
      order_line: lines,
      warehouse_id: store.warehouse_id,
    }

    const order_id = await callKwCtx<number>('sale.order', 'create', [[order_vals]], {}, { force_company: store.company_id, pricelist: store.pricelist_id })

    // 4) 读取金额回显
    const order = await callKwCtx<any[]>('sale.order', 'read', [[order_id], ['name', 'amount_total', 'state']], {}, { force_company: store.company_id })

    return NextResponse.json({ ok: true, order_id, order: order?.[0] })
  } catch (e: any) {
    return NextResponse.json({ ok: false, error: String(e?.message || e) }, { status: 500 })
  }
}
```

### /api/payments/session（支付会话占位：返回跳转 URL）
```ts
// app/api/payments/session/route.ts
import { NextResponse } from 'next/server'

export const runtime = 'nodejs'

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(() => ({}))
    const order_id = Number(body?.order_id || 0)
    const amount = Number(body?.amount || 0)
    const method = String(body?.method || 'windcave')

    if (!order_id || !amount) return NextResponse.json({ ok: false, error: 'order_id and amount required' }, { status: 400 })

    if (method !== 'windcave') return NextResponse.json({ ok: false, error: 'unsupported_method' }, { status: 400 })

    // —— 占位：这里应调用 Windcave HPP/3DS2 接口创建支付会话，返回 redirect_url ——
    // 现在返回一个占位 URL，前端可跳转；接入真实网关后替换为返回的 hosted url。
    const redirect_url = `${process.env.WINDCAVE_RETURN_URL}?order=${order_id}&amount=${amount.toFixed(2)}&status=PENDING`

    return NextResponse.json({ ok: true, provider: 'windcave', redirect_url, order_id })
  } catch (e: any) {
    return NextResponse.json({ ok: false, error: String(e?.message || e) }, { status: 500 })
  }
}
```

### /api/payments/callback（回调占位：确认/失败）
```ts
// app/api/payments/callback/route.ts
import { NextResponse } from 'next/server'
import { callKwCtx } from '@/lib/odoo-ex'

export const runtime = 'nodejs'

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(async () => Object.fromEntries((await req.formData()).entries()))
    const status = String(body?.status || '') // e.g., SUCCESS / FAILED / CANCELLED
    const order_id = Number(body?.order_id || body?.order || 0)

    if (!order_id) return NextResponse.json({ ok: false, error: 'order_id required' }, { status: 400 })

    if (status.toUpperCase() === 'SUCCESS') {
      // 简化：直接确认订单；生产可引入 account.payment 注册收款
      try {
        await callKwCtx('sale.order', 'action_confirm', [[order_id]])
      } catch {}
      return NextResponse.json({ ok: true, order_id, state: 'confirmed' })
    }

    return NextResponse.json({ ok: true, order_id, state: 'pending', status })
  } catch (e: any) {
    return NextResponse.json({ ok: false, error: String(e?.message || e) }, { status: 500 })
  }
}
```

---

## 4) 最小验证流程
1. **配置门店映射**：设置 `.env.local` 的 `STORE_MAP`，确保 company/pricelist/warehouse id 正确；
2. **价表测试**：
   ```bash
   curl -X POST http://localhost:3000/api/pricing/compute \
     -H 'Content-Type: application/json' \
     -d '{"skus":["A2898","SM-A146P"],"qty":1,"partner_id":7,"store_key":"albany"}'
   ```
3. **库存锁定**：
   ```bash
   curl -X POST http://localhost:3000/api/cart/lock \
     -H 'Content-Type: application/json' \
     -d '{"items":[{"sku":"A2898","qty":1}],"store_key":"albany"}'
   # => 返回 { token }
   ```
4. **创建草稿订单**：
   ```bash
   curl -X POST http://localhost:3000/api/orders/create \
     -H 'Content-Type: application/json' \
     -d '{"lock_token":"<上一步的token>","partner_id":7,"store_key":"albany"}'
   ```
5. **创建支付会话（占位）**：
   ```bash
   curl -X POST http://localhost:3000/api/payments/session \
     -H 'Content-Type: application/json' \
     -d '{"order_id":123,"amount":199.00,"method":"windcave"}'
   # redirect_url 用于前端跳转（占位）
   ```
6. **回调模拟**：
   ```bash
   curl -X POST http://localhost:3000/api/payments/callback \
     -H 'Content-Type: application/json' \
     -d '{"order_id":123,"status":"SUCCESS"}'
   ```

---

## 5) 注意事项与后续
- **价表 API 差异**：不同 Odoo 版本可能没有 `get_product_price/price_get` 之一，已做多策略回退；若仍异常，可在 Odoo 侧提供一个轻量 Controller 封装官方定价逻辑（推荐）。
- **库存校验**：当前按 `stock.quant` 聚合 `quantity - reserved_quantity`；如有多地点策略，请扩展 domain（或后移到 Odoo Controller 统一计算）。
- **锁定策略**：仅逻辑锁（Redis TTL 15m），实际保留库存应结合拣货/预留（stock.move/stock.reservation），二期接入。
- **支付网关**：本步为占位；接入 Windcave HPP/3DS2 时：
  - 创建支付会话并保存 `txn_id` 与签名；
  - 回调校验签名（HMAC/RSA）与金额/币种/订单号；
  - 失败/取消要释放锁与撤销草稿单（或标记状态）。
- **合规**：生产环境务必走 **Hosted** 页或 Tokenize（SAQ-A/A-EP），不要让卡号触达你的服务器。
已推进到 **Step 4**，我把完整代码与说明放到右侧文档里了，主要包括：

- 价表/客户等级：按门店（company/pricelist/warehouse）与 `partner_id` 计算价格；
    
- 库存校验与短期锁定（Redis/TTL 15min）；
    
- 创建 `sale.order` 草稿（门店上下文 + 订单行）；
    
- 支付会话骨架（Windcave 3DS2/HPP 的占位接口 + 回调入口）。
    

你现在可以按 README 的“最小验证流程”跑一遍（价表 → 锁定 → 下单 → 支付会话 → 回调模拟）。

接下来我建议的 **Step 5**：

1. 接入 **Windcave 真正的 HPP/3DS2**（沙箱）：生成会话、跳转、签名校验、状态回写 Odoo（含 `account.payment`）。
    
2. **订单确认链路**：支付成功后自动 `action_confirm` → 生成拣货/发货任务；失败释放锁。
    
3. **错误与审计**：Sentry、结构化日志、对账脚本与幂等重放工具。




