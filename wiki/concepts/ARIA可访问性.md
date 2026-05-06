---
title: ARIA 可访问性
type: concept
tags: [cs, web, frontend, accessibility, mature]
sources: [raw/计算机/开发学习/语言/HTML/03-实践深化层/可访问性与国际化/]
created: 2026-05-05
updated: 2026-05-05
summary: ARIA(Accessible Rich Internet Applications)是 W3C 一组 HTML 属性扩展,通过 role/aria-* 让屏幕阅读器理解动态 Web 应用,WCAG 是更广泛的可访问性标准。
---

# ARIA 可访问性

## 定义

**ARIA(Accessible Rich Internet Applications)** 是 W3C 的一组 HTML 属性扩展,让动态 Web 应用对辅助技术(屏幕阅读器、语音控制、开关设备)可访问。它是 [[HTML语义化]] 不足时的补丁:当原生 HTML 元素无法表达组件语义(如自定义下拉、tabs、modal),ARIA 通过 `role` `aria-*` 属性把语义注入。

## 核心要点

### 1. 第一原则:能用语义 HTML 就别用 ARIA

```html
<!-- 反例 -->
<div role="button" tabindex="0" onclick="...">Save</div>

<!-- 正例 -->
<button>Save</button>
```

`<button>` 自带 role=button、可聚焦、回车/空格触发、被表单提交,ARIA 替代品需手写所有这些行为且容易出错。

### 2. 三大类属性

#### Role(角色)

声明元素是什么:

```html
<div role="alert">操作失败</div>
<div role="dialog" aria-labelledby="title">...</div>
<ul role="tablist">
  <li role="tab" aria-selected="true">Tab 1</li>
</ul>
```

常见 role:button、checkbox、tab、tablist、tabpanel、dialog、alert、menu、tree、grid、status、progressbar...

#### Property(属性)

描述元素特性:

- `aria-label="Close"`:无可见文本时提供标签
- `aria-labelledby="id"`:引用其他元素文本
- `aria-describedby="id"`:补充说明
- `aria-required="true"`:必填
- `aria-disabled="true"`:禁用(同时改样式)

#### State(状态)

动态变化的信息:

- `aria-expanded="true/false"`:菜单展开
- `aria-hidden="true"`:对辅助技术隐藏
- `aria-checked="true/mixed/false"`:复选框状态
- `aria-busy="true"`:加载中
- `aria-current="page"`:当前页/项

### 3. Live Regions(动态通告)

```html
<div aria-live="polite">已自动保存</div>
<div aria-live="assertive">错误!请检查输入</div>
```

- `polite`:等当前朗读完再播
- `assertive`:打断立即朗读

适合:实时聊天、表单错误、加载完成通知。

### 4. WCAG(Web Content Accessibility Guidelines)

W3C 更广泛的标准,目前 WCAG 2.2(2023)。四原则(POUR):

1. **可感知(Perceivable)**:替代文本、字幕、对比度
2. **可操作(Operable)**:键盘可达、足够时间、避免发作内容
3. **可理解(Understandable)**:可读、可预测、避错纠错
4. **健壮(Robust)**:辅助技术兼容

合规级别:A(基础)、AA(主流目标)、AAA(最高,部分场景不实际)。

### 5. 键盘导航

- 所有交互可用 Tab/Shift+Tab/Enter/Space/Esc/箭头操作
- 焦点环不要 `outline: none`(或提供替代视觉)
- 跳转链接:`<a href="#main">Skip to content</a>` 顶部
- Modal 焦点陷阱(focus trap)

### 6. 颜色对比度

- 普通文本与背景对比 ≥ 4.5:1(AA)
- 大文本(18pt+ / 14pt 粗) ≥ 3:1
- UI 控件、图形 ≥ 3:1
- 工具:Chrome DevTools、axe、WebAIM Contrast Checker

### 7. 屏幕阅读器

- **NVDA**(Windows,免费)
- **JAWS**(Windows,商业)
- **VoiceOver**(macOS/iOS,内置)
- **TalkBack**(Android)

测试时关掉显示器闭眼操作,真正体验盲人用户视角。

### 8. 工具

- **axe DevTools**:浏览器扩展自动审计
- **Lighthouse**:Accessibility 评分
- **eslint-plugin-jsx-a11y**:React 静态检查
- **Storybook a11y addon**:组件级测试

### 9. 法律与商业

美国 ADA、欧盟 EAA(2025 年 6 月生效)要求 Web 可访问。Domino's、Beyoncé、Target 等都被起诉过。AA 合规非可选。

### 10. 真实数据

- 全球 ~15% 人口有某种残障
- 老龄化让需求更普遍
- 字幕受益人群远超听障(嘈杂环境、外语学习)
- 可访问性优化往往同时提升 SEO、UX、移动可用性

## 关系

- 基础:[[HTML语义化]]
- 配合:[[响应式设计]] 触摸目标 ≥ 44x44px
- 工具:axe、Lighthouse
- 法规:ADA / EAA / WCAG
- 收益:同时提升 [[Core Web Vitals]] 用户体验

## 参考源

- raw/计算机/开发学习/语言/HTML/03-实践深化层/可访问性与国际化/03-6 WCAG可访问性标准.md
- raw/计算机/开发学习/语言/HTML/03-实践深化层/可访问性与国际化/03-7 ARIA属性应用.md
- raw/计算机/开发学习/语言/HTML/03-实践深化层/可访问性与国际化/03-8 键盘导航设计.md
