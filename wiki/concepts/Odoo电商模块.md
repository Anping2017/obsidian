---
title: Odoo 电商模块
type: concept
tags: [odoo, mature]
sources: [raw/Odoo/]
created: 2026-05-05
updated: 2026-05-05
summary: Odoo 电商模块(Website + eCommerce + Sale)把建站、商品、购物车、订单、支付、配送、库存、CRM 整合在同一系统,核心优势是 ERP-原生数据流通,劣势是高定制化场景受限。
---

# Odoo 电商模块

## 定义

Odoo 电商是 Odoo 在 Website 模块基础上的电商扩展,把网站建设(Website Builder)、商品管理(Product)、购物车与结账(eCommerce)、订单(Sale)、库存(Inventory)、配送(Delivery)、发票(Accounting)整合在同一 ERP 内。

它的产品定位介于 Shopify(独立电商 SaaS)和 Magento(开源专业电商)之间,**主要卖点是与企业 ERP 数据原生打通**——网站订单直接成为 ERP 中的销售订单,库存自动联动,客户即 CRM 中的联系人,无需 API 集成或数据同步。

## 核心模块

**Website Builder**

- 拖拽式页面构建(无需代码)
- 50+ 内置 Block(标题、文字、图片、CTA、视频)
- 主题市场(免费 + 付费)
- 响应式设计
- SEO 工具(meta、sitemap、structured data)
- 多语言

**eCommerce(电商核心)**

- 产品目录、分类、属性、变体
- 价格表(Price List)按客户/地区/数量分级
- 折扣、优惠券、促销活动
- 购物车、结账流程
- 客户账户(Wishlist、Past Orders)
- 评论与评分

**Sale 销售订单**

- 网站订单自动转销售订单
- 报价、订单确认、发货、开票
- 销售员、客户分配

**Inventory 库存**

- 实时库存查询(Avail. on Web)
- 库存路由(Receipt、Internal Transfer、Delivery)
- 多仓库

**Payment 支付**

- 多支付提供商:Stripe、PayPal、Adyen、支付宝、微信支付、Asiapay
- 支付方式:卡、钱包、银行转账、货到付款、Apple Pay/Google Pay

**Delivery 配送**

- 集成主流物流:DHL、FedEx、UPS、USPS、SF Express、邮政
- 实时计算运费(API 询价)
- 派送跟踪号自动同步给客户

## 与 Shopify/Magento 对比

| 维度 | Odoo | Shopify | Magento |
|---|---|---|---|
| 部署 | 自主 / Odoo.sh / 服务商 | SaaS 单一 | 自主 / Adobe Cloud |
| ERP 集成 | 原生 | 通过 API | 通过 API |
| 定制 | Python 模块 | Liquid 模板 + App | PHP/PHTML 模板 |
| 学习曲线 | 中(需懂 Odoo) | 低 | 高 |
| 大流量场景 | 中等 | 优 | 优 |
| 适用 | 已有 Odoo ERP 的企业 | DTC 独立站 | 中大型电商 |

## 业务集成案例

**B2C 直营**

中小企业用 Odoo 同时管财务、库存和电商网站,适合年订单量 < 100K 的场景。

**B2B 电商**

价格表分级、分仓、信用额度、报价审批等功能,Odoo 在 B2B 场景较强。

**Marketplace(单一卖家)**

不是真 marketplace,但可作多分类目录。多卖家平台需第三方模块(OCA marketplace)。

**O2O 与门店**

与 [[Odoo PoS销售点]] 集成,网订门取(BOPIS)、门店自提、库存共享。

## 多渠道场景

Odoo 电商可同时管理:
- B2C 网站
- B2B 网站(独立子站)
- 移动 App(API 集成)
- 多语言/多国家(每国一站,价格、税务自动)
- 第三方平台(Amazon、eBay、阿里巴巴)— 通过 OCA 模块或 API

## SEO 与 Marketing

**SEO**

- 自定义 URL slug
- meta title / description
- sitemap.xml 自动生成
- Schema.org structured data
- robots.txt
- 友好的 URL 结构

**Marketing 联动**

- Odoo Marketing Automation 自动化邮件营销
- 弃单提醒(Abandoned Cart)
- 推送通知(Web Push)
- A/B 测试(部分版本)
- Google Analytics、Tag Manager 集成

## 局限

- 高定制化场景:Liquid/Magento 主题市场更丰富,Odoo 模板较少
- 高并发:大流量电商需重度调优 Odoo Workers + DB
- 移动 App 体验:Odoo 自带网页 PWA,原生 App 需外购或自建
- 设计自由度:Website Builder 强但仍不及 Shopify 的设计师友好性
- 第三方扩展:Odoo App Store 比 Shopify App Store 数量少 10 倍以上

## 参考源

- raw/Odoo/
- 相关:[[Odoo模块体系]]、[[Odoo PoS销售点]]、[[Odoo Marketing Automation]]
