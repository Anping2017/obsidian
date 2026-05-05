# PostCSS

## PostCSS概述

PostCSS是CSS后处理器，通过插件系统扩展CSS功能，是现代CSS工程化的核心工具。

## PostCSS基础

### 1. 安装和配置
```bash
# 安装PostCSS
npm install postcss postcss-cli --save-dev

# 安装常用插件
npm install autoprefixer postcss-import postcss-nested --save-dev
```

### 2. 基本配置
```javascript
// postcss.config.js
module.exports = {
    plugins: [
        require('postcss-import'),
        require('postcss-nested'),
        require('autoprefixer')
    ]
};
```

### 3. 使用方式
```bash
# 命令行使用
postcss input.css -o output.css

# 监听文件变化
postcss input.css -o output.css --watch

# 使用配置文件
postcss input.css -o output.css --config postcss.config.js
```

## 常用插件

### 1. Autoprefixer
```css
/* 输入 */
.example {
    display: flex;
    transform: translateX(10px);
    user-select: none;
}

/* 输出 */
.example {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-transform: translateX(10px);
    -ms-transform: translateX(10px);
    transform: translateX(10px);
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}
```

### 2. postcss-import
```css
/* main.css */
@import 'variables.css';
@import 'mixins.css';
@import 'components/button.css';
@import 'components/card.css';
```

### 3. postcss-nested
```css
/* 输入 */
.button {
    padding: 0.75rem 1.5rem;
    
    &:hover {
        opacity: 0.9;
    }
    
    &--primary {
        background-color: #007bff;
        
        &:hover {
            background-color: #0056b3;
        }
    }
}

/* 输出 */
.button {
    padding: 0.75rem 1.5rem;
}

.button:hover {
    opacity: 0.9;
}

.button--primary {
    background-color: #007bff;
}

.button--primary:hover {
    background-color: #0056b3;
}
```

### 4. postcss-custom-properties
```css
/* 输入 */
:root {
    --primary-color: #007bff;
    --spacing: 1rem;
}

.button {
    background-color: var(--primary-color);
    padding: var(--spacing);
}

/* 输出（支持旧浏览器） */
.button {
    background-color: #007bff;
    background-color: var(--primary-color);
    padding: 1rem;
    padding: var(--spacing);
}
```

### 5. postcss-mixins
```css
/* 定义混入 */
@define-mixin button-base {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.25rem;
    cursor: pointer;
}

@define-mixin button-variant $color {
    background-color: $color;
    color: white;
    
    &:hover {
        opacity: 0.9;
    }
}

/* 使用混入 */
.button {
    @mixin button-base;
}

.button--primary {
    @mixin button-variant #007bff;
}

.button--secondary {
    @mixin button-variant #6c757d;
}
```

## 高级插件

### 1. postcss-preset-env
```css
/* 输入 */
.example {
    color: color-mod(blue alpha(50%));
    background: linear-gradient(45deg, red, blue);
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}

/* 输出 */
.example {
    color: rgba(0, 0, 255, 0.5);
    background: linear-gradient(45deg, red, blue);
    display: -ms-grid;
    display: grid;
    -ms-grid-columns: (minmax(200px, 1fr))[auto-fit];
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}
```

### 2. postcss-calc
```css
/* 输入 */
.example {
    width: calc(100% - 2rem);
    height: calc(100vh - 60px);
    margin: calc(1rem + 2px);
}

/* 输出 */
.example {
    width: calc(100% - 2rem);
    height: calc(100vh - 60px);
    margin: 18px;
}
```

### 3. postcss-pxtorem
```css
/* 输入 */
.example {
    font-size: 16px;
    margin: 20px;
    padding: 10px 15px;
}

/* 输出（假设根字体大小为16px） */
.example {
    font-size: 1rem;
    margin: 1.25rem;
    padding: 0.625rem 0.9375rem;
}
```

### 4. postcss-sorting
```css
/* 输入 */
.example {
    color: red;
    background: blue;
    margin: 10px;
    padding: 5px;
    border: 1px solid black;
}

/* 输出（按属性排序） */
.example {
    margin: 10px;
    padding: 5px;
    border: 1px solid black;
    background: blue;
    color: red;
}
```

## 构建工具集成

### 1. Webpack集成
```javascript
// webpack.config.js
module.exports = {
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    'style-loader',
                    'css-loader',
                    {
                        loader: 'postcss-loader',
                        options: {
                            postcssOptions: {
                                plugins: [
                                    require('autoprefixer'),
                                    require('postcss-nested')
                                ]
                            }
                        }
                    }
                ]
            }
        ]
    }
};
```

### 2. Vite集成
```javascript
// vite.config.js
import { defineConfig } from 'vite';

export default defineConfig({
    css: {
        postcss: {
            plugins: [
                require('autoprefixer'),
                require('postcss-nested')
            ]
        }
    }
});
```

### 3. Gulp集成
```javascript
// gulpfile.js
const gulp = require('gulp');
const postcss = require('gulp-postcss');
const autoprefixer = require('autoprefixer');
const nested = require('postcss-nested');

gulp.task('css', () => {
    return gulp.src('src/css/*.css')
        .pipe(postcss([
            nested(),
            autoprefixer()
        ]))
        .pipe(gulp.dest('dist/css'));
});
```

## 自定义插件

### 1. 简单插件
```javascript
// plugins/postcss-color-shorthand.js
module.exports = (opts = {}) => {
    return {
        postcssPlugin: 'postcss-color-shorthand',
        Rule(rule) {
            rule.walkDecls(decl => {
                if (decl.prop === 'color' && decl.value === 'red') {
                    decl.value = '#ff0000';
                }
            });
        }
    };
};

module.exports.postcss = true;
```

### 2. 复杂插件
```javascript
// plugins/postcss-theme-variables.js
module.exports = (opts = {}) => {
    const theme = opts.theme || {};
    
    return {
        postcssPlugin: 'postcss-theme-variables',
        Once(root) {
            root.walkRules(rule => {
                rule.walkDecls(decl => {
                    if (decl.value.includes('theme(')) {
                        const match = decl.value.match(/theme\(([^)]+)\)/);
                        if (match) {
                            const key = match[1].trim();
                            const value = theme[key];
                            if (value) {
                                decl.value = decl.value.replace(match[0], value);
                            }
                        }
                    }
                });
            });
        }
    };
};

module.exports.postcss = true;
```

### 3. 插件使用
```javascript
// postcss.config.js
const colorShorthand = require('./plugins/postcss-color-shorthand');
const themeVariables = require('./plugins/postcss-theme-variables');

module.exports = {
    plugins: [
        colorShorthand(),
        themeVariables({
            theme: {
                primary: '#007bff',
                secondary: '#6c757d'
            }
        })
    ]
};
```

## 性能优化

### 1. 插件优化
```javascript
// 只处理需要的文件
module.exports = {
    plugins: [
        process.env.NODE_ENV === 'production' && require('cssnano'),
        require('autoprefixer')
    ].filter(Boolean)
};
```

### 2. 缓存优化
```javascript
// 使用缓存
const postcss = require('postcss');
const fs = require('fs');
const path = require('path');

const cache = new Map();

function processCSS(input, plugins) {
    const key = input + JSON.stringify(plugins);
    
    if (cache.has(key)) {
        return cache.get(key);
    }
    
    const result = postcss(plugins).process(input);
    cache.set(key, result);
    
    return result;
}
```

### 3. 并行处理
```javascript
// 并行处理多个文件
const { Worker } = require('worker_threads');

function processFilesInParallel(files, plugins) {
    return Promise.all(
        files.map(file => 
            new Promise((resolve, reject) => {
                const worker = new Worker('./postcss-worker.js', {
                    workerData: { file, plugins }
                });
                
                worker.on('message', resolve);
                worker.on('error', reject);
            })
        )
    );
}
```

## 最佳实践

### 1. 插件选择
```javascript
// 生产环境配置
const productionPlugins = [
    require('autoprefixer'),
    require('postcss-preset-env'),
    require('cssnano')
];

// 开发环境配置
const developmentPlugins = [
    require('autoprefixer'),
    require('postcss-preset-env')
];
```

### 2. 配置管理
```javascript
// 环境特定配置
const config = {
    plugins: [
        require('postcss-import'),
        require('postcss-nested'),
        require('autoprefixer')
    ]
};

if (process.env.NODE_ENV === 'production') {
    config.plugins.push(require('cssnano'));
}

module.exports = config;
```

### 3. 错误处理
```javascript
// 错误处理
const postcss = require('postcss');

postcss(plugins)
    .process(css, { from: 'input.css', to: 'output.css' })
    .then(result => {
        console.log('CSS processed successfully');
    })
    .catch(error => {
        console.error('PostCSS error:', error);
    });
```

## 相关链接

- [[CSS模块化]] - 了解CSS模块化
- [[CSS-in-JS]] - 学习CSS-in-JS
- [[最佳实践/代码规范]] - 查看编码规范
- [[性能优化/渲染优化]] - 优化CSS性能

## 实践练习

### 基础练习
1. 配置PostCSS
2. 使用常用插件
3. 集成构建工具

### 进阶练习
1. 开发自定义插件
2. 优化构建性能
3. 实现复杂CSS处理

---

*下一步：学习 [[CSS-in-JS]] 了解现代CSS方案*
