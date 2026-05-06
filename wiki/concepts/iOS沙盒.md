---
title: iOS 沙盒
type: concept
tags: [iphone, ios, mature]
sources: [raw/iPhone/iPhone知识体系/]
created: 2026-05-05
updated: 2026-05-05
summary: iOS 沙盒(App Sandbox)是基于 BSD 内核安全机制的 App 隔离架构,每个 App 拥有独立文件系统视图、进程权限和数据空间,无法直接访问其他 App 数据,是 iOS 安全模型的根基。
---

# iOS 沙盒

## 定义

iOS 沙盒(App Sandbox)是 iOS 安全架构的核心,每个 App 安装后获得一个独立的、相互隔离的运行环境。它源自 macOS 的 App Sandbox(基于 Apple 早期 Seatbelt 技术),最终基于 BSD/Darwin 内核的 sandbox_init 系统调用。

沙盒不只是文件系统隔离,而是包含五个层次的全方位限制:
1. **文件系统隔离**:每 App 一个根目录,看不到其他 App 数据
2. **进程隔离**:不能向其他 App 进程发信号或注入代码
3. **资源访问限制**:相机、麦克风、定位、相册、通讯录都需用户授权
4. **网络访问**:可访问网络但需声明
5. **代码完整性(Code Signing)**:运行的二进制必须签名验证

这构成了 [[iOS隐私机制]] 的最底层基础设施。

## 沙盒目录结构

每个 App 在文件系统中有一个 Bundle Container 和一个 Data Container:

**Bundle Container**(只读)

- /Application.app/
  - 可执行二进制
  - 资源文件(图片、JSON、字体)
  - Info.plist 元数据

**Data Container**(可写)

- Documents/:用户文件,iTunes/Finder 可见,iCloud 备份
- Library/Application Support/:支持文件,iCloud 备份
- Library/Caches/:缓存,系统可清空
- Library/Preferences/:NSUserDefaults 数据
- tmp/:临时文件,系统可清空

每个 App 看到的文件系统是被"挂载"成只见自己的视图。

## 进程隔离

**MAC(Mandatory Access Control)**

iOS 用 BSD 强制访问控制 + Apple Sandbox 配置文件,内核拒绝进程访问其权限外的资源。

**禁止跨 App 进程通信(IPC)**

App 不能 fork、不能与其他 App 直接共享内存、不能发信号。跨 App 通信只能通过受控通道:
- URL Scheme(my-app://...)
- Universal Links
- App Extensions
- Shared App Group(显式声明)
- UIPasteboard(剪贴板)
- iCloud Drive 共享

## 资源访问授权

**首次访问触发权限弹窗**

- 相机、麦克风、定位、相册、通讯录、日历、提醒、HealthKit、HomeKit、Bluetooth、本地网络等
- 用户拒绝后 App 不能再次唤起,需手动设置中开启

**Info.plist 中预声明**

App 必须在 Info.plist 中预填用途字符串(NSCameraUsageDescription 等),否则 iOS 拒绝该 App 上架或功能崩溃。

**硬件后端授权**

部分 API 还需开发者账户启用 Capabilities(HealthKit、HomeKit、Push、CarPlay)。

## 后台执行限制

iOS 严格限制 App 后台运行,以保电量和性能:
- 默认后台立刻挂起
- 可申请有限后台模式:位置、音频播放、VoIP、Bluetooth 中央/外围、外部配件、后台 fetch、远程通知唤醒
- 后台 fetch 由系统决定何时调度,不可自定义频率
- 长后台计算请用 Background Task(限时几十秒)

## App Group(共享数据)

同一开发者的多个 App 可声明共同的 App Group,共享一个目录,实现 App 间数据共享:
- 主 App 与 Widget
- 主 App 与 Watch App
- 主 App 与 Action Extension

但 App Group 仍受同一开发者(Team ID)限制。

## 文件系统访问的解禁

**Files App + Document Provider**(iOS 11+)

允许用户主动让 App 访问 iCloud Drive、Files 中的文件。但 App 只能"被动接收"用户选择的文件,不能主动扫描。

**Photos Library 选择**(iOS 14+)

用户可选择"完全访问"或"仅访问选定照片",大幅缩小访问面。

**Local Network**(iOS 14+)

访问局域网内其他设备(Bonjour、HomeKit 之外)需独立授权。

## 沙盒与安全研究

沙盒是 iOS 防御未知攻击的核心。即使某个 App 被攻陷,攻击面也被限制在该 App 的沙盒内,不能横向感染系统其他部分。

**越狱(Jailbreak)**

越狱本质就是绕过沙盒和代码签名,获得 root 权限。Apple 与越狱社区的拉锯持续十多年,iOS 17+ 后越狱难度极高。

**Pegasus 等高危攻击**

像 NSO Pegasus 这类国家级监控软件需要利用 iOS 漏洞链(Lockdown Mode 减少攻击面)突破沙盒,Apple 持续打补丁。

## 与 Android 的对比

| 维度 | iOS 沙盒 | Android |
|---|---|---|
| 模型 | App Sandbox + Code Signing | UID 隔离(每 App 一个 Linux UID) |
| 文件系统 | 独立目录 | 独立目录 + 公共存储 |
| 跨 App 通信 | 受控通道 | Intents 较开放 |
| 侧载 | 默认禁止 | 默认允许 |
| 硬件权限 | 一次性弹窗 + 设置中开关 | 类似但 13+ 加细 |

iOS 沙盒模型整体更严,代价是开发自由度更低、企业内部应用更难。

## 参考源

- raw/iPhone/iPhone知识体系/
- 相关:[[iOS隐私机制]]、[[iOS系统架构]]、[[App Store 审核]]
