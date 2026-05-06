---
title: iCloud 云服务
type: concept
tags: [iphone, ios, mature]
sources: [raw/iPhone/iPhone知识体系/]
created: 2026-05-05
updated: 2026-05-05
summary: iCloud 是 Apple 的云服务平台,提供照片、文件、邮件、日历、通讯录、设备备份等的端云同步,5GB 起步免费,用 iCloud+ 订阅升级容量与隐私功能,是 Apple 生态粘性的关键支柱。
---

# iCloud 云服务

## 定义

iCloud 是 Apple 在 2011 年推出的云服务,继承自 MobileMe,逐步成长为 Apple 生态的"中枢神经"。它把用户的数据(照片、邮件、文档、备份、设置、健康数据等)同步到 Apple 的云端,使任何 Apple 设备登入同一 Apple ID 后即获得连贯的体验。

iCloud 不仅是存储服务,更是 Apple 软硬件一体战略的胶合剂——从 Continuity、AirDrop 到通用剪贴板、Find My,几乎所有跨设备协同特性背后都是 iCloud 在做账户与数据中转。

## 核心服务模块

**iCloud Photos**:照片与视频自动云同步,所有设备共享原图或缩略图(开"优化存储")

**iCloud Drive**:类似 Dropbox 的文件夹同步,iOS 文件 App 与 macOS Finder 中可见

**iCloud Backup**:iOS 设备每日自动备份(Wi-Fi + 充电时),包括 App 数据、设置、消息、HomeKit 配置等

**iCloud Mail**:@icloud.com 邮箱

**联系人/日历/提醒/备忘录**:全部端云同步

**Find My**:查找 iPhone、iPad、Mac、Watch、AirPods、AirTag,断网时也可通过临近 Apple 设备的 Find My 网络中转定位

**Keychain(钥匙串)**:跨设备同步密码、信用卡、Wi-Fi 凭据,端到端加密

**Health**:健康数据云同步(端到端加密)

**iMessage 与 FaceTime**:用 Apple ID 同步消息历史与未读状态

**家人共享(Family Sharing)**:最多 6 人共享 iCloud+ 容量、Apple 订阅、App 购买、定位

## 容量分级与 iCloud+

**免费层**:5GB(从 2011 年至今未变,引发持续批评)

**iCloud+ 付费层(自 2021 年)**:

- 50GB(¥6/月)
- 200GB(¥21/月)
- 2TB(¥68/月)
- 6TB / 12TB(2023 年新增,大家庭/创意工作者)

iCloud+ 同时附赠隐私功能:
- **隐私转发(iCloud Private Relay)**:类似 VPN,把 Safari 流量经两跳代理隐藏 IP
- **隐藏邮件(Hide My Email)**:自动生成匿名邮箱别名转发到真实邮箱
- **HomeKit 安全视频**:支持 5 个相机的端到端加密录像

## 隐私架构

**端到端加密(E2EE)**

并非所有数据都端到端加密——下列数据 E2EE,Apple 自己也无法访问:
- 钥匙串、健康数据、Home 数据、地图记录、Memoji、屏幕时间、Wi-Fi 密码、Siri 信息
- 高级数据保护(Advanced Data Protection,2022+):用户主动开启后,iCloud Backup、iCloud Drive、Photos、Notes、Reminders 等也升级为 E2EE

**未端到端加密**(默认)

- 邮件(SMTP 协议自身限制)
- 日历(为兼容 CalDAV 标准)
- 联系人(同上)

**与监管博弈**

- 高级数据保护让 Apple 即便面对法院传票也无法解密用户主数据,引发 FBI 等执法机构反对
- 中国大陆 iCloud 由"云上贵州"代运营,数据存放本地

## 在 Apple 生态中的角色

iCloud 是 Apple 生态护城河的隐形支柱:
- 用户数据"在云上"使迁移到安卓极为痛苦
- 多设备无缝体验吸引追加购买(iPhone → iPad → Mac → Watch)
- 与 [[Apple生态系统]] 的 Continuity、Handoff、AirDrop、Universal Clipboard 共同提供"一个账户,所有设备"体验

## 备份与恢复

**iCloud Backup**:Wi-Fi + 锁屏 + 充电三条件每日自动,新设备 Setup 时一键还原

**Finder 本地备份**:Mac 上插 USB-C 用 Finder(macOS Catalina+)或 iTunes(更早系统)做本地备份,可加密包括钥匙串、健康数据

**iCloud Backup vs Finder 本地备份**:

| 维度 | iCloud | 本地 |
|---|---|---|
| 触发 | 自动(Wi-Fi+充电) | 手动 |
| 速度 | 受网络限制 | 快 |
| 容量 | 受 iCloud 计划限制 | 受本地磁盘限 |
| 加密 | 默认服务端,可升 E2EE | 可选加密 |
| 包含范围 | 不含部分大数据(可独立同步) | 全部 |

## 参考源

- raw/iPhone/iPhone知识体系/
- 相关:[[Apple生态系统]]、[[iOS隐私机制]]、[[Find My网络]]
