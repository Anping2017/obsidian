---
title: Python元类
type: concept
tags: [cs, programming, mature]
sources: [raw/计算机/开发学习/语言/Python/02_认知层-核心概念与范式/2.1.5 元编程与动态特性.md]
created: 2026-05-05
updated: 2026-05-05
summary: 元类是"类的类",通过 metaclass 钩子在类被创建时改写其结构,是 Python 元编程最深的抽象层,常用于框架对类做声明式增强。
---

# Python元类

## 定义

在 Python 中,**类本身也是对象**;创建类的"类"称为**元类(Metaclass)**。默认元类是 `type`——`class Foo: ...` 等价于 `Foo = type('Foo', (object,), {...})`。通过自定义元类可以在类被定义时拦截、检查或改写其属性、方法、基类。

## 核心要点

- **类创建过程**:解释器执行类体得到 namespace 字典 → 调用 `metaclass(name, bases, namespace)` 生成类对象。
- **三个钩子**
  - `__init_subclass__`(类方法):子类被定义时调用,大多数场景已够用,无需写元类。
  - `__set_name__`(描述器协议):描述器知道自己被绑到哪个属性名。
  - 自定义 `metaclass`:重写 `__new__`/`__init__`/`__call__` 改写创建/实例化语义。
- **常用模式**
  - 注册表(自动登记子类到全局表)。
  - ORM 字段声明式映射(SQLAlchemy、Django Model、Pydantic)。
  - 接口/抽象基类(`abc.ABCMeta`)。
  - 单例与不可变类。
- **冲突规则**:多继承时所有基类元类必须兼容(线性化合一),否则抛 `TypeError`。
- **使用建议**:Tim Peters 名言"如果你需要问是否要用元类,就不需要"——优先用装饰器、`__init_subclass__`、描述器。

## 关系

- 与 [[Python装饰器]]:类装饰器与元类有重叠用途;装饰器更轻量,元类影响所有子类。
- 与 [[面向对象编程]] 的 MRO/多态机制深度耦合。
- 在 [[设计模式]] 中,元类常用于实现工厂、注册表、单例等创建型模式。
- ORM(SQLAlchemy、Django、[[Odoo ORM]])用元类把字段类属性转化为表列定义。
- 与 [[Python GIL]] 无直接关系,但所有元类逻辑在导入期单线程执行,避免并发问题。
- 类似抽象在其他语言中较少见——Ruby 的 singleton class、Java 的 reflection 是部分类比。

## 参考源

- raw/计算机/开发学习/语言/Python/02_认知层-核心概念与范式/2.1.5 元编程与动态特性.md
- raw/计算机/开发学习/语言/Python/02_认知层-核心概念与范式/2.1.2 继承与MRO算法.md
