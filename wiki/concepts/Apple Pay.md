---
title: Apple Pay
type: concept
tags: [iphone, ios, mature]
sources: [raw/iPhone/iPhone知识体系/]
created: 2026-05-05
updated: 2026-05-05
summary: Apple Pay 是 Apple 2014 年推出的移动支付方案,基于 NFC + Secure Element + Token 化机制,在隐私和安全上比传统刷卡更优,改变了实体支付的交互模型。
---

# Apple Pay

## 定义

Apple Pay 是 Apple 在 2014 年随 iPhone 6 推出的移动支付平台,使 iPhone、Apple Watch 用户在线下 NFC POS 终端、App 内、Web 端结账,完成卡片支付。它的关键创新不在"用手机替代卡片",而在引入设备账号(DAN, Device Account Number)Token 化机制,把真实卡号永远不离开发卡行的安全边界。

技术实现依赖三个支柱:NFC 通信、Secure Element 安全芯片、生物识别认证([[Touch ID]] 或 [[Face ID]])。

## 工作原理

**Token 化(Tokenization)**

绑卡时不存储真实 PAN(Primary Account Number),而是从发卡行请求一个仅对该设备有效的 Device Account Number(DAN)。每次支付时:

1. iPhone 用 DAN 而非 PAN 与商户终端通信
2. 商户的支付网络识别 DAN 后向发卡行请求映射真实 PAN
3. 发卡行验证后授权交易,商户从未接触真实卡号

这意味着即便商户被入侵,黑客拿到的也是无价值的 DAN。

**动态 CVV / Cryptogram**

每次交易生成一次性密码(类似 EMV 芯片卡的密码),即便 DAN 泄露也无法重放。

**Secure Element**

DAN 与密钥存于 [[Secure Enclave]] 中独立的安全芯片(Secure Element),硬件隔离,iOS 主系统也无法读取。

**生物识别授权**

每次支付前必须 Face ID / Touch ID / 设备密码确认,丢失或失窃的手机无法被他人使用。

## 与传统刷卡的对比

| 维度 | 传统刷卡 | Apple Pay |
|---|---|---|
| 卡号传输 | 真实 PAN | DAN(Token) |
| 商户存储 | 可能存储真实卡号 | 永远不接触真实卡号 |
| 失窃风险 | 卡号 + CVV 可被刷 | 无生物识别无法支付 |
| 支付速度 | 插卡/磁条 + 签名/PIN | 接近瞬时 |
| 跨境兼容 | 各家网络 | EMVCo 标准,通用 |

## 服务延展

**Apple Cash**

Apple 与 Green Dot 合作的预付卡式钱包,用于 iMessage 转账(美国)。

**Apple Card**

2019 年 Apple 与 Goldman Sachs 合作推出的信用卡,无年费、按消费类别返现 1-3%、配套 iOS 钱包深度集成,后期 Apple 收回部分自营。

**Apple Pay Later**(2023 年发布,2024 年关闭)

四期分期,Apple 自营信贷;后被合作伙伴(Affirm 等)替代。

**Apple Cash Family**

家长为子女管理预付资金。

**Wallet App 整合**

除支付卡外,Wallet 也存储:登机牌、酒店钥匙、活动票、忠诚卡、学生证、车钥匙(Car Key)、家钥匙(Home Key)、ID(部分美国州的驾照)。

## 在不同市场的渗透

- 美国:渗透率最高,几乎所有大型零售商支持
- 欧洲:中等偏高,部分国家与本地银行联盟竞争
- 中国:与微信/支付宝双寡头共存,渗透率有限,主要用于地铁公交、Apple 生态内
- 日本:支持 Suica、ID、QUICPay 等本地交通与支付协议

## 监管与博弈

**欧盟反垄断**:2022-2024 年,欧盟以 Apple 限制其他第三方钱包访问 NFC API 为由提起反垄断诉讼,迫使 Apple 在 2024 开放 NFC 给第三方支付 App。

**银行卡组织博弈**:Apple 与 Visa、Mastercard、Amex 协商每笔交易抽 0.15% 手续费(美国市场),银行抗议但需迎合用户需求。

**数字身份扩展**:Apple 推动 Wallet 成为身份证件容器,挑战政府主导的数字身份方案。

## 参考源

- raw/iPhone/iPhone知识体系/
- 相关:[[Secure Enclave]]、[[Apple生态系统]]、[[Touch ID]]、[[Face ID]]
