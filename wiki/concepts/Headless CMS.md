---
title: Headless CMS
type: concept
tags: [cs, web, stub]
sources: []
created: 2026-05-11
updated: 2026-05-11
summary: Headless CMS 把内容管理与前端渲染解耦,通过 API 供任意前端消费,是现代 Jamstack 与多端分发架构的核心组件。
---

# Headless CMS

## 定义

**Headless CMS** 是把"内容存储管理"与"前端呈现"完全解耦的内容管理系统。相比传统 CMS(如 WordPress)自带主题模板一体化,Headless CMS 只暴露内容 API(REST 或 GraphQL),让任意前端(网站、App、小程序、IoT 设备)通过 API 消费。

## 核心要点

- **API-first**:内容以结构化 JSON 输出,前端自由决定如何渲染
- **多端分发**:同一份内容供网页、App、AR/VR、语音助手等使用
- **前后端团队解耦**:内容编辑与前端工程并行
- **代表产品**:Contentful、Strapi、Sanity、Directus、Ghost(headless 模式)、WordPress REST 模式
- **典型架构**:Headless CMS + [[Next.js]] / [[React]] / [[Vue]] + [[CDN]] / [[Vercel 与 Netlify]]
- **权衡**:灵活性高但需自建前端;预览功能实现复杂;编辑体验不如传统 CMS 一站式

## 和其他概念的关系

- 是现代 Web 架构核心组件,常与 [[Jamstack]]、[[SSG]]、[[SSR]] 组合
- 数据出口通常是 [[RESTful API]] 或 [[GraphQL]]
- 与 [[微服务]] 架构哲学一脉相承(内容作为一种服务)
- 反向对比传统 CMS([[Laravel]] 内容模块、WordPress 一体化)

## 参考源

- 综合行业实践(Contentful/Strapi/Sanity 文档)
