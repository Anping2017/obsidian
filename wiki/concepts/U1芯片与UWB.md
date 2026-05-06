---
title: U1 芯片与 UWB
type: concept
tags: [iphone, ios, mature]
sources: [raw/iPhone/iPhone知识体系/02-技术规格层/连接通信/]
created: 2026-05-05
updated: 2026-05-05
summary: U1/U2 是 Apple 自研的超宽带(UWB)芯片,在 iPhone 11 起搭载,提供厘米级方向定位与极低延迟通信,支撑 AirTag 精确查找、AirDrop 优先级、HomePod 接近交互。
---

# U1 芯片与 UWB

## 定义

U1 是 Apple 在 2019 年随 iPhone 11 引入的自研 UWB(超宽带,Ultra-Wideband)芯片,iPhone 15 Pro 起升级为 U2,进一步增强带宽与功耗效率。它使设备在数十厘米至数米范围内具备**厘米级精度方向定位**和**极低延迟数据交换**能力,是 Apple "空间感知"战略的核心硬件。

UWB 是一项相对小众但性能优异的无线技术,在 iPhone 出现前主要用于工业测距、室内导航。Apple 把它带入消费电子,推动了 UWB 标准化(FiRa Consortium)的快速发展。

## 工作原理

**超宽带射频**

UWB 利用 6.5-8 GHz 等极宽频带(>500 MHz),发射极短脉冲(纳秒级),通过测量信号往返时间(Two-Way Ranging)和到达角度(Angle of Arrival)计算距离与方向。

**与 Wi-Fi、Bluetooth 对比**

| 维度 | UWB | Wi-Fi | Bluetooth |
|---|---|---|---|
| 距离精度 | ±10 cm | 数米 | 数米 |
| 方向 | 有 | 无 | 无 |
| 数据率 | 很低 | 极高 | 中 |
| 功耗 | 极低 | 高 | 低 |
| 干扰 | 极低(低功率宽带) | 中 | 中 |

UWB 不是用来传数据的,而是用来"测距和定向"。

## 应用场景

**1. AirTag 精确查找(Precision Finding)**

最早也最经典的应用。iPhone 进入 AirTag 几米范围后,屏幕显示箭头方向 + 距离 + 振动反馈,用户像玩"冷热游戏"一样找到 AirTag。

**2. AirDrop 智能排序**

iPhone 15 Pro 起,把手机指向另一台 iPhone 自动把它排在 AirDrop 首选。

**3. HomePod 与 iPhone 互动**

iPhone 靠近 HomePod 时自动唤起音乐控制界面,根据距离动态显示信息密度。

**4. 数字车钥匙(Car Key)**

宝马、现代、起亚等部分车型支持 iPhone 作车钥匙,UWB 让"靠近车自动解锁、走开自动锁"成为可能,且可避免传统蓝牙的"中继攻击"(因 UWB 测距精确,无法被远距欺骗)。

**5. 数字 Home Key**

智能门锁(Aqara、Schlage)支持 UWB 数字钥匙,精确测距确保只在用户真在门外时解锁。

**6. Vision Pro 与 iPhone 协作**

Vision Pro 用 UWB 检测附近 Apple 设备位置。

**7. Find My Network 中的设备发现**

精确定位丢失的 iPhone、AirTag 在房间内的具体位置。

## U1 与 U2 的演进

**U1(2019,iPhone 11)**

- 首发,支持 Precision Finding、AirDrop 智能排序
- 功耗较高

**U2(2023,iPhone 15 Pro)**

- 工艺升级
- 范围提升 3 倍
- 功耗降低 50%
- 推动数字车钥匙、Vision Pro 等更多场景

## 标准与生态

**FiRa Consortium**

由 Apple、Samsung、NXP 等创立的 UWB 互操作标准组织,推动 UWB 在汽车、智能家居、零售、移动支付等领域的统一规范。

**与 Matter 协作**

Matter 设备未来将整合 UWB 用于"基于位置的自动化"——用户靠近设备时自动响应。

**安全应用前景**

UWB 测距的精确性使其成为防"中继攻击"的标准方案,可能逐步取代部分 NFC 与 Bluetooth Pay 场景。

## 与 Samsung、小米的对比

- Samsung Galaxy S21+:首款搭载 UWB 的安卓旗舰,与 SmartTag+ 配合
- 小米 / OPPO / Vivo 部分高端机型:陆续加入 UWB
- 汽车厂商(BMW、宝马、奔驰、福特):积极采用 UWB 数字车钥匙

## 参考源

- raw/iPhone/iPhone知识体系/02-技术规格层/连接通信/
- 相关:[[Find My网络]]、[[Apple生态系统]]、[[Apple Pay]]
