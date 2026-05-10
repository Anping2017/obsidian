---
title: iOS 备份与恢复
type: concept
tags: [ios, mature]
sources: [raw/iPhone/]
created: 2026-05-05
updated: 2026-05-05
summary: iOS 备份分 iCloud 自动备份与本地(Mac/PC 加密)备份两套体系,前者增量、跨设备、需付费空间,后者完整、本地、可加密;恢复流程支持设置时迁移与全量回滚。
---

# iOS 备份与恢复

## 定义

iOS 备份与恢复(Backup & Restore)指把 iPhone / iPad 当前状态(应用数据、设置、健康记录、消息、相册)复制到 iCloud 或本地电脑,以便日后还原到同一设备或新设备。Apple 提供 **iCloud 备份** 与 **本地加密备份** 两套并行机制,各有覆盖范围与还原能力差异。

## 核心要点

**两种备份的对比**

| 维度 | iCloud 备份 | 本地(Mac/PC)备份 |
|---|---|---|
| 触发 | 自动(连 Wi-Fi + 充电 + 锁定) | 手动(连接电脑 + 启动 Finder/iTunes) |
| 存储位置 | Apple iCloud 服务器 | 本机硬盘 |
| 容量限制 | 5 GB 免费,需 iCloud+ 付费扩展 | 受本地硬盘限制 |
| 加密 | 始终加密(端到端不一定) | 需勾选"加密"(否则不含 Health/Keychain) |
| 备份内容差异 | 不含已 App Store 重下的 App 二进制 | 完整(理论可逆向还原) |
| 速度 | 受网络限制 | 取决于 USB / 电脑 |

**iCloud 备份的覆盖范围**

包含:
- 应用数据(App 沙盒里 NSUserDefaults / Documents)
- 设备设置 / 主屏布局 / 桌面壁纸
- iMessage / SMS / MMS(若开 iCloud 消息)
- 相机胶卷(若未单独开 iCloud 照片)
- 健康数据(若开 iCloud Health)
- HomeKit 配置
- 铃声、Visual Voicemail

不包含(因为这些已存于云):
- iCloud 邮件、联系人、日历、备忘录
- App Store 中的应用本体(还原时重新下载)
- Apple Music / iTunes 已购内容
- iCloud Drive 文件

**iCloud 备份的限制**

- 单台设备 5 GB 免费空间往往不够,iCloud 9.99 ¥/月可升级 50 GB
- 备份大小不等于设备占用;Apple 算"应用数据 + 照片"
- 备份失败常见因:Wi-Fi 不稳、空间不足、设备未充电

**本地加密备份的特殊性**

- 必须勾选"为本地备份加密"才包含:Health 数据、Keychain 密码、Wi-Fi 设置、网站历史、通话记录
- 加密密码忘记 = 备份不可恢复(无法找回)
- 加密备份还可恢复 Apple Watch 配对

**还原场景**

1. **新机迁移**:开机后选"从 iCloud 备份恢复"或"从 Mac/PC 备份恢复",或用"快速开始"近距离传输
2. **同设备回滚**:抹掉所有内容,重新走设置流程并恢复
3. **跨设备恢复**:旧 iPhone 备份还原到新 iPhone,大多数数据可迁移(部分 App 自身限制除外)

**快速开始(Quick Start)**

iOS 12.4+ 引入,支持两台 iPhone 近距离直连传输全部数据,无需先备份。前提两机均运行 iOS 12.4+,旧机靠近新机后弹窗确认。

## 与其他概念的关系

备份与恢复是 [[iCloud云服务]] 在设备层的核心应用之一,与 [[Apple生态系统]] 中"无缝迁移"哲学一致。涉及 [[iOS沙盒]] 数据范围、[[Apple Pay]]、[[HealthKit生态]] 等敏感数据隔离规则。也是 [[二手回收以旧换新]] 流程的关键步骤。

## 高频陷阱

- iCloud 备份不等于 iCloud 同步:备份是"快照",同步是"实时",两者覆盖内容不同
- 不开"加密本地备份"会丢失 Keychain / Health(很多人首次看不到 Health 还原原因在此)
- 5 GB 不够时不要盲目"删除旧备份",这等于丢失历史快照
- App 退订 / 已下架时无法重新从 App Store 拉,需在备份内事先保留 .ipa(高级用户)

## 参考源

- raw/iPhone/(备份恢复章节)
- 相关:[[iCloud云服务]]、[[Apple生态系统]]、[[iOS沙盒]]、[[二手回收以旧换新]]
