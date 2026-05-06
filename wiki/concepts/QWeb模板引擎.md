---
title: QWeb 模板引擎
type: concept
tags: [erp, mature]
sources: [raw/Odoo/03-应用实践层/03-报表开发/QWeb报表定制.md, raw/Odoo/03-应用实践层/02-视图开发/自定义视图组件.md]
created: 2026-05-05
updated: 2026-05-05
summary: QWeb 是 Odoo 自研的基于 XML 的模板引擎,既用于服务端渲染报表/网站,也用于客户端 OWL 组件,通过 t- 前缀指令实现循环、条件、表达式。
---

# QWeb 模板引擎

## 定义

QWeb 是 Odoo 自研的 XML 模板引擎。"Q" 来自 OpenObject 时代的 quick web。它的独特之处在于 **同一套语法既跑服务端(Python)又跑客户端(JavaScript)**:服务端用于生成 PDF 报表、网站静态页;客户端用于 OWL 组件渲染。这是 [[Odoo模块体系]]"全栈一致性"的关键。

## 核心要点

### 语法基础

所有指令都以 `t-` 前缀,放在元素属性上:

```xml
<div t-if="user.is_admin">
    <ul>
        <t t-foreach="orders" t-as="o">
            <li>
                <span t-esc="o.name"/>
                <span t-field="o.amount_total"/>
            </li>
        </t>
    </ul>
</div>
```

### 关键指令

| 指令 | 作用 |
|---|---|
| `t-if`, `t-elif`, `t-else` | 条件渲染 |
| `t-foreach`, `t-as`, `t-index`, `t-first`, `t-last` | 循环 |
| `t-esc` | 输出 Python/JS 表达式(转义) |
| `t-raw` | 输出原始 HTML(慎用) |
| `t-field` | 字段输出,**自动格式化**(货币、日期、HTML 字段) |
| `t-att-X` | 动态属性,如 `t-att-class="'red' if x else 'green'"` |
| `t-call` | 调用其他模板,可传参 |
| `t-set` | 局部变量 |
| `t-options` | 给字段输出加选项 |

### 服务端与客户端差异

- **服务端 QWeb**(Python):用于报表 PDF、网站静态页、邮件模板。表达式按 Python 语法。
- **客户端 QWeb**(JavaScript):用于 OWL 组件、看板视图自定义模板。表达式按 JS 语法。

90% 的指令两边相同,但 `t-on-click="onClick"` 这类事件绑定只存在于客户端。

### 与 Jinja/EJS/Mustache 的对比

| 维度 | QWeb | Jinja2 | Mustache |
|---|---|---|---|
| 载体 | XML 元素属性 | `{% %}`/`{{ }}` | `{{ }}` |
| 双端共用 | ✓(Py+JS) | ✗(Py only) | ✓ |
| 设计哲学 | 显式属性 | 宏块语法 | 逻辑无关 |

QWeb 的设计代价是 **XML 严格性**——任何标签必须闭合,这让 IDE 校验更容易,但写起来比模板字符串更啰嗦。

### 与视图渲染的关系

[[Odoo视图体系]] 中的 form/tree/kanban 视图本质上也是 QWeb 模板。Kanban 看板尤其明显:

```xml
<kanban>
    <templates>
        <t t-name="kanban-box">
            <div class="oe_kanban_card">
                <field name="name"/>
                <span t-if="record.state.raw_value == 'draft'" class="badge">草稿</span>
            </div>
        </t>
    </templates>
</kanban>
```

### 网站模板

`website` 模块用 QWeb 定义页面模板。任何用户在前台改动布局,都被存为 QWeb 模板的扩展记录,这种"代码 vs 数据库存储"的双轨制是 Odoo Website Builder 的基础。

## 关系

- 是 [[Odoo报表引擎]] 的模板层
- 是 [[Odoo视图体系]] kanban/website 视图的渲染基础
- 客户端 QWeb 与 OWL 框架协同(参考 [[Odoo模块体系]])

## 参考源

- raw/Odoo/03-应用实践层/03-报表开发/QWeb报表定制.md
- raw/Odoo/03-应用实践层/02-视图开发/自定义视图组件.md
