# CSS模块化

## CSS模块化概述

CSS模块化是现代前端工程化的重要组成部分，通过模块化方式组织和管理CSS代码。

## 模块化方案

### 1. CSS Modules
```css
/* Button.module.css */
.button {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.25rem;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.primary {
    background-color: #007bff;
    color: white;
}

.secondary {
    background-color: #6c757d;
    color: white;
}

.large {
    padding: 1rem 2rem;
    font-size: 1.125rem;
}
```

```javascript
// Button.jsx
import React from 'react';
import styles from './Button.module.css';

function Button({ variant = 'primary', size = 'medium', children, ...props }) {
    const className = [
        styles.button,
        styles[variant],
        styles[size]
    ].filter(Boolean).join(' ');
    
    return (
        <button className={className} {...props}>
            {children}
        </button>
    );
}

export default Button;
```

### 2. Styled Components
```javascript
// Button.styled.js
import styled from 'styled-components';

const Button = styled.button`
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.25rem;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s ease;
    
    ${props => props.variant === 'primary' && `
        background-color: #007bff;
        color: white;
    `}
    
    ${props => props.variant === 'secondary' && `
        background-color: #6c757d;
        color: white;
    `}
    
    ${props => props.size === 'large' && `
        padding: 1rem 2rem;
        font-size: 1.125rem;
    `}
    
    &:hover {
        opacity: 0.9;
    }
    
    &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
`;

export default Button;
```

### 3. Emotion
```javascript
// Button.emotion.js
import { css } from '@emotion/react';
import styled from '@emotion/styled';

const buttonStyles = css`
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.25rem;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s ease;
`;

const primaryStyles = css`
    background-color: #007bff;
    color: white;
`;

const secondaryStyles = css`
    background-color: #6c757d;
    color: white;
`;

const largeStyles = css`
    padding: 1rem 2rem;
    font-size: 1.125rem;
`;

const Button = styled.button`
    ${buttonStyles}
    
    ${props => props.variant === 'primary' && primaryStyles}
    ${props => props.variant === 'secondary' && secondaryStyles}
    ${props => props.size === 'large' && largeStyles}
    
    &:hover {
        opacity: 0.9;
    }
    
    &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
`;

export default Button;
```

## 构建工具集成

### 1. Webpack配置
```javascript
// webpack.config.js
module.exports = {
    module: {
        rules: [
            {
                test: /\.module\.css$/,
                use: [
                    'style-loader',
                    {
                        loader: 'css-loader',
                        options: {
                            modules: {
                                localIdentName: '[name]__[local]--[hash:base64:5]'
                            }
                        }
                    }
                ]
            },
            {
                test: /\.css$/,
                exclude: /\.module\.css$/,
                use: ['style-loader', 'css-loader']
            }
        ]
    }
};
```

### 2. Vite配置
```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [react()],
    css: {
        modules: {
            localsConvention: 'camelCase',
            generateScopedName: '[name]__[local]--[hash:base64:5]'
        }
    }
});
```

### 3. PostCSS配置
```javascript
// postcss.config.js
module.exports = {
    plugins: [
        require('postcss-import'),
        require('postcss-nested'),
        require('autoprefixer'),
        require('postcss-modules')({
            generateScopedName: '[name]__[local]--[hash:base64:5]'
        })
    ]
};
```

## 组件库架构

### 1. 组件结构
```
src/
├── components/
│   ├── Button/
│   │   ├── Button.jsx
│   │   ├── Button.module.css
│   │   ├── Button.test.js
│   │   └── index.js
│   ├── Card/
│   │   ├── Card.jsx
│   │   ├── Card.module.css
│   │   ├── Card.test.js
│   │   └── index.js
│   └── index.js
├── styles/
│   ├── variables.css
│   ├── mixins.css
│   └── global.css
└── utils/
    ├── classNames.js
    └── theme.js
```

### 2. 样式变量
```css
/* styles/variables.css */
:root {
    /* 颜色变量 */
    --color-primary: #007bff;
    --color-secondary: #6c757d;
    --color-success: #28a745;
    --color-danger: #dc3545;
    --color-warning: #ffc107;
    --color-info: #17a2b8;
    
    /* 间距变量 */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    
    /* 字体变量 */
    --font-size-sm: 0.875rem;
    --font-size-base: 1rem;
    --font-size-lg: 1.125rem;
    --font-size-xl: 1.25rem;
    
    /* 边框变量 */
    --border-radius-sm: 0.25rem;
    --border-radius-md: 0.5rem;
    --border-radius-lg: 0.75rem;
    
    /* 阴影变量 */
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
    --shadow-md: 0 2px 4px rgba(0,0,0,0.1);
    --shadow-lg: 0 4px 8px rgba(0,0,0,0.15);
}
```

### 3. 样式混入
```css
/* styles/mixins.css */
@mixin button-base {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: var(--border-radius-sm);
    cursor: pointer;
    font-size: var(--font-size-base);
    text-decoration: none;
    text-align: center;
    transition: all 0.3s ease;
}

@mixin button-variant($bg-color, $text-color) {
    background-color: $bg-color;
    color: $text-color;
    
    &:hover {
        opacity: 0.9;
    }
    
    &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
}

@mixin card-base {
    background: white;
    border-radius: var(--border-radius-md);
    box-shadow: var(--shadow-md);
    overflow: hidden;
}
```

## 工具函数

### 1. 类名合并
```javascript
// utils/classNames.js
export function classNames(...classes) {
    return classes.filter(Boolean).join(' ');
}

// 使用示例
const className = classNames(
    'button',
    'button--primary',
    isLarge && 'button--large',
    isDisabled && 'button--disabled'
);
```

### 2. 主题工具
```javascript
// utils/theme.js
export const theme = {
    colors: {
        primary: '#007bff',
        secondary: '#6c757d',
        success: '#28a745',
        danger: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8'
    },
    spacing: {
        xs: '0.25rem',
        sm: '0.5rem',
        md: '1rem',
        lg: '1.5rem',
        xl: '2rem'
    },
    typography: {
        fontSize: {
            sm: '0.875rem',
            base: '1rem',
            lg: '1.125rem',
            xl: '1.25rem'
        }
    }
};

export function getThemeValue(path) {
    return path.split('.').reduce((obj, key) => obj?.[key], theme);
}
```

### 3. 样式生成器
```javascript
// utils/styleGenerator.js
export function generateButtonStyles(variant, size) {
    const baseStyles = {
        display: 'inline-block',
        padding: '0.75rem 1.5rem',
        border: 'none',
        borderRadius: '0.25rem',
        cursor: 'pointer',
        fontSize: '1rem',
        transition: 'all 0.3s ease'
    };
    
    const variantStyles = {
        primary: {
            backgroundColor: '#007bff',
            color: 'white'
        },
        secondary: {
            backgroundColor: '#6c757d',
            color: 'white'
        }
    };
    
    const sizeStyles = {
        small: {
            padding: '0.5rem 1rem',
            fontSize: '0.875rem'
        },
        large: {
            padding: '1rem 2rem',
            fontSize: '1.125rem'
        }
    };
    
    return {
        ...baseStyles,
        ...variantStyles[variant],
        ...sizeStyles[size]
    };
}
```

## 测试策略

### 1. 样式测试
```javascript
// Button.test.js
import React from 'react';
import { render } from '@testing-library/react';
import Button from './Button';
import styles from './Button.module.css';

describe('Button', () => {
    it('renders with default styles', () => {
        const { container } = render(<Button>Click me</Button>);
        const button = container.firstChild;
        
        expect(button).toHaveClass(styles.button);
    });
    
    it('applies variant styles', () => {
        const { container } = render(<Button variant="primary">Click me</Button>);
        const button = container.firstChild;
        
        expect(button).toHaveClass(styles.primary);
    });
    
    it('applies size styles', () => {
        const { container } = render(<Button size="large">Click me</Button>);
        const button = container.firstChild;
        
        expect(button).toHaveClass(styles.large);
    });
});
```

### 2. 视觉回归测试
```javascript
// visual.test.js
import { test, expect } from '@playwright/test';

test('button visual regression', async ({ page }) => {
    await page.goto('/components/button');
    
    // 测试不同状态的按钮
    await expect(page.locator('.button--primary')).toHaveScreenshot('button-primary.png');
    await expect(page.locator('.button--secondary')).toHaveScreenshot('button-secondary.png');
    await expect(page.locator('.button--large')).toHaveScreenshot('button-large.png');
});
```

## 性能优化

### 1. 代码分割
```javascript
// 动态导入样式
const Button = lazy(() => import('./Button'));

// 按需加载样式
import('./Button.module.css').then(styles => {
    // 使用样式
});
```

### 2. 样式优化
```css
/* 使用CSS变量减少重复 */
.button {
    --button-padding: 0.75rem 1.5rem;
    --button-border-radius: 0.25rem;
    
    padding: var(--button-padding);
    border-radius: var(--button-border-radius);
}

.button--large {
    --button-padding: 1rem 2rem;
}
```

### 3. 构建优化
```javascript
// webpack.config.js
module.exports = {
    optimization: {
        splitChunks: {
            cacheGroups: {
                styles: {
                    name: 'styles',
                    test: /\.css$/,
                    chunks: 'all',
                    enforce: true
                }
            }
        }
    }
};
```

## 相关链接

- [[BEM方法论]] - 了解CSS命名规范
- [[OOCSS]] - 学习面向对象CSS
- [[SMACSS]] - 了解可扩展CSS架构
- [[PostCSS]] - 学习CSS后处理器

## 实践练习

### 基础练习
1. 创建CSS模块
2. 实现组件样式
3. 配置构建工具

### 进阶练习
1. 构建组件库
2. 实现主题系统
3. 优化构建性能

---

*下一步：学习 [[PostCSS]] 了解CSS后处理器*
