# CSS-in-JS

## CSS-in-JS概述

CSS-in-JS是将CSS样式直接写在JavaScript中的技术方案，提供了组件级别的样式封装。

## 主要库对比

### 1. Styled Components
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

### 2. Emotion
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

const Button = styled.button`
    ${buttonStyles}
    
    ${props => props.variant === 'primary' && css`
        background-color: #007bff;
        color: white;
    `}
    
    ${props => props.variant === 'secondary' && css`
        background-color: #6c757d;
        color: white;
    `}
    
    &:hover {
        opacity: 0.9;
    }
`;

export default Button;
```

### 3. Stitches
```javascript
// Button.stitches.js
import { styled } from '@stitches/react';

const Button = styled('button', {
    display: 'inline-block',
    padding: '0.75rem 1.5rem',
    border: 'none',
    borderRadius: '0.25rem',
    cursor: 'pointer',
    fontSize: '1rem',
    transition: 'all 0.3s ease',
    
    variants: {
        variant: {
            primary: {
                backgroundColor: '#007bff',
                color: 'white',
            },
            secondary: {
                backgroundColor: '#6c757d',
                color: 'white',
            }
        },
        size: {
            small: {
                padding: '0.5rem 1rem',
                fontSize: '0.875rem',
            },
            large: {
                padding: '1rem 2rem',
                fontSize: '1.125rem',
            }
        }
    },
    
    compoundVariants: [
        {
            variant: 'primary',
            size: 'large',
            css: {
                fontWeight: 'bold',
            }
        }
    ],
    
    defaultVariants: {
        variant: 'primary',
        size: 'medium',
    }
});

export default Button;
```

## 主题系统

### 1. Styled Components主题
```javascript
// theme.js
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

// App.jsx
import { ThemeProvider } from 'styled-components';
import { theme } from './theme';

function App() {
    return (
        <ThemeProvider theme={theme}>
            <Button variant="primary">按钮</Button>
        </ThemeProvider>
    );
}
```

### 2. Emotion主题
```javascript
// theme.js
export const theme = {
    colors: {
        primary: '#007bff',
        secondary: '#6c757d'
    },
    spacing: {
        md: '1rem',
        lg: '1.5rem'
    }
};

// App.jsx
import { ThemeProvider } from '@emotion/react';
import { theme } from './theme';

function App() {
    return (
        <ThemeProvider theme={theme}>
            <Button variant="primary">按钮</Button>
        </ThemeProvider>
    );
}
```

## 动态样式

### 1. 条件样式
```javascript
// 基于props的条件样式
const Button = styled.button`
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.25rem;
    cursor: pointer;
    
    ${props => props.variant === 'primary' && `
        background-color: #007bff;
        color: white;
    `}
    
    ${props => props.variant === 'secondary' && `
        background-color: #6c757d;
        color: white;
    `}
    
    ${props => props.disabled && `
        opacity: 0.6;
        cursor: not-allowed;
    `}
`;
```

### 2. 响应式样式
```javascript
// 响应式样式
const Container = styled.div`
    padding: 1rem;
    
    @media (min-width: 768px) {
        padding: 2rem;
    }
    
    @media (min-width: 1024px) {
        padding: 3rem;
    }
`;

// 使用主题断点
const ResponsiveContainer = styled.div`
    padding: ${props => props.theme.spacing.md};
    
    ${props => props.theme.breakpoints.tablet} {
        padding: ${props => props.theme.spacing.lg};
    }
    
    ${props => props.theme.breakpoints.desktop} {
        padding: ${props => props.theme.spacing.xl};
    }
`;
```

### 3. 动画样式
```javascript
// 动画样式
const AnimatedButton = styled.button`
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.25rem;
    cursor: pointer;
    transition: all 0.3s ease;
    
    &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    &:active {
        transform: translateY(0);
    }
`;

// 关键帧动画
const SpinningIcon = styled.div`
    animation: spin 1s linear infinite;
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
`;
```

## 性能优化

### 1. 样式缓存
```javascript
// 样式缓存
const Button = styled.button`
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.25rem;
    cursor: pointer;
`;

// 使用React.memo优化
const MemoizedButton = React.memo(Button);
```

### 2. 样式提取
```javascript
// 样式提取
import { extractCritical } from '@emotion/server';

const { html, css } = extractCritical(htmlString);
```

### 3. 懒加载样式
```javascript
// 懒加载样式
const LazyStyledComponent = lazy(() => 
    import('./StyledComponent').then(module => ({
        default: module.StyledComponent
    }))
);
```

## 服务端渲染

### 1. Styled Components SSR
```javascript
// server.js
import { ServerStyleSheet } from 'styled-components';
import { renderToString } from 'react-dom/server';

const sheet = new ServerStyleSheet();

try {
    const html = renderToString(sheet.collectStyles(<App />));
    const styleTags = sheet.getStyleTags();
    
    res.send(`
        <html>
            <head>${styleTags}</head>
            <body>
                <div id="root">${html}</div>
            </body>
        </html>
    `);
} finally {
    sheet.seal();
}
```

### 2. Emotion SSR
```javascript
// server.js
import { renderToString } from 'react-dom/server';
import { extractCritical } from '@emotion/server';

const html = renderToString(<App />);
const { html: criticalHtml, css } = extractCritical(html);

res.send(`
    <html>
        <head>
            <style>${css}</style>
        </head>
        <body>
            <div id="root">${criticalHtml}</div>
        </body>
    </html>
`);
```

## 测试策略

### 1. 组件测试
```javascript
// Button.test.js
import React from 'react';
import { render } from '@testing-library/react';
import { ThemeProvider } from 'styled-components';
import Button from './Button';
import { theme } from './theme';

describe('Button', () => {
    it('renders with primary variant', () => {
        const { container } = render(
            <ThemeProvider theme={theme}>
                <Button variant="primary">Click me</Button>
            </ThemeProvider>
        );
        
        const button = container.firstChild;
        expect(button).toHaveStyle('background-color: #007bff');
    });
    
    it('applies custom styles', () => {
        const { container } = render(
            <ThemeProvider theme={theme}>
                <Button $customColor="#ff0000">Click me</Button>
            </ThemeProvider>
        );
        
        const button = container.firstChild;
        expect(button).toHaveStyle('color: #ff0000');
    });
});
```

### 2. 快照测试
```javascript
// Button.test.js
import React from 'react';
import { render } from '@testing-library/react';
import Button from './Button';

describe('Button', () => {
    it('matches snapshot', () => {
        const { container } = render(<Button>Click me</Button>);
        expect(container.firstChild).toMatchSnapshot();
    });
});
```

## 最佳实践

### 1. 样式组织
```javascript
// 样式常量
const BUTTON_SIZES = {
    small: '0.5rem 1rem',
    medium: '0.75rem 1.5rem',
    large: '1rem 2rem'
};

const Button = styled.button`
    padding: ${props => BUTTON_SIZES[props.size] || BUTTON_SIZES.medium};
    border: none;
    border-radius: 0.25rem;
    cursor: pointer;
`;
```

### 2. 类型安全
```typescript
// Button.types.ts
interface ButtonProps {
    variant?: 'primary' | 'secondary' | 'danger';
    size?: 'small' | 'medium' | 'large';
    disabled?: boolean;
}

// Button.styled.ts
const Button = styled.button<ButtonProps>`
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.25rem;
    cursor: pointer;
    
    ${props => props.variant === 'primary' && `
        background-color: #007bff;
        color: white;
    `}
`;
```

### 3. 性能监控
```javascript
// 性能监控
import { performance } from 'perf_hooks';

const start = performance.now();
// 渲染组件
const end = performance.now();
console.log(`渲染时间: ${end - start}ms`);
```

## 相关链接

- [[CSS模块化]] - 了解CSS模块化
- [[PostCSS]] - 学习CSS后处理器
- [[最佳实践/代码规范]] - 查看编码规范
- [[性能优化/渲染优化]] - 优化CSS性能

## 实践练习

### 基础练习
1. 使用Styled Components
2. 实现主题系统
3. 创建动态样式

### 进阶练习
1. 优化CSS-in-JS性能
2. 实现服务端渲染
3. 构建组件库

---

*下一步：学习 [[浏览器兼容性/兼容性策略]] 了解浏览器兼容性*
