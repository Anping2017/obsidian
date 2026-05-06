---
title: Find My 网络
type: concept
tags: [iphone, ios, mature]
sources: [raw/iPhone/iPhone知识体系/]
created: 2026-05-05
updated: 2026-05-05
summary: Find My 网络是 Apple 2019 年构建的众包定位系统,利用全球数十亿活跃 Apple 设备作为定位中转节点,使断网设备和 AirTag 也可被定位,核心创新是端到端加密的匿名众包定位。
---

# Find My 网络

## 定义

Find My 网络(Find My Network)是 Apple 在 2019 年(iOS 13)重构的设备查找服务,从原先的"在线设备主动报告位置"扩展为"利用所有 Apple 设备的蓝牙信号作为众包定位节点",使**离线、断网、关机的设备也能被定位**。

它的标志性产品是 [[AirTag]](2021 推出的小型物品追踪器),依靠全球数十亿 Apple 设备作为接力点,让一个无网络无电的小铁片也能被定位。

## 工作原理

**短距蓝牙信标(BLE Beacon)**

每台 Apple 设备(iPhone、iPad、Mac、AirPods、AirTag)持续广播加密的蓝牙信标,包含轮换的公钥。

**附近 Apple 设备中转**

任何路过的、开启 Find My 的 Apple 设备(陌生人也行),嗅到信标后:
1. 用信标公钥加密自己当时的 GPS 位置
2. 把加密包上传到 Apple 服务器
3. 服务器只看到密文,不知道是谁的位置

**所有者解密**

只有信标设备的所有者(其 iPhone、iPad)持有匹配私钥,从 Apple 服务器下载加密包并解密,看到自己设备最后位置。

**端到端加密**

Apple 自身全程不知道:谁在找谁、谁在哪里、谁帮谁中转。这与 Tile、Samsung SmartThings 等同类服务的隐私模型形成鲜明对比。

## 主要功能

**Find Devices(查找设备)**

iPhone、iPad、Mac、Watch、AirPods、AirTag、Apple Pencil 全部支持。地图显示位置,可:
- 播放声音定位
- 标记为丢失(Lost Mode)
- 远程擦除
- 通过附近 Apple 设备路过获取最新位置

**Find People(查找朋友)**

家人朋友相互分享位置,需双向授权。可设置临时(1 小时)或永久。可与"家人共享"绑定。

**Find Items(查找物品)**

AirTag、第三方 Find My 兼容产品(Chipolo、Pebblebee、自行车、手提箱)。

**精确查找(Precision Finding)**

使用 [[U1芯片与UWB]],iPhone 11+ 可对 AirTag 实现厘米级方向引导(箭头指向)。

## AirTag 隐私与安全

**反跟踪机制**

- 不属于你的 AirTag 跟随你超过 8-24 小时(随机延迟),你的 iPhone 收到通知
- 安卓用户也可下载 Tracker Detect App 扫描
- AirTag 离开主人 3 天后会发出声音

**与 Apple 设备配对绑定**

配对时需主人设备靠近,AirTag 与该 Apple ID 绑定。换主人需主人主动重置。

## 历史与监管

**初代 Find My iPhone(2010)**

仅在线设备可查,断网即失效。

**2019 重构**

引入众包网络与端到端加密。

**AirTag 发布(2021)**

引发隐私争议:小且便宜的追踪器被滥用于跟踪伴侣或盗窃。Apple 持续加固反跟踪机制。

**Detecting Unwanted Location Trackers(2024)**

Apple 与 Google 联合制定行业标准,跨平台检测各品牌追踪器。

## 与同类服务对比

| 维度 | Find My | Google Find My Device | Tile / SmartThings |
|---|---|---|---|
| 网络规模 | 十亿 + Apple 设备 | 数十亿安卓 | 千万级用户 |
| 隐私模型 | E2EE 众包 | E2EE 众包(2024+) | 集中式 |
| 离线定位 | 强 | 强 | 弱 |
| 跨平台 | 否(仅 Apple) | 仅 Android | iOS/Android |

## 参考源

- raw/iPhone/iPhone知识体系/
- 相关:[[Apple生态系统]]、[[iCloud云服务]]、[[U1芯片与UWB]]
