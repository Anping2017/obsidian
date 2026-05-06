---
title: HealthKit 生态
type: concept
tags: [iphone, ios, mature]
sources: [raw/iPhone/iPhone知识体系/]
created: 2026-05-05
updated: 2026-05-05
summary: HealthKit 是 iOS 2014 年引入的统一健康数据中枢,定义了 100+ 数据类型与权限模型,使设备、App、医疗机构在用户授权下交换健康数据,核心理念是"数据归用户"。
---

# HealthKit 生态

## 定义

HealthKit 是 Apple 于 iOS 8(2014)推出的健康数据框架与生态系统。其核心由三部分组成:
1. **HealthKit Framework**:iOS 系统级 API,所有健康类 App 通过它写入和读取数据
2. **Health App**:用户面向的中央仪表盘,聚合所有来源数据
3. **HealthKit 数据存储**:本地加密数据库,iCloud 端到端加密同步

它是 Apple 健康战略的基石,贯穿 [[Apple Watch]]、第三方健身设备、医疗机构、CareKit、ResearchKit。

## 数据模型

**100+ 内置数据类型**,覆盖:

- **生命体征**:心率、血压、血氧、呼吸率、皮肤温度、血糖
- **体能**:步数、距离、活动卡路里、训练时长、跑步力学指标
- **睡眠**:睡眠分期(清醒/浅睡/深睡/REM)、卧床时间
- **女性健康**:月经周期、症状、生育力
- **听力健康**:环境音量、耳机音量
- **心理健康**:状态记录、正念分钟数
- **营养**:水、咖啡因、营养素
- **临床数据**:实验室结果、用药、过敏、免疫记录(通过 FHIR 集成)

每条数据都有时间戳、单位、来源 App。

## 权限与隐私模型

**细粒度授权**

App 必须明确请求每种数据类型的"读"或"写"权限:
- 写权限:App 可写入数据
- 读权限:App 可读取数据
- 用户可在 Health App 中随时撤销

**只本地或端到端加密**

健康数据存储在 iPhone 本地或 iCloud 中,默认端到端加密(只有用户的 Apple ID 设备可解密),Apple 自身也无法读取。

**用户数据所有权**

数据导出为 XML/CDA 格式;迁移到新设备完整保留。

**与 ResearchKit 协作**

用户可主动捐赠数据给医学研究项目,严格匿名化。

## 数据来源

**Apple 设备**

- iPhone(自动:步数、行走稳定性、环境音量)
- Apple Watch(心率、运动、ECG、血氧、睡眠等数十项)
- AirPods Pro(听力健康)

**第三方设备**

- 智能体重秤(Withings、Garmin)
- 血糖仪(Dexcom、FreeStyle Libre)
- 血压计(Omron、QardioArm)
- 健身设备(Peloton、跑步机)

**第三方 App**

- 训练 App(Strava、Nike Run Club)
- 营养 App(MyFitnessPal、Lifesum)
- 冥想 App(Headspace、Calm)
- 女性健康 App(Clue、Flo)

**医疗机构**

通过 Health Records,把医院电子病历(检查结果、处方、过敏、免疫)直接同步到 iPhone(美国 800+ 医疗机构支持)。

## 核心特性

**Activity Rings**

三环理念:活动(Move)、运动(Exercise)、站立(Stand)——量化日常健康目标。

**Health Sharing**(2021+)

家人之间互相分享指定健康指标,长辈跌倒、心率异常时家人立刻收到通知。

**Mobility 移动指标**

行走稳定性、步态、心率变异性——长期趋势可揭示衰老迹象。

**Mental Wellbeing**

记录情绪状态,与 mindful minutes 配合形成心理健康闭环。

**听力健康**

环境噪音长期统计,警示噪声暴露;耳机音量管理。

## 临床合规

**FDA 与 CE 认证**

- 心率不齐通知(2018):FDA Class II 医疗设备认证
- ECG App:FDA 批准
- 房颤历史(AFib History):FDA 批准

**临床研究**

- Apple Heart Study(2017):40 万 + 用户参与心律研究
- Apple Women's Health Study、Hearing Study、Heart and Movement Study(持续中)

## 与谷歌 Fit / Health Connect 对比

- Apple HealthKit:严格端到端加密,数据分类详尽,设备生态封闭
- Google Health Connect(2022 替代 Google Fit):跨 App 数据中介,云同步默认 SP 加密但需用户授权

## 参考源

- raw/iPhone/iPhone知识体系/
- 相关:[[Apple Watch]]、[[iCloud云服务]]、[[Apple生态系统]]
