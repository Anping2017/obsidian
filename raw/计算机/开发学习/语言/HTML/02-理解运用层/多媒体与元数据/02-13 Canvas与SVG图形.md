# Canvas与SVG图形

## 🎨 SVG矢量图形

### 📋 SVG基础语法

```html
<svg width="200" height="200" viewBox="0 0 200 200">
    <circle cx="100" cy="100" r="50" fill="blue" />
    <rect x="50" y="150" width="100" height="30" fill="red" />
</svg>
```

## 🖼️ Canvas画布

### 📋 Canvas基础使用

```html
<canvas id="myCanvas" width="300" height="200"></canvas>

<script>
const canvas = document.getElementById('myCanvas');
const ctx = canvas.getContext('2d');
ctx.fillStyle = 'blue';
ctx.fillRect(50, 50, 100, 100);
</script>
```

## 🎯 图形处理对比

| 特性 | SVG | Canvas |
|------|-----|--------|
| **图形类型** | 矢量图形 | 位图图形 |
| **可伸缩性** | ✅ 完美缩放 | ❌ 像素化 |
| **文件大小** | 🔴 大文件 | ✅ 小文件 |
| **交互性** | ✅ 事件支持 | ⚠️ 需手动处理 |
| **SEO友好** | ✅ 搜索可索引 | ❌ 不可索引 |

---
