# TypeScript 构建工具链完全指南

## 🎯 现代构建工具链概览

### 📊 构建工具生态系统

```mermaid
graph TD
    A[Build Tools] --> B[Bundlers]
    A --> C[Task Runners]
    A --> D[Type Checkers]
    A --> E[Code Generators]
    
    B --> B1[Webpack]
    B --> B2[Vite]
    B --> B3[Rollup]
    B --> B4[esbuild]
    
    C --> C1[npm scripts]
    C --> C2[Gulp.js]
    C --> C3[Just tasks]
    C --> C4[Nx]
    
    D --> D1[tcs]
    D --> D2[Swaage]
    D --> D3[tsc-watch]
    
    E --> E1[ts-node]
    E --> E2[ts-jest]
    E --> E3[@babel/preset-typescript]
```

## 🔧 Webpack + TypeScript 配置

### 💡 现代化 Webpack 配置

```typescript
// webpack.config.ts
import { Configuration } from 'webpack';
import { resolve } from 'path';
import HtmlWebpackPlugin from 'html-webpack-plugin';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import ForkTsCheckerWebpackPlugin from 'fork-ts-checker-webpack-plugin';
import CopyWebpackPlugin from 'copy-webpack-plugin';

interface WebpackConfig extends Configuration {
    resolve?: {
        alias: Record<string, string>;
        extensions: string[];
        fallback?: Record<string, string>;
    };
}

const isProduction = process.env.NODE_ENV === 'production';
const isDevelopment = !isProduction;

const config: WebpackConfig = {
    mode: isProduction ? 'production' : 'development',
    
    // 入口配置
    entry: {
        main: resolve(__dirname, 'src/index.tsx'),
        vendor: ['react', 'react-dom', 'react-router-dom'],
    },
    
    // 输出配置
    output: {
        path: resolve(__dirname, 'dist'),
        filename: isProduction ? '[name].[contenthash:8].js' : '[name].js',
        chunkFilename: isProduction ? '[name].[contenthash:8].chunk.js' : '[name].chunk.js',
        publicPath: '/',
        clean: true,
    },
    
    // 模块解析配置
    resolve: {
        alias: {
            '@': resolve(__dirname, 'src'),
            '@components': resolve(__dirname, 'src/components'),
            '@utils': resolve(__dirname, 'src/utils'),
            '@services': resolve(__dirname, 'src/services'),
            '@hooks': resolve(__dirname, 'src/hooks'),
            '@types': resolve(__dirname, 'src/types'),
            '@assets': resolve(__dirname, 'src/assets'),
        },
        extensions: ['.tsx', '.ts', '.jsx', '.js', '.json'],
        fallback: {
            "path": false,
            "fs": false,
        },
    },
    
    // 模块规则
    module: {
        rules: [
            // TypeScript/JavaScript 规则
            {
                test: /\.(ts|tsx|js|jsx)$/,
                exclude: /node_modules/,
                use: [
                    {
                        loader: 'babel-loader',
                        options: {
                            presets: [
                                '@babel/preset-env',
                                [
                                    '@babel/preset-react',
                                    {
                                        runtime: 'automatic',
                                        development: isDevelopment,
                                    }
                                ],
                                '@babel/preset-typescript',
                            ],
                            plugins: [
                                '@babel/plugin-proposal-class-properties',
                                '@babel/plugin-transform-runtime',
                                ...(isDevelopment ? ['react-refresh/babel'] : []),
                            ],
                            cacheDirectory: true,
                        },
                    },
                ],
            },
            
            // CSS/SCSS 规则
            {
                test: /\.css$/,
                use: [
                    isProduction ? MiniCssExtractPlugin.loader : 'style-loader',
                    'css-loader',
                    {
                        loader: 'postcss-loader',
                        options: {
                            postcssOptions: {
                                plugins: [
                                    'autoprefixer',
                                    ...(isProduction ? ['cssnano'] : []),
                                ],
                            },
                        },
                    },
                ],
            },
            
            {
                test: /\.(scss|sass)$/,
                use: [
                    isProduction ? MiniCssExtractPlugin.loader : 'style-loader',
                    'css-loader',
                    {
                        loader: 'postcss-loader',
                        options: {
                            postcssOptions: {
                                plugins: [
                                    'autoprefixer',
                                    ...(isProduction ? ['cssnano'] : []),
                                ],
                            },
                        },
                    },
                    'sass-loader',
                ],
            },
            
            // 资源文件规则
            {
                test: /\.(png|jpg|jpeg|gif|svg|webp|ico)$/,
                type: 'asset/resource',
                generator: {
                    filename: 'assets/images/[name].[contenthash:8][ext]',
                },
            },
            
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/,
                type: 'asset/resource',
                generator: {
                    filename: 'assets/fonts/[name].[contenthash:8][ext]',
                },
            },
        ],
    },
    
    // 插件配置
    plugins. [
        // HTML 模板插件
        new HtmlWebpackPlugin({
            template: resolve(__dirname, 'public/index.html'),
            filename: 'index.html',
            inject: 'body',
            minify: isProduction ? {
                removeComments: true,
                collapseWhitespace: true,
                removeRedundantAttributes: true,
                useShortDoctype: true,
                removeEmptyAttributes: true,
                removeStyleLinkTypeAttributes: true,
                keepClosingSlash: true,
                minifyJS: true,
                minifyCSS: true,
                minifyURLs: true,
            } : false,
        }),
        
        // CSS 提取插件
        new MiniCssExtractPlugin({
            filename: isProduction ? '[name].[contenthash:8].css' : '[name].css',
            chunkFilename: isProduction ? '[name].[contenthash:8].chunk.css' : '[name].chunk.css',
        }),
        
        // TypeScript 类型检查插件
        new ForkTsCheckerWebpackPlugin({
            typescript: {
                configFile: resolve(__dirname, 'tsconfig.json'),
                diagnosticOptions: {
                    semantic: true,
                    syntactic: true,
                },
                mode: 'write-references',
            },
            async: true,
        }),
        
        // 资源复制插件
        new CopyWebpackPlugin({
            patterns: [
                {
                    from: resolve(__dirname, 'public'),
                    to: resolve(__dirname, 'dist'),
                    globOptions: {
                        ignore: ['**/index.html'],
                    },
                },
            ],
        }),
        
        ...(isDevelopment ? [
            // 开发环境特有插件
            new webpack.HotModuleReplacementPlugin(),
            new webpack.DefinePlugin({
                'process.env.NODE_ENV': JSON.stringify('development'),
            }),
        ] : [
            // 生产环境特有插件
            new webpack.DefinePlugin({
                'process.env.NODE_ENV': JSON.stringify('production'),
            }),
            new webpack.SourceMapDevToolPlugin({
                filename: '[file].map[query]',
                exclude: ['vendor.js'],
            }),
        ]),
    ],
    
    // 优化配置
    optimization: {
        splitChunks: {
            chunks: 'all',
            cacheGroups: {
                vendor: {
                    test: /[\\/]node_modules[\\/]/,
                    name: 'vendors',
                    priority: 10,
                    reuseExistingChunk: true,
                },
                common: {
                    name: 'common',
                    minChunks: 2,
                    priority: 5,
                    reuseExistingChunk: true,
                },
            },
        },
        runtimeChunk: {
            name: 'runtime',
        },
        usedExports: true,
        sideEffects: false,
    },
    
    // 开发服务器配置
    devServer: {
        contentBase: resolve(__dirname, 'public'),
        hot: true,
        compress: true,
        port: 3000,
        open: true,
        historyApiFallback: true,
        overlay: {
            warnings: true,
            errors: true,
        },
        stats: {
            colors: true,
            chunks: false,
            modules: false,
            children: false,
        },
    },
    
    // 性能提示
    performance: {
        hints: isProduction ? 'warning' : false,
        maxEntrypointSize: 512000,
        maxAssetSize: 512000,
    },
    
    // Source maps
    devtool: isProduction ? 'source-map' : 'eval-cheap-module-source-map',
};

export default config;
```

### 🎪 高级 Webpack 功能

```typescript
// webpack.config.advanced.ts
import { Configuration } from 'webpack';
import { BundleAnalyzerPlugin } from 'webpack-bundle-analyzer';
import CompressionPlugin from 'compression-webpack-plugin';
import path from 'path';
import Wwebpack from 'webpack';

class WebpackConfigBuilder {
    private config: Configuration = {};
    
    // 环境配置
    setEnvironment(env: 'development' | 'production'): this {
        this.config.mode = env;
        return this;
    }
    
    // 配置代码分割
    setCodeSplitting(strategy: 'static' | 'dynamic' | 'manual'): this {
        switch (strategy) {
            case 'static':
                this.config.optimization = {
                    ...this.config.optimization,
                    splitChunks: {
                        chunks: 'all',
                        cacheGroups: {
                            vendor: {
                                test: /[\\/]node_modules[\\/]/,
                                name: 'vendors',
                                chunks: 'all',
                            },
                            common: {
                                name: 'common',
                                minChunks: 2,
                                chunks: 'all',
                            },
                        },
                    },
                };
                break;
                
            case 'dynamic':
                this.config.optimization = {
                    ...this.config.optimization,
                    splitChunks: {
                        chunks: 'async',
                        maxSize: 200000,
                    },
                };
                break;
                
            case 'manual':
                this.config.entry = {
                    main: './src/index.tsx',
                    vendor: ['react', 'react-dom'],
                };
                break;
        }
        return this;
    }
    
    // 配置压缩
    setCompression(enable: boolean): this {
        if (enable) {
            this.config.plugins = [
                ...(this.config.plugins || []),
                new CompressionPlugin({
                    algorithm: 'gzip',
                    test: /\.(js|css|html|svg)$/,
                    threshold: 8192,
                    minRatio: 0.8,
                }),
            ];
        }
        return this;
    }
    
    // 配置包分析
    setBundleAnalysis(enable: boolean): this {
        if (enable) {
            this.config.plugins = [
                ...(this.config.plugins || []),
                new BundleAnalyzerPlugin({
                    analyzerMode: 'static',
                    openAnalyzer: false,
                    reportFilename: 'bundle-report.html',
                }),
            ];
        }
        return this;
    }
    
    // 配置 PWA
    setPWA(pwaConfig: PWAConfig): this {
        if (pwaConfig.enabled) {
            const WorkboxPlugin = require('workbox-webpack-plugin');
            
            this.config.plugins = [
                ...(this.config.plugins || []),
                new WorkboxPlugin.GenerateSW({
                    clientsClaim: true,
                    skipWaiting: true,
                    navigateFallback: '/index.html',
                    runtimeCaching: pwaConfig.caching || [],
                }
            ];
        }
        return this;
    }
    
    // 配置微前端
    setMicroFrontend(config: MicroFrontendConfig): this {
        const ModuleFederationPlugin = require('@module-federation/webpack');
        
        this.config.plugins = [
            ...(this.config.plugins || []),
            new ModuleFederationPlugin({
                name: config.name,
                filename: 'remoteEntry.js',
                exposes: config.exposes || {},
                remotes: config.remotes || {},
                shared: config.shared || {},
            }),
        ];
        
        this.config.experiments = {
            ...this.config.experiments,
            topLevelAwait: true,
        };
        
        return this;
    }
    
    // 配置 Web Workers
    setWebWorkers(workerConfig: WorkerConfig): this {
        if (workerConfig.enabled) {
            this.config.module = {
                ...this.config.module,
                rules: {
                    ...this.config.module?.rules,
                    worker: {
                        test: /\.worker\.ts$/,
                        use: {
                            loader: 'worker-loader',
                            options: workerConfig.options,
                        },
                    },
                },
            };
        }
        return this;
    }
    
    // 构建最终配置
    build(): Configuration {
        return this.config;
    }
}

interface PWAConfig {
    enabled: boolean;
    caching?: Array<{
        urlPattern: RegExp;
        handler: string;
        options?: any;
    }>;
}

interface MicroFrontendConfig {
    name: string;
    exposes?: Record<string, string>;
    remotes?: Record<string, string>;
    shared?: Record<string, any>;
}

interface WorkerConfig {
    enabled: boolean;
    options?: {
        name?: string;
        inline?: boolean;
        fallback?: boolean;
    };
}

// 使用方法
const webpackConfig = new WebpackConfigBuilder()
    .setEnvironment('production')
    .setCodeSplitting('static')
    .setCompression(true)
    .setBundleAnalysis(true)
    .setPWA({
        enabled: true,
        caching: [
            {
                urlPattern: /\.(?:png|jpg|jpeg|svg)$/,
                handler: 'CacheFirst',
            },
        ],
    })
    .setMicroFrontend({
        name: 'host',
        exposes: {},
        remotes: {
            auth: 'auth@http://localhost:3001/remoteEntry.js',
        },
        shared: {
            react: { singleton: true },
            'react-dom': { singleton: true },
        },
    })
    .build();
```

## 🚀 Vite + TypeScript 配置

### 🔄 现代化 Vite 配置

```typescript
// vite.config.ts
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';
import { resolve } from 'path';
import { visualizer } from 'rollup-plugin-visualizer';
import viteCompression from 'vite-plugin-compression';

export default defineConfig(({ command, mode }) => {
    // 加载环境变量
    const env = loadEnv(mode, process.cwd(), '');
    
    const isDev = command === 'serve';
    const isProd = command === 'build';
    
    return {
        // 插件配置
        plugins: [
            react({
                babel: {
                    plugins: [
                        [
                            '@babel/plugin-transform-runtime',
                            {
                                regenerator: true,
                            },
                        ],
                    ],
                },
            }),
            
            // TypeScript 路径别名支持
            tsconfigPaths(),
            
            // 包分析插件
            ...(isProd ? [
                visualizer({
                    filename: 'dist/stats.html',
                    open: false,
                    gzipSize: true,
                }),
            ] : []),
            
            // 压缩插件
            ...(isProd ? [
                viteCompression({
                    verbose: true,
                    disable: false,
                    threshold: 10240,
                    algorithm: 'gzip',
                    ext: '.gz',
                }),
            ] : []),
        ],
        
        // 路径别名
        resolve: {
            alias: {
                '@': resolve(__dirname, 'src'),
                '@components': resolve(__dirname, 'src/components'),
                '@pages': resolve(__dirname, 'src/pages'),
                '@hooks': resolve(__dirname, 'src/hooks'),
                '@services': resolve(__dirname, 'src/services'),
                '@utils': resolve(__dirname, 'src/utils'),
                '@types': resolve(__dirname, 'src/types'),
                '@assets': resolve(__dirname, 'src/assets'),
                '@styles': resolve(__dirname, 'src/styles'),
            },
        },
        
        // 开发服务器配置
        server: {
            port: 3000,
            open: true,
            proxy: {
                '/api': {
                    target: env.VITE_API_BASE_URL || 'http://localhost:8000',
                    changeOrigin: true,
                    rewrite: (path) => path.replace(/^\/api/, ''),
                },
            },
            hmr: {
                overlay: true,
            },
        },
        
        // 构建配置
        build: {
            target: 'es2020',
            outDir: 'dist',
            sourcemap: isProd,
            rollupOptions: {
                output: {
                    manualChunks: {
                        vendor: ['react', 'react-dom'],
                        router: ['react-router-dom'],
                        ui: ['@myorg/ui-components'],
                    },
                },
                external: (id) => {
                    // 排除不需要打包的依赖
                    if (id.includes('node_modules/')) {
                        return false;
                    }
                    return false;
                },
            },
            chunkSizeWarningLimit: 1000,
            minify: 'terser',
            terserOptions: {
                compress: {
                    drop_console: isProd,
                    drop_debugger: isProd,
                },
            },
        },
        
        // CSS 配置
        css: {
            preprocessorOptions: {
                scss: {
                    additionalData: `@import "@/styles/variables.scss";`,
                },
                less: {
                    modifyVars: {
                        '@primary-color': '#1890ff',
                    },
                },
            },
            modules: {
                localsConvention: 'camelCase',
                generateScopedName: isDev 
                    ? '[name]__[local]__[hash:base64:5]'
                    : '[hash:base64:8]',
            },
        },
        
        // 优化配置
        optimizeDeps: {
            include: [
                'react',
                'react-dom',
                'react-router-dom',
                '@myorg/ui-components',
            ],
            exclude: ['@myorg/dynamic-modules'],
        },
        
        // 环境变量前缀
        envPrefix: 'VITE_',
        
        // 依赖预构建
        prebuild: {
            dependenciesCleanup: false,
        },
    };
});
```

### 🎯 Vite 插件开发

```typescript
// vite.plugin.custom.ts
import { Plugin } from 'vite';
import { transform } from '@babel/core';
import fs from 'fs-extra';
import path from 'path';

interface CustomPluginOptions {
    targetDir?: string;
    includeHotReload?: boolean;
    generateTypes?: boolean;
}

export function customTypeScriptPlugin(options: CustomPluginOptions = {}): Plugin {
    const {
        targetDir = 'dist',
        includeHotReload = true,
        generateTypes = true,
    } = options;
    
    return {
        name: 'custom-typescript-plugin',
        configureServer(server) {
            // 开发服务器配置
            if (includeHotReload) {
                server.middlewares.use('/hmr', (req, res, next) => {
                    // 自定义 HMR 逻辑
                    next();
                });
            }
        },
        
        async buildStart() {
            // 构建开始时执行
            if (generateTypes) {
                await this.generateTypeDeclarations();
            }
        },
        
        async transform(code, id) {
            // TypeScript 文件自定义转换
            if (id.endsWith('.ts') || id.endsWith('.tsx')) {
                try {
                    // Babel 转换
                    const result = await transform(code, {
                        filename: id,
                        presets: [
                            ['@babel/preset-env', { targets: { node: '14' } }],
                            '@babel/preset-react',
                            '@babel/preset-typescript',
                        ],
                        plugins: [
                            '@babel/plugin-proposal-decorators',
                            '@babel/plugin-proposal-class-properties',
                        ],
                    });
                    
                    return {
                        code: result?.code || code,
                        map: result?.map,
                    };
                } catch (error) {
                    this.error(`Transform error: ${error.message}`);
                }
            }
            
            return null;
        },
        
        async generateBundle(options, bundle) {
            // Bundle 生成后处理
            for (const [fileName, chunk] of Object.entries(bundle)) {
                if (chunk.type === 'chunk' && chunk.isEntry) {
                    // 对入口 chunk 进行后处理
                    await this.processEntryChunk(fileName, chunk);
                }
            }
            
            // 生成自定义元数据
            this.emitFile({
                type: 'asset',
                fileName: 'metadata.json',
                source: JSON.stringify({
                    buildTime: new Date().toISOString(),
                    version: this.getVersion(),
                    chunks: Object.keys(bundle).length,
                }, null, 2),
            });
        },
        
        async generateTypeDeclarations() {
            // 生成类型声明文件
            const typeFiles = await this.getTypeFiles();
            
            for (const file of typeFiles) {
                const content = await fs.readFile(file, 'utf-8');
                const declarations = this.extractDeclarations(content);
                
                const outputPath = path.join(targetDir, 'types', path.basename(file, path.extname(file)) + '.d.ts');
                await fs.ensureDir(path.dirname(outputPath));
                await fs.writeFile(outputPath, declarations.join('\n'));
            }
        },
        
        getTypeFiles(): Promise<string[]> {
            // 查找类型文件
            return fs.glob('src/**/*.ts', { ignore: 'src/**/*.test.ts' });
        },
        
        extractDeclarations(content: string): string[] {
            // 提取声明内容
            const declarations = [];
            
            // 简单的声明提取 (实际实现会更复杂)
            const exportMatches = content.match(/export\s+[\w\s]+\s+[\w]+/g);
            if (exportMatches) {
                declarations.push(...exportMatches);
            }
            
            return declarations;
        },
        
        processEntryChunk(fileName: string, chunk: any) {
            // 处理入口 chunk
            console.log(`Processing entry chunk: ${fileName}`);
            
            // 可以在这里添加自定义的代码注入、转换等逻辑
            return chunk;
        },
        
        getVersion(): string {
            // 获取版本信息
            try {
                const packageJson = require('../package.json');
                return packageJson.version;
            } catch {
                return '1.0.0';
            }
        },
    };
}

// 使用自定义插件
export const viteWithCustomPlugin = defineConfig({
    plugins: [
        customTypeScriptPlugin({
            targetDir: 'dist',
            includeHotReload: true,
            generateTypes: true,
        }),
    ],
});
```

## 📚 Rollup + TypeScript 配置

### 🔧 现代化 Rollup 构建

```typescript
// rollup.config.ts
import { RollupOptions } from 'rollup';
import { NodeResolve } from '@rollup/plugin-node-resolve';
import typescript from '@rollup/plugin-typescript';
import commonjs from '@rollup/plugin-commonjs';
import json from '@rollup/plugin-json';
import terser from '@rollup/plugin-terser';
import dts from 'rollup-plugin-dts';

const isDev = process.env.NODE_ENV === 'development';
const isProd = !isDev;

const basePlugins = [
    NodeResolve({
        browser: true,
        preferBuiltins: false,
    }),
    commonjs(),
    json(),
    typescript({
        tsconfig: './tsconfig.json',
        declaration: true,
        declarationDir: 'dist/types',
        outDir: 'dist',
        exclude: ['**/*.test.ts', '**/*.spec.ts'],
    }),
];

const plugins = isProd 
    ? [...basePlugins, terser()]
    : basePlugins;

const configs: RollupOptions[] = [
    // ESM 构建
    {
        input: 'src/index.ts',
        output: {
            file: 'dist/index.esm.js',
            format: 'esm',
            sourcemap: true,
        },
        external: ['react', 'react-dom'],
        plugins,
    },
    
    // CJS 构建
    {
        input: 'src/index.ts',
        output: {
            file: 'dist/index.cjs.js',
            format: 'cjs',
            sourcemap: true,
            exports: 'named',
        },
        external: ['react', 'react-dom'],
        plugins,
    },
    
    // UMD 构建
    {
        input: 'src/index.ts',
        output: {
            file: 'dist/index.umd.json',
            format: 'umd',
            name: 'MyLibrary',
            sourcemap: true,
            globals: {
                react: 'React',
                'react-dom': 'ReactDOM',
            },
        },
        plugins,
    },
    
    // 类型声明文件构建
    {
        input: 'src/index.ts',
        output: {
            file: 'dist/index.d.ts',
            format: 'esm',
        },
        external: ['react', 'react-dom'],
        plugins: [
            dts({
                respectExternal: true,
            }),
        ],
    },
];

export default configs;
```

### 🔗 相关深入学习

- [[01-tsconfig-json大师级配置]] - TypeScript 核心配置
- [[02-Production优化策略]] - 生产环境优化
- [[03-Multi-project多项目管理]] - 多项目构建协调

---
*💡 现代化的构建工具链是 TypeScript 项目成功的基础，掌握不同工具的配置和优化是提升开发效率的关键*
