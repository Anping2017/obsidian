---
title: Odoo 电子发票
type: concept
tags: [erp, mature]
sources: [raw/Odoo/]
created: 2026-05-05
updated: 2026-05-05
summary: Odoo 电子发票(e-invoicing)集成多国税务局直连接口,生成符合 UBL/Factur-X/PEPPOL 等标准的 XML/PDF/A-3 格式电子发票,实现签发、送达、归档全流程合规自动化。
---

# Odoo 电子发票

## 定义

Odoo **电子发票(Electronic Invoicing / e-Invoicing)** 是符合各国税务局电子化要求的发票自动生成、签发、送达、归档系统。它将 Odoo 内的发票数据转化为**法定电子格式**(欧盟 UBL 2.1、法国 Factur-X、意大利 FatturaPA、PEPPOL BIS、墨西哥 CFDI 等),并通过税务局或 PEPPOL 网络送达买方,完成从开票到税务报送的全自动化。

## 核心要点

**多国合规标准**

| 国家 / 地区 | 标准 | 要求 |
|---|---|---|
| 欧盟 | UBL 2.1 / EN 16931 | 跨境电子发票通用 |
| 法国 | Factur-X(混合 PDF/XML) | 2024 起强制 B2B |
| 意大利 | FatturaPA | 2019 起 B2B/B2G 强制 |
| 西班牙 | Facturae / SII | 实时税务报告 |
| 墨西哥 | CFDI 4.0 | SAT 在线签发 |
| 智利 | DTE | SII 直连 |
| 印度 | IRN / GSTN | 政府发票登记号 |
| 沙特 | ZATCA Phase 2 | 二维码 + 加密 |
| 中国大陆 | 数电票 | 全电发票通过税局直连 |

**发票格式三大类**

1. **结构化 XML**:可机读,内容标准化(UBL、CFDI、FatturaPA)
2. **混合 PDF/XML**:PDF 内嵌 XML,人机两可读(Factur-X、ZUGFeRD)
3. **传统 PDF + 旁路 XML**:PDF 给人看,XML 单独传税局

**Odoo 发送通道**

1. **PEPPOL 网络**:欧洲电子发票公共网络,买卖双方都接入 PEPPOL access point 即可互通
2. **税务局直连**:通过 API 把发票上传税局,税局返回签发号(意大利 SDI、印度 IRP)
3. **邮件 / 门户**:通过电邮 / 客户门户发 PDF + XML
4. **第三方平台**:Tradeshift、Basware、Coupa 等 B2B 网络

**Odoo 实现**

- **核心模块** `account_edi`:统一 EDI 框架
- **国家本地化** `l10n_xx_edi`:各国本地化(l10n_es_edi、l10n_it_edi、l10n_mx_edi)
- 发票发送时自动调用对应通道,记录回执
- 收票方:Odoo 自动解析 PEPPOL / 邮件中的 XML,生成对应供应商账单

**签名与法律效力**

- 多数国家要求**电子签名**(基于 X.509 证书)
- 签名嵌入 XML / PDF,确保不被篡改
- Odoo 通过本地化模块或第三方 KYC 服务集成证书
- 归档:法律要求 7-10 年,Odoo 提供归档存储

**与传统发票的差异**

- 传统:开票 → 打印 → 邮寄 → 客户录入 → 税务核对
- 电子:开票 → 一键发送 → 客户系统自动接收 → 税局自动核对
- 时延从天级降至分钟级,错误率下降,合规风险降低

## 与其他概念的关系

电子发票是 Odoo Accounting 模块的合规延伸,与 [[Odoo电子签名]] 配合实现"全数字单据流"。涉及 [[Odoo工作流]] 中发票确认动作触发 EDI 发送、[[Odoo多公司架构]] 不同国家公司各自合规。

## 高频陷阱

- 各国格式互不兼容,跨境发票需双重本地化
- 证书过期会导致签名失败,需提前续期
- PEPPOL 接入需企业 Peppol ID(参与号)
- 时区问题:发票日期与税务报送日的对齐
- 数电票(中国)与传统增值税专用发票并存,过渡期复杂

## 参考源

- raw/Odoo/(电子发票章节)
- 相关:[[Odoo工作流]]、[[Odoo多公司架构]]、[[Odoo电子签名]]
